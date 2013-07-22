#!/usr/bin/python
from PyQt4 import QtCore, QtGui
import os
import sys



progPath =  sys.argv[0].split(os.sep)
print progPath
if(len(progPath) > 1):
  pwd = os.sep.join(progPath[0:-1])
  cwd = os.path.abspath(pwd)
else:
  cwd = os.path.abspath(os.getcwd())
  
sys.path.append(cwd.rstrip(os.sep) + os.sep + "lib")

import rbhusAuthMod
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
  
  

class Ui_Form(rbhusAuthMod.Ui_MainWindowAuth):
  def setupUi(self, Form):
    dbConn = dbRbhus.dbRbhus()
    clientPrefs = dbConn.getClientPrefs()
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(_fromUtf8(cwd.rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/rbhus.svg")), QtGui.QIcon.Normal, QtGui.QIcon.On)
    
    Form.setWindowIcon(icon)
    self.center()
    rbhusAuthMod.Ui_MainWindowAuth.setupUi(self,Form)
    self.pushButton.clicked.connect(self.tryAuth)
    self.acl = auth.login()
    
    if(sys.platform.find("linux") >= 0):
      self.acl.useEnvUser()
      os.system("env |& grep -i rbhus_")
      os.system("guiBin"+ os.sep +"_rbhusSubmit.py &")
      sys.exit(0)
      
    if(not clientPrefs['authentication']):
      self.acl.useEnvUser()
      os.system("env |& grep -i rbhus_")
      os.system("guiBin"+ os.sep +"_rbhusSubmit.py &")
      sys.exit(0)
      
    rms = self.acl.tryRememberMe()
    if(rms):
      print(str(self.acl.username))
      os.system("env |& grep -i rbhus_")
      os.system("guiBin"+ os.sep +"_rbhusSubmit.py &")
      sys.exit(0)
      
    
  
  def center(self):
    
    qr = Form.frameGeometry()
    cp = QtGui.QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    Form.move(qr.topLeft())
  
  def tryAuth(self):
    
    rM = self.checkBoxRememberMe.isChecked()
    ret = self.acl.ldapLogin(str(self.lineEditUser.text()), str(self.lineEditPass.text()), rM)
    if(ret):
      print("VALID")
      print(str(self.acl.username))
      os.system("env |& grep -i rbhus_")
      if(sys.platform.find("win") >= 0):
        os.system("guiBin"+ os.sep +"_rbhusSubmit.py &")
      elif(sys.platform.find("linux") >= 0):
        os.system("guiBin"+ os.sep +"_rbhusSubmit.py &")
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