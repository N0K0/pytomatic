from ctypes import *
from ctypes.wintypes import *

user32 = WinDLL('user32', use_last_error=True)

HC_ACTION = 0
WH_MOUSE_LL = 14

WM_QUIT = 0x0012

MSG_TEXT = {0x0200:     'WM_MOUSEMOVE',
            0x0201:     'WM_LBUTTONDOWN',
            0x0202:     'WM_LBUTTONUP',
            0x0204:     'WM_RBUTTONDOWN',
            0x0205:     'WM_RBUTTONUP',
            0x0207:     'WM_MBUTTONDOWN',
            0x0208:     'WM_MBUTTONUP',
            0x020A:     'WM_MOUSEWHEEL',
            0x020E:     'WM_MOUSEHWHEEL'}

ULONG_PTR = WPARAM
LRESULT = LPARAM
LPMSG = POINTER(MSG)

HOOKPROC = WINFUNCTYPE(LRESULT, c_int, WPARAM, LPARAM)
LowLevelMouseProc = HOOKPROC


class MSLLHOOKSTRUCT(Structure):
    _fields_ = (('pt',          POINT),
                ('mouseData',   DWORD),
                ('flags',       DWORD),
                ('time',        DWORD),
                ('dwExtraInfo', ULONG_PTR))

LPMSLLHOOKSTRUCT = POINTER(MSLLHOOKSTRUCT)

def errcheck_bool(result, func, args):
    if not result:
        raise WinError(get_last_error())
    return args

user32.SetWindowsHookExW.errcheck = errcheck_bool
user32.SetWindowsHookExW.restype = HHOOK
user32.SetWindowsHookExW.argtypes = (c_int,     # _In_ idHook
                                     HOOKPROC,  # _In_ lpfn
                                     HINSTANCE, # _In_ hMod
                                     DWORD)     # _In_ dwThreadId

user32.CallNextHookEx.restype = LRESULT
user32.CallNextHookEx.argtypes = (HHOOK,  # _In_opt_ hhk
                                  c_int,  # _In_     nCode
                                  WPARAM, # _In_     wParam
                                  LPARAM) # _In_     lParam

user32.GetMessageW.argtypes = (LPMSG, # _Out_    lpMsg
                               HWND,  # _In_opt_ hWnd
                               UINT,  # _In_     wMsgFilterMin
                               UINT)  # _In_     wMsgFilterMax

user32.TranslateMessage.argtypes = (LPMSG,)
user32.DispatchMessageW.argtypes = (LPMSG,)

@LowLevelMouseProc
def LLMouseProc(nCode, wParam, lParam):
    msg = cast(lParam, LPMSLLHOOKSTRUCT)[0]
    if nCode == HC_ACTION:
        msgid = MSG_TEXT.get(wParam, str(wParam))
        msg = ((msg.pt.x, msg.pt.y),
                msg.mouseData, msg.flags,
                msg.time, msg.dwExtraInfo)
        print('{:15s}: {}'.format(msgid, msg))
    return user32.CallNextHookEx(None, nCode, wParam, lParam)

def mouse_msg_loop():
    hHook = user32.SetWindowsHookExW(WH_MOUSE_LL, LLMouseProc, None, 0)
    msg = MSG()
    while True:
        bRet = user32.GetMessageW(byref(msg), None, 0, 0)
        if not bRet:
            break
        if bRet == -1:
            raise WinError(get_last_error())
        user32.TranslateMessage(byref(msg))
        user32.DispatchMessageW(byref(msg))

if __name__ == '__main__':
    import time
    import threading
    t = threading.Thread(target=mouse_msg_loop)
    t.start()
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            user32.PostThreadMessageW(t.ident, WM_QUIT, 0, 0)
            break