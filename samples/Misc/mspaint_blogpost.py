import time

from pytomatic.actions import PixelSearch, WindowHandlers, Helpers, MouseMovement
import logging
import subprocess
import random

MSPAINT_PATH = "C:\WINDOWS\system32\mspaint.exe"

logging.basicConfig(level=logging.DEBUG)

# We are using random backoff cooldown, that means that per loop the chance of an action happening increases.
# Its just a simple way to make the randomness i need in an incremental way.
cooldown_color = 0


def draw_line(wh, ps, mm):
    pass


def change_color(wh_, ps, mm: MouseMovement):
    row_one = 14.0 / 50
    row_two = 40.0 / 50

    col_one = 40.0 / 260
    col_lst = 250.0 / 260

    col_num = 14

    col_offset = (col_lst - col_one) / col_num

    row = random.randint(0, 1)
    y_pos = (row_one, row_two)[row]

    col = random.randint(0, col_num - 1)
    x_pos = col_one + col_offset * col

    mm.click((x_pos, y_pos))
    mm.click((x_pos, y_pos))
    mm.click((x_pos, y_pos))


def check_change():
    """
    This can be ignored really, just a complicated way to figure out what i want to change
    :return: col, brush, size
    """
    global cooldown_color
    check_color = random.randint(0, 100)

    col = brush = size = False

    if check_color < cooldown_color:
        col = True
        cooldown_color = 0
    else:
        cooldown_color += 1

    return col, brush, size


def paint_loop(wh, ps, mm):
    col, brush, size = check_change()
    if col:
        change_color(wh, ps, mm)

    draw_line(wh, ps, mm)


if __name__ == '__main__':
    # Setting up the basics of the framework
    # Name of the class is found via the Spy++ utility from microsoft/ Visual Studio
    # https://docs.microsoft.com/en-us/visualstudio/debugger/introducing-spy-increment

    try:
        wh_all = WindowHandlers.WinHandler(class_name="MSPaintApp")
    except ValueError as e:
        subprocess.Popen(MSPAINT_PATH, shell=True)
        time.sleep(1)
        wh_all = WindowHandlers.WinHandler(class_name="MSPaintApp")

    wh_paint = WindowHandlers.WinHandler(parent_class="MSPaintApp", class_name="Afx:1000000:8")
    wh_control = WindowHandlers.WinHandler(parent_class="MSPaintApp", title="Tools", class_name="AfxWnd42u")
    ps = PixelSearch.PixelSearch(wh_all)
    mm = MouseMovement.MouseMovement(wh_all)
    mm_paint = MouseMovement.MouseMovement(wh_paint)
    mm_control = MouseMovement.MouseMovement(wh_control)

    wh_all.init_window(pos=(0.0, 0.0, 0.2, 0.6))

    # mm_paint.click((0.5, 0.5))
    mm_control.click((0.4, 0.5))
    # for _ in range(100):
    #    change_color(wh_paint, ps, mm_paint)

    # paint_loop(wh, ps, mm)
