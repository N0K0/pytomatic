import time
import win32api
import win32con
import logging
import sys

FORMAT = "%(levelname)s-%(module)s-Line %(lineno)s: %(message)s"
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG, format=FORMAT)


class MouseMovement:
    def click(self, coords, button="left"):
        """
        Args:
            coords (touple): coords takes two arguments, either both float
                or int. If float is supplied, it will try to treat them as
                percentages.
            button (string): either "left","right" or "middle". Decides what button that
                will be sent to the running program.

        Returns:
            bool: True if successful, False otherwise.

        Raises:
            SyntaxError: The button param does not contain "left","right og "middle"
        """


        if all(isinstance(elem, float) for elem in coords):
            coords = self.to_pixel(coords)

        logging.debug("Trying to click on:" + str(coords) + " with " + button + " button")


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
        elif "middle" in button.lower():
            _button_state = win32con.MK_MBUTTON
            _button_down = win32con.WM_MBUTTONDOWN
            _button_up = win32con.WM_MBUTTONUP
        else:
            raise SyntaxError('Button needs to contain "left", "right" or "middle"')

        l_param = win32api.MAKELONG(x, y)
        self._pycwnd.SendMessage(win32con.WM_MOUSEMOVE, 0, l_param)
        self._pycwnd.SendMessage(_button_down, _button_state, l_param)
        time.sleep(0.2)
        self._pycwnd.SendMessage(_button_up, 0, l_param)

        self._last_x = x
        self._last_y = y
        return True

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

        if all(isinstance(elem, float) for elem in [x,y]):
            x,y = self.to_pixel([x,y])

        return self.click([self._last_x + x, self._last_y + y], button)

    def to_coord(self, pos_x, pos_y):
        print "Implement to_coord"
        raise NotImplementedError

    def to_pixel(self, coords):
        """
        Args:
            coords (touple): a pair of floating point numbers between 0.0 and 1.0
                representing a percentage of the screen in the x/y directions
        Returns:
            touple: a pair of integers representing the actual coordinates in
                the form of pixels
        """



        self.window_size = self._pycwnd.GetWindowPlacement()[4]
        size_vert = int(self.window_size[3] - self.window_size[1])
        size_horiz = int(self.window_size[2] - self.window_size[0])
        x, y = coords[0] * size_horiz, coords[1] * size_vert

        return int(x), int(y)

    def __init__(self, window_handler):
        self._last_x = 0
        self._last_y = 0
        self._win_handler = window_handler
        self._pycwnd = self._win_handler.get_pycwnd()
        self.window_size = self._pycwnd.GetWindowPlacement()[4]
