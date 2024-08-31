# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rbhusPipeSubmitRenderMod.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_rbhusSubmit(object):
    def setupUi(self, rbhusSubmit):
        rbhusSubmit.setObjectName("rbhusSubmit")
        rbhusSubmit.resize(530, 782)
        self.centralwidget = QtWidgets.QWidget(rbhusSubmit)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.lineEditOutName = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditOutName.sizePolicy().hasHeightForWidth())
        self.lineEditOutName.setSizePolicy(sizePolicy)
        self.lineEditOutName.setDragEnabled(True)
        self.lineEditOutName.setReadOnly(False)
        self.lineEditOutName.setObjectName("lineEditOutName")
        self.gridLayout.addWidget(self.lineEditOutName, 6, 1, 1, 1)
        self.labelBatching = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelBatching.sizePolicy().hasHeightForWidth())
        self.labelBatching.setSizePolicy(sizePolicy)
        self.labelBatching.setObjectName("labelBatching")
        self.gridLayout.addWidget(self.labelBatching, 21, 0, 1, 1)
        self.afterTimeEdit = QtWidgets.QDateTimeEdit(self.centralwidget)
        self.afterTimeEdit.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.afterTimeEdit.sizePolicy().hasHeightForWidth())
        self.afterTimeEdit.setSizePolicy(sizePolicy)
        self.afterTimeEdit.setTime(QtCore.QTime(14, 0, 0))
        self.afterTimeEdit.setCurrentSection(QtWidgets.QDateTimeEdit.YearSection)
        self.afterTimeEdit.setCalendarPopup(True)
        self.afterTimeEdit.setObjectName("afterTimeEdit")
        self.gridLayout.addWidget(self.afterTimeEdit, 18, 1, 1, 1)
        self.pushSelectHostGroups = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushSelectHostGroups.sizePolicy().hasHeightForWidth())
        self.pushSelectHostGroups.setSizePolicy(sizePolicy)
        self.pushSelectHostGroups.setObjectName("pushSelectHostGroups")
        self.gridLayout.addWidget(self.pushSelectHostGroups, 11, 2, 1, 1)
        self.lineEditHostGroups = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditHostGroups.sizePolicy().hasHeightForWidth())
        self.lineEditHostGroups.setSizePolicy(sizePolicy)
        self.lineEditHostGroups.setReadOnly(True)
        self.lineEditHostGroups.setObjectName("lineEditHostGroups")
        self.gridLayout.addWidget(self.lineEditHostGroups, 11, 1, 1, 1)
        self.lineEditDescription = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditDescription.sizePolicy().hasHeightForWidth())
        self.lineEditDescription.setSizePolicy(sizePolicy)
        self.lineEditDescription.setDragEnabled(True)
        self.lineEditDescription.setObjectName("lineEditDescription")
        self.gridLayout.addWidget(self.lineEditDescription, 24, 1, 1, 1)
        self.labelPrio = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelPrio.sizePolicy().hasHeightForWidth())
        self.labelPrio.setSizePolicy(sizePolicy)
        self.labelPrio.setObjectName("labelPrio")
        self.gridLayout.addWidget(self.labelPrio, 19, 0, 1, 1)
        self.labelImageName = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelImageName.sizePolicy().hasHeightForWidth())
        self.labelImageName.setSizePolicy(sizePolicy)
        self.labelImageName.setObjectName("labelImageName")
        self.gridLayout.addWidget(self.labelImageName, 6, 0, 1, 1)
        self.checkExrMov = QtWidgets.QCheckBox(self.centralwidget)
        self.checkExrMov.setChecked(False)
        self.checkExrMov.setObjectName("checkExrMov")
        self.gridLayout.addWidget(self.checkExrMov, 25, 1, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.labelMinBatch = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelMinBatch.sizePolicy().hasHeightForWidth())
        self.labelMinBatch.setSizePolicy(sizePolicy)
        self.labelMinBatch.setObjectName("labelMinBatch")
        self.horizontalLayout_3.addWidget(self.labelMinBatch)
        self.spinMinBatch = QtWidgets.QSpinBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinMinBatch.sizePolicy().hasHeightForWidth())
        self.spinMinBatch.setSizePolicy(sizePolicy)
        self.spinMinBatch.setMinimum(1)
        self.spinMinBatch.setMaximum(999999999)
        self.spinMinBatch.setObjectName("spinMinBatch")
        self.horizontalLayout_3.addWidget(self.spinMinBatch)
        spacerItem = QtWidgets.QSpacerItem(30, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.labelMaxBatch = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelMaxBatch.sizePolicy().hasHeightForWidth())
        self.labelMaxBatch.setSizePolicy(sizePolicy)
        self.labelMaxBatch.setObjectName("labelMaxBatch")
        self.horizontalLayout_3.addWidget(self.labelMaxBatch)
        self.spinMaxBatch = QtWidgets.QSpinBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinMaxBatch.sizePolicy().hasHeightForWidth())
        self.spinMaxBatch.setSizePolicy(sizePolicy)
        self.spinMaxBatch.setMinimum(1)
        self.spinMaxBatch.setMaximum(999999999)
        self.spinMaxBatch.setProperty("value", 2)
        self.spinMaxBatch.setObjectName("spinMaxBatch")
        self.horizontalLayout_3.addWidget(self.spinMaxBatch)
        self.gridLayout.addLayout(self.horizontalLayout_3, 21, 1, 1, 1)
        self.lineEditFileName = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditFileName.sizePolicy().hasHeightForWidth())
        self.lineEditFileName.setSizePolicy(sizePolicy)
        self.lineEditFileName.setToolTip("")
        self.lineEditFileName.setDragEnabled(True)
        self.lineEditFileName.setObjectName("lineEditFileName")
        self.gridLayout.addWidget(self.lineEditFileName, 1, 1, 1, 1)
        self.labelFrange = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelFrange.sizePolicy().hasHeightForWidth())
        self.labelFrange.setSizePolicy(sizePolicy)
        self.labelFrange.setObjectName("labelFrange")
        self.gridLayout.addWidget(self.labelFrange, 8, 0, 1, 1)
        self.pushSubmit = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushSubmit.sizePolicy().hasHeightForWidth())
        self.pushSubmit.setSizePolicy(sizePolicy)
        self.pushSubmit.setObjectName("pushSubmit")
        self.gridLayout.addWidget(self.pushSubmit, 27, 2, 1, 1)
        self.comboRenderer = QtWidgets.QComboBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboRenderer.sizePolicy().hasHeightForWidth())
        self.comboRenderer.setSizePolicy(sizePolicy)
        self.comboRenderer.setObjectName("comboRenderer")
        self.gridLayout.addWidget(self.comboRenderer, 13, 1, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.comboRes = QtWidgets.QComboBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboRes.sizePolicy().hasHeightForWidth())
        self.comboRes.setSizePolicy(sizePolicy)
        self.comboRes.setObjectName("comboRes")
        self.horizontalLayout.addWidget(self.comboRes)
        self.lineEditRes = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditRes.sizePolicy().hasHeightForWidth())
        self.lineEditRes.setSizePolicy(sizePolicy)
        self.lineEditRes.setToolTip("")
        self.lineEditRes.setObjectName("lineEditRes")
        self.horizontalLayout.addWidget(self.lineEditRes)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.gridLayout.addLayout(self.horizontalLayout, 10, 1, 1, 1)
        self.lineEditLayer = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditLayer.sizePolicy().hasHeightForWidth())
        self.lineEditLayer.setSizePolicy(sizePolicy)
        self.lineEditLayer.setToolTip("")
        self.lineEditLayer.setObjectName("lineEditLayer")
        self.gridLayout.addWidget(self.lineEditLayer, 15, 1, 1, 1)
        self.comboFileType = QtWidgets.QComboBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboFileType.sizePolicy().hasHeightForWidth())
        self.comboFileType.setSizePolicy(sizePolicy)
        self.comboFileType.setObjectName("comboFileType")
        self.gridLayout.addWidget(self.comboFileType, 2, 1, 1, 1)
        self.labelUser = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelUser.sizePolicy().hasHeightForWidth())
        self.labelUser.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.labelUser.setFont(font)
        self.labelUser.setObjectName("labelUser")
        self.gridLayout.addWidget(self.labelUser, 0, 1, 1, 1)
        self.checkAfterTime = QtWidgets.QCheckBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkAfterTime.sizePolicy().hasHeightForWidth())
        self.checkAfterTime.setSizePolicy(sizePolicy)
        self.checkAfterTime.setObjectName("checkAfterTime")
        self.gridLayout.addWidget(self.checkAfterTime, 18, 2, 1, 1)
        self.labelOsType = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelOsType.sizePolicy().hasHeightForWidth())
        self.labelOsType.setSizePolicy(sizePolicy)
        self.labelOsType.setObjectName("labelOsType")
        self.gridLayout.addWidget(self.labelOsType, 16, 0, 1, 1)
        self.labelLayer = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelLayer.sizePolicy().hasHeightForWidth())
        self.labelLayer.setSizePolicy(sizePolicy)
        self.labelLayer.setObjectName("labelLayer")
        self.gridLayout.addWidget(self.labelLayer, 15, 0, 1, 1)
        self.checkPngMov = QtWidgets.QCheckBox(self.centralwidget)
        self.checkPngMov.setChecked(False)
        self.checkPngMov.setObjectName("checkPngMov")
        self.gridLayout.addWidget(self.checkPngMov, 26, 1, 1, 1)
        self.labelDescription = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelDescription.sizePolicy().hasHeightForWidth())
        self.labelDescription.setSizePolicy(sizePolicy)
        self.labelDescription.setObjectName("labelDescription")
        self.gridLayout.addWidget(self.labelDescription, 24, 0, 1, 1)
        self.comboPrio = QtWidgets.QComboBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboPrio.sizePolicy().hasHeightForWidth())
        self.comboPrio.setSizePolicy(sizePolicy)
        self.comboPrio.setObjectName("comboPrio")
        self.comboPrio.addItem("")
        self.comboPrio.addItem("")
        self.comboPrio.addItem("")
        self.gridLayout.addWidget(self.comboPrio, 19, 1, 1, 1)
        self.lineEditAfterTask = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditAfterTask.sizePolicy().hasHeightForWidth())
        self.lineEditAfterTask.setSizePolicy(sizePolicy)
        self.lineEditAfterTask.setObjectName("lineEditAfterTask")
        self.gridLayout.addWidget(self.lineEditAfterTask, 17, 1, 1, 1)
        self.labelFileName = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelFileName.sizePolicy().hasHeightForWidth())
        self.labelFileName.setSizePolicy(sizePolicy)
        self.labelFileName.setObjectName("labelFileName")
        self.gridLayout.addWidget(self.labelFileName, 1, 0, 1, 1)
        self.labelAfterTask = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelAfterTask.sizePolicy().hasHeightForWidth())
        self.labelAfterTask.setSizePolicy(sizePolicy)
        self.labelAfterTask.setObjectName("labelAfterTask")
        self.gridLayout.addWidget(self.labelAfterTask, 17, 0, 1, 1)
        self.labelAfterTime = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelAfterTime.sizePolicy().hasHeightForWidth())
        self.labelAfterTime.setSizePolicy(sizePolicy)
        self.labelAfterTime.setObjectName("labelAfterTime")
        self.gridLayout.addWidget(self.labelAfterTime, 18, 0, 1, 1)
        self.labelImageType = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelImageType.sizePolicy().hasHeightForWidth())
        self.labelImageType.setSizePolicy(sizePolicy)
        self.labelImageType.setObjectName("labelImageType")
        self.gridLayout.addWidget(self.labelImageType, 5, 0, 1, 1)
        self.labelResolution = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelResolution.sizePolicy().hasHeightForWidth())
        self.labelResolution.setSizePolicy(sizePolicy)
        self.labelResolution.setObjectName("labelResolution")
        self.gridLayout.addWidget(self.labelResolution, 10, 0, 1, 1)
        self.lineEditFrange = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditFrange.sizePolicy().hasHeightForWidth())
        self.lineEditFrange.setSizePolicy(sizePolicy)
        self.lineEditFrange.setToolTip("")
        self.lineEditFrange.setObjectName("lineEditFrange")
        self.gridLayout.addWidget(self.lineEditFrange, 8, 1, 1, 1)
        self.checkSloppy = QtWidgets.QCheckBox(self.centralwidget)
        self.checkSloppy.setObjectName("checkSloppy")
        self.gridLayout.addWidget(self.checkSloppy, 17, 2, 1, 1)
        self.comboImageType = QtWidgets.QComboBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboImageType.sizePolicy().hasHeightForWidth())
        self.comboImageType.setSizePolicy(sizePolicy)
        self.comboImageType.setObjectName("comboImageType")
        self.gridLayout.addWidget(self.comboImageType, 5, 1, 1, 1)
        self.labelCamera = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelCamera.sizePolicy().hasHeightForWidth())
        self.labelCamera.setSizePolicy(sizePolicy)
        self.labelCamera.setObjectName("labelCamera")
        self.gridLayout.addWidget(self.labelCamera, 9, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.comboOsType = QtWidgets.QComboBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboOsType.sizePolicy().hasHeightForWidth())
        self.comboOsType.setSizePolicy(sizePolicy)
        self.comboOsType.setObjectName("comboOsType")
        self.gridLayout.addWidget(self.comboOsType, 16, 1, 1, 1)
        self.checkBatching = QtWidgets.QCheckBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBatching.sizePolicy().hasHeightForWidth())
        self.checkBatching.setSizePolicy(sizePolicy)
        self.checkBatching.setChecked(False)
        self.checkBatching.setObjectName("checkBatching")
        self.gridLayout.addWidget(self.checkBatching, 21, 2, 1, 1)
        self.labeFileType = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labeFileType.sizePolicy().hasHeightForWidth())
        self.labeFileType.setSizePolicy(sizePolicy)
        self.labeFileType.setObjectName("labeFileType")
        self.gridLayout.addWidget(self.labeFileType, 2, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.checkHold = QtWidgets.QCheckBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkHold.sizePolicy().hasHeightForWidth())
        self.checkHold.setSizePolicy(sizePolicy)
        self.checkHold.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.checkHold.setObjectName("checkHold")
        self.horizontalLayout_2.addWidget(self.checkHold)
        self.gridLayout.addLayout(self.horizontalLayout_2, 27, 1, 1, 1)
        self.labeRenderer = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labeRenderer.sizePolicy().hasHeightForWidth())
        self.labeRenderer.setSizePolicy(sizePolicy)
        self.labeRenderer.setObjectName("labeRenderer")
        self.gridLayout.addWidget(self.labeRenderer, 13, 0, 1, 1)
        self.labelHostGroup = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelHostGroup.sizePolicy().hasHeightForWidth())
        self.labelHostGroup.setSizePolicy(sizePolicy)
        self.labelHostGroup.setObjectName("labelHostGroup")
        self.gridLayout.addWidget(self.labelHostGroup, 11, 0, 1, 1)
        self.lineEditCameras = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditCameras.sizePolicy().hasHeightForWidth())
        self.lineEditCameras.setSizePolicy(sizePolicy)
        self.lineEditCameras.setObjectName("lineEditCameras")
        self.gridLayout.addWidget(self.lineEditCameras, 9, 1, 1, 1)
        self.labelOutDir = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelOutDir.sizePolicy().hasHeightForWidth())
        self.labelOutDir.setSizePolicy(sizePolicy)
        self.labelOutDir.setObjectName("labelOutDir")
        self.gridLayout.addWidget(self.labelOutDir, 3, 0, 1, 1)
        self.lineEditOutDir = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditOutDir.sizePolicy().hasHeightForWidth())
        self.lineEditOutDir.setSizePolicy(sizePolicy)
        self.lineEditOutDir.setToolTip("")
        self.lineEditOutDir.setDragEnabled(True)
        self.lineEditOutDir.setObjectName("lineEditOutDir")
        self.gridLayout.addWidget(self.lineEditOutDir, 3, 1, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.pushOutDir = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushOutDir.sizePolicy().hasHeightForWidth())
        self.pushOutDir.setSizePolicy(sizePolicy)
        self.pushOutDir.setMinimumSize(QtCore.QSize(1, 0))
        self.pushOutDir.setObjectName("pushOutDir")
        self.horizontalLayout_4.addWidget(self.pushOutDir)
        self.checkOutDir = QtWidgets.QCheckBox(self.centralwidget)
        self.checkOutDir.setText("")
        self.checkOutDir.setObjectName("checkOutDir")
        self.horizontalLayout_4.addWidget(self.checkOutDir)
        self.gridLayout.addLayout(self.horizontalLayout_4, 3, 2, 1, 1)
        rbhusSubmit.setCentralWidget(self.centralwidget)

        self.retranslateUi(rbhusSubmit)
        QtCore.QMetaObject.connectSlotsByName(rbhusSubmit)

    def retranslateUi(self, rbhusSubmit):
        _translate = QtCore.QCoreApplication.translate
        rbhusSubmit.setWindowTitle(_translate("rbhusSubmit", "rbhusSubmit"))
        self.lineEditOutName.setToolTip(_translate("rbhusSubmit", "name of the image file. eg: wtf.png"))
        self.lineEditOutName.setWhatsThis(_translate("rbhusSubmit", "<html><head/><body><p>name of the image file. eg: <span style=\" font-weight:600;\">wtfigo.png</span></p></body></html>"))
        self.lineEditOutName.setText(_translate("rbhusSubmit", "default"))
        self.labelBatching.setText(_translate("rbhusSubmit", "batching"))
        self.afterTimeEdit.setDisplayFormat(_translate("rbhusSubmit", "yyyy-M-d h:mm A"))
        self.pushSelectHostGroups.setText(_translate("rbhusSubmit", "select"))
        self.lineEditHostGroups.setToolTip(_translate("rbhusSubmit", "comma seperated list of cameras to render"))
        self.lineEditHostGroups.setText(_translate("rbhusSubmit", "default"))
        self.lineEditDescription.setText(_translate("rbhusSubmit", "default"))
        self.labelPrio.setText(_translate("rbhusSubmit", "priority"))
        self.labelImageName.setText(_translate("rbhusSubmit", "outName"))
        self.checkExrMov.setText(_translate("rbhusSubmit", "convert exr to MOV"))
        self.labelMinBatch.setText(_translate("rbhusSubmit", "min"))
        self.labelMaxBatch.setText(_translate("rbhusSubmit", "max"))
        self.lineEditFileName.setWhatsThis(_translate("rbhusSubmit", "comma seperated list of files to render"))
        self.labelFrange.setText(_translate("rbhusSubmit", "fRange     "))
        self.pushSubmit.setText(_translate("rbhusSubmit", "submit"))
        self.lineEditRes.setWhatsThis(_translate("rbhusSubmit", "<html><head/><body><p>frame range in the format</p><p>startframe-endframe:byframes</p><p>eg:</p><p>render frames from 1 to 100     : <span style=\" font-weight:600;\">1-100</span></p><p>render every 5th frame from 1 to 100     : <span style=\" font-weight:600;\">1-100:5</span></p><p>render 1 frame         :<span style=\" font-weight:600;\"> 1</span></p><p><br/></p><p><br/></p></body></html>"))
        self.lineEditRes.setText(_translate("rbhusSubmit", "default"))
        self.lineEditLayer.setText(_translate("rbhusSubmit", "default"))
        self.labelUser.setText(_translate("rbhusSubmit", "TextLabel"))
        self.checkAfterTime.setText(_translate("rbhusSubmit", "enable"))
        self.labelOsType.setText(_translate("rbhusSubmit", "osType"))
        self.labelLayer.setText(_translate("rbhusSubmit", "layers"))
        self.checkPngMov.setText(_translate("rbhusSubmit", "convert png to MOV"))
        self.labelDescription.setText(_translate("rbhusSubmit", "description"))
        self.comboPrio.setItemText(0, _translate("rbhusSubmit", "normal"))
        self.comboPrio.setItemText(1, _translate("rbhusSubmit", "low"))
        self.comboPrio.setItemText(2, _translate("rbhusSubmit", "high"))
        self.lineEditAfterTask.setText(_translate("rbhusSubmit", "0"))
        self.labelFileName.setText(_translate("rbhusSubmit", "fileName"))
        self.labelAfterTask.setText(_translate("rbhusSubmit", "afterTasks"))
        self.labelAfterTime.setText(_translate("rbhusSubmit", "afterTime "))
        self.labelImageType.setText(_translate("rbhusSubmit", "imageType"))
        self.labelResolution.setText(_translate("rbhusSubmit", "resolution"))
        self.lineEditFrange.setWhatsThis(_translate("rbhusSubmit", "<html><head/><body><p>frame range in the format</p><p>startframe-endframe:byframes</p><p>eg:</p><p>render frames from 1 to 100     : <span style=\" font-weight:600;\">1-100</span></p><p>render every 5th frame from 1 to 100     : <span style=\" font-weight:600;\">1-100:5</span></p><p>render 1 frame         :<span style=\" font-weight:600;\"> 1</span></p><p><br/></p><p><br/></p></body></html>"))
        self.lineEditFrange.setText(_translate("rbhusSubmit", "1"))
        self.checkSloppy.setText(_translate("rbhusSubmit", "sloppy"))
        self.labelCamera.setText(_translate("rbhusSubmit", "cameras"))
        self.label.setText(_translate("rbhusSubmit", "USER"))
        self.checkBatching.setText(_translate("rbhusSubmit", "enable"))
        self.labeFileType.setText(_translate("rbhusSubmit", "fileType"))
        self.checkHold.setToolTip(_translate("rbhusSubmit", "Submit , but put the task on hold"))
        self.checkHold.setText(_translate("rbhusSubmit", "deactivate"))
        self.labeRenderer.setText(_translate("rbhusSubmit", "renderer"))
        self.labelHostGroup.setText(_translate("rbhusSubmit", "hostGroup"))
        self.lineEditCameras.setToolTip(_translate("rbhusSubmit", "comma seperated list of cameras to render"))
        self.lineEditCameras.setText(_translate("rbhusSubmit", "default"))
        self.labelOutDir.setText(_translate("rbhusSubmit", "outDir"))
        self.lineEditOutDir.setWhatsThis(_translate("rbhusSubmit", "output directory to dump files"))
        self.lineEditOutDir.setText(_translate("rbhusSubmit", "default"))
        self.pushOutDir.setText(_translate("rbhusSubmit", "open"))
