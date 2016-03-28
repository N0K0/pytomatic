import win32gui as gui
import win32api as api

import WindowHandlers
import MouseMovement
import PixelSearch
import numpy
import logging

from time import sleep

def main_loop():
    print "Implement main_loop"
    raise NotImplementedError

def order_squads():
    print "Implement order_squads"
    raise NotImplementedError

def use_spec():
    print "Implement use_spec"
    raise NotImplementedError

def use_UAV():
    print "Implement use_UAV"
    raise NotImplementedError

def pause():
    print "Implement pause"
    raise NotImplementedError

def debug_out():
    print "Implement debug_out"
    raise NotImplementedError


def test():
    mm = MouseMovement()
    coords = (0.1,0.1)
    pos = mm.to_pixel(coords)
    mm.click(pos,"right")

if __name__ == '__main__':
    numpy.set_printoptions(formatter={'int':hex})
    win_handler = WindowHandlers.win_handler()
    pix_handler = PixelSearch.PixelSearch(win_handler)
    img = pix_handler.grab_window()
    img = pix_handler.img_to_numpy(img)
    print img[600:610,300:310]
