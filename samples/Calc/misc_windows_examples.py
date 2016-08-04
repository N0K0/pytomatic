import os
import sys

import time

import win32api

import win32con

from src.actions import WindowHandlers
from src.actions import PixelSearch
from src.actions import MouseMovement


def move_window_around():
    os.system('calc.exe') #Lets run the calculator app
    win_handler = WindowHandlers.WinHandler('Kalkulator') #Init of the window handler
    window_pos = win_handler.get_bbox()
    for x in range(0,800,100):
        for y in range(300,100,-50):
            win_handler.move((x,y))
            time.sleep(0.3)


def click_and_drag():
    win_handler = WindowHandlers.WinHandler('Nox')
    win_handler.init_window()
    mouse_handler = MouseMovement.MouseMovement(win_handler)
    mouse_handler.hold_and_drag((150,150),(1000,1000),100)
    time.sleep(1)



click_and_drag()

