#!/usr/bin/env python2
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys
import os

file_dir = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-1])
base_dir = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2])
ui_dir = os.path.join(base_dir,"rbhusUI","lib","rbhusPipe_assImporter")
rbhus_lib_dir = os.path.join(base_dir,"rbhus")

sys.path.append(base_dir)
import rbhus.dbPipe

from PyQt5 import QtWidgets, QtGui, QtCore, uic



ui_main = os.path.join(ui_dir,"ui_main.ui")

dbcon = rbhus.dbPipe.dbPipe()
assesTypes = dbcon.execute("select distinct(assetType) from assets where projName='AndePirki_se01_ep003_SavingPrivateRyan'",dictionary=True)
print(assesTypes)

app = QtWidgets.QApplication(sys.argv)

mainUid = uic.loadUi(ui_main)


os._exit((app.exec_()))