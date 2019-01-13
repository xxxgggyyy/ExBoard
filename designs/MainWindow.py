# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'xml/MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1186, 818)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(0, 1, 0, 0)
        self.gridLayout.setHorizontalSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.board_tabs = QtWidgets.QTabWidget(self.centralwidget)
        self.board_tabs.setTabsClosable(True)
        self.board_tabs.setMovable(True)
        self.board_tabs.setObjectName("board_tabs")
        self.gridLayout.addWidget(self.board_tabs, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1186, 26))
        self.menubar.setStyleSheet("QMenu{background-color:#606a85;\n"
"color:rgb(255, 255, 255)}\n"
"QMenu::Item:selected{\n"
"background-color:rgba(255, 170, 0, 60)\n"
"}")
        self.menubar.setObjectName("menubar")
        self.file_menu = QtWidgets.QMenu(self.menubar)
        self.file_menu.setStyleSheet("")
        self.file_menu.setObjectName("file_menu")
        self.tool_menu = QtWidgets.QMenu(self.menubar)
        self.tool_menu.setObjectName("tool_menu")
        MainWindow.setMenuBar(self.menubar)
        self.top_toolBar = QtWidgets.QToolBar(MainWindow)
        self.top_toolBar.setStyleSheet("background-color:#ffffff")
        self.top_toolBar.setObjectName("top_toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.top_toolBar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.dockWidget_3 = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget_3.setMinimumSize(QtCore.QSize(320, 122))
        self.dockWidget_3.setObjectName("dockWidget_3")
        self.tool_dock = QtWidgets.QWidget()
        self.tool_dock.setObjectName("tool_dock")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tool_dock)
        self.gridLayout_2.setContentsMargins(5, 5, 5, 5)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.scrollArea = QtWidgets.QScrollArea(self.tool_dock)
        self.scrollArea.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollArea.setStyleSheet("")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.tool_scrollAreaWidgetContents = QtWidgets.QWidget()
        self.tool_scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 308, 716))
        self.tool_scrollAreaWidgetContents.setStyleSheet("#tool_scrollAreaWidgetContents\n"
"{\n"
"background-color:rgb(255, 255, 255)\n"
"}")
        self.tool_scrollAreaWidgetContents.setObjectName("tool_scrollAreaWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.tool_scrollAreaWidgetContents)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea.setWidget(self.tool_scrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.scrollArea, 0, 0, 1, 1)
        self.dockWidget_3.setWidget(self.tool_dock)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget_3)
        self.actionnew_board = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/res/img/new.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionnew_board.setIcon(icon)
        self.actionnew_board.setAutoRepeat(True)
        self.actionnew_board.setIconVisibleInMenu(True)
        self.actionnew_board.setShortcutVisibleInContextMenu(True)
        self.actionnew_board.setObjectName("actionnew_board")
        self.actionsave = QtWidgets.QAction(MainWindow)
        self.actionsave.setObjectName("actionsave")
        self.file_menu.addAction(self.actionnew_board)
        self.menubar.addAction(self.file_menu.menuAction())
        self.menubar.addAction(self.tool_menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.file_menu.setTitle(_translate("MainWindow", "文件"))
        self.tool_menu.setTitle(_translate("MainWindow", "工具"))
        self.dockWidget_3.setWindowTitle(_translate("MainWindow", "工具"))
        self.actionnew_board.setText(_translate("MainWindow", "新建Board"))
        self.actionnew_board.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.actionsave.setText(_translate("MainWindow", "保存"))

