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
  def __init__(self, parent=None, *args):
    super(MyDelegate,self).__init__(parent, *args)
    self.ass_ui = uic.loadUi(ui_asset_details)
    self.ass_ui.setParent(parent)

  # def paintEvent(self,e):
  #   qp = QPainter()
  #   qp.begin(self)
  #   self.drawWidget(self.ass_ui)
  #   qp.end()

  def paint(self, painter, option, index):
    painter.save()

    # set background color
    painter.setPen(QtGui.QPen(QtCore.Qt.NoPen))
    if option.state & QtWidgets.QStyle.State_Selected:
      painter.setBrush(QtGui.QBrush(QtCore.Qt.red))
    else:
      painter.setBrush(QtGui.QBrush(QtCore.Qt.white))
    painter.drawRect(option.rect)

    # set text color
    painter.setPen(QtGui.QPen(QtCore.Qt.black))
    value = index.data(QtCore.Qt.DisplayRole)
    if value:
      text = str(value)
      # painter.drawText(option.rect, QtCore.Qt.AlignLeft, text)
    # painter.drawWidget(self.ass_ui)
    painter.restore()


####################################################################
class MyListModel(QtCore.QAbstractListModel):
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
