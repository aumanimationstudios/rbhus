#!/usr/bin/python
from PyQt4 import QtCore, QtGui
import glob
import os
import sys
import datetime
import re

progPath =  sys.argv[0].split(os.sep)
print progPath
if(len(progPath) > 1):
  pwd = os.sep.join(progPath[0:-1])
  cwd = os.path.abspath(pwd)
else:
  cwd = os.path.abspath(os.getcwd())
  
sys.path.append(cwd.rstrip(os.sep) + os.sep + "lib")
import rbhusSubmitMod
print(cwd.rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")
sys.path.append(cwd.rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")
import dbRbhus
import constants
import utils as rUtils

dbconn = dbRbhus.dbRbhus()

try:
  _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
  _fromUtf8 = lambda s: s
  

class Ui_Form(rbhusSubmitMod.Ui_rbhusSubmit):
  def setupUi(self, Form):
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(_fromUtf8(cwd.rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/rbhus.svg")), QtGui.QIcon.Normal, QtGui.QIcon.On)
    Form.setWindowIcon(icon)
    
    rbhusSubmitMod.Ui_rbhusSubmit.setupUi(self,Form)
    self.pushFileName.clicked.connect(self.selectFileName)
    self.pushOutDir.clicked.connect(self.selectOutDir)
    self.autoOutDir.clicked.connect(self.setOutDir)
    self.pushSubmit.clicked.connect(self.submitTasks)
    self.comboHostGroup.currentIndexChanged.connect(self.printGroupSel)
    self.comboPrio.currentIndexChanged.connect(self.printPrioSel)
    self.comboFileType.currentIndexChanged.connect(self.fileTypePrint)
    self.comboOsType.currentIndexChanged.connect(self.osTypePrint)
    self.checkAfterTime.clicked.connect(self.afterTimeEnable)
    groups = rUtils.getHostGroups()
    ostypes = rUtils.getOsTypes()
    ftypes = rUtils.getFileTypes()
    
    
    self.autoOutDir.setIcon(icon)
    self.autoOutDir.setIconSize(QtCore.QSize(12, 12))
    
    
    for group in groups:
      self.comboHostGroup.addItem(_fromUtf8(group))
    ind = 0
    try:
      ind = groups.index("default")
    except:
      pass
    self.comboHostGroup.setCurrentIndex(ind)
    
    for ft in ftypes:
      self.comboFileType.addItem(_fromUtf8(ft))
    ind = 0
    try:
      ind = ftypes.index("default")
    except:
      pass
    self.comboFileType.setCurrentIndex(ind)
      
    for ost in ostypes:
      self.comboOsType.addItem(_fromUtf8(ost))
    ind = 0
    try:
      ind = ostypes.index("default")
    except:
      pass
    self.comboOsType.setCurrentIndex(ind)
      
    
    
  def printGroupSel(self):
    print self.comboHostGroup.currentText()
    
    
  def printPrioSel(self):
    print self.comboPrio.currentText()
    
  
  
  def fileTypePrint(self):
    print(self.comboFileType.currentText())
    renders = rUtils.getRenderers()
    self.comboRenderer.clear()
    for x in renders[str(self.comboFileType.currentText())]:
      self.comboRenderer.addItem(_fromUtf8(x))

    
  
  def osTypePrint(self):
    print(self.comboOsType.currentText())
  
  
  def setFileTypes(self):
    rows = rUtils.getFileTypes()
      
    if(rows):
      for row in rows:
        self.comboFileType.addItem(_fromUtf8(row))
      
      return(1)
    else:
      return(0)
      
      
  def setOsTypes(self):
    rows = rUtils.getOsTypes()
      
    if(rows):
      for row in rows:
        self.comboOsType.addItem(_fromUtf8(row))
      
      return(1)
    else:
      return(0)     
  
  def selectFileName(self):
    fila = QtGui.QFileDialog.getOpenFileNames()
    if(fila):
      if(self.lineEditFileName.text()):
        self.lineEditFileName.setText(self.lineEditFileName.text() +","+ fila.join(","))
      else:
        self.lineEditFileName.setText(fila.join(","))
      
  def setOutDir(self):
    outFile = str(self.lineEditFileName.text())
    if(len(outFile.split(",")) > 1):
      print("TOO MANY FILENAMES TO AUTO DO THE OUTPUTDIR")
      return(0)
    if(sys.platform.find("win") >= 0):
      self.lineEditOutDir.setText("z:/"+ "/".join(outFile.split("/")[3:-1]) +"/"+ ".".join(outFile.split("/")[-1].split(".")[0:-1]))
    else:
      self.lineEditOutDir.setText("/projdump/"+ "/".join(outFile.split("/")[2:-1]) +"/"+ ".".join(outFile.split("/")[-1].split(".")[0:-1]))
  
  def selectOutDir(self):
    dirac = QtGui.QFileDialog.getExistingDirectory()
    if(dirac):
      self.lineEditOutDir.setText(dirac)
  
  def afterTimeEnable(self):
    cAT = self.checkAfterTime.isChecked()
    if(cAT):
      self.afterTimeEdit.setEnabled(True)
    else:
      self.afterTimeEdit.setEnabled(False)
      
  def submitTasks(self):
    submitDict = {}
    files = str(self.lineEditFileName.text())
    cameras = str(self.lineEditCameras.text())
    submitDict['fRange'] = str(self.lineEditFrange.text())
    submitdir = str(self.lineEditOutDir.text())
    submitDict['description'] = str(self.lineEditDescription.text())
    submitDict['resolution'] = str(self.lineEditResolution.text())
    if(self.checkAfterTime.isChecked()):
      submitDict['afterTime'] = str(self.afterTimeEdit.dateTime().date().year()) +"-"+ str(self.afterTimeEdit.dateTime().date().month()) +"-"+ str(self.afterTimeEdit.dateTime().date().day()) +" "+ str(self.afterTimeEdit.dateTime().time().hour()) +":"+ str(self.afterTimeEdit.dateTime().time().minute()) +":" + str(self.afterTimeEdit.dateTime().time().second())
    
    submitDict['os'] = str(self.comboOsType.currentText())
    submitDict['fileType'] = self.comboFileType.currentText()
    prios = str(self.comboPrio.currentText())
    if(prios == "low"):
      p = 1
    if(prios == "high"):
      p = 300
    if(prios == "normal"):
      p = 150
    batchFlag = str(self.comboBatching.currentText())
    if(batchFlag == "active"):
      submitDict['batch'] = str(constants.batchActive)
    else:
      submitDict['batch'] = str(constants.batchDeactive)
    
    submitDict['minBatch'] = str(self.spinMinBatch.value())
    submitDict['maxBatch'] = str(self.spinMaxBatch.value())
    submitDict['priority'] = str(p)
      
    if((submitDict['fileType'] == "3dsmax") and ((submitDict['os'] == "default") or (submitDict['os'] == "win"))):
      submitDict['afterFrameCmd'] = "Z:/pythonTestWindoze.DONOTDELETE/rbhus/etc/3dsmax/afterFrame.py"
      submitDict['beforeFrameCmd'] = "Z:/pythonTestWindoze.DONOTDELETE/rbhus/etc/3dsmax/beforeFrame.py"
    elif((submitDict['fileType'] == "3dsmax2013") and ((submitDict['os'] == "default") or (submitDict['os'] == "win"))):
      submitDict['afterFrameCmd'] = "Z:/pythonTestWindoze.DONOTDELETE/rbhus/etc/3dsmax2013/afterFrame.py"
      submitDict['beforeFrameCmd'] = "Z:/pythonTestWindoze.DONOTDELETE/rbhus/etc/3dsmax2013/beforeFrame.py"
      
    a = rUtils.tasks()
    
    for f in files.split(","):
      if(f):
        submitDict['fileName'] = f.replace("\\","/")
        sd = submitdir.replace("\\","/")
        #submitDict['cameras'] = cameras
        
        
        if(re.search('^default$',sd) == None):
          sd = sd.rstrip("/") +"/"+ ".".join(str((submitDict['fileName']).split("/")[-1]).split(".")[0:-1]) +"/"
          print(str(sd))
          
          
          for c in cameras.split(","):
            if(c):
              submitDict['camera'] = c
              if(re.search('^default$',submitDict['camera']) == None):
                sd = sd.rstrip("/") +"/"+ c + "/"
              if(re.search('^default$',submitDict['resolution']) == None):
                sd = sd.rstrip("/") +"/"+ submitDict['resolution'] + "/"
                
              submitDict['outDir'] = sd
              try:
                b = a.submit(submitDict)
                print("Submiting task : "+ str(b) +" : "+ str(submitDict['fileName']))
              except:
                print("Error inserting task : "+ str(sys.exc_info()))
        else:
          for c in cameras.split(","):
            if(c):
              submitDict['camera'] = c
              try:
                b = a.submit(submitDict)
                print("Submiting task : "+ str(b) +" : "+ str(submitDict['fileName']))
              except:
                print("Error inserting task : "+ str(sys.exc_info()))
                
            
              
            
          
        #if((submitDict['cameras'].indexOf("default") == -1) or (submitDict['cameras'].length() > 7) ):
          #submitDict['cameras'] = submitDict['cameras'] + "/"
          
          #print(str(submitDict['outDir']))
        #try:
          #b = a.submit(submitDict)
          #print("Submiting task : "+ str(b) +" : "+ str(submitDict['fileName']))
        #except:
          #print("Error inserting task : "+ str(sys.exc_info()))
    
    QtGui.qApp.closeAllWindows()
    
    
    
    
    
    
if __name__ == "__main__":
  app = QtGui.QApplication(sys.argv)
  Form = QtGui.QMainWindow()
  ui = Ui_Form()
  ui.setupUi(Form)
  Form.show()
  sys.exit(app.exec_())
    
    
