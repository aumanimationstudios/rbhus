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

rL = "rbhusList.py"
rS = "rbhusSubmit.py"
rH = "rbhusHost.py"
  
rbhuslistCmd = dirSelf.rstrip(os.sep) + os.sep + rL
rbhuslistCmd = rbhuslistCmd.replace("\\","/")

rbhusSubmitCmd = dirSelf.rstrip(os.sep) + os.sep + rS
rbhusSubmitCmd = rbhusSubmitCmd.replace("\\","/")

rbhusHostCmd = dirSelf.rstrip(os.sep) + os.sep + rH
rbhusHostCmd = rbhusHostCmd.replace("\\","/")

print rbhuslistCmd
import rbhusRenderMain
print(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")
sys.path.append(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")
import db
import constants
import auth
import dbRbhus

try:
  _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
  _fromUtf8 = lambda s: s
  

class Ui_Form(rbhusRenderMain.Ui_MainWindow):
  def setupUi(self, Form):
    rbhusRenderMain.Ui_MainWindow.setupUi(self,Form)
    self.authL = auth.login()
    self.username = None
    self.userProjIds = []
    self.center()
    try:
      self.username = os.environ['rbhus_acl_user'].rstrip().lstrip()
    except:
      pass
    try:
      self.userProjIds = os.environ['rbhus_acl_projIds'].split()
    except:
      pass
    
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(_fromUtf8(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/rbhus.svg")), QtGui.QIcon.Normal, QtGui.QIcon.On)
    Form.setWindowIcon(icon)
    self.pushLogout.setText("logout : "+ str(self.username))
    self.pushList.clicked.connect(self.rbhusList)
    self.pushSubmit.clicked.connect(self.rbhusSubmit)
    self.pushHosts.clicked.connect(self.rbhusHost)
    self.pushLogout.clicked.connect(self.logout)
    self.form = Form
    
    
  def rbhusList(self):
    self.pushList.setText("opening")
    p = QtCore.QProcess(parent=self.form)
    self.pushList.setEnabled(False)
    p.start(sys.executable,rbhuslistCmd.split())
    p.finished.connect(self.rbhusListEnable)
    p.started.connect(self.rbhusListWait)
    
  
  def rbhusListWait(self):
    self.pushList.setText("list open")
  

  def rbhusListEnable(self,exitStatus):
    self.pushList.setText("list")
    self.pushList.setEnabled(True)
  
  
  def rbhusSubmit(self):
    self.pushSubmit.setText("opening")
    p = QtCore.QProcess(parent=self.form)
    self.pushSubmit.setEnabled(False)
    p.start(sys.executable,rbhusSubmitCmd.split())
    p.finished.connect(self.rbhusSubmitEnable)
    p.started.connect(self.rbhusSubmitWait)
    

  def rbhusSubmitWait(self):
    self.pushSubmit.setText("new open")
  

  def rbhusSubmitEnable(self,exitStatus):
    self.pushSubmit.setText("new")
    self.pushSubmit.setEnabled(True)


  def rbhusHost(self):
    self.pushHosts.setText("opening")
    p = QtCore.QProcess(parent=self.form)
    self.pushHosts.setEnabled(False)
    p.start(sys.executable,rbhusHostCmd.split())
    p.finished.connect(self.rbhusHostEnable)
    p.started.connect(self.rbhusHostWait)
    

  def rbhusHostWait(self):
    self.pushHosts.setText("hosts open")
  

  def rbhusHostEnable(self,exitStatus):
    self.pushHosts.setText("hosts")
    self.pushHosts.setEnabled(True)
    

  def logout(self):
    self.authL.logout()
    QtCore.QCoreApplication.instance().quit()
  

  def center(self):
    Form.move(QtGui.QApplication.desktop().screen().rect().center()- Form.rect().center())
      
    
if __name__ == "__main__":
  import sys
  app = QtGui.QApplication(sys.argv)
  Form = QtGui.QMainWindow()
  ui = Ui_Form()
  ui.setupUi(Form)
  Form.show()
  sys.exit(app.exec_())
