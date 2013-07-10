#!/usr/bin/python
from PyQt4 import QtCore, QtGui
import glob
import os
import sys
import datetime
import re
import argparse


progPath =  sys.argv[0].split(os.sep)
print progPath
if(len(progPath) > 1):
  pwd = os.sep.join(progPath[0:-1])
  cwd = os.path.abspath(pwd)
else:
  cwd = os.path.abspath(os.getcwd())
  
print cwd
sys.path.append(cwd.rstrip(os.sep) + os.sep + "lib")
import rbhusEditTaskHostGroupsMod
print(cwd.rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")
sys.path.append(cwd.rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")
import dbRbhus
import constants
import utils as rUtils
import auth

dbconn = dbRbhus.dbRbhus()




parser.add_argument("-i","--input",dest='input',help='comma seperated input list')
parser.add_argument("-d","--default",dest='def',help='comma seperated default checked list')
args = parser.parse_args()


try:
  _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
  _fromUtf8 = lambda s: s
  

class Ui_Form(rbhusEditTaskHostGroupsMod.Ui_rbhusTaskHostGroups):
  def setupUi(self, Form):
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(_fromUtf8(cwd.rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/rbhus.svg")), QtGui.QIcon.Normal, QtGui.QIcon.On)
    Form.setWindowIcon(icon)
    self.authL = auth.login()
    rbhusEditTaskHostGroupsMod.Ui_rbhusTaskHostGroups.setupUi(self,Form)
    
    self.hostGroupsBoxed = rUtils.getHostGroups()
    self.checkBoxes = {}
    #self.verticalLayout.clear()
    for x in self.hostGroupsBoxed:
      print(x)
      self.checkBoxes[x] = QtGui.QCheckBox(self.scrollAreaWidgetContents)
      self.checkBoxes[x].setObjectName(_fromUtf8(x))
      self.verticalLayout.addWidget(self.checkBoxes[x])
      self.checkBoxes[x].setText(_fromUtf8(x))
      
      
    #self.checkBox_2 = QtGui.QCheckBox(self.scrollAreaWidgetContents)
    #self.checkBox_2.setObjectName(_fromUtf8("checkBox_2"))
    #self.verticalLayout.addWidget(self.checkBox_2)
    
    
if __name__ == "__main__":
  app = QtGui.QApplication(sys.argv)
  Form = QtGui.QMainWindow()
  ui = Ui_Form()
  ui.setupUi(Form)
  Form.show()
  sys.exit(app.exec_())
    
    
