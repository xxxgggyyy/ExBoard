from designs import Ui_MainWindow
from designs import DrawerWidget
from .Board import Board
from .ExInterFace import ExInterFace
from .SettingDialog import SettingDialog
from .PluginManagerWidget import PluginManagerWidget


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

        self.__board_properties = [{'proName':'id','name':"Id",'itemWdg':None,'type':str}, {'proName':'name','name':'Name', 'itemWdg': None, 'type': str}]#属性实际的名字:{}

        #设置底部控件
        self.taskName = QLabel("当前Task: ")
        self.taskProgress = QProgressBar()
        self.taskProgress.setStyleSheet('QProgressBar{border:2px solid grey;border-radius:5px;text-align:center;}QProgressBar::chunk{background-color:#05B8CC;width:20px;}')
        self.taskProgress.setMaximum(100)
        self.taskProgress.setMinimum(0)
        self.taskProgress.setMaximumWidth(200)
        self.taskProgress.setVisible(False)
        self.ui.statusbar.addWidget(self.taskName)
        self.ui.statusbar.addWidget(self.taskProgress)

        #初始化设置对话框
        self.settingDialog = SettingDialog(self)
        self.ui.actionsetting.triggered.connect(self.settingDialog.show)
        #设置插件管理 设置
        self.pluginManagerWidget = PluginManagerWidget(self.settingDialog)
        self.settingDialog.addPluginSetting("PluginManager", self.pluginManagerWidget)

        #连接信号和槽

        #连接newBoard的
        self.ui.actionnew_board.triggered.connect(self.newBoard)
        #tab切换的信号
        self.ui.board_tabs.currentChanged.connect(self.boardSwitched)

    def __last_init(self):#插件加载完毕后执行的一些初始化
        #根据加载的Board属性列建立Item
        self.ui.board_pro_table.setRowCount(len(self.__board_properties))
        self.ui.board_pro_table.setColumnCount(2)
        for i, details in enumerate(self.__board_properties):
            name_item = QTableWidgetItem(details['name'])
            value_item = self.__board_properties[i]['itemWdg']
            # 设置属性列 不可编辑
            name_item.setFlags(Qt.NoItemFlags)
            self.ui.board_pro_table.setItem(i, 0, name_item)
            if not value_item:
                value_item = QTableWidgetItem()
                self.ui.board_pro_table.setItem(i, 1, value_item)
            else:
                self.ui.board_pro_table.setCellWidget(i, 1, value_item)

        #Item值改变时的信号
        self.ui.board_pro_table.itemChanged.connect(self.boardPropertyChanged)

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
            #挂载Board需要显示和可修改的属性列表

            #挂载插件设置界面控件
            self.settingDialog.addPluginSetting(plugin.getPluginName(), plugin.getPluginSettingWidget())

        #放入插件管理器控件
        self.pluginManagerWidget.addAllPlugins(plugins)

        self.__last_init()

    @pyqtSlot(QTableWidgetItem)
    def boardPropertyChanged(self, item):
        row = self.ui.board_pro_table.indexFromItem(item).row()
        board = self.ui.board_tabs.currentWidget()
        setattr(board,self.__board_properties[row]['proName'], item.text())

    @pyqtSlot(int)
    def closeTab(self, index):
        if self.ui.board_tabs.count() > 1:
            self.ui.board_tabs.removeTab(index)

    @pyqtSlot()
    def newBoard(self):
        board = ExInterFace.addBorad("new")
        #定位到新建的Board
        self.ui.board_tabs.setCurrentWidget(board)

    @pyqtSlot(int)
    def boardSwitched(self , curindex):
        curBoard = self.ui.board_tabs.currentWidget()
        if curBoard:
            #刷新Boar的属性表
            for i, details in enumerate(self.__board_properties):
                value = getattr(curBoard, details['proName'], "未知")
                self.ui.board_pro_table.item(i, 1).setText(value)

    @pyqtSlot(object)
    def updateBoardName(self, Board):
        self.ui.board_tabs.setTabText(self.ui.board_tabs.indexOf(Board), Board.name)

    def addBoard(self,board):
        #if not self.__plugins:
            #raise RuntimeError("插件没有注册到MainWindow中")
        board.registerPlugins(self.__plugins)
        self.ui.board_tabs.addTab(board, board.name)
        #tab_index = self.ui.board_tabs.indexOf(board)
        board.NameChanged.connect(self.updateBoardName)
        return board

    def removeBoard(self, b):
        if isinstance(b, int):
            self.ui.board_tabs.removeTab(b)
        elif isinstance(b, Board):
            self.ui.board_tabs.removeTab(self.ui.board_tabs.indexOf(b))

    def getAllBoards(self):
        re = []
        for i in range(self.ui.board_tabs.count()):
            re.append(self.ui.board_tabs.widget(i))
        return re