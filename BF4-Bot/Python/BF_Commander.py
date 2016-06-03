from time import sleep

import numpy

import MouseMovement    as mm
import PixelSearch      as ps
import WindowHandlers   as wh

# from ConfigParser import SafeConfigParser

numpy.set_printoptions(formatter={'int': hex})

import sys
import logging
FORMAT = "%(levelname)s-%(module)s-Line %(lineno)s: %(message)s"
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG, format=FORMAT)



class CommandAndControl:
    def main_loop(self):
        print "Implement main_loop"
        raise NotImplementedError

    def order_squads(self):
        print "Implement order_squads"
        raise NotImplementedError

    def use_spec(self):
        print "Implement use_spec"
        raise NotImplementedError

    # noinspection PyPep8Naming
    def use_UAV(self, coords):
        self.mouse_handler.click(coords,button='right')
        sleep(1)
        self.mouse_handler.offset_click(0.0,-0.05)

    def use_EMP(self,coords):
        self.mouse_handler.click(coords, button='right')
        sleep(1)
        self.mouse_handler.offset_click(0.0, -0.1)

    def pause(self):
        print "Implement pause"
        raise NotImplementedError

    def debug_out(self):
        print "Implement debug_out"
        raise NotImplementedError

    def __init__(self, win_h,pix_h,mo_h):

        self.win_handler = win_h
        self.pix_handler = pix_h
        self.mouse_handler = mo_h


if __name__ == '__main__':
    cmd = CommandAndControl()
