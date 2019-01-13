from designs import Ui_MainWindow
from designs import DrawerWidget
from .Board import Board
from .ExInterFace import ExInterFace

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
        self.ui.board_tabs.tabCloseRequested.connect(self.closeTab)
        self.__plugins = None

        #连接信号和槽

        #连接newBoard的
        self.ui.actionnew_board.triggered.connect(self.newBoard)

    def registerPulgins(self, plugins):
        self.__plugins = plugins
        for plugin in self.__plugins:
            # 执行插件的初始化代码
            plugin.init()
            # 挂载侧边栏工具
            drawerItems = plugin.getToolItems()
            if drawerItems:
                for drawerItem in drawerItems:
                    self.drawerWdg.addDrawerItem(drawerItem)
            #挂载菜单栏按钮
            if plugin.getFileMenus(QAction):
                for action in plugin.getFileMenus(QAction):
                    self.ui.file_menu.addAction(action)
            if plugin.getFileMenus(QAction):
                for menu in plugin.getFileMenus(QMenu):
                    self.ui.file_menu.addMenu(menu)

    @pyqtSlot(int)
    def closeTab(self, index):
        if self.ui.board_tabs.count()>1:
            self.ui.board_tabs.removeTab(index)

    @pyqtSlot()
    def newBoard(self):
        ExInterFace.addBorad("new")

    def addBoard(self,board):
        #if not self.__plugins:
            #raise RuntimeError("插件没有注册到MainWindow中")
        board.registerPlugins(self.__plugins)
        self.ui.board_tabs.addTab(board, board.name)
        tab_index = self.ui.board_tabs.indexOf(board)
        return tab_index

    def removeBoard(self, b):
        if isinstance(b, int):
            self.ui.board_tabs.removeTab(b)
        elif isinstance(b, Board):
            self.ui.board_tabs.removeTab(self.ui.board_tabs.indexOf(b))