
from pytomatic.actions import PixelSearch, WindowHandlers, Helpers
def search_for_pixels():
    wh = WindowHandlers.WinHandler()
    wh.set_target(title_name='Untitled - Notepad')
    wh.init_window(borderless=True)
    px = PixelSearch.PixelSearch(wh)
    mx = px.pixel_search(0xFFFFFF,shades=50)
    Helpers.Helpers.show_matrix(mx)

search_for_pixels()