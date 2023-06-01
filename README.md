# Feed Hashlookup

This project aim to feed an other project named [Hashlookup](https://github.com/hashlookup/hashlookup-forensic-analyser). 

The goal of this repository is to get the hash of all files in a Windows machine, to feed the database of Hashlookup with million of hash completely safe.

## Requirements

- [VirtualBox](https://www.virtualbox.org/wiki/Linux_Downloads)
- virtualBox guest addition
  - `sudo apt-get install virtualbox-guest-additions-iso`
- ssdeep
  - On Ubuntu:
    - `sudo apt-get install build-essential libffi-dev python3 python3-dev python3-pip libfuzzy-dev`
    - `pip install ssdeep`
- python-tlsh
- ndjson
- BeautifulSoup4
- requests

## Important

Add in `win_postinstall` locate at : `/usr/share/virtualbox/UnattendedTemplates`

```
reg.exe add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" /v EnableLUA /t REG_DWORD /d 0 /f
```

## VM creation

The first step, is to create VM from iso file.

- Download iso [here](https://www.microsoft.com/software-download/windows11)
- Name the iso like the name you will give to your VM: `Windows11_en.iso`, `Windows10_en.vdi`
- fill  `config/config.cfg`
- Run `bin/VmUnattended.py`

VM will be created using the script `bin/Vm11Creator`
