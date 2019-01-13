from PyQt5 import *
from PyQt5.QtWidgets import *

class Board(QFrame):

    #插件的各个事件函数 在这里得到调用
    def __init__(self, name,parent=None):
        super().__init__(parent)
        self.__plugins = None
        self.name = name

    def getName(self):
        return self.name

    def registerPlugins(self, plugins):
        self.__plugins = plugins

    def mouseReleaseEvent(self, *args, **kwargs):
        if self.__plugins:
            for plugin in self.__plugins:
                plugin.mouseReleaseEvent(args)

    def mousePressEvent(self, *args, **kwargs):
        if self.__plugins:
            for plugin in self.__plugins:
                plugin.mousePressEvent(args)

    def mouseDoubleClickEvent(self, *args, **kwargs):
        if self.__plugins:
            for plugin in self.__plugins:
                plugin.mouseDoubleClickEvent(args)

    def mouseMoveEvent(self, *args, **kwargs):
        if self.__plugins:
            for plugin in self.__plugins:
                plugin.mouseMoveEvent(args)

    def keyPressEvent(self, *args, **kwargs):
        if self.__plugins:
            for plugin in self.__plugins:
                plugin.keyPressEvent(args)

    def keyReleaseEvent(self, *args, **kwargs):
        if self.__plugins:
            for plugin in self.__plugins:
                plugin.keyReleaseEvent(args)

    def paintEvent(self, QPaintEvent):
        if self.__plugins:
            for plugin in self.__plugins:
                plugin.paintEvent(QPaintEvent)