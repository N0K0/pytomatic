import logging
import sys
from time import sleep
import numpy as np
from ConfigParser import SafeConfigParser
from PIL import ImageGrab
from PIL import Image

FORMAT = "%(levelname)s-%(module)s-Line %(lineno)s: %(message)s"
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG, format=FORMAT)


def extract_color_band(value, band):
    if band == 1 or band == 'R':
        return value >> 16
    elif band == 2 or band == 'G':
        return (value >> 8) & 0x0000FF
    elif band == 3 or band == 'B':
        return value & 0x0000FF
    else:
        raise ValueError('Invalid Bandinput')


class PixelSearch:
    def __init__(self, win_handler = None):
        self.last_image = None
        self.wh = win_handler

    def pixel_search(self, color, shades=0, bbox=None, debug=None):
        logging.debug("Searching for the pixels with color {} and shade {} ".format(str(color), str(shades)))

        wnd = self.grab_window(file=debug, bbox=bbox)
        px_data = self.img_to_numpy(wnd, compound=False)

        if bbox:
            px_data = px_data[bbox[0]:bbox[2], bbox[1]:bbox[3]]

        hits = self.find_pixel_in_array(px_data, color, shades)

        logging.debug("Found {} valid posistions".format(np.count_nonzero(hits)))

        return hits

    def grab_window(self, file=None, bbox=None):
        """
        Grabs the window and returns a image based on the on a hwnd and the
            bounding box that follows.

        Returns:
            PIL.Image.Image: Returns the imagedata grabbed by pillow
        """

        logging.debug("Trying to capture window")

        if bbox is None:
            bbox = self.wh.create_boundingbox(self.wh.get_hwnd())

        temp_img = ImageGrab.grab(bbox)

        if file is not None:
            logging.debug("Saving image as {}".format('grab_' + file))
            temp_img.save('grab_' + file)

        self.last_image = temp_img
        return temp_img

    def img_to_numpy(self, image, compound=False):
        """
        Converts an PIL.Image object to a numpy array and then collapses the
            array into an rgb array

        Args:
            image (PIL.image): the image object to be converted

        Returns:
            A 2d/3d array with x*y elements. Each element represent a pixel with
            an RGB value. For example 0xab01ee  -> RGB (171,1,238) or simply by
            having R G B as the third dimension of the matrix
            :param compound:
        """

        array = np.asarray(image, dtype="uint8")

        # DEPRECATED
        if compound:
            newarray = self.RGB_to_Hex(array)
            return newarray

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

        if len(numpy_array.shape) == 3:  # TODO: Either use Vectorization or some inline C magic
            logging.debug('Got a expanded RGB array')

            ret = self.aproximate_color_3d(numpy_array, color, shades)
            ret = np.all(ret, axis=2)
            return ret

        elif len(numpy_array.shape) == 2:
            logging.debug('Got a compound RGB array')

            aprox = np.vectorize(self.aproximate_color_2d)
            array = aprox(numpy_array, color, shades)

        else:
            logging.debug('WTF did i just get?')
            raise TypeError('Got an malformed array')

        return array

    @staticmethod
    def aproximate_color_2d(target, found, shade):
        red = abs((found >> 16) - (target >> 16)) <= shade
        green = abs((found >> 8) & 0x0000FF - (target >> 8) & 0x0000FF) <= shade
        blue = abs(found & 0x0000FF - target & 0x0000FF) <= shade

        if red and green and blue:
            return 1

        return 0

    @staticmethod
    def aproximate_color_3d(array, color, shade):
        r = extract_color_band(color, 'R')
        g = extract_color_band(color, 'G')
        b = extract_color_band(color, 'B')

        numpy_array = abs(array[:, :, :] - (r, g, b)) <= shade
        return numpy_array

    @staticmethod
    # DEPRECATED
    def RGB_to_Hex(numpy_array):
        logging.debug("Converting numpy_array to RGB")
        array = np.asarray(numpy_array, dtype='uint32')
        return (array[:, :, 0] << 16) + (array[:, :, 1] << 8) + array[:, :, 2]

    @staticmethod
    def get_red_pos(max_try=10):
        print "Implement get_red_pos"
        bbox = None
        return bbox
