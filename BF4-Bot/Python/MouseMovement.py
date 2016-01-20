import win32gui
import win32api

class MouseMovement:

    self._last_x = 0
    self._last_y = 0



    def click(self, x, y, button = "left", speed = 0):
        print "Implement click"

        _button_state = {
            'left': win32con.MK_LBUTTON,
            'right': win32con.MK_RBUTTON
        }[button](x)

        _button_down = {
            'left': win32con.WM_LBUTTONDOWN,
            'right': win32con.WM_RBUTTONDOWN
        }[button](x)

        _button_up = {
            'left': win32con.WM_LBUTTONUP,
            'right': win32con.WM_RBUTTONUP
        }[button](x)

        l_param = win32api.MAKELONG(x,y)
        pycwnd.SendMessage(win32con.WM_MOUSEMOVE, 0, l_param)
        pycwnd.SendMessage(_button_down, _button_state, l_param)
        time.sleep(0.01)
        pycwnd.SendMessage(_button_up, 0, l_param)

        self._last_x = x
        self._last_y = y

    def offset_click(self, x, y, type = "left", speed = 0):
        print "Implement offset_click"

    def to_coord(self, pos_x, pos_y, win_x, win_y):
        print "Implement to_coord"

    def to_pixel(self, pos_x, pos_y, win_x, win_y):
        print "Implement to_coord"

    def __init__(self,title = "Battlefield 4"):
        self.hwnd = win32gui.FindWindowEx(0, 0, None, title)
        self.pyc_wnd = win32ui.CreateWindowFromHandle(hwnd)
        f_click(pyc_wnd)
