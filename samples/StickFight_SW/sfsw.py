import os
import time
import random
from pytomatic.actions import WindowHandlers
from pytomatic.actions import PixelSearch
from pytomatic.actions import MouseMovement
import logging
import cv2
import numpy as np
import imutils
from PIL import Image
from pprint import pprint

logging.basicConfig(level=logging.DEBUG)


class Sfws:
    STATE = None

    def __init__(self):
        self.win_hwnd: WindowHandlers.WinHandler
        self.mouse: MouseMovement.MouseMovement
        self.pxs: PixelSearch.PixelSearch

    def find_window(self):
        print("Finding window")
        self.win_hwnd = WindowHandlers.WinHandler()
        self.win_hwnd.set_target("BlueStacks Android PluginAndroid", parent_title="BlueStacks")
        self.mouse = MouseMovement.MouseMovement(self.win_hwnd)
        print(self.win_hwnd)
        print(self.win_hwnd.get_bbox())
        return self.win_hwnd

    def fetch_cnt_pos(self, cnt):
        pos = []
        for c in cnt:
            m = cv2.moments(c)
            cx = cy = 0
            if m["m00"] != 0:
                cx = int(m["m10"] / m["m00"])
                pos.append((cx, 0))
            else:
                continue
        return pos

    def find_enemies(self, bbox, img):
        """
        :param bbox: The bounding box of the Bluestacks window
        :param img: The image of the Bluestacks window
        :return: A touple containing list,list. Where the first list is the percentage of ready enemies. And the secondary
            is for the ready enemies
        """
        _DOT_AREA = 0.0087, 0.75, 0.997, 0.8
        _ENEMY_NOT_READY = 0x00000
        _ENEMY_READY = 0xDFDFDF
        bbox = x1, y1, x2, y2 = self.pxs.percent_to_coord_box(bbox, _DOT_AREA)
        img_enemy = img[y1:y2, x1:x2]
        # cv2.imshow('enemy_img', img_enemy)

        dots_ready = self.pxs.find_pixel_in_array(img_enemy, np.uint32(_ENEMY_READY), 3) * 255
        dots_ready = dots_ready.astype('uint8')

        dots_not_ready = self.pxs.find_pixel_in_array(img_enemy, np.uint32(_ENEMY_NOT_READY), 3) * 255
        dots_not_ready = dots_not_ready.astype('uint8')

        cnt_ready, _ = cv2.findContours(dots_ready, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        cnt_not_ready, _ = cv2.findContours(dots_not_ready, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        cv2.imshow("dots_ready", dots_ready)
        cv2.imshow("dots_not_ready", dots_not_ready)

        pos_ready = self.fetch_cnt_pos(cnt_ready)
        pos_not_ready = self.fetch_cnt_pos(cnt_not_ready)

        enemies = ([], [])

        for p in pos_ready:
            pos = self.pxs.coord_to_percent(bbox, p)
            enemies[0].append(pos)

        for p in pos_not_ready:
            pos = self.pxs.coord_to_percent(bbox, p)
            enemies[1].append(pos)

        return enemies

    def make_move_click(self, direction):
        """
        :param direction: String, left or right
        """

        _CLICK_LEFT = 0.25, 0.75
        _CLICK_RIGHT = 0.75, 0.75

        if direction == "left":
            self.mouse.click(_CLICK_LEFT)
        elif direction == "right":
            self.mouse.click(_CLICK_RIGHT)
        else:
            raise ValueError("left or right is needed")

    def make_move(self, bbox, img):
        ready, not_ready = self.find_enemies(bbox, img)

        if len(ready) > 0:
            target = ready.pop()
            if target[0] < 0.5:
                self.make_move_click("left")
            else:
                self.make_move_click("right")

        time.sleep(0.1)

    def start_game(self):
        print("Starting game")
        _START_CLICK_COORD = 0.485, 0.882
        self.mouse.click(_START_CLICK_COORD)
        print("Click")

    def find_state(self, bbox, img):
        print("Finding state")
        # Possible states:
        #   Main menu:
        #       Check for the burger menu in the corner
        #
        _MENU_CHECK_AREA = 0.9168, 0.8705, 0.9480, 0.8798
        _MENU_CHECK_COLOR = 0xFFFFFF
        x1, y1, x2, y2 = self.pxs.percent_to_coord_box(bbox, _MENU_CHECK_AREA)
        menu_img = img[y1:y2, x1:x2]
        cv2.imshow("menu", menu_img)
        menu_img = self.pxs.aproximate_color_3d(menu_img, _MENU_CHECK_COLOR, 1)
        if np.all(menu_img):
            print("Setting state menu")
            self.STATE = "running"
            self.start_game()
        elif self.STATE == "running":
            print("Setting running")
            self.make_move(bbox, img)

        # How do you figure out if im currently in an ad or in the game?

    def main(self):
        window = self.find_window()
        bbox = window.get_bbox()
        self.pxs = PixelSearch.PixelSearch(window)
        while True:
            image = self.pxs.grab_window()
            img = self.pxs.img_to_numpy(image)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

            cv2.imshow('image_name', img)
            cv2.setMouseCallback('image_name', self.pxs.print_win_percentage_click, bbox)

            self.find_state(bbox, img)

            k = cv2.waitKey(1)
            if k == ord('q'):  # wait for ESC key to exit
                cv2.destroyAllWindows()
                quit(0)


sfws = Sfws()
sfws.main()
