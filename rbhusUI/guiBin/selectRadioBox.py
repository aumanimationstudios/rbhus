#!/usr/bin/python
from PyQt4 import QtCore, QtGui
import glob
import os
import sys
import datetime
import re
import argparse


dirSelf = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep) + os.sep + "lib")

import selectRadioBoxMod

sys.path.append(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")

parser = argparse.ArgumentParser()



parser.add_argument("-i","--input",dest='inputlist',help='comma seperated input list')
parser.add_argument("-d","--default",dest='defaultlist',help='comma seperated default checked list')
args = parser.parse_args()


try:
  _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
  _fromUtf8 = lambda s: s
  

class Ui_Form(selectRadioBoxMod.Ui_selectRadioBox):
  def setupUi(self, Form):
    selectRadioBoxMod.Ui_selectRadioBox.setupUi(self,Form)
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(_fromUtf8(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/rbhus.svg")), QtGui.QIcon.Normal, QtGui.QIcon.On)
    Form.setWindowIcon(icon)
    self.inList = []
    self.defList = []
    self.updateLine = []
    if(args.inputlist):
      self.inList = args.inputlist.split(",")
    if(args.defaultlist):
      self.defList = args.defaultlist.split(",")
      
    self.radioButts = {}
    self.updateCheckBoxes()
    self.updateSelected()
    self.pushApply.clicked.connect(self.pApply)
    self.lineEditSearch.textChanged.connect(self.updateCheckBoxes)
    self.pushClearSearch.clicked.connect(self.lineEditSearch.clear)
    Form.closeEvent = self.closeEvent
  
  
  def closeEvent(self,event):
    print(",".join(self.defList))
    event.accept()
    
  
  
  def pApply(self):
    print(",".join(self.updateLine))
    QtCore.QCoreApplication.instance().quit()
    
    
    
    
  def updateCheckBoxes(self):
    findList = []
    for x in self.inList:
      if((x.lower()).find(str(self.lineEditSearch.text()).lower()) >= 0):
        findList.append(x)
    
    
    for x in self.inList:
      try:
        self.radioButts[x].setParent(None)
        self.radioButts[x].deleteLater()
        self.radioButts[x] = None
        
        del(self.radioButts[x])
      except:
        pass
      
    if(findList):
      for x in findList:
        self.radioButts[x] = QtGui.QRadioButton(self.scrollAreaWidgetContents)
        self.radioButts[x].setObjectName(_fromUtf8(x))
        self.verticalLayout.addWidget(self.radioButts[x])
        self.radioButts[x].setText(_fromUtf8(x))
        self.radioButts[x].toggled.connect(self.updateSelected)
        if(x in self.defList):
          self.radioButts[x].setChecked(2)
    #self.defList = []
    
    
        
  def deselectall(self):
    for x in self.inList:
      self.radioButts[x].setChecked(0)
        
  
  def selectall(self):
    for x in self.inList:
      self.radioButts[x].setChecked(2)
  
  
  def updateSelected(self):
    self.updateLine = []
    #self.plainTextEditSelected.setReadOnly(False)
    self.plainTextEditSelected.clear()
    for x in self.radioButts.keys():
      #print(x + " : "+ str(self.radioButts[x].isChecked()))
      if(self.radioButts[x].isChecked()):
        self.updateLine.append(str(x))
    self.plainTextEditSelected.setPlainText(_fromUtf8(",".join(self.updateLine)))
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
    
    
