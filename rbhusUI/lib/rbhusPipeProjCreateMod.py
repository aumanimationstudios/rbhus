# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rbhusPipeProjCreateMod.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(420, 335)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.labelDesc = QtWidgets.QLabel(self.centralwidget)
        self.labelDesc.setObjectName("labelDesc")
        self.gridLayout.addWidget(self.labelDesc, 8, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 10, 0, 1, 2)
        self.labelDue = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelDue.sizePolicy().hasHeightForWidth())
        self.labelDue.setSizePolicy(sizePolicy)
        self.labelDue.setObjectName("labelDue")
        self.gridLayout.addWidget(self.labelDue, 4, 0, 1, 1)
        self.checkRI = QtWidgets.QCheckBox(self.centralwidget)
        self.checkRI.setEnabled(False)
        self.checkRI.setChecked(True)
        self.checkRI.setObjectName("checkRI")
        self.gridLayout.addWidget(self.checkRI, 13, 0, 1, 3)
        self.labelProj_2 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelProj_2.sizePolicy().hasHeightForWidth())
        self.labelProj_2.setSizePolicy(sizePolicy)
        self.labelProj_2.setObjectName("labelProj_2")
        self.gridLayout.addWidget(self.labelProj_2, 0, 0, 1, 1)
        self.labelName = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelName.sizePolicy().hasHeightForWidth())
        self.labelName.setSizePolicy(sizePolicy)
        self.labelName.setObjectName("labelName")
        self.gridLayout.addWidget(self.labelName, 1, 0, 1, 1)
        self.labelAclGroup = QtWidgets.QLabel(self.centralwidget)
        self.labelAclGroup.setObjectName("labelAclGroup")
        self.gridLayout.addWidget(self.labelAclGroup, 7, 0, 1, 1)
        self.labelAdmin = QtWidgets.QLabel(self.centralwidget)
        self.labelAdmin.setObjectName("labelAdmin")
        self.gridLayout.addWidget(self.labelAdmin, 5, 0, 1, 1)
        self.labelDirectory = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelDirectory.sizePolicy().hasHeightForWidth())
        self.labelDirectory.setSizePolicy(sizePolicy)
        self.labelDirectory.setObjectName("labelDirectory")
        self.gridLayout.addWidget(self.labelDirectory, 2, 0, 1, 1)
        self.labelAclUser = QtWidgets.QLabel(self.centralwidget)
        self.labelAclUser.setObjectName("labelAclUser")
        self.gridLayout.addWidget(self.labelAclUser, 6, 0, 1, 1)
        self.labelLinked = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelLinked.sizePolicy().hasHeightForWidth())
        self.labelLinked.setSizePolicy(sizePolicy)
        self.labelLinked.setObjectName("labelLinked")
        self.gridLayout.addWidget(self.labelLinked, 9, 0, 1, 1)
        self.lineEditLinked = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditLinked.setObjectName("lineEditLinked")
        self.gridLayout.addWidget(self.lineEditLinked, 9, 1, 1, 1)
        self.pushLinked = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushLinked.sizePolicy().hasHeightForWidth())
        self.pushLinked.setSizePolicy(sizePolicy)
        self.pushLinked.setObjectName("pushLinked")
        self.gridLayout.addWidget(self.pushLinked, 9, 2, 1, 1)
        self.lineEditDesc = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditDesc.setText("")
        self.lineEditDesc.setObjectName("lineEditDesc")
        self.gridLayout.addWidget(self.lineEditDesc, 8, 1, 1, 2)
        self.lineEditAclGroup = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditAclGroup.setEnabled(False)
        self.lineEditAclGroup.setObjectName("lineEditAclGroup")
        self.gridLayout.addWidget(self.lineEditAclGroup, 7, 1, 1, 2)
        self.lineEditAclUser = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditAclUser.setEnabled(False)
        self.lineEditAclUser.setObjectName("lineEditAclUser")
        self.gridLayout.addWidget(self.lineEditAclUser, 6, 1, 1, 2)
        self.dateEditDue = QtWidgets.QDateTimeEdit(self.centralwidget)
        self.dateEditDue.setCalendarPopup(True)
        self.dateEditDue.setObjectName("dateEditDue")
        self.gridLayout.addWidget(self.dateEditDue, 4, 1, 1, 2)
        self.comboDirectory = QtWidgets.QComboBox(self.centralwidget)
        self.comboDirectory.setObjectName("comboDirectory")
        self.gridLayout.addWidget(self.comboDirectory, 2, 1, 1, 2)
        self.lineEditName = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditName.setObjectName("lineEditName")
        self.gridLayout.addWidget(self.lineEditName, 1, 1, 1, 2)
        self.comboProjType = QtWidgets.QComboBox(self.centralwidget)
        self.comboProjType.setObjectName("comboProjType")
        self.gridLayout.addWidget(self.comboProjType, 0, 1, 1, 2)
        self.line = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 11, 0, 1, 3)
        self.pushCreate = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushCreate.sizePolicy().hasHeightForWidth())
        self.pushCreate.setSizePolicy(sizePolicy)
        self.pushCreate.setObjectName("pushCreate")
        self.gridLayout.addWidget(self.pushCreate, 14, 0, 1, 3)
        self.lineEditAdmins = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditAdmins.setObjectName("lineEditAdmins")
        self.gridLayout.addWidget(self.lineEditAdmins, 5, 1, 1, 1)
        self.pushUsers = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushUsers.sizePolicy().hasHeightForWidth())
        self.pushUsers.setSizePolicy(sizePolicy)
        self.pushUsers.setObjectName("pushUsers")
        self.gridLayout.addWidget(self.pushUsers, 5, 2, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Rbhus Pipe NEW PROJECT"))
        self.labelDesc.setToolTip(_translate("MainWindow", "group owner of the project directory"))
        self.labelDesc.setText(_translate("MainWindow", "description"))
        self.labelDue.setText(_translate("MainWindow", "due date"))
        self.checkRI.setText(_translate("MainWindow", "rbhusRender intergration"))
        self.labelProj_2.setText(_translate("MainWindow", "projType"))
        self.labelName.setText(_translate("MainWindow", "name"))
        self.labelAclGroup.setToolTip(_translate("MainWindow", "group owner of the project directory"))
        self.labelAclGroup.setText(_translate("MainWindow", "aclGroup"))
        self.labelAdmin.setText(_translate("MainWindow", "admins"))
        self.labelDirectory.setWhatsThis(_translate("MainWindow", "directory to store the output data from file. eg : rendered output of lighting files."))
        self.labelDirectory.setText(_translate("MainWindow", "directory"))
        self.labelAclUser.setToolTip(_translate("MainWindow", "user owner of the project directory"))
        self.labelAclUser.setText(_translate("MainWindow", "aclUser"))
        self.labelLinked.setText(_translate("MainWindow", "linked"))
        self.lineEditLinked.setText(_translate("MainWindow", "default"))
        self.pushLinked.setText(_translate("MainWindow", "select"))
        self.lineEditDesc.setToolTip(_translate("MainWindow", "group owner of the project directory"))
        self.lineEditAclGroup.setToolTip(_translate("MainWindow", "group owner of the project directory"))
        self.lineEditAclGroup.setText(_translate("MainWindow", "artist"))
        self.lineEditAclUser.setToolTip(_translate("MainWindow", "user owner of the project directory"))
        self.lineEditAclUser.setText(_translate("MainWindow", "kryptos"))
        self.pushCreate.setText(_translate("MainWindow", "create"))
        self.lineEditAdmins.setToolTip(_translate("MainWindow", "list of comma separated usernames"))
        self.pushUsers.setText(_translate("MainWindow", "select"))
