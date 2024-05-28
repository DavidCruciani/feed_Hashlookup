import os
import ndjson
import shutil
import subprocess
import hashlib
import ssdeep
import tlsh
import datetime
import io
import time
import poppy


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




def get_all_hashes(vdi_folder, vm_path, vm_name, feeder_path, sysinfo_path, bloom_filter_info):

    exportPath = os.path.join(feeder_path, vm_name)
    if not os.path.isdir(exportPath):
        os.mkdir(exportPath)

    if bloom_filter_info["active"]:
        if not os.path.isdir(bloom_filter_info["path"]):
            os.mkdir(bloom_filter_info["path"])
        bloom_filter_vm_path = os.path.join(bloom_filter_info["path"], f"{vm_name}.pop")
        global_bloom_filter_path = os.path.join(bloom_filter_info["path"], "global.pop")
        if not os.path.isfile(bloom_filter_vm_path):
            ## create bloom filter
            vm_bloom_filter = poppy.BloomFilter(bloom_filter_info["capacity"], bloom_filter_info["false_probability"])
            vm_bloom_filter.save(bloom_filter_vm_path)
        else:
            vm_bloom_filter = poppy.load(bloom_filter_vm_path)

        if not os.path.isfile(global_bloom_filter_path):
            global_bloom_filter = poppy.BloomFilter(50000000, bloom_filter_info["false_probability"])
            global_bloom_filter.save(global_bloom_filter_path)
        else:
            global_bloom_filter = poppy.load(global_bloom_filter_path)

        if vm_bloom_filter.is_full():
            print(f"[-] Bloom filter for {vm_name} is full...")
        if global_bloom_filter.is_full():
            print(f"[-] Global Bloom filter is full...")

    ## Convert windows machine into raw format
    pathToConvert = os.path.join(vdi_folder, "convert")
    if not os.path.isdir(pathToConvert):
        os.mkdir(pathToConvert)
    convert_file = f"{pathToConvert}/{vm_name}.img"

    print(f"## Conversion ## ({datetime.datetime.now()})")
    res = subprocess.run(["VBoxManage", "clonehd", vm_path, convert_file, "--format", "raw"], capture_output=True)
    print("...")
    while "Clone medium created in format" not in res.stdout.decode():
        print("[-] Conversion error... Retry in 30 sec")
        time.sleep(30)
        res = subprocess.run(["VBoxManage", "clonehd", vm_path, convert_file, "--format", "raw"], capture_output=True)
    print(f"## Conversion Finish ## ({datetime.datetime.now()}) \n")

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
                flag_bloom = False
                try:
                    sha256Glob = hashlib.sha256(open(filename, 'rb').read()).hexdigest()
                    if bloom_filter_info["active"]:
                        if vm_bloom_filter.contains_str(sha256Glob):
                            flag_bloom = True
                        else:
                            if not vm_bloom_filter.is_full():
                                vm_bloom_filter.insert_str(sha256Glob)
                        if global_bloom_filter.contains_str(sha256Glob):
                            flag_bloom = True
                        else:
                            if not global_bloom_filter.is_full():
                                global_bloom_filter.insert_str(sha256Glob)
                    if not flag_bloom:
                        md5Glob = hashlib.md5(open(filename, 'rb').read()).hexdigest()
                        sha1Glob = hashlib.sha1(open(filename, 'rb').read()).hexdigest()
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
    print(f"\t[+] Umount ({datetime.datetime.now()})")
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