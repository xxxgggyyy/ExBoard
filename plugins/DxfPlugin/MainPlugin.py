from business import Plugin,ExInterFace

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMenu,QAction
from PyQt5.QtGui import QMouseEvent, QIcon

from .designs import resources
from .DxfReader import DxfReader,Entity

class MainPlugin(Plugin):

    def __init__(self, name):
        super().__init__(name)

        self.importAction = QAction(QIcon(":/dxfplugin_res/img/import.png"), "导入dxf文件", None)#讲道理 这里可以用eval简化写法
        self.importAction.triggered.connect(self.importActionTrigger)

    @pyqtSlot()
    def importActionTrigger(self):
        print(DxfReader.GetLayers("D:/test.dxf"))
        print(DxfReader.GetShapeData("D:/test.dxf", Entity.LINE))

    def getPluginDescription(self):
        return '''读取cad的dxf格式的文件'''

    def getFileMenus(self, type):
        if type==QMenu:
            return None
        elif type==QAction:
            return [self.importAction]
        else:
            return None