# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rbhusPipeProjCreateMod.ui'
#
# Created: Thu Oct 17 23:15:13 2013
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
    MainWindow.resize(308, 207)
    self.centralwidget = QtGui.QWidget(MainWindow)
    self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
    self.gridLayout = QtGui.QGridLayout(self.centralwidget)
    self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
    self.labelDue = QtGui.QLabel(self.centralwidget)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.labelDue.sizePolicy().hasHeightForWidth())
    self.labelDue.setSizePolicy(sizePolicy)
    self.labelDue.setObjectName(_fromUtf8("labelDue"))
    self.gridLayout.addWidget(self.labelDue, 5, 0, 1, 1)
    self.labelName = QtGui.QLabel(self.centralwidget)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.labelName.sizePolicy().hasHeightForWidth())
    self.labelName.setSizePolicy(sizePolicy)
    self.labelName.setObjectName(_fromUtf8("labelName"))
    self.gridLayout.addWidget(self.labelName, 0, 0, 1, 1)
    self.lineEdit = QtGui.QLineEdit(self.centralwidget)
    self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
    self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)
    self.labelLibrary = QtGui.QLabel(self.centralwidget)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.labelLibrary.sizePolicy().hasHeightForWidth())
    self.labelLibrary.setSizePolicy(sizePolicy)
    self.labelLibrary.setObjectName(_fromUtf8("labelLibrary"))
    self.gridLayout.addWidget(self.labelLibrary, 2, 0, 1, 1)
    self.labelProj = QtGui.QLabel(self.centralwidget)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.labelProj.sizePolicy().hasHeightForWidth())
    self.labelProj.setSizePolicy(sizePolicy)
    self.labelProj.setObjectName(_fromUtf8("labelProj"))
    self.gridLayout.addWidget(self.labelProj, 1, 0, 1, 1)
    self.labelProjdump = QtGui.QLabel(self.centralwidget)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.labelProjdump.sizePolicy().hasHeightForWidth())
    self.labelProjdump.setSizePolicy(sizePolicy)
    self.labelProjdump.setObjectName(_fromUtf8("labelProjdump"))
    self.gridLayout.addWidget(self.labelProjdump, 3, 0, 1, 1)
    self.comboLibrary = QtGui.QComboBox(self.centralwidget)
    self.comboLibrary.setObjectName(_fromUtf8("comboLibrary"))
    self.gridLayout.addWidget(self.comboLibrary, 2, 1, 1, 1)
    self.comboProj = QtGui.QComboBox(self.centralwidget)
    self.comboProj.setObjectName(_fromUtf8("comboProj"))
    self.gridLayout.addWidget(self.comboProj, 1, 1, 1, 1)
    self.comboProjdump = QtGui.QComboBox(self.centralwidget)
    self.comboProjdump.setObjectName(_fromUtf8("comboProjdump"))
    self.gridLayout.addWidget(self.comboProjdump, 3, 1, 1, 1)
    self.line = QtGui.QFrame(self.centralwidget)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
    self.line.setSizePolicy(sizePolicy)
    self.line.setFrameShape(QtGui.QFrame.HLine)
    self.line.setFrameShadow(QtGui.QFrame.Sunken)
    self.line.setObjectName(_fromUtf8("line"))
    self.gridLayout.addWidget(self.line, 7, 0, 1, 2)
    spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
    self.gridLayout.addItem(spacerItem, 6, 0, 1, 2)
    self.dateEditDue = QtGui.QDateEdit(self.centralwidget)
    self.dateEditDue.setCalendarPopup(True)
    self.dateEditDue.setObjectName(_fromUtf8("dateEditDue"))
    self.gridLayout.addWidget(self.dateEditDue, 5, 1, 1, 1)
    self.pushCreate = QtGui.QPushButton(self.centralwidget)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.pushCreate.sizePolicy().hasHeightForWidth())
    self.pushCreate.setSizePolicy(sizePolicy)
    self.pushCreate.setObjectName(_fromUtf8("pushCreate"))
    self.gridLayout.addWidget(self.pushCreate, 10, 0, 1, 2)
    self.checkBox = QtGui.QCheckBox(self.centralwidget)
    self.checkBox.setChecked(True)
    self.checkBox.setObjectName(_fromUtf8("checkBox"))
    self.gridLayout.addWidget(self.checkBox, 9, 0, 1, 3)
    MainWindow.setCentralWidget(self.centralwidget)

    self.retranslateUi(MainWindow)
    QtCore.QMetaObject.connectSlotsByName(MainWindow)

  def retranslateUi(self, MainWindow):
    MainWindow.setWindowTitle(_translate("MainWindow", "Rbhus Pipe NEW PROJECT", None))
    self.labelDue.setText(_translate("MainWindow", "due date", None))
    self.labelName.setText(_translate("MainWindow", "name", None))
    self.labelLibrary.setText(_translate("MainWindow", "libraryDisk", None))
    self.labelProj.setText(_translate("MainWindow", "projDisk", None))
    self.labelProjdump.setText(_translate("MainWindow", "projdumpDisk", None))
    self.pushCreate.setText(_translate("MainWindow", "create", None))
    self.checkBox.setText(_translate("MainWindow", "rbhusRender intergration", None))

