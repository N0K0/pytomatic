import os
import time
import random
from pytomatic.actions import WindowHandlers
from pytomatic.actions import PixelSearch
from pytomatic.actions import MouseMovement
import logging


logging.basicConfig(level=logging.DEBUG)

def move_window_around():
    os.system('calc.exe')  # Lets run the calculator app
    win_handler = WindowHandlers.WinHandler(title='Kalkulator')  # Init of the window handler
    window_pos = win_handler.get_bbox()
    for x in range(0, 800, 100):
        for y in range(300, 100, -50):
            win_handler.move((x, y))
            time.sleep(0.3)


def click_and_drag():
    # Note this will not work if its the 64bit version of paint that starts

    os.system(f"start C:\Windows\System32\mspaint.exe")
    time.sleep(1)
    win_handler = WindowHandlers.WinHandler()
    win_handler.set_target(class_name='Afx:770000:8', parent_class='MSPaintApp')
    win_handler.init_window()
    mouse_handler = MouseMovement.MouseMovement(win_handler)
    for _ in range(0, 100):
        bbox = win_handler.get_bbox()
        rand_w_s = random.randrange(0, bbox[2])
        rand_h_s = random.randrange(0, bbox[3])
        rand_w_e = random.randrange(0, bbox[2])
        rand_h_e = random.randrange(0, bbox[3])

        mouse_handler.hold_and_drag((rand_w_s, rand_h_s), (rand_w_e, rand_h_e), steps=5, button="left")
        time.sleep(0.05)


click_and_drag()
