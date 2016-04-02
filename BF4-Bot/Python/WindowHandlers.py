from ConfigParser import SafeConfigParser
import win32gui
import win32ui
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
        print title_text
        logging.debug("Where supplied title: " + title_text)
        self.hwnd = win32gui.FindWindow(None, title_text)
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
        logging.debug("Make pyc hwnd with handle %d" % hwnd)
        if hwnd == -1:
            logging.debug("Hwnd not supplied, using %d instead" % self.hwnd)
            hwnd = self.hwnd
        self.pycwnd = win32ui.CreateWindowFromHandle(hwnd)
        self.pycwnd
        return self.pycwnd

    def init_window(self, hwnd=-1):
        """
        At the moment only sets the window in the foreground.

        Args:
            hwnd (int): the window handle to "initialize". If not supplied
                the hwnd from the last get_hwnd_by_title will be used

        Returns:
            If the window was brought to the foreground, the return value is
                nonzero. If the window was not brought to the foreground, the
                return value is zero.
        """

        if hwnd == -1:
            hwnd = self.hwnd
        return win32gui.SetForegroundWindow(hwnd)

    def create_boundingbox(self, hwnd=-1):

        """
        Creates a bounding box of the window.

        Args:
            hwnd (int): the window handle we are going to find. If not supplied
                the hwnd from the last get_hwnd_by_title will be used

        Returns:
            Creates a touple with four elements. The upper right coordinates
                and the lower left coordinates.
        """

        if hwnd == -1:
            hwnd = self.hwnd
        logging.debug('Trying to find the box for %d' % hwnd)
        self.bbox = win32gui.GetWindowRect(hwnd)
        logging.debug('Found %s' % ','.join(map(str, self.bbox)))
        return self.bbox

    def __init__(self):

        parser = SafeConfigParser()
        parser.read('config.ini')

        self.title = parser.get('general', 'winTitle')
        self.hwnd = self.get_hwnd_by_title(self.title)
        self.pycwnd = self.make_pyc_wnd(self.hwnd)
        self.bbox = self.create_boundingbox(self.hwnd)


if __name__ == '__main__':
    wh = WinHandler()
