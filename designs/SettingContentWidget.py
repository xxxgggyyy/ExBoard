from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class SettingContentWidget(QFrame):

    closeSignal = pyqtSignal()

    def __init__(self,parent=None):
        super().__init__(parent)