# Feed Hashlookup

This project aim to feed an other project named [Hashlookup](https://github.com/hashlookup/hashlookup-forensic-analyser). 

The goal of this repository is to get the hash of all files in a Windows machine, to feed the database of Hashlookup with million of hash completely safe.



## Requirements

- [pyautogui](https://github.com/asweigart/pyautogui)
- [VirtualBox](https://www.virtualbox.org/wiki/Linux_Downloads)
- [FreeRDP](https://doc.ubuntu-fr.org/freerdp)
- ssdeep
  - On Ubuntu:
    - `sudo apt-get install build-essential libffi-dev python3 python3-dev python3-pip libfuzzy-dev`
    - `pip install ssdeep`

- python-tlsh

## VM creation

The first step, is to create VM from iso file.

- Download iso [here](https://www.microsoft.com/software-download/windows11)
- Name the iso like the name you will give to your VM: `Win11_en.iso`, `Win11_en.vdi`
- List the VM name in `etc/listVM.txt`.  Ex: `Win11_en`
- Run `bin/Vm11Creator`

#### Usage

~~~bash
./VmCreator name_of_the_vm 
./VmCreator name_of_the_vm del # delete the VM based on the name give in first 
~~~

Now the VM is created 



## ISO Installation

- Open a new tab
- If the VM will be execute on a remote server:
  - connect to the server with a tunnel: `ssh -l username server -L localport:server:3389`
- Else do nothing and leave the tab open

- Run `bin/vmCreation.py`
- Don't click somewhere with your mouse or the focus on the VM will be lost and the program will not work
- It's better to not use your PC during the execution



## Feed Hashlookup

- Run a VM you create and do `systeminfo`  in a terminal and write in a file:
  - System version.    Ex: `10.0.22000 N/A Build 22000`
  - Name of the os.    Ex: `Microsoft Windows 11 Pro`
- Fill `etc/allVariables`
- Run `bin/feed_hashlookup`

#### Usage

~~~bash
dacru@dacru:~/github/feed_Hashlookup/bin$ python3 feed_hashlookup.py -h
usage: feed_hashlookup.py [-h] [-e]

optional arguments:
  -h, --help         show this help message and exit
  -e, --export_file  Export all file from the VM to the PC
~~~

