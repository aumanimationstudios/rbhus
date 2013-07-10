# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rbhusEditTaskHostGroupsMod.ui'
#
# Created: Wed Jul 10 00:18:09 2013
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

class Ui_rbhusTaskHostGroups(object):
  def setupUi(self, rbhusTaskHostGroups):
    rbhusTaskHostGroups.setObjectName(_fromUtf8("rbhusTaskHostGroups"))
    rbhusTaskHostGroups.resize(648, 411)
    self.centralwidget = QtGui.QWidget(rbhusTaskHostGroups)
    self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
    self.gridLayout = QtGui.QGridLayout(self.centralwidget)
    self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
    self.lineEdit = QtGui.QLineEdit(self.centralwidget)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
    self.lineEdit.setSizePolicy(sizePolicy)
    self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
    self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 4)
    self.horizontalLayout_2 = QtGui.QHBoxLayout()
    self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
    spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
    self.horizontalLayout_2.addItem(spacerItem)
    self.pushButton = QtGui.QPushButton(self.centralwidget)
    self.pushButton.setObjectName(_fromUtf8("pushButton"))
    self.horizontalLayout_2.addWidget(self.pushButton)
    self.gridLayout.addLayout(self.horizontalLayout_2, 3, 0, 1, 5)
    self.horizontalLayout = QtGui.QHBoxLayout()
    self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
    self.pushDeselect = QtGui.QPushButton(self.centralwidget)
    self.pushDeselect.setObjectName(_fromUtf8("pushDeselect"))
    self.horizontalLayout.addWidget(self.pushDeselect)
    spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
    self.horizontalLayout.addItem(spacerItem1)
    self.pushClearSearch = QtGui.QPushButton(self.centralwidget)
    self.pushClearSearch.setObjectName(_fromUtf8("pushClearSearch"))
    self.horizontalLayout.addWidget(self.pushClearSearch)
    self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 5)
    self.label = QtGui.QLabel(self.centralwidget)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Maximum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
    self.label.setSizePolicy(sizePolicy)
    self.label.setObjectName(_fromUtf8("label"))
    self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
    self.frame = QtGui.QFrame(self.centralwidget)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
    self.frame.setSizePolicy(sizePolicy)
    self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
    self.frame.setFrameShadow(QtGui.QFrame.Raised)
    self.frame.setObjectName(_fromUtf8("frame"))
    self.verticalLayout_2 = QtGui.QVBoxLayout(self.frame)
    self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
    self.scrollArea = QtGui.QScrollArea(self.frame)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
    self.scrollArea.setSizePolicy(sizePolicy)
    self.scrollArea.setWidgetResizable(True)
    self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
    self.scrollAreaWidgetContents = QtGui.QWidget()
    self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 620, 269))
    self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
    self.verticalLayout = QtGui.QVBoxLayout(self.scrollAreaWidgetContents)
    self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
    self.scrollArea.setWidget(self.scrollAreaWidgetContents)
    self.verticalLayout_2.addWidget(self.scrollArea)
    self.gridLayout.addWidget(self.frame, 2, 0, 1, 5)
    self.lineEdit_2 = QtGui.QLineEdit(self.centralwidget)
    self.lineEdit_2.setEnabled(True)
    self.lineEdit_2.setReadOnly(True)
    self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
    self.gridLayout.addWidget(self.lineEdit_2, 4, 0, 1, 5)
    rbhusTaskHostGroups.setCentralWidget(self.centralwidget)

    self.retranslateUi(rbhusTaskHostGroups)
    QtCore.QMetaObject.connectSlotsByName(rbhusTaskHostGroups)

  def retranslateUi(self, rbhusTaskHostGroups):
    rbhusTaskHostGroups.setWindowTitle(_translate("rbhusTaskHostGroups", "MainWindow", None))
    self.pushButton.setText(_translate("rbhusTaskHostGroups", "apply", None))
    self.pushDeselect.setText(_translate("rbhusTaskHostGroups", "deselect all", None))
    self.pushClearSearch.setText(_translate("rbhusTaskHostGroups", "clear search", None))
    self.label.setText(_translate("rbhusTaskHostGroups", "search", None))
    self.lineEdit_2.setText(_translate("rbhusTaskHostGroups", "dfdf", None))

