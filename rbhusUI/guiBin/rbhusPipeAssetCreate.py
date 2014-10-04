#!/usr/bin/python
from PyQt4 import QtCore, QtGui
import glob
import os
import sys
import time


dirSelf = os.path.dirname(os.path.realpath(__file__))
print(dirSelf)
sys.path.append(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep) + os.sep + "lib")


import rbhusPipeAssetCreateMod
print(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")
sys.path.append(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")
import dbPipe
import constantsPipe
import authPipe
import utilsPipe


try:
  _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
  _fromUtf8 = lambda s: s
  

class Ui_Form(rbhusPipeAssetCreateMod.Ui_MainWindow):
  def setupUi(self, Form):
    self.form = Form
    rbhusPipeAssetCreateMod.Ui_MainWindow.setupUi(self,Form)
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(_fromUtf8(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/rbhusPipe.svg")), QtGui.QIcon.Normal, QtGui.QIcon.On)
    Form.setWindowIcon(icon)
    
    self.username = None
    self.project = None
    self.directory = None
    try:
      self.username = os.environ['rbhusPipe_acl_user'].rstrip().lstrip()
    except:
      pass
    try:
      self.project = os.environ['rp_proj_projName']
    except:
      pass
    try:
      self.directory = os.environ['rp_proj_directory']
    except:
      pass
    
    self.center()
    #self.setProjTypes()
    self.comboSequence.currentIndexChanged.connect(self.setScene)
    self.dateEditDue.setDateTime(QtCore.QDateTime.currentDateTime())
    self.pushCreate.clicked.connect(self.cAss)
    self.checkAssName.clicked.connect(self.enableAssName)
    
    
    self.setDirectory()
    self.setAssTypes()
    self.setFileTypes()
    self.setNodeTypes()
    self.setSequence()
    self.setStageTypes()
    self.enableAssName()
    
    
    
  def center(self):
    Form.move(QtGui.QApplication.desktop().screen().rect().center()- Form.rect().center())

  def enableAssName(self):
    if(self.checkAssName.isChecked()):
      self.lineEditAssName.setEnabled(True)
    else:
      self.lineEditAssName.setEnabled(False)

  
  def cAss(self):
    assdict = {}
    if(self.lineEditAssName.text()):
      assdict['assName'] = str(self.lineEditAssName.text())
      
    assdict['assetType'] = str(self.comboAssType.currentText())
    assdict['projName'] = os.environ['rp_proj_projName']
    assdict['directory'] = str(self.comboDirectory.currentText())
    assdict['nodeType'] = str(self.comboNodeType.currentText())
    assdict['stageType'] = str(self.comboStageType.currentText())
    assdict['sequenceName'] = str(self.comboSequence.currentText())
    assdict['sceneName'] = str(self.comboScene.currentText())
    assdict['dueDate'] = str(self.dateEditDue.dateTime().date().year()) +"-"+ str(self.dateEditDue.dateTime().date().month()) +"-"+ str(self.dateEditDue.dateTime().date().day()) +" "+ str(self.dateEditDue.dateTime().time().hour()) +":"+ str(self.dateEditDue.dateTime().time().minute()) +":" + str(self.dateEditDue.dateTime().time().second())
    assdict['assignedWorker'] = str(self.lineEditWorkers.text())
    assdict['description'] = str(self.lineEditDesc.text())
    assdict['fileType'] = str(self.comboFileType.currentText())
    self.centralwidget.setEnabled(False)
    utilsPipe.assRegister(assdict)
    self.centralwidget.setEnabled(True)
    
    
    
    
  
  
  
  def setDirectory(self):
    dirs = utilsPipe.getDirMaps()
    self.comboDirectory.clear()
    if(dirs):
      for d in dirs:
        self.comboDirectory.addItem(_fromUtf8(d['directory']))
      return(1)
    return(0)
    
    
  def setStageTypes(self):
    rows = utilsPipe.getStageTypes()
    self.comboStageType.clear()  
    if(rows):
      for row in rows:
        self.comboStageType.addItem(_fromUtf8(row['type']))
      return(1)
    return(0)     
  
  
  
 
  
  
  def setScene(self):
    seqName = str(self.comboSequence.currentText())
    rows = utilsPipe.getSequenceScenes(os.environ['rp_proj_projName'],seq=seqName)
    self.comboScene.clear()
    scenes = {}
    if(rows):
      for x in rows:
        scenes[x['sceneName']] = 1
    if(scenes):
      for x in scenes:
        self.comboScene.addItem(_fromUtf8(x))
    return(1)
        
        
      
    
    
    
  
  
  def setSequence(self):
    rows = utilsPipe.getSequenceScenes(os.environ['rp_proj_projName'])
    self.comboSequence.clear()  
    seq = {}
    if(rows):
      for row in rows:
        if(row['projName'] == os.environ['rp_proj_projName']):
          seq[row['sequenceName']] = 1
      if(seq):
        for x in seq.keys():
          self.comboSequence.addItem(_fromUtf8(x))
      return(1)
    return(0)     
    
  
  def setNodeTypes(self):
    rows = utilsPipe.getNodeTypes()
    self.comboNodeType.clear()  
    if(rows):
      for row in rows:
        self.comboNodeType.addItem(_fromUtf8(row['type']))
      return(1)
    return(0)     
  
  
  def setFileTypes(self):
    rows = utilsPipe.getFileTypes()
    self.comboFileType.clear()  
    if(rows):
      for row in rows:
        self.comboFileType.addItem(_fromUtf8(row['type']))
      return(1)
    return(0)
  
  
  def setAssTypes(self):
    rows = utilsPipe.getAssTypes()
    self.comboAssType.clear()  
    if(rows):
      for row in rows:
        self.comboAssType.addItem(_fromUtf8(row['type']))
      return(1)
    return(0)
  
  def setDefaults(self):
    defs = utilsPipe.getProjDefaults()
    




if __name__ == "__main__":
  app = QtGui.QApplication(sys.argv)
  Form = QtGui.QMainWindow()
  ui = Ui_Form()
  ui.setupUi(Form)
  Form.show()
  sys.exit(app.exec_())
    