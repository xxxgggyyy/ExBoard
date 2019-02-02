# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'xml/MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import Qt

class BoardTabWidget(QtWidgets.QTabWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFocusPolicy(Qt.StrongFocus)

    def keyPressEvent(self, QKeyEvent):
        self.currentWidget().keyPressEvent(QKeyEvent)


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
        self.board_tabs = BoardTabWidget(self.centralwidget)
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
"background-color:#1a7dc4\n"
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
        self.dockWidget_3.setMinimumSize(QtCore.QSize(320, 134))
        self.dockWidget_3.setObjectName("dockWidget_3")
        self.tool_dock = QtWidgets.QWidget()
        self.tool_dock.setObjectName("tool_dock")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.tool_dock)
        self.horizontalLayout_2.setContentsMargins(5, 5, 5, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.scrollArea = QtWidgets.QScrollArea(self.tool_dock)
        self.scrollArea.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollArea.setStyleSheet("")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.tool_scrollAreaWidgetContents = QtWidgets.QWidget()
        self.tool_scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 308, 413))
        self.tool_scrollAreaWidgetContents.setStyleSheet("#tool_scrollAreaWidgetContents\n"
"{\n"
"background-color:rgb(255, 255, 255)\n"
"}")
        self.tool_scrollAreaWidgetContents.setObjectName("tool_scrollAreaWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.tool_scrollAreaWidgetContents)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea.setWidget(self.tool_scrollAreaWidgetContents)
        self.horizontalLayout_2.addWidget(self.scrollArea)
        self.dockWidget_3.setWidget(self.tool_dock)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget_3)
        self.dockWidget = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget.setObjectName("dockWidget")
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.dockWidgetContents)
        self.horizontalLayout.setContentsMargins(5, 5, 5, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.board_pro_table = QtWidgets.QTableWidget(self.dockWidgetContents)
        self.board_pro_table.setStyleSheet("QTableWidget::Item{background-color:#ffffde;color:black}\n"
"QTableWidget::Item:selected\n"
"{\n"
"background-color: #0078d7\n"
"}\n"
"")
        self.board_pro_table.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked)
        self.board_pro_table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.board_pro_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.board_pro_table.setRowCount(0)
        self.board_pro_table.setColumnCount(2)
        self.board_pro_table.setObjectName("board_pro_table")
        item = QtWidgets.QTableWidgetItem()
        self.board_pro_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.board_pro_table.setHorizontalHeaderItem(1, item)
        self.board_pro_table.horizontalHeader().setHighlightSections(False)
        self.board_pro_table.horizontalHeader().setStretchLastSection(True)
        self.board_pro_table.verticalHeader().setVisible(False)
        self.horizontalLayout.addWidget(self.board_pro_table)
        self.dockWidget.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget)
        self.actionnew_board = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/res/img/new.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionnew_board.setIcon(icon)
        self.actionnew_board.setAutoRepeat(True)
        self.actionnew_board.setIconVisibleInMenu(True)
        self.actionnew_board.setShortcutVisibleInContextMenu(True)
        self.actionnew_board.setObjectName("actionnew_board")
        self.actionsetting = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/res/img/setting.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionsetting.setIcon(icon1)
        self.actionsetting.setObjectName("actionsetting")
        self.file_menu.addAction(self.actionnew_board)
        self.file_menu.addAction(self.actionsetting)
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
        self.dockWidget.setWindowTitle(_translate("MainWindow", "Board属性"))
        item = self.board_pro_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "属性"))
        item = self.board_pro_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "值"))
        self.actionnew_board.setText(_translate("MainWindow", "新建Board"))
        self.actionnew_board.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.actionsetting.setText(_translate("MainWindow", "设置"))
