from pytomatic.actions import PixelSearch, WindowHandlers, Helpers
import win32api

def search_for_pixels():
    wh = WindowHandlers.WinHandler()
    wh.set_target(title_name='Untitled - Notepad') #desktop is a special case that is the primary monitor
    wh.init_window()
    px = PixelSearch.PixelSearch(wh)
    mx = px.pixel_search(0xFFFFFF,shades=50)
    Helpers.Helpers.show_matrix(mx)


def multi_screen():
    wh = WindowHandlers.WinHandler()
    print(wh.get_desktop_stats())
    px = PixelSearch.PixelSearch(win_handler=wh)

    img = px.grab_window()
    img.show()


multi_screen()

