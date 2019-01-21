# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'xml/SettingDialog.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SettingDialog(object):
    def setupUi(self, SettingDialog):
        SettingDialog.setObjectName("SettingDialog")
        SettingDialog.resize(865, 715)
        SettingDialog.setModal(False)
        self.horizontalLayout = QtWidgets.QHBoxLayout(SettingDialog)
        self.horizontalLayout.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.scrollArea = QtWidgets.QScrollArea(SettingDialog)
        self.scrollArea.setStyleSheet("*{font-size:18px}")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.plugin_list = QtWidgets.QWidget()
        self.plugin_list.setGeometry(QtCore.QRect(0, 0, 242, 703))
        self.plugin_list.setStyleSheet("#plugin_list{background-color:rgb(255, 255, 255)}")
        self.plugin_list.setObjectName("plugin_list")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.plugin_list)
        self.verticalLayout.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea.setWidget(self.plugin_list)
        self.horizontalLayout.addWidget(self.scrollArea)
        self.scrollArea_2 = QtWidgets.QScrollArea(SettingDialog)
        self.scrollArea_2.setStyleSheet("")
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.content_wraper = QtWidgets.QWidget()
        self.content_wraper.setGeometry(QtCore.QRect(0, 0, 609, 703))
        self.content_wraper.setAutoFillBackground(False)
        self.content_wraper.setStyleSheet("#content_wraper{background-color:rgb(255, 255, 255)}")
        self.content_wraper.setObjectName("content_wraper")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.content_wraper)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.content = QtWidgets.QGroupBox(self.content_wraper)
        self.content.setStyleSheet("#content{font-size:23px}")
        self.content.setFlat(False)
        self.content.setObjectName("content")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.content)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_2.addWidget(self.content)
        self.scrollArea_2.setWidget(self.content_wraper)
        self.horizontalLayout.addWidget(self.scrollArea_2)
        self.horizontalLayout.setStretch(0, 2)
        self.horizontalLayout.setStretch(1, 5)

        self.retranslateUi(SettingDialog)
        QtCore.QMetaObject.connectSlotsByName(SettingDialog)

    def retranslateUi(self, SettingDialog):
        _translate = QtCore.QCoreApplication.translate
        SettingDialog.setWindowTitle(_translate("SettingDialog", "设置"))
        self.content.setTitle(_translate("SettingDialog", "None"))

