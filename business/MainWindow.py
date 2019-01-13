from designs import Ui_MainWindow
from designs import DrawerWidget

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.drawerWdg = DrawerWidget(self.ui.tool_scrollAreaWidgetContents)
        self.ui.tool_scrollAreaWidgetContents.layout().addWidget(self.drawerWdg)
