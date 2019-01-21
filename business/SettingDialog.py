from designs import Ui_SettingDialog,SettingListWidget,SettingListItem,SettingContentWidget

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class DefaultSettingContent(SettingContentWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        #self.defaultContentWdg = QWidget(self.ui.content)
        self.defaultContentLayout = QVBoxLayout(self)
        self.defaultContentVspacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.setLayout(self.defaultContentLayout)
        self.defaultContentLable = QLabel("这个插件没有设置选项")
        self.defaultContentLable.setStyleSheet("font-size:20px;color:gray")
        self.defaultContentLayout.addWidget(self.defaultContentLable)
        self.defaultContentLayout.addItem(self.defaultContentVspacer)


class SettingDialog(QDialog):

    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self.ui = Ui_SettingDialog()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(":/res/img/setting.png"))
        self.listWdg = SettingListWidget(self)
        self.ui.plugin_list.layout().addWidget(self.listWdg)
        self.__itemMap = {}

        self.defaultContentWdg = DefaultSettingContent(self)
        self.defaultContentWdg.setVisible(False)

    def addPluginSetting(self, pluginName, uiWdg):
        if not isinstance(uiWdg, SettingContentWidget):
            raise TypeError("setting widget must inherit SettingContentWidget")
        item = SettingListItem(pluginName, self.listWdg)
        if not uiWdg:
            uiWdg = self.defaultContentWdg
        #连接关闭信号
        uiWdg.closeSignal.connect(self.close)
        uiWdg.setVisible(False)
        item.changedSignal.connect(self.itemSwitched)
        self.ui.content.layout().addWidget(uiWdg)
        self.listWdg.addItem(item)
        #默认选中第一个
        if not self.__itemMap:
            item.setChecked(True)
            uiWdg.setVisible(True)
            self.ui.content.setTitle(item.getText())
        self.__itemMap[item] = uiWdg

    @pyqtSlot(object)
    def itemSwitched(self, item):
        for _item, setting in self.__itemMap.items():
            if setting.isVisible():
                setting.setVisible(False)
                break
        self.__itemMap[item].setVisible(True)
        self.ui.content.setTitle(item.getText())
