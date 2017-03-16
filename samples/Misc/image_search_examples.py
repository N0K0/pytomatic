from pytomatic.actions import PixelSearch, WindowHandlers, Helpers
import win32api

def search_for_pixels():
    wh = WindowHandlers.WinHandler()
    wh.set_target(title_name='Untitled - Notepad') #desktop is a special case that is the primary monitor
    wh.init_window()
    px = PixelSearch.PixelSearch(wh)
    mx = px.pixel_search(0xFFFFFF,shades=50)
    Helpers.show_matrix(mx)


def multi_screen():
    wh = WindowHandlers.WinHandler("Netflix")
    print(wh.get_desktop_stats())
    px = PixelSearch.PixelSearch(win_handler=wh)

    mat = px.pixel_search(0xA87161,12)
    Helpers.show_matrix(mat)


multi_screen()

