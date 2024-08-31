#!/usr/bin/env python3
from PyQt5 import QtWidgets, QtCore, QtGui
import glob
import os
import sys
import socket
import time
import subprocess
import re


dirSelf = os.path.dirname(os.path.realpath(__file__))
print(dirSelf)
sys.path.append(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep) + os.sep + "lib")

scb = "selectCheckBox.py"

selectCheckBoxCmd = dirSelf.rstrip(os.sep) + os.sep + scb
selectCheckBoxCmd = selectCheckBoxCmd.replace("\\","/")


myIps = sys.argv[1].split(",")

import rbhusHostEditMultiMod

print(dirSelf.rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")
sys.path.append(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")
import db
import constants
import auth
import dbRbhus
import utils as rUtils

try:
  _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
  _fromUtf8 = lambda s: s
  

def str_convert(text):
  if isinstance(text, bytes):
    return str(text, 'utf-8')
  return str(text)


class Ui_Form(rbhusHostEditMultiMod.Ui_rbhusHostEdit):
  def setupUi(self, Form):
    rbhusHostEditMultiMod.Ui_rbhusHostEdit.setupUi(self,Form)
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(str_convert(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/rbhus.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
    Form.setWindowIcon(icon)
    self.popData()
    self.pushApply.clicked.connect(self.applyResources)
    
    self.pushSelect.clicked.connect(self.printGroupSel)
    self.pushReset.clicked.connect(self.popData)
    
   
    
  def popData(self):
    self.lineEditGroups.setText("")
  
  def applyResources(self):
    for ip in myIps:
      h = rUtils.hosts(hostIp=ip)
      h.updateGroups(str_convert(self.lineEditGroups.text()))
    QtCore.QCoreApplication.instance().quit()
    
  def printGroupSel(self):
    groups = rUtils.getHostGroupsActive()
    
    outGroups = subprocess.Popen([sys.executable,selectCheckBoxCmd,"-i",",".join(groups),"-d",str_convert(self.lineEditGroups.text()).rstrip().lstrip()],stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].rstrip().lstrip()
    outGroups = str_convert(outGroups)
    if(outGroups == ""):
      return()
    self.lineEditGroups.setText(str_convert(outGroups))
    
    
    
if __name__ == "__main__":
  app = QtWidgets.QApplication(sys.argv)
  Form = QtWidgets.QMainWindow()
  ui = Ui_Form()
  ui.setupUi(Form)
  Form.show()
  sys.exit(app.exec_())   