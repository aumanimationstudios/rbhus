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
    
  def showEvent(self,event):
    #self.movie.setEnabled(True)
    self.movie.start()
    #self.show()
    
    
  def hideEvent(self,event):
    self.movie.stop()
    #self.movie.setEnabled(False)
    #self.hide()
    
    
    
class Worker(QtCore.QObject):
  finished = QtCore.pyqtSignal()
  dataPending = QtCore.pyqtSignal()
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
    self.dataPending.emit()
    # print("in get asses")
    self.asses = ()
    self.absdict = {}
    try:
      self.asses = utilsPipe.getProjAsses(os.environ['rp_proj_projName'])
      if(self.asses):
        for x in range(0,len(self.asses)):
          self.absdict[self.asses[x]['path']] = utilsPipe.getAbsPath(self.asses[x]['path'])
    except:
      print(str(sys.exc_info()))
    
    self.finished.emit()
    # print("out get asses")
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
    self.oldasses = None
    self.oldassesdict = None
    self.center()
    self.firstTime = True
    self.listFirstTime = False

    self.menuMine = QtGui.QMenu()
    self.mineCreatedAction = QtGui.QAction("created",self.menuMine,checkable=True)
    self.mineCreatedAction.setChecked(True)
    self.mineAssignedAction = QtGui.QAction("assigned",self.menuMine,checkable=True)
    self.mineAssignedAction.setChecked(True)
    self.menuMine.addAction(self.mineCreatedAction)
    self.menuMine.addAction(self.mineAssignedAction)
    self.menuMine.triggered.connect(self.menuMineShow)


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
    
    
    #self.tableWidget.resizeEvent
    
    self.quitAction = self.trayMenu.addAction("quit")
    self.quitAction.triggered.connect(self.quitFunc)
    
    self.trayIcon.setContextMenu(self.trayMenu)
    self.trayIcon.activated.connect(self.showMain)
    
    self.actionNew_project.triggered.connect(self.rbhusPipeProjCreate)
    self.actionSet_project.triggered.connect(self.rbhusPipeSetProject)
    self.actionNew_seq_scn.triggered.connect(self.rbhusPipeSeqSceCreate)
    self.pushNewAsset.clicked.connect(self.rbhusPipeAssetCreate)
    self.filterRefresh.clicked.connect(self.resetFilterDefault)
    self.assRefresh.clicked.connect(self.assRefreshPressed)
    
    
    
    slineedit = self.comboStageType.lineEdit()
    slineedit.setReadOnly(True)
    self.comboStageType.editTextChanged.connect(self.listAssets)
    self.comboStageType.view().activated.connect(self.pressedStageType)
    #self.comboStageType.completer().setCompletionMode(QtGui.QCompleter.PopupCompletion)
    self.pushResetStage.clicked.connect(self.setStageTypes)
    
    nlineedit = self.comboNodeType.lineEdit()
    nlineedit.setReadOnly(True)
    self.comboNodeType.editTextChanged.connect(self.listAssets)
    self.comboNodeType.view().activated.connect(self.pressedNodeType)
    #self.comboNodeType.completer().setCompletionMode(QtGui.QCompleter.PopupCompletion)
    self.pushResetNode.clicked.connect(self.setNodeTypes)
    
    
    seqlineedit = self.comboSequence.lineEdit()
    seqlineedit.setReadOnly(True)
    self.comboSequence.editTextChanged.connect(self.setSeqSce)
    self.comboSequence.view().activated.connect(self.pressedSequence)
    #self.comboSequence.completer().setCompletionMode(QtGui.QCompleter.PopupCompletion)
    self.pushResetSeq.clicked.connect(self.setSequence)
    
    
    scelineedit = self.comboScene.lineEdit()
    scelineedit.setReadOnly(True)
    self.comboScene.editTextChanged.connect(self.listAssets)
    self.comboScene.view().activated.connect(self.pressedScene)
    #self.comboScene.completer().setCompletionMode(QtGui.QCompleter.PopupCompletion)
    self.pushResetScene.clicked.connect(self.setScene)
    
    
    filelineedit = self.comboFileType.lineEdit()
    filelineedit.setReadOnly(True)
    self.comboFileType.editTextChanged.connect(self.listAssets)
    self.comboFileType.view().activated.connect(self.pressedFileType)
    #self.comboFileType.completer().setCompletionMode(QtGui.QCompleter.PopupCompletion)
    self.pushResetFile.clicked.connect(self.setFileTypes)
    
    
    self.comboAssType.currentIndexChanged.connect(self.listAssets)
    #self.comboAssType.completer().setCompletionMode(QtGui.QCompleter.PopupCompletion)
    self.pushResetAsset.clicked.connect(self.setAssTypes)
    
    self.comboFileType.currentIndexChanged.connect(self.listAssets)
    #self.comboFileType.completer().setCompletionMode(QtGui.QCompleter.PopupCompletion)
    
    self.radioAllAss.clicked.connect(self.listAssets)
    # self.radioMineAss.toggled.connect(self.listAssets)
    self.radioMineAss.clicked.connect(self.popupMine)
    
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
    self.tableWidget.verticalScrollBar().valueChanged.connect(self.tableWidgetResizeContents)
    #self.updateAll()

    self.listAssetsTimed()
    self.timerAss = QtCore.QTimer()
    self.timerAss.timeout.connect(self.listAssetsTimed)
    self.timerAss.start(60000)
  
  
  def setSeqSce(self):
    self.setScene()
    self.listAssets()
  
  def resizeEvent(self,event):
    self.loader.resizeEvent(event)
    self.tableWidget.resizeColumnsToContents()
    
  
  def assRefreshPressed(self):
    self.firstTime = True
    self.listAssetsTimed()

  def tableWidgetResizeContents(self):
    self.tableWidget.resizeColumnsToContents()
  
  def comboStageTypeEvent(self,event):
    print(event)
  
  def listAssets(self):
    # self.listAssetsTimed()
    self.listAssets_thread()
    
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
    if(action == assRender):
      self.renderAss()
      
      
  def popupMine(self):
    cursor =QtGui.QCursor()
    action = self.menuMine.exec_(cursor.pos())
    self.listAssets()

  def menuMineShow(self):
    self.menuMine.show()

  def renderAss(self):
    listAsses = self.selectedAsses()
    print(listAsses)
    
    
      
      
  def copyNewAss(self):
    pass
    
  
  def copyPathToClip(self):
    listAsses = self.selectedAsses()
    print(listAsses)
    if(listAsses):
      x = listAsses[0]
      abspath =  utilsPipe.getAbsPath(x)
      pyperclip.copy(abspath)
      
  
  def openFileAss(self):
    listAsses = self.selectedAsses()
    print(listAsses)
    fcmd = fileSelectCmd
    if(listAsses):
      x = listAsses[0]
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
    listAsses = self.selectedAsses()
    if(listAsses): # and (len(listAsses) == 1)
      x = str(listAsses[0])
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
  
  
  
  
  
  
  def delAss(self):
    wtf = self.messageBox()
    if(wtf):
      listAsses = self.selectedAsses()
      
      for x in listAsses:
        print(x)
        if(str(x)):
          utilsPipe.assDelete(assPath=str(x))
        
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
    #defStage = utilsPipe.getDefaults("stageTypes")
    self.comboStageType.clear()  
    indx = 0
    
    model = QtGui.QStandardItemModel(len(rows),1)
    
    if(rows):
      for row in rows:
        item = QtGui.QStandardItem(row['type'])
        item.setFlags(QtCore.Qt.ItemIsUserCheckable)
        item.setData(QtCore.Qt.Unchecked, QtCore.Qt.CheckStateRole)
        model.setItem(indx,0,item)
        abrush = QtGui.QBrush()
        color = QtGui.QColor()
        color.setAlpha(0)
        abrush.setColor(color)
        model.item(indx).setForeground(abrush)
        indx = indx + 1
      self.comboStageType.setModel(model)
      self.comboStageType.setEditText("default")
      return(1)
    return(0)     
  
  
  
  def pressedStageType(self, index):
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
      abrush = QtGui.QBrush()
      color = QtGui.QColor()
      color.setGreen(10)
      color.setBlue(125)
      color.setRed(225)
      abrush.setColor(color)
      self.comboStageType.model().item(index.row()).setForeground(abrush)
    
    for i in range(0,self.comboStageType.model().rowCount()):
      if(self.comboStageType.model().item(i).checkState() == QtCore.Qt.Checked):
        selectedStages.append(str(self.comboStageType.model().item(i).text()))
      
    #print("EVENT CALLED : "+ str(index.row()))
    if(selectedStages):
      self.comboStageType.setEditText(",".join(selectedStages))
    else:
      self.comboStageType.setEditText("default")
        
            
  def setScene(self):
    seqNames = str(self.comboSequence.currentText()).split(",")
    
    self.comboScene.clear()
    scenes = {}
    indx =  0
    foundIndx = -1
    
    for x in seqNames:
      rows = utilsPipe.getSequenceScenes(os.environ['rp_proj_projName'],seq=x)
      if(rows):
        for x in rows:
          scenes[x['sceneName']] = 1
    if(scenes):
      model = QtGui.QStandardItemModel(len(scenes),1)
      for x in scenes:
        item = QtGui.QStandardItem(x)
        item.setFlags(QtCore.Qt.ItemIsUserCheckable)
        item.setData(QtCore.Qt.Unchecked, QtCore.Qt.CheckStateRole)
        model.setItem(indx,0,item)
        abrush = QtGui.QBrush()
        color = QtGui.QColor()
        color.setAlpha(0)
        abrush.setColor(color)
        model.item(indx).setForeground(abrush)
        indx = indx + 1
      self.comboScene.setModel(model)
      self.comboScene.setEditText("default")
      return(1)
    return(0)     
        
  
  def pressedScene(self, index):
    selectedStages = []
    
    if(self.comboScene.model().item(index.row()).checkState() != 0):
      self.comboScene.model().item(index.row()).setCheckState(QtCore.Qt.Unchecked)
      #self.comboStageType.model().item(index.row()).setEnabled(False)
      abrush = QtGui.QBrush()
      color = QtGui.QColor()
      color.setAlpha(0)
      abrush.setColor(color)
      self.comboScene.model().item(index.row()).setForeground(abrush)
    else:
      self.comboScene.model().item(index.row()).setCheckState(QtCore.Qt.Checked)
      #self.comboStageType.model().item(index.row()).setEnabled(True)
      abrush = QtGui.QBrush()
      color = QtGui.QColor()
      color.setGreen(10)
      color.setBlue(125)
      color.setRed(225)
      abrush.setColor(color)
      self.comboScene.model().item(index.row()).setForeground(abrush)
    
    for i in range(0,self.comboScene.model().rowCount()):
      if(self.comboScene.model().item(i).checkState() == QtCore.Qt.Checked):
        selectedStages.append(str(self.comboScene.model().item(i).text()))
      
    #print("EVENT CALLED : "+ str(index.row()))
    if(selectedStages):
      self.comboScene.setEditText(",".join(selectedStages))
    else:
      self.comboScene.setEditText("default")
  
  
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
    
    for row in rows:
      seq[row['sequenceName']] = 1
    
    model = QtGui.QStandardItemModel(len(seq),1)
    
    if(seq):
      for row in seq.keys():
        item = QtGui.QStandardItem(row)
        item.setFlags(QtCore.Qt.ItemIsUserCheckable)
        item.setData(QtCore.Qt.Unchecked, QtCore.Qt.CheckStateRole)
        model.setItem(indx,0,item)
        abrush = QtGui.QBrush()
        color = QtGui.QColor()
        color.setAlpha(0)
        abrush.setColor(color)
        model.item(indx).setForeground(abrush)
        indx = indx + 1
      self.comboSequence.setModel(model)
      self.comboSequence.setEditText("default")
      return(1)
    return(0)     
  
    
    #if(rows):
      #for row in rows:
        #if(row['projName'] == os.environ['rp_proj_projName']):
          #seq[row['sequenceName']] = 1
      #if(seq):
        #for x in seq.keys():
          #if(x == present):
            #foundIndx = indx
          #self.comboSequence.addItem(_fromUtf8(x))
          #indx = indx + 1
        #if(foundIndx != -1):
          #self.comboSequence.setCurrentIndex(foundIndx)
          
      #return(1)
    #return(0)     
  
  
  def pressedSequence(self, index):
    selectedStages = []
    
    if(self.comboSequence.model().item(index.row()).checkState() != 0):
      self.comboSequence.model().item(index.row()).setCheckState(QtCore.Qt.Unchecked)
      #self.comboStageType.model().item(index.row()).setEnabled(False)
      abrush = QtGui.QBrush()
      color = QtGui.QColor()
      color.setAlpha(0)
      abrush.setColor(color)
      self.comboSequence.model().item(index.row()).setForeground(abrush)
    else:
      self.comboSequence.model().item(index.row()).setCheckState(QtCore.Qt.Checked)
      #self.comboStageType.model().item(index.row()).setEnabled(True)
      abrush = QtGui.QBrush()
      color = QtGui.QColor()
      color.setGreen(10)
      color.setBlue(125)
      color.setRed(225)
      abrush.setColor(color)
      self.comboSequence.model().item(index.row()).setForeground(abrush)
    
    for i in range(0,self.comboSequence.model().rowCount()):
      if(self.comboSequence.model().item(i).checkState() == QtCore.Qt.Checked):
        selectedStages.append(str(self.comboSequence.model().item(i).text()))
      
    #print("EVENT CALLED : "+ str(index.row()))
    if(selectedStages):
      self.comboSequence.setEditText(",".join(selectedStages))
    else:
      self.comboSequence.setEditText("default")
  
  
  def setNodeTypes(self):
    rows = utilsPipe.getNodeTypes()
    #defStage = utilsPipe.getDefaults("nodeTypes")
    
    self.comboNodeType.clear()  
    indx = 0
    
    model = QtGui.QStandardItemModel(len(rows),1)
    if(rows):
      for row in rows:
        item = QtGui.QStandardItem(row['type'])
        item.setFlags(QtCore.Qt.ItemIsUserCheckable)
        item.setData(QtCore.Qt.Unchecked, QtCore.Qt.CheckStateRole)
        model.setItem(indx,0,item)
        abrush = QtGui.QBrush()
        color = QtGui.QColor()
        color.setAlpha(0)
        abrush.setColor(color)
        model.item(indx).setForeground(abrush)
        indx = indx + 1
      self.comboNodeType.setModel(model)
      self.comboNodeType.setEditText("default")
      return(1)
    return(0)     
  
  
  
  def pressedNodeType(self, index):
    selectedStages = []
    if(self.comboNodeType.model().item(index.row()).checkState() != 0):
      self.comboNodeType.model().item(index.row()).setCheckState(QtCore.Qt.Unchecked)
      #self.comboStageType.model().item(index.row()).setEnabled(False)
      abrush = QtGui.QBrush()
      color = QtGui.QColor()
      color.setAlpha(0)
      abrush.setColor(color)
      self.comboNodeType.model().item(index.row()).setForeground(abrush)
    else:
      self.comboNodeType.model().item(index.row()).setCheckState(QtCore.Qt.Checked)
      #self.comboStageType.model().item(index.row()).setEnabled(True)
      abrush = QtGui.QBrush()
      color = QtGui.QColor()
      color.setGreen(10)
      color.setBlue(125)
      color.setRed(225)
      abrush.setColor(color)
      self.comboNodeType.model().item(index.row()).setForeground(abrush)
    
    for i in range(0,self.comboNodeType.model().rowCount()):
      if(self.comboNodeType.model().item(i).checkState() == QtCore.Qt.Checked):
        selectedStages.append(str(self.comboNodeType.model().item(i).text()))
      
    #print("EVENT CALLED : "+ str(index.row()))
    if(selectedStages):
      self.comboNodeType.setEditText(",".join(selectedStages))
    else:
      self.comboNodeType.setEditText("default")
  
  
  
  def setFileTypes(self):
    rows = utilsPipe.getFileTypes()
    #defStage = utilsPipe.getDefaults("fileTypes")
    model = QtGui.QStandardItemModel(len(rows),1)
    
    indx = 0
    self.comboFileType.clear()  
    if(rows):
      for row in rows:
        item = QtGui.QStandardItem(row['type'])
        item.setFlags(QtCore.Qt.ItemIsUserCheckable)
        item.setData(QtCore.Qt.Unchecked, QtCore.Qt.CheckStateRole)
        model.setItem(indx,0,item)
        abrush = QtGui.QBrush()
        color = QtGui.QColor()
        color.setAlpha(0)
        abrush.setColor(color)
        model.item(indx).setForeground(abrush)
        indx = indx + 1
      self.comboFileType.setModel(model)
      self.comboFileType.setEditText("default")
      return(1)
    return(0)     
    
  
  
  def pressedFileType(self, index):
    selectedStages = []
    
    if(self.comboFileType.model().item(index.row()).checkState() != 0):
      self.comboFileType.model().item(index.row()).setCheckState(QtCore.Qt.Unchecked)
      #self.comboStageType.model().item(index.row()).setEnabled(False)
      abrush = QtGui.QBrush()
      color = QtGui.QColor()
      color.setAlpha(0)
      abrush.setColor(color)
      self.comboFileType.model().item(index.row()).setForeground(abrush)
    else:
      self.comboFileType.model().item(index.row()).setCheckState(QtCore.Qt.Checked)
      #self.comboStageType.model().item(index.row()).setEnabled(True)
      abrush = QtGui.QBrush()
      color = QtGui.QColor()
      color.setGreen(10)
      color.setBlue(125)
      color.setRed(225)
      abrush.setColor(color)
      self.comboFileType.model().item(index.row()).setForeground(abrush)
    
    for i in range(0,self.comboFileType.model().rowCount()):
      if(self.comboFileType.model().item(i).checkState() == QtCore.Qt.Checked):
        selectedStages.append(str(self.comboFileType.model().item(i).text()))
      
    #print("EVENT CALLED : "+ str(index.row()))
    if(selectedStages):
      self.comboFileType.setEditText(",".join(selectedStages))
    else:
      self.comboFileType.setEditText("default")
    
    
    
    #rows = utilsPipe.getFileTypes()
    #self.comboFileType.clear()  
    #if(rows):
      #for row in rows:
        #self.comboFileType.addItem(_fromUtf8(row['type']))
      #return(1)
    #return(0)
  
  
  def setAssTypes(self):
    rows = utilsPipe.getAssTypes()
    #defStage = utilsPipe.getDefaults("assetTypes")
    #try:
      #if(self.default):
        #present = None
      #else:
        #present = str(self.comboAssType.currentText())
    #except:
      #present = None
    self.comboAssType.clear()  
    indx = 0
    foundIndx = -1
    if(rows):
      for row in rows:
        self.comboAssType.addItem(_fromUtf8(row['type']))
        indx = indx + 1
      self.comboAssType.setEditText("default")
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
    
    if(self.hf):
      if(self.hf.isRunning()):
        if(self.firstTime):
          self.resetFirstTime()
        return(0)
    #print("in get asses timed 1")
    
    #self.tableWidget.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.WaitCursor))
    self.hf = QtCore.QThread(parent=self.tableWidget)
    #print("in get asses timed 2")  
    assget = Worker()
    assget.moveToThread(self.hf)
    assget.dataReady.connect(self.setAssesData)
    if(self.firstTime):
      self.firstTime = False
      assget.dataPending.connect(self.resetFirstTime)
      
    
    #print("in get asses timed 3")
    self.hf.setTerminationEnabled(True)
    self.hf.started.connect(assget.getAsses)
    self.hf.run = assget.getAsses
    self.hf.start()
    
    
    #print("in get asses timed 4")
    
  def setAssesData(self,asslist,assdict):
    self.oldasses = asslist
    self.oldassesdict = assdict
    if(self.listFirstTime):
      self.listFirstTime = False
      self.listAssets_thread()
      # self.loader.hide()
      
    # self.listAssets_thread()
  def resetFirstTime(self):
    self.listFirstTime = True
    # self.loader.show()
    

  def tableWidgetScrollEvent(self,event):
    self.resizeColumnsToContents()
  
  
  def selectedAsses(self):
    rowstask=[]
    rowsSelected = []
    rowsModel = self.tableWidget.selectionModel().selectedRows()
    #print("1 : "+ str(rowsModel))
    for idx in rowsModel:
      #print(dir(idx.model()))
      rowsSelected.append(idx.row())
    print(rowsSelected)
    for row in rowsSelected:
      
      doc = QtGui.QTextDocument()
      doc.setHtml(str(self.tableWidget.cellWidget(row,0).text()))
      text = doc.toPlainText()
      #print("2 : "+ text)
      rowstask.append(str(text))
    return(rowstask)



  
  def listAssets_thread(self,asslist=None,assdict=None):
    #print(str((time.time() - self.listAssTimeOld)))
    #if((time.time() - self.listAssTimeOld) < 1.0):
      #return(0)
    #self.listAssTimeOld = time.time()
    self.loader.show()
    print("list ass thread called")
    selAsses = self.selectedAsses()
    colNames = ['asset','assigned','preview']
    assesList = []
    assesNames = {}
    assesColor = {}
    #self.tableWidget.clear()
    self.tableWidget.clearContents()
    self.tableWidget.setSortingEnabled(False)
    #self.tableWidget.resizeColumnsToContents()
    self.tableWidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
    if(asslist):
      asses = asslist
      self.oldasses = asses
    else:
      asses = self.oldasses

    if(asslist):
      assesdict = assdict
      self.oldassesdict = assesdict
    else:
      assesdict = self.oldassesdict

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

          if(asses[x]['createdUser'] == self.username or asses[x]['assignedWorker'] == self.username):
            
            if(self.considerFilter):

              if(str(self.comboStageType.currentText()) != "default"):
                if(str(asses[x]['stageType']) in str(self.comboStageType.currentText()).split(",")):
                  stageTypeAss = 1
              else:
                stageTypeAss = 1
              
              if(str(self.comboNodeType.currentText()) != "default"):
                if(str(asses[x]['nodeType']) in str(self.comboNodeType.currentText()).split(",")):
                  nodeTypeAss = 1
              else:
                nodeTypeAss = 1
              
              if(str(self.comboSequence.currentText()) != "default"):
                if(str(asses[x]['sequenceName']) in str(self.comboSequence.currentText()).split(",")):
                  seqAss = 1
              else:
                seqAss = 1
                
              if(str(self.comboScene.currentText()) != "default"):
                if(str(asses[x]['sceneName']) in str(self.comboScene.currentText()).split(",")):
                  scnAss = 1
              else:
                scnAss = 1
                
              if(str(self.comboFileType.currentText()) != "default"):
                if(str(asses[x]['fileType']) in str(self.comboFileType.currentText()).split(",")):
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
              assesColor[asses[x]['path']] = utilsPipe.assPathColorCoded(asses[x])
            
            if(stageTypeAss and nodeTypeAss and seqAss and scnAss and nodeTypeAss and fileTypeAss and assTypeAss):
              assesList.append(asses[x]['path'])
              assesNames[asses[x]['path']] = asses[x]
              assesColor[asses[x]['path']] = utilsPipe.assPathColorCoded(asses[x])

        elif(self.radioAllAss.isChecked()):
          
          if(self.considerFilter):

            if(str(self.comboStageType.currentText()) != "default"):
              if(str(asses[x]['stageType']) in str(self.comboStageType.currentText()).split(",")):
                stageTypeAss = 1
            else:
              stageTypeAss = 1
                
            if(str(self.comboNodeType.currentText()) != "default"):
              if(str(asses[x]['nodeType']) in str(self.comboNodeType.currentText()).split(",")):
                nodeTypeAss = 1
            else:
              nodeTypeAss = 1
              
            if(str(self.comboSequence.currentText()) != "default"):
              if(str(asses[x]['sequenceName']) in str(self.comboSequence.currentText()).split(",")):
                seqAss = 1
            else:
              seqAss = 1
              
            if(str(self.comboScene.currentText()) != "default"):
              if(str(asses[x]['sceneName']) in str(self.comboScene.currentText()).split(",")):
                scnAss = 1
            else:
              scnAss = 1
              
            if(str(self.comboFileType.currentText()) != "default"):
              if(str(asses[x]['fileType']) in str(self.comboFileType.currentText()).split(",")):
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
            assesColor[asses[x]['path']] = utilsPipe.assPathColorCoded(asses[x])
          if(stageTypeAss and nodeTypeAss and seqAss and scnAss and nodeTypeAss and fileTypeAss and assTypeAss):
            assesList.append(asses[x]['path'])
            assesNames[asses[x]['path']] = asses[x]
            assesColor[asses[x]['path']] = utilsPipe.assPathColorCoded(asses[x])
    # assesList.sort()      
    if(assesList):
      self.tableWidget.setColumnCount(len(colNames))
      self.tableWidget.setRowCount(len(assesList))
      for cn in range(0,len(colNames)):
        itemcn = QtGui.QTableWidgetItem()
        itemcn.setText(str(colNames[cn]))
        self.tableWidget.setHorizontalHeaderItem(cn, itemcn)
      for x in range(0,len(assesList)):
        #item = QtGui.QTableWidgetItem()
        item = QtGui.QLabel()
        textAss = '<font color="'+ str(assesColor[assesList[x]].split(":")[0]).split("#")[1] +'">'+ (assesColor[assesList[x]].split(":")[0]).split("#")[0] +'</font>'
        if(len(assesColor[assesList[x]].split(":")) > 1):
          for fc in assesColor[assesList[x]].split(":")[1:]:
            textAss = textAss + ':' +'<font color="'+ fc.split("#")[1] +'">'+ fc.split("#")[0] +'</font>'
        
        
        item.setText(textAss)
        #item.setReadOnly(True)
        item.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        item.setTextFormat(QtCore.Qt.RichText)
        #item.setFixedWidth(len(str(assesList[x])))
        item.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        assAbsPath = assesdict[assesList[x]]
        self.tableWidget.setCellWidget(x,0,item)
        

        
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
          #print(assAbsPath +"/"+ previewName +".png")
          prevItem = ImageWidget(assAbsPath +"/"+ previewName +".png",self.tableWidget)
          prevItem.setToolTip('<img src="'+ assAbsPath +"/"+ previewName +".png"+'" height="192"/>')
          self.tableWidget.setCellWidget(x,2,prevItem)
        
        
        
    
    #
    
    #self.tableWidget.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
    
    self.tableWidget.resizeColumnsToContents()
    self.form.statusBar().showMessage("total : "+ str(len(assesList)))
    #self.timerAssetsRefresh.stop()
    self.loader.hide()
    self.tableWidget.setSortingEnabled(True)
    self.tableWidget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
  
  
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
