from business import Plugin,ExInterFace

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMenu,QAction, QFileDialog, QMessageBox
from PyQt5.QtGui import QMouseEvent, QIcon

from .designs import resources
from .DxfReader import DxfReader,Entity,EntitiesSection, TablesSection
from .DxfReader import Table as dxfTable

class MainPlugin(Plugin):

    def __init__(self, name):
        super().__init__(name)

        self.importAction = QAction(QIcon(":/dxfplugin_res/img/import.png"), "导入dxf文件", None)#讲道理 这里可以用eval简化写法
        self.importAction.triggered.connect(self.importActionTrigger)

    @pyqtSlot()
    def importActionTrigger(self):
        file_path, ext = QFileDialog.getOpenFileName(filter="*.dxf")
        if file_path:#如果选择了文件
            if ext != '*.dxf':
                QMessageBox.warning(None, "文件格式错误","只能导入.dxf格式的cad文件", QMessageBox.Yes)

            try:
                dxfReader = DxfReader(file_path)
                sections = dxfReader.ParseSections()
                layers = []#解析出的图层数据
                shapes = []#解析出的图元数据
                for section in sections:
                    if isinstance(section, TablesSection):#先解析出图层
                        tables = section.ParseTables(dxfTable.LAYER)
                        for table in tables:
                            entries = table.ParseEntries()
                            for entry in entries:
                                layers.append(entry.parse())
                    elif isinstance(section, EntitiesSection):
                        entities = section.ParseEntities(None)#解析出所有的图元
                        for entity in entities:
                            shapes.append(entity.parse())

                boards = []
                for layer in layers:
                    boards.append(ExInterFace.addBorad(layer["name"]))
                paintShape = ExInterFace.getPlugin('PaintShape')
                for shape in shapes:
                    for board in boards:
                        if board.name == shape['layer']:
                            paintShape.addShape(board, MainPlugin.ShapeFromObject(shape))
                            break
            except Exception as e:
                QMessageBox.critical(None, "文件解析出错", str(e),QMessageBox.Yes)
                print("异常:"+str(e))

    @staticmethod
    def ShapeFromObject(dxfobject):
        from plugins.PaintShape import ExShape
        if dxfobject['type'] == 'line':
            return ExShape.ExLine(dxfobject['x0'],dxfobject['y0'],dxfobject['x1'],dxfobject['y1'])
        if dxfobject['type'] == 'arc':
            if dxfobject['angle_1'] > dxfobject['angle_0']:
                spanAngle = dxfobject['angle_1'] - dxfobject['angle_0']
            else:
                spanAngle = 360 - dxfobject['angle_0'] + dxfobject['angle_1']
            return ExShape.ExArc(dxfobject['x'],dxfobject['y'],dxfobject['r'],360 - dxfobject['angle_1'],spanAngle)


    def getPluginDescription(self):
        return '''读取cad的dxf格式的文件'''

    def getFileMenus(self, type):
        if type==QMenu:
            return None
        elif type==QAction:
            return [self.importAction]
        else:
            return None