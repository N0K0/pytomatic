import numpy

import MouseMovement
import PixelSearch
import WindowHandlers

#from ConfigParser import SafeConfigParser

numpy.set_printoptions(formatter={'int': hex})


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
    def use_UAV(self):
        print "Implement use_UAV"
        raise NotImplementedError

    def pause(self):
        print "Implement pause"
        raise NotImplementedError

    def debug_out(self):
        print "Implement debug_out"
        raise NotImplementedError

    def get_win_handler(self):
        return self._win_handler

    def __init__(self):

        self._win_handler = WindowHandlers.WinHandler()
        self._pix_handler = PixelSearch.PixelSearch(self._win_handler)
        self._mouse_handler = MouseMovement.MouseMovement(self._win_handler)


if __name__ == '__main__':

    cmd = CommandAndControl()

