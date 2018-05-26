#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys

from PyQt5.QtWidgets import QApplication, QFileSystemModel, QTreeView, QWidget, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore



class fsm(QFileSystemModel):
  def __init__(self):
    super(fsm, self).__init__()




class App(QWidget):

  def __init__(self):
    super(App,self).__init__()
    self.title = 'PyQt5 file system view - pythonspot.com'
    self.left = 10
    self.top = 10
    self.width = 640
    self.height = 480
    self.initUI()

  def initUI(self):
    self.setWindowTitle(self.title)
    self.setGeometry(self.left, self.top, self.width, self.height)

    self.model = fsm()
    self.model.setFilter(QtCore.QDir.NoDot | QtCore.QDir.NoDotDot |QtCore.QDir.Dirs)

    self.model.setRootPath(sys.argv[1])
    self.tree = QTreeView()
    self.tree.setModel(self.model)

    self.tree.setAnimated(True)
    self.tree.setIndentation(20)
    self.tree.setSortingEnabled(True)

    self.tree.setWindowTitle("Dir View")
    # self.tree.resize(640, 480)

    windowLayout = QVBoxLayout()
    windowLayout.addWidget(self.tree)
    self.setLayout(windowLayout)

    self.show()


if __name__ == '__main__':
  app = QApplication(sys.argv)
  ex = App()
  sys.exit(app.exec_())