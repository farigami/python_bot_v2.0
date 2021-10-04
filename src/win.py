from win32 import win32gui, win32process
from time import sleep
import win32con

class Win:
    def findWindow(self, hwnd, windowClass):
        return win32gui.FindWindow(hwnd, windowClass)

    def setWindowText(self, hwnd, windowCaption):
        win32gui.SetWindowText(hwnd, windowCaption)
    
    def getWindowThreadProcessId(self, hwnd):
        return win32process.GetWindowThreadProcessId(hwnd)[1]
    
    def postMessage(sellf, hwnd, key):
        win32gui.PostMessage(hwnd, win32con.WM_KEYDOWN, key, 0)
        sleep(0.05)
        win32gui.PostMessage(hwnd, win32con.WM_KEYUP, key, 0)
    
    def getWindowCaption(self, hwnd):
        return win32gui.GetWindowText(hwnd)