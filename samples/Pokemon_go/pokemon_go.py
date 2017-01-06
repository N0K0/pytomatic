import cv2
import pytomatic.actions.WindowHandlers as Windows_handler
import pytomatic.actions.PixelSearch as Pixel_handler
import pytomatic.actions.MouseMovement as Mouse_handler
import numpy as np
import tempfile
import sys
import os

path = r"C:\Users\Neon\PycharmProjects\pytomatic\samples\Pokemon_go\training_data\pokestops"

config = {}


def mouse_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:

        print(x, '--',y)

        size = 20

        maxX,maxY, _ = param.shape
        tf = tempfile.NamedTemporaryFile(dir=path)

        if x < 0 + size: x = 0 + size
        if y < 0 + size: y = 0 + size

        if maxX < x - size: x = maxX - size
        if maxY < y - size: y = maxY + size

        img = param[y-size:y+size,x-size:x+size]

        cv2.imwrite(tf.name + '.png',img)

    return


def main():
    img = None
    main_win = Windows_handler.WinHandler(title='Nox',class_name='Qt5QWindowIcon')
    main_box = main_win.get_bbox()
    px_handler = Pixel_handler.PixelSearch(win_handler=main_win)
    mouse = Mouse_handler.MouseMovement(window_handler=main_win)
    main_win.init_window()
    cv2.namedWindow('image_name')
    cv2.namedWindow('config')

    while True:

        img = px_handler.grab_window(bbox=main_box)
        img = px_handler.img_to_numpy(img,compound=False)
        img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)

        orb = cv2.ORB_create()
        kp = orb.detect(img, None)
        kp, des = orb.compute(img, kp)
        img2 = cv2.drawKeypoints(img, kp)

        cv2.imshow('image_name',img2)
        cv2.setMouseCallback('image_name', mouse_event, param=img)


        k = cv2.waitKey(1)
        if k == ord('q'):  # wait for ESC key to exit
            cv2.destroyAllWindows()
            quit(0)


if __name__ == '__main__':
    main()