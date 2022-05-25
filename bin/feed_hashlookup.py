import os
import re
import sys
import time
import ndjson
import shutil
import subprocess
import pathlib
pathProg = pathlib.Path(__file__).parent.absolute()
pathWork = ""
for i in re.split(r"/|\\", str(pathProg))[:-1]:
    pathWork += i + "/"
sys.path.append(pathWork + "etc")
import allVariables

import hashlib
import ssdeep
import tlsh


def callSubprocessPopen(request, shellUse = False):
    if shellUse:
        p = subprocess.Popen(request, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p_status = p.wait()
    else:
        p = subprocess.Popen(request, stdout=subprocess.PIPE)
        (output, err) = p.communicate()
        p_status = p.wait()


# Get the list of running vms
def runningVms():
    req = [allVariables.VBoxManage, "list", "runningvms"]
    return subprocess.run(req, capture_output=True)



if __name__ == '__main__':

    for file in os.listdir(allVariables.pathToWindowsVM):
        vmPath = os.path.join(allVariables.pathToWindowsVM, file)
        vmName = file.split(".")[0]
        print(f"VM: {vmName}")

        res = runningVms()

        request = [allVariables.VBoxManage, 'startvm', allVariables.WindowsVM, '--type', 'headless']
        if not allVariables.WindowsVM in res.stdout.decode():
            ## Start windows machine
            print("[+] Windows Start")
            callSubprocessPopen(request)
        else:
            print("[+] Windows Running")

        ## Wait windows machine to shutdown
        res = runningVms()

        ## Output to see the time that the windows machine is running
        cptime = 0
        while allVariables.WindowsVM in res.stdout.decode():
            time.sleep(60)
            cptime += 1
            print("\rTime spent: %s min" % (cptime), end="")
            res = runningVms()

        print("\n[+] Windows stop\n")


        ## Convert windows machine into raw format
        convert_file = "%s%s.img" %(allVariables.pathToConvert, vmName)

        print("## Convertion ##")
        res = subprocess.call([allVariables.VBoxManage, "clonehd", vmPath, convert_file, "--format", "raw"])
        print("## Convertion Finish ##\n")

        ## create mount directory
        pathMnt = "./mnt_convert"
        if not os.path.isdir(pathMnt):
            os.mkdir(pathMnt)


        print("[+] Feed Hashlookup setup")
        
        ## mount the convert image
        print("\t[+] Mount")
        request = "sudo mount -o loop,ro,noexec,noload,offset=$((512*104448)) %s %s" % (convert_file, pathMnt)
        callSubprocessPopen(request, True)

        intermediate_file = "./intermediate_file" 
        print("\t[+] List of all files")
        request = "find %s -type f > %s" % (pathMnt, intermediate_file)
        callSubprocessPopen(request, True)

        data = list()
        sysinfofile = open(allVariables.pathToSysInfo, "r")
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

        with open(allVariables.pathToFeedHashlookup + "/" + vmName + ".json", 'w') as outfile:
            ndjson.dump(data, outfile)

        os.remove(intermediate_file)

        ## umount the convert image
        print("\t[+] Umount")
        request = "sudo umount " + pathMnt
        callSubprocessPopen(request, True)

            
        ## Suppression of the current raw disk
        os.remove(convert_file)
        request = [allVariables.VBoxManage, "closemedium", "disk", convert_file, "--delete"]
        callSubprocessPopen(request)

    ## Suppression of mount folder
    try:
        shutil.rmtree(pathMnt)
    except:
        pass
    