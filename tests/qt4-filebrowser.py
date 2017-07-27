#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from PyQt4.QtGui import *


class Browser(QWidget):
  def __init__(self):
    super(Browser, self).__init__()
    mimeFileter = []
    # history = []
    mimeFileter.append("image/png")
    mimeFileter.append("image/x-exr")
    mimeFileter.append("image/jpeg")
    mimeFileter.append("video/avi")
    mimeFileter.append("video/mp4")
    mimeFileter.append("video/quicktime")
    self.resize(700, 600)
    self.setWindowTitle("File Browser")
    self.treeView = QListView()
    self.fileSystemModel = QFileSystemModel(self.treeView)
    self.fileSystemModel.setReadOnly(True)
    root = self.fileSystemModel.setRootPath(sys.argv[1])
    self.treeView.setModel(self.fileSystemModel)
    self.treeView.setRootIndex(root)

    Layout = QVBoxLayout(self)
    Layout.addWidget(self.treeView)
    self.setLayout(Layout)


if __name__ == "__main__":
  app = QApplication(sys.argv)
  main = Browser()
  main.show()
  sys.exit(app.exec_())
