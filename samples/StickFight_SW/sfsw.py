import os
import time
import random
from pytomatic.actions import WindowHandlers
from pytomatic.actions import PixelSearch
from pytomatic.actions import MouseMovement
import logging
import cv2
import numpy as np

class Sfws:
    STATE = None

    def find_window(self):
        win_hwnd = WindowHandlers.WinHandler(title="Bluestacks")
        print(win_hwnd)
        print(win_hwnd.get_bbox())
        return win_hwnd

    def fetch_screen(self):
        pass


    def find_enemies(self):
        pass


    def find_state(self,pxs, bbox, img):
        # Possible states:
        #   Main menu:
        #       Check for the burger menu in the corner
        #
        _MENU_CHECK_AREA = 0.8887, 0.87576, 0.93483, 0.88376
        _MENU_CHECK_COLOR = 0xFFFFFF
        x1, y1, x2, y2 = pxs.percent_to_coord_box(bbox, _MENU_CHECK_AREA)
        menu_img = img[y1:y2, x1:x2]
        menu_img = pxs.aproximate_color_3d(menu_img, _MENU_CHECK_COLOR, 1)
        if np.all(menu_img):
            if self.STATE != "menu":
                print("Setting state menu")
                self.STATE = "menu"

        # How do you figure out if im currently in an ad or in the game?

    def main(self):
        window = self.find_window()
        bbox = window.get_bbox()
        pxs = PixelSearch.PixelSearch(window)
        while True:
            image = pxs.grab_window()
            img = pxs.img_to_numpy(image)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

            cv2.imshow('image_name', img)
            cv2.setMouseCallback('image_name', pxs.print_win_percentage_click, bbox)

            self.find_state(pxs, bbox, img)

            k = cv2.waitKey(1)
            if k == ord('q'):  # wait for ESC key to exit
                cv2.destroyAllWindows()
                quit(0)


sfws = Sfws()
sfws.main()