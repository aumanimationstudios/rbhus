# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'lib/rbhusEditMod.ui'
#
# Created: Sat Jul 28 22:22:21 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_rbhusEdit(object):
    def setupUi(self, rbhusEdit):
        rbhusEdit.setObjectName(_fromUtf8("rbhusEdit"))
        rbhusEdit.resize(714, 575)
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
        self.gridLayout_2.addWidget(self.afterTimeEdit, 8, 1, 1, 1)
        self.labelOutPutDir = QtGui.QLabel(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelOutPutDir.sizePolicy().hasHeightForWidth())
        self.labelOutPutDir.setSizePolicy(sizePolicy)
        self.labelOutPutDir.setObjectName(_fromUtf8("labelOutPutDir"))
        self.gridLayout_2.addWidget(self.labelOutPutDir, 1, 0, 1, 1)
        self.pushOutPutDir = QtGui.QPushButton(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushOutPutDir.sizePolicy().hasHeightForWidth())
        self.pushOutPutDir.setSizePolicy(sizePolicy)
        self.pushOutPutDir.setObjectName(_fromUtf8("pushOutPutDir"))
        self.gridLayout_2.addWidget(self.pushOutPutDir, 1, 2, 1, 1)
        self.lineEditAfc = QtGui.QLineEdit(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditAfc.sizePolicy().hasHeightForWidth())
        self.lineEditAfc.setSizePolicy(sizePolicy)
        self.lineEditAfc.setObjectName(_fromUtf8("lineEditAfc"))
        self.gridLayout_2.addWidget(self.lineEditAfc, 7, 1, 1, 1)
        self.lineEditLogbase = QtGui.QLineEdit(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditLogbase.sizePolicy().hasHeightForWidth())
        self.lineEditLogbase.setSizePolicy(sizePolicy)
        self.lineEditLogbase.setObjectName(_fromUtf8("lineEditLogbase"))
        self.gridLayout_2.addWidget(self.lineEditLogbase, 9, 1, 1, 1)
        self.comboType = QtGui.QComboBox(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboType.sizePolicy().hasHeightForWidth())
        self.comboType.setSizePolicy(sizePolicy)
        self.comboType.setObjectName(_fromUtf8("comboType"))
        self.gridLayout_2.addWidget(self.comboType, 3, 1, 1, 1)
        self.labelAfc = QtGui.QLabel(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelAfc.sizePolicy().hasHeightForWidth())
        self.labelAfc.setSizePolicy(sizePolicy)
        self.labelAfc.setObjectName(_fromUtf8("labelAfc"))
        self.gridLayout_2.addWidget(self.labelAfc, 7, 0, 1, 1)
        self.labelAfterTime = QtGui.QLabel(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelAfterTime.sizePolicy().hasHeightForWidth())
        self.labelAfterTime.setSizePolicy(sizePolicy)
        self.labelAfterTime.setObjectName(_fromUtf8("labelAfterTime"))
        self.gridLayout_2.addWidget(self.labelAfterTime, 8, 0, 1, 1)
        self.lineEditFileName = QtGui.QLineEdit(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditFileName.sizePolicy().hasHeightForWidth())
        self.lineEditFileName.setSizePolicy(sizePolicy)
        self.lineEditFileName.setDragEnabled(True)
        self.lineEditFileName.setObjectName(_fromUtf8("lineEditFileName"))
        self.gridLayout_2.addWidget(self.lineEditFileName, 0, 1, 1, 1)
        self.labelRerunThresh = QtGui.QLabel(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelRerunThresh.sizePolicy().hasHeightForWidth())
        self.labelRerunThresh.setSizePolicy(sizePolicy)
        self.labelRerunThresh.setObjectName(_fromUtf8("labelRerunThresh"))
        self.gridLayout_2.addWidget(self.labelRerunThresh, 10, 0, 1, 1)
        self.checkAfterTime = QtGui.QCheckBox(self.groupBox_2)
        self.checkAfterTime.setObjectName(_fromUtf8("checkAfterTime"))
        self.gridLayout_2.addWidget(self.checkAfterTime, 8, 2, 1, 1)
        self.comboHostGroup = QtGui.QComboBox(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboHostGroup.sizePolicy().hasHeightForWidth())
        self.comboHostGroup.setSizePolicy(sizePolicy)
        self.comboHostGroup.setObjectName(_fromUtf8("comboHostGroup"))
        self.gridLayout_2.addWidget(self.comboHostGroup, 4, 1, 1, 1)
        self.labelType = QtGui.QLabel(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelType.sizePolicy().hasHeightForWidth())
        self.labelType.setSizePolicy(sizePolicy)
        self.labelType.setObjectName(_fromUtf8("labelType"))
        self.gridLayout_2.addWidget(self.labelType, 3, 0, 1, 1)
        self.pushAfc = QtGui.QPushButton(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushAfc.sizePolicy().hasHeightForWidth())
        self.pushAfc.setSizePolicy(sizePolicy)
        self.pushAfc.setObjectName(_fromUtf8("pushAfc"))
        self.gridLayout_2.addWidget(self.pushAfc, 7, 2, 1, 1)
        self.lineEditBfc = QtGui.QLineEdit(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditBfc.sizePolicy().hasHeightForWidth())
        self.lineEditBfc.setSizePolicy(sizePolicy)
        self.lineEditBfc.setObjectName(_fromUtf8("lineEditBfc"))
        self.gridLayout_2.addWidget(self.lineEditBfc, 6, 1, 1, 1)
        self.labelHostGroup = QtGui.QLabel(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelHostGroup.sizePolicy().hasHeightForWidth())
        self.labelHostGroup.setSizePolicy(sizePolicy)
        self.labelHostGroup.setObjectName(_fromUtf8("labelHostGroup"))
        self.gridLayout_2.addWidget(self.labelHostGroup, 4, 0, 1, 1)
        self.pushLogOpen = QtGui.QPushButton(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushLogOpen.sizePolicy().hasHeightForWidth())
        self.pushLogOpen.setSizePolicy(sizePolicy)
        self.pushLogOpen.setObjectName(_fromUtf8("pushLogOpen"))
        self.gridLayout_2.addWidget(self.pushLogOpen, 9, 2, 1, 1)
        self.lineEditImageName = QtGui.QLineEdit(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditImageName.sizePolicy().hasHeightForWidth())
        self.lineEditImageName.setSizePolicy(sizePolicy)
        self.lineEditImageName.setObjectName(_fromUtf8("lineEditImageName"))
        self.gridLayout_2.addWidget(self.lineEditImageName, 2, 1, 1, 1)
        self.spinRerunThresh = QtGui.QSpinBox(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinRerunThresh.sizePolicy().hasHeightForWidth())
        self.spinRerunThresh.setSizePolicy(sizePolicy)
        self.spinRerunThresh.setObjectName(_fromUtf8("spinRerunThresh"))
        self.gridLayout_2.addWidget(self.spinRerunThresh, 10, 1, 1, 1)
        self.lineEditFrange = QtGui.QLineEdit(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditFrange.sizePolicy().hasHeightForWidth())
        self.lineEditFrange.setSizePolicy(sizePolicy)
        self.lineEditFrange.setObjectName(_fromUtf8("lineEditFrange"))
        self.gridLayout_2.addWidget(self.lineEditFrange, 5, 1, 1, 1)
        self.labelImageName = QtGui.QLabel(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelImageName.sizePolicy().hasHeightForWidth())
        self.labelImageName.setSizePolicy(sizePolicy)
        self.labelImageName.setObjectName(_fromUtf8("labelImageName"))
        self.gridLayout_2.addWidget(self.labelImageName, 2, 0, 1, 1)
        self.labelBfc = QtGui.QLabel(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelBfc.sizePolicy().hasHeightForWidth())
        self.labelBfc.setSizePolicy(sizePolicy)
        self.labelBfc.setObjectName(_fromUtf8("labelBfc"))
        self.gridLayout_2.addWidget(self.labelBfc, 6, 0, 1, 1)
        self.labelFrange = QtGui.QLabel(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelFrange.sizePolicy().hasHeightForWidth())
        self.labelFrange.setSizePolicy(sizePolicy)
        self.labelFrange.setObjectName(_fromUtf8("labelFrange"))
        self.gridLayout_2.addWidget(self.labelFrange, 5, 0, 1, 1)
        self.labelLogbase = QtGui.QLabel(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelLogbase.sizePolicy().hasHeightForWidth())
        self.labelLogbase.setSizePolicy(sizePolicy)
        self.labelLogbase.setObjectName(_fromUtf8("labelLogbase"))
        self.gridLayout_2.addWidget(self.labelLogbase, 9, 0, 1, 1)
        self.pushFileName = QtGui.QPushButton(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushFileName.sizePolicy().hasHeightForWidth())
        self.pushFileName.setSizePolicy(sizePolicy)
        self.pushFileName.setObjectName(_fromUtf8("pushFileName"))
        self.gridLayout_2.addWidget(self.pushFileName, 0, 2, 1, 1)
        self.labelFileName = QtGui.QLabel(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelFileName.sizePolicy().hasHeightForWidth())
        self.labelFileName.setSizePolicy(sizePolicy)
        self.labelFileName.setObjectName(_fromUtf8("labelFileName"))
        self.gridLayout_2.addWidget(self.labelFileName, 0, 0, 1, 1)
        self.lineEditOutPutDir = QtGui.QLineEdit(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditOutPutDir.sizePolicy().hasHeightForWidth())
        self.lineEditOutPutDir.setSizePolicy(sizePolicy)
        self.lineEditOutPutDir.setObjectName(_fromUtf8("lineEditOutPutDir"))
        self.gridLayout_2.addWidget(self.lineEditOutPutDir, 1, 1, 1, 1)
        self.pushBfc = QtGui.QPushButton(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushBfc.sizePolicy().hasHeightForWidth())
        self.pushBfc.setSizePolicy(sizePolicy)
        self.pushBfc.setObjectName(_fromUtf8("pushBfc"))
        self.gridLayout_2.addWidget(self.pushBfc, 6, 2, 1, 1)
        self.labelPriority = QtGui.QLabel(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelPriority.sizePolicy().hasHeightForWidth())
        self.labelPriority.setSizePolicy(sizePolicy)
        self.labelPriority.setObjectName(_fromUtf8("labelPriority"))
        self.gridLayout_2.addWidget(self.labelPriority, 11, 0, 1, 1)
        self.spinPriority = QtGui.QSpinBox(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinPriority.sizePolicy().hasHeightForWidth())
        self.spinPriority.setSizePolicy(sizePolicy)
        self.spinPriority.setMaximum(999999999)
        self.spinPriority.setObjectName(_fromUtf8("spinPriority"))
        self.gridLayout_2.addWidget(self.spinPriority, 11, 1, 1, 1)
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
        self.textEdit = QtGui.QTextEdit(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(195, 195, 195))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(195, 195, 195))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(244, 244, 244))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.textEdit.setPalette(palette)
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.textEdit.setFont(font)
        self.textEdit.setFrameShape(QtGui.QFrame.StyledPanel)
        self.textEdit.setFrameShadow(QtGui.QFrame.Raised)
        self.textEdit.setLineWidth(1)
        self.textEdit.setUndoRedoEnabled(False)
        self.textEdit.setReadOnly(True)
        self.textEdit.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.verticalLayout.addWidget(self.textEdit)
        rbhusEdit.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(rbhusEdit)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        rbhusEdit.setStatusBar(self.statusbar)

        self.retranslateUi(rbhusEdit)
        QtCore.QMetaObject.connectSlotsByName(rbhusEdit)

    def retranslateUi(self, rbhusEdit):
        rbhusEdit.setWindowTitle(QtGui.QApplication.translate("rbhusEdit", "rbhusEdit", None, QtGui.QApplication.UnicodeUTF8))
        self.afterTimeEdit.setDisplayFormat(QtGui.QApplication.translate("rbhusEdit", "yyyy-M-d h:mm A", None, QtGui.QApplication.UnicodeUTF8))
        self.labelOutPutDir.setText(QtGui.QApplication.translate("rbhusEdit", "outPutDir", None, QtGui.QApplication.UnicodeUTF8))
        self.pushOutPutDir.setText(QtGui.QApplication.translate("rbhusEdit", "open", None, QtGui.QApplication.UnicodeUTF8))
        self.labelAfc.setText(QtGui.QApplication.translate("rbhusEdit", "afc          ", None, QtGui.QApplication.UnicodeUTF8))
        self.labelAfterTime.setText(QtGui.QApplication.translate("rbhusEdit", "afterTime ", None, QtGui.QApplication.UnicodeUTF8))
        self.labelRerunThresh.setText(QtGui.QApplication.translate("rbhusEdit", "rerunThres", None, QtGui.QApplication.UnicodeUTF8))
        self.checkAfterTime.setText(QtGui.QApplication.translate("rbhusEdit", "enable", None, QtGui.QApplication.UnicodeUTF8))
        self.labelType.setText(QtGui.QApplication.translate("rbhusEdit", "type", None, QtGui.QApplication.UnicodeUTF8))
        self.pushAfc.setText(QtGui.QApplication.translate("rbhusEdit", "open", None, QtGui.QApplication.UnicodeUTF8))
        self.labelHostGroup.setText(QtGui.QApplication.translate("rbhusEdit", "hostGroup", None, QtGui.QApplication.UnicodeUTF8))
        self.pushLogOpen.setText(QtGui.QApplication.translate("rbhusEdit", "open", None, QtGui.QApplication.UnicodeUTF8))
        self.labelImageName.setText(QtGui.QApplication.translate("rbhusEdit", "imageName", None, QtGui.QApplication.UnicodeUTF8))
        self.labelBfc.setText(QtGui.QApplication.translate("rbhusEdit", "bfc          ", None, QtGui.QApplication.UnicodeUTF8))
        self.labelFrange.setText(QtGui.QApplication.translate("rbhusEdit", "fRange     ", None, QtGui.QApplication.UnicodeUTF8))
        self.labelLogbase.setText(QtGui.QApplication.translate("rbhusEdit", "logbase   ", None, QtGui.QApplication.UnicodeUTF8))
        self.pushFileName.setText(QtGui.QApplication.translate("rbhusEdit", "open", None, QtGui.QApplication.UnicodeUTF8))
        self.labelFileName.setText(QtGui.QApplication.translate("rbhusEdit", "fileName", None, QtGui.QApplication.UnicodeUTF8))
        self.pushBfc.setText(QtGui.QApplication.translate("rbhusEdit", "open", None, QtGui.QApplication.UnicodeUTF8))
        self.labelPriority.setText(QtGui.QApplication.translate("rbhusEdit", "priority", None, QtGui.QApplication.UnicodeUTF8))
        self.pushCancel.setText(QtGui.QApplication.translate("rbhusEdit", "cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.pushApply.setText(QtGui.QApplication.translate("rbhusEdit", "apply", None, QtGui.QApplication.UnicodeUTF8))
        self.textEdit.setHtml(QtGui.QApplication.translate("rbhusEdit", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:italic;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600; font-style:normal; color:#c00000;\">--HELP--</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-style:normal;\">bfc : beforeFrameCmd</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-style:normal;\">       These commands run before a frame starts</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-style:normal;\">afc : afterFrameCmd</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-style:normal;\">       These commands run after a frame completes</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-style:normal;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-style:normal;\">fRange : Frame Range</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-style:normal;\">             start-end:byframes</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-style:normal;\">             eg: if we want every 5th frame to render from 1 to 300 </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-style:normal;\">                   we can input 1-300:5 , </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-style:normal;\">             </span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

