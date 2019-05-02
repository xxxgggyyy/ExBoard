from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMenu,QAction,QFrame
from PyQt5.QtGui import QMouseEvent,QIcon

#from .designs import resources
from .PhaseArraySettingWidget import PhaseArraySettingWidget

from business import Plugin,ExInterFace
from designs import DrawerItem, DrawerContentItem

class MainPlugin(Plugin):

    def __init__(self, name):
        super().__init__(name)
        self.PhaseArraySettingWidget = PhaseArraySettingWidget(self)

        self.PhaseArrayMen = QMenu("相控阵")

        self.__drawerItem = DrawerItem("相控阵")
        self.__allContentItem = []

        self.__runAllContentItem = DrawerContentItem("运行(&R)", parent=self.__drawerItem,
                                                  icon=QIcon(":/paintshape_res/img/line.png"))
        self.__allContentItem.append(self.__runAllContentItem)


        self.__drawerItem.addContentItems(self.__allContentItem)

        # 连接contentItem的点击信号
        for item in self.__allContentItem:
            item.clickedSignal.connect(self.drawerItemChanged)

    @pyqtSlot(object, bool)
    def drawerItemChanged(self, item, checked):
        pass


    def getTopToolBarActions(self):
        return []

    def getToolItems(self):
        return [self.__drawerItem]

    def getMenu(self):
        return self.PhaseArrayMen

    def getPluginSettingWidget(self):
        #return self.PhaseArraySettingWidget
        return None

    def getPluginDescription(self):
        return '''相控阵检测工艺设计'''

    # 这些定义的接口将在 Board中相应的函数中得到调用
    def keyPressEvent(self, QKeyEvent):
        pass

    def keyReleaseEvent(self, QKeyEvent):
        pass


    def mouseDoubleClickEvent(self, QMouseEvent):
        pass

    def mouseMoveEvent(self, QMouseEvent):
        pass

    def mousePressEvent(self, QMouseEvent):
        pass

    def mouseReleaseEvent(self, QMouseEvent):
        pass

    def wheelEvent(self, QWheelEvent):
        pass

    def paintEvent(self, QPaintEvent):
        pass