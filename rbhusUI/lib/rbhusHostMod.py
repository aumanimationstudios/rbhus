# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rbhusHostMod.ui'
#
# Created: Thu Jan 10 22:29:11 2013
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

class Ui_MainWindow(object):
  def setupUi(self, MainWindow):
    MainWindow.setObjectName(_fromUtf8("MainWindow"))
    MainWindow.resize(1053, 355)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
    MainWindow.setSizePolicy(sizePolicy)
    self.centralwidget = QtGui.QWidget(MainWindow)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
    self.centralwidget.setSizePolicy(sizePolicy)
    self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
    self.gridLayout = QtGui.QGridLayout(self.centralwidget)
    self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
    self.tableHost = QtGui.QTableWidget(self.centralwidget)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Expanding)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.tableHost.sizePolicy().hasHeightForWidth())
    self.tableHost.setSizePolicy(sizePolicy)
    self.tableHost.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
    self.tableHost.setObjectName(_fromUtf8("tableHost"))
    self.tableHost.setColumnCount(0)
    self.tableHost.setRowCount(0)
    self.tableHost.horizontalHeader().setCascadingSectionResizes(True)
    self.tableHost.horizontalHeader().setStretchLastSection(True)
    self.tableHost.verticalHeader().setStretchLastSection(False)
    self.gridLayout.addWidget(self.tableHost, 2, 0, 1, 1)
    self.verticalLayout = QtGui.QVBoxLayout()
    self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
    self.pushEdit = QtGui.QPushButton(self.centralwidget)
    self.pushEdit.setObjectName(_fromUtf8("pushEdit"))
    self.verticalLayout.addWidget(self.pushEdit)
    self.pushEnable = QtGui.QPushButton(self.centralwidget)
    self.pushEnable.setObjectName(_fromUtf8("pushEnable"))
    self.verticalLayout.addWidget(self.pushEnable)
    self.pushDisable = QtGui.QPushButton(self.centralwidget)
    self.pushDisable.setObjectName(_fromUtf8("pushDisable"))
    self.verticalLayout.addWidget(self.pushDisable)
    spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
    self.verticalLayout.addItem(spacerItem)
    self.gridLayout.addLayout(self.verticalLayout, 2, 1, 1, 1)
    self.horizontalLayout_2 = QtGui.QHBoxLayout()
    self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
    spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
    self.horizontalLayout_2.addItem(spacerItem1)
    self.pushRefresh = QtGui.QPushButton(self.centralwidget)
    self.pushRefresh.setObjectName(_fromUtf8("pushRefresh"))
    self.horizontalLayout_2.addWidget(self.pushRefresh)
    self.gridLayout.addLayout(self.horizontalLayout_2, 3, 0, 1, 2)
    MainWindow.setCentralWidget(self.centralwidget)

    self.retranslateUi(MainWindow)
    QtCore.QMetaObject.connectSlotsByName(MainWindow)

  def retranslateUi(self, MainWindow):
    MainWindow.setWindowTitle(_translate("MainWindow", "rbhusHost", None))
    self.tableHost.setSortingEnabled(True)
    self.pushEdit.setText(_translate("MainWindow", "edit", None))
    self.pushEnable.setText(_translate("MainWindow", "enable", None))
    self.pushDisable.setText(_translate("MainWindow", "disable", None))
    self.pushRefresh.setText(_translate("MainWindow", "refresh", None))

