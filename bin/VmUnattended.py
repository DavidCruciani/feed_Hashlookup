import os
import re
import sys
import time
import pathlib
pathProg = pathlib.Path(__file__).parent.absolute()
pathWork = ""
for i in re.split(r"/|\\", str(pathProg))[:-1]:
    pathWork += i + "/"
sys.path.append(pathWork + "etc")
import allVariables
import subprocess

# Get the list of running vms
def runningVms():
    req = ["VBoxManage", "list", "runningvms"]
    return subprocess.run(req, capture_output=True)

for file in os.listdir(allVariables.pathToWindowsIsoFolder):
    vmPath = os.path.join(allVariables.pathToWindowsIsoFolder, file)
    vmName = file.split(".")[0]

    if not os.path.isdir(vmPath):
        print(f"VM: {vmName}")
        pathToVdi = os.path.join(allVariables.pathToWindowsIsoFolder, "vdi")
        if not os.path.isdir(pathToVdi):
            os.mkdir(pathToVdi)
        request = ["./Vm11Creator", vmName, vmPath, pathToVdi]
        subprocess.call(request)

        request = ["VBoxManage", "startvm", vmName, "--type", "headless"]
        p = subprocess.Popen(request, stdout=subprocess.PIPE)
        (output, err) = p.communicate()
        p_status = p.wait()

        ## Wait windows machine to shutdown
        res = runningVms()

        ## Output to see the time that the windows machine is running
        cptime = 0
        while vmName in res.stdout.decode():
            time.sleep(300)
            cptime += 5
            print("\rTime spent: %s min" % (cptime), end="")
            res = runningVms()

        print("\n[+] Windows stop\n")