#!/usr/bin/python
from PyQt4 import QtCore, QtGui
import os
import sys
import tempfile
import time
import subprocess
import math


dirSelf = os.path.dirname(os.path.realpath(__file__))
print(dirSelf)
sys.path.append(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep) + os.sep + "lib")

tempDir = tempfile.gettempdir()
rpA = "rbhusPipeProjCreate.py"
rpAss = "rbhusPipeAssetCreate.py"
rpAssEdit = "rbhusPipeAssetEdit.py"
srb = "selectRadioBox.py"
rpS = "rbhusPipeSeqSceCreate.py" 
fileSelect = "fileSelectUI.py"
scb = "selectCheckBox.py"

selectCheckBoxCmd = dirSelf.rstrip(os.sep) + os.sep + scb
#selectCheckBoxCmd = selectCheckBoxCmd.replace("\\","/")
rbhusPipeProjCreateCmd = dirSelf.rstrip(os.sep) + os.sep + rpA
rbhusPipeAssetCreateCmd = dirSelf.rstrip(os.sep) + os.sep + rpAss
rbhusPipeAssetEditCmd = dirSelf.rstrip(os.sep) + os.sep + rpAssEdit
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
  

class ImageWidget(QtGui.QWidget):
  def __init__(self, imagePath, parent):
    super(ImageWidget, self).__init__(parent)
    self.picture = QtGui.QPixmap(imagePath)
    self.picture  = self.picture.scaledToHeight(32,0)

  def paintEvent(self, event):
    painter = QtGui.QPainter(self)
    painter.drawPixmap(0, 0, self.picture)
    



class ImagePlayer(QtGui.QWidget):
  def __init__(self, filename, parent):
    super(ImagePlayer,self).__init__(parent)
    self.parent = parent

    # Load the file into a QMovie
    self.movie = QtGui.QMovie(filename, QtCore.QByteArray(), parent)
    self.newSize = QtCore.QSize(100,100)
    self.movie.setScaledSize(self.newSize)

    self.movie_screen = QtGui.QLabel()
    self.movie_screen.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
    self.movie_screen.setAlignment(QtCore.Qt.AlignCenter)

    # Add the QMovie object to the label
    self.movie.setCacheMode(QtGui.QMovie.CacheAll)
    self.movie.setSpeed(100)
    self.movie_screen.setMovie(self.movie)
    
    
    # Create the layout
    main_layout = QtGui.QVBoxLayout()
    main_layout.addWidget(self.movie_screen)
    self.setLayout(main_layout)
    
    self.movie.start()
    
  def resizeEvent(self, event):
    self.move((self.parent.geometry().width()-100)/2,(self.parent.geometry().height()-100)/2)
    
    
    
    
class Worker(QtCore.QObject):
  finished = QtCore.pyqtSignal()
  dataReady = QtCore.pyqtSignal(tuple,dict)
  
  def __init__(self):
    super(Worker, self).__init__()
    self.asses = ()
    self.absdict = {}
    print("init worker thread")
  
  #def terminateEvent(self):
    #print("holy cow . quiting!!")
    #if(self.asses or self.absdict):
      #self.finished.emit()
    #else:
      #self.dataReady.emit(self.asses,self.absdict)
    
  def getAsses(self):
    print("in get asses")
    try:
      self.asses = utilsPipe.getProjAsses(os.environ['rp_proj_projName'])
      if(self.asses):
        for x in range(0,len(self.asses)):
          self.absdict[self.asses[x]['path']] = utilsPipe.getAbsPath(self.asses[x]['path'])
    except:
      print(str(sys.exc_info()))
    
    self.finished.emit()
    print("out get asses")
    self.dataReady.emit(self.asses,self.absdict)
    
    

  


