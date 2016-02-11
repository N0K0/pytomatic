from ConfigParser import SafeConfigParser
import win32gui
import win32ui

class win_handler:

    def get_hwnd_by_title(self,title_text = ""):
        print title_text
        self.hwnd = win32gui.FindWindow(None, title_text)
        print self.hwnd
        return self.hwnd

    def make_pyc_wnd(self,title = "Battlefield 4"):
        self.pycwnd = win32ui.CreateWindowFromHandle(self.hwnd)
        self.pycwnd
        return self.pycwnd

    def init_window(self,hwnd):
        return win32gui.SetForegroundWindow(self.hwnd)

    def create_boundingbox(self,hwnd):
        self.bbox = win32gui.GetWindowRect(hwnd)
        print self.bbox
        return self.bbox


    def __init__(self):

        parser = SafeConfigParser()
        parser.read('config.ini')

        self.title = parser.get('general','winTitle')
        self.hwnd = self.get_hwnd_by_title(self.title)
        self.pycwnd = self.make_pyc_wnd(self.title)
        self.bbox = self.create_boundingbox(self.hwnd)


if __name__ == '__main__':
    wh = win_handler()
