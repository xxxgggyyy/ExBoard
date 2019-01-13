from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.Qt import *
from PyQt5 import QtCore
import designs.resources


class DrawerContentItem(QFrame):

    __CHECKABLE_STYLE = "#drawerContentItem{background-color:#fffefc}QPushButton{color:black;text-align:left}"
    __UNCHECKABLE_STYLE = "#drawerContentItem{background-color:#fffefc}QPushButton{color:black;text-align:left}#drawerContentItem:hover{background-color:#defffa}"
    __CHECKED_STYLE = "#drawerContentItem{background-color:rgba(255, 170, 127, 120)}QPushButton{color:black;text-align:left}"

    # 定义信号
    clickedSignal = pyqtSignal(object,bool)

    def __init__(self, title, icon=None, parent=None):
        super().__init__(parent)
        self.checkable = True
        self.hLayout = QHBoxLayout(self)
        self.hLayout.setContentsMargins(0,0,0,0)
        self.hLayout.setSpacing(0)
        self.setLayout(self.hLayout)
        self.iconBtn = QPushButton('',self)
        if not icon:
            icon = QIcon(":/res/img/none.png")
        self.iconBtn.setIcon(icon)
        self.iconBtn.setMaximumSize(30,30)
        self.iconBtn.setEnabled(False)
        self.iconBtn.setFlat(True)
        self.titleBtn = QPushButton(title,self)
        self.titleBtn.setEnabled(False)
        self.titleBtn.setFlat(True)
        #必须为Btn设置事件过滤器
        self.iconBtn.installEventFilter(self)
        self.titleBtn.installEventFilter(self)
        self.hLayout.addWidget(self.iconBtn)
        self.hLayout.addWidget(self.titleBtn)
        self.setObjectName("drawerContentItem")
        self.setStyleSheet(self.__CHECKABLE_STYLE)
        #选中状态
        self.__checked = False


    def setCheckable(self, bool):
        self.checkable = bool
        if not self.checkable:
            self.setStyleSheet(self.__UNCHECKABLE_STYLE)
        else:
            self.setStyleSheet(self.__CHECKABLE_STYLE)

    def isChecked(self):
        return self.__checked

    def setChecked(self,b):
        self.__checked = b
        if self.checkable:
            if self.__checked:
                # 设置选中时的样式
                self.setStyleSheet(self.__CHECKED_STYLE)
            else:
                # 恢复样式
                self.setStyleSheet(self.__CHECKABLE_STYLE)


    def eventFilter(self, QObject, QEvent):
        if QObject is self.titleBtn or QObject is self.iconBtn:
            if QEvent.type() == QtCore.QEvent.MouseButtonPress:
                if QEvent.button() == QtCore.Qt.LeftButton:
                    self.__checked = not self.__checked
                    if self.checkable:
                        if self.__checked:
                            #设置选中时的样式
                            self.setStyleSheet(self.__CHECKED_STYLE)
                        else:
                            #恢复样式
                            self.setStyleSheet(self.__CHECKABLE_STYLE)
                    #发射点击信号
                    self.clickedSignal.emit(self, self.__checked)
                    return True
            else:
                return False
        else:
            return False



class DrawerItemHeader(QFrame):

    def __init__(self, title, parent=None):
        super().__init__(parent=parent)
        self.dIcon = QIcon(":/res/img/arrowD.png")
        self.rIcon = QIcon(":/res/img/arrowR.png")
        self.hLayout = QHBoxLayout()
        self.setLayout(self.hLayout)
        self.hLayout.setDirection(QHBoxLayout.LeftToRight)
        self.hLayout.setContentsMargins(0, 0, 0, 0)
        self.hLayout.setSpacing(0)
        self.labelBtn = QPushButton(self.rIcon, '', self)
        self.labelBtn.setFixedSize(30, 30)
        self.labelBtn.setFlat(True)
        self.labelBtn.setEnabled(False)
        self.titleBtn = QPushButton(title, self)
        self.titleBtn.setFixedHeight(30)
        self.titleBtn.setFlat(True)
        self.titleBtn.setEnabled(False)
        self.titleBtn.installEventFilter(self)
        self.labelBtn.installEventFilter(self)
        self.setObjectName("drawerHeader")
        self.setStyleSheet("#drawerHeader{border:1px solid gray;background-color:#e9e7e5}QPushButton{color:black}")
        self.hLayout.addWidget(self.labelBtn)
        self.hLayout.addWidget(self.titleBtn)
        self.toggleState = False

    def setBody(self,body):
        self.body = body

    def eventFilter(self, QObject, QEvent):
        if QObject is self.titleBtn or QObject is self.labelBtn:
            if QEvent.type() == QtCore.QEvent.MouseButtonPress:
                if QEvent.button() == QtCore.Qt.LeftButton:
                    if self.body:
                        self.toggleState = not self.toggleState
                        self.body.setVisible(self.toggleState)
                        if self.toggleState:
                            self.labelBtn.setIcon(self.dIcon)
                        else:
                            self.labelBtn.setIcon(self.rIcon)

                    return True
            else:
                return False
        else:
            return False

class DrawerItem(QFrame):

    SINGLE_TOGGLE = 0#在同一时刻只有一个能保持触发状态
    MULTI_TOGGLE = 1#在同一时刻可以有多个个能保持触发状态

    def __init__(self, title, parent=None):
        super().__init__(parent)
        #上半部分 标题
        self.upFrame = DrawerItemHeader(title)

        #下半部分 通过点击打开关闭
        self.dVLayout = QVBoxLayout()
        self.dVLayout.setContentsMargins(0, 0, 0, 0)
        self.dVLayout.setSpacing(0)
        self.downFrame = QFrame(self)
        self.downFrame.setLayout(self.dVLayout)

        self.vLayout = QVBoxLayout(self)
        self.vLayout.setContentsMargins(0, 0, 0, 0)
        self.vLayout.setSpacing(0)
        self.vLayout.addWidget(self.upFrame)
        self.vLayout.addWidget(self.downFrame)
        self.setLayout(self.vLayout)

        self.downFrame.setVisible(False)
        self.upFrame.setBody(self.downFrame)

        self.toggle_mode = DrawerItem.SINGLE_TOGGLE
        self.contentItems = []

    def addContentItem(self, item):
        if isinstance(item, DrawerContentItem):
            self.dVLayout.addWidget(item)
            self.contentItems.append(item)
            item.clickedSignal.connect(self.contentItemToggled)
        else:
            raise TypeError("item must inherit DrawerContentItem")

    @pyqtSlot(object,bool)
    def contentItemToggled(self, obj,b):
        if self.toggle_mode == self.SINGLE_TOGGLE:
            if b:
                for item in self.contentItems:
                    if not item is obj and item.isChecked():
                        item.setChecked(False)
                        break


    def setToggleModel(self, mode):
        self.toggle_mode = mode



class DrawerWidget(QWidget):

    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout)
        self.upWdgLayout = QVBoxLayout()
        self.upWdgLayout.setContentsMargins(0, 0, 0, 0)
        self.vspacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout.addLayout(self.upWdgLayout)
        self.verticalLayout.addItem(self.vspacer)
        self.upWdgLayout.setSpacing(1)


    def addDrawerItem(self, obj):
        self.upWdgLayout.addWidget(obj)

