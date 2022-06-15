import pyautogui
import time
import subprocess

pyautogui.PAUSE = 2.5

def stringModification(string):
    """Convert string in qwerty"""
    return string.translate(str.maketrans('azqwAZQW&é"\'(-è_çà)^$Mù,?;:!§1234567890','qwazQWAZ1234567890-[]:\'mM,./?!@#$%^&*()'))


with open("../etc/listVM.txt") as read_file:
    listVM = read_file.readlines()

for vm in listVM:
    vm = vm.rstrip("\n")
    vm = stringModification(vm)

    time.sleep(1)
    pyautogui.keyDown('ctrl')
    pyautogui.press('pagedown')
    pyautogui.keyUp('ctrl')

    time.sleep(1)
    pyautogui.typewrite(vm, interval=1)
    #pyautogui.typewrite(f'VBoxManage startvm {vm} --type headless', interval=1)
    pyautogui.press('enter')

    time.sleep(5)
    pyautogui.keyDown('ctrl')
    pyautogui.press('pagedown')
    pyautogui.keyUp('ctrl')

    exit(0)

    # request = ['xfreerdp', '-v:localhost:5001']
    # subprocess.Popen(request)

    # pyautogui.moveTo(300,300)
    # pyautogui.click()

    time.sleep(55)

    # screen language
    time.sleep(2)
    pyautogui.typewrite(['tab', 'tab', 'tab', 'enter'], interval=1)

    # screen install
    time.sleep(2)
    pyautogui.typewrite(['enter'], interval=1)

    # screen license
    time.sleep(20)
    pyautogui.typewrite(['tab', 'tab', 'tab', 'enter'], interval=1)

    # screen os choose (familly, pro, ...)
    time.sleep(2)
    pyautogui.press(['down'], presses=5)
    pyautogui.press(['enter', 'enter'])
    # pyautogui.typewrite(['enter'], interval=1)

    # screen prob with win11
    time.sleep(5)
    pyautogui.keyDown('shift')
    pyautogui.press('f10')
    pyautogui.keyUp('shift')

    # screen cmd
    time.sleep(2)
    pyautogui.typewrite(['r', 'e', 'g', 'e', 'd', 'i', 't', 'enter'], interval=1)

    # screen regedit
    time.sleep(4)
    pyautogui.press(['down'], presses=3)
    pyautogui.press(['right'])
    pyautogui.press(['down'], presses=6)
    pyautogui.press(['right'])

    # System -> Setup
    time.sleep(1)
    pyautogui.press(['down'], presses=10)
    pyautogui.press(['right'])

    # New key
    time.sleep(1)
    pyautogui.press(['f10'], interval=1)
    time.sleep(1)
    pyautogui.press(['right'])
    time.sleep(1)
    pyautogui.press(['enter'])

    time.sleep(1)
    pyautogui.press(['right', 'enter'])
    time.sleep(1)
    pyautogui.typewrite(['L', 'q', 'b', 'C', 'o', 'n', 'f', 'i', 'g', 'enter'], interval=1)

    #Dword value
    for i in range(0,4):
        time.sleep(1)
        pyautogui.press(['f10'], interval=1)
        time.sleep(1)
        pyautogui.press(['right'])
        time.sleep(1)
        pyautogui.press(['enter'])

        time.sleep(1)
        pyautogui.press(['right'])
        time.sleep(1)

        pyautogui.press(['down'], presses=3)
        time.sleep(1)
        pyautogui.press(['enter'])
        time.sleep(1)
        if i == 0:
            pyautogui.typewrite('BypqssTP:Check', interval=1)
        elif i == 1:
            pyautogui.typewrite('BypqssRQ:Check', interval=1)
        elif i == 2:
            pyautogui.typewrite('BypqssCPUCheck', interval=1)
        elif i == 3:
            pyautogui.typewrite('BypqssSecureBootCheck', interval=1)
        
        time.sleep(1)
        pyautogui.press(['enter'])
        time.sleep(1)
        pyautogui.press(['enter'])
        time.sleep(5)
        # press 1
        pyautogui.press(['!'])
        time.sleep(2)
        pyautogui.press(['enter'])

        time.sleep(1)
        pyautogui.typewrite(['tab', 'tab'], interval=1)

    # close 3 windows
    for i in range(0,3):
        time.sleep(2)
        pyautogui.keyDown('alt')
        pyautogui.press('f4')
        pyautogui.keyUp('alt')

    time.sleep(2)
    pyautogui.press(['left'])
    time.sleep(1)
    pyautogui.press(['enter', 'enter'])


    # Go back to the beginning
    # screen install
    time.sleep(2)
    pyautogui.typewrite(['enter'], interval=1)

    # screen license
    time.sleep(20)
    pyautogui.typewrite(['tab', 'tab', 'tab', 'enter'], interval=1)

    # screen os choose (familly, pro, ...)
    time.sleep(2)
    pyautogui.press(['down'], presses=5)
    pyautogui.press(['enter', 'enter'])

    # screen accept conditions
    time.sleep(3)
    pyautogui.typewrite(['space', 'tab', 'enter'], interval=1)

    # screen type of installation
    time.sleep(2)
    pyautogui.press(['down', 'enter', 'enter'])

    # screen choose disk
    time.sleep(2)
    pyautogui.typewrite(['enter'], interval=1)

    # Wait until the end of the installation
    print("Installation...")
    time.sleep(1740)


    # screen region
    print("End of Installation")
    time.sleep(2)
    pyautogui.typewrite(['enter'], interval=1)

    # screen keyboard
    time.sleep(25)
    pyautogui.typewrite(['enter'], interval=1)
    time.sleep(2)
    pyautogui.typewrite(['enter'], interval=1)

    # screen name for the computer
    print("First update")
    time.sleep(300)
    print("End First update")
    # time.sleep(100)
    pyautogui.typewrite(['tab', 'enter'], interval=1)

    # screen configuration
    time.sleep(25)
    pyautogui.typewrite(['tab', 'tab', 'enter', 'enter'], interval=1)

    # screen miscrosoft account
    time.sleep(10)
    pyautogui.typewrite(['tab', 'tab', 'tab', 'tab', 'enter'], interval=1)

    # screen confiramtion offline account
    time.sleep(3)
    pyautogui.typewrite(['tab', 'tab', 'enter'], interval=1)

    # screen ignore microsoft account
    time.sleep(10)
    pyautogui.typewrite(['tab', 'enter'], interval=1)

    # screen name account
    time.sleep(5)
    pyautogui.typewrite(['B', 'o', 'b', 'tab', 'tab', 'tab', 'enter'], interval=1)

    # screen password
    time.sleep(2)
    pyautogui.typewrite(['tab', 'tab', 'tab', 'enter'], interval=1)

    # screen autorisation
    time.sleep(20)
    pyautogui.typewrite(['tab', 'tab', 'tab'], interval=1)
    pyautogui.press(['down'])
    pyautogui.typewrite(['enter', 'enter'], interval=1)
    pyautogui.typewrite(['tab', 'tab', 'enter'], interval=1)

    time.sleep(2)
    pyautogui.press(['down'])
    pyautogui.typewrite(['enter', 'enter'], interval=1)
    pyautogui.typewrite(['tab', 'tab', 'enter'], interval=1)

    time.sleep(2)
    pyautogui.press(['down'])
    pyautogui.typewrite(['enter', 'enter'], interval=1)
    pyautogui.typewrite(['tab', 'tab', 'enter'], interval=1)

    time.sleep(2)
    pyautogui.press(['down'])
    pyautogui.typewrite(['enter', 'enter'], interval=1)
    pyautogui.typewrite(['tab', 'tab', 'enter'], interval=1)

    time.sleep(2)
    pyautogui.press(['down'])
    pyautogui.typewrite(['enter', 'enter'], interval=1)
    pyautogui.typewrite(['tab', 'tab', 'enter'], interval=1)

    time.sleep(2)
    pyautogui.press(['down'])
    pyautogui.typewrite(['enter', 'enter'], interval=1)
    pyautogui.typewrite(['tab', 'tab', 'enter'], interval=1)

    # do some udpate
    time.sleep(300)
    pyautogui.typewrite(['tab'], interval=1)
    pyautogui.press(['right'], presses=5)
    pyautogui.typewrite(['enter', 'enter'], interval=1)

    time.sleep(10)
    pyautogui.press(['down'], presses=11)
    pyautogui.typewrite(['enter', 'enter'], interval=1)
    time.sleep(5)
    pyautogui.typewrite(['tab', 'tab', 'enter'], interval=1)

    print("Begin update")
    time.sleep(1800)
    print("End update")
    for i in range(0, 2):
        pyautogui.keyDown('alt')
        pyautogui.press('f4')
        pyautogui.keyUp('alt')
        time.sleep(2)

    pyautogui.typewrite(['enter'], interval=1)