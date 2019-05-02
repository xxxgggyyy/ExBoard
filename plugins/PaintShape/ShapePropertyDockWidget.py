from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from business import ExInterFace

class ShapePropertyTableItem:

    def __init__(self):
        self.shape = None
        self.proName = None

    def setShape(self, shape, proName):
        self.shape = shape
        self.proName = proName

    def setValue(self, value):
        pass

    def getValue(self):
        pass


class NumEditItem(QDoubleSpinBox,ShapePropertyTableItem):

    def __init__(self):
        super().__init__()
        self.valueChanged.connect(self.valueChangedSlot)

    @pyqtSlot(float)
    def valueChangedSlot(self, value):
        if self.shape and self.proName:
            setattr(self.shape, self.proName, self.getValue())  # 为shape赋值
            ExInterFace.getCurrentBoard().repaint()

    def getValue(self):
        return self.value()

class ExPointItem(QLineEdit, ShapePropertyTableItem):

    def __init__(self):
        super().__init__()
        #连接自身的信号
        self.textEdited.connect(self.valueChanged)
        self.oriValue = None

    def setValue(self, value):
        from .ExShape import ExPoint#防止交叉引用
        if isinstance(value, ExPoint):
            self.oriValue = "%.2f,%.2f" % (value.x,value.y)
            self.setText(self.oriValue)

    def getValue(self):
        from .ExShape import ExPoint
        try:
            text = self.text()
            text.index(",")
            values = text.split(",")
            if len(values) != 2:
                raise ValueError("只要两个数")
            value = ExPoint(float(values[0]), float(values[1]))
            self.oriValue = "%.2f,%.2f" % (value.x, value.y)
            return value
        except ValueError as e:
            # 没有找到',' 或者其他格式错误 不修改 直接赋予原值
            raise e


    @pyqtSlot(str)
    def valueChanged(self, text):
        try:
            if self.shape and self.proName:
                setattr(self.shape, self.proName, self.getValue())  # 为shape赋值

                ExInterFace.getCurrentBoard().repaint()
        except ValueError as e:
            #没有找到',' 或者其他格式错误 不修改 直接赋予原值
            self.setText(self.oriValue)

class QColorItem(QLineEdit, ShapePropertyTableItem):

    def __init__(self):
        super().__init__()
        #连接自身的信号
        self.textEdited.connect(self.valueChanged)
        self.oriValue = None


    def setValue(self, value):
        if isinstance(value, QColor):
            self.oriValue = "%d,%d,%d" % (value.red(),value.green(),value.blue())
            self.setText(self.oriValue)

    def getValue(self):
        try:
            text = self.text()
            values = text.split(",")
            if len(values) != 3:
                raise ValueError("只要三个数")
            r = float(values[0])
            g = float(values[1])
            b = float(values[2])
            if r<0 or r>255 or g<0 or g>255 or b<0 or b>255:
                raise ValueError("超出颜色值的范围")
            value = QColor(r, g, b)
            self.oriValue = "%d,%d,%d" % (r, g, b)
            return value
        except ValueError as e:
            # 没有找到',' 或者其他格式错误 不修改 直接赋予原值
            raise e


    @pyqtSlot(str)
    def valueChanged(self, text):
        try:
            if self.shape and self.proName:
                setattr(self.shape, self.proName, self.getValue())  # 为shape赋值
                ExInterFace.getCurrentBoard().repaint()
        except ValueError as e:
            #没有找到',' 或者其他格式错误 不修改 直接赋予原值
            self.setText(self.oriValue)



class BoolComboBox(QComboBox, ShapePropertyTableItem):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.addItem("True", None)
        self.addItem("False", None)

        #连接自身的信号
        self.currentIndexChanged.connect(self.currentIndexChangedSlot)


    @pyqtSlot(int)
    def currentIndexChangedSlot(self, index):
        if self.shape and self.proName:
            setattr(self.shape, self.proName, self.getValue())
            ExInterFace.getCurrentBoard().repaint()

    def setShape(self, shape, proName):
        self.shape = shape
        self.proName = proName

    def setValue(self, b):
        if b:
            self.setCurrentIndex(0)
        else:
            self.setCurrentIndex(1)

    def getValue(self):
        if self.currentIndex()==0:
            return True
        else:
            return False




class ShapePropertyDockWidget(QDockWidget):

    def __init__(self, title,parent=None):
        super().__init__(title, parent)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.setWidget(self.dockWidgetContents)
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.dockWidgetContents)
        self.horizontalLayout.setContentsMargins(5, 5, 5, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.dockWidgetContents.setLayout(self.horizontalLayout)

        self.shapePropertyTable = QtWidgets.QTableWidget(self.dockWidgetContents)
        self.shapePropertyTable.setStyleSheet("QTableWidget::Item{background-color:#ffffde;color:black}\n"
                                           "QTableWidget::Item:selected\n"
                                           "{\n"
                                           "background-color: #0078d7\n"
                                           "}\n"
                                           "")
        self.shapePropertyTable.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked)
        self.shapePropertyTable.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.shapePropertyTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.shapePropertyTable.setRowCount(100)
        self.shapePropertyTable.setColumnCount(2)
        self.shapePropertyTable.setObjectName("shapePropertyTable")
        item = QtWidgets.QTableWidgetItem()
        item.setText("属性")
        self.shapePropertyTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("值")
        self.shapePropertyTable.setHorizontalHeaderItem(1, item)
        self.shapePropertyTable.horizontalHeader().setHighlightSections(False)
        self.shapePropertyTable.horizontalHeader().setStretchLastSection(True)
        self.shapePropertyTable.verticalHeader().setVisible(False)
        self.horizontalLayout.addWidget(self.shapePropertyTable)

        self.currentShape = None

    def clearAll(self):
        self.shapePropertyTable.clearContents()

    def updateValues(self, shape):
        self.shapePropertyTable.clearContents()
        self.currentShape = shape
        propertyList = self.currentShape.getPropertiesList()
        self.shapePropertyTable.setRowCount(len(propertyList))
        for i in range(len(propertyList)):

            nameItem = QTableWidgetItem(propertyList[i]['name'])
            nameItem.setFlags(Qt.NoItemFlags)
            self.shapePropertyTable.setItem(i, 0, nameItem)
            nameItem.setText(propertyList[i]['name'])

            valueItem = propertyList[i]['itemWdg']
            if not valueItem:
                valueItem = QTableWidgetItem(str(getattr(self.currentShape, propertyList[i]['proName'], None)))
                self.shapePropertyTable.setItem(i, 1, valueItem)
            else:
                self.shapePropertyTable.setCellWidget(i, 1, valueItem)

            if isinstance(valueItem, ShapePropertyTableItem):
                valueItem.setShape(self.currentShape, propertyList[i]['proName'])
                valueItem.setValue(getattr(self.currentShape, propertyList[i]['proName']))

    @pyqtSlot(QTableWidgetItem)
    def shapePropertyChanged(self, item):
        row = self.shapePropertyTable.indexFromItem(item).row()
        self.currentShape.changeValueByPropertiesList(row, item.text())




