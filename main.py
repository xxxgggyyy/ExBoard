#-*- encoding:utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication
import PyQt5.sip
from business import MainWindow, ExInterFace

if __name__=='__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    ExInterFace.init(mw)
    ExInterFace.addBorad("new")
    mw.showMaximized()
    sys.exit(app.exec())