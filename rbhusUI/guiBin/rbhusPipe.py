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
fileSelect = "fileSelectUI.py"
rbhusPipeProjCreateCmd = dirSelf.rstrip(os.sep) + os.sep + rpA
rbhusPipeAssetCreateCmd = dirSelf.rstrip(os.sep) + os.sep + rpAss
rbhusPipeSeqSceCreateCmd = dirSelf.rstrip(os.sep) + os.sep + rpS
fileSelectCmd = dirSelf.rstrip(os.sep) + os.sep + fileSelect



selectRadioBoxCmd = dirSelf.rstrip(os.sep) + os.sep + srb
selectRadioBoxCmd = selectRadioBoxCmd.replace("\\","/")


import rbhusPipeMainMod
print(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")
sys.path.append(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")
import constantsPipe
import authPipe
import dbPipe
import utilsPipe
import pyperclip

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
    self.filterRefresh.setIcon(iconRefresh)
    
    
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
    self.assRefresh.clicked.connect(self.updateAll)
    
    self.comboStageType.currentIndexChanged.connect(self.listAssets)
    self.comboNodeType.currentIndexChanged.connect(self.listAssets)
    self.comboScene.currentIndexChanged.connect(self.listAssets)
    self.comboAssType.currentIndexChanged.connect(self.listAssets)
    self.comboFileType.currentIndexChanged.connect(self.listAssets)
    
    
    self.radioAllAss.toggled.connect(self.listAssets)
    self.radioMineAss.toggled.connect(self.listAssets)
    
    
    self.lineEditSearch.returnPressed.connect(self.listAssets)
    
    self.checkBoxFilter.clicked.connect(self.checkFilerFunc)
    
    
    #self.form.closeEvent = self.closeEvent
    self.checkFilerFunc()
    self.rbhusPipeSetProjDefault()
    self.form.hideEvent = self.hideEvent
    self.form.closeEvent = self.hideEvent
    self.setStageTypes()
    self.setNodeTypes()
    self.setFileTypes()
    self.setAssTypes()
    
    # set up the right-click context menu for listWidget
    self.listWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    self.listWidget.customContextMenuRequested.connect(self.popupAss)
    
    
    self.timer = QtCore.QTimer()
    self.timer.timeout.connect(self.updateAll)
    self.checkRefresh.clicked.connect(self.timeCheck)
  
  def timeCheck(self):
    cRefresh = self.checkRefresh.isChecked()
    if(cRefresh):
      self.startTimer()
    else:
      self.stopTimer()
  
  def startTimer(self):
    self.timer.start(5000)

  def stopTimer(self):
    self.timer.stop()
  
  
  def checkFilerFunc(self):
    if(self.checkBoxFilter.isChecked()):
      self.groupBoxFilter.setVisible(True)
    else:
      self.groupBoxFilter.setVisible(False)
    
  def popupAss(self, pos):
    menu = QtGui.QMenu()
    openFileAction = menu.addAction("open file")
    openFolderAction = menu.addAction("open folder")
    #newFolderAction = menu.addAction("new folder")
    assEditAction = menu.addAction("edit")
    assCopyToClip = menu.addAction("copy path to clipboard")
    assCopyNew = menu.addAction("copy/new")
    assDeleteAction = menu.addAction("delete")
    
    action = menu.exec_(self.listWidget.mapToGlobal(pos))
    if(action == openFileAction):
      self.openFileAss()
    if(action == openFolderAction):
      self.openFolderAss()
    if(action == assCopyToClip):
      self.copyPathToClip()
    if(action == assEditAction):
      self.editAss()
    if(action == assDeleteAction):
      self.delAss()
    if(action == assCopyNew):
      self.copyNewAss()
      
      
  def copyNewAss(self):
    pass
    
  
  def copyPathToClip(self):
    listAsses = self.listWidget.selectedItems()
    if(listAsses and (len(listAsses) == 1)):
      x = str(listAsses[0].text())
      abspath =  utilsPipe.getAbsPath(x)
      pyperclip.copy(abspath)
      
  
  def openFileAss(self):
    listAsses = self.listWidget.selectedItems()
    fcmd = fileSelectCmd
    if(listAsses and (len(listAsses) == 1)):
      x = str(listAsses[0].text())
      fcmd = fcmd +" "+ utilsPipe.getAbsPath(x)
      print(fcmd)
      p = QtCore.QProcess(parent=self.form)
      #p.setStandardOutputFile(tempDir + os.sep +"rbhusOpenFileAss_"+ self.username +".log")
      p.setStandardErrorFile(tempDir + os.sep +"rbhusOpenFileAss_"+ self.username +".err")
      p.start(sys.executable,fcmd.split())
      p.waitForFinished()
      filename = str(p.readAllStandardOutput()).rstrip().lstrip()
      if(filename):
        assdets = utilsPipe.getAssDetails(assPath=x)
        runCmd = utilsPipe.openAssetCmd(assdets,filename)
        print("wtf1 : "+ str(runCmd))
        fileTypeDets = None
        if(runCmd):
          runCmd = runCmd.rstrip().lstrip()
          subprocess.Popen(runCmd,shell=True)
        else:
          import webbrowser
          webbrowser.open(filename)
      
      
      
      
      #f = os.popen("python "+ cwd +"/lib/fileSelectUI.py \""+ filePath +"\"")
      #elif(typeSelected == "maya"):
  #f = os.popen("python "+ cwd +"/lib/fileSelectUI.py \""+ filePath +"\"")
      #fileSelected = f.readline().rstrip().lstrip()  
      
      
      
    
  def openFolderAss(self):
    listAsses = self.listWidget.selectedItems()
    
    if(listAsses and (len(listAsses) == 1)):
      x = str(listAsses[0].text())
      p = utilsPipe.getAbsPath(x)
      if(os.path.exists(p)):
        fila = QtGui.QFileDialog.getOpenFileNames(directory=p)
        print(fila)
        if(fila):
          print(str(fila[0]))
          filename = str(fila[0])
          assdets = utilsPipe.getAssDetails(assPath=x)
          runCmd = utilsPipe.openAssetCmd(assdets,filename)
          if(runCmd):
            runCmd = runCmd.rstrip().lstrip()
            subprocess.Popen(runCmd,shell=True)
          else:
            import webbrowser
            webbrowser.open(filename)
          
        
   
  
  def newFolderAss(self):
    pass
  
  
  def editAss(self):
    pass
  
  
  def delAss(self):
    listAsses = self.listWidget.selectedItems()
    
    for x in listAsses:
      if(str(x.text())):
        utilsPipe.assDelete(assPath=str(x.text()))
        
    self.listAssets()
  
  
  
  
  def setStageTypes(self):
    rows = utilsPipe.getStageTypes()
    defStage = utilsPipe.getDefaults("stageTypes")
    try:
      present = str(self.comboStageType.currentText())
    except:
      present = None
    self.comboStageType.clear()  
    indx = 0
    foundIndx = -1
    if(rows):
      for row in rows:
        self.comboStageType.addItem(_fromUtf8(row['type']))
        if(present):
          if(row['type'] == present):
            foundIndx = indx
        else:
          if(defStage['type'] == row['type']):
            foundIndx = indx
        indx = indx + 1
      if(foundIndx != -1):
        self.comboStageType.setCurrentIndex(foundIndx)
      return(1)
    return(0)     
  
  
  def setScene(self):
    seqName = str(self.comboSequence.currentText())
    rows = utilsPipe.getSequenceScenes(os.environ['rp_proj_projName'],seq=seqName)
    try:
      present = str(self.comboScene.currentText())
    except:
      present = None
    self.comboScene.clear()
    scenes = {}
    indx =  0
    foundIndx = -1

    if(rows):
      for x in rows:
        scenes[x['sceneName']] = 1
    if(scenes):
      for x in scenes:
        if(x == present):
          foundIndx = indx
        self.comboScene.addItem(_fromUtf8(x))
        indx = indx + 1
    if(foundIndx != -1):
      self.comboScene.setCurrentIndex(foundIndx)
    return(1)
  
  
  def setSequence(self):
    rows = utilsPipe.getSequenceScenes(os.environ['rp_proj_projName'])
    try:
      present = str(self.comboSequence.currentText())
    except:
      present = None
    self.comboSequence.clear()  
    seq = {}
    indx =  0
    foundIndx = -1
    if(rows):
      for row in rows:
        if(row['projName'] == os.environ['rp_proj_projName']):
          seq[row['sequenceName']] = 1
      if(seq):
        for x in seq.keys():
          if(x == present):
            foundIndx = indx
          self.comboSequence.addItem(_fromUtf8(x))
          indx = indx + 1
        if(foundIndx != -1):
          self.comboSequence.setCurrentIndex(foundIndx)
          
      return(1)
    return(0)     
    
  
  def setNodeTypes(self):
    rows = utilsPipe.getNodeTypes()
    defStage = utilsPipe.getDefaults("nodeTypes")
    try:
      present = str(self.comboNodeType.currentText())
    except:
      present = None
    self.comboNodeType.clear()  
    indx = 0
    foundIndx = -1
    if(rows):
      for row in rows:
        self.comboNodeType.addItem(_fromUtf8(row['type']))
        if(present):
          if(row['type'] == present):
            foundIndx = indx
        else:
          if(defStage['type'] == row['type']):
            foundIndx = indx
        indx = indx + 1
      if(foundIndx != -1):
        self.comboNodeType.setCurrentIndex(foundIndx)
      return(1)
    return(0)     
  
  
  
    #self.comboNodeType.clear()  
    #if(rows):
      #for row in rows:
        #self.comboNodeType.addItem(_fromUtf8(row['type']))
      #return(1)
    #return(0)     
  
  
  def setFileTypes(self):
    rows = utilsPipe.getFileTypes()
    defStage = utilsPipe.getDefaults("fileTypes")
    try:
      present = str(self.comboFileType.currentText())
    except:
      present = None
    self.comboFileType.clear()  
    indx = 0
    foundIndx = -1
    if(rows):
      for row in rows:
        self.comboFileType.addItem(_fromUtf8(row['type']))
        if(present):
          if(row['type'] == present):
            foundIndx = indx
        else:
          if(defStage['type'] == row['type']):
            foundIndx = indx
        indx = indx + 1
      if(foundIndx != -1):
        self.comboFileType.setCurrentIndex(foundIndx)
      return(1)
    return(0)     
    
    
    
    
    #rows = utilsPipe.getFileTypes()
    #self.comboFileType.clear()  
    #if(rows):
      #for row in rows:
        #self.comboFileType.addItem(_fromUtf8(row['type']))
      #return(1)
    #return(0)
  
  
  def setAssTypes(self):
    rows = utilsPipe.getAssTypes()
    defStage = utilsPipe.getDefaults("assetTypes")
    try:
      present = str(self.comboAssType.currentText())
    except:
      present = None
    self.comboAssType.clear()  
    indx = 0
    foundIndx = -1
    if(rows):
      for row in rows:
        self.comboAssType.addItem(_fromUtf8(row['type']))
        if(present):
          if(row['type'] == present):
            foundIndx = indx
        else:
          if(defStage['type'] == row['type']):
            foundIndx = indx
        indx = indx + 1
      if(foundIndx != -1):
        self.comboAssType.setCurrentIndex(foundIndx)
      return(1)
    return(0)     
  
  
    #rows = utilsPipe.getAssTypes()
    #self.comboAssType.clear()  
    #if(rows):
      #for row in rows:
        #self.comboAssType.addItem(_fromUtf8(row['type']))
      #return(1)
    #return(0)
  
  
  
  def rbhusPipeProjCreate(self):
    p = QtCore.QProcess(parent=self.form)
    p.setStandardOutputFile(tempDir + os.sep +"rbhusPipeProjCreate_"+ self.username +".log")
    p.setStandardErrorFile(tempDir + os.sep +"rbhusPipeProjCreate_"+ self.username +".err")
    self.actionNew_project.setEnabled(False)
    p.start(sys.executable,rbhusPipeProjCreateCmd.split())
    p.finished.connect(self.rbhusPipeProjCreateEnable)
    
    
  
  def listAssets(self):
    self.listWidget.clear()
    try:
      asses = utilsPipe.getProjAsses(os.environ['rp_proj_projName'])
    except:
      return(0)
    #print(asses)
    searchItems = str(self.lineEditSearch.text())
    print("search : "+ str(searchItems))
    if(asses):
      for x in range(0,len(asses)):
        if(searchItems):
          if(not (str(asses[x]['path']).find(searchItems) >= 0)):
            continue
          
        stageTypeAss = 0
        nodeTypeAss = 0
        seqAss = 0
        scnAss = 0
        fileTypeAss = 0
        assTypeAss = 0
        if(self.radioMineAss.isChecked()):
#          print("test1")
#          print(asses[x]['createdUser'])
          
          
          if(asses[x]['createdUser'] == self.username):
            
            if(str(self.comboStageType.currentText()) != "default"):
              if(str(self.comboStageType.currentText()) == str(asses[x]['stageType'])):
                stageTypeAss = 1
            else:
              stageTypeAss = 1
            
            if(str(self.comboNodeType.currentText()) != "default"):
              if(str(self.comboNodeType.currentText()) == str(asses[x]['nodeType'])):
                nodeTypeAss = 1
            else:
              nodeTypeAss = 1
            #yesAss = 0
            
            if(str(self.comboSequence.currentText()) != "default"):
              if(str(self.comboSequence.currentText()) == str(asses[x]['sequenceName'])):
                seqAss = 1
            else:
              seqAss = 1
              
            if(str(self.comboScene.currentText()) != "default"):
              if(str(self.comboScene.currentText()) == str(asses[x]['sceneName'])):
                scnAss = 1
            else:
              scnAss = 1
              
            if(str(self.comboNodeType.currentText()) != "default"):
              if(str(self.comboNodeType.currentText()) == str(asses[x]['nodeType'])):
                nodeTypeAss = 1
            else:
              nodeTypeAss = 1
              
            if(str(self.comboFileType.currentText()) != "default"):
              if(str(self.comboFileType.currentText()) == str(asses[x]['fileType'])):
                fileTypeAss = 1
            else:
              fileTypeAss = 1
              
            if(str(self.comboAssType.currentText()) != "default"):
              if(str(self.comboAssType.currentText()) == str(asses[x]['assetType'])):
                assTypeAss = 1
            else:
              assTypeAss = 1
              
              
              
                
#            print("test2")
            if(stageTypeAss and nodeTypeAss and seqAss and scnAss and nodeTypeAss and fileTypeAss and assTypeAss):
              item = QtGui.QListWidgetItem()
              item.setText(asses[x]['path'])
              self.listWidget.addItem(item)
        elif(self.radioAllAss.isChecked()):
          if(str(self.comboStageType.currentText()) != "default"):
            if(str(self.comboStageType.currentText()) == str(asses[x]['stageType'])):
              stageTypeAss = 1
          else:
            stageTypeAss = 1
            
          if(str(self.comboNodeType.currentText()) != "default"):
            if(str(self.comboNodeType.currentText()) == str(asses[x]['nodeType'])):
              nodeTypeAss = 1
          else:
            nodeTypeAss = 1
            #yesAss = 0
            
          if(str(self.comboSequence.currentText()) != "default"):
            if(str(self.comboSequence.currentText()) == str(asses[x]['sequenceName'])):
              seqAss = 1
          else:
            seqAss = 1
            
          if(str(self.comboScene.currentText()) != "default"):
            if(str(self.comboScene.currentText()) == str(asses[x]['sceneName'])):
              scnAss = 1
          else:
            scnAss = 1
            
          if(str(self.comboNodeType.currentText()) != "default"):
            if(str(self.comboNodeType.currentText()) == str(asses[x]['nodeType'])):
              nodeTypeAss = 1
          else:
            nodeTypeAss = 1
            
          if(str(self.comboFileType.currentText()) != "default"):
            if(str(self.comboFileType.currentText()) == str(asses[x]['fileType'])):
              fileTypeAss = 1
          else:
            fileTypeAss = 1
            
          if(str(self.comboAssType.currentText()) != "default"):
            if(str(self.comboAssType.currentText()) == str(asses[x]['assetType'])):
              assTypeAss = 1
          else:
            assTypeAss = 1
            
            
            
              
#          print("test2")
          if(stageTypeAss and nodeTypeAss and seqAss and scnAss and nodeTypeAss and fileTypeAss and assTypeAss):
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
    
  
  
  def rbhusPipeSetProjDefault(self):
    from os.path import expanduser
    home = expanduser("~")
    projFile = 0
    if(os.path.exists(home.rstrip(os.sep) + os.sep +"projSet.default")):
      projFile = open(home.rstrip(os.sep) + os.sep +"projSet.default","r")
    
    if(projFile):
      for x in projFile.readlines():
        if(x):
          utilsPipe.exportProj(x)
          self.form.setWindowTitle(x)
          self.actionSet_project.setText("set project ("+ x +")")
          for y in os.environ.keys():
            if(y.find("rp_") >= 0):
              print(y +":"+ str(os.environ[y]))
            
          self.setSequence()
          self.listAssets()
          break
        
    
  
  def rbhusPipeSetProject(self):
    from os.path import expanduser
    home = expanduser("~")
    projFile = open(home.rstrip(os.sep) + os.sep +"projSet.default","w")
    
    
    
    projNames = []
    projects = utilsPipe.getProjDetails(status="all")
    for x in projects:
      projNames.append(x['projName'])
    projN = subprocess.Popen([sys.executable,selectRadioBoxCmd,"-i",",".join(projNames)],stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].rstrip().lstrip()
    print(projN)
    if(not projN):
      return(0)
    
    
    projFile.writelines(projN)
    projFile.close()
    
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
    self.updateAll()
  
  
  
  def updateAll(self):
    self.setStageTypes()
    self.setAssTypes()
    self.setFileTypes()
    self.setNodeTypes()
    self.setSequence()
    self.setScene()
    self.setAssTypes()
    self.listAssets()
    
  def rbhusPipeAssCreateEnable(self,exitStatus):
    self.pushNewAsset.setEnabled(True)
  
  def rbhusPipeSeqSceCreateEnable(self,exitStatus):
    self.actionNew_seq_scn.setEnabled(True)
    self.updateAll()
    
  
  
  def closeEvent(self,event):
    event.ignore()
    QtGui.QMessageBox.about(self.form,"QUITING?","Minimizing to Tray .\nPlease quit from the tray icon if you really want to quit!")
    self.form.setVisible(False) 
    
  def hideEvent(self,event):
    
    self.form.setVisible(False) 
    self.form.setWindowFlags(self.wFlag & QtCore.Qt.Tool)
    event.ignore()
    
   
  
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
