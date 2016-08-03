import logging
import unittest
import win32gui
from ConfigParser import SafeConfigParser
from time import sleep

import numpy as np
import win32con
from PIL import Image

from BF_Commander import CommandAndControl
from src.actions import PixelSearch as ps
from src.actions import WindowHandlers as wh
from src.actions import MouseMovement as mm


class TestCommander(unittest.TestCase):
    def setUp(self):
        logging.debug("Parsing config")
        parser = SafeConfigParser()
        parser.read('config.ini')
        title = parser.get('general', 'winTitle')
        logging.debug("Looking for BF4")
        hwnd = win32gui.FindWindow(None, title)
        # assert (hwnd != 0)
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

    def test_window_grab(self):
        logging.debug("Running pixel search test")

        win_handler = wh.WinHandler('Kalkulator')
        pixel_search = ps.PixelSearch(win_handler)
        win_handler.init_window(pos=[0, 0, 320, 510])
        sleep(1)
        pixel_search.grab_window('pixel_search.png')

        file = pixel_search.grab_window('pixel_search.png')
        im = Image.open('pixel_search_sample.png')
        im = Image.Image.crop(im, (20, 20, 200, 200))
        im.load()
        im2 = Image.Image.crop(file, (20, 20, 200, 200))
        im2.load()

        mat1 = im.tobytes()
        mat2 = im2.tobytes()
        assert (mat1 == mat2)

    def test_pixel_search(self):
        logging.debug("Running pixelsearch test")
        win_handler = wh.WinHandler('Kalkulator')
        pixel_search = ps.PixelSearch(win_handler)
        win_handler.init_window(pos=(0, 0, 320, 510))
        sleep(1)
        im = Image.open('pixel_search_sample.png')
        array = np.array(im)
        print array

    def test_manipulate_ui(self):
        logging.debug('Starting UI test')

        win_handler = wh.WinHandler('Kalkulator')

        hwnd = win_handler.get_hwnd()
        style_base = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)

        win_handler.hide_extra_ui()
        style_removed = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        assert style_base != style_removed

        win_handler.hide_extra_ui(remove=False)
        style_added = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        assert style_removed != style_added

    def test_basic_commander(self):
        logging.debug("Running a basic test of the commander functions")

        parser = SafeConfigParser()
        parser.read('config.ini')
        color = parser.get('PixelScan', 'redColor')
        color = int(color, 16)
        win_handler = wh.WinHandler()
        pixel_search = ps.PixelSearch(win_handler)
        mouse_handler = mm.MouseMovement(win_handler)

        bbox = win_handler.get_bbox()
        bbox_size = win_handler.get_bbox_size()
        win_handler.init_window(borderless=True)
        sleep(0.1)

        px = pixel_search.pixel_search(color, shades=2, debug='check.png')

        places = np.nonzero(px)

        for hit in range(len(places[0])):
            mouse_handler.click((places[1][hit], places[0][hit]))
            sleep(1)

    def test_basic_commands(self):
        win_handler = wh.WinHandler()
        pixel_handler = ps.PixelSearch(win_handler)
        mouse_handler = mm.MouseMovement(win_handler)

        com = CommandAndControl(win_handler, pixel_handler, mouse_handler)

        com.use_UAV((0.5, 0.5))
        sleep(2)
        com.use_EMP((0.4, 0.4))


if __name__ == '__main__':
    unittest.main()
