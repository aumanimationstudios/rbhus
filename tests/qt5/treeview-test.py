#!/usr/bin/env python2
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys
import os

sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-1]))



# Form implementation generated from reading ui file 'treeview-test.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

import collections


basepath = os.path.abspath(sys.argv[1])
paths = os.walk(basepath)
pathDict = {}
for path in paths:
  pathDict[path[0]] = [os.path.join(path[0],subPath) for subPath in path[1]]

print(pathDict)

class Ui_Form(object):
  def setupUi(self, Form):
    Form.setObjectName("Form")
    Form.resize(400, 300)
    self.verticalLayout = QtWidgets.QVBoxLayout(Form)
    self.verticalLayout.setObjectName("verticalLayout")
    self.treeWidget = QtWidgets.QTreeWidget(Form)
    self.treeWidget.setObjectName("treeWidget")

    # item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
    #
    # for rootpath in rootpaths[1]:
    #   item = QtWidgets.QTreeWidgetItem(self.treeWidget)
    #   item.setText(0,rootpath)
    #   item.absPath =
    #


    # item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
    # item_1 = QtWidgets.QTreeWidgetItem(item_0)
    # item_2 = QtWidgets.QTreeWidgetItem(item_1)
    # item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
    # item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
    # item_1 = QtWidgets.QTreeWidgetItem(item_0)
    # item_2 = QtWidgets.QTreeWidgetItem(item_1)
    # item_1 = QtWidgets.QTreeWidgetItem(item_0)
    self.verticalLayout.addWidget(self.treeWidget)

    # self.retranslateUi(Form)
    QtCore.QMetaObject.connectSlotsByName(Form)

  # def retranslateUi(self, Form):
  #   _translate = QtCore.QCoreApplication.translate
  #   Form.setWindowTitle(_translate("Form", "Form"))
  #   self.treeWidget.headerItem().setText(0, _translate("Form", "Dir"))
  #   __sortingEnabled = self.treeWidget.isSortingEnabled()
  #   self.treeWidget.setSortingEnabled(False)
  #   self.treeWidget.topLevelItem(0).setText(0, _translate("Form", "test"))
  #   self.treeWidget.topLevelItem(0).child(0).setText(0, _translate("Form", "test-sub1"))
  #   self.treeWidget.topLevelItem(0).child(0).child(0).setText(0, _translate("Form", "test-sub1-sub2"))
  #   self.treeWidget.topLevelItem(1).setText(0, _translate("Form", "test1"))
  #   self.treeWidget.topLevelItem(2).setText(0, _translate("Form", "test2"))
  #   self.treeWidget.topLevelItem(2).child(0).setText(0, _translate("Form", "test2-sub1"))
  #   self.treeWidget.topLevelItem(2).child(0).child(0).setText(0, _translate("Form", "test2-sub1-sub2"))
  #   self.treeWidget.topLevelItem(2).child(1).setText(0, _translate("Form", "test2-sub2"))
  #   self.treeWidget.setSortingEnabled(__sortingEnabled)


if __name__ == "__main__":
  import sys
  app = QtWidgets.QApplication(sys.argv)
  Form = QtWidgets.QWidget()
  ui = Ui_Form()
  ui.setupUi(Form)
  Form.show()
  sys.exit(app.exec_())

