from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore

from designs import Ui_PluginManagerWidget,SettingContentWidget

class PluginItem(QFrame):

    clickedSignal = pyqtSignal(object)

    def __init__(self, name, parent=None):
        super().__init__(parent)
        self.hLayout = QHBoxLayout()
        self.setLayout(self.hLayout)
        self.hLayout.setContentsMargins(2,5,2,5)
        self.hLayout.setSpacing(0)
        self.checkBox = QCheckBox(self)
        self.checkBox.setText("")
        self.checkBox.setFixedWidth(20)
        self.checkBox.setChecked(True)
        self.label = QLabel(self)
        self.label.setText(name)
        self.label.setMaximumWidth(300)
        self.hLayout.addWidget(self.label)
        self.hLayout.addWidget(self.checkBox)
        self.__checked = False
        self.setObjectName("PluginItem")

    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == QtCore.Qt.LeftButton:
            # 发射点击信号
            self.clickedSignal.emit(self)

    def isChecked(self):
        return self.__checked

    def setChecked(self, b):
        self.__checked = b
        if self.__checked:
            self.setStyleSheet("#PluginItem{background-color:#1a7dc4}")
        else:
            self.setStyleSheet("#PluginItem{background-color:#ffffff}")


class PluginManagerWidget(SettingContentWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_PluginManagerWidget()
        self.ui.setupUi(self)
        self.itemMap ={}

        #连接信号
        self.ui.close.clicked.connect(self.close)

    def addAllPlugins(self, plugins):
        for plugin in plugins:
            self.addPluginItem(plugin)

    def addPluginItem(self, plugin):

        item = PluginItem(plugin.getPluginName(), self.ui.pluginList)
        item.clickedSignal.connect(self.itemSwitch)
        self.ui.pluginList.layout().addWidget(item)

        # 默认选中第一个
        if not self.itemMap:
            item.setChecked(True)
            # 设置详细信息
            self.ui.pluginName.setText(plugin.getPluginName())
            self.ui.description.setText(plugin.getPluginDescription())

        self.itemMap[item] = plugin

    @pyqtSlot(object)
    def itemSwitch(self,item):
        item.setChecked(True)
        for _item, v in self.itemMap.items():
            if (not item is _item) and _item.isChecked():
                _item.setChecked(False)

        #设置详细信息
        self.ui.pluginName.setText(self.itemMap[item].getPluginName())
        self.ui.description.setText(self.itemMap[item].getPluginDescription())

    @pyqtSlot()
    def close(self):
        self.closeSignal.emit()

    @pyqtSlot()
    def apply(self):
        pass

    @pyqtSlot()
    def applyAndClose(self):
        self.apply()
        self.close()