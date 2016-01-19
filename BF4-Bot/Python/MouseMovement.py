import win32gui
import win32api

class MouseMovement:

    def click(self, x, y, type = "left", speed = 0):
        print "Implement click"

    def offset_click(self, x, y, type = "left", speed = 0):
        print "Implement offset_click"

    def to_coord(self, pos_x, pos_y, win_x, win_y):
        print "Implement to_coord"

    def to_pixel(self, pos_x, pos_y, win_x, win_y):
        print "Implement to_coord"

    def __init__(self,title = "Battlefield 4"):
        self.title = title
