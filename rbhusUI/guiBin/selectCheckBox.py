#!/usr/bin/env python3
from PyQt5 import QtWidgets, QtCore, QtGui
import glob
import os
import sys
import datetime
import re
import argparse


dirSelf = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep) + os.sep + "lib")

import selectCheckBoxMod

sys.path.append(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")

parser = argparse.ArgumentParser()



parser.add_argument("-i","--input",dest='inputlist',help='comma seperated input list')
parser.add_argument("-d","--default",dest='defaultlist',help='comma seperated default checked list')
args = parser.parse_args()


try:
  _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
  _fromUtf8 = lambda s: s


def str_convert(text):
  if isinstance(text, bytes):
    return str(text, 'utf-8')
  return str(text)


def lowerString(a):
  return(a.lower())

class Ui_Form(selectCheckBoxMod.Ui_selectCheckBox):
  def setupUi(self, Form):
    selectCheckBoxMod.Ui_selectCheckBox.setupUi(self,Form)
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(str_convert(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/rbhus.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
    Form.setWindowIcon(icon)
    self.inList = []
    self.defList = []
    self.updateLine = []
    if(args.inputlist):
      self.inList = args.inputlist.split(",")
      self.inList = sorted(self.inList,key=lowerString)
    if(args.defaultlist):
      self.defList = args.defaultlist.split(",")
      
    self.checkBoxes = {}

    self.populateCheckBoxes()
    # self.updateCheckBoxes()
    self.updateSelected()
    self.pushApply.clicked.connect(self.pApply)
    self.pushDeselect.clicked.connect(self.deselectall)
    self.pushSelect.clicked.connect(self.selectall)
    self.lineEditSearch.textChanged.connect(self.updateCheckBoxes)
    self.pushClearSearch.clicked.connect(self.lineEditSearch.clear)
    Form.closeEvent = self.closeEvent
  
  
  def closeEvent(self,event):
    print(",".join(self.defList))
    event.accept()
    
  
  
  def pApply(self):
    print(",".join(self.updateLine))
    QtCore.QCoreApplication.instance().quit()
    

  def populateCheckBoxes(self):
    for x in self.inList:

      self.checkBoxes[x] = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
      self.checkBoxes[x].setObjectName(str_convert(x))
      self.verticalLayout.addWidget(self.checkBoxes[x])
      self.checkBoxes[x].setText(str_convert(x))
      self.checkBoxes[x].stateChanged.connect(self.updateSelected)
      if(x in self.defList):
        self.checkBoxes[x].setChecked(2)

    
    
  def updateCheckBoxes(self):
    findList = []
    for x in self.inList:
      if((x.lower()).find(str_convert(self.lineEditSearch.text()).lower()) >= 0):
        findList.append(x)
    
    
    for x in self.inList:
      try:
        # self.checkBoxes[x].setParent(None)
        # self.checkBoxes[x].deleteLater()
        # self.checkBoxes[x] = None
        #
        # del(self.checkBoxes[x])
        if(findList):
          if(x in findList):
            self.checkBoxes[x].show()
          else:
            self.checkBoxes[x].hide()

        else:
          self.checkBoxes[x].show()

      except:
        print(sys.exc_info())
      
    # if(findList):
    #   for x in findList:
    #     self.checkBoxes[x] = QtGui.QCheckBox(self.scrollAreaWidgetContents)
    #     self.checkBoxes[x].setObjectName(_fromUtf8(x))
    #     self.verticalLayout.addWidget(self.checkBoxes[x])
    #     self.checkBoxes[x].setText(_fromUtf8(x))
    #     self.checkBoxes[x].stateChanged.connect(self.updateSelected)
    #     if(x in self.defList):
    #       self.checkBoxes[x].setChecked(2)

    
        
  def deselectall(self):
    for x in self.inList:
      self.checkBoxes[x].setChecked(0)
        
  
  def selectall(self):
    for x in self.inList:
      self.checkBoxes[x].setChecked(2)
  
  
  def updateSelected(self):
    self.updateLine = []
    #self.plainTextEditSelected.setReadOnly(False)
    self.plainTextEditSelected.clear()
    for x in self.checkBoxes.keys():
      #print(x + " : "+ str(self.checkBoxes[x].isChecked()))
      if(self.checkBoxes[x].isChecked()):
        self.updateLine.append(str(x))
    self.plainTextEditSelected.setPlainText(str_convert(",".join(self.updateLine)))
    #self.plainTextEditSelected.setReadOnly(True)
      
        
      
      
    #self.checkBox_2 = QtGui.QCheckBox(self.scrollAreaWidgetContents)
    #self.checkBox_2.setObjectName(_fromUtf8("checkBox_2"))
    #self.verticalLayout.addWidget(self.checkBox_2)
    
    
if __name__ == "__main__":
  app = QtWidgets.QApplication(sys.argv)
  Form = QtWidgets.QMainWindow()
  ui = Ui_Form()
  ui.setupUi(Form)
  Form.show()
  sys.exit(app.exec_())
    
    
