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
        return temp_img

    def img_to_numpy(self,image):
        array = numpy.array(image)
        return self.RGB_to_Hex(array)

    def find_pixel_in_array(self, numpy_array, color,shades = 0):
        print "Implement pixel in array"

    def RGB_to_Hex(self, numpy_array):
        array = numpy.asarray(numpy_array, dtype='uint32')
        return ((array[:, :, 0]<<16) + (array[:, :, 1]<<8) + array[:, :, 2])


    def get_red_pos(self,maxTry = 10):

        print "Implement get_red_pos"

        return bbox
