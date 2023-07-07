import re
import time
import subprocess
import datetime

def write_to_log(log_file, msg):
    log_file.write(f"\n{datetime.datetime.now()}: {msg}")

def update_vm(vm_name, path_os_vdi, log_file, installation_flag=False):
    print("[+] Start for update")
    write_to_log(log_file, f"Start {vm_name} for update")
    request = ["VBoxManage", "startvm", vm_name, "--type", "headless"]
    p = subprocess.Popen(request, stdout=subprocess.PIPE)

    print("[+] Try to update...")
    need_wait = True
    ## Execute all powershell commands needed to run updates
    # if os_type == "Windows2016" or os_type == "Windows2019":

    if installation_flag:
        command = '(Install-PackageProvider -Name NuGet -Force ); (Install-Module PSWindowsUpdate -Force); (Set-ExecutionPolicy Unrestricted -Force); (Import-Module PSWindowsUpdate); (Get-WindowsUpdate -MicrosoftUpdate -AcceptAll -Install -AutoReboot)'
    else:
        command = "(Get-WindowsUpdate -MicrosoftUpdate -AcceptAll -Install -AutoReboot)"
    request = ["vboxmanage", "guestcontrol", vm_name, "run", "C:/Windows/System32/WindowsPowerShell/v1.0/powershell.exe", "--username", "John", "--password", "John", "--wait-stdout", "--", "-command", command]
    while need_wait:
        print(request)
        p = subprocess.run(request, capture_output=True)
        if not len(p.stderr):
            print(f"[+] Updates done")
            need_wait = False
        else:
            write_to_log(log_file, f"Error {vm_name}: {p.stderr}")
            print("[+] Waiting the VM to be usable...")
            time.sleep(30)
    
    time.sleep(30)

    ## Wait the VM to reboot
    print("[+] Wait vm to reboot and install updates")
    write_to_log(log_file, f"Wait VM {vm_name} to reboot and install updates")
    need_wait = True
    request = ["vboxmanage", "guestcontrol", vm_name, "run", "C:/Windows/System32/WindowsPowerShell/v1.0/powershell.exe", "--username", "John", "--password", "John", "--wait-stdout", "--", "-command", "whoami"]
    while need_wait:
        print(request)
        p = subprocess.run(request, capture_output=True)
        if not len(p.stderr):
            # print(f"[+] Output: {p.stdout}")
            ## Get system information for hashlookup
            request_sysinfo = ["vboxmanage", "guestcontrol", vm_name, "run", "cmd.exe", "--username", "John", "--password", "John", "--wait-stdout", "--", "/c", "systeminfo"]
            s = subprocess.run(request_sysinfo, capture_output=True)
            # print(s.stdout)
            try:
                SystemVersion = s.stdout.decode("cp850").split("\n")[3]
                SystemName = s.stdout.decode("cp850").split("\n")[2]
            except:
                continue

            x = re.search(r" {2,}(?P<version>.*)", SystemVersion)
            y = re.search(r" {2,}(?P<name>.*)", SystemName)

            with open(f"{path_os_vdi}/sysinfo_{vm_name}", "w") as write_file:
                write_file.write(x.group("version"))
                write_file.write(y.group("name"))

            time.sleep(2)
            
            request_shutdown = ["vboxmanage", "guestcontrol", vm_name, "run", "cmd.exe", "--username", "John", "--password", "John", "--wait-stdout", "--", "/c", "shutdown /s /t 0"]
            p = subprocess.run(request_shutdown, capture_output=True)

            need_wait = False
        else:
            write_to_log(log_file, f"Error {vm_name}: {p.stderr}")
            print("[+] Waiting the VM to be usable...")
            time.sleep(20)