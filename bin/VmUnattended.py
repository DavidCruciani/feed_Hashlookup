import os
import re
import sys
import pathlib
pathProg = pathlib.Path(__file__).parent.absolute()
pathWork = ""
for i in re.split(r"/|\\", str(pathProg))[:-1]:
    pathWork += i + "/"
sys.path.append(pathWork + "etc")
import allVariables
import subprocess

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