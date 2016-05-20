import logging
import sys
import numpy
from ConfigParser import SafeConfigParser

from PIL import ImageGrab

FORMAT = "%(levelname)s-%(module)s-Line %(lineno)s: %(message)s"
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG, format=FORMAT)


class PixelSearch:
    def __init__(self, win_handler=None):
        config = SafeConfigParser()
        config.read('config.ini')

        self.last_image = None
        self.wh = win_handler

        self.score_box = config.get('PixelScan', 'ScoreBox').split(',')
        self.score_box = map(float, self.score_box)

    def wipe_scorebox(self, score_box=None, numpy_image=None):
        if score_box is None:
            score_box = self.score_box

        score_box = self.wh.create_boundingbox_from_coords(score_box)

        numpy_image[score_box[0]:score_box[2], score_box[1]:score_box[3]] = 0x0

        return numpy_image

    def pixel_search(self, color, shades = 0, bbox = None):
        logging.debug("Searching for the pixels with color {} and shade {} ".format(str(color), str(shades)))

        wnd = self.grab_window()
        px_data = self.img_to_numpy(wnd)
        hits = self.find_pixel_in_array(px_data,color,shades)

        print "Implement pixel_search"
        raise NotImplementedError

    def grab_window(self,file = None):
        """
        Grabs the window and returns a image based on the on a hwnd and the
            bounding box that follows.

        Returns:
            PIL.Image.Image: Returns the imagedata grabbed by pillow
        """

        logging.debug("Trying to capture window")

        #self.wh.init_window(self.wh.hwnd) #Dont need this line. The user should fix this himself
        temp_img = ImageGrab.grab(self.wh.create_boundingbox(self.wh.hwnd))
        if file is not None:
            logging.debug("Saving image as {}".format(file))
            temp_img.save(file)

        self.last_image = temp_img
        return temp_img

    def img_to_numpy(self, image,compound = False):
        """
        Converts an PIL.Image object to a numpy array and then collapses the
            array into an rgb array

        Args:
            image (PIL.image): the image object to be converted

        Returns:
            A 2d/3d array with x*y elements. Each element represent a pixel with
            an RGB value. For example 0xab01ee  -> RGB (171,1,238) or simply by
            having R G B as the third dimension of the matrix
        """

        array = numpy.array(image)
        if compound:
            array = self.RGB_to_Hex(array)

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

        if len(numpy_array.shape) == 3:
            logging.debug('Got a expanded RGB array')
            raise NotImplementedError('Expanded Array grabber not implemented')
        elif len(numpy_array.shape) == 2:
            logging.debug('Got a compound RGB array')
            aprox = numpy.vectorize(self.aproximate_color)
            array = aprox(numpy_array, color, shades)

        else:
            logging.debug('WTF did i just get?')
            raise TypeError('Got an malformed array')

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
        bbox = None
        return bbox
