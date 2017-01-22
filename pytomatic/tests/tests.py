import unittest
import os
from pytomatic.actions.WindowHandlers import WinHandler
from pytomatic.actions.MouseMovement import MouseMovement
from pytomatic.actions.PixelSearch import PixelSearch
import cv2
from matplotlib import pyplot as plt

from time import sleep
import random

class TestWindowManMethods(unittest.TestCase):
    def setUp(self):
        os.system("calc.exe")
        sleep(0.2)
        self.wh = WinHandler("Kalkulator")
        self.mm = MouseMovement(self.wh)
        self.px = PixelSearch(self.wh)
        self.wh.move((400, 600, 400, 400))
        self.wh.init_window()
        sleep(0.2)

    def test_move_wnd(self):
        self.wh.move((random.randrange(0,99),random.randrange(0,99)))
        wnd = self.wh.get_bbox()
        assert wnd[0] < 100
        assert wnd[1] < 100

        self.wh.move((100,100))
        wnd = self.wh.get_bbox()
        assert wnd[0] == 100
        assert wnd[1] == 100

        self.wh.move((200,200,0,0))
        wnd = self.wh.get_bbox()
        assert wnd[0] == 200
        assert wnd[1] == 200
        assert wnd[2] == 416
        assert wnd[3] == 564

    def test_templating(self):

        bbox = self.wh.create_boundingbox()
        scaled_bbox = self.wh.bbox_scale(bbox,0.5)
        sub_image = self.px.grab_window(scaled_bbox)
        sub_image = self.px.img_to_numpy(sub_image)

        w, h = sub_image.shape[0:2]

        main_image = cv2.imread('pytomatic/tests/assets/calc_clean.PNG')
        res = cv2.matchTemplate(main_image, sub_image, cv2.TM_CCOEFF)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv2.rectangle(main_image, top_left, bottom_right, 255, 2)
        assert top_left == (89,89)
        assert bottom_right == (290,290)

        #plt.imshow(main_image)
        #plt.show()

    def test_templating_proper(self):
        bbox = self.wh.create_boundingbox()
        scaled_bbox = self.wh.bbox_scale(bbox,0.9)
        main_image = self.px.grab_window(scaled_bbox)

        sub_image = cv2.imread('pytomatic/tests/assets/calc_8.PNG')
        main_image = self.px.img_to_numpy(main_image)
        location = self.px.find_subimage_in_array(sub_image,main_image,None,True)


    def tearDown(self):
        sleep(1)
        os.system("taskkill /T /F /IM Calculator.exe")


if __name__ == '__main__':
    unittest.main()