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


def request_document(current_release_date, start_win_10, start_win_11, retry = False):
    request_date = current_release_date.strftime("%Y-%b")
    response = requests.get(f"https://api.msrc.microsoft.com/cvrf/v3.0/cvrf/{request_date}", headers={"Accept": "application/json"})
    flag_retry = True
    if response.status_code == 200:
        html_data = response.json()["DocumentNotes"][0]["Value"]
        soup = BeautifulSoup(html_data, "html.parser")
        table = soup.find_all('table')
        
        os_applied = json.loads(html_to_json(str(table[-1])))
        for update_info in os_applied:
            if "applies to" in update_info:
                flag_retry = False
                if "Windows 10" in update_info["applies to"]:
                    start_win_10 = True
                if "Windows 11" in update_info["applies to"]:
                    start_win_11 = True
                # if "Windows Server 2016" in update_info["applies to"]:
                #     start_win_2016 = True
                # if "Windows Server 2019" in update_info["applies to"]:
                #     start_win_2019 = True
    else:
        print("[-] Document not reached... Will retry in 3 seconds.")
        print(response.status_code)
        time.sleep(3)
        return request_document(current_release_date, start_win_10, start_win_11, retry=False)

    if flag_retry and retry:
        print("[-] Error when reading document. Will retry in 3 seconds.")
        time.sleep(3)
        return request_document(current_release_date, start_win_10, start_win_11, retry=False)

    return start_win_10, start_win_11


def start_process_vm(os_type, vdi_path, hashlookup_path, log_file):
    path_os_vdi = os.path.join(vdi_path, os_type)
    if os.path.isdir(path_os_vdi):
        for vm_file in os.listdir(path_os_vdi):
            if vm_file.endswith(".vdi"):
                vm_name = vm_file.split(".")[0]
                update_vm(vm_name=vm_name, path_os_vdi=path_os_vdi, log_file=log_file)
                ## Wait the VM to shutdown
                res = runningVms()
                while vm_name in res.stdout.decode():
                    time.sleep(10)
                    res = runningVms()
                get_all_hashes(vdi_folder=path_os_vdi, vm_path=f"{os.path.join(path_os_vdi, vm_name)}.vdi", vm_name=vm_name, feeder_path=hashlookup_path, sysinfo_path=os.path.join(path_os_vdi, f"sysinfo_{vm_name}"))



def api_check(current_release_date, vdi_path, hashlookup_path, w10, w11, log_file):
    start_win_10 = False
    start_win_11 = False
    # start_win_2016 = False
    # start_win_2019 = False
    flag_new_release = False
    try:
        current_year = datetime.datetime.now().strftime("%Y")
        response = requests.get(f"https://api.msrc.microsoft.com/cvrf/v3.0/updates('{current_year}')", headers={"Accept": "application/json"})
        if response.status_code == 200:
            for release_date in response.json()["value"]:
                api_current_release_date = datetime.datetime.strptime(release_date["CurrentReleaseDate"], "%Y-%m-%dT%H:%M:%SZ")
                api_initial_release_date = datetime.datetime.strptime(release_date["InitialReleaseDate"], "%Y-%m-%dT%H:%M:%SZ")

                if api_current_release_date > current_release_date:
                    print(f"[+] New release: {api_current_release_date}")
                    current_release_date = api_current_release_date
                    start_win_10, start_win_11 = request_document(current_release_date, start_win_10, start_win_11, retry=True)
                    flag_new_release = True
                    break
                elif api_initial_release_date > current_release_date:
                    print(f"[+] New release: {api_initial_release_date}")
                    current_release_date = api_initial_release_date
                    start_win_10, start_win_11 = request_document(current_release_date, start_win_10, start_win_11, retry=True)
                    flag_new_release = True
                    break
        if not flag_new_release:
            print(f"[*] No new Release {current_release_date}")
    except Exception as e:
        print(f"[-] Error: {e}")
        pass


    if start_win_10 and w10:
        start_process_vm("Windows10", vdi_path, hashlookup_path, log_file)

    if start_win_11 and w11:
        start_process_vm("Windows11", vdi_path, hashlookup_path, log_file)

    # if start_win_2016:
    #     start_process_vm("Windows2016", vdi_path, hashlookup_path, log_file)

    # if start_win_2019:
    #     start_process_vm("Windows2019", vdi_path, hashlookup_path, log_file)

    return current_release_date