#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'templateUI.ui'
#
# Created: Thu Dec 16 18:56:09 2010
#      by: PyQt4 UI code generator 4.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtWidgets, QtCore, QtGui
import glob
import os
import re

try:
  _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
  _fromUtf8 = lambda s: s

class Ui_Form(object):
  def setupUi(self, Form):
    Form.setObjectName(_fromUtf8("Form"))
    Form.resize(519, 171)
    self.center()
    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
    Form.setSizePolicy(sizePolicy)
    self.gridlayout = QtWidgets.QGridLayout(Form)
    self.gridlayout.setMargin(9)
    self.gridlayout.setSpacing(6)
    self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
    self.listWidget = QtWidgets.QListWidget(Form)
    self.listWidget.setObjectName(_fromUtf8("listWidget"))
    self.gridlayout.addWidget(self.listWidget, 0, 0, 1, 1)
    self.getFiles()
    self.listWidget.sortItems()
    self.retranslateUi(Form)
    QtCore.QObject.connect(self.listWidget, QtCore.SIGNAL(_fromUtf8("doubleClicked(QModelIndex)")), self.printSelected)
    QtCore.QMetaObject.connectSlotsByName(Form)


  def retranslateUi(self, Form):
    Form.setWindowTitle(QtWidgets.QApplication.translate("Form", sys.argv[1], None, QtWidgets.QApplication.UnicodeUTF8))
    self.listWidget.setSortingEnabled(True)
    
    
  def printSelected(self):
    fRelative = str(self.listWidget.currentItem().text())
    fAbs = os.path.abspath(sys.argv[1].rstrip("/"))
    print(fAbs +"/"+ fRelative)
    Form.close()
    
    
  def getFiles(self):
    files = glob.glob(sys.argv[1].rstrip("/") +"/*")
    if(files):
      for f in files:
        if(os.path.isfile(f)):
          if(not f.endswith("~")):
            fS = QtWidgets.QListWidgetItem(_fromUtf8(f.split("/")[-1]))
            self.listWidget.addItem(fS)
      
      
  def center(self):
    screen = QtWidgets.QDesktopWidget().screenGeometry()
    size =  Form.geometry()
    Form.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)
      
    
  

if __name__ == "__main__":
  import sys
  app = QtWidgets.QApplication(sys.argv)
  Form = QtWidgets.QWidget()
  ui = Ui_Form()
  ui.setupUi(Form)
  Form.show()
  sys.exit(app.exec_())

