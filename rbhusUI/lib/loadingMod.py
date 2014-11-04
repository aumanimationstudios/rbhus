# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'loadingMod.ui'
#
# Created: Sun Nov  2 19:21:09 2014
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

class Ui_loading(object):
  def setupUi(self, loading):
    loading.setObjectName(_fromUtf8("loading"))
    loading.setWindowModality(QtCore.Qt.WindowModal)
    loading.resize(400, 31)
    self.gridLayout = QtGui.QGridLayout(loading)
    self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
    self.progressBar = QtGui.QProgressBar(loading)
    self.progressBar.setProperty("value", 24)
    self.progressBar.setObjectName(_fromUtf8("progressBar"))
    self.gridLayout.addWidget(self.progressBar, 0, 0, 1, 1)

    self.retranslateUi(loading)
    QtCore.QMetaObject.connectSlotsByName(loading)

  def retranslateUi(self, loading):
    loading.setWindowTitle(_translate("loading", "in progress", None))

