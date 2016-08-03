from time import sleep
import numpy
from ConfigParser import SafeConfigParser

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
        self.mouse_handler.click(coords, button='right')
        sleep(1)
        self.mouse_handler.offset_click(0.0, -0.05)

    def use_EMP(self, coords):
        self.mouse_handler.click(coords, button='right')
        sleep(1)
        self.mouse_handler.offset_click(0.0, -0.1)

    def pause(self):
        print "Implement pause"
        raise NotImplementedError

    def debug_out(self):
        print "Implement debug_out"
        raise NotImplementedError

    def __init__(self, win_h, pix_h, mo_h):
        self.win_handler = win_h
        self.pix_handler = pix_h
        self.mouse_handler = mo_h


def wipe_scorebox(score_box1, wh, score_box=None, numpy_image=None):
    score_box = config.get('PixelScan', 'ScoreBox').split(',')
    score_box = map(float, score_box)

    score_box = wh.create_boundingbox_from_coords(score_box)
    numpy_image[score_box[0]:score_box[2], score_box[1]:score_box[3]] = 0x0
    return numpy_image


if __name__ == '__main__':
    config = SafeConfigParser()
    config.read('config.ini')
    cmd = CommandAndControl()
