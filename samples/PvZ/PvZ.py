from pytomatic.actions.WindowHandlers import WinHandler
from pytomatic.actions.MouseMovement import MouseMovement
from pytomatic.actions.PixelSearch import PixelSearch
import cv2
from time import sleep
import logging
import sys

FORMAT = "%(levelname)s-%(module)s-Line %(lineno)s: %(message)s"
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG, format=FORMAT)

class PvZHandler():

    def __init__(self):
        self.wh = WinHandler(title='Nox',class_name='Qt5QWindowIcon')
        self.px = PixelSearch(self.wh)
        self.mm = MouseMovement(self.wh)
        self.wh.init_window(pos=(0, 0))
        sleep(1)

    def press_button(self,file_name):
        button = cv2.imread(file_name)
        window = self.px.grab_window()
        window = self.px.img_to_numpy(window)
        area = self.px.find_subimage_in_array(button, window,debug=True)
        area = area[0]
        self.mm.click((area[0] + 20, area[1] + 20))
        sleep(5)

    def check_exist(self,file_name):
        target = cv2.imread(file_name,0)
        window = self.px.grab_window()
        window = self.px.img_to_numpy(window)
        targets = self.px.find_features_in_array_SIFT(target,window,debug=True)

        centre = self.px.validate_clustering(target,window,targets,debug=True)

        sys.exit(1)

        if len(targets) > 0:
            return True
        else:
            return False



    def watch_ad(self):
        if not self.ad_ready():
            return False

        self.press_button('assets/ad_ready.PNG')

        if self.ad_avaliable() and not self.ad_not_avaliable():
            self.press_button('assets/ad_watch.PNG')
        elif not self.ad_avaliable() and self.ad_not_avaliable():
            self.press_button('assets/ad_close_menu.PNG')
        else:
            raise ValueError("Unable to find the button")

    def ad_ready(self):
        return self.check_exist('assets/ad_ready.PNG')

    def ad_avaliable(self):
        if self.check_exist('assets/ad_watch.PNG'):
            return True

    def ad_not_avaliable(self):
        if self.check_exist('assets/ad_not_available.PNG'):
            return True

    def check_battle_state(self):
        if self.check_exist('assets/bar_zombies.PNG')   : return 1
        if self.check_exist('assets/bar_plant.PNG')     : return 2
        if self.check_exist('assets/bar_trick.PNG')     : return 3
        if self.check_exist('assets/bar_battle.PNG')    : return 4
        return 0

if __name__ == '__main__':
    pvz = PvZHandler()
    pvz.watch_ad()
