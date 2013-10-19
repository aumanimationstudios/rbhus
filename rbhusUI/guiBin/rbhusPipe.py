#!/usr/bin/python
from PyQt4 import QtCore, QtGui
import os
import sys
import tempfile
import time


dirSelf = os.path.dirname(os.path.realpath(__file__))
print(dirSelf)
sys.path.append(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep) + os.sep + "lib")

tempDir = tempfile.gettempdir()
rpA = "rbhusPipeAdmin.py"

  
rbhusPipeAdminCmd = dirSelf.rstrip(os.sep) + os.sep + rpA

import rbhusPipeMainMod
print(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")
sys.path.append(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")
import constantsPipe
import authPipe
import dbPipe
import utils as rUtils

try:
  _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
  _fromUtf8 = lambda s: s
  

class Ui_Form(rbhusPipeMainMod.Ui_MainWindow):
  def setupUi(self, Form):
    rbhusPipeMainMod.Ui_MainWindow.setupUi(self,Form)
    self.authL = authPipe.login()
    self.username = None
    self.center()
    try:
      self.username = os.environ['rbhusPipe_acl_user'].rstrip().lstrip()
    except:
      pass
    
    
    
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(_fromUtf8(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/rbhusPipe.svg")), QtGui.QIcon.Normal, QtGui.QIcon.On)
    Form.setWindowIcon(icon)
    self.pushLogout.setText("logout : "+ str(self.username))
    self.pushAdmin.clicked.connect(self.rbhusPipeAdmin)
    #self.pushSubmit.clicked.connect(self.rbhusSubmit)
    #self.pushHosts.clicked.connect(self.rbhusHost)
    self.pushLogout.clicked.connect(self.logout)
    self.form = Form
    self.trayIcon = QtGui.QSystemTrayIcon(QtGui.QIcon(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/rbhusPipe.svg"))
    self.trayIcon.show()
    
    self.trayMenu = QtGui.QMenu()
    
    
    self.adminAction = self.trayMenu.addAction("admin")
    self.quitAction = self.trayMenu.addAction("quit")
    self.quitAction.triggered.connect(self.quitFunc)
    self.adminAction.triggered.connect(self.rbhusPipeAdmin)
    
    self.trayIcon.setContextMenu(self.trayMenu)
    self.trayIcon.activated.connect(self.showMain)
    
    self.form.closeEvent = self.closeEvent
    
    
  
  def rbhusPipeAdmin(self):
    self.pushAdmin.setText("opening")
    p = QtCore.QProcess(parent=self.form)
    p.setStandardOutputFile(tempDir + os.sep +"rbhusPipeAdmin.log")
    p.setStandardErrorFile(tempDir + os.sep +"rbhusPipeAdmin.err")
    self.pushAdmin.setEnabled(False)
    self.adminAction.setEnabled(False)
    p.start(sys.executable,rbhusPipeAdminCmd.split())
    p.finished.connect(self.rbhusPipeAdminEnable)
    p.started.connect(self.rbhusPipeAdminWait)
    
  
  def rbhusPipeAdminWait(self):
    self.pushAdmin.setText("admin open")
  

  def rbhusPipeAdminEnable(self,exitStatus):
    self.pushAdmin.setText("ADMIN")
    self.pushAdmin.setEnabled(True)
    self.adminAction.setEnabled(True)
  
  
  
  def closeEvent(self,event):
    event.ignore()
    QtGui.QMessageBox.about(self.form,"QUITING?","Minimizing to Tray .\nPlease quit from the tray icon if you really want to quit!")
    self.form.setVisible(False) 
    
   
  
  def showMain(self,actReason):
    if(actReason == 2):
      self.form.setVisible(True)
    

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
