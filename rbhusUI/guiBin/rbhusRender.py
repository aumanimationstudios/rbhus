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
import utils as rUtils

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
    
    self.hostDets = rUtils.hosts()
    
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(_fromUtf8(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/rbhus.svg")), QtGui.QIcon.Normal, QtGui.QIcon.On)
    Form.setWindowIcon(icon)
    self.pushLogout.setText("logout : "+ str(self.username))
    self.pushList.clicked.connect(self.rbhusList)
    self.pushSubmit.clicked.connect(self.rbhusSubmit)
    self.pushHosts.clicked.connect(self.rbhusHost)
    self.pushLogout.clicked.connect(self.logout)
    self.form = Form
    self.trayIcon = QtGui.QSystemTrayIcon(QtGui.QIcon(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/rbhus.svg"))
    self.trayIcon.show()
    
    self.trayMenu = QtGui.QMenu()
    self.hostMenu = QtGui.QMenu()
    self.listAction = self.trayMenu.addAction("list")
    self.newAction = self.trayMenu.addAction("new")
    self.hostAction = self.trayMenu.addAction("hosts")
    self.quitAction = self.trayMenu.addAction("quit")
    
    self.hostEnableAction = self.hostMenu.addAction("enable")
    self.hostDisableAction = self.hostMenu.addAction("stop")
    self.hostEnableAction.triggered.connect(self.hostDets.hEnable)
    self.hostDisableAction.triggered.connect(self.hostDets.hStop)
    
    
    self.trayIcon.setContextMenu(self.trayMenu)
    self.trayIcon.activated.connect(self.showMain)
    self.listAction.triggered.connect(self.rbhusList)
    self.newAction.triggered.connect(self.rbhusSubmit)
    self.hostAction.setMenu(self.hostMenu)
    #self.hostAction.triggered.connect(self.rbhusHost)
    self.quitAction.triggered.connect(self.quitFunc)
    self.form.closeEvent = self.closeEvent
    
    
  def closeEvent(self,event):
    QtGui.QMessageBox.about(self.form,"QUITING?","Minimizing to Tray . Please quit from the tray icon if you really want to quit!")
    event.ignore()
    self.form.setVisible(False) 
    
    
  def showMain(self,actReason):
    if(actReason == 2):
      self.form.setVisible(True)
    
  def rbhusList(self):
    self.pushList.setText("opening")
    p = QtCore.QProcess(parent=self.form)
    self.pushList.setEnabled(False)
    self.listAction.setEnabled(False)
    p.start(sys.executable,rbhuslistCmd.split())
    p.finished.connect(self.rbhusListEnable)
    p.started.connect(self.rbhusListWait)
    
  
  def rbhusListWait(self):
    self.pushList.setText("list open")
  

  def rbhusListEnable(self,exitStatus):
    self.pushList.setText("list")
    self.pushList.setEnabled(True)
    self.listAction.setEnabled(True)
  
  
  def rbhusSubmit(self):
    self.pushSubmit.setText("opening")
    p = QtCore.QProcess(parent=self.form)
    self.pushSubmit.setEnabled(False)
    self.newAction.setEnabled(False)
    p.start(sys.executable,rbhusSubmitCmd.split())
    p.finished.connect(self.rbhusSubmitEnable)
    p.started.connect(self.rbhusSubmitWait)
    

  def rbhusSubmitWait(self):
    self.pushSubmit.setText("new open")
  

  def rbhusSubmitEnable(self,exitStatus):
    self.pushSubmit.setText("new")
    self.pushSubmit.setEnabled(True)
    self.newAction.setEnabled(True)


  def rbhusHost(self):
    self.pushHosts.setText("opening")
    p = QtCore.QProcess(parent=self.form)
    self.pushHosts.setEnabled(False)
    self.hostAction.setEnabled(False)
    p.start(sys.executable,rbhusHostCmd.split())
    p.finished.connect(self.rbhusHostEnable)
    p.started.connect(self.rbhusHostWait)
    

  def rbhusHostWait(self):
    self.pushHosts.setText("hosts open")
  

  def rbhusHostEnable(self,exitStatus):
    self.pushHosts.setText("hosts")
    self.pushHosts.setEnabled(True)
    self.hostAction.setEnabled(True)
    

  def logout(self):
    self.authL.logout()
    QtCore.QCoreApplication.instance().quit()
  
  def quitFunc(self):
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
