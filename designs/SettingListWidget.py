
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore

class SettingListItem(QFrame):

    clickedSignal = pyqtSignal(object, bool)
    changedSignal = pyqtSignal(object)

    def __init__(self, name,parent):
        super().__init__(parent)
        self.hLayout = QHBoxLayout(self)
        self.hLayout.setContentsMargins(0,0,0,0)
        self.hLayout.setSpacing(0)
        self.setLayout(self.hLayout)
        self.iconBtn = QPushButton('',self)
        self.iconBtn.setFlat(True)
        self.iconBtn.setFixedHeight(30)
        self.iconBtn.setFixedWidth(50)
        self.textBtn = QPushButton(name)
        self.textBtn.setFlat(True)
        self.textBtn.setEnabled(False)
        self.hLayout.addWidget(self.textBtn)
        self.hLayout.addWidget(self.iconBtn)
        self.__checked = False
        self.rIcon = QIcon(":/res/img/rArrow.png")
        self.setObjectName("pluginListItem")
        self.setStyleSheet("#pluginListItem:hover{background-color:#1a7dc4}QPushButton{color:black;text-align:left}")
        self.textBtn.installEventFilter(self)
        self.iconBtn.installEventFilter(self)
        self.__name = name

    def getText(self):
        return self.__name

    def eventFilter(self, QObject, QEvent):
        if QObject is self.textBtn or QObject is self.iconBtn:
            if QEvent.type() == QtCore.QEvent.MouseButtonPress:
                if QEvent.button() == QtCore.Qt.LeftButton:
                    #self.__checked = not self.__checked
                    if not self.__checked:
                        self.__checked = True
                        self.iconBtn.setIcon(self.rIcon)
                        self.changedSignal.emit(self)
                    #else:
                        #self.iconBtn.setIcon(QIcon())

                    return True
            else:
                return False
        else:
            return False

    def isChecked(self):
        return self.__checked

    def setChecked(self, b):
        self.__checked = b
        if self.__checked:
            self.iconBtn.setIcon(self.rIcon)
        else:
            self.iconBtn.setIcon(QIcon())


class SettingListWidget(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.vLayout = QVBoxLayout(self)
        self.setLayout(self.vLayout)
        self.vLayout.setContentsMargins(5,5,5,5)
        self.vLayout.setSpacing(0)
        self.vspacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.upWdgLayout = QVBoxLayout(self)
        self.upWdgLayout.setContentsMargins(0, 0, 0, 0)
        self.upWdgLayout.setSpacing(0)

        self.vLayout.addLayout(self.upWdgLayout)
        self.vLayout.addItem(self.vspacer)

        self.__items = []


    def addItem(self, listItem):
        self.__items.append(listItem)
        self.upWdgLayout.addWidget(listItem)
        listItem.changedSignal.connect(self.itemToggled)

    @pyqtSlot(object)
    def itemToggled(self,item):
        for i in self.__items:
            if not i is item and i.isChecked():
                i.setChecked(False)
                break