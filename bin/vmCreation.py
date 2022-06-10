import pyautogui
import time
import pydirectinput

pyautogui.PAUSE = 2.5

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
pydirectinput.press(['down'], presses=5)
pydirectinput.press(['enter', 'enter'])
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
pydirectinput.press(['down'], presses=3)
pydirectinput.press(['right'])
pydirectinput.press(['down'], presses=6)
pydirectinput.press(['right'])

# System -> Setup
time.sleep(1)
pydirectinput.press(['down'], presses=10)
pydirectinput.press(['right'])

# New key
time.sleep(1)
pydirectinput.press(['f10', 'f10'], interval=1)
time.sleep(1)
pydirectinput.press(['right'])
time.sleep(1)
pydirectinput.press(['enter'])

time.sleep(1)
pydirectinput.press(['down'])
time.sleep(1)
pydirectinput.press(['right', 'enter', 'enter'])
time.sleep(1)
pyautogui.typewrite(['L', 'a', 'b', 'C', 'o', 'n', 'f', 'i', 'g', 'enter'], interval=1)

#Dword value
for i in range(0,4):
    time.sleep(1)
    pydirectinput.press(['f10'], interval=1)
    time.sleep(1)
    pydirectinput.press(['right'])
    time.sleep(1)
    pydirectinput.press(['enter'])

    time.sleep(1)
    pydirectinput.press(['down'])
    time.sleep(1)
    pydirectinput.press(['right'])
    time.sleep(1)
    pydirectinput.press(['enter'])
    time.sleep(1)

    pydirectinput.press(['down'], presses=3)
    time.sleep(1)
    pydirectinput.press(['enter', 'enter'])
    time.sleep(1)
    if i == 0:
        pyautogui.typewrite('BypassTPMCheck', interval=1)
    elif i == 1:
        pyautogui.typewrite('BypassRAMCheck', interval=1)
    elif i == 2:
        pyautogui.typewrite('BypassCPUCheck', interval=1)
    elif i == 3:
        pyautogui.typewrite('BypassSecureBootCheck', interval=1)
    
    time.sleep(1)
    pydirectinput.press(['enter'])
    time.sleep(1)
    pydirectinput.press(['enter'])
    time.sleep(5)
    pyautogui.press(['1', '1'])
    time.sleep(2)
    pydirectinput.press(['enter'])

    time.sleep(1)
    pyautogui.typewrite(['tab', 'tab'], interval=1)

# close 3 windows
for i in range(0,3):
    time.sleep(2)
    pyautogui.keyDown('alt')
    pyautogui.press('f4')
    pyautogui.keyUp('alt')

time.sleep(2)
pydirectinput.press(['left'])
time.sleep(1)
pydirectinput.press(['enter', 'enter'])


# Go back to the beginning
# screen install
time.sleep(2)
pyautogui.typewrite(['enter'], interval=1)

# screen license
time.sleep(20)
pyautogui.typewrite(['tab', 'tab', 'tab', 'enter'], interval=1)

# screen os choose (familly, pro, ...)
time.sleep(2)
pydirectinput.press(['down'], presses=5)
pydirectinput.press(['enter', 'enter'])

# screen accept conditions
time.sleep(3)
pyautogui.typewrite(['space', 'tab', 'enter'], interval=1)

# screen type of installation
time.sleep(2)
pydirectinput.press(['down', 'enter', 'enter'])

# screen choose disk
time.sleep(2)
pyautogui.typewrite(['enter'], interval=1)

# Wait until the end of the installation
print("Installation...")
time.sleep(1740)


# screen region
print("End of Installation")
pyautogui.typewrite(['enter'], interval=1)

# screen keyboard
time.sleep(20)
pyautogui.typewrite(['enter'], interval=1)
time.sleep(2)
pyautogui.typewrite(['enter'], interval=1)

# screen name for the computer
print("First update")
time.sleep(240)
print("End First update")
# time.sleep(100)
pyautogui.typewrite(['tab', 'enter'], interval=1)

# screen configuration
time.sleep(20)
pyautogui.typewrite(['tab', 'tab', 'enter', 'enter'], interval=1)

# screen miscrosoft account
time.sleep(7)
pyautogui.typewrite(['tab', 'tab', 'tab', 'tab', 'enter'], interval=1)

# screen confiramtion offline account
time.sleep(3)
pyautogui.typewrite(['tab', 'tab', 'enter'], interval=1)

# screen ignore microsoft account
time.sleep(10)
pyautogui.typewrite(['tab', 'enter'], interval=1)

# screen name account
time.sleep(5)
pyautogui.typewrite(['C', 'o', 'b', 'tab', 'tab', 'tab', 'enter'], interval=1)

# screen password
time.sleep(2)
pyautogui.typewrite(['tab', 'tab', 'tab', 'enter'], interval=1)

# screen autorisation
time.sleep(20)
pyautogui.typewrite(['tab', 'tab', 'tab'], interval=1)
pydirectinput.press(['down'])
pyautogui.typewrite(['enter', 'enter'], interval=1)
pyautogui.typewrite(['tab', 'tab', 'enter'], interval=1)

time.sleep(2)
pydirectinput.press(['down'])
pyautogui.typewrite(['enter', 'enter'], interval=1)
pyautogui.typewrite(['tab', 'tab', 'enter'], interval=1)

time.sleep(2)
pydirectinput.press(['down'])
pyautogui.typewrite(['enter', 'enter'], interval=1)
pyautogui.typewrite(['tab', 'tab', 'enter'], interval=1)

time.sleep(2)
pydirectinput.press(['down'])
pyautogui.typewrite(['enter', 'enter'], interval=1)
pyautogui.typewrite(['tab', 'tab', 'enter'], interval=1)

time.sleep(2)
pydirectinput.press(['down'])
pyautogui.typewrite(['enter', 'enter'], interval=1)
pyautogui.typewrite(['tab', 'tab', 'enter'], interval=1)

time.sleep(2)
pydirectinput.press(['down'])
pyautogui.typewrite(['enter', 'enter'], interval=1)
pyautogui.typewrite(['tab', 'tab', 'enter'], interval=1)

# do some udpate
time.sleep(300)
pyautogui.typewrite(['tab'], interval=1)
pydirectinput.press(['right'], presses=5)
pyautogui.typewrite(['enter', 'enter'], interval=1)

time.sleep(5)
pydirectinput.press(['down'], presses=11)
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