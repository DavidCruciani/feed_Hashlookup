import os
import requests
import subprocess
import json
from bs4 import BeautifulSoup
import datetime
import time
from feed_hashlookup import get_all_hashes
from update_vm import update_vm



def runningVms():
    """ Get the list of running vms """
    req = ["VBoxManage", "list", "runningvms"]
    return subprocess.run(req, capture_output=True)


def html_to_json(content, indent=None):
    soup = BeautifulSoup(content, "html.parser")
    rows = soup.find_all("tr")
    
    headers = {}
    thead = soup.find("thead")
    if thead:
        thead = soup.find_all("th")
        for i in range(len(thead)):
            headers[i] = thead[i].text.strip().lower()
    data = []
    for row in rows:
        cells = row.find_all("td")
        if thead:
            items = {}
            if len(cells) > 0:
                for index in headers:
                    items[headers[index]] = cells[index].text
        else:
            items = []
            for index in cells:
                items.append(index.text.strip())
        if items:
            data.append(items)
    return json.dumps(data, indent=indent)


def start_process_vm(os_type, iso_path, hashlookup_path, log_file):
    path_win_10 = os.path.join(iso_path, os_type)
    if os.path.isdir(path_win_10):
        path_os_vdi = os.path.join(iso_path, os_type)
        for vm_file in os.listdir(path_win_10):
            if vm_file.endswith(".vdi"):
                vm_name = vm_file.split(".")[0]
                update_vm(vm_name=vm_name, path_os_vdi=path_os_vdi, log_file=log_file)
                ## Wait the VM to shutdown
                res = runningVms()
                while vm_name in res.stdout.decode():
                    time.sleep(10)
                    res = runningVms()
                get_all_hashes(vdi_folder=path_os_vdi, vm_path=f"{os.path.join(path_os_vdi, vm_name)}.vdi", vm_name=vm_name, feeder_path=hashlookup_path, sysinfo_path=os.path.join(path_os_vdi, f"sysinfo_{vm_name}"))



def api_check(iso_path, hashlookup_path, log_file):
    # current_release_date = datetime.datetime.strptime("2023-03-14T07:00:00Z", "%Y-%m-%dT%H:%M:%SZ")
    current_release_date = datetime.datetime.strptime("2023-05-23T01:00:00Z", "%Y-%m-%dT%H:%M:%SZ")
    start_win_10 = False
    start_win_11 = False
    start_win_2016 = False
    start_win_2019 = False
    try:
        response = requests.get("https://api.msrc.microsoft.com/cvrf/v2.0/updates", headers={"Accept": "application/json"})
        if response.status_code == 200:
            api_current_release_date = datetime.datetime.strptime(response.json()["value"][-1]["CurrentReleaseDate"], "%Y-%m-%dT%H:%M:%SZ")
            if api_current_release_date > current_release_date:
                print(f"[+] New release: {datetime.datetime.now()}")
                current_release_date = api_current_release_date
                response = requests.get("https://api.msrc.microsoft.com/cvrf/v2.0/document/2023-May", headers={"Accept": "application/json"})
                if response.status_code == 200:
                    html_data = response.json()["DocumentNotes"][0]["Value"]
                    soup = BeautifulSoup(html_data, "html.parser")
                    table = soup.find_all('table')
                    
                    os_applied = json.loads(html_to_json(str(table[-1])))
                    for update_info in os_applied:
                        if "Windows 10" in update_info["applies to"]:
                            start_win_10 = True
                        if "Windows 11" in update_info["applies to"]:
                            start_win_11 = True
                        if "Windows Server 2016" in update_info["applies to"]:
                            start_win_2016 = True
                        if "Windows Server 2019" in update_info["applies to"]:
                            start_win_2019 = True
            else:
                print(f"[*] No new Release {current_release_date}")
    except Exception as e:
        print(f"[-] Error: {e}")
        pass


    if start_win_10:
        start_process_vm("Windows10", iso_path, hashlookup_path, log_file)

    if start_win_11:
        start_process_vm("Windows11", iso_path, hashlookup_path, log_file)

    if start_win_2016:
        start_process_vm("Windows2016", iso_path, hashlookup_path, log_file)

    if start_win_2019:
        start_process_vm("Windows2019", iso_path, hashlookup_path, log_file)

