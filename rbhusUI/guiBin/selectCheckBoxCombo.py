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

import selectCheckBoxComboMod

sys.path.append(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")

parser = argparse.ArgumentParser()



parser.add_argument("-i","--input",dest='inputlist',help='comma seperated input list')
parser.add_argument("-d","--default",dest='defaultlist',help='comma seperated default checked list')
args = parser.parse_args()


try:
  _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
  _fromUtf8 = lambda s: s
  

class Ui_Form(selectCheckBoxComboMod.Ui_selectCheckBox):
  def setupUi(self, Form):
    selectCheckBoxComboMod.Ui_selectCheckBox.setupUi(self,Form)
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(_fromUtf8(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/rbhus.svg")), QtGui.QIcon.Normal, QtGui.QIcon.On)
    Form.setWindowIcon(icon)
    self.inList = []
    self.inDict = {}
    self.defList = []
    self.updateLine = []
    if(args.inputlist):
      self.inList = args.inputlist.split(",")
      for x in self.inList:
        dets = x.split("#")
        if(len(dets) > 1):
          self.inDict[dets[0]] = dets[1].split("%")
        else:
          self.inDict[dets[0]] = None
      
    if(args.defaultlist):
      self.defList = args.defaultlist.split(",")
      
    self.checkBoxes = {}
    self.updateCheckBoxes()
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
    
    
    
    
  def updateCheckBoxes(self):
    findList = []
    for x in self.inList:
      if(x.find(str(self.lineEditSearch.text())) >= 0):
        findList.append(x)
    
    
    for x in self.inList:
      try:
        self.checkBoxes[x][0].setParent(None)
        self.checkBoxes[x][0].deleteLater()
        self.checkBoxes[x][0] = None
        
        del(self.checkBoxes[x])
      except:
        pass
      
    if(findList):
      for x in findList:
        groupBox = QtGui.QGroupBox(self.scrollAreaWidgetContents)
        #groupBox.setObjectName(_fromUtf8("groupBox"))
        gridLayout_2 = QtGui.QGridLayout(groupBox)
        #gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        checkBox = QtGui.QCheckBox(groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(checkBox.sizePolicy().hasHeightForWidth())
        checkBox.setSizePolicy(sizePolicy)
        checkBox.setText(_fromUtf8(""))
        #checkBox.setObjectName(_fromUtf8("checkBox"))
        gridLayout_2.addWidget(checkBox, 0, 0, 1, 1)
        comboBox = QtGui.QComboBox(groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(comboBox.sizePolicy().hasHeightForWidth())
        comboBox.setSizePolicy(sizePolicy)
        #comboBox.setObjectName(_fromUtf8("comboBox"))
        gridLayout_2.addWidget(comboBox, 0, 1, 1, 1)


        self.checkBoxes[x] = [groupBox,checkBox,comboBox]
        self.checkBoxes[x][0].setTitle(_fromUtf8(x))
        self.verticalLayout.addWidget(self.checkBoxes[x][0])
        self.checkBoxes[x][1].stateChanged.connect(self.updateSelected)
        if(x in self.defList):
          self.checkBoxes[x][1].setChecked(2)
    #self.defList = []
    
    
        
  def deselectall(self):
    for x in self.inList:
      self.checkBoxes[x][1].setChecked(0)
        
  
  def selectall(self):
    for x in self.inList:
      self.checkBoxes[x][1].setChecked(2)
  
  
  def updateSelected(self):
    self.updateLine = []
    #self.plainTextEditSelected.setReadOnly(False)
    self.plainTextEditSelected.clear()
    for x in self.checkBoxes.keys():
      #print(x + " : "+ str(self.checkBoxes[x].isChecked()))
      if(self.checkBoxes[x][1].isChecked()):
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
    
    
