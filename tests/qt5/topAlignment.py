#!/usr/bin/env python2
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys
import os

sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-1]))


from PyQt5 import QtWidgets, QtGui, QtCore, uic

app = QtWidgets.QApplication(sys.argv)

loadUI = uic.loadUi("./topAlignment.ui")
loadUI.verticalLayoutWidgets.setAlignment(QtCore.Qt.AlignTop)
loadUI.show()
sys.exit(app.exec_())

