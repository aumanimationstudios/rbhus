#!/usr/bin/python
from PyQt4 import QtCore, QtGui
import glob
import os
import sys
import time
import subprocess


dirSelf = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep) + os.sep + "lib")


scb = "selectCheckBox.py"
scbc = "selectCheckBoxCombo.py"
srb = "selectRadioBox.py"
selectCheckBoxCmd = dirSelf.rstrip(os.sep) + os.sep + scb
selectRadioBoxCmd = dirSelf.rstrip(os.sep) + os.sep + srb
selectCheckBoxComboCmd = dirSelf.rstrip(os.sep) + os.sep + scbc





import rbhusPipeAssetCreateMod
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
      self.projDets = utilsPipe.getProjDetails(projName = self.project)
    except:
      pass
    try:
      self.directory = os.environ['rp_proj_directory']
    except:
      pass
    
    
    
    
    self.center()
    #self.setProjTypes()
    self.comboSequence.currentIndexChanged.connect(self.setSceneTemp)
    self.dateEditDue.setDateTime(QtCore.QDateTime.currentDateTime())
    self.comboStageType.currentIndexChanged.connect(self.setNodeTypes)
    self.pushCreate.clicked.connect(self.cAss)
    self.pushTags.clicked.connect(self.setTags)
    self.pushUsers.clicked.connect(self.setUsers)
    self.pushReviewers.clicked.connect(self.setReviewers)
    self.pushNodes.clicked.connect(self.setNodes)
    self.pushScenes.clicked.connect(self.setScene)
    self.checkAssName.clicked.connect(self.enableAssName)
    self.checkAssignSelf.clicked.connect(self.setAssignedWorker)
    self.checkReviewSelf.clicked.connect(self.setReviewerSelf)
    
    
    self.setDirectory()
    self.setAssTypes()
    #self.setFileTypes()
    #self.setNodeTypes()
    self.setSequence()
    self.setStageTypes()
    self.enableAssName()
    self.setAssignedWorker()
    self.setReviewerSelf()
    
    
    
  def center(self):
    Form.move(QtGui.QApplication.desktop().screen().rect().center()- Form.rect().center())

  def enableAssName(self):
    if(self.checkAssName.isChecked()):
      self.lineEditAssName.setEnabled(True)
    else:
      self.lineEditAssName.setEnabled(False)
  
  
  def setSceneTemp(self):
    seqName = str(self.comboSequence.currentText())
    rows = utilsPipe.getSequenceScenes(os.environ['rp_proj_projName'],seqName)
    scenes = []
    if(rows):
      for x in rows:
        if(x['sceneName'].rstrip().lstrip()):
          scenes.append(x['sceneName'])
    if(scenes):
      self.lineEditScenes.setText(scenes[0])
  
  def setScene(self):
    seqName = str(self.comboSequence.currentText())
    rows = utilsPipe.getSequenceScenes(os.environ['rp_proj_projName'],seqName)
    scenes = []
    if(rows):
      for x in rows:
        if(x['sceneName'].rstrip().lstrip()):
          scenes.append(x['sceneName'])
    outScenes = subprocess.Popen([sys.executable,selectCheckBoxCmd,"-i",",".join(scenes),"-d",str(self.lineEditScenes.text()).rstrip().lstrip()],stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].rstrip().lstrip()
    if(outScenes == ""):
      outScenes = self.lineEditScenes.text()
    self.lineEditScenes.setText(_fromUtf8(outScenes))
    #self.comboScene.clear()
    #scenes = {}
    #indx =  0
    #foundIndx = -1
    #rows = utilsPipe.getSequenceScenes(os.environ['rp_proj_projName'],seqName)
    #if(rows):
      #for x in rows:
        #scenes[x['sceneName']] = 1
    #if(scenes):
      #model = QtGui.QStandardItemModel(len(scenes),1)
      #for x in scenes:
        #item = QtGui.QStandardItem(x)
        #item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        #item.setData(QtCore.Qt.Unchecked, QtCore.Qt.CheckStateRole)
        #model.setItem(indx,0,item)
        #abrush = QtGui.QBrush()
        #color = QtGui.QColor()
        #color.setAlpha(0)
        #abrush.setColor(color)
        #model.item(indx).setForeground(abrush)
        #indx = indx + 1
      #model.itemChanged.connect(self.itemChangedScenes)
      #self.comboScene.setModel(model)
      #self.comboScene.setEditText("default")
      #return(1)
    #return(0)
  
  
  def setAssignedWorker(self):
    if(self.checkAssignSelf.isChecked()):
      self.lineEditWorkers.setText(str(self.username))
      self.lineEditWorkers.setEnabled(False)
      self.pushUsers.setEnabled(False)
    else:
      self.lineEditWorkers.setEnabled(True)
      self.pushUsers.setEnabled(True)


  def setReviewerSelf(self):
    if(self.checkReviewSelf.isChecked()):
      self.lineEditReviewers.setText(str(self.username))
      self.lineEditReviewers.setEnabled(False)
      self.pushReviewers.setEnabled(False)
    else:
      self.lineEditReviewers.setEnabled(True)
      self.pushReviewers.setEnabled(True)


  
  def cAss(self):
    self.centralwidget.setCursor(QtCore.Qt.WaitCursor)
    assdict = {}
    ntypes = str(self.lineEditNodes.text()).split(",")
    assesNames = []
    assdict['assetType'] = str(self.comboAssType.currentText()).rstrip().lstrip()
    assdict['projName'] = os.environ['rp_proj_projName'].rstrip().lstrip()
    assdict['directory'] = str(self.comboDirectory.currentText()).rstrip().lstrip()
    assdict['stageType'] = str(self.comboStageType.currentText()).rstrip().lstrip()
    assdict['sequenceName'] = str(self.comboSequence.currentText()).rstrip().lstrip()
    sN = str(self.lineEditScenes.text()).rstrip().lstrip()
    assdict['dueDate'] = str(self.dateEditDue.dateTime().date().year()) +"-"+ str(self.dateEditDue.dateTime().date().month()) +"-"+ str(self.dateEditDue.dateTime().date().day()) +" "+ str(self.dateEditDue.dateTime().time().hour()) +":"+ str(self.dateEditDue.dateTime().time().minute()) +":" + str(self.dateEditDue.dateTime().time().second()).rstrip().lstrip()
    assdict['assignedWorker'] = str(self.lineEditWorkers.text()).rstrip().lstrip()
    assdict['description'] = str(self.lineEditDesc.text()).rstrip().lstrip()
    assdict['tags'] = str(self.lineEditTags.text()).rstrip().lstrip()
    assdict['fRange'] = str(self.lineEditFRange.text()).rstrip().lstrip()
    assdict['reviewUser'] = str(self.lineEditReviewers.text()).rstrip().lstrip()
    if(self.checkVersion.isChecked()):
      assdict['versioning'] = 1
    else:
      assdict['versioning'] = 0
    self.centralwidget.setEnabled(False)
    if(self.lineEditAssName.text()):
      assesNames = str(self.lineEditAssName.text()).split(",")
      for aN in assesNames:
        if(aN):
          assdict['assName'] = aN.rstrip().lstrip()
          for s in sN.split(","):
            if(s.rstrip().lstrip()):
              assdict['sceneName'] = s.rstrip().lstrip()
              
              for x in ntypes:
                assdict['nodeType'] = x.split("#")[0].rstrip().lstrip()
                if(len(x.split("#")) > 1):
                  for ft in (x.split("#")[1]).split("%"):
                    assdict['fileType'] = ft.rstrip().lstrip()
                    utilsPipe.assRegister(assdict)
                else:
                  assdict['fileType'] = "default"
                  utilsPipe.assRegister(assdict)
    else:
      for s in sN.split(","):
        if(s.rstrip().lstrip()):
          assdict['sceneName'] = s.rstrip().lstrip()
      
          for x in ntypes:
            assdict['nodeType'] = x.split("#")[0].rstrip().lstrip()
            if(len(x.split("#")) > 1):
              for ft in (x.split("#")[1]).split("%"):
                assdict['fileType'] = ft.rstrip().lstrip()
                utilsPipe.assRegister(assdict)
            else:
              assdict['fileType'] = "default"
              utilsPipe.assRegister(assdict)

    self.centralwidget.setEnabled(True)
    self.centralwidget.setCursor(QtCore.Qt.ArrowCursor)
    
    
    
  def setTags(self):
    tags = utilsPipe.getTags(projName=os.environ['rp_proj_projName'])
    outTags = subprocess.Popen([sys.executable,selectCheckBoxCmd,"-i",",".join(tags),"-d",str(self.lineEditTags.text()).rstrip().lstrip()],stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].rstrip().lstrip()
    if(outTags == ""):
      outTags = "default"
    self.lineEditTags.setText(_fromUtf8(outTags))
  
  
  
  def setUsers(self):
    users = utilsPipe.getUsers()
    outUsers = subprocess.Popen([sys.executable,selectRadioBoxCmd,"-i",",".join(users),"-d",str(self.lineEditWorkers.text()).rstrip().lstrip()],stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].rstrip().lstrip()
    if(outUsers == ""):
      outUsers = str(self.lineEditWorkers.text()).rstrip().lstrip()
    self.lineEditWorkers.setText(_fromUtf8(outUsers))


  def setReviewers(self):
    users = utilsPipe.getUsers()
    outUsers = subprocess.Popen([sys.executable,selectRadioBoxCmd,"-i",",".join(users),"-d",str(self.lineEditWorkers.text()).rstrip().lstrip()],stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].rstrip().lstrip()
    if(outUsers == ""):
      outUsers = str(self.lineEditReviewers.text()).rstrip().lstrip()
    self.lineEditReviewers.setText(_fromUtf8(outUsers))

  
  
  def setDirectory(self):
    dirs = utilsPipe.getDirMaps()
    self.comboDirectory.clear()
    i = 0
    foundIndx = 0
    if(dirs):
      for d in dirs:
        if(d['directory'] == self.projDets['directory']):
          foundIndx = i
        self.comboDirectory.addItem(_fromUtf8(d['directory']))
        i = i + 1
      self.comboDirectory.setCurrentIndex(foundIndx)
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
  
  
  
 
  
  
  #def setScene(self):
    #seqName = str(self.comboSequence.currentText())
    #rows = utilsPipe.getSequenceScenes(os.environ['rp_proj_projName'],seq=seqName)
    #self.comboScene.clear()
    #scenes = {}
    #if(rows):
      #for x in rows:
        #scenes[x['sceneName']] = 1
    #if(scenes):
      #for x in scenes:
        #self.comboScene.addItem(_fromUtf8(x))
    #return(1)
        
        
      
    
    
    
  
  
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
    rowsNodes = utilsPipe.getNodeTypes()
    
    print(rowsStage)
    stageDefNodes = rowsStage['validNodeTypes'].split(",")
    editNodes = []
    for sdf in stageDefNodes:
      for rn in rowsNodes:
        if(sdf == rn['type']):
          editNodes.append(sdf +"#"+"%".join(rn['defaultFileType'].split(",")))
          
    self.lineEditNodes.setText(",".join(editNodes))
    return(1)
  
  def setNodes(self):
    ntypes = [str(x['type']) for x in utilsPipe.getNodeTypes()]
    ftypes = [str(x['type']) for x in utilsPipe.getFileTypes()]
    
    defNodes =[str(df.split("#")[0]) for df in self.lineEditNodes.text().split(",")]
    print(sys.executable,selectCheckBoxComboCmd,"-i",",".join(ntypes),"-c",",".join(ftypes),"-d",str(self.lineEditNodes.text()))
    outNodes = subprocess.Popen([sys.executable,selectCheckBoxComboCmd,"-i",",".join(ntypes),"-c",",".join(ftypes),"-d",str(self.lineEditNodes.text())],stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].rstrip().lstrip()
    
    if(outNodes == ""):
      outNodes = str(self.lineEditNodes.text())
    self.lineEditNodes.setText(_fromUtf8(outNodes))
  
  
  #def setFileTypes(self):
    #rows = utilsPipe.getFileTypes()
    #self.comboFileType.clear()  
    #if(rows):
      #for row in rows:
        #self.comboFileType.addItem(_fromUtf8(row['type']))
      #return(1)
    #return(0)
  
  
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
    