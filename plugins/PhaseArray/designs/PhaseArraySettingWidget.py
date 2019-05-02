# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'xml/PhaseArraySettingWidget.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PhaseArray(object):
    def setupUi(self, PhaseArray):
        PhaseArray.setObjectName("PhaseArray")
        PhaseArray.resize(807, 740)
        self.verticalLayout = QtWidgets.QVBoxLayout(PhaseArray)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(PhaseArray)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)

        self.retranslateUi(PhaseArray)
        QtCore.QMetaObject.connectSlotsByName(PhaseArray)

    def retranslateUi(self, PhaseArray):
        _translate = QtCore.QCoreApplication.translate
        PhaseArray.setWindowTitle(_translate("PhaseArray", "Frame"))
        self.label.setText(_translate("PhaseArray", "this is a test frame"))


