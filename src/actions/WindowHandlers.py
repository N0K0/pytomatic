from ConfigParser import SafeConfigParser
import win32gui
import win32ui
from ctypes import windll

import win32con
import logging
import sys


FORMAT = "%(levelname)s-%(module)s-Line %(lineno)s: %(message)s"
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG, format=FORMAT)


class WinHandler:
    def get_hwnd_by_title(self, title_text=""):
        """ Returns a windows window_handler

        Args:
            title_text (string): the title of the window we are looking for

        Returns:
            int: the handler for the window if found

        Raises:
            win32.error: If the windowtitle is invalid

        """
        logging.debug("Where supplied title: " + title_text)
        self.hwnd = win32gui.FindWindow(None, title_text)

        if self.hwnd == 0:
            raise ValueError('Unable to find a window with that title')

        return self.hwnd

    def make_pyc_wnd(self, hwnd=-1):
        """
        Creates a python window object from the hwnd handle found earlier

        Args:
            hwnd (int): The title of the window we are looking for
                if hwnd is not supplied, it will use the one found in an earlier
                call to get_hwnd_by_title

        Returns:
            pycwnd: a handle to the window we are looking for

        """
        logging.debug("Make pyc hwnd with handle 0x%x" % hwnd)
        if hwnd == -1:
            logging.debug("Hwnd not supplied, using %x instead" % self.hwnd)
            hwnd = self.hwnd

        if hwnd == 0:
            raise ValueError('Hwnd is not a valid handle or window not found')

        self.pycwnd = win32ui.CreateWindowFromHandle(hwnd)
        return self.pycwnd

    def init_window(self, hwnd=None, pos=None, borderless=False, config = None):
        """
        At the moment only sets the window in the foreground and moves it to a posistion set in the config.

        Args:
            hwnd (int): the window handle to "initialize". If not supplied
                the hwnd from the last get_hwnd_by_title will be used
            pos (tuple): a tuple describing the X,Y,Height and Width of the window
            borderless (Bool): Removes extra styling like borders if true. Can be reapplied with:
                hide_extra_ui(hwnd,remove=False)
        Returns:
            If the window was brought to the foreground, the return value is
                nonzero. If the window was not brought to the foreground, the
                return value is zero.
        """

        if hwnd is None:
            hwnd = self.hwnd

        logging.debug("Init window (0x%x)" % hwnd)

        if pos is None:
            pos = None

            if config is not None:
                config = SafeConfigParser()
                config.read('config.ini')
                pos = config.get('general', 'winPos').split(',')
                pos = map(int, pos)

        if borderless:
            self.hide_extra_ui()

        if pos is not None:
            self.move(pos, hwnd)
        return win32gui.SetForegroundWindow(hwnd)
    def move(self, pos, hwnd=None):
        """
        :param pos: A tuple describing the (X,Y,Width,Height) of the window OR
            A tuple describing the (X,Y) coordinates of the top right windows position
        :param hwnd: Move supplied window. If not supplied, then the default window is moved
        :return: The window handle
        """

        if hwnd is None:
            hwnd = self.get_hwnd()


        if len(pos) == 4:
            win32gui.MoveWindow(hwnd, pos[0], pos[1], pos[2], pos[3], 1)
        if len(pos) == 2:
            win_size = self.get_bbox_size()
            win32gui.MoveWindow(hwnd,pos[0],pos[1],win_size[0],win_size[1], 1)

    def hide_extra_ui(self, hwnd=None, remove=True):
        """
        :param hwnd: Hwnd to remove all styling from. If not supplied, then the default hwnd is used
        :param remove: If true: Removes all styling. If false: Adds back the removed styles
        :return: NoneType
        """

        logging.debug('Trying to manipulate UI')

        if hwnd is None:
            hwnd = self.get_hwnd()

        style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)

        if remove:
            logging.debug('Removing UI')
            style = style | win32con.WS_POPUP
            style = style & ~win32con.WS_OVERLAPPEDWINDOW
        else:
            logging.debug('Adding UI')
            style = style & ~win32con.WS_POPUP
            style = style | win32con.WS_OVERLAPPEDWINDOW

        win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
        win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, style)
        win32gui.ShowWindow(hwnd, win32con.SW_SHOW)

    def create_boundingbox(self, hwnd=None,windows_style=False):
        """
        Creates a bounding box of the window.

        Args:
            hwnd (int): the window handle we are going to find. If not supplied
                the hwnd from the last get_hwnd_by_title will be used

        Returns:
            Creates a tuple with four elements. The upper right coordinates
                and the lower left coordinates.
        """

        if hwnd == None:
            hwnd = self.hwnd
        logging.debug('Trying to find the box for 0x%x' % hwnd)

        self.bbox = win32gui.GetWindowRect(hwnd)
        logging.debug('Found %s' % ','.join(map(str, self.bbox)))

        if windows_style:
            pos_size = self.get_bbox_size(self.get_bbox())
            return ()
        else:
            return self.bbox

    def create_boundingbox_from_coords(self, coords, hwnd=None):

        if not hwnd:
            hwnd = self.hwnd

        bounding_box = self.create_boundingbox(hwnd)
        bounding_box = coords[0] * bounding_box[2], coords[1] * bounding_box[3], coords[2] * bounding_box[2], \
                       coords[3] * bounding_box[3]
        bounding_box = map(int, bounding_box)
        return bounding_box

    def get_bbox(self,hwnd=None):
        '''
        :return: A tuple with two elements. Containing the width and height of the default window
        '''
        if hwnd is None:
            hwnd = self.get_hwnd()

        return self.create_boundingbox(hwnd)

    def get_bbox_size(self, hwnd=None):
        """
        :param hwnd: If supplied: Calculates the size of boundingbox for the given handle.
            If not:  the boundingbox for the default window
        :return: a tuple, with the (width, height) data
        """

        if hwnd is None:
            hwnd = self.get_hwnd()

        bbox = self.get_bbox()
        bbox_size = bbox[2] - bbox[0], bbox[3] - bbox[1]
        logging.debug('Found following size: %d, %d' % (bbox[2] - bbox[0], bbox[3] - bbox[1]))
        return bbox_size

    def __init__(self, title,config=None):

        if config is not None:
            parser = SafeConfigParser()
            parser.read(config)
            self.title = parser.get('general', 'winTitle')
        else:
            self.title = title

        self.hwnd = self.get_hwnd_by_title(self.title)
        self.pycwnd = self.make_pyc_wnd(self.hwnd)
        self.bbox = None

    def get_pycwnd(self):
        return self.pycwnd

    def get_hwnd(self):
        return self.hwnd

    def get_title(self):
        return self.title


if __name__ == '__main__':
    wh = WinHandler()
