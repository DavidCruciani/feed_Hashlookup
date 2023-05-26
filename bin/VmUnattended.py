import os
import re
import time
import subprocess
import configparser
import datetime
from  feed_hashlookup import get_all_hashes

pathConf = '../config/config.cfg'

if os.path.isfile(pathConf):
    config = configparser.ConfigParser()
    config.read(pathConf)
else:
    print("[-] No conf file found")
    exit(1)

if "iso" in config:
    iso_path = config["iso"]["path"]
else:
    print("[-] Need a location for ISO files")
    exit(1)

if "hashlookup" in config:
    hashlookup_path = config["hashlookup"]["path"]



log_file = open("VmUnattended.log", "a")


def write_to_log(msg):
    log_file.write(f"\n{datetime.datetime.now()}: {msg}")

def runningVms():
    """ Get the list of running vms """
    req = ["VBoxManage", "list", "runningvms"]
    return subprocess.run(req, capture_output=True)

## List all iso files
for file in os.listdir(iso_path):
    isoPath = os.path.join(iso_path, file)
    vm_name = file.split(".")[0]

    ## Do the process for all VM
    if not os.path.isdir(isoPath):
        print(f"VM: {vm_name}")

        pathToVdi = os.path.join(iso_path, "vdi")
        if not os.path.isdir(pathToVdi):
            os.mkdir(pathToVdi)

        ## Create the VM
        write_to_log(f"Create vm {vm_name}")
        request = ["./Vm11Creator", vm_name, isoPath, pathToVdi]
        subprocess.call(request)

        ## Install the iso
        print("[+] Windows Start")
        write_to_log(f"Windows {vm_name} Start")
        request = ["VBoxManage", "startvm", vm_name, "--type", "headless"]
        p = subprocess.Popen(request, stdout=subprocess.PIPE)
        (output, err) = p.communicate()
        p_status = p.wait()

        ## Wait the VM to shutdown
        res = runningVms()
        cptime = 0
        while vm_name in res.stdout.decode():
            time.sleep(180)
            cptime += 3
            print("\rTime spent: %s min" % (cptime), end="")
            res = runningVms()
        print("\n[+] Windows stop\n")
        write_to_log(f"Windows {vm_name} stop")


        ## Run again the VM to install updates
        print("[+] Start for update")
        write_to_log(f"Start {vm_name} for update")
        request = ["VBoxManage", "startvm", vm_name, "--type", "headless"]
        p = subprocess.Popen(request, stdout=subprocess.PIPE)

        print("[+] Try to update...")
        need_wait = True
        ## Execute all powershell commands needed to run updates
        command = '(Install-PackageProvider -Name NuGet -Force ); (Install-Module PSWindowsUpdate -Force); (Set-ExecutionPolicy Unrestricted -Force); (Get-WindowsUpdate -MicrosoftUpdate -AcceptAll -Install -AutoReboot)'
        request = ["vboxmanage", "guestcontrol", vm_name, "run", "C:/Windows/System32/WindowsPowerShell/v1.0/powershell.exe", "--username", "John", "--password", "John", "--wait-stdout", "--", "-command", command]
        while need_wait:
            print(request)
            p = subprocess.run(request, capture_output=True)
            if not len(p.stderr):
                print(f"[+] Updates done")
                need_wait = False
            else:
                write_to_log(f"Error {vm_name}: {p.stderr}")
                print("[+] Waiting the VM to be usable...")
                time.sleep(30)

        
        ## Wait the VM to reboot
        print("[+] Wait vm to reboot and install updates")
        write_to_log(f"Wait VM {vm_name} to reboot and install updates")
        need_wait = True
        request = ["vboxmanage", "guestcontrol", vm_name, "run", "C:/Windows/System32/WindowsPowerShell/v1.0/powershell.exe", "--username", "John", "--password", "John", "--wait-stdout", "--", "-command", "whoami"]
        while need_wait:
            print(request)
            p = subprocess.run(request, capture_output=True)
            if not len(p.stderr):
                print(f"[+] Output: {p.stdout}")
                ## Get system information for hashlookup
                request_sysinfo = ["vboxmanage", "guestcontrol", vm_name, "run", "cmd.exe", "--username", "John", "--password", "John", "--wait-stdout", "--", "/c", "systeminfo"]
                s = subprocess.run(request_sysinfo, capture_output=True)
                print(s.stdout)
                SystemVersion = s.stdout.decode("cp850").split("\n")[3]
                SystemName = s.stdout.decode("cp850").split("\n")[2]

                x = re.search(r" {2,}(?P<version>.*)", SystemVersion)
                y = re.search(r" {2,}(?P<name>.*)", SystemName)

                with open(f"{pathToVdi}/sysinfo", "w") as write_file:
                    write_file.write(x.group("version"))
                    write_file.write(y.group("name"))

                
                request = ["vboxmanage", "guestcontrol", vm_name, "run", "cmd.exe", "--username", "John", "--password", "John", "--wait-stdout", "--", "/c", "shutdown /s /t 0"]
                p = subprocess.run(request, capture_output=True)

                need_wait = False
            else:
                write_to_log(f"Error {vm_name}: {p.stderr}")
                print("[+] Waiting the VM to be usable...")
                time.sleep(20)

        ## Wait windows machine to shutdown
        res = runningVms()

        print(f"[+] Windows stop")
        write_to_log(f"Windows {vm_name} stop")

        get_all_hashes(vdi_folder=pathToVdi, vm_path=f"{os.path.join(pathToVdi, vm_name)}.vdi", vm_name=vm_name, feeder_path=hashlookup_path, sysinfo_path=os.path.join(pathToVdi, "sysinfo"))