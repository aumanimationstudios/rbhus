#!/usr/bin/python
from PyQt4 import QtCore, QtGui
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


myIp = sys.argv[1]

import rbhusHostEditMod

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
  

class Ui_Form(rbhusHostEditMod.Ui_rbhusHostEdit):
  def setupUi(self, Form):
    rbhusHostEditMod.Ui_rbhusHostEdit.setupUi(self,Form)
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(_fromUtf8(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/rbhus.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
    Form.setWindowIcon(icon)
    self.h = rUtils.hosts(myIp)
    self.popData()
    self.pushApply.clicked.connect(self.applyResources)
    
    self.pushSelect.clicked.connect(self.printGroupSel)
    self.pushReset.clicked.connect(self.popData)
    self.db_eCpus = 0
    self.db_groups = 0
    
    
  
  def popData(self):
    self.spinCpu.setRange(0,int(self.h.hostDetails['totalCpus']))
    self.spinCpu.setValue(int(self.h.hostDetails['eCpus']))
    self.lineEditGroups.setText(self.h.hostDetails['groups'])
  
  def applyResources(self):
    self.h.setHostData("hostEffectiveResource","eCpus",str(self.spinCpu.value()))
    self.h.setGroups(str(self.lineEditGroups.text()))
    QtCore.QCoreApplication.instance().quit()
    
  def printGroupSel(self):
    groups = rUtils.getHostGroupsActive()
    
    outGroups = subprocess.Popen([sys.executable,selectCheckBoxCmd,"-i",",".join(groups),"-d",str(self.lineEditGroups.text()).rstrip().lstrip()],stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].rstrip().lstrip()
    outGroupsDict = {}
    for x in outGroups.split(","):
      outGroupsDict[x] = 1
    outGroupsDict['default'] = 1
    outGroupsDict[self.h.hostDetails['hostName']] = 1
    
    outGroups = ",".join(outGroupsDict.keys())
    
    self.lineEditGroups.setText(_fromUtf8(outGroups))
    
    
    
    
if __name__ == "__main__":
  app = QtGui.QApplication(sys.argv)
  Form = QtGui.QMainWindow()
  ui = Ui_Form()
  ui.setupUi(Form)
  Form.show()
  app.exec_()
  sys.exit()   