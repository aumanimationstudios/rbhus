# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rbhusEditMod.ui'
#
# Created: Wed Mar 26 10:53:34 2014
#      by: PyQt4 UI code generator 4.10.3
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

class Ui_rbhusEdit(object):
  def setupUi(self, rbhusEdit):
    rbhusEdit.setObjectName(_fromUtf8("rbhusEdit"))
    rbhusEdit.resize(550, 732)
    self.centralwidget = QtGui.QWidget(rbhusEdit)
    self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
    self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
    self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
    self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
    self.groupBox_2 = QtGui.QGroupBox(self.centralwidget)
    self.groupBox_2.setTitle(_fromUtf8(""))
    self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
    self.gridLayout_2 = QtGui.QGridLayout(self.groupBox_2)
    self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
    self.labelMaxBatch = QtGui.QLabel(self.groupBox_2)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.labelMaxBatch.sizePolicy().hasHeightForWidth())
    self.labelMaxBatch.setSizePolicy(sizePolicy)
    self.labelMaxBatch.setObjectName(_fromUtf8("labelMaxBatch"))
    self.gridLayout_2.addWidget(self.labelMaxBatch, 25, 0, 1, 1)
    self.labelAfc = QtGui.QLabel(self.groupBox_2)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.labelAfc.sizePolicy().hasHeightForWidth())
    self.labelAfc.setSizePolicy(sizePolicy)
    self.labelAfc.setObjectName(_fromUtf8("labelAfc"))
    self.gridLayout_2.addWidget(self.labelAfc, 18, 0, 1, 1)
    self.labelAfterTime = QtGui.QLabel(self.groupBox_2)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.labelAfterTime.sizePolicy().hasHeightForWidth())
    self.labelAfterTime.setSizePolicy(sizePolicy)
    self.labelAfterTime.setObjectName(_fromUtf8("labelAfterTime"))
    self.gridLayout_2.addWidget(self.labelAfterTime, 19, 0, 1, 1)
    self.afterTimeEdit = QtGui.QDateTimeEdit(self.groupBox_2)
    self.afterTimeEdit.setEnabled(False)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.afterTimeEdit.sizePolicy().hasHeightForWidth())
    self.afterTimeEdit.setSizePolicy(sizePolicy)
    self.afterTimeEdit.setTime(QtCore.QTime(14, 0, 0))
    self.afterTimeEdit.setCurrentSection(QtGui.QDateTimeEdit.YearSection)
    self.afterTimeEdit.setCalendarPopup(True)
    self.afterTimeEdit.setObjectName(_fromUtf8("afterTimeEdit"))
    self.gridLayout_2.addWidget(self.afterTimeEdit, 19, 1, 1, 1)
    self.labelPriority = QtGui.QLabel(self.groupBox_2)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.labelPriority.sizePolicy().hasHeightForWidth())
    self.labelPriority.setSizePolicy(sizePolicy)
    self.labelPriority.setObjectName(_fromUtf8("labelPriority"))
    self.gridLayout_2.addWidget(self.labelPriority, 22, 0, 1, 1)
    self.labelLogbase = QtGui.QLabel(self.groupBox_2)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.labelLogbase.sizePolicy().hasHeightForWidth())
    self.labelLogbase.setSizePolicy(sizePolicy)
    self.labelLogbase.setObjectName(_fromUtf8("labelLogbase"))
    self.gridLayout_2.addWidget(self.labelLogbase, 20, 0, 1, 1)
    self.pushAfc = QtGui.QPushButton(self.groupBox_2)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.pushAfc.sizePolicy().hasHeightForWidth())
    self.pushAfc.setSizePolicy(sizePolicy)
    self.pushAfc.setObjectName(_fromUtf8("pushAfc"))
    self.gridLayout_2.addWidget(self.pushAfc, 18, 2, 1, 1)
    self.labelFileName = QtGui.QLabel(self.groupBox_2)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.labelFileName.sizePolicy().hasHeightForWidth())
    self.labelFileName.setSizePolicy(sizePolicy)
    self.labelFileName.setObjectName(_fromUtf8("labelFileName"))
    self.gridLayout_2.addWidget(self.labelFileName, 0, 0, 1, 1)
    self.lineEditAfc = QtGui.QLineEdit(self.groupBox_2)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.lineEditAfc.sizePolicy().hasHeightForWidth())
    self.lineEditAfc.setSizePolicy(sizePolicy)
    self.lineEditAfc.setObjectName(_fromUtf8("lineEditAfc"))
    self.gridLayout_2.addWidget(self.lineEditAfc, 18, 1, 1, 1)
    self.labelOutPutDir = QtGui.QLabel(self.groupBox_2)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.labelOutPutDir.sizePolicy().hasHeightForWidth())
    self.labelOutPutDir.setSizePolicy(sizePolicy)
    self.labelOutPutDir.setObjectName(_fromUtf8("labelOutPutDir"))
    self.gridLayout_2.addWidget(self.labelOutPutDir, 3, 0, 1, 1)
    self.pushBfc = QtGui.QPushButton(self.groupBox_2)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.pushBfc.sizePolicy().hasHeightForWidth())
    self.pushBfc.setSizePolicy(sizePolicy)
    self.pushBfc.setObjectName(_fromUtf8("pushBfc"))
    self.gridLayout_2.addWidget(self.pushBfc, 17, 2, 1, 1)
    self.spinPriority = QtGui.QSpinBox(self.groupBox_2)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.spinPriority.sizePolicy().hasHeightForWidth())
    self.spinPriority.setSizePolicy(sizePolicy)
    self.spinPriority.setMaximum(999999999)
    self.spinPriority.setObjectName(_fromUtf8("spinPriority"))
    self.gridLayout_2.addWidget(self.spinPriority, 22, 1, 1, 1)
    self.lineEditImageName = QtGui.QLineEdit(self.groupBox_2)
    self.lineEditImageName.setEnabled(False)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.lineEditImageName.sizePolicy().hasHeightForWidth())
    self.lineEditImageName.setSizePolicy(sizePolicy)
    self.lineEditImageName.setObjectName(_fromUtf8("lineEditImageName"))
    self.gridLayout_2.addWidget(self.lineEditImageName, 4, 1, 1, 1)
    self.labelBatching = QtGui.QLabel(self.groupBox_2)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.labelBatching.sizePolicy().hasHeightForWidth())
    self.labelBatching.setSizePolicy(sizePolicy)
    self.labelBatching.setObjectName(_fromUtf8("labelBatching"))
    self.gridLayout_2.addWidget(self.labelBatching, 23, 0, 1, 1)
    self.pushOutPutDir = QtGui.QPushButton(self.groupBox_2)
    self.pushOutPutDir.setEnabled(False)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.pushOutPutDir.sizePolicy().hasHeightForWidth())
    self.pushOutPutDir.setSizePolicy(sizePolicy)
    self.pushOutPutDir.setObjectName(_fromUtf8("pushOutPutDir"))
    self.gridLayout_2.addWidget(self.pushOutPutDir, 3, 2, 1, 1)
    self.pushFileName = QtGui.QPushButton(self.groupBox_2)
    self.pushFileName.setEnabled(False)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.pushFileName.sizePolicy().hasHeightForWidth())
    self.pushFileName.setSizePolicy(sizePolicy)
    self.pushFileName.setObjectName(_fromUtf8("pushFileName"))
    self.gridLayout_2.addWidget(self.pushFileName, 0, 2, 1, 1)
    self.spinRerunThresh = QtGui.QSpinBox(self.groupBox_2)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.spinRerunThresh.sizePolicy().hasHeightForWidth())
    self.spinRerunThresh.setSizePolicy(sizePolicy)
    self.spinRerunThresh.setObjectName(_fromUtf8("spinRerunThresh"))
    self.gridLayout_2.addWidget(self.spinRerunThresh, 21, 1, 1, 1)
    self.checkAfterTime = QtGui.QCheckBox(self.groupBox_2)
    self.checkAfterTime.setObjectName(_fromUtf8("checkAfterTime"))
    self.gridLayout_2.addWidget(self.checkAfterTime, 19, 2, 1, 1)
    self.labelMinBatch = QtGui.QLabel(self.groupBox_2)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.labelMinBatch.sizePolicy().hasHeightForWidth())
    self.labelMinBatch.setSizePolicy(sizePolicy)
    self.labelMinBatch.setObjectName(_fromUtf8("labelMinBatch"))
    self.gridLayout_2.addWidget(self.labelMinBatch, 24, 0, 1, 1)
    self.spinMaxBatch = QtGui.QSpinBox(self.groupBox_2)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.spinMaxBatch.sizePolicy().hasHeightForWidth())
    self.spinMaxBatch.setSizePolicy(sizePolicy)
    self.spinMaxBatch.setMinimum(1)
    self.spinMaxBatch.setMaximum(999999999)
    self.spinMaxBatch.setObjectName(_fromUtf8("spinMaxBatch"))
    self.gridLayout_2.addWidget(self.spinMaxBatch, 25, 1, 1, 1)
    self.spinMinBatch = QtGui.QSpinBox(self.groupBox_2)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.spinMinBatch.sizePolicy().hasHeightForWidth())
    self.spinMinBatch.setSizePolicy(sizePolicy)
    self.spinMinBatch.setMinimum(1)
    self.spinMinBatch.setMaximum(999999999)
    self.spinMinBatch.setObjectName(_fromUtf8("spinMinBatch"))
    self.gridLayout_2.addWidget(self.spinMinBatch, 24, 1, 1, 1)
    self.lineEditBfc = QtGui.QLineEdit(self.groupBox_2)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.lineEditBfc.sizePolicy().hasHeightForWidth())
    self.lineEditBfc.setSizePolicy(sizePolicy)
    self.lineEditBfc.setObjectName(_fromUtf8("lineEditBfc"))
    self.gridLayout_2.addWidget(self.lineEditBfc, 17, 1, 1, 1)
    self.pushLogOpen = QtGui.QPushButton(self.groupBox_2)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.pushLogOpen.sizePolicy().hasHeightForWidth())
    self.pushLogOpen.setSizePolicy(sizePolicy)
    self.pushLogOpen.setObjectName(_fromUtf8("pushLogOpen"))
    self.gridLayout_2.addWidget(self.pushLogOpen, 20, 2, 1, 1)
    self.comboBatching = QtGui.QComboBox(self.groupBox_2)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.comboBatching.sizePolicy().hasHeightForWidth())
    self.comboBatching.setSizePolicy(sizePolicy)
    self.comboBatching.setObjectName(_fromUtf8("comboBatching"))
    self.comboBatching.addItem(_fromUtf8(""))
    self.comboBatching.addItem(_fromUtf8(""))
    self.gridLayout_2.addWidget(self.comboBatching, 23, 1, 1, 1)
    self.labelDescription = QtGui.QLabel(self.groupBox_2)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.labelDescription.sizePolicy().hasHeightForWidth())
    self.labelDescription.setSizePolicy(sizePolicy)
    self.labelDescription.setObjectName(_fromUtf8("labelDescription"))
    self.gridLayout_2.addWidget(self.labelDescription, 26, 0, 1, 1)
    self.lineEditFileName = QtGui.QLineEdit(self.groupBox_2)
    self.lineEditFileName.setEnabled(False)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.lineEditFileName.sizePolicy().hasHeightForWidth())
    self.lineEditFileName.setSizePolicy(sizePolicy)
    self.lineEditFileName.setDragEnabled(True)
    self.lineEditFileName.setObjectName(_fromUtf8("lineEditFileName"))
    self.gridLayout_2.addWidget(self.lineEditFileName, 0, 1, 1, 1)
    self.lineEditLogbase = QtGui.QLineEdit(self.groupBox_2)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.lineEditLogbase.sizePolicy().hasHeightForWidth())
    self.lineEditLogbase.setSizePolicy(sizePolicy)
    self.lineEditLogbase.setObjectName(_fromUtf8("lineEditLogbase"))
    self.gridLayout_2.addWidget(self.lineEditLogbase, 20, 1, 1, 1)
    self.lineEditOutPutDir = QtGui.QLineEdit(self.groupBox_2)
    self.lineEditOutPutDir.setEnabled(False)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.lineEditOutPutDir.sizePolicy().hasHeightForWidth())
    self.lineEditOutPutDir.setSizePolicy(sizePolicy)
    self.lineEditOutPutDir.setObjectName(_fromUtf8("lineEditOutPutDir"))
    self.gridLayout_2.addWidget(self.lineEditOutPutDir, 3, 1, 1, 1)
    self.labelImageName = QtGui.QLabel(self.groupBox_2)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.labelImageName.sizePolicy().hasHeightForWidth())
    self.labelImageName.setSizePolicy(sizePolicy)
    self.labelImageName.setObjectName(_fromUtf8("labelImageName"))
    self.gridLayout_2.addWidget(self.labelImageName, 4, 0, 1, 1)
    self.lineEditFrange = QtGui.QLineEdit(self.groupBox_2)
    self.lineEditFrange.setEnabled(True)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.lineEditFrange.sizePolicy().hasHeightForWidth())
    self.lineEditFrange.setSizePolicy(sizePolicy)
    self.lineEditFrange.setObjectName(_fromUtf8("lineEditFrange"))
    self.gridLayout_2.addWidget(self.lineEditFrange, 8, 1, 1, 1)
    self.labelBfc = QtGui.QLabel(self.groupBox_2)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.labelBfc.sizePolicy().hasHeightForWidth())
    self.labelBfc.setSizePolicy(sizePolicy)
    self.labelBfc.setObjectName(_fromUtf8("labelBfc"))
    self.gridLayout_2.addWidget(self.labelBfc, 17, 0, 1, 1)
    self.labelFrange = QtGui.QLabel(self.groupBox_2)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.labelFrange.sizePolicy().hasHeightForWidth())
    self.labelFrange.setSizePolicy(sizePolicy)
    self.labelFrange.setObjectName(_fromUtf8("labelFrange"))
    self.gridLayout_2.addWidget(self.labelFrange, 8, 0, 1, 1)
    self.lineEditDescription = QtGui.QLineEdit(self.groupBox_2)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.lineEditDescription.sizePolicy().hasHeightForWidth())
    self.lineEditDescription.setSizePolicy(sizePolicy)
    self.lineEditDescription.setDragEnabled(True)
    self.lineEditDescription.setObjectName(_fromUtf8("lineEditDescription"))
    self.gridLayout_2.addWidget(self.lineEditDescription, 26, 1, 1, 1)
    self.labelRerunThresh = QtGui.QLabel(self.groupBox_2)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.labelRerunThresh.sizePolicy().hasHeightForWidth())
    self.labelRerunThresh.setSizePolicy(sizePolicy)
    self.labelRerunThresh.setObjectName(_fromUtf8("labelRerunThresh"))
    self.gridLayout_2.addWidget(self.labelRerunThresh, 21, 0, 1, 1)
    self.comboRenderer = QtGui.QComboBox(self.groupBox_2)
    self.comboRenderer.setEnabled(True)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.comboRenderer.sizePolicy().hasHeightForWidth())
    self.comboRenderer.setSizePolicy(sizePolicy)
    self.comboRenderer.setObjectName(_fromUtf8("comboRenderer"))
    self.gridLayout_2.addWidget(self.comboRenderer, 13, 1, 1, 1)
    self.labelOsType = QtGui.QLabel(self.groupBox_2)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.labelOsType.sizePolicy().hasHeightForWidth())
    self.labelOsType.setSizePolicy(sizePolicy)
    self.labelOsType.setObjectName(_fromUtf8("labelOsType"))
    self.gridLayout_2.addWidget(self.labelOsType, 15, 0, 1, 1)
    self.labelHostGroup = QtGui.QLabel(self.groupBox_2)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.labelHostGroup.sizePolicy().hasHeightForWidth())
    self.labelHostGroup.setSizePolicy(sizePolicy)
    self.labelHostGroup.setObjectName(_fromUtf8("labelHostGroup"))
    self.gridLayout_2.addWidget(self.labelHostGroup, 11, 0, 1, 1)
    self.lineEditLayer = QtGui.QLineEdit(self.groupBox_2)
    self.lineEditLayer.setEnabled(False)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.lineEditLayer.sizePolicy().hasHeightForWidth())
    self.lineEditLayer.setSizePolicy(sizePolicy)
    self.lineEditLayer.setToolTip(_fromUtf8(""))
    self.lineEditLayer.setText(_fromUtf8(""))
    self.lineEditLayer.setObjectName(_fromUtf8("lineEditLayer"))
    self.gridLayout_2.addWidget(self.lineEditLayer, 14, 1, 1, 1)
    self.labelCamera = QtGui.QLabel(self.groupBox_2)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.labelCamera.sizePolicy().hasHeightForWidth())
    self.labelCamera.setSizePolicy(sizePolicy)
    self.labelCamera.setObjectName(_fromUtf8("labelCamera"))
    self.gridLayout_2.addWidget(self.labelCamera, 9, 0, 1, 1)
    self.lineEditCamera = QtGui.QLineEdit(self.groupBox_2)
    self.lineEditCamera.setEnabled(False)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.lineEditCamera.sizePolicy().hasHeightForWidth())
    self.lineEditCamera.setSizePolicy(sizePolicy)
    self.lineEditCamera.setObjectName(_fromUtf8("lineEditCamera"))
    self.gridLayout_2.addWidget(self.lineEditCamera, 9, 1, 1, 1)
    self.labelResolution = QtGui.QLabel(self.groupBox_2)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.labelResolution.sizePolicy().hasHeightForWidth())
    self.labelResolution.setSizePolicy(sizePolicy)
    self.labelResolution.setObjectName(_fromUtf8("labelResolution"))
    self.gridLayout_2.addWidget(self.labelResolution, 10, 0, 1, 1)
    self.lineEditResolution = QtGui.QLineEdit(self.groupBox_2)
    self.lineEditResolution.setEnabled(False)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.lineEditResolution.sizePolicy().hasHeightForWidth())
    self.lineEditResolution.setSizePolicy(sizePolicy)
    self.lineEditResolution.setObjectName(_fromUtf8("lineEditResolution"))
    self.gridLayout_2.addWidget(self.lineEditResolution, 10, 1, 1, 1)
    self.labelLayer = QtGui.QLabel(self.groupBox_2)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.labelLayer.sizePolicy().hasHeightForWidth())
    self.labelLayer.setSizePolicy(sizePolicy)
    self.labelLayer.setObjectName(_fromUtf8("labelLayer"))
    self.gridLayout_2.addWidget(self.labelLayer, 14, 0, 1, 1)
    self.labeRenderer = QtGui.QLabel(self.groupBox_2)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.labeRenderer.sizePolicy().hasHeightForWidth())
    self.labeRenderer.setSizePolicy(sizePolicy)
    self.labeRenderer.setObjectName(_fromUtf8("labeRenderer"))
    self.gridLayout_2.addWidget(self.labeRenderer, 13, 0, 1, 1)
    self.lineEditAfterTask = QtGui.QLineEdit(self.groupBox_2)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.lineEditAfterTask.sizePolicy().hasHeightForWidth())
    self.lineEditAfterTask.setSizePolicy(sizePolicy)
    self.lineEditAfterTask.setObjectName(_fromUtf8("lineEditAfterTask"))
    self.gridLayout_2.addWidget(self.lineEditAfterTask, 16, 1, 1, 1)
    self.labelAfterTask = QtGui.QLabel(self.groupBox_2)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.labelAfterTask.sizePolicy().hasHeightForWidth())
    self.labelAfterTask.setSizePolicy(sizePolicy)
    self.labelAfterTask.setObjectName(_fromUtf8("labelAfterTask"))
    self.gridLayout_2.addWidget(self.labelAfterTask, 16, 0, 1, 1)
    self.comboOsType = QtGui.QComboBox(self.groupBox_2)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.comboOsType.sizePolicy().hasHeightForWidth())
    self.comboOsType.setSizePolicy(sizePolicy)
    self.comboOsType.setObjectName(_fromUtf8("comboOsType"))
    self.gridLayout_2.addWidget(self.comboOsType, 15, 1, 1, 1)
    self.labelImageType = QtGui.QLabel(self.groupBox_2)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.labelImageType.sizePolicy().hasHeightForWidth())
    self.labelImageType.setSizePolicy(sizePolicy)
    self.labelImageType.setObjectName(_fromUtf8("labelImageType"))
    self.gridLayout_2.addWidget(self.labelImageType, 5, 0, 1, 1)
    self.lineEditHostGroups = QtGui.QLineEdit(self.groupBox_2)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.lineEditHostGroups.sizePolicy().hasHeightForWidth())
    self.lineEditHostGroups.setSizePolicy(sizePolicy)
    self.lineEditHostGroups.setReadOnly(True)
    self.lineEditHostGroups.setObjectName(_fromUtf8("lineEditHostGroups"))
    self.gridLayout_2.addWidget(self.lineEditHostGroups, 11, 1, 1, 1)
    self.pushSelectHostGroups = QtGui.QPushButton(self.groupBox_2)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.pushSelectHostGroups.sizePolicy().hasHeightForWidth())
    self.pushSelectHostGroups.setSizePolicy(sizePolicy)
    self.pushSelectHostGroups.setObjectName(_fromUtf8("pushSelectHostGroups"))
    self.gridLayout_2.addWidget(self.pushSelectHostGroups, 11, 2, 1, 1)
    self.checkSloppy = QtGui.QCheckBox(self.groupBox_2)
    self.checkSloppy.setObjectName(_fromUtf8("checkSloppy"))
    self.gridLayout_2.addWidget(self.checkSloppy, 16, 2, 1, 1)
    self.comboImageType = QtGui.QComboBox(self.groupBox_2)
    self.comboImageType.setEnabled(False)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.comboImageType.sizePolicy().hasHeightForWidth())
    self.comboImageType.setSizePolicy(sizePolicy)
    self.comboImageType.setObjectName(_fromUtf8("comboImageType"))
    self.gridLayout_2.addWidget(self.comboImageType, 5, 1, 1, 1)
    self.labelType = QtGui.QLabel(self.groupBox_2)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.labelType.sizePolicy().hasHeightForWidth())
    self.labelType.setSizePolicy(sizePolicy)
    self.labelType.setObjectName(_fromUtf8("labelType"))
    self.gridLayout_2.addWidget(self.labelType, 1, 0, 1, 1)
    self.comboType = QtGui.QComboBox(self.groupBox_2)
    self.comboType.setEnabled(True)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.comboType.sizePolicy().hasHeightForWidth())
    self.comboType.setSizePolicy(sizePolicy)
    self.comboType.setObjectName(_fromUtf8("comboType"))
    self.gridLayout_2.addWidget(self.comboType, 1, 1, 1, 1)
    self.verticalLayout.addWidget(self.groupBox_2)
    self.line = QtGui.QFrame(self.centralwidget)
    self.line.setFrameShape(QtGui.QFrame.HLine)
    self.line.setFrameShadow(QtGui.QFrame.Sunken)
    self.line.setObjectName(_fromUtf8("line"))
    self.verticalLayout.addWidget(self.line)
    self.horizontalLayout = QtGui.QHBoxLayout()
    self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
    spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
    self.horizontalLayout.addItem(spacerItem)
    self.pushCancel = QtGui.QPushButton(self.centralwidget)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.pushCancel.sizePolicy().hasHeightForWidth())
    self.pushCancel.setSizePolicy(sizePolicy)
    self.pushCancel.setObjectName(_fromUtf8("pushCancel"))
    self.horizontalLayout.addWidget(self.pushCancel)
    self.pushApply = QtGui.QPushButton(self.centralwidget)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.pushApply.sizePolicy().hasHeightForWidth())
    self.pushApply.setSizePolicy(sizePolicy)
    self.pushApply.setObjectName(_fromUtf8("pushApply"))
    self.horizontalLayout.addWidget(self.pushApply)
    self.verticalLayout.addLayout(self.horizontalLayout)
    rbhusEdit.setCentralWidget(self.centralwidget)
    self.statusbar = QtGui.QStatusBar(rbhusEdit)
    self.statusbar.setObjectName(_fromUtf8("statusbar"))
    rbhusEdit.setStatusBar(self.statusbar)

    self.retranslateUi(rbhusEdit)
    QtCore.QMetaObject.connectSlotsByName(rbhusEdit)

  def retranslateUi(self, rbhusEdit):
    rbhusEdit.setWindowTitle(_translate("rbhusEdit", "rbhusEdit", None))
    self.labelMaxBatch.setText(_translate("rbhusEdit", "maxBatch", None))
    self.labelAfc.setText(_translate("rbhusEdit", "afc          ", None))
    self.labelAfterTime.setText(_translate("rbhusEdit", "afterTime ", None))
    self.afterTimeEdit.setDisplayFormat(_translate("rbhusEdit", "yyyy-M-d h:mm A", None))
    self.labelPriority.setText(_translate("rbhusEdit", "priority", None))
    self.labelLogbase.setText(_translate("rbhusEdit", "logbase   ", None))
    self.pushAfc.setText(_translate("rbhusEdit", "open", None))
    self.labelFileName.setText(_translate("rbhusEdit", "fileName", None))
    self.labelOutPutDir.setText(_translate("rbhusEdit", "outDir", None))
    self.pushBfc.setText(_translate("rbhusEdit", "open", None))
    self.labelBatching.setText(_translate("rbhusEdit", "batching", None))
    self.pushOutPutDir.setText(_translate("rbhusEdit", "open", None))
    self.pushFileName.setText(_translate("rbhusEdit", "open", None))
    self.checkAfterTime.setText(_translate("rbhusEdit", "enable", None))
    self.labelMinBatch.setText(_translate("rbhusEdit", "minBatch", None))
    self.pushLogOpen.setText(_translate("rbhusEdit", "open", None))
    self.comboBatching.setItemText(0, _translate("rbhusEdit", "deactive", None))
    self.comboBatching.setItemText(1, _translate("rbhusEdit", "active", None))
    self.labelDescription.setText(_translate("rbhusEdit", "description", None))
    self.labelImageName.setText(_translate("rbhusEdit", "outName", None))
    self.labelBfc.setText(_translate("rbhusEdit", "bfc          ", None))
    self.labelFrange.setText(_translate("rbhusEdit", "fRange     ", None))
    self.lineEditDescription.setText(_translate("rbhusEdit", "default", None))
    self.labelRerunThresh.setText(_translate("rbhusEdit", "rerunThres", None))
    self.labelOsType.setText(_translate("rbhusEdit", "osType", None))
    self.labelHostGroup.setText(_translate("rbhusEdit", "hostGroup", None))
    self.labelCamera.setText(_translate("rbhusEdit", "camera", None))
    self.labelResolution.setText(_translate("rbhusEdit", "resolution", None))
    self.labelLayer.setText(_translate("rbhusEdit", "layer", None))
    self.labeRenderer.setText(_translate("rbhusEdit", "renderer", None))
    self.lineEditAfterTask.setText(_translate("rbhusEdit", "0", None))
    self.labelAfterTask.setText(_translate("rbhusEdit", "afterTasks", None))
    self.labelImageType.setText(_translate("rbhusEdit", "imageType", None))
    self.lineEditHostGroups.setToolTip(_translate("rbhusEdit", "comma seperated list of cameras to render", None))
    self.lineEditHostGroups.setText(_translate("rbhusEdit", "default", None))
    self.pushSelectHostGroups.setText(_translate("rbhusEdit", "select", None))
    self.checkSloppy.setText(_translate("rbhusEdit", "sloppy", None))
    self.labelType.setText(_translate("rbhusEdit", "fileType", None))
    self.pushCancel.setText(_translate("rbhusEdit", "reset", None))
    self.pushApply.setText(_translate("rbhusEdit", "apply", None))

