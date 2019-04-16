from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMenu,QAction
from PyQt5.QtGui import QMouseEvent

#from .designs import resources

from business import Plugin,ExInterFace
from designs import DrawerItem, DrawerContentItem

class MainPlugin(Plugin):

    def __init__(self, name):
        super().__init__(name)


    def getTopToolBarActions(self):
        return []

    def getToolItems(self):
        return []

    def getPluginSettingWidget(self):
        return None

    def getPluginDescription(self):
        return '''相控阵检测工艺设计'''

    # 这些定义的接口将在 Board中相应的函数中得到调用
    def keyPressEvent(self, QKeyEvent):
        pass

    def keyReleaseEvent(self, QKeyEvent):
        pass


    def mouseDoubleClickEvent(self, QMouseEvent):
        pass

    def mouseMoveEvent(self, QMouseEvent):
        pass

    def mousePressEvent(self, QMouseEvent):
        pass

    def mouseReleaseEvent(self, QMouseEvent):
        pass

    def wheelEvent(self, QWheelEvent):
        pass

    def paintEvent(self, QPaintEvent):
        pass