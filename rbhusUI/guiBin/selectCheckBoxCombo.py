#!/usr/bin/python
from PyQt4 import QtCore, QtGui
import glob
import os
import sys
import datetime
import re
import argparse
import logging
import logging.handlers
import socket
import tempfile
import copy



dirSelf = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep) + os.sep + "lib")

import selectCheckBoxComboMod

sys.path.append(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")

parser = argparse.ArgumentParser()

hostname = socket.gethostname()
tempDir = os.path.abspath(tempfile.gettempdir())

if(sys.platform.find("win") >= 0):
  try:
    username = os.environ['USERNAME']
  except:
    username = "nobody"
if(sys.platform.find("linux") >= 0):
  try:
    username = os.environ['USER']
  except:
    username = "nobody"


LOG_FILENAME = logging.FileHandler(tempDir + os.sep +"rbhusPipe_selectCheckBoxCombo_"+ username +"_"+ str(hostname) +".log")
  #LOG_FILENAME = logging.FileHandler('z:/pythonTestWindoze.DONOTDELETE/clientLogs/rbhusDb_'+ hostname +'.log')

#LOG_FILENAME = logging.FileHandler('/var/log/rbhusDb_module.log')
selectCheckBoxComboLogger = logging.getLogger("selectCheckBoxComboLogger")
selectCheckBoxComboLogger.setLevel(logging.DEBUG)


#ROTATE_FILENAME = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=104857600, backupCount=3)
BASIC_FORMAT = logging.Formatter("%(asctime)s - %(funcName)s - %(levelname)s - %(message)s")
LOG_FILENAME.setFormatter(BASIC_FORMAT)
selectCheckBoxComboLogger.addHandler(LOG_FILENAME)


parser.add_argument("-i","--input",dest='inputlist',help='comma seperated input list')
parser.add_argument("-c","--combolist",dest='combolist',help='comma seperated list for comboBox')
parser.add_argument("-d","--defaultlist",dest='defaultlist',help='comma seperated list of input list to be selected by default')

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
    self.form = Form
    self.inList = []
    self.inDict = {}
    self.defCombo = []
    self.updateLine = []
    self.defDict = {}
    self.findList = []
    if(args.inputlist):
      self.inList = args.inputlist.split(",")
      for x in self.inList:
        dets = x.split("#")
        if(len(dets) > 1):
          self.inDict[dets[0]] = dets[1].split("%")
        else:
          self.inDict[dets[0]] = []
      
    if(args.combolist):
      self.defCombo = args.combolist.split(",")
    if(args.defaultlist):
      self.defList = args.defaultlist.split(",")
      for x in self.defList:
        dets = x.split("#")
        if(len(dets) > 1):
          self.defDict[dets[0]] = dets[1].split("%")
        else:
          self.defDict[dets[0]] = []
    selectCheckBoxComboLogger.debug(self.defDict)
    self.checkBoxes = {}
    self.updateCheckBoxes()
    self.updateSelected()
    self.pushApply.clicked.connect(self.pApply)
    self.pushDeselect.clicked.connect(self.deselectall)
    self.pushSelect.clicked.connect(self.selectall)
    self.lineEditSearch.textChanged.connect(self.searchReset)
    self.pushClearSearch.clicked.connect(self.lineEditSearch.clear)
    Form.closeEvent = self.closeEvent
  
  
  
  def searchReset(self):
    try:
      selectCheckBoxComboLogger.debug(str(self.plainTextEditSelected.document().toPlainText()))
      self.defList = str(self.plainTextEditSelected.document().toPlainText()).split(",")
      #self.defDict = {}
      for x in self.defList:
        dets = x.split("#")
        if(len(dets) > 1):
          self.defDict[dets[0]] = dets[1].split("%")
        else:
          self.defDict[dets[0]] = []
      self.updateCheckBoxes()
    #self.updateSelected()
    except:
      selectCheckBoxComboLogger.debug(str(sys.exc_info()))
  
  
  def closeEvent(self,event):
    #finalblow = []
    #for x in self.defList:
      #finalblow.append(x +"#"+"%".join(self.inDict[x]))
    #print(",".join(finalblow))
    event.accept()
    
  
  
  def pApply(self):
    print(str(self.plainTextEditSelected.document().toPlainText()))
    QtCore.QCoreApplication.instance().quit()
    
    
    
    
  def updateCheckBoxes(self):
    self.findList = []
    for x in self.inDict.keys():
      if(x.find(str(self.lineEditSearch.text())) >= 0):
        self.findList.append(x)
    
    
    for x in self.inDict.keys():
      try:
        self.checkBoxes[x][0].setParent(None)
        self.checkBoxes[x][0].deleteLater()
        self.checkBoxes[x][0] = None
        
        del(self.checkBoxes[x])
      except:
        pass
      
    if(self.findList):
      #model = QtGui.QStandardItemModel(len(self.findList),1)
      for x in self.findList:
        indx = 0
        groupBox = QtGui.QGroupBox(self.scrollAreaWidgetContents)
        comboBox = QtGui.QComboBox(groupBox)
        model = QtGui.QStandardItemModel(len(self.defCombo),1)
        model.setParent(comboBox)
        
        for row in self.defCombo:
          item = QtGui.QStandardItem(row)
          if(sys.platform.find("linux") >=0):
            item.setFlags(QtCore.Qt.ItemIsEnabled)
          elif(sys.platform.find("win") >=0):
            item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
          #item.setFlags(QtCore.Qt.ItemIsUserCheckable)
          item.setData(QtCore.Qt.Unchecked, QtCore.Qt.CheckStateRole)
          model.setItem(indx,0,item)
          abrush = QtGui.QBrush()
          color = QtGui.QColor()
          color.setAlpha(0)
          abrush.setColor(color)
          model.item(indx).setForeground(abrush)
          indx = indx + 1
        
        
        
        
        
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
        comboBox.setObjectName(_fromUtf8(x))
        gridLayout_2.addWidget(checkBox, 0, 0, 1, 1)
        
        comboBox.setEditable(True)
        comboBox.lineEdit().setReadOnly(True)
        comboBox.setModel(model)
        if(x in self.defDict):
          comboBox.setEditText(",".join(self.defDict[x]))
        else:
          comboBox.setEditText("default")
        
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(comboBox.sizePolicy().hasHeightForWidth())
        comboBox.setSizePolicy(sizePolicy)
        
        
    
        #comboBox.pressedFileType = pressedFileType
        
        
        comboBox.setObjectName(_fromUtf8(x))
        gridLayout_2.addWidget(comboBox, 0, 1, 1, 1)


        self.checkBoxes[x] = [groupBox,checkBox,comboBox]
        self.checkBoxes[x][0].setTitle(_fromUtf8(x))
        self.verticalLayout.addWidget(self.checkBoxes[x][0])
        self.checkBoxes[x][1].stateChanged.connect(self.updateSelected)
        self.checkBoxes[x][2].editTextChanged.connect(self.updateSelected)
        self.checkBoxes[x][2].view().activated.connect(lambda index, x=x : self.pressedFileType(index,self.checkBoxes[x][2]))
        #print(self.checkBoxes[x][2].objectName())
        if(x in self.defDict):
          self.checkBoxes[x][1].setChecked(2)
    #self.defCombo = []
    
  def pressedFileType(self,*args):
    selectedStages = []
    index = args[0]
    father = args[1]
    if(father.model().item(index.row()).checkState() != 0):
      father.model().item(index.row()).setCheckState(QtCore.Qt.Unchecked)
      #self.comboStageType.model().item(index.row()).setEnabled(False)
      abrush = QtGui.QBrush()
      color = QtGui.QColor()
      color.setAlpha(0)
      abrush.setColor(color)
      father.model().item(index.row()).setForeground(abrush)
    else:
      father.model().item(index.row()).setCheckState(QtCore.Qt.Checked)
      #self.comboStageType.model().item(index.row()).setEnabled(True)
      abrush = QtGui.QBrush()
      color = QtGui.QColor()
      color.setGreen(10)
      color.setBlue(125)
      color.setRed(225)
      abrush.setColor(color)
      father.model().item(index.row()).setForeground(abrush)
    changes = False
    for i in range(0,father.model().rowCount()):
      if(father.model().item(i).checkState() == QtCore.Qt.Checked):
        selectedStages.append(str(father.model().item(i).text()))
        changes = True
      
    ##print("EVENT CALLED : "+ str(index.row()))
    if(changes):
      father.setEditText(",".join(selectedStages))
    else:
      father.setEditText("default")
        
  def deselectall(self):
    self.defList = []
    self.defDict = {}
    for x in self.findList:
      self.checkBoxes[x][1].setChecked(0)
        
  
  def selectall(self):
    for x in self.findList:
      self.checkBoxes[x][1].setChecked(2)
  
  
  def updateSelected(self):
    try:


      if(len(str(self.lineEditSearch.text())) > 0):
        a = str(self.plainTextEditSelected.document().toPlainText()).split(",")
        temDict = {}
        for x in a:
          detsa = x.split("#")
          if(len(detsa) > 1):
            temDict[detsa[0]] = detsa[1].split("%")
          else:
            temDict[detsa[0]] = []
        
        tempShit = []
        for y in self.checkBoxes.keys():
          if(self.checkBoxes[y][1].isChecked()):
            tempShit.append(str(y) +"#"+ "%".join(str(self.checkBoxes[y][2].currentText()).split(",")))
          else:
            try:
              del temDict[str(y)]
            except:
              selectCheckBoxComboLogger.debug(str(sys.exc_info()))
        for z in tempShit:
          detsb = z.split("#")
          if(len(detsb) > 1):
            temDict[detsb[0]] = detsb[1].split("%")
          else:
            temDict[detsb[0]] = []

        tempshit2 = []
        for v in temDict.keys():
           if(temDict[v]):
             tempshit2.append(str(v) +"#"+ "%".join(temDict[v]))

        selectCheckBoxComboLogger.debug(tempshit2)
        tempshit2.sort()
        self.plainTextEditSelected.clear()
        
        self.plainTextEditSelected.setPlainText(_fromUtf8(",".join(tempshit2)))
      else:
        self.updateLine = []
        for x in self.checkBoxes.keys():
          if(self.checkBoxes[x][1].isChecked()):
            self.updateLine.append(str(x) +"#"+ "%".join(str(self.checkBoxes[x][2].currentText()).split(",")))
        self.updateLine.sort()
        self.plainTextEditSelected.clear()
        self.plainTextEditSelected.setPlainText(_fromUtf8(",".join(self.updateLine)))
    except:
      selectCheckBoxComboLogger.debug(str(sys.exc_info()))
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
    
    
