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
        centre = self.check_exist(file_name)
        if centre is None:
            return None

        centre = centre[0]

        # TODO: Update this click
        self.mm.click(centre)
        sleep(5)
        return centre

    def check_exist(self,file_name):
        target = cv2.imread(file_name,1)
        window = self.px.grab_window()
        window = self.px.img_to_numpy(window)
        targets = self.px.find_features_in_array_SIFT(target,window,debug=False)

        centres = self.px.validate_clustering(target,window,targets,debug=True)
        if centres is not None:
            return centres[0]
        return None

    def watch_ad(self):

        # Pressing the buttons for free gems
        ad_free = self.press_button('assets/ad_ready.PNG')
        if ad_free is None:
            return False

        #Watch ad button
        ad_watch = self.press_button('assets/ad_watch.PNG')
        if ad_watch is None:
            return None

        # TODO: Check if there is no ad


        # Ad is being watched and we need to click the X at some point
        print("Sleeping 45")
        sleep(15)
        print("Sleeping 30")
        sleep(15)
        print("Sleeping 15")
        sleep(15)
        print("Sleeping 00")

        click_close = self.press_button('assets/ad_done_1.PNG')
        if click_close is None:
            click_close = self.press_button('assets/ad_done_2.PNG')

        if click_close is None:
            self.mm.click((0.97,0.06))
            return None

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
