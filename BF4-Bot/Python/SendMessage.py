#This is a testfile for the SendMessage functionality, lets see if bf4 support this
import win32api, win32con, win32gui, win32ui, win32service, os, time
import time

def f_click(pycwnd):
    time.sleep(1)
    l_param = win32api.MAKELONG(15,90)
    pycwnd.SendMessage(win32con.WM_MOUSEMOVE, 0, l_param)
    pycwnd.SendMessage(win32con.WM_RBUTTONDOWN, win32con.MK_RBUTTON, l_param);
    time.sleep(0.2)
    pycwnd.SendMessage(win32con.WM_RBUTTONUP, 0, l_param);


def make_pycwnd(hwnd):

    return PyCWnd

hwnd = win32gui.FindWindowEx(0, 0, None, 'Battlefield 4')
pyc_wnd = win32ui.CreateWindowFromHandle(hwnd)
f_click(pyc_wnd)
