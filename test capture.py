from PIL import ImageGrab
import os
import time
import cv2
import numpy
import threading
import ctypes
import winsound

template = cv2.imread('samples/7.png',0)
w, h = template.shape[::-1]

def beep(Dur):
    Freq = 2500 # Set Frequency To 2500 Hertz
    winsound.Beep(Freq,Dur)

SendInput = ctypes.windll.user32.SendInput
SPACE = 0x40
EACCENT = 0x02

# C struct redefinitions 
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Actuals Functions

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def isAFish():
    box = (752,60,813,150)
    im = ImageGrab.grab(box)
    img_rgb = cv2.cvtColor(numpy.array(im), cv2.COLOR_RGB2BGR)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    #im.save(os.getcwd() + '\\full_snap__' + str(int(time.time())) + '.png', 'PNG')
    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = numpy.where( res >= threshold)
    found = False
    
    for pt in zip(*loc[::1]):
        found = True
        break
    
    return found

def fishing():
    if(isAFish()):
        print("there is a fish")
        time.sleep(2.5)
        beep(1000)
        #PressKey(SPACE)
        #time.sleep(2.6)
        #PressKey(EACCENT)
        #time.sleep(2.6)
        #PressKey(SPACE)
    else:
        print("still waiting")

def repeatingExec():
    while(True):
        time.sleep(0.1)
        fishing()

def main():
    #time.sleep(2.6)
    #PressKey(EACCENT)
    #time.sleep(2.6)
    #PressKey(SPACE)
    #time.sleep(2.6)
    repeatingExec()
 
if __name__ == '__main__':
    main()
