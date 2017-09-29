# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rbhusPipeVersionsMod.ui'
#
# Created by: PyQt4 UI code generator 4.12
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
    MainWindow.resize(669, 678)
    self.centralwidget = QtGui.QWidget(MainWindow)
    self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
    self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
    self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
    self.splitter = QtGui.QSplitter(self.centralwidget)
    self.splitter.setOrientation(QtCore.Qt.Vertical)
    self.splitter.setObjectName(_fromUtf8("splitter"))
    self.groupVersions = QtGui.QGroupBox(self.splitter)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.MinimumExpanding)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.groupVersions.sizePolicy().hasHeightForWidth())
    self.groupVersions.setSizePolicy(sizePolicy)
    self.groupVersions.setObjectName(_fromUtf8("groupVersions"))
    self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupVersions)
    self.verticalLayout_2.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
    self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
    self.tableVersions = QtGui.QTableWidget(self.groupVersions)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.tableVersions.sizePolicy().hasHeightForWidth())
    self.tableVersions.setSizePolicy(sizePolicy)
    self.tableVersions.setMouseTracking(True)
    self.tableVersions.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
    self.tableVersions.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
    self.tableVersions.setObjectName(_fromUtf8("tableVersions"))
    self.tableVersions.setColumnCount(0)
    self.tableVersions.setRowCount(0)
    self.tableVersions.horizontalHeader().setVisible(False)
    self.tableVersions.horizontalHeader().setCascadingSectionResizes(False)
    self.tableVersions.horizontalHeader().setDefaultSectionSize(10)
    self.tableVersions.horizontalHeader().setHighlightSections(False)
    self.tableVersions.horizontalHeader().setMinimumSectionSize(5)
    self.tableVersions.horizontalHeader().setSortIndicatorShown(False)
    self.tableVersions.horizontalHeader().setStretchLastSection(True)
    self.tableVersions.verticalHeader().setVisible(False)
    self.verticalLayout_2.addWidget(self.tableVersions)
    self.groupBox = QtGui.QGroupBox(self.splitter)
    self.groupBox.setObjectName(_fromUtf8("groupBox"))
    self.verticalLayout_3 = QtGui.QVBoxLayout(self.groupBox)
    self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
    self.listWidget = QtGui.QListWidget(self.groupBox)
    self.listWidget.setObjectName(_fromUtf8("listWidget"))
    self.verticalLayout_3.addWidget(self.listWidget)
    self.verticalLayout.addWidget(self.splitter)
    self.horizontalLayout = QtGui.QHBoxLayout()
    self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
    self.pushWork = QtGui.QPushButton(self.centralwidget)
    self.pushWork.setObjectName(_fromUtf8("pushWork"))
    self.horizontalLayout.addWidget(self.pushWork)
    self.pushReInit = QtGui.QPushButton(self.centralwidget)
    self.pushReInit.setObjectName(_fromUtf8("pushReInit"))
    self.horizontalLayout.addWidget(self.pushReInit)
    self.pushCommit = QtGui.QPushButton(self.centralwidget)
    self.pushCommit.setObjectName(_fromUtf8("pushCommit"))
    self.horizontalLayout.addWidget(self.pushCommit)
    self.toolButton = QtGui.QToolButton(self.centralwidget)
    self.toolButton.setPopupMode(QtGui.QToolButton.InstantPopup)
    self.toolButton.setAutoRaise(False)
    self.toolButton.setArrowType(QtCore.Qt.RightArrow)
    self.toolButton.setObjectName(_fromUtf8("toolButton"))
    self.horizontalLayout.addWidget(self.toolButton)
    self.verticalLayout.addLayout(self.horizontalLayout)
    MainWindow.setCentralWidget(self.centralwidget)
    self.statusbar = QtGui.QStatusBar(MainWindow)
    self.statusbar.setObjectName(_fromUtf8("statusbar"))
    MainWindow.setStatusBar(self.statusbar)

    self.retranslateUi(MainWindow)
    QtCore.QMetaObject.connectSlotsByName(MainWindow)

  def retranslateUi(self, MainWindow):
    MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
    self.groupVersions.setTitle(_translate("MainWindow", "versions", None))
    self.tableVersions.setSortingEnabled(True)
    self.groupBox.setToolTip(_translate("MainWindow", "Check to auto commit everytime u commit this asset. Will work only if the respected asset is ASSIGNED to you", None))
    self.groupBox.setTitle(_translate("MainWindow", "Related Assets ", None))
    self.pushWork.setText(_translate("MainWindow", "open", None))
    self.pushReInit.setText(_translate("MainWindow", "re-initialize", None))
    self.pushCommit.setText(_translate("MainWindow", "commit", None))
    self.toolButton.setText(_translate("MainWindow", "...", None))

