# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'lib/rbhusHostMod.ui'
#
# Created: Tue Aug  7 23:53:08 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1029, 360)
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
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
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
        self.horizontalLayout.addWidget(self.tableHost)
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
        self.horizontalLayout.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "rbhusHost", None, QtGui.QApplication.UnicodeUTF8))
        self.pushEdit.setText(QtGui.QApplication.translate("MainWindow", "edit", None, QtGui.QApplication.UnicodeUTF8))
        self.pushEnable.setText(QtGui.QApplication.translate("MainWindow", "enable", None, QtGui.QApplication.UnicodeUTF8))
        self.pushDisable.setText(QtGui.QApplication.translate("MainWindow", "disable", None, QtGui.QApplication.UnicodeUTF8))

