import time
import win32api

import win32con
import logging

from pytomatic.actions.Helpers import to_pixel

FORMAT = "%(levelname)s-%(module)s-Line %(lineno)s: %(message)s"


# logging.basicConfig(stream='mouse.log', level=logging.DEBUG, format=FORMAT)

# https://msdn.microsoft.com/en-us/library/windows/desktop/ms646260(v=vs.85).aspx
class MouseMovement:
    def resolve_mouse_events(self, button="left"):
        """
        :param button: which button
        :return: _button_state, _button_down, _button_up
        """
        if "right" in button.lower():
            _button_state = win32con.MK_RBUTTON
            _button_down = win32con.WM_RBUTTONDOWN
            _button_up = win32con.WM_RBUTTONUP
        elif "left" in button.lower():
            _button_state = win32con.MK_LBUTTON
            _button_down = win32con.WM_LBUTTONDOWN
            _button_up = win32con.WM_LBUTTONUP
        elif "middle" in button.lower():
            _button_state = win32con.MK_MBUTTON
            _button_down = win32con.WM_MBUTTONDOWN
            _button_up = win32con.WM_MBUTTONUP
        else:
            raise SyntaxError('"Button" needs to contain "left", "right" or "middle"')

        return _button_state, _button_down, _button_up

    def click_new(self, coords, button="left", hold=False):
        mouse_evt = win32api.mouse_event()

    def click(self, coords, button="left", hold=False):
        """
        Args:
            coords (touple): coords takes two arguments, either both float
                or int. If float is supplied, it will try to treat them as
                percentages. X, Y
            button (string): either "left","right" or "middle". Decides what button that
                will be sent to the running program.

        Returns:
            bool: True if successful, False otherwise.

        Raises:
            SyntaxError: The button param does not contain "left","right og "middle"
            :param hold:
        """

        hwnd = self.win_handler.get_hwnd()
        bbox = self.win_handler.get_bbox_size()

        if all(isinstance(elem, float) for elem in coords):
            coords = to_pixel(coords, bbox)

        logging.debug("Trying to click on:" + str(coords) + " with " + button + " button")

        x = coords[0]
        y = coords[1]

        _button_state, _button_down, _button_up = self.resolve_mouse_events(button.lower())

        l_param = win32api.MAKELONG(x, y)

        win32api.SendMessage(hwnd, win32con.WM_MOUSEMOVE, 0, l_param)

        time.sleep(0.1)
        win32api.SendMessage(hwnd, _button_down, _button_state, l_param)
        time.sleep(0.05)

        if not hold:  # Do not release the button if hold is true
            win32api.SendMessage(hwnd, _button_up, 0, l_param)

        self._last_x = x
        self._last_y = y
        return True

    def release_button(self, coords, button="left"):

        _button_state, _button_down, _button_up = self.resolve_mouse_events(button.lower())

        if all(isinstance(elem, float) for elem in coords):
            coords = to_pixel(self.win_handler, coords)
        x = coords[0]
        y = coords[1]

        l_param = win32api.MAKELONG(x, y)

        hwnd = self.win_handler.get_hwnd()
        win32api.SendMessage(hwnd, _button_up, 0, l_param)

        raise NotImplementedError

    def offset_click(self, x, y, button="left"):
        """
        Args:
            x (int): The offset in the left/right direction
            y (int): The offset in the up/down direction
            button (string): either "left" or "right". Decides what button that
                will be sent to the running program.
        Returns:
            bool: True if successful, False otherwise.

        Raises:
            SyntaxError: The button param does not contain "left" or "right"
        """

        if all(isinstance(elem, float) for elem in [x, y]):
            bbox = self.win_handler.create_boundingbox()
            x,y = to_pixel([x,y],bbox)

        return self.click([self._last_x + x, self._last_y + y], button)

    def move(self, coords, button="left"):
        if all(isinstance(elem, float) for elem in coords):
            bbox = self.win_handler.create_boundingbox()
            coords = to_pixel(coords,bbox)

        _button_state, _button_down, _button_up = self.resolve_mouse_events(button.lower())
        l_param = win32api.MAKELONG(coords[0], coords[1])
        win32api.PostMessage(self.win_handler.get_hwnd(), win32con.WM_MOUSEMOVE, _button_state, l_param)

    def hold_and_drag(self, start, end, steps, button="left"):
        hwnd = self.win_handler.get_hwnd()

        if all(isinstance(elem, float) for elem in start):
            start = to_pixel(self.win_handler, start)

        if all(isinstance(elem, float) for elem in end):
            end = to_pixel(self.win_handler, end)

        step_x = (float(end[0] - start[0])) / steps
        step_y = (float(end[1] - start[1])) / steps

        _button_state, _button_down, _button_up = self.resolve_mouse_events(button.lower())

        self.move(start)
        l_param = win32api.MAKELONG(start[0], start[1])

        time.sleep(0.1)
        win32api.SendMessage(hwnd, _button_down, _button_state, l_param)
        time.sleep(0.1)

        x, y = start
        for step in range(0, steps):
            x += step_x
            y += step_y
            self.move((int(x), int(y)), button=button)
            time.sleep(0.01)

        l_param = win32api.MAKELONG(int(x), int(y))
        win32api.SendMessage(hwnd, _button_up, 0, l_param)
        self._last_x = x
        self._last_y = y


    # TODO: Move into common folder, make it accept bbox too
    def to_ratio(self, coords):
        size_vertical, size_horizontal = self.win_handler.get_bbox_size()

        x, y = coords[0] / size_horizontal, coords[1] / size_vertical
        return float(x), float(y)

    def click_centre(self, bbox, button="left"):
        return self.click()

    def __init__(self, window_handler):
        self._last_x = 0
        self._last_y = 0
        self.win_handler = window_handler
        self._pycwnd = self.win_handler.get_pycwnd()
        self.window_size = self._pycwnd.GetWindowPlacement()[4]
