#!/usr/bin/env python2
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys
import os
import setproctitle

setproctitle.setproctitle("wtf1")

from PyQt5 import QtCore, uic, QtGui, QtWidgets


app = QtWidgets.QApplication(sys.argv)

clip = QtWidgets.QApplication.clipboard()
conts = clip.text()
print(conts)

urlToCopy = QtCore.QUrl("file:////home/shrinidhi/Downloads/WTF")
# urlToCopy.fromLocalFile("/home/shrinidhi/Downloads/WTF")
mimeData = QtCore.QMimeData()
mimeData.setUrls([urlToCopy])
QtWidgets.QApplication.clipboard().setMimeData(mimeData)


sys.exit(app.exec_())