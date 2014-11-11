# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'selectCheckBoxComboMod.ui'
#
# Created: Tue Nov 11 11:31:44 2014
#      by: PyQt4 UI code generator 4.10.4
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

class Ui_selectCheckBox(object):
  def setupUi(self, selectCheckBox):
    selectCheckBox.setObjectName(_fromUtf8("selectCheckBox"))
    selectCheckBox.resize(232, 449)
    self.centralwidget = QtGui.QWidget(selectCheckBox)
    self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
    self.gridLayout = QtGui.QGridLayout(self.centralwidget)
    self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
    self.label = QtGui.QLabel(self.centralwidget)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Maximum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
    self.label.setSizePolicy(sizePolicy)
    self.label.setObjectName(_fromUtf8("label"))
    self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
    self.lineEditSearch = QtGui.QLineEdit(self.centralwidget)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.lineEditSearch.sizePolicy().hasHeightForWidth())
    self.lineEditSearch.setSizePolicy(sizePolicy)
    self.lineEditSearch.setObjectName(_fromUtf8("lineEditSearch"))
    self.gridLayout.addWidget(self.lineEditSearch, 0, 1, 1, 2)
    self.pushClearSearch = QtGui.QPushButton(self.centralwidget)
    self.pushClearSearch.setObjectName(_fromUtf8("pushClearSearch"))
    self.gridLayout.addWidget(self.pushClearSearch, 0, 3, 1, 1)
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
    self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 204, 224))
    self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
    self.verticalLayout = QtGui.QVBoxLayout(self.scrollAreaWidgetContents)
    self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
    self.scrollArea.setWidget(self.scrollAreaWidgetContents)
    self.verticalLayout_2.addWidget(self.scrollArea)
    self.gridLayout.addWidget(self.frame, 2, 0, 3, 4)
    self.verticalLayout_3 = QtGui.QVBoxLayout()
    self.verticalLayout_3.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
    self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
    self.horizontalLayout_2 = QtGui.QHBoxLayout()
    self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
    spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Minimum)
    self.horizontalLayout_2.addItem(spacerItem)
    self.pushApply = QtGui.QPushButton(self.centralwidget)
    self.pushApply.setObjectName(_fromUtf8("pushApply"))
    self.horizontalLayout_2.addWidget(self.pushApply)
    self.verticalLayout_3.addLayout(self.horizontalLayout_2)
    self.plainTextEditSelected = QtGui.QPlainTextEdit(self.centralwidget)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.plainTextEditSelected.sizePolicy().hasHeightForWidth())
    self.plainTextEditSelected.setSizePolicy(sizePolicy)
    self.plainTextEditSelected.setMaximumSize(QtCore.QSize(16777215, 50))
    self.plainTextEditSelected.setReadOnly(True)
    self.plainTextEditSelected.setObjectName(_fromUtf8("plainTextEditSelected"))
    self.verticalLayout_3.addWidget(self.plainTextEditSelected)
    self.gridLayout.addLayout(self.verticalLayout_3, 6, 0, 1, 4)
    self.horizontalLayout = QtGui.QHBoxLayout()
    self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
    self.pushDeselect = QtGui.QPushButton(self.centralwidget)
    self.pushDeselect.setObjectName(_fromUtf8("pushDeselect"))
    self.horizontalLayout.addWidget(self.pushDeselect)
    spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
    self.horizontalLayout.addItem(spacerItem1)
    self.pushSelect = QtGui.QPushButton(self.centralwidget)
    self.pushSelect.setObjectName(_fromUtf8("pushSelect"))
    self.horizontalLayout.addWidget(self.pushSelect)
    self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 4)
    selectCheckBox.setCentralWidget(self.centralwidget)

    self.retranslateUi(selectCheckBox)
    QtCore.QMetaObject.connectSlotsByName(selectCheckBox)

  def retranslateUi(self, selectCheckBox):
    selectCheckBox.setWindowTitle(_translate("selectCheckBox", "MainWindow", None))
    self.label.setText(_translate("selectCheckBox", "search", None))
    self.pushClearSearch.setText(_translate("selectCheckBox", "clear", None))
    self.pushApply.setText(_translate("selectCheckBox", "apply", None))
    self.plainTextEditSelected.setPlainText(_translate("selectCheckBox", "rwst", None))
    self.pushDeselect.setText(_translate("selectCheckBox", "deselect all", None))
    self.pushSelect.setText(_translate("selectCheckBox", "select all", None))

