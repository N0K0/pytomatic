import argparse
from cv2 import namedWindow, destroyAllWindows, destroyWindow
import cv2
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QPixmap, QImage
import ctypes
import sys
from pytomatic.actions.PixelSearch import PixelSearch
from pytomatic.actions.WindowHandlers import WinHandler
import logging
from PIL import ImageQt
import time

import logging


FORMAT = "%(levelname)s-%(module)s-Line %(lineno)s: %(message)s"
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG, format=FORMAT)

class SampleCollector(QWidget):

    def __init__(self,wnd_target = None):
        """
        Sets up the needed classes:

            The window manager
            The Annotator
            The file saver
        """

        super().__init__()

        self.annotator = Annotator()
        self.wh = WinHandler()
        self.px = PixelSearch(self.wh)
        self.worker = WorkerThread(self)

        self.target_wnd_title = None

        self.setup_ui()


    def setup_ui(self):
        self.setWindowTitle("Proc Selector")
        layout = QVBoxLayout()
        proc_btn = QPushButton("Select Proc")
        proc_btn.clicked.connect(lambda x: self.setup_proc_wnd())

        self.label = QLabel('Pixmap')
        self.label.setScaledContents(True)

        layout.addWidget(proc_btn)
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.worker.start()
        self.show()

    def setup_proc_wnd(self):
        def ok_btn_click():
            self.target_wnd_title = list.currentItem().text()
            proc_wnd.close()

        proc_wnd = QWidget()

        layout = QVBoxLayout()
        proc_wnd.setLayout(layout)

        list = QListWidget()
        ok_btn = QPushButton("Ok")

        layout.addWidget(list)
        layout.addWidget(ok_btn)

        items = self.wh.get_window_list()

        for item in items:
            list.addItem(item[1])

        ok_btn.clicked.connect(ok_btn_click)

        proc_wnd.show()

class WorkerThread(QThread):
    def __init__(self,main):
        super(WorkerThread,self).__init__()


        self.main_wnd = main
        self.wh = main.wh # type: WinHandler
        self.px = main.px # type: PixelSearch
        self.running = True

    def run(self):

        while True:
            if self.main_wnd.target_wnd_title is None:
                time.sleep(1)
                print("No target")
                continue

            print("Got target")
            print(self.main_wnd.target_wnd_title)

            try:
                self.wh.set_target(title_name=self.main_wnd.target_wnd_title)
            except ValueError:
                print("Unable to find window. Resetting scanner")
                self.main_wnd.target_wnd_title = None
                continue

            img = self.px.grab_window()
            imgqt = ImageQt.ImageQt(img)
            px = QPixmap.fromImage(imgqt)
            self.main_wnd.label.setPixmap(px)



class Annotator():

    def annotator(self,image,name_base):
       raise NotImplementedError

    def write_annotation(self,file_name, annotation_list):
        """
        Creates an fitting annotation textfile with the regions matching the areas of value.
        Args:
            file_name: Name of the Imagefile used
            annotation_list: A list of tuples containing the coordinates we are instrested in the (x1,y1,x2,y2) format
        """

        raise NotImplementedError


if __name__ == '__main__':
    app = QApplication(sys.argv)

    sample_collector = SampleCollector()
    #sample_collector.main_loop()

    sys.exit(app.exec_())