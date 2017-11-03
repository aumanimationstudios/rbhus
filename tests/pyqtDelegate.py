#!/usr/bin/env python2
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys
import os

file_dir = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-1])
base_dir = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2])

ui_dir = os.path.join(base_dir,"rbhusUI","lib","qt5","rbhusPipe_main")

ui_asset_details = os.path.join(ui_dir,"assetDetailRow.ui")

rbhus_lib_dir = os.path.join(base_dir,"rbhus")

sys.path.append(base_dir)
import rbhus.dbPipe
import rbhus.constantsPipe
import rbhus.utilsPipe
import rbhus.debug

import time

from PyQt5 import QtWidgets, QtGui, QtCore, uic
import sip



####################################################################
def main():
  app = QtWidgets.QApplication(sys.argv)
  w = MyWindow()
  w.show()
  sys.exit(app.exec_())


####################################################################
class MyWindow(QtWidgets.QWidget):
  def __init__(self, *args):
    super(MyWindow,self).__init__(*args)

    # create objects
    list_data = [1, 2, 3, 4]
    lm = MyListModel(list_data, self)
    lv = QtWidgets.QListView()
    de = MyDelegate(lv)
    lv.setModel(lm)
    lv.setItemDelegate(de)

    # layout
    layout = QtWidgets.QVBoxLayout()
    layout.addWidget(lv)
    self.setLayout(layout)


####################################################################
class MyDelegate(QtWidgets.QItemDelegate):
  def createEditor(self, parent, option, index):
    comboBox = QComboBox(parent)
    # if index.column() == 1:
    comboBox.addItem("Normal")
    comboBox.addItem("Active")
    comboBox.addItem("Disabled")
    comboBox.addItem("Selected")
    # elif index.column() == 2:
    #   comboBox.addItem("Off")
    #   comboBox.addItem("On")

    comboBox.activated.connect(self.emitCommitData)

    return comboBox

  def setEditorData(self, editor, index):
    comboBox = editor
    if not comboBox:
      return

    pos = comboBox.findText(index.model().data(index), Qt.MatchExactly)
    comboBox.setCurrentIndex(pos)

  def setModelData(self, editor, model, index):
    comboBox = editor
    if not comboBox:
      print("wtf1")
      return

    model.setData(index, comboBox.currentText())

  def emitCommitData(self):
    self.commitData.emit(self.sender())


####################################################################
class MyListModel(QtCore.QAbstractItemModel):
  def __init__(self, datain, parent=None, *args):
    """ datain: a list where each item is a row
    """
    super(MyListModel,self).__init__(parent, *args)
    self.listdata = datain

  def rowCount(self, parent=QtCore.QModelIndex()):
    return len(self.listdata)

  def data(self, index, role):
    if index.isValid() and role == QtCore.Qt.DisplayRole:
      return QtCore.QVariant(self.listdata[index.row()])
    else:
      return QtCore.QVariant()


####################################################################
if __name__ == "__main__":
  main()
