# Feed Hashlookup

This project aim to feed an other project named [Hashlookup](https://github.com/hashlookup/hashlookup-forensic-analyser). 

The goal of this repository is to get the hash of all files in a Windows machine, to feed the database of Hashlookup with million of hash completely safe.



## Requirements

- [VirtualBox](https://www.virtualbox.org/wiki/Linux_Downloads)
- ssdeep
  - On Ubuntu:
    - `sudo apt-get install build-essential libffi-dev python3 python3-dev python3-pip libfuzzy-dev`
    - `pip install ssdeep`
- python-tlsh

## VM creation

The first step, is to create VM from iso file.

- Download iso [here](https://www.microsoft.com/software-download/windows11)
- Name the iso like the name you will give to your VM: `Win11_en.iso`, `Win11_en.vdi`
- fill the first line of  `etc/allVariables.py`
- Run `bin/VmUnattended.py`

VM will be created using the script `bin/Vm11Creator`



#### Usage

~~~~bash
dacru@dacru:~/github/feed_Hashlookup/bin$ ./Vm11Creator vmName isoPath vdipath
~~~~

`vmName` : Name that the VM will have

`isoPath` :  Path to the iso to use during the installation

`vdipath` : Path to the vdi to use for the VM



#### Note

`bin/Vm11Creator` is called by `bin/VmUnattended`, so it's very important to fill the first line of `etc/allVariables.py`. The program will do the work.



## Feed Hashlookup

- Run a created VM, do `systeminfo`  in a terminal and write in a file:
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

