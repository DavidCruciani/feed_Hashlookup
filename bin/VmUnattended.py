import os
import time
import subprocess
import configparser
import datetime
import argparse
from feed_hashlookup import get_all_hashes
from update_vm import update_vm
from api_check import api_check

pathConf = '../config/config.cfg'

if os.path.isfile(pathConf):
    config = configparser.ConfigParser()
    config.read(pathConf)
else:
    print("[-] No conf file found")
    exit(1)

if "vm" in config:
    iso_path = config["vm"]["iso_path"]
    vdi_path = config["vm"]["vdi_path"]
else:
    print("[-] Need locations for VMs")
    exit(1)

if "hashlookup" in config:
    hashlookup_path = config["hashlookup"]["path"]

if "bloomfilter" in config:
    bloom_filter_info = {}
    bloom_filter_info["path"] = config["bloomfilter"]["path"]
    bloom_filter_info["capacity"] = config["bloomfilter"]["capacity"]
    bloom_filter_info["false_probability"] = config["bloomfilter"]["false_probability"]

if not os.path.isdir(hashlookup_path):
    os.mkdir(hashlookup_path)



log_path = os.path.join(iso_path, "log")
if not os.path.isdir(log_path):
    os.mkdir(log_path)

log_file = open(os.path.join(log_path, "VmUnattended.log"), "a")

if not os.path.isdir(vdi_path):
    os.mkdir(vdi_path)


try:
    with open("ignored_vms", "r") as read_file:
        ignored_vms = read_file.readlines()
except:
    ignored_vms = []

for i in range(0, len(ignored_vms)):
    ignored_vms[i] = ignored_vms[i].rstrip()




def write_to_log(msg):
    log_file.write(f"\n{datetime.datetime.now()}: {msg}")

def runningVms():
    """ Get the list of running vms """
    req = ["VBoxManage", "list", "runningvms"]
    return subprocess.run(req, capture_output=True)




parser = argparse.ArgumentParser()
parser.add_argument("-w10", "--win10", help="Work with Windows 10 vms", action="store_true")
parser.add_argument("-w11", "--win11", help="Work with Windows 11 vms", action="store_true")
parser.add_argument("-u", "--update_only", help="Skip the creation part", action="store_true")
parser.add_argument("-d", "--delete_all", help="Delete all vms", action="store_true")
parser.add_argument("-b", "--bloom_filter", help="Use bloom filter", action="store_true")
args = parser.parse_args()

w10 = args.win10
w11 = args.win11
if not w10 and not w11:
    print("[-] Need to choose windows 10 or windows 11")
    exit(1)

bloom_filter_info["active"] = args.bloom_filter

if args.delete_all:
    for file in os.listdir(vdi_path):
        vdi_vm_Path = os.path.join(vdi_path, file)
        if file.endswith(".vdi"):
            vm_name = file.split(".")[0]

            request = ["./Vm11Creator", vm_name, "del"]
            subprocess.call(request)
else:
    if not args.update_only:
        ## List all iso files
        for file in os.listdir(iso_path):
            iso_vm_Path = os.path.join(iso_path, file)
            if not os.path.isdir(iso_vm_Path) and file.split(".")[0] not in ignored_vms:
                vm_name = file.split(".")[0]
                os_type = vm_name.split("_")[0]
                print(os_type)
                if os_type == "Windows10" or os_type == "Windows11" or os_type == "Windows2016" or os_type == "Windows2019":
                    ## Do the process for all VM
                    print(f"VM: {vm_name}")

                    path_os_vdi = os.path.join(vdi_path, os_type)
                    if not os.path.isdir(path_os_vdi):
                        os.mkdir(path_os_vdi)

                    ## Create the VM
                    write_to_log(f"Create vm {vm_name}")
                    request = ["./Vm11Creator", vm_name, iso_vm_Path, path_os_vdi, os_type + "_64"]
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
                    update_vm(vm_name=vm_name, path_os_vdi=path_os_vdi, log_file=log_file, installation_flag=True)


                    ## Wait the VM to shutdown
                    res = runningVms()
                    while vm_name in res.stdout.decode():
                        time.sleep(10)
                        res = runningVms()
                    get_all_hashes(vdi_folder=path_os_vdi, 
                                   vm_path=f"{os.path.join(path_os_vdi, vm_name)}.vdi", 
                                   vm_name=vm_name, 
                                   feeder_path=hashlookup_path, 
                                   sysinfo_path=os.path.join(path_os_vdi, f"sysinfo_{vm_name}"),
                                   bloom_filter_info=bloom_filter_info )
                else:
                    print(f"[-] Change the name of {vm_name}, Format: Windows10_en, Windows11_fr, Windows2016_de, Windows2019_it")
                    exit(1)


    current_release_date = datetime.datetime.now()
    # current_release_date = datetime.datetime.strptime("2023-06-27T01:00:00Z", "%Y-%m-%dT%H:%M:%SZ")

    print(f"[+] Finished at: {current_release_date}")

    while True:
        current_release_date = api_check(current_release_date, vdi_path, hashlookup_path, w10, w11, log_file, bloom_filter_info)
        print(f"[+] {datetime.datetime.now()}: Waiting for 12 hours for a new check")

        time.sleep(43200) # 12 hours

log_file.close()