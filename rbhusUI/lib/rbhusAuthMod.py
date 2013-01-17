# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rbhusAuthMod.ui'
#
# Created: Tue Jan 15 22:49:35 2013
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
  _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
  def _fromUtf8(s):
    return s

try:
  _encoding = QtGui.QApplication.UnicodeUTF8
  def _translate(context, text, disambig):
    return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
  def _translate(context, text, disambig):
    return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindowAuth(object):
  def setupUi(self, MainWindowAuth):
    MainWindowAuth.setObjectName(_fromUtf8("MainWindowAuth"))
    MainWindowAuth.resize(498, 116)
    self.centralwidget = QtGui.QWidget(MainWindowAuth)
    self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
    self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
    self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
    self.gridLayout = QtGui.QGridLayout()
    self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
    self.label = QtGui.QLabel(self.centralwidget)
    self.label.setObjectName(_fromUtf8("label"))
    self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
    self.lineEdit = QtGui.QLineEdit(self.centralwidget)
    self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
    self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)
    self.label_2 = QtGui.QLabel(self.centralwidget)
    self.label_2.setObjectName(_fromUtf8("label_2"))
    self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
    self.lineEdit_2 = QtGui.QLineEdit(self.centralwidget)
    self.lineEdit_2.setEchoMode(QtGui.QLineEdit.Password)
    self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
    self.gridLayout.addWidget(self.lineEdit_2, 1, 1, 1, 1)
    self.verticalLayout.addLayout(self.gridLayout)
    spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
    self.verticalLayout.addItem(spacerItem)
    self.horizontalLayout_3 = QtGui.QHBoxLayout()
    self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
    spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
    self.horizontalLayout_3.addItem(spacerItem1)
    self.pushButton = QtGui.QPushButton(self.centralwidget)
    self.pushButton.setObjectName(_fromUtf8("pushButton"))
    self.horizontalLayout_3.addWidget(self.pushButton)
    self.verticalLayout.addLayout(self.horizontalLayout_3)
    MainWindowAuth.setCentralWidget(self.centralwidget)

    self.retranslateUi(MainWindowAuth)
    QtCore.QMetaObject.connectSlotsByName(MainWindowAuth)

  def retranslateUi(self, MainWindowAuth):
    MainWindowAuth.setWindowTitle(_translate("MainWindowAuth", "MainWindow", None))
    self.label.setText(_translate("MainWindowAuth", "username", None))
    self.label_2.setText(_translate("MainWindowAuth", "password", None))
    self.pushButton.setText(_translate("MainWindowAuth", "try ur luck!", None))

