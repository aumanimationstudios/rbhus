#!/usr/bin/env python3
from PyQt5 import QtWidgets, QtCore, QtGui
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
import debug


try:
  _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
  _fromUtf8 = lambda s: s


def str_convert(text):
  if isinstance(text, bytes):
    return str(text, 'utf-8')
  return str(text)


class Ui_Form(rbhusPipeAssetCreateMod.Ui_MainWindow):
  def setupUi(self, Form):
    self.form = Form
    rbhusPipeAssetCreateMod.Ui_MainWindow.setupUi(self,Form)
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(str_convert(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/rbhusPipe.svg")), QtGui.QIcon.Normal, QtGui.QIcon.On)
    Form.setWindowIcon(icon)
    self.assetTypeRadios = []
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
    self.pushAssets.clicked.connect(self.getAssNames)
    
    
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
    Form.move(QtWidgets.QApplication.desktop().screen().rect().center()- Form.rect().center())

  def enableAssName(self):
    if(self.checkAssName.isChecked()):
      self.lineEditAssName.setEnabled(True)
      self.pushAssets.setEnabled(True)
    else:
      self.lineEditAssName.setEnabled(False)
      self.pushAssets.setEnabled(False)
  
  
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
    outScenes = subprocess.Popen([sys.executable,selectCheckBoxCmd,"-i",",".join(scenes),"-d",str_convert(self.lineEditScenes.text()).rstrip().lstrip()],stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].rstrip().lstrip()
    outScenes = str_convert(outScenes)
    if(outScenes == ""):
      outScenes = str_convert(self.lineEditScenes.text())
    self.lineEditScenes.setText(str_convert(outScenes))

  
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
    ntypes = str_convert(self.lineEditNodes.text()).split(",")
    assesNames = []
    for aT in self.assetTypeRadios:
      if(aT.isChecked()):
        assdict['assetType'] = str_convert(aT.text()).rstrip().lstrip()
        break
    else:
      debug.info("reached the end and no asset types - WTF!")

    if 'assetType' not in assdict:
      QtWidgets.QMessageBox.critical(self.form,"WTF!!!","assetType not selected. Please select one")
      self.centralwidget.setEnabled(True)
      self.centralwidget.setCursor(QtCore.Qt.ArrowCursor)
      return
    assdict['projName'] = os.environ['rp_proj_projName'].rstrip().lstrip()
    assdict['directory'] = str(self.comboDirectory.currentText()).rstrip().lstrip()
    assdict['stageType'] = str(self.comboStageType.currentText()).rstrip().lstrip()
    assdict['sequenceName'] = str(self.comboSequence.currentText()).rstrip().lstrip()
    sN = str_convert(self.lineEditScenes.text()).rstrip().lstrip()
    assdict['dueDate'] = str(self.dateEditDue.dateTime().date().year()) +"-"+ str(self.dateEditDue.dateTime().date().month()) +"-"+ str(self.dateEditDue.dateTime().date().day()) +" "+ str(self.dateEditDue.dateTime().time().hour()) +":"+ str(self.dateEditDue.dateTime().time().minute()) +":" + str(self.dateEditDue.dateTime().time().second()).rstrip().lstrip()
    assdict['assignedWorker'] = str_convert(self.lineEditWorkers.text()).rstrip().lstrip()
    assdict['description'] = str_convert(self.lineEditDesc.text()).rstrip().lstrip()
    assdict['tags'] = str_convert(self.lineEditTags.text()).rstrip().lstrip()
    assdict['fRange'] = str_convert(self.lineEditFRange.text()).rstrip().lstrip()
    assdict['reviewUser'] = str_convert(self.lineEditReviewers.text()).rstrip().lstrip()
    if(self.checkVersion.isChecked()):
      assdict['versioning'] = 1
    else:
      assdict['versioning'] = 0
    self.centralwidget.setEnabled(False)
    if str_convert(self.lineEditAssName.text()):
      assesNames = str_convert(self.lineEditAssName.text()).split(",")
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
    outTags = subprocess.Popen([sys.executable,selectCheckBoxCmd,"-i",",".join(tags),"-d",str_convert(self.lineEditTags.text()).rstrip().lstrip()],stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].rstrip().lstrip()
    outTags = str_convert(outTags)
    if(outTags == ""):
      outTags = "default"
    self.lineEditTags.setText(str_convert(outTags))
  
  
  def getAssNames(self):
    asses = utilsPipe.getDistinctAssNames(projName=os.environ['rp_proj_projName'])
    if(asses):
      selectedAss = subprocess.Popen([sys.executable,selectCheckBoxCmd,"-i",",".join(asses),"-d",str_convert(self.lineEditAssName.text()).rstrip().lstrip()],stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].rstrip().lstrip()
      selectedAss = str_convert(selectedAss)
      if (selectedAss == ""):
        selectedAss = ""
      self.lineEditAssName.setText(str_convert(selectedAss))


  def setUsers(self):
    users = utilsPipe.getUsers()
    outUsers = subprocess.Popen([sys.executable,selectRadioBoxCmd,"-i",",".join(users),"-d",str_convert(self.lineEditWorkers.text()).rstrip().lstrip()],stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].rstrip().lstrip()
    outUsers = str_convert(outUsers)
    if(outUsers == ""):
      outUsers = str(self.lineEditWorkers.text()).rstrip().lstrip()
    self.lineEditWorkers.setText(str_convert(outUsers))


  def setReviewers(self):
    users = utilsPipe.getUsers()
    outUsers = subprocess.Popen([sys.executable,selectRadioBoxCmd,"-i",",".join(users),"-d",str_convert(self.lineEditWorkers.text()).rstrip().lstrip()],stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].rstrip().lstrip()
    outUsers = str_convert(outUsers)
    if(outUsers == ""):
      outUsers = str(self.lineEditReviewers.text()).rstrip().lstrip()
    self.lineEditReviewers.setText(str_convert(outUsers))

  
  
  def setDirectory(self):
    dirs = utilsPipe.getDirMaps()
    self.comboDirectory.clear()
    i = 0
    foundIndx = 0
    if(dirs):
      for d in dirs:
        if(d['directory'] == self.projDets['directory']):
          foundIndx = i
        self.comboDirectory.addItem(str_convert(d['directory']))
        i = i + 1
      self.comboDirectory.setCurrentIndex(foundIndx)
      return(1)
    return(0)
    
    
  def setStageTypes(self):
    rows = utilsPipe.getStageTypes()
    self.comboStageType.clear()  
    if(rows):
      for row in rows:
        self.comboStageType.addItem(str_convert(row['type']))
      return(1)
    return(0)     
  

  def setSequence(self):
    rows = utilsPipe.getSequenceScenes(os.environ['rp_proj_projName'])
    self.comboSequence.clear()  
    seq = {}
    if(rows):
      for row in rows:
        if(row['projName'] == os.environ['rp_proj_projName']):
          seq[row['sequenceName']] = 1
      if(seq):
        for x in list(seq.keys()):
          self.comboSequence.addItem(str_convert(x))
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
    
    defNodes =[str(df.split("#")[0]) for df in str_convert(self.lineEditNodes.text()).split(",")]
    print(sys.executable,selectCheckBoxComboCmd,"-i",",".join(ntypes),"-c",",".join(ftypes),"-d",str_convert(self.lineEditNodes.text()))
    outNodes = subprocess.Popen([sys.executable,selectCheckBoxComboCmd,"-i",",".join(ntypes),"-c",",".join(ftypes),"-d",str_convert(self.lineEditNodes.text())],stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].rstrip().lstrip()
    outNodes = str_convert(outNodes)
    if(outNodes == ""):
      outNodes = str_convert(self.lineEditNodes.text())
    self.lineEditNodes.setText(str_convert(outNodes))
  

  def setAssTypes(self):
    rows = utilsPipe.getAssTypes(status=constantsPipe.typesAll)
    if(rows):
      for row in rows:
        radioButton = QtWidgets.QRadioButton()
        radioButton.setObjectName("radio_"+ str_convert(row['type']))
        radioButton.setText(str_convert(row['type']))
        self.horizontalLayout_3.addWidget(radioButton)
        self.assetTypeRadios.append(radioButton)
      return(1)
    return(0)
  
  def setDefaults(self):
    defs = utilsPipe.getProjDefaults()
    




if __name__ == "__main__":
  app = QtWidgets.QApplication(sys.argv)
  Form = QtWidgets.QMainWindow()
  ui = Ui_Form()
  ui.setupUi(Form)
  Form.show()
  sys.exit(app.exec_())
    