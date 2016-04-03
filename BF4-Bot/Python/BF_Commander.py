import numpy

import MouseMovement
import PixelSearch
import WindowHandlers

from ConfigParser import SafeConfigParser

numpy.set_printoptions(formatter={'int': hex})


def main_loop():
    print "Implement main_loop"
    raise NotImplementedError


def order_squads():
    print "Implement order_squads"
    raise NotImplementedError


def use_spec():
    print "Implement use_spec"
    raise NotImplementedError


# noinspection PyPep8Naming
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
    coords = (0.1, 0.1)
    pos = mm.to_pixel(coords)
    mm.click(pos, "right")


if __name__ == '__main__':


    win_handler = WindowHandlers.WinHandler()
    pix_handler = PixelSearch.PixelSearch(win_handler)
    img = pix_handler.grab_window()
    img = pix_handler.img_to_numpy(img)
    targets = pix_handler.find_pixel_in_array(img, 0xf7f7f7L, 5)
