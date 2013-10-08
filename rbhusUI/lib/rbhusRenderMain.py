# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rbhusRenderMain.ui'
#
# Created: Mon Oct  7 14:53:15 2013
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
    MainWindow.resize(589, 112)
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
    self.pushList = QtGui.QPushButton(self.groupBox)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.pushList.sizePolicy().hasHeightForWidth())
    self.pushList.setSizePolicy(sizePolicy)
    font = QtGui.QFont()
    font.setBold(False)
    font.setWeight(50)
    self.pushList.setFont(font)
    self.pushList.setMouseTracking(False)
    self.pushList.setAutoFillBackground(False)
    self.pushList.setCheckable(False)
    self.pushList.setAutoDefault(False)
    self.pushList.setDefault(False)
    self.pushList.setFlat(False)
    self.pushList.setObjectName(_fromUtf8("pushList"))
    self.gridLayout_2.addWidget(self.pushList, 0, 0, 1, 1)
    self.pushHosts = QtGui.QPushButton(self.groupBox)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.pushHosts.sizePolicy().hasHeightForWidth())
    self.pushHosts.setSizePolicy(sizePolicy)
    self.pushHosts.setObjectName(_fromUtf8("pushHosts"))
    self.gridLayout_2.addWidget(self.pushHosts, 0, 2, 1, 1)
    self.pushSubmit = QtGui.QPushButton(self.groupBox)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.pushSubmit.sizePolicy().hasHeightForWidth())
    self.pushSubmit.setSizePolicy(sizePolicy)
    self.pushSubmit.setObjectName(_fromUtf8("pushSubmit"))
    self.gridLayout_2.addWidget(self.pushSubmit, 0, 1, 1, 1)
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
    MainWindow.setWindowTitle(_translate("MainWindow", "Rbhus Render Management", None))
    self.pushList.setText(_translate("MainWindow", "list", None))
    self.pushHosts.setText(_translate("MainWindow", "hosts", None))
    self.pushSubmit.setText(_translate("MainWindow", "submit", None))
    self.pushLogout.setText(_translate("MainWindow", "logout", None))

