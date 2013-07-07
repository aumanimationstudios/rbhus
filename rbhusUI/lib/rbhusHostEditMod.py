# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rbhusHostEditMod.ui'
#
# Created: Sat Jul  6 22:46:25 2013
#      by: PyQt4 UI code generator 4.10.1
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

class Ui_rbhusHostEdit(object):
  def setupUi(self, rbhusHostEdit):
    rbhusHostEdit.setObjectName(_fromUtf8("rbhusHostEdit"))
    rbhusHostEdit.resize(503, 97)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(rbhusHostEdit.sizePolicy().hasHeightForWidth())
    rbhusHostEdit.setSizePolicy(sizePolicy)
    self.centralwidget = QtGui.QWidget(rbhusHostEdit)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
    self.centralwidget.setSizePolicy(sizePolicy)
    self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
    self.gridLayout = QtGui.QGridLayout(self.centralwidget)
    self.gridLayout.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
    self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
    self.labelImageName = QtGui.QLabel(self.centralwidget)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.labelImageName.sizePolicy().hasHeightForWidth())
    self.labelImageName.setSizePolicy(sizePolicy)
    self.labelImageName.setObjectName(_fromUtf8("labelImageName"))
    self.gridLayout.addWidget(self.labelImageName, 0, 0, 1, 1)
    self.horizontalLayout = QtGui.QHBoxLayout()
    self.horizontalLayout.setContentsMargins(-1, 10, -1, -1)
    self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
    spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
    self.horizontalLayout.addItem(spacerItem)
    self.pushApply = QtGui.QPushButton(self.centralwidget)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.pushApply.sizePolicy().hasHeightForWidth())
    self.pushApply.setSizePolicy(sizePolicy)
    self.pushApply.setObjectName(_fromUtf8("pushApply"))
    self.horizontalLayout.addWidget(self.pushApply)
    self.gridLayout.addLayout(self.horizontalLayout, 2, 1, 1, 2)
    self.spinBox = QtGui.QSpinBox(self.centralwidget)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.spinBox.sizePolicy().hasHeightForWidth())
    self.spinBox.setSizePolicy(sizePolicy)
    self.spinBox.setObjectName(_fromUtf8("spinBox"))
    self.gridLayout.addWidget(self.spinBox, 0, 1, 1, 1)
    self.label = QtGui.QLabel(self.centralwidget)
    self.label.setObjectName(_fromUtf8("label"))
    self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
    self.lineEdit = QtGui.QLineEdit(self.centralwidget)
    self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
    self.gridLayout.addWidget(self.lineEdit, 1, 1, 1, 1)
    rbhusHostEdit.setCentralWidget(self.centralwidget)

    self.retranslateUi(rbhusHostEdit)
    QtCore.QMetaObject.connectSlotsByName(rbhusHostEdit)

  def retranslateUi(self, rbhusHostEdit):
    rbhusHostEdit.setWindowTitle(_translate("rbhusHostEdit", "rbhusHostEdit", None))
    self.labelImageName.setText(_translate("rbhusHostEdit", "eCpus", None))
    self.pushApply.setText(_translate("rbhusHostEdit", "apply", None))
    self.label.setText(_translate("rbhusHostEdit", "groups", None))

