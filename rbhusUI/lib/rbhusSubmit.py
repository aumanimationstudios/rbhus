# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'lib/rbhusSubmit.ui'
#
# Created: Tue Jun  5 12:24:46 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_rbhusSubmit(object):
    def setupUi(self, rbhusSubmit):
        rbhusSubmit.setObjectName(_fromUtf8("rbhusSubmit"))
        rbhusSubmit.resize(679, 93)
        self.centralwidget = QtGui.QWidget(rbhusSubmit)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pushFileName = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushFileName.sizePolicy().hasHeightForWidth())
        self.pushFileName.setSizePolicy(sizePolicy)
        self.pushFileName.setObjectName(_fromUtf8("pushFileName"))
        self.gridLayout.addWidget(self.pushFileName, 0, 2, 1, 1)
        self.labelFileName = QtGui.QLabel(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelFileName.sizePolicy().hasHeightForWidth())
        self.labelFileName.setSizePolicy(sizePolicy)
        self.labelFileName.setObjectName(_fromUtf8("labelFileName"))
        self.gridLayout.addWidget(self.labelFileName, 0, 0, 1, 1)
        self.lineEditFileName = QtGui.QLineEdit(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditFileName.sizePolicy().hasHeightForWidth())
        self.lineEditFileName.setSizePolicy(sizePolicy)
        self.lineEditFileName.setDragEnabled(True)
        self.lineEditFileName.setObjectName(_fromUtf8("lineEditFileName"))
        self.gridLayout.addWidget(self.lineEditFileName, 0, 1, 1, 1)
        self.labelFrange = QtGui.QLabel(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelFrange.sizePolicy().hasHeightForWidth())
        self.labelFrange.setSizePolicy(sizePolicy)
        self.labelFrange.setObjectName(_fromUtf8("labelFrange"))
        self.gridLayout.addWidget(self.labelFrange, 1, 0, 1, 1)
        self.lineEditFrange = QtGui.QLineEdit(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditFrange.sizePolicy().hasHeightForWidth())
        self.lineEditFrange.setSizePolicy(sizePolicy)
        self.lineEditFrange.setObjectName(_fromUtf8("lineEditFrange"))
        self.gridLayout.addWidget(self.lineEditFrange, 1, 1, 1, 1)
        rbhusSubmit.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(rbhusSubmit)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 679, 19))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        rbhusSubmit.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(rbhusSubmit)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        rbhusSubmit.setStatusBar(self.statusbar)

        self.retranslateUi(rbhusSubmit)
        QtCore.QMetaObject.connectSlotsByName(rbhusSubmit)

    def retranslateUi(self, rbhusSubmit):
        rbhusSubmit.setWindowTitle(QtGui.QApplication.translate("rbhusSubmit", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.pushFileName.setText(QtGui.QApplication.translate("rbhusSubmit", "open", None, QtGui.QApplication.UnicodeUTF8))
        self.labelFileName.setText(QtGui.QApplication.translate("rbhusSubmit", "fileName", None, QtGui.QApplication.UnicodeUTF8))
        self.labelFrange.setText(QtGui.QApplication.translate("rbhusSubmit", "fRange     ", None, QtGui.QApplication.UnicodeUTF8))

