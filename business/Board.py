from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from utils import randomStr

class Board(QFrame):

    NameChanged = pyqtSignal(object)

    #插件的各个事件函数 在这里得到调用
    def __init__(self, name, parent=None):
        super().__init__(parent)
        self.__plugins = None
        self.__name = name
        self.__id = randomStr(9)#board的唯一标识符
        self.popMenu = QMenu(self)
        self.setMouseTracking(True)
        self.setObjectName("Board")

    def setBackgroundColor(self, color):
        self.setStyleSheet("#Board{background-color:#"+color+"}")

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if value != self.__name:
            self.__name = value
            self.NameChanged.emit(self)

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        if value != self.__id:
            self.__id = value

    def getName(self):
        return self.__name

    def registerPlugins(self, plugins):
        self.__plugins = plugins
        for plugin in self.__plugins:
            #用board初始化plugin
            plugin.boardInit(self)
            #连接信号
            plugin.repaintSignal.connect(self.repaint)

            # 挂载弹出菜单选项
            if plugin.getPopMenus():
                for item in plugin.getPopMenus():
                    if isinstance(item, QMenu):
                        self.popMenu.addMenu(item)
                    elif isinstance(item, QAction):
                        self.popMenu.addAction(item)

    def mouseReleaseEvent(self, QMouseEvent):
        if self.__plugins:
            for plugin in self.__plugins:
                plugin.mouseReleaseEvent(QMouseEvent, self)

    def mousePressEvent(self, QMouseEvent):
        if self.__plugins:
            for plugin in self.__plugins:
                plugin.mousePressEvent(QMouseEvent, self)

    def mouseDoubleClickEvent(self, QMouseEvent):
        if self.__plugins:
            for plugin in self.__plugins:
                plugin.mouseDoubleClickEvent(QMouseEvent, self)

    def mouseMoveEvent(self, QMouseEvent):
        if self.__plugins:
            for plugin in self.__plugins:
                plugin.mouseMoveEvent(QMouseEvent, self)

    def keyPressEvent(self, *args, **kwargs):
        if self.__plugins:
            for plugin in self.__plugins:
                plugin.keyPressEvent(args, self)

    def keyReleaseEvent(self, *args, **kwargs):
        if self.__plugins:
            for plugin in self.__plugins:
                plugin.keyReleaseEvent(args, self)

    def paintEvent(self, QPaintEvent):
        try:
            if self.__plugins:
                for plugin in self.__plugins:
                    plugin.paintEvent(QPaintEvent, self)
        except Exception as e:
            print(e)

    def contextMenuEvent(self,QContextMenuEvent):
        pass
        #self.popMenu.popup(QContextMenuEvent.globalPos())