import asyncio
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

logging.basicConfig(level=logging.WARNING)

ATK_COOLDOWN_AMOUNT = 10  # Number of ticks waiting between attacks


class Sfws:
    STATE = None

    def fire_and_forget(f):
        def wrapped(*args, **kwargs):
            return asyncio.get_event_loop().run_in_executor(None, f, *args, *kwargs)

        return wrapped

    def __init__(self):
        self.win_hwnd: WindowHandlers.WinHandler
        self.mouse: MouseMovement.MouseMovement
        self.pxs: PixelSearch.PixelSearch
        self.tick = 0
        self.atk_cooldown = 0

    def find_window(self):
        print("Finding window")
        self.win_hwnd = WindowHandlers.WinHandler()
        self.win_hwnd.set_target("BlueStacks Android PluginAndroid", parent_title="BlueStacks")
        self.mouse = MouseMovement.MouseMovement(self.win_hwnd)
        print(self.win_hwnd)
        print(self.win_hwnd.get_bbox())
        return self.win_hwnd

    def fetch_cnt_pos_2d(self,cnt):
        pos = []
        for c in cnt:
            m = cv2.moments(c)
            cx = cy = 0
            if m["m00"] != 0:
                cx = int(m["m10"] / m["m00"])
                cY = int(m["m01"] / m["m00"])
                pos.append((cx, cY))
            else:
                continue
        return pos

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

    def figure_out_ad(self, bbox, img):
        """
        Will try to find all the different types of ads we might encounter.
        :param bbox:
        :param img:
        :return:
        """

        # Normal X in the corner
        CLOSE_AD_COLOR = 0x7C7C7C
        CLOSE_AD_AREA = 0.918, 0.05, 0.999, 0.15
        x1, y1, x2, y2 = self.pxs.percent_to_coord_box(bbox, CLOSE_AD_AREA)
        x_area = img[y1:y2, x1:x2]
        cv2.imshow('x_area', x_area)
        x_ready = self.pxs.find_pixel_in_array(x_area, np.uint32(CLOSE_AD_COLOR), 3) * 255
        x_ready = x_ready.astype('uint8')
        ready, _ = cv2.findContours(x_ready, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        pos_ready = self.fetch_cnt_pos_2d(ready)
        if len(pos_ready):
            print(pos_ready)
            pos = pos_ready[0]
            self.mouse.click(pos)

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

    def calculate_distance(self, points, middle_point):
        """
        :param points: Takes a list of points tuples. Note that the Y point is always 0
        :return: Returns a sorted list of the tuples. The Y is changed with the distance to the middle point
        """
        accum = []
        for p in points:
            node = list(p)
            node[1] = abs(p[0] - middle_point)
            accum.append(node)

        s_accum = sorted(accum, key=lambda x: x[1])
        return s_accum

    @fire_and_forget
    def make_move_click(self, direction):
        """
        :param direction: String, left or right
        """

        _CLICK_LEFT = 0.25, 0.75
        _CLICK_RIGHT = 0.75, 0.75
        print(f"Moving {direction}")
        if direction == "left":
            self.mouse.click(_CLICK_LEFT)
        elif direction == "right":
            self.mouse.click(_CLICK_RIGHT)
        else:
            raise ValueError("left or right is needed")

    def make_move(self, bbox, img):
        _MOVE_LENGTH = 0.3  # Percentage of the screen
        _READY_LENGTH = 0.4

        ready, not_ready = self.find_enemies(bbox, img)
        ready = self.calculate_distance(ready, 0.5)
        not_ready = self.calculate_distance(not_ready, 0.5)

        first_move = None
        next_move = None

        self.atk_cooldown -= 1

        if len(ready) == 0:
            return

        target = ready.pop()

        if target[1] < _MOVE_LENGTH:
            # Found the target in range, lets figure out which direction is good
            if target[0] < 0.5:
                first_move = "left"
            else:
                first_move = "right"

        # If an other target also is in range just pick that one too
        if len(ready) > 0:
            target = ready.pop()
            if target[1] < _READY_LENGTH:
                if target[0] < 0.5:
                    next_move = "left"
                else:
                    next_move = "right"
        elif len(not_ready) > 0:  # There is a target, but its outside of the normal range
            pass

        # We need an cooldown amount to avoid too much spamming of attacks so that we get stunned
        if self.atk_cooldown < 0:
            self.atk_cooldown = ATK_COOLDOWN_AMOUNT
            self.make_move_click(first_move)
            if next_move:
                self.make_move_click(next_move)

    def start_game(self):
        print("Starting game")
        _START_CLICK_COORD = 0.485, 0.882
        self.mouse.click(_START_CLICK_COORD)
        print("Click")

    def find_state(self, bbox, img):
        # Possible states:
        #   Main menu:
        #       Check for the burger menu in the corner
        #
        _MENU_CHECK_AREA = 0.9168, 0.8705, 0.9480, 0.8798
        _MENU_CHECK_COLOR = 0xFFFFFF

        _RUNNING_PAUSE_BUTTON = 0.95, 0.075, 0.955, 0.12
        _RUNNING_CHECK_COLOR = 0xFFFFFF

        x1, y1, x2, y2 = self.pxs.percent_to_coord_box(bbox, _MENU_CHECK_AREA)
        px1, py1, px2, py2 = self.pxs.percent_to_coord_box(bbox, _RUNNING_PAUSE_BUTTON)
        menu_img = img[y1:y2, x1:x2]
        pause_img = img[py1:py2, px1:px2]
        cv2.imshow("menu_img", menu_img)
        cv2.imshow("pause_img", pause_img)

        menu_img = self.pxs.aproximate_color_3d(menu_img, _MENU_CHECK_COLOR, 1)
        pause_img = self.pxs.aproximate_color_3d(pause_img, _RUNNING_CHECK_COLOR, 1)
        if np.all(menu_img):  # Found the burger menu on the main screen
            print("Setting state menu")
            self.STATE = "menu"
            self.start_game()
            self.tick = 0
        elif np.all(pause_img):  # Looking for the pause button -> Game Running
            self.STATE = "running"
            self.make_move(bbox, img)
        else:
            self.STATE = "Unknown"
            print("Unknown state. Ads?")
            self.figure_out_ad(bbox, img)
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
