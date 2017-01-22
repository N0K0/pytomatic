import win32gui
import win32ui
from ctypes import windll


import win32api
import win32con
import logging
import sys


FORMAT = "%(levelname)s-%(module)s-Line %(lineno)s: %(message)s"
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG, format=FORMAT)


class WinHandler:
    def get_hwnd_by_title_class(self, class_text = None, title_text= None, parent_title = None,parent_class = None):

        """ Returns a windows window_handler

        Args:
            title_text (string): the title of the window we are looking for
            SPECIAL CASE: if "desktop:n" is given, a handle to the desktop number n handle is given

        Returns:
            int: the handler for the window if found

        Raises:
            win32.error: If the windowtitle is invalid

        """

        if 'desktop:' in title_text.lower():
            _ , num = title_text.lower().split(':',1)
            num = int(num)
            monitors = win32api.EnumDisplayMonitors()
            tar_mon = monitors[num]
            self.hwnd = tar_mon[1]
            return self.hwnd

        if title_text.lower() == "desktop":
            self.hwnd = win32gui.GetDesktopWindow()
            return self.hwnd

        child_hwnd = []
        def child_enumerator(hwnd,param):
            child_hwnd.append(hwnd)
            return True

        if parent_title is not None or parent_class is not None:
            logging.debug("Where supplied title/class: {0}/{1}".format(str(title_text), str(class_text)))
            parent_hwnd = self.get_hwnd_by_title_class(class_text=parent_class,title_text=parent_title)
            win32gui.EnumChildWindows(parent_hwnd,child_enumerator,None)

            for hwnd in child_hwnd:
                hwnd_title = win32gui.GetWindowText(hwnd)
                hwnd_class = win32gui.GetClassName(hwnd)
                if (hwnd_title == title_text and title_text is not None) or \
                    (hwnd_class == class_text and class_text is not None):
                    self.hwnd = hwnd
                    return hwnd

            # logging.debug("Found parent with title/class {0}{1} at {2}".format(parent_title,parent_class,parent_hwnd))
            # self.hwnd = win32gui.FindWindowEx(parent_hwnd,0,class_text,title_text)
        else:
            logging.debug("Where supplied title/class: {0}/{1}".format(str(title_text), str(class_text)))
            self.hwnd = win32gui.FindWindow(class_text, title_text)


        if self.hwnd == 0:
            raise ValueError('Unable to find a window with that title or class')

        return self.hwnd

    def make_pyc_wnd(self, hwnd=None):
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
        if hwnd is None:
            logging.debug("Hwnd not supplied, using {} instead".format(self.hwnd))
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
            hwnd = self.get_hwnd()

        logging.debug("Init window (0x%x)" % hwnd)

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

    def create_boundingbox(self, hwnd = None, windows_style=False):
        """
        Creates a bounding box of the window.

        Args:
            hwnd (int): the window handle we are going to find. If not supplied
                the hwnd from the last get_hwnd_by_title will be used

        Returns:
            Creates a tuple with four elements. The upper left coordinates
                and the lower right coordinates. (left, top, right,buttom window borders)
        """

        if hwnd is None:
            hwnd = self.get_hwnd()

        logging.debug('Trying to find the box for {}'.format(hwnd))

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
        """
        Creates a tuple with four elements. The upper right coordinates
                and the lower left coordinates.
        """

        return self.create_boundingbox(hwnd)

    def get_bbox_size(self, hwnd=None):
        """
        :param hwnd: If supplied: Calculates the size of boundingbox for the given handle.
            If not:  the boundingbox for the default window

        :return: a tuple, with the (width, height) data
        """


        bbox = self.get_bbox()
        bbox_size = bbox[2] - bbox[0], bbox[3] - bbox[1]
        logging.debug('Found following size: %d, %d' % (bbox[2] - bbox[0], bbox[3] - bbox[1]))
        return bbox_size

    def bbox_scale(self,bbox, scale):
        """
        Args:
            bbox: A bounding box to scale
            scale: The target scale for the matrix

        Returns:
            A new boundingbox with the new scale
        """

        def percent_in_range(start,stop,scale):
            return ((stop - start) * scale) + start

        centre = bbox[0] + (bbox[2] - bbox[0]) / 2 ,bbox[1]+ (bbox[3]-bbox[1]) / 2

        left    = int(percent_in_range(centre[0],bbox[0],scale))
        right   = int(percent_in_range(centre[0],bbox[2],scale))
        top     = int(percent_in_range(centre[1],bbox[1],scale))
        bottom  = int(percent_in_range(centre[1],bbox[3],scale))
        scaled_box = (left,top,right,bottom)

        logging.debug("Scaled bbox: {} ({}%) -> {}".format(bbox,scale*100,scaled_box))

        return scaled_box

    def __init__(self, title = None,class_name = None,config=None):
        self.hwnd = None
        self.pycwnd = None
        self.bbox = None

        self.title = title
        self.class_name = class_name

        if self.title is not None or self.class_name is not None:
            self.hwnd = self.get_hwnd_by_title_class(self.class_name, self.title)
            self.pycwnd = self.make_pyc_wnd(self.hwnd)
            self.bbox = None
        else:
            logging.warning("NOTE: No valid initializers for the window handler, user set_target() to set a window")

    def get_pycwnd(self):
        return self.pycwnd

    def get_hwnd(self):
        return self.hwnd

    def get_title(self):
        return self.title

    def set_hwnd(self,hwnd):
        self.hwnd = hwnd
        self.pycwnd = self.make_pyc_wnd(hwnd)

    def get_desktop_stats(self):
        left = windll.user32.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
        top = windll.user32.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
        width = windll.user32.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        height = windll.user32.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)

        logging.debug("Desktop stats: Origo: {}\tSize: {}".format((left,top),(width,height)))
        return left,top,width,height



    def translate_virt_to_real(self,pos):
        """
        This function takes a boundingbox found in the virutal space (IE where negative coordinates are possible
            and origo is on the primary screen) and outputs them as absolute coordinates where origo is top-left og all
            screens. The boundingbox needed is created by the create_boundingbox() function
        Args:
            pos: (left,top,right,buttom)

        Returns:
            translated (X_pox, Y_pos, windows_width, window_height)
        """

        left, top, _, _ = self.get_desktop_stats()

        translated = (pos[0]-left,pos[1]-top,pos[2]-left,pos[3]-left)
        logging.debug("Virt to real: {} -> {}".format(pos,translated))

        return translated

    def set_target(self,title_name=None,class_name=None,parent_title=None,parent_class=None):
        logging.debug('Setting target:\n\tTitle: {1}\n\tClass: {0}\n\tParent title:{2}\n\tParent class: {3}\n'
                      .format(class_name,title_name,parent_title,parent_class))
        self.hwnd = self.get_hwnd_by_title_class(class_name,title_name,parent_title,parent_class)
        self.pycwnd = self.make_pyc_wnd(self.hwnd)
        self.title = title_name
        self.class_name = class_name


if __name__ == '__main__':
    wh = WinHandler()
