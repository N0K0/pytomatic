import os
import sys

import time

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