class Ui_Form(rbhusPipeMainMod.Ui_MainWindow):
  def setupUi(self, Form):
    rbhusPipeMainMod.Ui_MainWindow.setupUi(self,Form)
    self.form = Form
    self.authL = authPipe.login()
    self.rbhusAssetEditCmdMod = ""
    self.username = None
    self.listAssTimeOld = time.time()
    self.default = False
    self.considerFilter = False
    self.assList = None
    self.absPathList = {}
    self.getAssesLock = False
    self.hf = None
    self.center()
    try:
      self.username = os.environ['rbhusPipe_acl_user'].rstrip().lstrip()
    except:
      pass
    
    
    iconRefresh = QtGui.QIcon()
    iconRefresh.addPixmap(QtGui.QPixmap(_fromUtf8(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/ic_action_refresh.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
    self.assRefresh.setIcon(iconRefresh)
    

    iconCancel = QtGui.QIcon()
    iconCancel.addPixmap(QtGui.QPixmap(_fromUtf8(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/ic_action_cancel.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
    self.pushResetAsset.setIcon(iconCancel)
    self.pushResetSeq.setIcon(iconCancel)
    self.pushResetStage.setIcon(iconCancel)
    self.pushResetScene.setIcon(iconCancel)
    self.pushResetNode.setIcon(iconCancel)
    self.pushResetAsset.setIcon(iconCancel)
    self.pushResetFile.setIcon(iconCancel)
    self.filterRefresh.setIcon(iconCancel)

    
    self.iconDanger = QtGui.QIcon()
    self.iconDanger.addPixmap(QtGui.QPixmap(_fromUtf8(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/danger.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
    
    
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(_fromUtf8(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/rbhusPipe.svg")), QtGui.QIcon.Normal, QtGui.QIcon.On)
    Form.setWindowIcon(icon)
    
    #self.timerAssetsRefresh = QtCore.QTimer()
    #self.timerAssetsRefresh.timeout.connect(self.listAssetsTimed)
    
    
    
    self.pushLogout.setText("logout : "+ str(self.username))
    self.pushLogout.clicked.connect(self.logout)
    
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
    self.filterRefresh.clicked.connect(self.resetFilterDefault)
    self.assRefresh.clicked.connect(self.listAssets)
    
    self.comboSequence.currentIndexChanged.connect(self.setScene)
    self.comboSequence.completer().setCompletionMode(QtGui.QCompleter.PopupCompletion)
    
    
    self.comboStageType.editTextChanged.connect(self.listAssets)
    self.comboStageType.view().activated.connect(self.handleItemPressedForCombo)
    #self.comboStageType.view().event = self.comboStageTypeEvent
    #self.comboStageType.view().clicked.connect(self.handleItemPressedForCombo)
    #self.comboStageType.view().itemChanged.connect(self.handleItemPressedForCombo)
    self.comboStageType.completer().setCompletionMode(QtGui.QCompleter.PopupCompletion)
    self.pushResetStage.clicked.connect(self.setStageTypes)
    
    
    self.comboNodeType.currentIndexChanged.connect(self.listAssets)
    self.comboNodeType.completer().setCompletionMode(QtGui.QCompleter.PopupCompletion)
    
    self.comboScene.currentIndexChanged.connect(self.listAssets)
    self.comboScene.completer().setCompletionMode(QtGui.QCompleter.PopupCompletion)
    
    
    self.comboAssType.currentIndexChanged.connect(self.listAssets)
    self.comboAssType.completer().setCompletionMode(QtGui.QCompleter.PopupCompletion)
    
    self.comboFileType.currentIndexChanged.connect(self.listAssets)
    self.comboFileType.completer().setCompletionMode(QtGui.QCompleter.PopupCompletion)
    
    self.radioAllAss.toggled.connect(self.listAssets)
    self.radioMineAss.toggled.connect(self.listAssets)
    
    
    self.lineEditSearch.returnPressed.connect(self.listAssets)
    self.lineEditSearch.textChanged.connect(self.listAssets)
  
    
    self.checkBoxFilter.clicked.connect(self.checkFilterFunc)
    self.checkCase.clicked.connect(self.listAssets)
    self.checkWords.clicked.connect(self.listAssets)
    
    
    #self.form.closeEvent = self.closeEvent
   
    
    self.loadingGif = dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/loading.gif"
    self.loader = ImagePlayer(self.loadingGif,parent=self.tableWidget)
    self.loader.hide()
    
    
    self.rbhusPipeSetProjDefault()
    self.form.hideEvent = self.hideEvent
    self.form.closeEvent = self.hideEvent
    
    # set up the right-click context menu for tableWidget
    self.tableWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    self.tableWidget.customContextMenuRequested.connect(self.popupAss)
    
    
    self.timer = QtCore.QTimer()
    self.timer.timeout.connect(self.listAssets)
    self.checkRefresh.clicked.connect(self.timeCheck)
    
    self.checkFilterFunc()
    self.centralwidget.resizeEvent  = self.resizeEvent
    self.tableWidget.resizeEvent = self.resizeEvent
    #self.updateAll()
    #self.listAssetsTimed()
    
  
  
  def resizeEvent(self,event):
    self.loader.resizeEvent(event)
    
  
  def comboStageTypeEvent(self,event):
    print(event)
  
  def listAssets(self):
    self.listAssetsTimed()
    
    #print("list assets called")
    #if(self.timerAssetsRefresh.isActive()):
      #self.timerAssetsRefresh.stop()
      #self.timerAssetsRefresh.start(500)
    #else:
      #self.timerAssetsRefresh.start(500)
  
  
  
  
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
  
  
  def checkFilterFunc(self):
    if(self.checkBoxFilter.isChecked()):
      self.groupBoxFilter.setVisible(True)
      self.considerFilter  = True
      self.listAssets()
    else:
      self.groupBoxFilter.setVisible(False)
      self.considerFilter = False
      self.listAssets()
    
  def popupAss(self, pos):
    menu = QtGui.QMenu()
    openFileAction = menu.addAction("open file")
    openFolderAction = menu.addAction("open folder")
    assEditAction = menu.addAction("edit")
    assCopyToClip = menu.addAction("copy path to clipboard")
    assCopyNew = menu.addAction("copy/new")
    assCreatePrev = menu.addAction("create preview")
    assRender = menu.addAction("submit to render")
    assDeleteAction = menu.addAction("delete")
    
    action = menu.exec_(self.tableWidget.mapToGlobal(pos))
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
    listAsses = self.tableWidget.selectedItems()
    print(listAsses)
    if(listAsses):
      x = str(listAsses[0].text())
      abspath =  utilsPipe.getAbsPath(x)
      pyperclip.copy(abspath)
      
  
  def openFileAss(self):
    listAsses = self.tableWidget.selectedItems()
    print(listAsses)
    fcmd = fileSelectCmd
    if(listAsses):
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
    listAsses = self.tableWidget.selectedItems()
    if(listAsses): # and (len(listAsses) == 1)
      x = str(listAsses[0].text())
      print(x)
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
  
  
  
  def selectedAsses(self):
    rowstask=[]
    rowsSelected = []
    rowsModel = self.tableWidget.selectionModel().selectedRows()
    
    for idx in rowsModel:
      rowsSelected.append(idx.row())
    for row in rowsSelected:
      rowstask.append(str(self.tableWidget.item(row,0).text()))
    return(rowstask)
  
  
  def delAss(self):
    wtf = self.messageBox()
    if(wtf):
      listAsses = self.tableWidget.selectedItems()
      
      for x in listAsses:
        if(str(x.text())):
          utilsPipe.assDelete(assPath=str(x.text()))
        
      self.listAssets()
  
  
  def editAss(self):
    listAsses = self.selectedAsses()
    print(listAsses)
    if(listAsses):
      self.rbhusAssetEditCmdMod = rbhusPipeAssetEditCmd +" -p "+ ",".join(listAsses)
      print(self.rbhusAssetEditCmdMod)
      self.rbhusPipeAssetEdit()
    #for x in listAsses:
      #if(str(x)):
        #print(str(x))
      
  
  def setStageTypes(self):
    rows = utilsPipe.getStageTypes()
    defStage = utilsPipe.getDefaults("stageTypes")
    try:
      if(self.default):
        present = None
      else:
        present = str(self.comboStageType.currentText())
    except:
      present = None
    self.comboStageType.clear()  
    indx = 0
    foundIndx = -1
    
    model = QtGui.QStandardItemModel(len(defStage),1)
    
    if(rows):
      for row in rows:
        item = QtGui.QStandardItem(row['type'])
        item.setFlags(QtCore.Qt.ItemIsUserCheckable)
        #item.setFlags(QtCore.Qt.NoItemFlags)
        item.setData(QtCore.Qt.Unchecked, QtCore.Qt.CheckStateRole)
        #item.setCheckable(True)
        model.setItem(indx,0,item)
        abrush = QtGui.QBrush()
        color = QtGui.QColor()
        color.setAlpha(0)
        abrush.setColor(color)
        model.item(indx).setForeground(abrush)
        
        
        #self.comboStageType.addItem(_fromUtf8(row['type']))
        #if(present):
          #if(row['type'] == present):
            #foundIndx = indx
        #else:
          #if(defStage['type'] == row['type']):
            #foundIndx = indx
        indx = indx + 1
      self.comboStageType.setModel(model)
      #if(foundIndx != -1):
      self.comboStageType.setEditText(defStage['type'])
      return(1)
    return(0)     
  
  
  
  def handleItemPressedForCombo(self, index):
    selectedStages = []
    
    if(self.comboStageType.model().item(index.row()).checkState() != 0):
      self.comboStageType.model().item(index.row()).setCheckState(QtCore.Qt.Unchecked)
      #self.comboStageType.model().item(index.row()).setEnabled(False)
      abrush = QtGui.QBrush()
      color = QtGui.QColor()
      color.setAlpha(0)
      abrush.setColor(color)
      self.comboStageType.model().item(index.row()).setForeground(abrush)
    else:
      self.comboStageType.model().item(index.row()).setCheckState(QtCore.Qt.Checked)
      #self.comboStageType.model().item(index.row()).setEnabled(True)
      abrush = self.comboStageType.model().item(index.row()).background()
      color = QtGui.QColor()
      color.setGreen(10)
      color.setBlue(125)
      color.setRed(225)
      abrush.setColor(color)
      self.comboStageType.model().item(index.row()).setForeground(abrush)
    
    for i in range(0,self.comboStageType.model().rowCount()):
      if(self.comboStageType.model().item(i).checkState() == QtCore.Qt.Checked):
        selectedStages.append(str(self.comboStageType.model().item(i).text()))
      
    print("EVENT CALLED : "+ str(index.row()))
    self.comboStageType.setEditText(",".join(selectedStages))
        
            
  def setScene(self):
    seqName = str(self.comboSequence.currentText())
    rows = utilsPipe.getSequenceScenes(os.environ['rp_proj_projName'],seq=seqName)
    try:
      if(self.default):
        present = None
      else:
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
      if(self.default):
        present = None
      else:
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
      if(self.default):
        present = None
      else:
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
      if(self.default):
        present = None
      else:
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
      if(self.default):
        present = None
      else:
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
  def messageBox(self):
    msgbox = QtGui.QMessageBox()
    
    msgbox.setText("DELETE?!?!?!\nDo you want to really delete this asset?!")
    msgbox.setIconPixmap(QtGui.QPixmap(_fromUtf8(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/danger_128.png")))
    #noBut = QtGui.QPushButton("cancel")
    #yesBut = QtGui.QPushButton("yes")
    yesBut = msgbox.addButton("yes",QtGui.QMessageBox.YesRole)
    noBut = msgbox.addButton("cancel",QtGui.QMessageBox.NoRole)
    msgbox.setDefaultButton(noBut)
    msgbox.exec_()
    if(msgbox.clickedButton() == yesBut):
      return(1)
    else:
      return(0)
    
    #if(ok == QtGui.QMessageBox.Yes):
      #return(1)
    #else:
      #return(0)
  
  
  def rbhusPipeProjCreate(self):
    p = QtCore.QProcess(parent=self.form)
    p.setStandardOutputFile(tempDir + os.sep +"rbhusPipeProjCreate_"+ self.username +".log")
    p.setStandardErrorFile(tempDir + os.sep +"rbhusPipeProjCreate_"+ self.username +".err")
    self.actionNew_project.setEnabled(False)
    p.start(sys.executable,rbhusPipeProjCreateCmd.split())
    p.finished.connect(self.rbhusPipeProjCreateEnable)
    
    
  
  def listAssetsTimed(self):
    self.loader.show()
    if(self.hf):
      if(self.hf.isRunning()):
        return(0)
    #print("in get asses timed 1")
    
    self.tableWidget.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.WaitCursor))
    self.hf = QtCore.QThread(parent=self.tableWidget)
    #print("in get asses timed 2")  
    assget = Worker()
    assget.moveToThread(self.hf)
    assget.dataReady.connect(self.listAssets_thread)
    
    #print("in get asses timed 3")
    self.hf.setTerminationEnabled(True)
    self.hf.started.connect(assget.getAsses)
    self.hf.run = assget.getAsses
    self.hf.start()
    
    
    #print("in get asses timed 4")
    
  
  
  
  



  
  def listAssets_thread(self,asslist,assdict):
    #print(str((time.time() - self.listAssTimeOld)))
    #if((time.time() - self.listAssTimeOld) < 1.0):
      #return(0)
    #self.listAssTimeOld = time.time()
    print("list ass thread called")
    selAsses = self.selectedAsses()
    colNames = ['asset','assigned','preview']
    assesList = []
    assesNames = {}
    self.tableWidget.clear()
    self.tableWidget.clearContents()
    self.tableWidget.setSortingEnabled(False)
    self.tableWidget.resizeColumnsToContents()
    self.tableWidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
    
    asses = asslist
    searchItems = str(self.lineEditSearch.text())
    print("search : "+ str(searchItems))
    if(asses):
      for x in range(0,len(asses)):
        
        if(searchItems):
          #print("reload 2")
          if(self.checkCase.isChecked()):
            if(self.checkWords.isChecked()):
              if(self.checkTags.isChecked()):
                if(not (str(asses[x]['tags']).lower() == searchItems.lower())):
                  continue
              else:
                if(not (str(asses[x]['assName']).lower() == searchItems.lower())):
                  continue
            else:
              if(self.checkTags.isChecked()):
                if(not (str(asses[x]['tags']).lower().find(searchItems.lower()) >= 0)):
                  continue
              else:
                if(not (str(asses[x]['assName']).lower().find(searchItems.lower()) >= 0)):
                  continue
          else:
            if(self.checkWords.isChecked()):
              if(self.checkTags.isChecked()):
                if(not (str(asses[x]['tags']) == searchItems)):
                  continue
              else:
                if(not (str(asses[x]['assName']) == searchItems)):
                  continue
            else:
              if(self.checkTags.isChecked()):
                if(not (str(asses[x]['tags']).find(searchItems) >= 0)):
                  continue
              else:
                if(not (str(asses[x]['assName']).find(searchItems) >= 0)):
                  continue
          
        stageTypeAss = 0
        nodeTypeAss = 0
        seqAss = 0
        scnAss = 0
        fileTypeAss = 0
        assTypeAss = 0
        if(self.radioMineAss.isChecked()):
          #print("reload 3")

          if(asses[x]['createdUser'] == self.username):
            
            if(self.considerFilter):

              if(str(self.comboStageType.currentText()) != "default"):
                if(str(asses[x]['stageType']) in str(self.comboStageType.currentText()).split(",")):
                  stageTypeAss = 1
              else:
                stageTypeAss = 1
              
              if(str(self.comboNodeType.currentText()) != "default"):
                if(str(self.comboNodeType.currentText()) == str(asses[x]['nodeType'])):
                  nodeTypeAss = 1
              else:
                nodeTypeAss = 1
              
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
            else:
              assesList.append(asses[x]['path'])
              assesNames[asses[x]['path']] = asses[x]
            
            if(stageTypeAss and nodeTypeAss and seqAss and scnAss and nodeTypeAss and fileTypeAss and assTypeAss):
              assesList.append(asses[x]['path'])
              assesNames[asses[x]['path']] = asses[x]

        elif(self.radioAllAss.isChecked()):
          
          if(self.considerFilter):

            if(str(self.comboStageType.currentText()) != "default"):
              if(str(asses[x]['stageType']) in str(self.comboStageType.currentText()).split(",")):
                stageTypeAss = 1
            else:
              stageTypeAss = 1
                
            if(str(self.comboNodeType.currentText()) != "default"):
              if(str(self.comboNodeType.currentText()) == str(asses[x]['nodeType'])):
                nodeTypeAss = 1
            else:
              nodeTypeAss = 1
              
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
          else:
            assesList.append(asses[x]['path'])  
            assesNames[asses[x]['path']] = asses[x]
          if(stageTypeAss and nodeTypeAss and seqAss and scnAss and nodeTypeAss and fileTypeAss and assTypeAss):
            assesList.append(asses[x]['path'])
            assesNames[asses[x]['path']] = asses[x]
          
    if(assesList):
      self.tableWidget.setColumnCount(len(colNames))
      self.tableWidget.setRowCount(len(assesList))
      for x in range(0,len(colNames)):
        item = QtGui.QTableWidgetItem()
        item.setText(str(colNames[x]))
        self.tableWidget.setHorizontalHeaderItem(x, item)
      for x in range(0,len(assesList)):
        item = QtGui.QTableWidgetItem()
        item.setText(str(assesList[x]))
        assAbsPath = assdict[assesList[x]]
        self.tableWidget.setItem(x,0,item)
        
        if(assesList[x] in selAsses):
          self.tableWidget.selectRow(x)
        
        itemTag = QtGui.QTableWidgetItem()
        itemTag.setText(str(assesNames[assesList[x]]['assignedWorker']))
        self.tableWidget.setItem(x,1,itemTag)
        
        if(assesNames[assesList[x]]['assName'] == "default"):
          previewName = "preview"
        else:
          previewName = assesNames[assesList[x]]['assName']
        if(os.path.exists(assAbsPath +"/"+ previewName +".png")):
          prevItem = ImageWidget(assAbsPath +"/"+ previewName +".png",self.tableWidget)
          prevItem.setToolTip('<img src="'+ assAbsPath +"/"+ previewName +".png"+'" height="192"/>')
          self.tableWidget.setCellWidget(x,2,prevItem)
        
        
        
    self.tableWidget.resizeColumnsToContents()
    self.tableWidget.setSortingEnabled(True)
    
    self.tableWidget.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
    self.tableWidget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
    #self.timerAssetsRefresh.stop()
    self.loader.hide()
    
  
  
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
    
    
  def rbhusPipeAssetEdit(self):
    p = QtCore.QProcess(parent=self.form)
    p.setStandardOutputFile(tempDir + os.sep +"rbhusPipeAssetEdit_"+ self.username +".log")
    p.setStandardErrorFile(tempDir + os.sep +"rbhusPipeAssetEdit_"+ self.username +".err")
    p.start(sys.executable,self.rbhusAssetEditCmdMod.split())
    p.finished.connect(self.listAssets)
    
  
  
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
            
          self.updateAll()
          #self.listAssets()
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
      
    self.updateAll()
    
    
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
    
  
  def resetFilterDefault(self):
    self.default = True
    self.setStageTypes()
    self.setAssTypes()
    self.setFileTypes()
    self.setNodeTypes()
    self.setSequence()
    self.setScene()
    self.setAssTypes()
    self.default = False
  
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
