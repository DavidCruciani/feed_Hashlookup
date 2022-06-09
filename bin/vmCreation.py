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
pydirectinput.press(['f10', 'alt'], interval=1)
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
    time.sleep(2)
    pyautogui.press(['1', '1'])
    time.sleep(2)
    pydirectinput.press(['enter'])

    time.sleep(1)
    pyautogui.typewrite(['tab', 'tab'], interval=1)
