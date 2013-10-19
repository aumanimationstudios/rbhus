#!/usr/bin/python
from PyQt4 import QtCore, QtGui
import glob
import os
import sys


dirSelf = os.path.dirname(os.path.realpath(__file__))
print(dirSelf)
sys.path.append(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep) + os.sep + "lib")

scb = "rbhusPipeProjCreate.py"

rppc = dirSelf.rstrip(os.sep) + os.sep + scb
rppc = rppc.replace("\\","/")

import rbhusPipeAdminPanelMod
print(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")
sys.path.append(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")
import dbPipe
import constantsPipe
import utils as rUtils
import authPipe


try:
  _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
  _fromUtf8 = lambda s: s
  

class Ui_Form(rbhusPipeAdminPanelMod.Ui_MainWindow):
  def setupUi(self, Form):
    rbhusPipeAdminPanelMod.Ui_MainWindow.setupUi(self,Form)
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(_fromUtf8(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/rbhusPipe.svg")), QtGui.QIcon.Normal, QtGui.QIcon.On)
    Form.setWindowIcon(icon)
    self.center()
    
    
  def rbhusPipeCreateProj(self):
    self.pushCreate.setText("opening")
    p = QtCore.QProcess(parent=self.form)
    p.setStandardOutputFile(tempDir + os.sep +"rbhusPipeAdmin.log")
    p.setStandardErrorFile(tempDir + os.sep +"rbhusPipeAdmin.err")
    self.pushCreate.setEnabled(False)
    self.adminAction.setEnabled(False)
    p.start(sys.executable,rppc.split())
    p.finished.connect(self.rppcEnable)
    p.started.connect(self.rppcWait)
    
  
  def rppcWait(self):
    self.pushCreate.setText("admin open")
  

  def rppcEnable(self,exitStatus):
    self.pushCreate.setText("ADMIN")
    self.pushCreate.setEnabled(True)
    self.adminAction.setEnabled(True)
  
  
  
  
  def center(self):
    Form.move(QtGui.QApplication.desktop().screen().rect().center()- Form.rect().center())
    
    
if __name__ == "__main__":
  app = QtGui.QApplication(sys.argv)
  Form = QtGui.QMainWindow()
  ui = Ui_Form()
  ui.setupUi(Form)
  Form.show()
  sys.exit(app.exec_())
    