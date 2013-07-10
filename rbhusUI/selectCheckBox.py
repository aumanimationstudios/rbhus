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
import selectCheckBoxMod
print(cwd.rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")
sys.path.append(cwd.rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")
import dbRbhus
import constants
import utils as rUtils
import auth

dbconn = dbRbhus.dbRbhus()
parser = argparse.ArgumentParser()



parser.add_argument("-i","--input",dest='inputlist',help='comma seperated input list')
parser.add_argument("-d","--default",dest='defaultlist',help='comma seperated default checked list')
args = parser.parse_args()


try:
  _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
  _fromUtf8 = lambda s: s
  

class Ui_Form(selectCheckBoxMod.Ui_selectCheckBox):
  def setupUi(self, Form):
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(_fromUtf8(cwd.rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/rbhus.svg")), QtGui.QIcon.Normal, QtGui.QIcon.On)
    Form.setWindowIcon(icon)
    self.authL = auth.login()
    selectCheckBoxMod.Ui_selectCheckBox.setupUi(self,Form)
    
    self.inList = args.inputlist.split(",")
    self.defList = args.defaultlist.split(",")
    self.checkBoxes = {}
    self.updateCheckBoxes()
    self.updateSelected()
      
    
    
  def updateCheckBoxes(self):
    for x in self.inList:
      self.checkBoxes[x] = QtGui.QCheckBox(self.scrollAreaWidgetContents)
      self.checkBoxes[x].setObjectName(_fromUtf8(x))
      self.verticalLayout.addWidget(self.checkBoxes[x])
      self.checkBoxes[x].setText(_fromUtf8(x))
      self.checkBoxes[x].stateChanged.connect(self.updateSelected)
      if(x in self.defList):
        self.checkBoxes[x].setChecked(2)
        
        
  def updateSelected(self):
    updateLine = []
    #self.plainTextEditSelected.setReadOnly(False)
    self.plainTextEditSelected.clear()
    for x in self.checkBoxes.keys():
      #print(x + " : "+ str(self.checkBoxes[x].isChecked()))
      if(self.checkBoxes[x].isChecked()):
        updateLine.append(str(x))
    self.plainTextEditSelected.setPlainText(_fromUtf8(", ".join(updateLine)))
    #self.plainTextEditSelected.setReadOnly(True)
      
        
      
      
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
    
    
