# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rbhusPipeAssetCreateMod.ui'
#
# Created: Sat Nov  1 20:34:40 2014
#      by: PyQt4 UI code generator 4.11.2
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
    MainWindow.setEnabled(True)
    MainWindow.resize(397, 423)
    self.centralwidget = QtGui.QWidget(MainWindow)
    self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
    self.gridLayout = QtGui.QGridLayout(self.centralwidget)
    self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
    self.labelFRange = QtGui.QLabel(self.centralwidget)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.labelFRange.sizePolicy().hasHeightForWidth())
    self.labelFRange.setSizePolicy(sizePolicy)
    self.labelFRange.setObjectName(_fromUtf8("labelFRange"))
    self.gridLayout.addWidget(self.labelFRange, 10, 0, 1, 1)
    self.comboScene = QtGui.QComboBox(self.centralwidget)
    self.comboScene.setObjectName(_fromUtf8("comboScene"))
    self.gridLayout.addWidget(self.comboScene, 6, 1, 1, 4)
    self.labelStageType = QtGui.QLabel(self.centralwidget)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.labelStageType.sizePolicy().hasHeightForWidth())
    self.labelStageType.setSizePolicy(sizePolicy)
    self.labelStageType.setObjectName(_fromUtf8("labelStageType"))
    self.gridLayout.addWidget(self.labelStageType, 8, 0, 1, 1)
    self.comboAssType = QtGui.QComboBox(self.centralwidget)
    self.comboAssType.setObjectName(_fromUtf8("comboAssType"))
    self.gridLayout.addWidget(self.comboAssType, 3, 1, 1, 4)
    self.pushCreate = QtGui.QPushButton(self.centralwidget)
    self.pushCreate.setObjectName(_fromUtf8("pushCreate"))
    self.gridLayout.addWidget(self.pushCreate, 17, 0, 1, 5)
    self.labelNodeType = QtGui.QLabel(self.centralwidget)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.labelNodeType.sizePolicy().hasHeightForWidth())
    self.labelNodeType.setSizePolicy(sizePolicy)
    self.labelNodeType.setObjectName(_fromUtf8("labelNodeType"))
    self.gridLayout.addWidget(self.labelNodeType, 9, 0, 1, 1)
    self.comboSequence = QtGui.QComboBox(self.centralwidget)
    self.comboSequence.setObjectName(_fromUtf8("comboSequence"))
    self.gridLayout.addWidget(self.comboSequence, 5, 1, 1, 4)
    self.labelScene = QtGui.QLabel(self.centralwidget)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.labelScene.sizePolicy().hasHeightForWidth())
    self.labelScene.setSizePolicy(sizePolicy)
    self.labelScene.setObjectName(_fromUtf8("labelScene"))
    self.gridLayout.addWidget(self.labelScene, 6, 0, 1, 1)
    self.lineEditWorkers = QtGui.QLineEdit(self.centralwidget)
    self.lineEditWorkers.setEnabled(False)
    self.lineEditWorkers.setObjectName(_fromUtf8("lineEditWorkers"))
    self.gridLayout.addWidget(self.lineEditWorkers, 12, 1, 1, 1)
    self.labelFileType = QtGui.QLabel(self.centralwidget)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.labelFileType.sizePolicy().hasHeightForWidth())
    self.labelFileType.setSizePolicy(sizePolicy)
    self.labelFileType.setObjectName(_fromUtf8("labelFileType"))
    self.gridLayout.addWidget(self.labelFileType, 4, 0, 1, 1)
    self.comboFileType = QtGui.QComboBox(self.centralwidget)
    self.comboFileType.setObjectName(_fromUtf8("comboFileType"))
    self.gridLayout.addWidget(self.comboFileType, 4, 1, 1, 4)
    self.labelSequence = QtGui.QLabel(self.centralwidget)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.labelSequence.sizePolicy().hasHeightForWidth())
    self.labelSequence.setSizePolicy(sizePolicy)
    self.labelSequence.setObjectName(_fromUtf8("labelSequence"))
    self.gridLayout.addWidget(self.labelSequence, 5, 0, 1, 1)
    self.lineEditDesc = QtGui.QLineEdit(self.centralwidget)
    self.lineEditDesc.setText(_fromUtf8(""))
    self.lineEditDesc.setObjectName(_fromUtf8("lineEditDesc"))
    self.gridLayout.addWidget(self.lineEditDesc, 13, 1, 1, 4)
    self.labelDue = QtGui.QLabel(self.centralwidget)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.labelDue.sizePolicy().hasHeightForWidth())
    self.labelDue.setSizePolicy(sizePolicy)
    self.labelDue.setObjectName(_fromUtf8("labelDue"))
    self.gridLayout.addWidget(self.labelDue, 11, 0, 1, 1)
    self.comboStageType = QtGui.QComboBox(self.centralwidget)
    self.comboStageType.setObjectName(_fromUtf8("comboStageType"))
    self.gridLayout.addWidget(self.comboStageType, 8, 1, 1, 4)
    self.labelAdmin = QtGui.QLabel(self.centralwidget)
    self.labelAdmin.setObjectName(_fromUtf8("labelAdmin"))
    self.gridLayout.addWidget(self.labelAdmin, 12, 0, 1, 1)
    self.dateEditDue = QtGui.QDateTimeEdit(self.centralwidget)
    self.dateEditDue.setCalendarPopup(True)
    self.dateEditDue.setObjectName(_fromUtf8("dateEditDue"))
    self.gridLayout.addWidget(self.dateEditDue, 11, 1, 1, 4)
    self.labelAssType = QtGui.QLabel(self.centralwidget)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.labelAssType.sizePolicy().hasHeightForWidth())
    self.labelAssType.setSizePolicy(sizePolicy)
    self.labelAssType.setObjectName(_fromUtf8("labelAssType"))
    self.gridLayout.addWidget(self.labelAssType, 3, 0, 1, 1)
    self.line = QtGui.QFrame(self.centralwidget)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
    self.line.setSizePolicy(sizePolicy)
    self.line.setFrameShape(QtGui.QFrame.HLine)
    self.line.setFrameShadow(QtGui.QFrame.Sunken)
    self.line.setObjectName(_fromUtf8("line"))
    self.gridLayout.addWidget(self.line, 16, 0, 1, 5)
    spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
    self.gridLayout.addItem(spacerItem, 15, 0, 1, 5)
    self.labelAssName = QtGui.QLabel(self.centralwidget)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.labelAssName.sizePolicy().hasHeightForWidth())
    self.labelAssName.setSizePolicy(sizePolicy)
    self.labelAssName.setObjectName(_fromUtf8("labelAssName"))
    self.gridLayout.addWidget(self.labelAssName, 0, 0, 1, 1)
    self.labelDesc = QtGui.QLabel(self.centralwidget)
    self.labelDesc.setObjectName(_fromUtf8("labelDesc"))
    self.gridLayout.addWidget(self.labelDesc, 13, 0, 1, 1)
    self.labelDirectory = QtGui.QLabel(self.centralwidget)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.labelDirectory.sizePolicy().hasHeightForWidth())
    self.labelDirectory.setSizePolicy(sizePolicy)
    self.labelDirectory.setObjectName(_fromUtf8("labelDirectory"))
    self.gridLayout.addWidget(self.labelDirectory, 2, 0, 1, 1)
    self.comboDirectory = QtGui.QComboBox(self.centralwidget)
    self.comboDirectory.setObjectName(_fromUtf8("comboDirectory"))
    self.gridLayout.addWidget(self.comboDirectory, 2, 1, 1, 4)
    self.labelTags = QtGui.QLabel(self.centralwidget)
    self.labelTags.setObjectName(_fromUtf8("labelTags"))
    self.gridLayout.addWidget(self.labelTags, 14, 0, 1, 1)
    self.pushTags = QtGui.QPushButton(self.centralwidget)
    self.pushTags.setObjectName(_fromUtf8("pushTags"))
    self.gridLayout.addWidget(self.pushTags, 14, 4, 1, 1)
    self.checkAssign = QtGui.QCheckBox(self.centralwidget)
    self.checkAssign.setChecked(True)
    self.checkAssign.setObjectName(_fromUtf8("checkAssign"))
    self.gridLayout.addWidget(self.checkAssign, 12, 2, 1, 1)
    self.pushUsers = QtGui.QPushButton(self.centralwidget)
    self.pushUsers.setEnabled(False)
    self.pushUsers.setObjectName(_fromUtf8("pushUsers"))
    self.gridLayout.addWidget(self.pushUsers, 12, 4, 1, 1)
    self.lineEditTags = QtGui.QLineEdit(self.centralwidget)
    self.lineEditTags.setObjectName(_fromUtf8("lineEditTags"))
    self.gridLayout.addWidget(self.lineEditTags, 14, 1, 1, 2)
    self.lineEditAssName = QtGui.QLineEdit(self.centralwidget)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.lineEditAssName.sizePolicy().hasHeightForWidth())
    self.lineEditAssName.setSizePolicy(sizePolicy)
    self.lineEditAssName.setObjectName(_fromUtf8("lineEditAssName"))
    self.gridLayout.addWidget(self.lineEditAssName, 0, 1, 1, 3)
    self.checkAssName = QtGui.QCheckBox(self.centralwidget)
    self.checkAssName.setEnabled(True)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.checkAssName.sizePolicy().hasHeightForWidth())
    self.checkAssName.setSizePolicy(sizePolicy)
    self.checkAssName.setText(_fromUtf8(""))
    self.checkAssName.setChecked(False)
    self.checkAssName.setObjectName(_fromUtf8("checkAssName"))
    self.gridLayout.addWidget(self.checkAssName, 0, 4, 1, 1)
    self.lineEditFRange = QtGui.QLineEdit(self.centralwidget)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.lineEditFRange.sizePolicy().hasHeightForWidth())
    self.lineEditFRange.setSizePolicy(sizePolicy)
    self.lineEditFRange.setObjectName(_fromUtf8("lineEditFRange"))
    self.gridLayout.addWidget(self.lineEditFRange, 10, 1, 1, 4)
    self.pushNodes = QtGui.QPushButton(self.centralwidget)
    self.pushNodes.setObjectName(_fromUtf8("pushNodes"))
    self.gridLayout.addWidget(self.pushNodes, 9, 4, 1, 1)
    self.lineEditNodes = QtGui.QLineEdit(self.centralwidget)
    self.lineEditNodes.setObjectName(_fromUtf8("lineEditNodes"))
    self.gridLayout.addWidget(self.lineEditNodes, 9, 1, 1, 3)
    MainWindow.setCentralWidget(self.centralwidget)
    self.statusBar = QtGui.QStatusBar(MainWindow)
    self.statusBar.setObjectName(_fromUtf8("statusBar"))
    MainWindow.setStatusBar(self.statusBar)

    self.retranslateUi(MainWindow)
    QtCore.QMetaObject.connectSlotsByName(MainWindow)

  def retranslateUi(self, MainWindow):
    MainWindow.setWindowTitle(_translate("MainWindow", "Create Asset", None))
    self.labelFRange.setText(_translate("MainWindow", "fRange", None))
    self.labelStageType.setText(_translate("MainWindow", "stageType", None))
    self.pushCreate.setText(_translate("MainWindow", "create", None))
    self.labelNodeType.setText(_translate("MainWindow", "nodeType", None))
    self.labelScene.setText(_translate("MainWindow", "scene", None))
    self.lineEditWorkers.setToolTip(_translate("MainWindow", "list of space separated usernames", None))
    self.labelFileType.setText(_translate("MainWindow", "fileType", None))
    self.labelSequence.setText(_translate("MainWindow", "sequence", None))
    self.lineEditDesc.setToolTip(_translate("MainWindow", "group owner of the project directory", None))
    self.labelDue.setText(_translate("MainWindow", "due date", None))
    self.labelAdmin.setText(_translate("MainWindow", "assign to", None))
    self.labelAssType.setText(_translate("MainWindow", "assetType", None))
    self.labelAssName.setText(_translate("MainWindow", "assetName", None))
    self.labelDesc.setToolTip(_translate("MainWindow", "group owner of the project directory", None))
    self.labelDesc.setText(_translate("MainWindow", "description", None))
    self.labelDirectory.setWhatsThis(_translate("MainWindow", "directory to store the output data from file. eg : rendered output of lighting files.", None))
    self.labelDirectory.setText(_translate("MainWindow", "directory", None))
    self.labelTags.setToolTip(_translate("MainWindow", "group owner of the project directory", None))
    self.labelTags.setText(_translate("MainWindow", "tags", None))
    self.pushTags.setText(_translate("MainWindow", "select", None))
    self.checkAssign.setText(_translate("MainWindow", "self", None))
    self.pushUsers.setText(_translate("MainWindow", "select", None))
    self.lineEditTags.setToolTip(_translate("MainWindow", "group owner of the project directory", None))
    self.lineEditTags.setText(_translate("MainWindow", "default", None))
    self.lineEditFRange.setText(_translate("MainWindow", "1", None))
    self.pushNodes.setText(_translate("MainWindow", "select", None))
    self.lineEditNodes.setToolTip(_translate("MainWindow", "group owner of the project directory", None))
    self.lineEditNodes.setText(_translate("MainWindow", "default", None))

