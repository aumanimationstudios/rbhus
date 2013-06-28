# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rbhusTextReadMod.ui'
#
# Created: Sat Jun 29 00:00:34 2013
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

class Ui_readText(object):
  def setupUi(self, readText):
    readText.setObjectName(_fromUtf8("readText"))
    readText.resize(800, 600)
    self.centralwidget = QtGui.QWidget(readText)
    self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
    self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
    self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
    self.plainTextEdit = QtGui.QPlainTextEdit(self.centralwidget)
    self.plainTextEdit.setObjectName(_fromUtf8("plainTextEdit"))
    self.verticalLayout.addWidget(self.plainTextEdit)
    self.checkRefresh = QtGui.QCheckBox(self.centralwidget)
    self.checkRefresh.setObjectName(_fromUtf8("checkRefresh"))
    self.verticalLayout.addWidget(self.checkRefresh)
    readText.setCentralWidget(self.centralwidget)
    self.menubar = QtGui.QMenuBar(readText)
    self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
    self.menubar.setObjectName(_fromUtf8("menubar"))
    readText.setMenuBar(self.menubar)
    self.statusbar = QtGui.QStatusBar(readText)
    self.statusbar.setObjectName(_fromUtf8("statusbar"))
    readText.setStatusBar(self.statusbar)

    self.retranslateUi(readText)
    QtCore.QMetaObject.connectSlotsByName(readText)

  def retranslateUi(self, readText):
    readText.setWindowTitle(_translate("readText", "MainWindow", None))
    self.checkRefresh.setText(_translate("readText", "autoRefresh", None))

