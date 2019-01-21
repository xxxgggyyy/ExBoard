from designs import SettingContentWidget
from .designs import Ui_PaintShapeSetting
from PyQt5.QtCore import *
from business import ExInterFace

class PaintShapSettingWidget(SettingContentWidget):

    def __init__(self, MainPlugin,parent=None):
        super().__init__(parent)
        self.ui = Ui_PaintShapeSetting()
        self.ui.setupUi(self)
        self.MainPlugin = MainPlugin

        #连接信号和槽
        self.ui.applyBtn.clicked.connect(self.apply)
        self.ui.applayCloseBtn.clicked.connect(self.applyAndClose)
        self.ui.closeBtn.clicked.connect(self.close)

    @pyqtSlot()
    def apply(self):
        #修改MainPlugin的中的值
        self.MainPlugin.unit_pixel = self.ui.unit_pixel.value()
        self.MainPlugin.unit = self.ui.unit.currentIndex()
        self.MainPlugin.font_size = self.ui.font_size.value()
        self.MainPlugin.background_color = self.ui.background_color.text()
        self.MainPlugin.line_width = self.ui.line_width.value()
        #保存到配置文件中
        self.MainPlugin.saveSetting()

        #调用Board接口修改背景色
        #这一句会调用setStyleSheet 所以会重绘
        ExInterFace.setBackgroundColor(self.MainPlugin.background_color)

    @pyqtSlot()
    def applyAndClose(self):
        self.apply()
        self.close()

    @pyqtSlot()
    def close(self):
        self.closeSignal.emit()