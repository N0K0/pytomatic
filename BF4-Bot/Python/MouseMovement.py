import win32gui
import win32api
import win32ui
import win32con
import time

class MouseMovement:

    def click(self, coords, button = "left"):

        if all(isinstance(elem,float) for elem in coords):
            coords = to_pixel(coords)

        x = coords[0]
        y = coords[1]

        if "right" in button.lower():
            _button_state = win32con.MK_RBUTTON
            _button_down = win32con.WM_RBUTTONDOWN
            _button_up = win32con.WM_RBUTTONUP
        elif "left" in button.lower():
            _button_state = win32con.MK_LBUTTON
            _button_down = win32con.WM_LBUTTONDOWN
            _button_up = win32con.WM_LBUTTONUP
        else:
            return 1

        l_param = win32api.MAKELONG(x,y)
        self.pycwnd.SendMessage(win32con.WM_MOUSEMOVE, 0, l_param)
        self.pycwnd.SendMessage(_button_down, _button_state, l_param)
        time.sleep(0.01)
        self.pycwnd.SendMessage(_button_up, 0, l_param)

        self._last_x = x
        self._last_y = y
        return 0

    def offset_click(self, x, y, button = "left"):
        self.click([coords[0] + x, coords[1] + y], button)


    def to_coord(self, pos_x, pos_y, win_x, win_y):
        print "Implement to_coord"

    def to_pixel(self, coords, win_coords):
        #Modes:
        #
        #0: Returns tuple
        #1: Returns x
        #2: Returns y

        return coords

        print "Implement to_coord"

    def __init__(self,title = "Battlefield 4"):
        self._last_x = 0
        self._last_y = 0
        self.hwnd = win32gui.FindWindowEx(0, 0, None, title)
        self.pycwnd = win32ui.CreateWindowFromHandle(self.hwnd)
