#!/usr/bin/env python3

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import os
import tempfile


tempDir = tempfile.gettempdir()
file_dir = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-1])
base_dir = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-3])
ui_dir = os.path.join(base_dir,"rbhusUI","lib","qt5","rbhusPipe_main")
rbhus_lib_dir = os.path.join(base_dir,"rbhus")
custom_widget_dir = os.path.join(base_dir,"rbhusUI","lib","qt5","customWidgets")
home_dir = os.path.expanduser("~")

sys.path.append(base_dir)
import rbhus.utilsPipe




my_array = [['00','01','02'],
            ['10','11','12'],
            ['20','21','22']]

class modelView(QAbstractTableModel):
  def __init__(self, datain, parent=None, *args):
    QAbstractTableModel.__init__(self, parent, *args)
    self.arraydata = datain


  def rowCount(self, parent):
    return len(self.arraydata)


  def columnCount(self, parent):
    return len(self.arraydata[0])


  def data(self, index, role):
    if not index.isValid():
      return QVariant()
    elif role != Qt.DisplayRole:
      return QVariant()
    if(index.column() == 2):
      l = QLabel()
      l.setText(str(self.arraydata[index.row()][index.column()]))
      return QVariant(l)
    else:
      return QVariant(self.arraydata[index.row()][index.column()])

class Window(QWidget):
  def __init__(self):
    QWidget.__init__(self)

    layout = QGridLayout()
    self.setLayout(layout)

    model = modelView(my_array)
    self.columnview = QTableView()
    self.columnview.setModel(model)
    layout.addWidget(self.columnview)

app = QApplication(sys.argv)

screen = Window()
screen.show()

sys.exit(app.exec_())