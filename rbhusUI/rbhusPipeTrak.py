#!/usr/bin/python
from PyQt4 import QtCore, QtGui
import os
import sys
import subprocess



dirSelf = os.path.dirname(os.path.realpath(__file__))
print(dirSelf)
sys.path.append(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep) + os.sep + "lib")

# os.environ['QT_STYLE_OVERRIDE'] = "windows"


import rbhusAuthMod
print(dirSelf.rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")
sys.path.append(dirSelf.rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")
import db
import constants
import authPipe
import dbPipe


try:
  _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
  _fromUtf8 = lambda s: s
  
  

class Ui_Form(rbhusAuthMod.Ui_MainWindowAuth):
  def setupUi(self, Form):
    self.form = Form
    #dbConn = dbRbhus.dbRbhus()
    #clientPrefs = dbConn.getClientPrefs()
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(_fromUtf8(dirSelf.rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/rbhus.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
    
    Form.setWindowIcon(icon)
    self.center()
    rbhusAuthMod.Ui_MainWindowAuth.setupUi(self,Form)
    self.pushButton.clicked.connect(self.tryAuth)
    self.acl = authPipe.login()

    if(sys.platform.find("linux") >= 0):
      self.acl.useEnvUser()
      self.runCmd("guiBin"+ os.sep +"rbhusPipeTrak.py")
      sys.exit(0)
      
    #if(not clientPrefs['authentication']):
      #self.acl.useEnvUser()
      #self.runCmd("guiBin"+ os.sep +"rbhusPipeTrak.py")
      #sys.exit(0)
      
    rms = self.acl.tryRememberMe()
    if(rms):
      print(str(self.acl.username))
      self.runCmd("guiBin"+ os.sep +"rbhusPipeTrak.py")
      sys.exit(0)
    
  
  def runCmd(self,cmd):
    p = QtCore.QProcess(parent=self.form)
    p.startDetached(sys.executable,cmd.split())
    
  
  def center(self):
    Form.move(QtGui.QApplication.desktop().screen().rect().center()- Form.rect().center())
  
  def tryAuth(self):
    
    rM = self.checkBoxRememberMe.isChecked()
    ret = self.acl.ldapLogin(str(self.lineEditUser.text()), str(self.lineEditPass.text()), rM)
    if(ret):
      print("VALID")
      print(str(self.acl.username))
      self.runCmd("guiBin"+ os.sep +"rbhusPipeTrak.py")
    else:
      print("\n&*^*&^*%&$&^(*)(__)&*%^$#   .. :) !\n")
    sys.exit(0)



if __name__ == "__main__":
  app = QtGui.QApplication(sys.argv)
  Form = QtGui.QMainWindow()
  ui = Ui_Form()
  ui.setupUi(Form)
  Form.show()
  sys.exit(app.exec_())