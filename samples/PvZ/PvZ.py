from pytomatic.actions.WindowHandlers import WinHandler
from pytomatic.actions.MouseMovement import MouseMovement
from pytomatic.actions.PixelSearch import PixelSearch
import cv2
from time import sleep

class PvZHandler():

    def __init__(self):
        self.wh = WinHandler(title='Nox',class_name='Qt5QWindowIcon')
        self.px = PixelSearch(self.wh)
        self.mm = MouseMovement(self.wh)
        self.wh.init_window(pos=(0, 0))

    def zombie_battle(self):
        button = cv2.imread('assets/zombie_mission.PNG')
        window = self.px.grab_window()
        window = self.px.img_to_numpy(window)

        area = self.px.find_subimage_in_array(button,window)

        self.mm.click((area[0]+20,area[1]+20))
        self.mm.click((area[0]+20,area[1]+20))
        sleep(3)

    def start_mission(self):
        button = cv2.imread('assets/mission_play_button.PNG')
        window = self.px.grab_window()
        window = self.px.img_to_numpy(window)

        area = self.px.find_subimage_in_array(button,window)

        self.mm.click((area[0]+20,area[1]+20))
        self.mm.click((area[0]+20,area[1]+20))
        sleep(3)

    def confirm_mulligan(self):
        button = cv2.imread('assets/confirm_mulligan.PNG')
        window = self.px.grab_window()
        window = self.px.img_to_numpy(window)

        area = self.px.find_subimage_in_array(button,window)

        self.mm.click((area[0]+20,area[1]+20))
        self.mm.click((area[0]+20,area[1]+20))
        sleep(3)


if __name__ == '__main__':
    pvz = PvZHandler()
    pvz.zombie_battle()
    pvz.start_mission()
    pvz.confirm_mulligan()

