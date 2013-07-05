#!/usr/bin/python
from PyQt4 import QtCore, QtGui
import glob
import os
import sys
import socket
import time
import subprocess
import re


progPath =  sys.argv[0].split(os.sep)
print progPath
if(len(progPath) > 1):
  pwd = os.sep.join(progPath[0:-1])
  cwd = os.path.abspath(pwd)
else:
  cwd = os.path.abspath(os.getcwd())
print cwd  
sys.path.append(cwd.rstrip(os.sep) + os.sep + "lib")

rEc = "rbhusHostEdit.py"
  
editHostCmd = cwd.rstrip(os.sep) + os.sep + rEc
editHostCmd = editHostCmd.replace("\\","/")
print editHostCmd
import rbhusListMod
print(cwd.rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")
sys.path.append(cwd.rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")
import db
import constants
import auth
import dbRbhus

try:
  _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
  _fromUtf8 = lambda s: s
  

class Ui_Form(rbhusListMod.Ui_mainRbhusList):
  def setupUi(self, Form):
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(_fromUtf8(cwd.rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/rbhus.svg")), QtGui.QIcon.Normal, QtGui.QIcon.On)
    Form.setWindowIcon(icon)
    self.authL = auth.login()
    self.pushApply.clicked.connect(self.applyResources)
    