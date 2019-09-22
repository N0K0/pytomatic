import os
import time
import random
from pytomatic.actions import WindowHandlers
from pytomatic.actions import PixelSearch
from pytomatic.actions import MouseMovement
import logging
import cv2
import numpy as np

logging.basicConfig(level=logging.DEBUG)

class Mousetest:
    STATE = None

    def __init__(self):
        self.win_hwnd = None
        self.mouse : MouseMovement.MouseMovement

    def find_window(self):
        print("Finding window")
        self.win_hwnd = WindowHandlers.WinHandler()
        self.win_hwnd.set_target("BlueStacks Android PluginAndroid", parent_title="BlueStacks")
        self.mouse = MouseMovement.MouseMovement(self.win_hwnd)
        print(self.win_hwnd)
        print(self.win_hwnd.get_bbox())
        return self.win_hwnd

    def main(self):
        window = self.find_window()
        bbox = window.get_bbox()
        pxs = PixelSearch.PixelSearch(window)
        self.mouse.click((0.5, 0.5))


sfws = Mousetest()
sfws.main()
