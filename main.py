#-*- encoding:utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication
from business import MainWindow
import plugins

if __name__=='__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()

    exit(app.exec())