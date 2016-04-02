import logging
import sys

import numpy
from PIL import ImageGrab

FORMAT = "%(levelname)s-%(module)s-Line %(lineno)s: %(message)s"
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG, format=FORMAT)


class PixelSearch:
    def __init__(self, win_handler=None):
        self.last_image = None
        self.wh = win_handler

    def pixel_search(self):
        print "Implement pixel_search"
        raise NotImplementedError

    def grab_window(self):
        """
        Grabs the window and returns a image based on the on a hwnd and the
            bounding box that follows.

        Returns:
            PIL.Image: Returns the imagedata grabbed by pillow
        """

        logging.debug("Trying to capture window")

        self.wh.init_window(self.wh.hwnd)
        temp_img = ImageGrab.grab(self.wh.create_boundingbox(self.wh.hwnd))
        temp_img.save('test.jpg', 'JPEG')
        self.last_image = temp_img
        return temp_img

    def img_to_numpy(self, image):
        """
        Converts an PIL.Image object to a numpy array and then collapses the
            array into an rgb array

        Args:
            image (PIL.image): the image object to be converted

        Returns:
            A 2d array with x*y elements. Each element represent a pixel with
            an RGB value. For example 0xab01ee  -> RGB (171,1,238)
        """

        array = numpy.array(image)
        array = self.RGB_to_Hex(array)
        print array
        return array

    def find_pixel_in_array(self, numpy_array, color, shades=0):
        """
        Creates a bool array where values whose match color withing n shades are
            marked true.

        Args:
            numpy_array (NDarray): The array we are going to search.

            color (numpy.uint32): The color we are looking for.

            shades (int): Defines the tolerance per rgb color which still
                evaluates to True

        Returns:
            A boolean array where the pixels that has aproximate the value of
                color is set to True

        """

        aprox = numpy.vectorize(self.aproximate_color)

        array = aprox(numpy_array, color, shades)

        # array = self.aproximate_color(numpy_array,color,shades)

        print array
        return array

    @staticmethod
    def aproximate_color(target, found, shade):
        red = abs((found >> 16) - (target >> 16)) <= shade
        green = abs((found >> 8) & 0x0000FF - (target >> 8) & 0x0000FF) <= shade
        blue = abs(found & 0x0000FF - target & 0x0000FF) <= shade

        return red and green and blue

    # noinspection PyPep8Naming
    @staticmethod
    def RGB_to_Hex(numpy_array):
        logging.debug("Converting numpy_array to RGB")
        array = numpy.asarray(numpy_array, dtype='uint32')
        return (array[:, :, 0] << 16) + (array[:, :, 1] << 8) + array[:, :, 2]

    @staticmethod
    def get_red_pos(max_try=10):
        print "Implement get_red_pos"

        return bbox
