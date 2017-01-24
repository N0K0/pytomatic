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

    def press_button(self,file_name):
        button = cv2.imread(file_name)
        window = self.px.grab_window()
        window = self.px.img_to_numpy(window)
        area = self.px.find_subimage_in_array(button, window)
        area = area[0]
        self.mm.click((area[0] + 20, area[1] + 20))
        sleep(5)

    def check_exist(self,file_name):
        target = cv2.imread(file_name)
        window = self.px.grab_window()
        window = self.px.img_to_numpy(window)
        targets = self.px.find_subimage_in_array(target, window,threshold=0.6)
        if len(targets) > 0:
            return True
        else:
            return False

    def zombie_battle(self):
        self.press_button('assets/zombie_mission.PNG')

    def plant_battle(self):
        self.press_button('assets/zombie_mission.PNG')

    def start_mission(self):
        self.press_button('assets/mission_play_button.PNG')

    def confirm_mulligan(self):
        self.press_button('assets/confirm_mulligan.PNG')


    def check_battle_state(self,plant = True):
        bar_state_1 = self.check_exist('assets/bar_zombies.PNG')
        bar_state_2 = self.check_exist('assets/bar_plant.PNG')
        bar_state_3 = self.check_exist('assets/bar_trick.PNG')
        bar_state_4 = self.check_exist('assets/bar_battle.PNG')

        if bar_state_1:
            return 1
        elif bar_state_2:
            return 2
        elif bar_state_3:
            return 3
        elif bar_state_4:
            return 4
        else:
            return 0

if __name__ == '__main__':
    pvz = PvZHandler()
    while True:
        print(pvz.check_battle_state())
