from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *


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

            if propertyList[i]['type'] == QColor:
                color = getattr(self.currentShape, propertyList[i]['proName'])
                valueItem.setText(str(color.red())+","+str(color.green())+","+str(color.blue()))
            elif propertyList[i]['type'] == bool:
                valueItem.setText(str(getattr(self.currentShape, propertyList[i]['proName'])))



    @pyqtSlot(QTableWidgetItem)
    def shapePropertyChanged(self, item):
        row = self.shapePropertyTable.indexFromItem(item).row()
        self.currentShape.changeValueByPropertiesList(row, item.text())




