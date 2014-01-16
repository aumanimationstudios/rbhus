#!/usr/bin/python
from PyQt4 import QtCore, QtGui
import glob
import os
import sys
import datetime
import re
import subprocess


dirSelf = os.path.dirname(os.path.realpath(__file__))
print(dirSelf)
sys.path.append(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep) + os.sep + "lib")

scb = "selectCheckBox.py"

selectCheckBoxCmd = dirSelf.rstrip(os.sep) + os.sep + scb
selectCheckBoxCmd = selectCheckBoxCmd.replace("\\","/")

import rbhusSubmitMod
print(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")
sys.path.append(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")
import dbRbhus
import constants
import utils as rUtils
import auth

dbconn = dbRbhus.dbRbhus()

try:
  _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
  _fromUtf8 = lambda s: s
  

class Ui_Form(rbhusSubmitMod.Ui_rbhusSubmit):
  def setupUi(self, Form):
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(_fromUtf8(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/rbhus.svg")), QtGui.QIcon.Normal, QtGui.QIcon.On)
    Form.setWindowIcon(icon)
    self.authL = auth.login()
    
    self.taskValues = 0
    try:
      self.task = rUtils.tasks()
      self.taskValues = self.task.taskFields
    except:
      pass
    if(len(sys.argv) == 2):
      try:
        self.task = rUtils.tasks(int(sys.argv[1]))
        self.taskValues = self.task.taskDetails
      except:
        pass
    
    self.fileTypeDefs = rUtils.getFileTypesAll()
    self.renders = rUtils.getRenderers()
    self.imageTypes = rUtils.getImageTypes()
    
    
    rbhusSubmitMod.Ui_rbhusSubmit.setupUi(self,Form)
    self.pushFileName.clicked.connect(self.selectFileName)
    self.pushOutDir.clicked.connect(self.selectOutDir)
    self.autoOutDir.clicked.connect(self.setOutDir)
    self.autoOutName.clicked.connect(self.setOutName)
    self.pushSubmit.clicked.connect(self.submitTasks)
    self.pushSelectHostGroups.clicked.connect(self.printGroupSel)
    self.comboPrio.currentIndexChanged.connect(self.printPrioSel)
    self.comboFileType.currentIndexChanged.connect(self.fileTypeChanged)
    self.comboOsType.currentIndexChanged.connect(self.osTypePrint)
    self.comboRes.currentIndexChanged.connect(self.resetRes)
    self.checkAfterTime.clicked.connect(self.afterTimeEnable)
    self.checkBatching.clicked.connect(self.batchingCheck)
    
    ostypes = rUtils.getOsTypes()
    ftypes = rUtils.getFileTypes()
    resTemplates = rUtils.getResTemplates()
    
    self.autoOutDir.setIcon(icon)
    self.autoOutDir.setIconSize(QtCore.QSize(12, 12))
    self.autoOutName.setIcon(icon)
    self.autoOutName.setIconSize(QtCore.QSize(12, 12))
    self.labelUser.setText(os.environ['rbhus_acl_user'])
    
    
    self.afterTimeEdit.setDateTime(QtCore.QDateTime.currentDateTime())
    #for group in groups:
      #self.comboHostGroup.addItem(_fromUtf8(group))
    #ind = 0
    #try:
      #ind = groups.index("default")
    #except:
      #pass
    #self.comboHostGroup.setCurrentIndex(ind)
    
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
    
    for rt in resTemplates:
      self.comboRes.addItem(_fromUtf8(rt['name']))
    ind = 0
    try:
      for rt in resTemplates:
        if(rt['name'] == "default"):
          break
        ind = ind + 1
    except:
      pass
    self.comboRes.setCurrentIndex(ind)
    
    self.popEditItems()
    self.batchingCheck()
    
    
    
  def batchingCheck(self):
    if(self.checkBatching.isChecked()):
      self.spinMaxBatch.setEnabled(True)
      self.spinMinBatch.setEnabled(True)
    else:
      self.spinMaxBatch.setEnabled(False)
      self.spinMinBatch.setEnabled(False)
  
  
  def fileTypeChanged(self):
    #self.fileTypePrint()
    self.setTaskOsTypes()
    
    self.setRenderer()
    self.setImageTypes()
  
  
  def printGroupSel(self):
    groups = rUtils.getHostGroups()
    
    outGroups = subprocess.Popen([sys.executable,selectCheckBoxCmd,"-i",",".join(groups),"-d",str(self.lineEditHostGroups.text()).rstrip().lstrip()],stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].rstrip().lstrip()
    if(outGroups == ""):
      outGroups = "default"
    print(outGroups)
    self.lineEditHostGroups.setText(_fromUtf8(outGroups))
    
    
  def printPrioSel(self):
    print self.comboPrio.currentText()
    
  
  
  def fileTypePrint(self):
    #print(self.comboFileType.currentText())
    self.comboRenderer.clear()
    if(self.comboFileType.currentText()):
      for x in self.renders:
        if(x['fileType'] == str(self.comboFileType.currentText())):
          self.comboRenderer.addItem(_fromUtf8(x['renderer']))
          
        

    
  
  
  
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
    if(sys.platform.find("win") >= 0):
      fila = QtGui.QFileDialog.getOpenFileNames(directory="x:/")
    elif(sys.platform.find("linux") >= 0):
      fila = QtGui.QFileDialog.getOpenFileNames(directory="/proj/")
    if(fila):
      if(self.lineEditFileName.text()):
        self.lineEditFileName.setText(self.lineEditFileName.text() +","+ fila.join(","))
      else:
        self.lineEditFileName.setText(fila.join(","))
      
  def setOutName(self):
    outFile = str(self.lineEditFileName.text())
    for x in self.imageTypes:
      if(x['imageType'] == str(self.comboImageType.currentText())):
        exten = x['extention']
    self.lineEditOutName.setText(".".join((outFile.replace("\\","/")).split("/")[-1].split(".")[0:-1]) +"."+ exten)
    
  def setOutDir(self):
    outFile = str(self.lineEditFileName.text())
    if(sys.platform.find("win") >= 0):
      self.lineEditOutDir.setText("z:/"+ "/".join((outFile.replace("\\","/")).split("/")[1:-1]).rstrip().lstrip() +"/")
    else:
      self.lineEditOutDir.setText("/projdump/"+ "/".join(outFile.split("/")[2:-1]) +"/")
  
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
  
      
  def popEditItems(self):
    if(self.taskValues):
      if(len(sys.argv) == 2):
        self.lineEditFileName.setText(self.taskValues['fileName'])
        #self.lineEditOutDir.setText(self.taskValues['outDir'])
        self.lineEditOutName.setText(self.taskValues['outName'])
        self.afterTimeEdit.setTime(QtCore.QTime(self.taskValues['afterTime'].hour, self.taskValues['afterTime'].minute, self.taskValues['afterTime'].second))
        self.afterTimeEdit.setDate(QtCore.QDate(self.taskValues['afterTime'].year, self.taskValues['afterTime'].month, self.taskValues['afterTime'].day))
        self.lineEditAfterTask.setText(self.taskValues['afterTasks'])
        
      self.lineEditFrange.setText(self.taskValues['fRange'])
      self.lineEditCameras.setText(self.taskValues['camera'])
      self.lineEditLayer.setText(self.taskValues['layer'])
      self.lineEditRes.setText(self.taskValues['resolution'])
      
      self.spinMinBatch.setValue(int(self.taskValues['minBatch']))
      self.spinMaxBatch.setValue(int(self.taskValues['maxBatch']))
      
      self.lineEditDescription.setText(self.taskValues['description'])
      batchFF = int(self.taskValues['batch'])
      if(batchFF):
        self.checkBatching.setChecked(True)
      else:
        self.checkBatching.setChecked(False)
      self.setTaskFileTypes()
      self.setTaskHostGroups()
      self.setTaskOsTypes()
      return(1)
    else:
      return(0)
      
      
  def setRenderer(self):
    self.comboRenderer.clear()
    indx = 0
    setIndx = 0
    try:
      for x in self.renders:
        if(x['fileType'] == str(self.comboFileType.currentText())):
          self.comboRenderer.addItem(_fromUtf8(x['renderer']))
          for y in self.fileTypeDefs:
            if(str(y['fileType']) == str(self.comboFileType.currentText())):
              if(str(y['defRenderer']) == str(x)):
                setIndx = indx
          indx = indx + 1
        self.comboRenderer.setCurrentIndex(setIndx)
      return(1)
    except:
      print(str(sys.exc_info()))
      return(0)
   
  def setImageTypes(self):
    self.comboImageType.clear()
    indx = 0
    setIndx = 0
    try:
      for x in self.imageTypes:
        if(x['fileType'] == str(self.comboFileType.currentText())):
          self.comboImageType.addItem(_fromUtf8(x['imageType']))
          for y in self.fileTypeDefs:
            if(str(y['fileType']) == str(self.comboFileType.currentText())):
              if(str(y['defImageType']) == str(x)):
                setIndx = indx
          indx = indx + 1
        self.comboImageType.setCurrentIndex(setIndx)
      return(1)
    except:
      print(str(sys.exc_info()))
      return(0)
   
  def setTaskOsTypes(self):
    rows = rUtils.getOsTypes()
    self.comboOsType.clear()
    print(": 11 :")
    if(rows):
      indx = 0
      setIndx = 0
      for row in rows:
        print(": 12 :")
        self.comboOsType.addItem(_fromUtf8(row))
        defFileType = str(self.comboFileType.currentText())
        defOs = str(self.taskValues['os'])
        for x in self.fileTypeDefs:
          if(x['fileType'] == defFileType):
            defOs = x['defOs']
        if(row.find(defOs) >= 0):
          setIndx = indx
        indx = indx + 1
      self.comboOsType.setCurrentIndex(setIndx)
      return(1)
    else:
      return(0)   
  
  
  def setTaskHostGroups(self):
    rows = rUtils.getHostGroups()
    self.lineEditHostGroups.setText(self.taskValues['hostGroups'])    
  
  
  def setTaskFileTypes(self):
    rows = rUtils.getFileTypes()
    self.comboFileType.clear()  
    if(rows):
      indx = 0
      setIndx = 0
      for row in rows:
        self.comboFileType.addItem(_fromUtf8(row))
        print(str(self.taskValues['fileType']))
        if(row.endswith(str(self.taskValues['fileType']))):
          setIndx = indx
        indx = indx + 1
      
      self.comboFileType.setCurrentIndex(setIndx)
      self.setRenderer()
      self.setImageTypes()
      return(1)
    else:
      return(0)
  
  
  def resetRes(self):
    self.lineEditRes.setText("default")
  
  
  def submitTasks(self):
    resTemplates = rUtils.getResTemplates()
    submitDict = {}
    files = str(self.lineEditFileName.text())
    cameras = str(self.lineEditCameras.text())
    submitDict['fRange'] = str(self.lineEditFrange.text())
    submitdir = str(self.lineEditOutDir.text())
    submitDict['description'] = str(self.lineEditDescription.text())
    if(str(self.lineEditRes.text()) == "default"):
      for rt in resTemplates:
        if(rt['name'] == str(self.comboRes.currentText())):
          submitDict['resolution'] = str(rt['res'])
          break
    else:
      submitDict['resolution'] = str(self.lineEditRes.text())
    if(self.checkAfterTime.isChecked()):
      submitDict['afterTime'] = str(self.afterTimeEdit.dateTime().date().year()) +"-"+ str(self.afterTimeEdit.dateTime().date().month()) +"-"+ str(self.afterTimeEdit.dateTime().date().day()) +" "+ str(self.afterTimeEdit.dateTime().time().hour()) +":"+ str(self.afterTimeEdit.dateTime().time().minute()) +":" + str(self.afterTimeEdit.dateTime().time().second())
    if(self.checkSloppy.isChecked()):
      submitDict['afterTaskSloppy'] = constants.afterTaskSloppyEnable
    
    hE = self.checkHold.isChecked()
    if(hE):
      submitDict['status'] = constants.taskStopped
    submitDict['afterTasks'] = str(self.lineEditAfterTask.text())
    submitDict['outName'] = str(self.lineEditOutName.text())
    submitDict['os'] = str(self.comboOsType.currentText())
    submitDict['fileType'] = str(self.comboFileType.currentText())
    submitDict['hostGroups'] = str(self.lineEditHostGroups.text())
    submitDict['renderer'] = str(self.comboRenderer.currentText())
    layers = str(self.lineEditLayer.text())
    submitDict['imageType'] = str(self.comboImageType.currentText())
    
    prios = str(self.comboPrio.currentText())
    if(prios == "low"):
      p = 1
    if(prios == "high"):
      p = 300
    if(prios == "normal"):
      p = 150
    batchFlag = ("active" if(self.checkBatching.isChecked()) else "deactive")
    if(batchFlag == "active"):
      submitDict['batch'] = str(constants.batchActive)
    else:
      submitDict['batch'] = str(constants.batchDeactive)
    
    submitDict['minBatch'] = str(self.spinMinBatch.value())
    submitDict['maxBatch'] = str(self.spinMaxBatch.value())
    submitDict['priority'] = str(p)
      
    
    
    
    for x in self.fileTypeDefs:
      if(x['fileType'] == submitDict['fileType']):
        submitDict['afterFrameCmd'] = x['defAfterFrameCmd']
        submitDict['beforeFrameCmd'] = x['defBeforeFrameCmd']
    
    
    #if((submitDict['fileType'] == "3dsmax") and ((submitDict['os'] == "default") or (submitDict['os'] == "win"))):
      #submitDict['afterFrameCmd'] = "Z:/pythonTestWindoze.DONOTDELETE/rbhus/etc/3dsmax/afterFrame.py"
      #submitDict['beforeFrameCmd'] = "Z:/pythonTestWindoze.DONOTDELETE/rbhus/etc/3dsmax/beforeFrame.py"
    #elif((submitDict['fileType'] == "3dsmax2013") and ((submitDict['os'] == "default") or (submitDict['os'] == "win"))):
      #submitDict['afterFrameCmd'] = "Z:/pythonTestWindoze.DONOTDELETE/rbhus/etc/3dsmax2013/afterFrame.py"
      #submitDict['beforeFrameCmd'] = "Z:/pythonTestWindoze.DONOTDELETE/rbhus/etc/3dsmax2013/beforeFrame.py"
    #elif((submitDict['fileType'] == "3dsmax2013_test") and ((submitDict['os'] == "default") or (submitDict['os'] == "win"))):
      #submitDict['afterFrameCmd'] = "Z:/pythonTestWindoze.DONOTDELETE/rbhus/etc/3dsmax2013/afterFrame.py"
      #submitDict['beforeFrameCmd'] = "Z:/pythonTestWindoze.DONOTDELETE/rbhus/etc/3dsmax2013/beforeFrame.py"
      
      
      
    a = rUtils.tasks()
    
    for f in files.split(","):
      if(f):
        submitDict['fileName'] = f.lstrip().replace("\\","/")
        sd = submitdir.replace("\\","/")
        #submitDict['cameras'] = cameras
        
        
        if(re.search('^default$',sd) == None):
          sd = sd.rstrip("/") +"/"+ ".".join(str((submitDict['fileName']).split("/")[-1]).split(".")[0:-1]).rstrip().lstrip() +"/"
          print(str(sd))
          
          sdc = sd
          for c in cameras.split(","):
            if(c):
              submitDict['camera'] = c.lstrip().rstrip()
              if(re.search('^default$',submitDict['camera']) == None):
                sdc = sd.rstrip("/") +"/"+ c + "/"
              if(re.search('^default$',submitDict['resolution']) == None):
                sdc = sdc.rstrip("/") +"/"+ submitDict['resolution'] + "/"
              if(re.search('^default$',layers) == None):
                sdcd = sdc
                for l in layers.split(","):
                  sdcd = sdc.rstrip("/") +"/"+ l.lstrip().rstrip() + "/"
                  submitDict['layer'] = l
                  submitDict['outDir'] = sdcd
                  try:
                    b = a.submit(submitDict)
                    print("Submiting task : "+ str(b) +" : "+ str(submitDict['fileName']))
                  except:
                    print("Error inserting task : "+ str(sys.exc_info()))
              else:
                submitDict['outDir'] = sdc
                try:
                  b = a.submit(submitDict)
                  print("Submiting task : "+ str(b) +" : "+ str(submitDict['fileName']))
                except:
                  print("Error inserting task : "+ str(sys.exc_info()))
        else:
          for c in cameras.split(","):
            if(c):
              submitDict['camera'] = c.lstrip().rstrip()
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
    
    
