import unittest
import win32gui
import sys
from BF_Commander import CommandAndControl
from ConfigParser import SafeConfigParser
import logging

FORMAT = "%(levelname)s-%(module)s-Line %(lineno)s: %(message)s"
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG, format=FORMAT)


class TestCommander(unittest.TestCase):
    def setUp(self):
        logging.debug("Parsing config")
        parser = SafeConfigParser()
        parser.read('config.ini')
        title = parser.get('general', 'winTitle')
        logging.debug("Looking for BF4")
        hwnd = win32gui.FindWindow(None, title)
        #assert (hwnd != 0)
        logging.debug("Found BF4")

    def test_init_window(self):
        logging.debug("Running setup test")
        cnc = CommandAndControl()
        cnc.get_win_handler().init_window(pos=[0, 0, 700, 500])
        bbox = cnc.get_win_handler().get_bbox()

        assert (len(bbox) == 4)
        assert (bbox == (0, 0, 700, 500))

    def test_hwnd_by_title(self):
        logging.debug("Running hwnd by title test")
        cnc = CommandAndControl()
        parser = SafeConfigParser()
        parser.read('config.ini')

        title = parser.get('general', 'winTitle')
        assert (title is "Battlefield 4")
        assert (win32gui.FindWindow(None, title) == cnc.get_win_handler().get_hwnd_by_title(title))

    def test_pixel_search(self):
        logging.debug("Running pixel search test")
        import WindowHandlers as wh
        import PixelSearch as ps
        import PIL
        from time import sleep
        win_handler =  wh.WinHandler('Kalkulator')
        pixel_search = ps.PixelSearch(win_handler)
        win_handler.init_window(pos=[0,0,320,510])
        sleep(1)

        file = pixel_search.grab_window()

pixel_search.grab_window("test_grab.jpg")



if __name__ == '__main__':
    unittest.main()
