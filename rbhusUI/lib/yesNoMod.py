# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'yesNoMod.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_yesNo(object):
    def setupUi(self, yesNo):
        yesNo.setObjectName("yesNo")
        yesNo.resize(384, 107)
        self.gridLayout = QtWidgets.QGridLayout(yesNo)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton = QtWidgets.QPushButton(yesNo)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 2, 0, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(yesNo)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 2, 3, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 1, 1, 1)
        self.label = QtWidgets.QLabel(yesNo)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setScaledContents(False)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(False)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 1, 1, 1)

        self.retranslateUi(yesNo)
        QtCore.QMetaObject.connectSlotsByName(yesNo)

    def retranslateUi(self, yesNo):
        _translate = QtCore.QCoreApplication.translate
        yesNo.setWindowTitle(_translate("yesNo", "Yes/No"))
        self.pushButton.setText(_translate("yesNo", "yes"))
        self.pushButton_2.setText(_translate("yesNo", "no"))
        self.label.setText(_translate("yesNo", "wtf"))
