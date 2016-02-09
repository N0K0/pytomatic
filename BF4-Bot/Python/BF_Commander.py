import win32gui as gui
import win32api as api

from MouseMovement import *
from PixelSearch import *
from time import sleep

def main_loop():
    print "Implement main_loop"

def order_squads():
    print "Implement order_squads"

def use_spec():
    print "Implement use_spec"

def use_UAV():
    print "Implement use_UAV"

def pause():
    print "Implement pause"

def debug_out():
    print "Implement debug_out"

def test():
    mm = MouseMovement()
    coords = (0.1,0.1)
    pos = mm.to_pixel(coords)
    mm.click(pos,"right")



if __name__ == '__main__':
    pyc_wnd = make_pyc_wnd()
