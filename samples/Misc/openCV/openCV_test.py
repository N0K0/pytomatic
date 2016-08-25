import cv2
import src.actions.WindowHandlers as Windows_handler
import src.actions.PixelSearch as Pixel_handler
import src.actions.MouseMovement as Mouse_handler
import numpy as np

main_win = Windows_handler.WinHandler(title='Nox',class_name='Qt5QWindowIcon')
main_box = main_win.get_bbox()
px_handler = Pixel_handler.PixelSearch(win_handler=main_win)
mouse = Mouse_handler.MouseMovement(window_handler=main_win)
main_win.init_window()

while True:
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    img = px_handler.grab_window(bbox=main_box)
    img = px_handler.img_to_numpy(img,compound=False)
    img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Initiate SIFT detector
    sift = cv2.SURF()
    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img, None)
    kp = sift.detect(img, None)

    img = cv2.drawKeypoints(img, kp, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    cv2.imshow('image',img)

    k = cv2.waitKey(1)
    if k == ord('q'):  # wait for ESC key to exit
        cv2.destroyAllWindows()
        quit(0)