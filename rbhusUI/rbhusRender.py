#!/usr/bin/env python3
from PyQt5 import QtWidgets, QtCore, QtGui
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
import auth
import dbRbhus


try:
  _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
  _fromUtf8 = lambda s: s


def str_convert(text):
  if isinstance(text, bytes):
    return str(text, 'utf-8')
  return str(text)


class Ui_Form(rbhusAuthMod.Ui_MainWindowAuth):
  def setupUi(self, Form):
    self.form = Form
    dbConn = dbRbhus.dbRbhus()
    clientPrefs = dbConn.getClientPrefs()
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(str_convert(dirSelf.rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/rbhus.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
    
    Form.setWindowIcon(icon)
    self.center()
    rbhusAuthMod.Ui_MainWindowAuth.setupUi(self,Form)
    self.pushButton.clicked.connect(self.tryAuth)
    self.acl = auth.login()

    if(sys.platform.find("linux") >= 0):
      self.acl.useEnvUser()
      self.runCmd(dirSelf.rstrip(os.sep) + os.sep +"guiBin"+ os.sep +"rbhusRender.py")
      sys.exit(0)
      
    if(not clientPrefs['authentication']):
      self.acl.useEnvUser()
      self.runCmd(dirSelf.rstrip(os.sep) + os.sep +"guiBin"+ os.sep +"rbhusRender.py")
      sys.exit(0)
      
    rms = self.acl.tryRememberMe()
    if(rms):
      print(str(self.acl.username))
      self.runCmd(dirSelf.rstrip(os.sep) + os.sep +"guiBin"+ os.sep +"rbhusRender.py")
      sys.exit(0)
    
  
  def runCmd(self,cmd):
    p = QtCore.QProcess(parent=self.form)
    p.startDetached(sys.executable,cmd.split())
    
  
  def center(self):
    Form.move(QtWidgets.QApplication.desktop().screen().rect().center()- Form.rect().center())
  
  def tryAuth(self):
    
    rM = self.checkBoxRememberMe.isChecked()
    ret = self.acl.ldapLogin(str_convert(self.lineEditUser.text()), str_convert(self.lineEditPass.text()), rM)
    if(ret):
      print("VALID")
      print(str(self.acl.username))
      self.runCmd(dirSelf.rstrip(os.sep) + os.sep +"guiBin"+ os.sep +"rbhusRender.py")
    else:
      print("\n&*^*&^*%&$&^(*)(__)&*%^$#   .. :) !\n")
    sys.exit(0)
    
if __name__ == "__main__":
  app = QtWidgets.QApplication(sys.argv)
  Form = QtWidgets.QMainWindow()
  ui = Ui_Form()
  ui.setupUi(Form)
  Form.show()
  sys.exit(app.exec_())