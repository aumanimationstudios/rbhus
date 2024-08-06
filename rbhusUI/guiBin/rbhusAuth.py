#!/usr/bin/env python3
from PyQt5 import QtWidgets, QtCore, QtGui
import os
import sys


dirSelf = os.path.dirname(os.path.realpath(__file__))
print(dirSelf)
sys.path.append(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep) + os.sep + "lib")

import rbhusAuthMod
print(dirSelf.rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")
sys.path.append(dirSelf.rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")
import constants
import auth


try:
  _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
  _fromUtf8 = lambda s: s
  
  

class Ui_Form(rbhusAuthMod.Ui_MainWindowAuth):
  def setupUi(self, Form):
    
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(_fromUtf8(dirSelf.rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/rbhus.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
    
    Form.setWindowIcon(icon)
    self.center()
    rbhusAuthMod.Ui_MainWindowAuth.setupUi(self,Form)
    self.pushButton.clicked.connect(self.tryAuth)
  
  def center(self):
    
    qr = Form.frameGeometry()
    cp = QtWidgets.QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    Form.move(qr.topLeft())
  
  def tryAuth(self):
    acl = auth.login()
    ret = acl.ldapLogin(str(self.lineEditUser.text()),str(self.lineEditPass.text()))
    if(ret):
      print("VALID")
      print(str(acl.username))
      os.system("env |& grep -i rbhus_")
    else:
      print("\n&*^*&^*%&$&^(*)(__)&*%^$#   .. :) !\n")
    
if __name__ == "__main__":
  #if(sys.platform.find("linux") >= 0):
    #acl = auth.login()
    #ret = acl.useEnvUser()
    #if(ret):
      #os.system("env |& grep -i rbhus_")
      #sys.exit(0)
    #else:
      #sys.exit(1)
  app = QtWidgets.QApplication(sys.argv)
  Form = QtWidgets.QMainWindow()
  ui = Ui_Form()
  ui.setupUi(Form)
  Form.show()
  sys.exit(app.exec_())