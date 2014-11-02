#!/usr/bin/python
from PyQt4 import QtCore, QtGui
import glob
import os
import sys
import time
import subprocess
import argparse


dirSelf = os.path.dirname(os.path.realpath(__file__))
print(dirSelf)
sys.path.append(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep) + os.sep + "lib")


scb = "selectCheckBox.py"

selectCheckBoxCmd = dirSelf.rstrip(os.sep) + os.sep + scb





import rbhusPipeAssetEditMod
print(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")
sys.path.append(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")
import dbPipe
import constantsPipe
import authPipe
import utilsPipe






parser = argparse.ArgumentParser()
parser.add_argument("-i","--id",dest='assId',help='comma seperated asset id list')
parser.add_argument("-p","--path",dest='assPath',help='comma seperated asset path list')
args = parser.parse_args()




try:
  _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
  _fromUtf8 = lambda s: s
  

class Ui_Form(rbhusPipeAssetEditMod.Ui_MainWindow):
  def setupUi(self, Form):
    self.form = Form
    rbhusPipeAssetEditMod.Ui_MainWindow.setupUi(self,Form)
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(_fromUtf8(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/rbhusPipe.svg")), QtGui.QIcon.Normal, QtGui.QIcon.On)
    Form.setWindowIcon(icon)
    
    self.idList = []
    self.pathList = []
    self.updateLine = []
    
    if(args.assId):
      self.idList = args.assId.split(",")
    if(args.assPath):
      self.pathList = args.assPath.split(",")
    
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
    self.pushTags.clicked.connect(self.setTags)
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

  
  def eAss(self):
    if(self.idList):
      for xid in self.idList:
        assdict = {}
        assdict['dueDate'] = str(self.dateEditDue.dateTime().date().year()) +"-"+ str(self.dateEditDue.dateTime().date().month()) +"-"+ str(self.dateEditDue.dateTime().date().day()) +" "+ str(self.dateEditDue.dateTime().time().hour()) +":"+ str(self.dateEditDue.dateTime().time().minute()) +":" + str(self.dateEditDue.dateTime().time().second())
        assdict['assignedWorker'] = str(self.lineEditWorkers.text())
        assdict['description'] = str(self.lineEditDesc.text())
        assdict['tags'] = str(self.lineEditTags.text())
        assdict['fRange'] = str(self.lineEditFRange.text())
        self.centralwidget.setEnabled(False)
        utilsPipe.assEdit(assid = xid , assdict=assdict)
     if(self.pathList):
      for xpath in self.pathList:
        assdict = {}
        assdict['dueDate'] = str(self.dateEditDue.dateTime().date().year()) +"-"+ str(self.dateEditDue.dateTime().date().month()) +"-"+ str(self.dateEditDue.dateTime().date().day()) +" "+ str(self.dateEditDue.dateTime().time().hour()) +":"+ str(self.dateEditDue.dateTime().time().minute()) +":" + str(self.dateEditDue.dateTime().time().second())
        assdict['assignedWorker'] = str(self.lineEditWorkers.text())
        assdict['description'] = str(self.lineEditDesc.text())
        assdict['tags'] = str(self.lineEditTags.text())
        assdict['fRange'] = str(self.lineEditFRange.text())
        self.centralwidget.setEnabled(False)
        utilsPipe.assEdit(asspath = xpath , assdict=assdict)
    self.centralwidget.setEnabled(True)
    
    
    
    
  def setTags(self):
    tags = utilsPipe.getTags(projName=os.environ['rp_proj_projName'])
    outTags = subprocess.Popen([sys.executable,selectCheckBoxCmd,"-i",",".join(tags),"-d",str(self.lineEditTags.text()).rstrip().lstrip()],stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].rstrip().lstrip()
    if(outTags == ""):
      outTags = "default"
    self.lineEditTags.setText(_fromUtf8(outTags))
  
  
  
  
  
  
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
    rowsStage = utilsPipe.getStageTypes(stype=str(self.comboStageType.currentText()))
    print(rowsStage)
    stageDefNodes = rowsStage['validNodeTypes']
    self.lineEditNodes.setText(stageDefNodes)
    return(1)
  
  def setNodes(self):
    ntypes = [str(x['type']) for x in utilsPipe.getNodeTypes()]
    outNodes = subprocess.Popen([sys.executable,selectCheckBoxCmd,"-i",",".join(ntypes),"-d",str(self.lineEditNodes.text()).rstrip().lstrip()],stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].rstrip().lstrip()
    if(outNodes == ""):
      outNodes = str(self.lineEditNodes.text())
    self.lineEditNodes.setText(_fromUtf8(outNodes))  
  
  
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
    