import win32gui as gui
import win32api as api

class PixelSearch:

    def __init__(self, title = "Battlefield 4"):
        self.title = title

    def pixel_search():
        print "Implement pixel_search"

    def grab_screen():
        print "Implement grab_screen"

    def get_red_pos(maxTry = 10):
        print "Implement get_red_pos"

def _get_hwnd_by_title(title_text):
    return gui.FindWindow(None, title_text)

def _init_window(hwnd):
    return gui.SetForeGroundWindow(hwnd)

if __name__ == '__main__':
    print _get_hwnd_by_title("Kalkulator")
