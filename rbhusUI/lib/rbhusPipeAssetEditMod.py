# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rbhusPipeAssetEditMod.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(441, 361)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(1, 1, 1, 1)
        self.gridLayout.setObjectName("gridLayout")
        self.checkDueDate = QtWidgets.QCheckBox(self.centralwidget)
        self.checkDueDate.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkDueDate.sizePolicy().hasHeightForWidth())
        self.checkDueDate.setSizePolicy(sizePolicy)
        self.checkDueDate.setText("")
        self.checkDueDate.setChecked(False)
        self.checkDueDate.setObjectName("checkDueDate")
        self.gridLayout.addWidget(self.checkDueDate, 4, 7, 1, 1)
        self.labelDesc = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelDesc.sizePolicy().hasHeightForWidth())
        self.labelDesc.setSizePolicy(sizePolicy)
        self.labelDesc.setObjectName("labelDesc")
        self.gridLayout.addWidget(self.labelDesc, 9, 0, 1, 1)
        self.checkVersion = QtWidgets.QCheckBox(self.centralwidget)
        self.checkVersion.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkVersion.sizePolicy().hasHeightForWidth())
        self.checkVersion.setSizePolicy(sizePolicy)
        self.checkVersion.setText("")
        self.checkVersion.setChecked(False)
        self.checkVersion.setObjectName("checkVersion")
        self.gridLayout.addWidget(self.checkVersion, 13, 7, 1, 1)
        self.checkDesc = QtWidgets.QCheckBox(self.centralwidget)
        self.checkDesc.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkDesc.sizePolicy().hasHeightForWidth())
        self.checkDesc.setSizePolicy(sizePolicy)
        self.checkDesc.setText("")
        self.checkDesc.setChecked(False)
        self.checkDesc.setObjectName("checkDesc")
        self.gridLayout.addWidget(self.checkDesc, 9, 7, 1, 1)
        self.labelAssignTo = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelAssignTo.sizePolicy().hasHeightForWidth())
        self.labelAssignTo.setSizePolicy(sizePolicy)
        self.labelAssignTo.setObjectName("labelAssignTo")
        self.gridLayout.addWidget(self.labelAssignTo, 6, 0, 1, 1)
        self.pushReviewers = QtWidgets.QPushButton(self.centralwidget)
        self.pushReviewers.setEnabled(True)
        self.pushReviewers.setObjectName("pushReviewers")
        self.gridLayout.addWidget(self.pushReviewers, 7, 6, 1, 1)
        self.pushTags = QtWidgets.QPushButton(self.centralwidget)
        self.pushTags.setObjectName("pushTags")
        self.gridLayout.addWidget(self.pushTags, 12, 6, 1, 1)
        self.pushUsers = QtWidgets.QPushButton(self.centralwidget)
        self.pushUsers.setObjectName("pushUsers")
        self.gridLayout.addWidget(self.pushUsers, 6, 6, 1, 1)
        self.checkReview = QtWidgets.QCheckBox(self.centralwidget)
        self.checkReview.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkReview.sizePolicy().hasHeightForWidth())
        self.checkReview.setSizePolicy(sizePolicy)
        self.checkReview.setText("")
        self.checkReview.setChecked(False)
        self.checkReview.setObjectName("checkReview")
        self.gridLayout.addWidget(self.checkReview, 7, 7, 1, 1)
        self.labelReview = QtWidgets.QLabel(self.centralwidget)
        self.labelReview.setObjectName("labelReview")
        self.gridLayout.addWidget(self.labelReview, 7, 0, 1, 1)
        self.lineEditWorkers = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditWorkers.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditWorkers.sizePolicy().hasHeightForWidth())
        self.lineEditWorkers.setSizePolicy(sizePolicy)
        self.lineEditWorkers.setObjectName("lineEditWorkers")
        self.gridLayout.addWidget(self.lineEditWorkers, 6, 1, 1, 4)
        self.checkVersionEnable = QtWidgets.QCheckBox(self.centralwidget)
        self.checkVersionEnable.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkVersionEnable.sizePolicy().hasHeightForWidth())
        self.checkVersionEnable.setSizePolicy(sizePolicy)
        self.checkVersionEnable.setText("")
        self.checkVersionEnable.setChecked(False)
        self.checkVersionEnable.setObjectName("checkVersionEnable")
        self.gridLayout.addWidget(self.checkVersionEnable, 13, 1, 1, 1)
        self.labelVersion = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelVersion.sizePolicy().hasHeightForWidth())
        self.labelVersion.setSizePolicy(sizePolicy)
        self.labelVersion.setObjectName("labelVersion")
        self.gridLayout.addWidget(self.labelVersion, 13, 0, 1, 1)
        self.checkReviewSelf = QtWidgets.QCheckBox(self.centralwidget)
        self.checkReviewSelf.setChecked(False)
        self.checkReviewSelf.setObjectName("checkReviewSelf")
        self.gridLayout.addWidget(self.checkReviewSelf, 7, 5, 1, 1)
        self.checkAssign = QtWidgets.QCheckBox(self.centralwidget)
        self.checkAssign.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkAssign.sizePolicy().hasHeightForWidth())
        self.checkAssign.setSizePolicy(sizePolicy)
        self.checkAssign.setText("")
        self.checkAssign.setChecked(False)
        self.checkAssign.setObjectName("checkAssign")
        self.gridLayout.addWidget(self.checkAssign, 6, 7, 1, 1)
        self.checkFRange = QtWidgets.QCheckBox(self.centralwidget)
        self.checkFRange.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkFRange.sizePolicy().hasHeightForWidth())
        self.checkFRange.setSizePolicy(sizePolicy)
        self.checkFRange.setText("")
        self.checkFRange.setChecked(False)
        self.checkFRange.setObjectName("checkFRange")
        self.gridLayout.addWidget(self.checkFRange, 2, 7, 1, 1)
        self.labelFRange = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelFRange.sizePolicy().hasHeightForWidth())
        self.labelFRange.setSizePolicy(sizePolicy)
        self.labelFRange.setObjectName("labelFRange")
        self.gridLayout.addWidget(self.labelFRange, 2, 0, 1, 1)
        self.checkTags = QtWidgets.QCheckBox(self.centralwidget)
        self.checkTags.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkTags.sizePolicy().hasHeightForWidth())
        self.checkTags.setSizePolicy(sizePolicy)
        self.checkTags.setText("")
        self.checkTags.setChecked(False)
        self.checkTags.setObjectName("checkTags")
        self.gridLayout.addWidget(self.checkTags, 12, 7, 1, 1)
        self.labelDue = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelDue.sizePolicy().hasHeightForWidth())
        self.labelDue.setSizePolicy(sizePolicy)
        self.labelDue.setObjectName("labelDue")
        self.gridLayout.addWidget(self.labelDue, 4, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 14, 0, 1, 7)
        self.lineEditTags = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditTags.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditTags.sizePolicy().hasHeightForWidth())
        self.lineEditTags.setSizePolicy(sizePolicy)
        self.lineEditTags.setObjectName("lineEditTags")
        self.gridLayout.addWidget(self.lineEditTags, 12, 1, 1, 5)
        self.checkAssignSelf = QtWidgets.QCheckBox(self.centralwidget)
        self.checkAssignSelf.setChecked(False)
        self.checkAssignSelf.setObjectName("checkAssignSelf")
        self.gridLayout.addWidget(self.checkAssignSelf, 6, 5, 1, 1)
        self.labelTags = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelTags.sizePolicy().hasHeightForWidth())
        self.labelTags.setSizePolicy(sizePolicy)
        self.labelTags.setObjectName("labelTags")
        self.gridLayout.addWidget(self.labelTags, 12, 0, 1, 1)
        self.lineEditDesc = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditDesc.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditDesc.sizePolicy().hasHeightForWidth())
        self.lineEditDesc.setSizePolicy(sizePolicy)
        self.lineEditDesc.setText("")
        self.lineEditDesc.setObjectName("lineEditDesc")
        self.gridLayout.addWidget(self.lineEditDesc, 9, 1, 1, 5)
        self.lineEditReviewers = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditReviewers.setEnabled(False)
        self.lineEditReviewers.setReadOnly(True)
        self.lineEditReviewers.setObjectName("lineEditReviewers")
        self.gridLayout.addWidget(self.lineEditReviewers, 7, 1, 1, 4)
        self.lineEditFRange = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditFRange.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditFRange.sizePolicy().hasHeightForWidth())
        self.lineEditFRange.setSizePolicy(sizePolicy)
        self.lineEditFRange.setObjectName("lineEditFRange")
        self.gridLayout.addWidget(self.lineEditFRange, 2, 1, 1, 6)
        self.dateEditDue = QtWidgets.QDateTimeEdit(self.centralwidget)
        self.dateEditDue.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dateEditDue.sizePolicy().hasHeightForWidth())
        self.dateEditDue.setSizePolicy(sizePolicy)
        self.dateEditDue.setCalendarPopup(True)
        self.dateEditDue.setObjectName("dateEditDue")
        self.gridLayout.addWidget(self.dateEditDue, 4, 1, 1, 6)
        self.pushEdit = QtWidgets.QPushButton(self.centralwidget)
        self.pushEdit.setObjectName("pushEdit")
        self.gridLayout.addWidget(self.pushEdit, 16, 0, 1, 8)
        self.line = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 15, 0, 1, 8)
        self.labelReviewNotify = QtWidgets.QLabel(self.centralwidget)
        self.labelReviewNotify.setObjectName("labelReviewNotify")
        self.gridLayout.addWidget(self.labelReviewNotify, 8, 0, 1, 1)
        self.lineEditReviewNotifiers = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditReviewNotifiers.setEnabled(False)
        self.lineEditReviewNotifiers.setReadOnly(True)
        self.lineEditReviewNotifiers.setObjectName("lineEditReviewNotifiers")
        self.gridLayout.addWidget(self.lineEditReviewNotifiers, 8, 1, 1, 5)
        self.pushReviewNotifiers = QtWidgets.QPushButton(self.centralwidget)
        self.pushReviewNotifiers.setEnabled(True)
        self.pushReviewNotifiers.setObjectName("pushReviewNotifiers")
        self.gridLayout.addWidget(self.pushReviewNotifiers, 8, 6, 1, 1)
        self.checkReviewNotifiers = QtWidgets.QCheckBox(self.centralwidget)
        self.checkReviewNotifiers.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkReviewNotifiers.sizePolicy().hasHeightForWidth())
        self.checkReviewNotifiers.setSizePolicy(sizePolicy)
        self.checkReviewNotifiers.setText("")
        self.checkReviewNotifiers.setChecked(False)
        self.checkReviewNotifiers.setObjectName("checkReviewNotifiers")
        self.gridLayout.addWidget(self.checkReviewNotifiers, 8, 7, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Edit Asset"))
        self.labelDesc.setToolTip(_translate("MainWindow", "group owner of the project directory"))
        self.labelDesc.setText(_translate("MainWindow", "description"))
        self.labelAssignTo.setText(_translate("MainWindow", "assign to"))
        self.pushReviewers.setText(_translate("MainWindow", "select"))
        self.pushTags.setText(_translate("MainWindow", "select"))
        self.pushUsers.setText(_translate("MainWindow", "select"))
        self.labelReview.setText(_translate("MainWindow", "reviewer"))
        self.lineEditWorkers.setToolTip(_translate("MainWindow", "list of space separated usernames"))
        self.lineEditWorkers.setText(_translate("MainWindow", "default"))
        self.labelVersion.setToolTip(_translate("MainWindow", "group owner of the project directory"))
        self.labelVersion.setText(_translate("MainWindow", "versioning"))
        self.checkReviewSelf.setText(_translate("MainWindow", "self"))
        self.labelFRange.setText(_translate("MainWindow", "fRange"))
        self.labelDue.setText(_translate("MainWindow", "due date"))
        self.lineEditTags.setToolTip(_translate("MainWindow", "group owner of the project directory"))
        self.lineEditTags.setText(_translate("MainWindow", "default"))
        self.checkAssignSelf.setText(_translate("MainWindow", "self"))
        self.labelTags.setToolTip(_translate("MainWindow", "group owner of the project directory"))
        self.labelTags.setText(_translate("MainWindow", "tags"))
        self.lineEditDesc.setToolTip(_translate("MainWindow", "group owner of the project directory"))
        self.lineEditReviewers.setToolTip(_translate("MainWindow", "list of space separated usernames"))
        self.lineEditReviewers.setText(_translate("MainWindow", "default"))
        self.lineEditFRange.setText(_translate("MainWindow", "1"))
        self.pushEdit.setText(_translate("MainWindow", "edit"))
        self.labelReviewNotify.setText(_translate("MainWindow", "review notify users"))
        self.lineEditReviewNotifiers.setToolTip(_translate("MainWindow", "list of space separated usernames"))
        self.lineEditReviewNotifiers.setText(_translate("MainWindow", "default"))
        self.pushReviewNotifiers.setText(_translate("MainWindow", "select"))
