import os
import time
import random
from src.actions import WindowHandlers
from src.actions import PixelSearch
from src.actions import MouseMovement


def move_window_around():
    os.system('calc.exe') #Lets run the calculator app
    win_handler = WindowHandlers.WinHandler(title='Kalkulator') #Init of the window handler
    window_pos = win_handler.get_bbox()
    for x in range(0,800,100):
        for y in range(300,100,-50):
            win_handler.move((x,y))
            time.sleep(0.3)


def click_and_drag():
    #Note this will not work if its the 64bit version of paint that starts

    os.system('start /MAX mspaint.exe')
    time.sleep(1)
    win_handler = WindowHandlers.WinHandler()
    win_handler.set_target(class_name='Afx:1f0000:8',parent_class='MSPaintApp')
    win_handler.init_window()
    mouse_handler = MouseMovement.MouseMovement(win_handler)
    for _ in range(0,100):
        bbox = win_handler.get_bbox()
        rand_w_s = random.randrange(bbox[0],bbox[2])
        rand_h_s = random.randrange(bbox[1],bbox[3])
        rand_w_e = random.randrange(bbox[0],bbox[2])
        rand_h_e = random.randrange(bbox[1],bbox[3])

        mouse_handler.hold_and_drag((rand_w_s,rand_h_s),(rand_w_e,rand_h_e),steps=200)




click_and_drag()

