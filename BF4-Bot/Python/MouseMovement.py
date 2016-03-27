import win32gui
import win32api
import win32ui
import win32con
import time

class MouseMovement:

    def click(self, coords, button = "left"):
        '''
        Args:
            coords (touple): coords takes two arguments, either both float
                or int. If float is supplied, it will try to treat them as
                percentages.
            button (string): either "left" or "right". Decides what button that
                will be sent to the running program.

        Returns:
            bool: True if successful, False otherwise.

        Raises:
            SyntaxError: The button param does not contain "left" or "right"
        '''

        print coords

        if all(isinstance(elem,float) for elem in coords):
            coords = self.to_pixel(coords)

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
            raise SyntaxError('Button needs to contain either "left" or "right"')

        l_param = win32api.MAKELONG(x,y)
        self.pycwnd.SendMessage(win32con.WM_MOUSEMOVE, 0, l_param)
        self.pycwnd.SendMessage(_button_down, _button_state, l_param)
        time.sleep(0.2)
        self.pycwnd.SendMessage(_button_up, 0, l_param)

        self._last_x = x
        self._last_y = y
        return True

    def offset_click(self, x, y, button = "left"):
        '''
        Args:
            x (int): The offset in the left/right direction
            y (int): The offset in the up/down direction
            button (string): either "left" or "right". Decides what button that
                will be sent to the running program.
        Returns:
            bool: True if successful, False otherwise.

        Raises:
            SyntaxError: The button param does not contain "left" or "right"
        '''

        return self.click([coords[0] + x, coords[1] + y], button)


    def to_coord(self, pos_x, pos_y):
        print "Implement to_coord"
        raise NotImplementedError


    def to_pixel(self, coords):
        '''
        Args:
            coords (touple): a pair of floating point numbers between 0.0 and 1.0
                representing a percentage of the screen in the x/y directions
        Returns:
            touple: a pair of integers representing the actual coordinates in
                the form of pixels
        '''
        
        self.window_size = self.pycwnd.GetWindowPlacement()[4]
        size_vert = int(self.window_size[3]-self.window_size[1])
        size_horiz = int(self.window_size[2]-self.window_size[0])
        x,y = coords[0]*size_horiz,coords[1]*size_vert

        return (int(x),int(y))


    def __init__(self,title = "Battlefield 4"):
        self._last_x = 0
        self._last_y = 0
        make_pyc_wnd()
        self.window_size = self.pycwnd.GetWindowPlacement()[4]
