import os
import ndjson
import shutil
import subprocess
import hashlib
import ssdeep
import tlsh
import datetime
import io


def callSubprocessPopen(request, shellUse = False):
    if shellUse:
        p = subprocess.Popen(request, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p_status = p.wait()
    else:
        p = subprocess.Popen(request, stdout=subprocess.PIPE)
        (output, err) = p.communicate()
        p_status = p.wait()


def get_start_offset(disk_path):
    mmls = subprocess.Popen(["mmls", disk_path], stdout=subprocess.PIPE)
    cut = subprocess.Popen(["cut", "-c43-55"], stdout=subprocess.PIPE, stdin=mmls.stdout)
    output = cut.stdout.read()

    with io.StringIO() as f:
        f.write(output.decode().rstrip())
        f.seek(0)

        max = 0
        cp_max = 0
        cp = 0
        for line in f.readlines():
            try:
                if int(line) > max:
                    max = int(line)
                    cp_max = cp
            except:
                pass
            cp += 1

    mmls = subprocess.Popen(["mmls", disk_path], stdout=subprocess.PIPE)
    cut_start_offset = subprocess.Popen(["cut", "-c17-26"], stdout=subprocess.PIPE, stdin=mmls.stdout)
    output = cut_start_offset.stdout.read()

    with io.StringIO() as f:
        f.write(output.decode().rstrip())
        f.seek(0)

        return int(f.readlines()[cp_max].rstrip())




def get_all_hashes(vdi_folder, vm_path, vm_name, feeder_path, sysinfo_path):

    exportPath = os.path.join(feeder_path, vm_name)
    if not os.path.isdir(exportPath):
        os.mkdir(exportPath)

    ## Convert windows machine into raw format
    pathToConvert = os.path.join(vdi_folder, "convert")
    if not os.path.isdir(pathToConvert):
        os.mkdir(pathToConvert)
    convert_file = f"{pathToConvert}/{vm_name}.img"

    print("## Convertion ##")
    res = subprocess.call(["VBoxManage", "clonehd", vm_path, convert_file, "--format", "raw"])
    print("## Convertion Finish ##\n")

    ## create mount directory
    pathMnt = "./mnt_convert"
    if not os.path.isdir(pathMnt):
        os.mkdir(pathMnt)


    print("[+] Feed Hashlookup setup")
    
    ## mount the convert image
    print("\t[+] Mount")
    start_offset = get_start_offset(convert_file)
    request = f"sudo mount -o loop,ro,noexec,noload,offset=$((512*{start_offset})) {convert_file} {pathMnt}"
    callSubprocessPopen(request, True)

    intermediate_file = "./intermediate_file" 
    print("\t[+] List of all files")
    request = "find %s -type f > %s" % (pathMnt, intermediate_file)
    callSubprocessPopen(request, True)

    data = list()
    sysinfofile = open(sysinfo_path, "r")
    sysinfo = sysinfofile.readlines()
    sysinfofile.close()
    SysVersion = sysinfo[0].rstrip("\n")
    SysName = sysinfo[1].rstrip("\n")
    
    with open(intermediate_file, 'r') as read_file:
        for line in read_file.readlines():
            filename = os.path.normpath(line.rstrip("\n"))

            if not os.path.isdir(filename):
                try:                                
                    md5Glob = hashlib.md5(open(filename, 'rb').read()).hexdigest()
                    sha1Glob = hashlib.sha1(open(filename, 'rb').read()).hexdigest()
                    sha256Glob = hashlib.sha256(open(filename, 'rb').read()).hexdigest()
                    sha512Glob = hashlib.sha512(open(filename, 'rb').read()).hexdigest()
                    tlshGlob = tlsh.hash(open(filename, 'rb').read())
                    ssdeepGlob = ssdeep.hash(open(filename, 'rb').read())

                    l = line.split("/")
                    nameFile = ""
                    for inter in range(2,len(l)):
                        nameFile += l[inter] + "/"
                    nameFile = nameFile[:-1]

                    data.append(
                        {
                            'FileName': nameFile.rstrip("\n"),
                            'FileSize': str(os.path.getsize(filename)),
                            'Windows:Version': SysVersion,
                            'Windows:OS': SysName,
                            'md5': md5Glob,
                            'sha-1': sha1Glob,
                            'sha-256': sha256Glob,
                            'sha-512': sha512Glob,
                            'tlsh': tlshGlob,
                            'ssdeep': ssdeepGlob
                        }
                    )

                except OSError as err:
                    #print(err)
                    pass

    with open(f"{exportPath}/{vm_name}_{datetime.datetime.now().strftime('%Y%m%d')}.json", 'w') as outfile:
        ndjson.dump(data, outfile)

    os.remove(intermediate_file)

    ## umount the convert image
    print("\t[+] Umount")
    request = "sudo umount " + pathMnt
    callSubprocessPopen(request, True)

        
    ## Suppression of the current raw disk
    os.remove(convert_file)
    request = ["VBoxManage", "closemedium", "disk", convert_file, "--delete"]
    callSubprocessPopen(request)

    ## Suppression of mount folder
    try:
        shutil.rmtree(pathMnt)
    except:
        pass
    ## Suppression of mount folder
    try:
        shutil.rmtree(pathToConvert)
    except:
        pass