import numpy as np
from time import time, sleep
import win32gui
import win32ui
import win32con
import cv2
import keyboard

def screenshot(w=800, h=450):
    hwnd = win32gui.FindWindow(None, "Trackmania")
    x, y, x1, y1 = win32gui.GetWindowRect(hwnd)
    if x1-x == w:
        # fullscreen
        borders = (0, 0)
    else:
        # window
        borders = (8, 31)
    wDC = win32gui.GetWindowDC(hwnd)
    dcObj = win32ui.CreateDCFromHandle(wDC)
    cDC = dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0, 0), (w, h), dcObj, borders, win32con.SRCCOPY)
    img_array = dataBitMap.GetBitmapBits(True)
    img = np.frombuffer(img_array, dtype='uint8')
    img.shape = (h, w, 4)
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())

    return cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)

