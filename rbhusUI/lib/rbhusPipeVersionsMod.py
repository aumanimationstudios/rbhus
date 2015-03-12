# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rbhusPipeVersionsMod.ui'
#
# Created: Wed Mar 11 21:26:30 2015
#      by: PyQt4 UI code generator 4.11.3
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
    MainWindow.resize(466, 425)
    self.centralwidget = QtGui.QWidget(MainWindow)
    self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
    self.gridLayout = QtGui.QGridLayout(self.centralwidget)
    self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
    self.gridLayout_2 = QtGui.QGridLayout()
    self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
    self.gridLayout.addLayout(self.gridLayout_2, 0, 0, 1, 3)
    self.verticalLayout = QtGui.QVBoxLayout()
    self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
    self.groupVersions = QtGui.QGroupBox(self.centralwidget)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.MinimumExpanding)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.groupVersions.sizePolicy().hasHeightForWidth())
    self.groupVersions.setSizePolicy(sizePolicy)
    self.groupVersions.setObjectName(_fromUtf8("groupVersions"))
    self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupVersions)
    self.verticalLayout_2.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
    self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
    self.tableVersions = QtGui.QTableWidget(self.groupVersions)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.tableVersions.sizePolicy().hasHeightForWidth())
    self.tableVersions.setSizePolicy(sizePolicy)
    self.tableVersions.setMouseTracking(True)
    self.tableVersions.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
    self.tableVersions.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
    self.tableVersions.setObjectName(_fromUtf8("tableVersions"))
    self.tableVersions.setColumnCount(2)
    self.tableVersions.setRowCount(2)
    item = QtGui.QTableWidgetItem()
    self.tableVersions.setVerticalHeaderItem(0, item)
    item = QtGui.QTableWidgetItem()
    self.tableVersions.setVerticalHeaderItem(1, item)
    item = QtGui.QTableWidgetItem()
    self.tableVersions.setHorizontalHeaderItem(0, item)
    item = QtGui.QTableWidgetItem()
    self.tableVersions.setHorizontalHeaderItem(1, item)
    self.tableVersions.horizontalHeader().setVisible(False)
    self.tableVersions.verticalHeader().setVisible(False)
    self.verticalLayout_2.addWidget(self.tableVersions)
    self.verticalLayout.addWidget(self.groupVersions)
    self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 3)
    self.pushCommit = QtGui.QPushButton(self.centralwidget)
    self.pushCommit.setObjectName(_fromUtf8("pushCommit"))
    self.gridLayout.addWidget(self.pushCommit, 4, 2, 1, 1)
    self.pushWork = QtGui.QPushButton(self.centralwidget)
    self.pushWork.setObjectName(_fromUtf8("pushWork"))
    self.gridLayout.addWidget(self.pushWork, 4, 0, 1, 1)
    MainWindow.setCentralWidget(self.centralwidget)
    self.statusbar = QtGui.QStatusBar(MainWindow)
    self.statusbar.setObjectName(_fromUtf8("statusbar"))
    MainWindow.setStatusBar(self.statusbar)

    self.retranslateUi(MainWindow)
    QtCore.QMetaObject.connectSlotsByName(MainWindow)

  def retranslateUi(self, MainWindow):
    MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
    self.groupVersions.setTitle(_translate("MainWindow", "versions", None))
    self.tableVersions.setSortingEnabled(True)
    item = self.tableVersions.verticalHeaderItem(0)
    item.setText(_translate("MainWindow", "tete", None))
    item = self.tableVersions.verticalHeaderItem(1)
    item.setText(_translate("MainWindow", "eteeee", None))
    item = self.tableVersions.horizontalHeaderItem(0)
    item.setText(_translate("MainWindow", "teset", None))
    item = self.tableVersions.horizontalHeaderItem(1)
    item.setText(_translate("MainWindow", "eee", None))
    self.pushCommit.setText(_translate("MainWindow", "commit", None))
    self.pushWork.setText(_translate("MainWindow", "open", None))

