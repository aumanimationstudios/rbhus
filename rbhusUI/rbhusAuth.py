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


try:
  _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
  _fromUtf8 = lambda s: s
  
  

class Ui_Form(rbhusAuthMod.Ui_MainWindowAuth):
  def setupUi(self, Form):
    
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(_fromUtf8(cwd.rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/rbhus.svg")), QtGui.QIcon.Normal, QtGui.QIcon.On)
    
    Form.setWindowIcon(icon)
    self.center()
    rbhusAuthMod.Ui_MainWindowAuth.setupUi(self,Form)
    self.pushButton.clicked.connect(self.tryAuth)
  
  def center(self):
    
    qr = Form.frameGeometry()
    cp = QtGui.QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    Form.move(qr.topLeft())
  
  def tryAuth(self):
    acl = auth.login()
    ret = acl.ldapLogin(str(self.lineEditUser.text()),str(self.lineEditPass.text()))
    if(ret):
      print("VALID")
      os.environ['rbhus_user'] = str(self.lineEditUser.text())
      print(str(acl.username))
      print(str(acl.userAcl))
      if(acl.userAcl):
        print("exporting environment variables...")
        for x in acl.userAcl.keys():
          os.environ['rbhus_acl_'+ str(x)] = str(acl.userAcl[x])
      os.system("env |& grep -i rbhus_")
    else:
      print("\n&*^*&^*%&$&^(*)(__)&*%^$#   .. :) !\n")
    
if __name__ == "__main__":
  app = QtGui.QApplication(sys.argv)
  Form = QtGui.QMainWindow()
  ui = Ui_Form()
  ui.setupUi(Form)
  Form.show()
  sys.exit(app.exec_())