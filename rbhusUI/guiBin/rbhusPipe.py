#!/usr/bin/python
from PyQt4 import QtCore, QtGui
import os
import sys
import tempfile
import time
import subprocess


dirSelf = os.path.dirname(os.path.realpath(__file__))
print(dirSelf)
sys.path.append(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep) + os.sep + "lib")

tempDir = tempfile.gettempdir()
rpA = "rbhusPipeProjCreate.py"
rpAss = "rbhusPipeAssetCreate.py"
srb = "selectRadioBox.py"
rpS = "rbhusPipeSeqSceCreate.py"  
rbhusPipeProjCreateCmd = dirSelf.rstrip(os.sep) + os.sep + rpA
rbhusPipeAssetCreateCmd = dirSelf.rstrip(os.sep) + os.sep + rpAss
rbhusPipeSeqSceCreateCmd = dirSelf.rstrip(os.sep) + os.sep + rpS




selectRadioBoxCmd = dirSelf.rstrip(os.sep) + os.sep + srb
selectRadioBoxCmd = selectRadioBoxCmd.replace("\\","/")


import rbhusPipeMainMod
print(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")
sys.path.append(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")
import constantsPipe
import authPipe
import dbPipe
import utilsPipe

try:
  _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
  _fromUtf8 = lambda s: s
  

class Ui_Form(rbhusPipeMainMod.Ui_MainWindow):
  def setupUi(self, Form):
    rbhusPipeMainMod.Ui_MainWindow.setupUi(self,Form)
    self.authL = authPipe.login()
    self.username = None
    self.center()
    try:
      self.username = os.environ['rbhusPipe_acl_user'].rstrip().lstrip()
    except:
      pass
    
    
    iconRefresh = QtGui.QIcon()
    iconRefresh.addPixmap(QtGui.QPixmap(_fromUtf8(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/ic_action_refresh.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
    self.assRefresh.setIcon(iconRefresh)
    
    
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(_fromUtf8(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/rbhusPipe.svg")), QtGui.QIcon.Normal, QtGui.QIcon.On)
    Form.setWindowIcon(icon)
    self.pushLogout.setText("logout : "+ str(self.username))
    self.pushLogout.clicked.connect(self.logout)
    self.form = Form
    self.wFlag = self.form.windowFlags()
    self.trayIcon = QtGui.QSystemTrayIcon(QtGui.QIcon(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/rbhusPipe.svg"))
    self.trayIcon.show()
    
    self.trayMenu = QtGui.QMenu()
    
    
    
    
    self.quitAction = self.trayMenu.addAction("quit")
    self.quitAction.triggered.connect(self.quitFunc)
    
    self.trayIcon.setContextMenu(self.trayMenu)
    self.trayIcon.activated.connect(self.showMain)
    
    self.actionNew_project.triggered.connect(self.rbhusPipeProjCreate)
    self.actionSet_project.triggered.connect(self.rbhusPipeSetProject)
    self.actionNew_seq_scn.triggered.connect(self.rbhusPipeSeqSceCreate)
    self.pushNewAsset.clicked.connect(self.rbhusPipeAssetCreate)
    self.comboSequence.currentIndexChanged.connect(self.setScene)
    
    
    
    
    
    #self.form.closeEvent = self.closeEvent
    self.form.hideEvent = self.hideEvent
    self.setStageTypes()
    self.setNodeTypes()
    self.setFileTypes()
    self.setAssTypes()
    
    # set up the right-click context menu for listWidget
    self.listWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    self.listWidget.customContextMenuRequested.connect(self.popupAss)
    
  
  def popupAss(self, pos):
    menu = QtGui.QMenu()
    openFileAction = menu.addAction("open file")
    openFolderAction = menu.addAction("open folder")
    newFolderAction = menu.addAction("new folder")
    assEditAction = menu.addAction("edit")
    assDeleteAction = menu.addAction("delete")
    
    action = menu.exec_(self.listWidget.mapToGlobal(pos))
    if(action == openFileAction):
      self.openFileAss()
    if(action == openFolderAction):
      self.openFolderAss()
    if(action == newFolderAction):
      self.newFolderAss()
    if(action == assEditAction):
      self.editAss()
    if(action == assDeleteAction):
      self.delAss()
  
  
  
  def openFileAss(self):
    listAsses = self.listWidget.selectedItems()
    
    for x in listAsses:
      print(x.text())
    print(listAsses)
    
  
  def openFolderAss(self):
    pass
  
  
  def newFolderAss(self):
    pass
  
  
  def editAss(self):
    pass
  
  
  def delAss(self):
    pass
  
  
  
  
  
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
  
  
  
  def rbhusPipeProjCreate(self):
    p = QtCore.QProcess(parent=self.form)
    p.setStandardOutputFile(tempDir + os.sep +"rbhusPipeProjCreate_"+ self.username +".log")
    p.setStandardErrorFile(tempDir + os.sep +"rbhusPipeProjCreate_"+ self.username +".err")
    self.actionNew_project.setEnabled(False)
    p.start(sys.executable,rbhusPipeProjCreateCmd.split())
    p.finished.connect(self.rbhusPipeProjCreateEnable)
    
    
  
  def listAssets(self):
    self.listWidget.clear()
    asses = utilsPipe.getProjAsses(os.environ['rp_proj_projName'])
    print(asses)
    if(asses):
      for x in range(0,len(asses)):
        item = QtGui.QListWidgetItem()
        item.setText(asses[x]['path'])
        self.listWidget.addItem(item)
        
    
    
  
  
  def rbhusPipeSeqSceCreate(self):
    p = QtCore.QProcess(parent=self.form)
    p.setStandardOutputFile(tempDir + os.sep +"rbhusPipeSeqSceCreate_"+ self.username +".log")
    p.setStandardErrorFile(tempDir + os.sep +"rbhusPipeSeqSceCreate_"+ self.username +".err")
    self.actionNew_seq_scn.setEnabled(False)
    p.start(sys.executable,rbhusPipeSeqSceCreateCmd.split())
    p.finished.connect(self.rbhusPipeSeqSceCreateEnable)
  
  
  
  def rbhusPipeAssetCreate(self):
    p = QtCore.QProcess(parent=self.form)
    p.setStandardOutputFile(tempDir + os.sep +"rbhusPipeAssetCreate_"+ self.username +".log")
    p.setStandardErrorFile(tempDir + os.sep +"rbhusPipeAssetCreate_"+ self.username +".err")
    self.pushNewAsset.setEnabled(False)
    p.start(sys.executable,rbhusPipeAssetCreateCmd.split())
    p.finished.connect(self.rbhusPipeAssCreateEnable)
    
  
  
  def rbhusPipeSetProject(self):
    projNames = []
    projects = utilsPipe.getProjDetails(status="all")
    for x in projects:
      projNames.append(x['projName'])
      
    
    projN = subprocess.Popen([sys.executable,selectRadioBoxCmd,"-i",",".join(projNames)],stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].rstrip().lstrip()
    print(projN)
    if(not projN):
      return(0)
    utilsPipe.exportProj(projN)
    self.form.setWindowTitle(projN)
    self.actionSet_project.setText("set project ("+ projN +")")
    for x in os.environ.keys():
      if(x.find("rp_") >= 0):
        print(x +":"+ str(os.environ[x]))
      
    self.setSequence()
    self.listAssets()
  
  def rbhusPipeProjCreateEnable(self,exitStatus):
    self.actionNew_project.setEnabled(True)
    
  def rbhusPipeAssCreateEnable(self,exitStatus):
    self.pushNewAsset.setEnabled(True)
  
  def rbhusPipeSeqSceCreateEnable(self,exitStatus):
    self.actionNew_seq_scn.setEnabled(True)
  
  
  def closeEvent(self,event):
    event.ignore()
    QtGui.QMessageBox.about(self.form,"QUITING?","Minimizing to Tray .\nPlease quit from the tray icon if you really want to quit!")
    self.form.setVisible(False) 
    
  def hideEvent(self,event):
    #event.ignore()
    self.form.setVisible(False) 
    self.form.setWindowFlags(self.wFlag & QtCore.Qt.Tool)
    
   
  
  def showMain(self,actReason):
    if(actReason == 2):
      self.form.setVisible(True)
      self.form.setWindowFlags(self.wFlag)
    

  def logout(self):
    self.authL.logout()
    QtCore.QCoreApplication.instance().quit()
  
  def quitFunc(self):
    QtCore.QCoreApplication.instance().quit()
  
  
  def center(self):
    Form.move(QtGui.QApplication.desktop().screen().rect().center()- Form.rect().center())
      
    
if __name__ == "__main__":
  import sys
  app = QtGui.QApplication(sys.argv)
  Form = QtGui.QMainWindow()
  ui = Ui_Form()
  ui.setupUi(Form)
  Form.show()
  sys.exit(app.exec_())
