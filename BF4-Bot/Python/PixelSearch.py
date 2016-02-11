import win32gui as gui
import win32api as api
from PIL import ImageGrab
import PIL
import numpy


class PixelSearch:

    def __init__(self, win_handler = None):
        self.wh = win_handler

    def pixel_search(self):
        print "Implement pixel_search"

    def grab_window(self):
        self.wh.init_window(self.wh.hwnd)
        temp_img = ImageGrab.grab(self.wh.create_boundingbox(self.wh.hwnd))
        temp_img.save('test.jpg','JPEG')
        self.last_image = temp_img
        print "Implement grab_screen"


    def get_red_pos(self,maxTry = 10):

        print "Implement get_red_pos"

        return bbox

if __name__ == '__main__':
    hwnd = _get_hwnd_by_title("Calculator")
