import logging
import sys
from time import sleep
import numpy as np
from PIL import ImageGrab
from PIL import Image
from pytomatic.actions.Helpers import Helpers
from ctypes import windll, c_int, c_uint, c_char_p, create_string_buffer
from struct import calcsize, pack
import win32con
import cv2
from matplotlib import pyplot as plt

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
    def __init__(self, win_handler):
        self.wh = win_handler

    def pixel_search(self, color, shades=0,bbox=None, debug=None):
        logging.debug("Searching for the pixels with color {} and shade {} ".format(str(color), str(shades)))

        wnd_img = self.grab_window(file=debug, bbox=bbox)
        px_data = self.img_to_numpy(wnd_img)

        if bbox:
            px_data = px_data[bbox[0]:bbox[2], bbox[1]:bbox[3]]

        hits = self.find_pixel_in_array(px_data, color, shades)

        logging.debug("Found {} valid posistions".format(np.count_nonzero(hits)))

        return hits

    def grab_screen(self, file=None, bbox=None):
        # TODO: Fix this brokenass shit (can only cap primary screen atm)
        # http://stackoverflow.com/questions/3585293/pil-imagegrab-fails-on-2nd-virtual-monitor-of-virtualbox
        temp_img = ImageGrab.grab(bbox)

        if file is not None:
            logging.debug("Saving image_name as {}".format('grab_' + file))
            temp_img.save('grab_' + file)

        return temp_img

    def grab_window(self, bbox=None,file=None):
        """
        Grabs the window and returns a image_name based on the on a hwnd and the
            bounding box that follows.

        Returns:
            PIL.Image.Image: Returns the image data grabbed by pillow
        """

        if self.wh.get_hwnd() is None and bbox is None:
            logging.error("You can not use grab grab_window without a windowhandler target or a BBOX")
            raise ReferenceError("You can not use grab grab_window without a windowhandler target or a BBOX")

        logging.debug("Trying to capture window")

        if bbox is None:
            hwnd = self.wh.get_hwnd()
            bbox = self.wh.create_boundingbox(hwnd)


        gdi32 = windll.gdi32
        # Win32 functions
        CreateDC = gdi32.CreateDCA
        CreateCompatibleDC = gdi32.CreateCompatibleDC
        GetDeviceCaps = gdi32.GetDeviceCaps
        CreateCompatibleBitmap = gdi32.CreateCompatibleBitmap
        BitBlt = gdi32.BitBlt
        SelectObject = gdi32.SelectObject
        GetDIBits = gdi32.GetDIBits
        DeleteDC = gdi32.DeleteDC
        DeleteObject = gdi32.DeleteObject

        # Win32 constants
        NULL = 0
        HORZRES = 8
        VERTRES = 10
        SRCCOPY = 13369376
        HGDI_ERROR = 4294967295
        ERROR_INVALID_PARAMETER = 87

        try:

            screen = CreateDC(c_char_p(b'DISPLAY'), NULL, NULL, NULL)
            screen_copy = CreateCompatibleDC(screen)

            if bbox:
                left, top, x2, y2 = bbox
                width = x2 - left + 1
                height = y2 - top + 1
            else:
                left = windll.user32.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
                top = windll.user32.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
                width = windll.user32.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
                height = windll.user32.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)

            bitmap = CreateCompatibleBitmap(screen, width, height)
            if bitmap == NULL:
                print('grab_screen: Error calling CreateCompatibleBitmap. Returned NULL')
                return

            hobj = SelectObject(screen_copy, bitmap)
            if hobj == NULL or hobj == HGDI_ERROR:
                print('grab_screen: Error calling SelectObject. Returned {0}.'.format(hobj))
                return

            if BitBlt(screen_copy, 0, 0, width, height, screen, left, top, SRCCOPY) == NULL:
                print('grab_screen: Error calling BitBlt. Returned NULL.')
                return

            bitmap_header = pack('LHHHH', calcsize('LHHHH'), width, height, 1, 24)
            bitmap_buffer = create_string_buffer(bitmap_header)
            bitmap_bits = create_string_buffer(b' ' * (height * ((width * 3 + 3) & -4)))
            got_bits = GetDIBits(screen_copy, bitmap, 0, height, bitmap_bits, bitmap_buffer, 0)
            if got_bits == NULL or got_bits == ERROR_INVALID_PARAMETER:
                print('grab_screen: Error calling GetDIBits. Returned {0}.'.format(got_bits))
                return

            image = Image.frombuffer('RGB', (width, height), bitmap_bits, 'raw', 'BGR', (width * 3 + 3) & -4, -1)
            return image
        finally:
            if bitmap is not None:
                if bitmap:
                    DeleteObject(bitmap)
                DeleteDC(screen_copy)
                DeleteDC(screen)

    def img_to_numpy(self, image):
        """
        Converts an PIL.Image object to a numpy array and then collapses the
            array into an rgb array

        Args:
            image_name (PIL.image_name): the image_name object to be converted

        Returns:
            A 2d/3d array with x*y elements. Each element represent a pixel with
            an RGB value. For example 0xab01ee  -> RGB (171,1,238) or simply by
            having R G B as the third dimension of the matrix
        """

        array = np.asarray(image, dtype="uint8")

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

    def find_subimage_in_array(self,sub_image, main_image,threshold = None, debug = False):
        """
        http://docs.opencv.org/3.1.0/d4/dc6/tutorial_py_template_matching.html

        Args:
            sub_image: A numby matrix containing the template we are trying to match
            main_image: A numpy array containing the main image we are trying to find the template in
            threshold: A treshhold regarding hos sensitive the matching should be. If its set to None, only the best match is returned
        Returns:
            If treshold is none:
                The bounding box of the best resulting area
            Else:
                A list of bounding boxes of varying accuracy

        """
        # TODO: Check the test_init_wnd test for how to implement this :)
        logging.debug("Doing a template match with {} as threshold".format(threshold))
        methods = [cv2.TM_CCOEFF, cv2.TM_CCOEFF_NORMED, cv2.TM_CCORR,cv2.TM_CCORR_NORMED, cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]
        method = methods[1]

        h, w = sub_image.shape[0:2]

        res = cv2.matchTemplate(main_image,sub_image,method)

        if threshold is None:
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            top_left = max_loc
            bottom_right = (top_left[0] + w, top_left[1] + h)
            if debug:
                cv2.rectangle(main_image, top_left, bottom_right, 255, 2)
                plt.imshow(main_image)
                plt.show()
            bounding_box = top_left[0], top_left[1] , bottom_right[0], bottom_right[1]
            logging.debug("Found the following area with templating: {}"
                          .format(bounding_box))
            return bounding_box

        else:
            loc = np.where(res >= threshold)
            locations = []
            for pt in zip(*loc[::-1]):
                locations.append((pt[0],pt[1],pt[0]+w,pt[1]+h))

            if debug:
                for pt in zip(*loc[::-1]):
                    cv2.rectangle(main_image, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
                plt.imshow(main_image)
                plt.show()
            return loc



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
