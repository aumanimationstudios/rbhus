# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rbhusPipeMainMod.ui'
#
# Created: Thu Oct 17 23:14:37 2013
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
    MainWindow.resize(494, 118)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Maximum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
    MainWindow.setSizePolicy(sizePolicy)
    palette = QtGui.QPalette()
    brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
    brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
    brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
    brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
    brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
    brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
    MainWindow.setPalette(palette)
    MainWindow.setDocumentMode(False)
    MainWindow.setTabShape(QtGui.QTabWidget.Rounded)
    self.centralwidget = QtGui.QWidget(MainWindow)
    self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
    self.gridLayout = QtGui.QGridLayout(self.centralwidget)
    self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
    self.groupBox = QtGui.QGroupBox(self.centralwidget)
    self.groupBox.setTitle(_fromUtf8(""))
    self.groupBox.setObjectName(_fromUtf8("groupBox"))
    self.gridLayout_2 = QtGui.QGridLayout(self.groupBox)
    self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
    self.pushProd = QtGui.QPushButton(self.groupBox)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.pushProd.sizePolicy().hasHeightForWidth())
    self.pushProd.setSizePolicy(sizePolicy)
    self.pushProd.setObjectName(_fromUtf8("pushProd"))
    self.gridLayout_2.addWidget(self.pushProd, 0, 1, 1, 1)
    self.pushPre = QtGui.QPushButton(self.groupBox)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.pushPre.sizePolicy().hasHeightForWidth())
    self.pushPre.setSizePolicy(sizePolicy)
    font = QtGui.QFont()
    font.setBold(False)
    font.setWeight(50)
    self.pushPre.setFont(font)
    self.pushPre.setMouseTracking(False)
    self.pushPre.setAutoFillBackground(False)
    self.pushPre.setCheckable(False)
    self.pushPre.setAutoDefault(False)
    self.pushPre.setDefault(False)
    self.pushPre.setFlat(False)
    self.pushPre.setObjectName(_fromUtf8("pushPre"))
    self.gridLayout_2.addWidget(self.pushPre, 0, 0, 1, 1)
    self.pushPost = QtGui.QPushButton(self.groupBox)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.pushPost.sizePolicy().hasHeightForWidth())
    self.pushPost.setSizePolicy(sizePolicy)
    self.pushPost.setObjectName(_fromUtf8("pushPost"))
    self.gridLayout_2.addWidget(self.pushPost, 0, 2, 1, 1)
    self.pushAdmin = QtGui.QPushButton(self.groupBox)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.pushAdmin.sizePolicy().hasHeightForWidth())
    self.pushAdmin.setSizePolicy(sizePolicy)
    self.pushAdmin.setObjectName(_fromUtf8("pushAdmin"))
    self.gridLayout_2.addWidget(self.pushAdmin, 0, 3, 1, 1)
    self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 3)
    self.pushLogout = QtGui.QPushButton(self.centralwidget)
    self.pushLogout.setObjectName(_fromUtf8("pushLogout"))
    self.gridLayout.addWidget(self.pushLogout, 2, 1, 1, 1)
    spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
    self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
    spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
    self.gridLayout.addItem(spacerItem1, 2, 2, 1, 1)
    self.line = QtGui.QFrame(self.centralwidget)
    self.line.setEnabled(True)
    self.line.setFrameShadow(QtGui.QFrame.Sunken)
    self.line.setLineWidth(1)
    self.line.setMidLineWidth(3)
    self.line.setFrameShape(QtGui.QFrame.HLine)
    self.line.setFrameShadow(QtGui.QFrame.Sunken)
    self.line.setObjectName(_fromUtf8("line"))
    self.gridLayout.addWidget(self.line, 1, 0, 1, 3)
    MainWindow.setCentralWidget(self.centralwidget)

    self.retranslateUi(MainWindow)
    QtCore.QMetaObject.connectSlotsByName(MainWindow)

  def retranslateUi(self, MainWindow):
    MainWindow.setWindowTitle(_translate("MainWindow", "Rbhus Production Management", None))
    self.pushProd.setText(_translate("MainWindow", "PROD", None))
    self.pushPre.setText(_translate("MainWindow", "PRE", None))
    self.pushPost.setText(_translate("MainWindow", "POST", None))
    self.pushAdmin.setText(_translate("MainWindow", "ADMIN", None))
    self.pushLogout.setText(_translate("MainWindow", "logout", None))

