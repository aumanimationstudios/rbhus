 #!/usr/bin/python
from PyQt4 import QtCore, QtGui, QtSql
import os
import sys
import tempfile
import time
import subprocess
import math
import pickle
from os.path import expanduser

home = expanduser("~")

dirSelf = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep) + os.sep + "lib")

tempDir = tempfile.gettempdir()
rpA = "rbhusPipeProjCreate.py"
rpAss = "rbhusPipeAssetCreate.py"
rpAssEdit = "rbhusPipeAssetEdit.py"
srb = "selectRadioBox.py"
rpS = "rbhusPipeSeqSceCreate.py"
rpSC = "rbhusPipeSeqSceEdit.py"
fileSelect = "fileSelectUI.py"
scb = "selectCheckBox.py"
vc = "rbhusPipeVersions.py"
rS = "rbhusPipeRenderSubmit.py"
rR = "rbhusPipeReview.py"


selectCheckBoxCmd = dirSelf.rstrip(os.sep) + os.sep + scb
#selectCheckBoxCmd = selectCheckBoxCmd.replace("\\","/")
rbhusPipeProjCreateCmd = dirSelf.rstrip(os.sep) + os.sep + rpA
rbhusPipeAssetCreateCmd = dirSelf.rstrip(os.sep) + os.sep + rpAss
rbhusPipeAssetEditCmd = dirSelf.rstrip(os.sep) + os.sep + rpAssEdit
rbhusPipeSeqSceCreateCmd = dirSelf.rstrip(os.sep) + os.sep + rpS
rbhusPipeSeqSceEditCmd = dirSelf.rstrip(os.sep) + os.sep + rpSC
fileSelectCmd = dirSelf.rstrip(os.sep) + os.sep + fileSelect
versionCmd = dirSelf.rstrip(os.sep) + os.sep + vc
rbhusPipeRenderSubmitCmd = dirSelf.rstrip(os.sep) + os.sep + rS
rbhusPipeReviewCmd = dirSelf.rstrip(os.sep) + os.sep + rR



selectRadioBoxCmd = dirSelf.rstrip(os.sep) + os.sep + srb
selectRadioBoxCmd = selectRadioBoxCmd.replace("\\","/")


import rbhusPipeMainMod
sys.path.append(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")
import constantsPipe
import authPipe
import dbPipe
import utilsPipe
import hgmod
import pyperclip
import debug



try:
  _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
  _fromUtf8 = lambda s: s



#db = QtSql.QSqlDatabase.addDatabase("QMYSQL")
#db.setHostName("blues2")
#db.setDatabaseName("rbhusPipe")
#db.open()

class saveSearch:
  searchPath = ''
  searchName = "new fav"

class ExtendedQLabel(QtGui.QLabel):
  clicked = QtCore.pyqtSignal()

  def __init(self):
    QtGui.QLabel.__init__(self)

  def mouseDoubleClickEvent(self, ev):
    self.clicked.emit()

class ImageWidget(QtGui.QPushButton):
  def __init__(self, imagePath, imageSize, parent):
    super(ImageWidget, self).__init__(parent)
    self.imagePath = imagePath
    self.picture = QtGui.QPixmap(imagePath)
    self.picture  = self.picture.scaledToHeight(imageSize,0)

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


#class workerPreviewItems(QtCore.QObject):
  #finished = QtCore.pyqtSignal()
  #dataPending = QtCore.pyqtSignal()
  #dataReady = QtCore.pyqtSignal(int,)


class workerGetAsses(QtCore.QObject):
  finished = QtCore.pyqtSignal()
  dataPending = QtCore.pyqtSignal()
  dataReady = QtCore.pyqtSignal(list,dict,dict,dict,dict)

  def __init__(self):
    super(workerGetAsses, self).__init__()
    self.asses = ()
    self.absdict = {}
    debug.info("init worker thread")
    self.whereDict = {}
    self.assesList = []
    self.assesNames = {}
    self.assesColor = {}
    self.assesLinked = ()
    self.isAssesLinked = False
    self.linkedProjects = ""

  #def terminateEvent(self):
    #debug.info("holy cow . quiting!!")
    #if(self.asses or self.absdict):
      #self.finished.emit()
    #else:
      #self.dataReady.emit(self.asses,self.absdict)

  def getAsses(self):
    self.dataPending.emit()
    # debug.info("in get asses")
    self.asses = ()
    self.assesLinked = ()

    self.absdict = {}
    self.assesList = []
    self.assesNames = {}
    self.assesColor = {}
    self.assModifiedTime = {}
    try:
      #if(self.whereDict):
        #if(self.isAssesLinked):
          #self.assesLinked = utilsPipe.getLibAsses(projNames = self.linkedProjects,whereDict=self.whereDict)
        #self.asses = utilsPipe.getProjAsses(os.environ['rp_proj_projName'],whereDict=self.whereDict)
      #else:
      if(self.isAssesLinked):
        self.assesLinked = utilsPipe.getLibAsses(self.linkedProjects,whereDict = self.whereDict)
        if(self.linkedProjects == "default"):
          self.asses = utilsPipe.getProjAsses(os.environ['rp_proj_projName'],whereDict=self.whereDict)
      else:
        self.asses = utilsPipe.getProjAsses(os.environ['rp_proj_projName'],whereDict=self.whereDict)
      if(self.asses):
        for x in range(0,len(self.asses)):
          try:
            self.absdict[self.asses[x]['path']] = utilsPipe.getAbsPath(self.asses[x]['path'])
          except:
            debug.info(str(sys.exc_info()))
      else:
        self.asses = ()

      if(self.assesLinked):
        for x in range(0,len(self.assesLinked)):
          try:
            self.absdict[self.assesLinked[x]['path']] = utilsPipe.getAbsPath(self.assesLinked[x]['path'])
          except:
            debug.info(str(sys.exc_info()))
      else:
        self.assesLinked = ()
    except:
      debug.info(str(sys.exc_info()))

    self.finished.emit()
    # debug.info("out get asses")
    if(self.asses):
      for x in range(0,len(self.asses)):
        try:
          self.assesList.append(self.asses[x]['path'])
          self.assesNames[self.asses[x]['path']] = self.asses[x]
          self.assesColor[self.asses[x]['path']] = utilsPipe.assPathColorCoded(self.asses[x])
          # self.assModifiedTime[self.asses[x]['path']] = 0
          if(sys.platform.find("linux") >= 0):
            self.assModifiedTime[self.asses[x]['path']] = time.strftime("%Y/%m/%d # %I:%M %p",time.localtime(os.path.getctime(self.absdict[self.asses[x]['path']])))
          elif(sys.platform.find("win") >= 0):
            self.assModifiedTime[self.asses[x]['path']] = time.strftime("%Y/%m/%d # %I:%M %p",time.localtime(os.path.getmtime(self.absdict[self.asses[x]['path']])))
        except:
          debug.info(str(sys.exc_info()))

    if(self.assesLinked):
      for x in range(0,len(self.assesLinked)):
        try:
          self.assesList.append(self.assesLinked[x]['path'])
          self.assesNames[self.assesLinked[x]['path']] = self.assesLinked[x]
          self.assesColor[self.assesLinked[x]['path']] = utilsPipe.assPathColorCoded(self.assesLinked[x])
          self.assModifiedTime[self.asses[x]['path']] = 0
          # if(sys.platform.find("linux") >= 0):
          #   self.assModifiedTime[self.assesLinked[x]['path']] = time.strftime("%Y/%m/%d # %I:%M %p",time.localtime(os.path.getctime(self.absdict[self.assesLinked[x]['path']])))
          # elif(sys.platform.find("win") >= 0):
          #   self.assModifiedTime[self.assesLinked[x]['path']] = time.strftime("%Y/%m/%d # %I:%M %p",time.localtime(os.path.getmtime(self.absdict[self.assesLinked[x]['path']])))
        except:
          debug.info(str(sys.exc_info()))

    self.dataReady.emit(self.assesList,self.assesNames,self.assesColor,self.absdict,self.assModifiedTime)






class Ui_Form(rbhusPipeMainMod.Ui_MainWindow):
  def setupUi(self, Form):

    rbhusPipeMainMod.Ui_MainWindow.setupUi(self,Form)
    self.form = Form
    self.form.setWindowState(QtCore.Qt.WindowMaximized)

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
    self.previewItems = {}
    self.previewWidgets = []

    self.searchDict = {}
    self.assFavDict = {}
    self.saveSearchArray = []
    self.assSearchArray = []

    self.saveFile = ""
    self.saveFileShortcut = ""
    self.dbcon = dbPipe.dbPipe()

    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(_fromUtf8(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/rbhusPipe.svg")), QtGui.QIcon.Normal, QtGui.QIcon.On)
    self.form.setWindowIcon(icon)



    self.menuMine = QtGui.QMenu()
    self.mineCreatedAction = QtGui.QAction("created",self.menuMine,checkable=True)
    self.mineCreatedAction.setChecked(False)
    self.mineCreatedAction.changed.connect(self.mineCheck)
    self.mineAssignedAction = QtGui.QAction("assigned",self.menuMine,checkable=True)
    self.mineAssignedAction.setChecked(True)
    self.mineAssignedAction.changed.connect(self.mineCheck)
    self.mineReviewAction = QtGui.QAction("toReview",self.menuMine,checkable=True)
    self.mineReviewAction.changed.connect(self.mineCheck)
    self.mineReviewAction.setChecked(False)

    self.menuMine.addAction(self.mineCreatedAction)
    self.menuMine.addAction(self.mineAssignedAction)
    self.menuMine.addAction(self.mineReviewAction)
    self.menuMine.triggered.connect(self.menuMineShow)

    self.splitterFilter.setStretchFactor(0, 10)
    self.splitterAssets.setStretchFactor(0, 10)
    try:
      self.username = os.environ['rbhusPipe_acl_user'].rstrip().lstrip()
    except:
      pass


    iconRefresh = QtGui.QIcon()
    iconRefresh.addPixmap(QtGui.QPixmap(_fromUtf8(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/ic_action_refresh.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)

    iconAdd= QtGui.QIcon()
    iconAdd.addPixmap(QtGui.QPixmap(_fromUtf8(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/ic_action_new.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)



    self.assRefresh.setIcon(iconRefresh)


    iconCancel = QtGui.QIcon()
    iconCancel.addPixmap(QtGui.QPixmap(_fromUtf8(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/ic_action_cancel.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)

    self.pushResetAsset.setIcon(iconRefresh)
    self.pushResetSeq.setIcon(iconRefresh)
    self.pushResetStage.setIcon(iconRefresh)
    self.pushResetScene.setIcon(iconRefresh)
    self.pushResetNode.setIcon(iconRefresh)
    self.pushResetAsset.setIcon(iconRefresh)
    self.pushResetFile.setIcon(iconRefresh)
    self.filterRefresh.setIcon(iconRefresh)
    self.pushResetLinked.setIcon(iconRefresh)
    self.pushAssetFavReset.setIcon(iconCancel)
    self.pushSearchFav.setIcon(iconRefresh)
    self.searchRefresh.setIcon(iconRefresh)

    self.pushSearchFav.setIcon(iconAdd)
    self.pushSearchFavReset.setIcon(iconCancel)


    self.iconDanger = QtGui.QIcon()
    self.iconDanger.addPixmap(QtGui.QPixmap(_fromUtf8(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/danger.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)




    self.timerAssetsRefresh = QtCore.QTimer()
    self.timerAssetsRefresh.timeout.connect(self.listAssetsTimed)



    self.pushLogout.setText("logout : "+ str(self.username))
    self.pushLogout.clicked.connect(self.logout)

    self.wFlag = self.form.windowFlags()
    self.trayIcon = QtGui.QSystemTrayIcon(QtGui.QIcon(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/rbhusPipe.svg"))
    self.trayIcon.show()

    self.trayMenu = QtGui.QMenu()



    #self.sliderPreview.valueChanged.connect(self.sliderZoom)



    #self.tableWidget.resizeEvent

    self.quitAction = self.trayMenu.addAction("quit")
    self.quitAction.triggered.connect(self.quitFunc)

    self.trayIcon.setContextMenu(self.trayMenu)
    self.trayIcon.activated.connect(self.showMain)

    self.actionNew_project.triggered.connect(self.rbhusPipeProjCreate)
    self.actionSet_project.triggered.connect(self.rbhusPipeSetProject)
    self.actionNew_seq_scn.triggered.connect(self.rbhusPipeSeqSceCreate)
    self.actionEdit_seq_scn.triggered.connect(self.rbhusPipeSeqSceEdit)
    self.pushNewAsset.clicked.connect(self.rbhusPipeAssetCreate)
    self.filterRefresh.clicked.connect(self.resetFilterDefault)
    self.assRefresh.clicked.connect(self.assRefreshPressed)
    self.previewEnabled.clicked.connect(self.previewCheck)



    slineedit = self.comboStageType.lineEdit()
    slineedit.setReadOnly(True)
    self.comboStageType.editTextChanged.connect(self.listAssets)
    self.comboStageType.view().activated.connect(self.pressedStageType)
    #self.comboStageType.released.connect(self.pressedAction)
    #self.comboStageType.completer().setCompletionMode(QtGui.QCompleter.PopupCompletion)
    self.pushResetStage.clicked.connect(self.setStageTypes)

    linkedit = self.comboLinked.lineEdit()
    linkedit.setReadOnly(True)
    self.comboLinked.editTextChanged.connect(self.listAssets)
    self.comboLinked.view().activated.connect(self.pressedLinked)
    #self.comboStageType.released.connect(self.pressedAction)
    #self.comboStageType.completer().setCompletionMode(QtGui.QCompleter.PopupCompletion)
    self.pushResetLinked.clicked.connect(self.setLinkedProj)

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

    asstypelineedit = self.comboAssType.lineEdit()
    asstypelineedit.setReadOnly(True)
    self.comboAssType.currentIndexChanged.connect(self.listAssets)
    #self.comboAssType.completer().setCompletionMode(QtGui.QCompleter.PopupCompletion)
    self.pushResetAsset.clicked.connect(self.setAssTypes)

    self.comboFileType.currentIndexChanged.connect(self.listAssets)
    #self.comboFileType.completer().setCompletionMode(QtGui.QCompleter.PopupCompletion)

    self.radioAllAss.clicked.connect(self.listAssets)
    self.checkLinkedProjects.clicked.connect(self.listAssets)
    # self.radioMineAss.toggled.connect(self.listAssets)
    self.radioMineAss.clicked.connect(self.popupMine)

    self.lineEditSearch.returnPressed.connect(self.listAssets)
    # self.lineEditSearch.textChanged.connect(self.listAssets)


    self.checkTags.clicked.connect(self.setTags)
    self.checkUsers.clicked.connect(self.setUsers)
    #self.checkCase.clicked.connect(self.listAssets)
    #self.checkWords.clicked.connect(self.listAssets)


    #self.form.closeEvent = self.closeEvent


    self.loadingGif = dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/loading.gif"
    self.loader = ImagePlayer(self.loadingGif,parent=self.tableWidget)
    self.loader.hide()


    self.rbhusPipeSetProjDefault()
    # self.form.hideEvent = self.hideEvent
    self.form.closeEvent = self.hideEvent

    # set up the right-click context menu for tableWidget
    self.tableWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    self.tableWidget.customContextMenuRequested.connect(self.popupAss)

    self.listWidgetSearch.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    self.listWidgetSearch.customContextMenuRequested.connect(self.popUpSearchFav)

    self.listWidgetAssets.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    self.listWidgetAssets.customContextMenuRequested.connect(self.popUpAssetFav)


    self.timer = QtCore.QTimer()
    self.timer.timeout.connect(self.listAssets)
    self.checkRefresh.clicked.connect(self.timeCheck)



    #self.checkFilterFunc()
    self.centralwidget.resizeEvent  = self.resizeEvent
    self.tableWidget.resizeEvent = self.resizeEvent
    self.tableWidget.verticalScrollBar().valueChanged.connect(self.tableWidgetResizeContents)
    #self.updateAll()

    self.listAssetsTimed()

    self.searchRefresh.clicked.connect(self.pushResetSearchFunc)
    self.pushSearchFav.clicked.connect(self.saveSearchItem)
    self.listWidgetSearch.itemChanged.connect(self.searchItemChanged)
    #self.listWidgetSearch.itemPressed.connect(self.searchItemActivate)
    self.pushSearchFavReset.clicked.connect(self.clearSearchFav)
    #self.timerAss = QtCore.QTimer()
    #self.timerAss.timeout.connect(self.listAssetsTimed)
    #self.timerAss.start(2000)
    #self.loadSearch()

  #def sliderZoom(self,value):
    #self.labelZoomValue.setText(str(value) +"x")
    #self.previewCheck()



  def pushResetSearchFunc(self):
    self.lineEditSearch.setText("")
    self.listAssets()

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
    pass
    # self.tableWidget.resizeColumnsToContents()

  def comboStageTypeEvent(self,event):
    debug.info(event)

  def listAssets(self):
    # self.listAssetsTimed()
    # self.listAssets_thread()

    #debug.info("list assets called")
    if(self.timerAssetsRefresh.isActive()):
      self.timerAssetsRefresh.stop()
      self.timerAssetsRefresh.start(2000)
    else:
      self.timerAssetsRefresh.start(2000)




  def timeCheck(self):
    cRefresh = self.checkRefresh.isChecked()
    if(cRefresh):
      self.startTimer()
    else:
      self.stopTimer()

  def startTimer(self):
    self.timer.start(15000)

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
    listAsses = self.selectedAsses()
    debug.info("selected asses : "+ str(len(listAsses)))
    if(len(listAsses) == 0):
      return(0)

    menu = QtGui.QMenu()
    menuProgress = QtGui.QMenu()
    menuCopy = QtGui.QMenu()
    menuCopy.setTitle("copy to clipboard")
    menuProgress.setTitle("progress status")

    inProgressAction = menuProgress.addAction("set to inProgress")
    inProgressDoneAction = menuProgress.addAction("set to done")

    assCopyToClip = menuCopy.addAction("copy path to clipboard")
    assCopyPathToClip = menuCopy.addAction("copy assetPath to clipboard")
    assPublishPath = menuCopy.addAction("copy publish path to clipboard")


    #openFileAction = menu.addAction("open file")
    openFolderAction = menu.addAction("open")
    addToFavAction = menu.addAction("add to shortcuts")
    #versionAction = menu.addAction("versioning")
    assEditAction = menu.addAction("edit")

    assReviewAction = menu.addAction("review")
    menu.addMenu(menuCopy)
    menu.addMenu(menuProgress)
    # assCopyNew = menu.addAction("copy/new")
    assGetTemplate = menu.addAction("reset templates")
    #assCmdLine = menu.addAction("cmd line")
    assRender = menu.addAction("submit to render")
    assDeleteAction = menu.addAction("delete - database only")
    #assDeleteActionHard = menu.addAction("delete - database and disk")

    action = menu.exec_(self.tableWidget.mapToGlobal(pos))
    #if(action == openFileAction):
      #self.openFileAss()
    if(action == openFolderAction):
      self.openFolderAss()
    if(action == assCopyToClip):
      self.copyPathToClip()
    if(action == assCopyPathToClip):
      self.copyPipePathToClip()
    if(action == assEditAction):
      self.editAss()
    if(action == assDeleteAction):
      self.delAss()
    #if(action == assDeleteActionHard):
      #self.delAss(hard=True)

    # if(action == assCopyNew):
    #   self.copyNewAss()
    if(action == assRender):
      self.renderAss()
    if(action == assGetTemplate):
      self.resetTemplateFiles()
    if(action == addToFavAction):
      self.assetFavSave()

    if(action == assReviewAction):
      self.reviewAss()
    if(action == assPublishPath):
      self.copyPublishPath()

    if(action == inProgressAction):
      self.setInProgress()
    if(action == inProgressDoneAction):
      self.setDone()

    #if(action == versionAction):
      #self.versionAss()



  def setInProgress(self):
    listAsses = self.selectedAsses()
    for x in listAsses:
      utilsPipe.setWorkInProgress(x)

  def setDone(self):
    listAsses = self.selectedAsses()
    for x in listAsses:
      utilsPipe.setWorkDone(x)




  def popupMine(self):
    cursor =QtGui.QCursor()
    self.menuMine.exec_(cursor.pos())
    # self.menuMine.popup(cursor.pos())
    self.listAssets()

  def mineCheck(self):
    if(not self.mineCreatedAction.isChecked() and not self.mineAssignedAction.isChecked() and not self.mineReviewAction.isChecked()):
      self.mineAssignedAction.setChecked(True)
    if(self.mineReviewAction.isChecked()):
      self.mineCreatedAction.setChecked(False)
      self.mineAssignedAction.setChecked(False)
    self.listAssets()



  def menuMineShow(self):
    self.menuMine.show()


  def reviewAss(self):
    listAsses = self.selectedAsses()
    listedAss = listAsses[0]
    if(sys.platform.find("win") >= 0):
      subprocess.Popen([rbhusPipeReviewCmd,"--assetpath",listedAss],shell = True)
    elif(sys.platform.find("linux") >= 0):
      subprocess.Popen(rbhusPipeReviewCmd +" --assetpath "+ listedAss,shell = True)




  def renderAss(self):
    filesTorender = self.getFileAss()
    listAsses = self.selectedAsses()
    listedAss = listAsses[0]
    renderFiles = []
    if(not isinstance(filesTorender,int)):
      for x in filesTorender:
        if(x):
          renderFiles.append(str(x))
    if(renderFiles):
      debug.info(renderFiles[0])
      subprocess.Popen(rbhusPipeRenderSubmitCmd +" --file \""+ renderFiles[0] +"\" --path \""+ listedAss +"\"",shell=True)      #os.system(versionCmd +" --path \""+ selass[-1] +"\"")
      return(1)
    else:
      return(0)



  def copyNewAss(self):
    pass


  def copyPathToClip(self):
    listAsses = self.selectedAsses()
    debug.info(listAsses)
    if(listAsses):
      x = listAsses[0]
      abspath =  utilsPipe.getAbsPath(x)
      pyperclip.copy(abspath)

  def copyPublishPath(self):
    listAsses = self.selectedAsses()
    debug.info(listAsses)
    if(listAsses):
      x = listAsses[0]
      abspath =  utilsPipe.getAbsPath(x)
      abspath = abspath + "/publish"
      pyperclip.copy(abspath)




  def copyPipePathToClip(self):
    listAsses = self.selectedAsses()
    debug.info(listAsses)
    if(listAsses):
      x = listAsses[0]
      pyperclip.copy(x)




  def openFileAss(self):
    listAsses = self.selectedAsses()
    debug.info(listAsses)
    fcmd = fileSelectCmd
    if(listAsses):
      x = listAsses[0]
      fcmd = fcmd +" "+ utilsPipe.getAbsPath(x)
      debug.info(fcmd)
      p = QtCore.QProcess(parent=self.form)
      #p.setStandardOutputFile(tempDir + os.sep +"rbhusOpenFileAss_"+ self.username +".log")
      p.setStandardErrorFile(tempDir + os.sep +"rbhusOpenFileAss_"+ self.username +".err")
      p.start(sys.executable,fcmd.split())
      p.waitForFinished()
      filename = str(p.readAllStandardOutput()).rstrip().lstrip()

      if(filename):
        debug.info(filename.split("."))
        if(filename.split(".")[-1] == "py"):
          subprocess.Popen("python "+ str(filename),shell=True)
        else:
          assdets = utilsPipe.getAssDetails(assPath=x)
          runCmd = utilsPipe.openAssetCmd(assdets,filename)
          debug.info("wtf1 : "+ str(runCmd))
          fileTypeDets = None
          if(runCmd):
            runCmd = runCmd.rstrip().lstrip()
            subprocess.Popen(runCmd,shell=True)
          else:
            import webbrowser
            webbrowser.open(filename)




  def getFileAss(self,favSearch=False):
    if(favSearch):
      i = self.listWidgetAssets.currentRow()
      debug.info("current row selected :"+ str(i))
      x = self.assSearchArray[i]
    else:
      listAsses = self.selectedAsses()
      x = str(listAsses[0])
    if(x): # and (len(listAsses) == 1)
      #x = str(listAsses[0])
      debug.info(x)
      p = utilsPipe.getAbsPath(x)
      if(os.path.exists(p)):
        fila = QtGui.QFileDialog.getOpenFileNames(directory=p)
        if(fila):
          return(fila)
        else:
          return(0)
      else:
        return(0)


  def openFolderAss(self,favSearch = False):
    self.centralwidget.setCursor(QtCore.Qt.WaitCursor)
    if(favSearch):
      i = self.listWidgetAssets.currentRow()
      debug.info("current row selected :"+ str(i))
      x = self.assSearchArray[i]
    else:
      listAsses = self.selectedAsses()
      x = str(listAsses[0])
    if(x): # and (len(listAsses) == 1)
      #x = str(listAsses[0])
      debug.info(x)
      p = utilsPipe.getAbsPath(x)
      assdets = utilsPipe.getAssDetails(assPath=x)
      debug.info("isAssCreated : "+ str(assdets['createdUser']) +" : "+ str(utilsPipe.isAssCreated(assdets)))
      debug.info("isAssAssigned : "+ str(assdets['assignedWorker']) +" : "+ str(utilsPipe.isAssAssigned(assdets)))
      debug.info("isStageAdmin : "+ str(assdets['stageType']) +" : "+ str(utilsPipe.isStageAdmin(assdets)))
      debug.info("isNodeAdmin : "+ str(assdets['nodeType']) +" : "+ str(utilsPipe.isNodeAdmin(assdets)))
      debug.info("isProjAdmin : "+ str(assdets['projName']) +" : "+ str(utilsPipe.isProjAdmin(assdets)))
      debug.info("versioning : "+ str(assdets['versioning']))
      if(os.path.exists(p)):
        if(assdets['versioning'] == 0):
          fila = QtGui.QFileDialog.getOpenFileNames(directory=p)
          debug.info(fila)
          if(fila):
            debug.info(str(fila[0]))
            filename = str(fila[0])
            debug.info(filename.split("."))
            assdets = utilsPipe.getAssDetails(assPath=x)
            runCmd = utilsPipe.openAssetCmd(assdets,filename)
            if(runCmd):
              runCmd = runCmd.rstrip().lstrip()
              if(sys.platform.find("win") >= 0):
                debug.info(runCmd)
                subprocess.Popen(runCmd,shell=True)
              elif(sys.platform.find("linux") >= 0):
                debug.info(runCmd)
                subprocess.Popen(runCmd,shell=True)
            else:
              import webbrowser
              webbrowser.open(filename)
        else:
          debug.info("wtf : opening version cmd ")
          if(sys.platform.find("win") >= 0):
            subprocess.Popen([versionCmd,"--path",x],shell = True)
          elif(sys.platform.find("linux") >= 0):
            subprocess.Popen(versionCmd +" --path "+ x,shell = True)
    self.centralwidget.setCursor(QtCore.Qt.ArrowCursor)
    for x in os.environ.keys():
      if(x.find("rp_") >= 0):
        debug.info(x +" : "+os.environ[x])





  def newFolderAss(self):
    pass






  def delAss(self,hard=False):
    wtf = self.messageBoxDelete(hard=hard)
    if(wtf):
      listAsses = self.selectedAsses()

      for x in listAsses:
        debug.info(x)
        if(str(x)):
          utilsPipe.assMarkForDelete(assPath=str(x))
      self.listAssets()


  def editAss(self):
    listAsses = self.selectedAsses()
    debug.info(listAsses)
    if(listAsses):
      self.rbhusAssetEditCmdMod = rbhusPipeAssetEditCmd +" -p "+ ",".join(listAsses)
      debug.info(self.rbhusAssetEditCmdMod)
      self.rbhusPipeAssetEdit()
    #for x in listAsses:
      #if(str(x)):
        #debug.info(str(x))

  def versionAss(self):
    selass = self.selectedAsses()
    subprocess.Popen(versionCmd +" --path \""+ selass[-1] +"\"",shell=True)      #os.system(versionCmd +" --path \""+ selass[-1] +"\"")


  def resetTemplateFiles(self):
    selass = self.selectedAsses()
    for x in range(0,len(selass)):
      debug.info(selass[x])
      assDets = utilsPipe.getAssDetails(assPath = selass[x])
      utilsPipe.setAssTemplate(assDets)

  def setLinkedProj(self):
    try:
      rows = os.environ["rp_proj_linkedProjects"].split(",")
    except:
      debug.info(str(sys.exc_info()))
      return(0)
    self.comboLinked.clear()
    indx = 0
    model = QtGui.QStandardItemModel(len(rows),1)
    if(rows):
      for row in rows:
        item = QtGui.QStandardItem(row)
        #item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        if(sys.platform.find("linux") >=0):
          item.setFlags(QtCore.Qt.ItemIsEnabled)
        elif(sys.platform.find("win") >=0):
          item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        item.setData(QtCore.Qt.Unchecked, QtCore.Qt.CheckStateRole)
        model.setItem(indx,0,item)
        abrush = QtGui.QBrush()
        color = QtGui.QColor()
        color.setAlpha(0)
        abrush.setColor(color)
        model.item(indx).setForeground(abrush)
        indx = indx + 1
      model.itemChanged.connect(self.itemChangedStageType)
      self.comboLinked.setModel(model)
      self.comboLinked.setEditText("default")
      return(1)
    return(0)


  def itemChangedLinked(self,item):
    if(item.checkState() == QtCore.Qt.Checked):
      abrush = QtGui.QBrush()
      color = QtGui.QColor()
      color.setGreen(10)
      color.setBlue(125)
      color.setRed(225)
      abrush.setColor(color)
      item.setForeground(abrush)
    else:
      abrush = QtGui.QBrush()
      color = QtGui.QColor()
      color.setAlpha(0)
      abrush.setColor(color)
      item.setForeground(abrush)

    linkedProjects = []

    for i in range(0,self.comboLinked.model().rowCount()):
      if(self.comboLinked.model().item(i).checkState() == QtCore.Qt.Checked):
        linkedProjects.append(str(self.comboLinked.model().item(i).text()))

    #debug.info("EVENT CALLED : "+ str(index.row()))
    if(linkedProjects):
      self.comboLinked.setEditText(",".join(linkedProjects))
    else:
      self.comboLinked.setEditText("default")


  def pressedLinked(self, index):
    if(self.comboLinked.model().item(index.row()).checkState() != 0):
      self.comboLinked.model().item(index.row()).setCheckState(QtCore.Qt.Unchecked)
      #self.comboStageType.model().item(index.row()).setEnabled(False)
      abrush = QtGui.QBrush()
      color = QtGui.QColor()
      color.setAlpha(0)
      abrush.setColor(color)
      self.comboLinked.model().item(index.row()).setForeground(abrush)
    else:
      self.comboLinked.model().item(index.row()).setCheckState(QtCore.Qt.Checked)
      #self.comboStageType.model().item(index.row()).setEnabled(True)
      abrush = QtGui.QBrush()
      color = QtGui.QColor()
      color.setGreen(10)
      color.setBlue(125)
      color.setRed(225)
      abrush.setColor(color)
      self.comboLinked.model().item(index.row()).setForeground(abrush)
    linkedProjects = []
    for i in range(0,self.comboLinked.model().rowCount()):
      if(self.comboLinked.model().item(i).checkState() == QtCore.Qt.Checked):
        linkedProjects.append(str(self.comboLinked.model().item(i).text()))
    #debug.info("EVENT CALLED : "+ str(index.row()))
    if(linkedProjects):
      self.comboLinked.setEditText(",".join(linkedProjects))
    else:
      self.comboLinked.setEditText("default")


  def setStageTypes(self):
    rows = utilsPipe.getStageTypes()
    #defStage = utilsPipe.getDefaults("stageTypes")
    self.comboStageType.clear()
    indx = 0
    model = QtGui.QStandardItemModel(len(rows),1)
    if(rows):
      for row in rows:
        item = QtGui.QStandardItem(row['type'])
        #item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        if(sys.platform.find("linux") >=0):
          item.setFlags(QtCore.Qt.ItemIsEnabled)
        elif(sys.platform.find("win") >=0):
          item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        item.setData(QtCore.Qt.Unchecked, QtCore.Qt.CheckStateRole)
        model.setItem(indx,0,item)
        abrush = QtGui.QBrush()
        color = QtGui.QColor()
        color.setAlpha(0)
        abrush.setColor(color)
        model.item(indx).setForeground(abrush)
        indx = indx + 1
      model.itemChanged.connect(self.itemChangedStageType)
      self.comboStageType.setModel(model)
      self.comboStageType.setEditText("default")
      return(1)
    return(0)

  def itemChangedStageType(self,item):
    if(item.checkState() == QtCore.Qt.Checked):
      abrush = QtGui.QBrush()
      color = QtGui.QColor()
      color.setGreen(10)
      color.setBlue(125)
      color.setRed(225)
      abrush.setColor(color)
      item.setForeground(abrush)
    else:
      abrush = QtGui.QBrush()
      color = QtGui.QColor()
      color.setAlpha(0)
      abrush.setColor(color)
      item.setForeground(abrush)

    selectedStages = []

    for i in range(0,self.comboStageType.model().rowCount()):
      if(self.comboStageType.model().item(i).checkState() == QtCore.Qt.Checked):
        selectedStages.append(str(self.comboStageType.model().item(i).text()))

    #debug.info("EVENT CALLED : "+ str(index.row()))
    if(selectedStages):
      self.comboStageType.setEditText(",".join(selectedStages))
    else:
      self.comboStageType.setEditText("default")

  def pressedStageType(self, index):
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
    selectedStages = []
    for i in range(0,self.comboStageType.model().rowCount()):
      if(self.comboStageType.model().item(i).checkState() == QtCore.Qt.Checked):
        selectedStages.append(str(self.comboStageType.model().item(i).text()))

    #debug.info("EVENT CALLED : "+ str(index.row()))
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
      sortedsc = []
      for s in scenes.keys():
        if(s):
          sortedsc.append(s)

      sortedsc.sort()
      model = QtGui.QStandardItemModel(len(scenes),1)
      for x in sortedsc:
        item = QtGui.QStandardItem(x)
        if(sys.platform.find("linux") >=0):
          item.setFlags(QtCore.Qt.ItemIsEnabled)
        elif(sys.platform.find("win") >=0):
          item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        #item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        item.setData(QtCore.Qt.Unchecked, QtCore.Qt.CheckStateRole)
        model.setItem(indx,0,item)
        abrush = QtGui.QBrush()
        color = QtGui.QColor()
        color.setAlpha(0)
        abrush.setColor(color)
        model.item(indx).setForeground(abrush)
        indx = indx + 1
      model.itemChanged.connect(self.itemChangedScenes)
      self.comboScene.setModel(model)
      self.comboScene.setEditText("default")
      return(1)
    return(0)


  def itemChangedScenes(self,item):
    if(item.checkState() == QtCore.Qt.Checked):
      abrush = QtGui.QBrush()
      color = QtGui.QColor()
      color.setGreen(10)
      color.setBlue(125)
      color.setRed(225)
      abrush.setColor(color)
      item.setForeground(abrush)
    else:
      abrush = QtGui.QBrush()
      color = QtGui.QColor()
      color.setAlpha(0)
      abrush.setColor(color)
      item.setForeground(abrush)

    selectedStages = []

    for i in range(0,self.comboScene.model().rowCount()):
      if(self.comboScene.model().item(i).checkState() == QtCore.Qt.Checked):
        selectedStages.append(str(self.comboScene.model().item(i).text()))

    #debug.info("EVENT CALLED : "+ str(index.row()))
    if(selectedStages):
      self.comboScene.setEditText(",".join(selectedStages))
    else:
      self.comboScene.setEditText("default")



  def pressedScene(self, index):


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
    selectedStages = []
    for i in range(0,self.comboScene.model().rowCount()):
      if(self.comboScene.model().item(i).checkState() == QtCore.Qt.Checked):
        selectedStages.append(str(self.comboScene.model().item(i).text()))

    #debug.info("EVENT CALLED : "+ str(index.row()))
    if(selectedStages):
      self.comboScene.setEditText(",".join(selectedStages))
    else:
      self.comboScene.setEditText("default")


  def setSequence(self):
    rows = utilsPipe.getSequenceScenes(os.environ['rp_proj_projName'])
    #try:
      #if(self.default):
        #present = None
      #else:
        #present = str(self.comboSequence.currentText())
    #except:
      #present = None
    self.comboSequence.clear()
    seq = {}
    indx =  0
    foundIndx = -1

    for row in rows:
      seq[row['sequenceName']] = 1

    model = QtGui.QStandardItemModel(len(seq),1)

    if(seq):
      sortedsc = []
      for s in seq.keys():
        if(s):
          sortedsc.append(s)

      sortedsc.sort()
      for row in sortedsc:
        item = QtGui.QStandardItem(row)
        if(sys.platform.find("linux") >=0):
          item.setFlags(QtCore.Qt.ItemIsEnabled)
        elif(sys.platform.find("win") >=0):
          item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        #item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        item.setData(QtCore.Qt.Unchecked, QtCore.Qt.CheckStateRole)
        model.setItem(indx,0,item)
        abrush = QtGui.QBrush()
        color = QtGui.QColor()
        color.setAlpha(0)
        abrush.setColor(color)
        model.item(indx).setForeground(abrush)
        indx = indx + 1
      model.itemChanged.connect(self.itemChangedSequence)
      self.comboSequence.setModel(model)
      self.comboSequence.setEditText("default")
      return(1)
    return(0)


  def itemChangedSequence(self,item):
    if(item.checkState() == QtCore.Qt.Checked):
      abrush = QtGui.QBrush()
      color = QtGui.QColor()
      color.setGreen(10)
      color.setBlue(125)
      color.setRed(225)
      abrush.setColor(color)
      item.setForeground(abrush)
    else:
      abrush = QtGui.QBrush()
      color = QtGui.QColor()
      color.setAlpha(0)
      abrush.setColor(color)
      item.setForeground(abrush)

    selectedStages = []

    for i in range(0,self.comboSequence.model().rowCount()):
      if(self.comboSequence.model().item(i).checkState() == QtCore.Qt.Checked):
        selectedStages.append(str(self.comboSequence.model().item(i).text()))

    #debug.info("EVENT CALLED : "+ str(index.row()))
    if(selectedStages):
      self.comboSequence.setEditText(",".join(selectedStages))
    else:
      self.comboSequence.setEditText("default")


  def pressedSequence(self, index):
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
    selectedStages = []
    for i in range(0,self.comboSequence.model().rowCount()):
      if(self.comboSequence.model().item(i).checkState() == QtCore.Qt.Checked):
        selectedStages.append(str(self.comboSequence.model().item(i).text()))

    #debug.info("EVENT CALLED : "+ str(index.row()))
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
        #item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        if(sys.platform.find("linux") >=0):
          item.setFlags(QtCore.Qt.ItemIsEnabled)
        elif(sys.platform.find("win") >=0):
          item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        item.setData(QtCore.Qt.Unchecked, QtCore.Qt.CheckStateRole)
        model.setItem(indx,0,item)
        abrush = QtGui.QBrush()
        color = QtGui.QColor()
        color.setAlpha(0)
        abrush.setColor(color)
        model.item(indx).setForeground(abrush)
        indx = indx + 1
      model.itemChanged.connect(self.itemChangedNodeType)
      self.comboNodeType.setModel(model)
      self.comboNodeType.setEditText("default")
      return(1)
    return(0)

  def itemChangedNodeType(self,item):
    if(item.checkState() == QtCore.Qt.Checked):
      abrush = QtGui.QBrush()
      color = QtGui.QColor()
      color.setGreen(10)
      color.setBlue(125)
      color.setRed(225)
      abrush.setColor(color)
      item.setForeground(abrush)
    else:
      abrush = QtGui.QBrush()
      color = QtGui.QColor()
      color.setAlpha(0)
      abrush.setColor(color)
      item.setForeground(abrush)

    selectedStages = []

    for i in range(0,self.comboNodeType.model().rowCount()):
      if(self.comboNodeType.model().item(i).checkState() == QtCore.Qt.Checked):
        selectedStages.append(str(self.comboNodeType.model().item(i).text()))

    #debug.info("EVENT CALLED : "+ str(index.row()))
    if(selectedStages):
      self.comboNodeType.setEditText(",".join(selectedStages))
    else:
      self.comboNodeType.setEditText("default")

  def pressedNodeType(self, index):

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
    selectedStages = []
    for i in range(0,self.comboNodeType.model().rowCount()):
      if(self.comboNodeType.model().item(i).checkState() == QtCore.Qt.Checked):
        selectedStages.append(str(self.comboNodeType.model().item(i).text()))

    #debug.info("EVENT CALLED : "+ str(index.row()))
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
        if(sys.platform.find("linux") >=0):
          item.setFlags(QtCore.Qt.ItemIsEnabled)
        elif(sys.platform.find("win") >=0):
          item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        #item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        #item.setFlags(QtCore.Qt.ItemIsEnabled)
        item.setData(QtCore.Qt.Unchecked, QtCore.Qt.CheckStateRole)
        model.setItem(indx,0,item)
        abrush = QtGui.QBrush()
        color = QtGui.QColor()
        color.setAlpha(0)
        abrush.setColor(color)
        model.item(indx).setForeground(abrush)
        indx = indx + 1
      model.itemChanged.connect(self.itemChangedFileType)
      self.comboFileType.setModel(model)
      self.comboFileType.setEditText("default")
      return(1)
    return(0)

  def itemChangedFileType(self,item):
    if(item.checkState() == QtCore.Qt.Checked):
      abrush = QtGui.QBrush()
      color = QtGui.QColor()
      color.setGreen(10)
      color.setBlue(125)
      color.setRed(225)
      abrush.setColor(color)
      item.setForeground(abrush)
    else:
      abrush = QtGui.QBrush()
      color = QtGui.QColor()
      color.setAlpha(0)
      abrush.setColor(color)
      item.setForeground(abrush)

    selectedStages = []

    for i in range(0,self.comboFileType.model().rowCount()):
      if(self.comboFileType.model().item(i).checkState() == QtCore.Qt.Checked):
        selectedStages.append(str(self.comboFileType.model().item(i).text()))

    #debug.info("EVENT CALLED : "+ str(index.row()))
    if(selectedStages):
      self.comboFileType.setEditText(",".join(selectedStages))
    else:
      self.comboFileType.setEditText("default")

  def pressedFileType(self, index):


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
    selectedStages = []
    for i in range(0,self.comboFileType.model().rowCount()):
      if(self.comboFileType.model().item(i).checkState() == QtCore.Qt.Checked):
        selectedStages.append(str(self.comboFileType.model().item(i).text()))

    #debug.info("EVENT CALLED : "+ str(index.row()))
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


  def messageBoxDelete(self,hard=False):
    msgbox = QtGui.QMessageBox()
    if(hard == True):
      delmsg = "DELETE (database and disk)?!?!?!"
    else:
      delmsg = "DELETE (database only)?!?!?!"
    msgbox.setText(delmsg +"\nDo you want to really delete this asset?!")
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
        return(0)
    self.hf = QtCore.QThread(parent=self.tableWidget)
    assget = workerGetAsses()
    assget.whereDict = {}
    assget.dataReady.connect(self.listAssets_thread)
    assget.dataPending.connect(self.loaderShow)


    if(self.radioMineAss.isChecked()):
      if(self.mineAssignedAction.isChecked()):
        assget.whereDict['assignedWorker'] = str(self.username)
      if(self.mineCreatedAction.isChecked()):
        assget.whereDict['createdUser'] = str(self.username)
      if(self.mineReviewAction.isChecked()):
        assget.whereDict['reviewUser'] = str(self.username)
        assget.whereDict['reviewStatus'] = str(constantsPipe.reviewStatusInProgress)
    if(self.comboStageType.currentText() != "default"):
      assget.whereDict['stageType'] = str(self.comboStageType.currentText())
    if(self.comboNodeType.currentText() != "default"):
      assget.whereDict['nodeType'] = str(self.comboNodeType.currentText())
    if(self.comboSequence.currentText() != "default"):
      assget.whereDict['sequenceName'] = str(self.comboSequence.currentText())
    if(self.comboScene.currentText() != "default"):
      assget.whereDict['sceneName'] = str(self.comboScene.currentText())
    if(self.comboFileType.currentText() != "default"):
      assget.whereDict['fileType'] = str(self.comboFileType.currentText())
    if(self.comboAssType.currentText() != "default"):
      assget.whereDict['assetType'] = str(self.comboAssType.currentText())

    if(self.checkLinkedProjects.isChecked()):
      #if(str(self.comboAssType.currentText()) == "library" or str(self.comboAssType.currentText()) == "default"):
      assget.isAssesLinked = True
      assget.linkedProjects = str(self.comboLinked.currentText())
      #assget.whereDict['assetType'] = "library"

    searchItems = str(self.lineEditSearch.text())
    if(searchItems):
      if(not self.radioMineAss.isChecked()):
        if(self.checkUsers.isChecked()):
          assget.whereDict['assignedWorker'] = searchItems
      if(self.checkTags.isChecked()):
        assget.whereDict['tags'] = searchItems
      if(self.checkAssetName.isChecked()):
        assget.whereDict['assName'] = searchItems
      if(self.checkAssetPath.isChecked()):
        assget.whereDict['path'] = searchItems

    self.hf.setTerminationEnabled(True)
    self.hf.run = assget.getAsses
    self.hf.start()

  #def setAssesData(self,asslist,assdict):
    #self.oldasses = asslist
    #self.oldassesdict = assdict
    #if(self.listFirstTime):
      #self.listAssets_thread()
      #self.listFirstTime = False
      #self.loader.hide()

    # self.listAssets_thread()
  def loaderShow(self):
    self.loader.show()


  def tableWidgetScrollEvent(self,event):
    self.resizeColumnsToContents()


  def selectedAsses(self):
    rowstask=[]
    rowsSelected = []
    rowsModel = self.tableWidget.selectionModel().selectedRows()
    debug.info("1 : "+ str(rowsModel))
    for idx in rowsModel:
      #debug.info(dir(idx.model()))
      rowsSelected.append(idx.row())
    debug.info(rowsSelected)
    for row in rowsSelected:
      try:
        doc = QtGui.QTextDocument()
        doc.setHtml(str(self.tableWidget.cellWidget(row,0).text()))
        text = doc.toPlainText()
        #debug.info("2 : "+ text)
        rowstask.append(str(text))
      except:
        debug.info(sys.exc_info())
    return(rowstask)


  def listAssets_thread(self,assesList=None,assesNames=None,assesColor=None,assdict=None,assModifiedTime=None):
    self.timerAssetsRefresh.stop()
    selAsses = self.selectedAsses()
    colNames = ['asset','assigned','created','reviewer','tags','modified time','versioning','review','progress','preview']
    #asses = asslist
    #assesdict = assdict
    self.tableWidget.clearContents()
    self.tableWidget.clear()


    self.tableWidget.setSortingEnabled(False)
    #self.tableWidget.resizeColumnsToContents()
    self.tableWidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
    self.previewItems = {}
    if(assesList):
      self.tableWidget.setColumnCount(len(colNames))
      self.tableWidget.setRowCount(len(assesList))
      for cn in range(0,len(colNames)):
        itemcn = QtGui.QTableWidgetItem()
        itemcn.setText(str(colNames[cn]))
        self.tableWidget.setHorizontalHeaderItem(cn, itemcn)
      for x in range(0,len(assesList)):
        assAbsPath = assdict[assesList[x]]
        try:
          item = ExtendedQLabel()
          item.setAlignment(QtCore.Qt.AlignVCenter)
          textAss = '<font color="'+ str(assesColor[assesList[x]].split(":")[0]).split("#")[1] +'">'+ (assesColor[assesList[x]].split(":")[0]).split("#")[0] +'</font>'
          if(len(assesColor[assesList[x]].split(":")) > 1):
            for fc in assesColor[assesList[x]].split(":")[1:]:
              textAss = textAss + ':' +'<font color="'+ fc.split("#")[1] +'">'+ fc.split("#")[0] +'</font>'
          item.setTextFormat(QtCore.Qt.RichText)
          item.setText(textAss)
          # item.setToolTip("CHECK OUT THE VERSION OPTION    };)\nEnable it by editing the asset")
          sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)

          item.setSizePolicy(sizePolicy)
          item.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
          item.clicked.connect(lambda item=item : self.versionCheck(item))

          self.tableWidget.setCellWidget(x,0,item)
        except:
          debug.info(str(sys.exc_info()))



        try:
          itemAss = QtGui.QTableWidgetItem()
          itemAss.setText(str(assesNames[assesList[x]]['assignedWorker']))
          self.tableWidget.setItem(x,1,itemAss)
        except:
          debug.info(str(sys.exc_info()))

        try:
          itemAss = QtGui.QTableWidgetItem()
          itemAss.setText(str(assesNames[assesList[x]]['createdUser']))
          self.tableWidget.setItem(x,2,itemAss)
        except:
          debug.info(str(sys.exc_info()))

        try:
          itemAss = QtGui.QTableWidgetItem()
          itemAss.setText(str(assesNames[assesList[x]]['reviewUser']))
          self.tableWidget.setItem(x,3,itemAss)
        except:
          debug.info(str(sys.exc_info()))

        try:
          itemTag = QtGui.QTableWidgetItem()
          itemTag.setText(str(assesNames[assesList[x]]['tags']))
          self.tableWidget.setItem(x,4,itemTag)
        except:
          debug.info(str(sys.exc_info()))


        try:
          itemModified = QtGui.QTableWidgetItem()
          itemModified.setText(str(assModifiedTime[assesList[x]]))
          self.tableWidget.setItem(x,5,itemModified)
        except:
          debug.info(str(sys.exc_info()))

        try:
          itemModified = QtGui.QTableWidgetItem()
          if(assesNames[assesList[x]]['versioning'] == 0):
            itemModified.setText("disabled")
          else:
            itemModified.setText("enabled : "+ str(assesNames[assesList[x]]['publishVersion']))
          self.tableWidget.setItem(x,6,itemModified)
        except:
          debug.info(str(sys.exc_info()))

        try:
          itemModified = QtGui.QTableWidgetItem()
          if(assesNames[assesList[x]]['reviewStatus'] == constantsPipe.reviewStatusNotDone):
            itemModified.setText("notDone")
          elif(assesNames[assesList[x]]['reviewStatus'] == constantsPipe.reviewStatusInProgress):
            itemModified.setText("inProgress : "+ str(assesNames[assesList[x]]['reviewVersion']))
          else:
            itemModified.setText("done : "+ str(assesNames[assesList[x]]['reviewVersion']))
          self.tableWidget.setItem(x,7,itemModified)
        except:
          debug.info(str(sys.exc_info()))


        try:
          itemModified = QtGui.QTableWidgetItem()
          if(assesNames[assesList[x]]['progressStatus'] == constantsPipe.assetProgressInProgress):
            itemModified.setText("inProgress")
          elif(assesNames[assesList[x]]['progressStatus'] == constantsPipe.assetProgressDone):
            itemModified.setText("done")
          self.tableWidget.setItem(x,8,itemModified)
        except:
          debug.info(str(sys.exc_info()))



        try:
          previewName = "preview"
          self.previewItems[x] = assAbsPath +"/"+ previewName +".png"
        except:
          debug.info(str(sys.exc_info()))

        if(assesList[x] in selAsses):
          self.tableWidget.selectRow(x)


    self.tableWidget.resizeColumnsToContents()
    self.form.statusBar().showMessage("total : "+ str(len(assesList)))
    #self.timerAssetsRefresh.stop()
    self.tableWidget.setSortingEnabled(True)
    self.tableWidget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
    self.previewCheck()
    self.loader.hide()




  def previewCheck(self):
    self.previewWidgets = []
    if(self.previewEnabled.isChecked()):
      if(self.previewItems):
        x = 0
        while(1):
          try:
            self.previewWidgets.append(ImageWidget(self.previewItems[x],64,self.tableWidget))
            self.previewWidgets[x].setToolTip("click on the image")
            self.tableWidget.setCellWidget(x,9,self.previewWidgets[x])
            self.previewWidgets[x].clicked.connect(lambda boool, x=x : self.imageWidgetClicked(x,self.previewWidgets[x],boool))
          except:
            debug.info(str(sys.exc_info()))
          x = x+1;
          if(x >= len(self.previewItems)):
            break;

  def imageWidgetClicked(self,*args):
    index = args[0]
    father = args[1]
    debug.info(args)
    import webbrowser
    webbrowser.open(father.imagePath)


  def versionCheck(self,*args):
    doc = QtGui.QTextDocument()
    doc.setHtml(args[0].text())
    text = doc.toPlainText()
    a = hgmod.hg(text)
    debug.info("in versionCheck : "+ str(os.getcwd()))
    #a._init()


  def rbhusPipeSeqSceCreate(self):
    p = QtCore.QProcess(parent=self.form)
    p.setStandardOutputFile(tempDir + os.sep +"rbhusPipeSeqSceCreate_"+ self.username +".log")
    p.setStandardErrorFile(tempDir + os.sep +"rbhusPipeSeqSceCreate_"+ self.username +".err")
    self.actionNew_seq_scn.setEnabled(False)
    p.start(sys.executable,rbhusPipeSeqSceCreateCmd.split())
    p.finished.connect(self.rbhusPipeSeqSceCreateEnable)


  def rbhusPipeSeqSceEdit(self):
    p = QtCore.QProcess(parent=self.form)
    p.setStandardOutputFile(tempDir + os.sep +"rbhusPipeSeqSceEdit_"+ self.username +".log")
    p.setStandardErrorFile(tempDir + os.sep +"rbhusPipeSeqSceEdit_"+ self.username +".err")
    self.actionEdit_seq_scn.setEnabled(False)
    p.start(sys.executable,rbhusPipeSeqSceEditCmd.split())
    p.finished.connect(self.rbhusPipeSeqSceEditEnable)




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


  def setTags(self):
    tags = utilsPipe.getTags(projName=os.environ['rp_proj_projName'])
    outTags = subprocess.Popen([sys.executable,selectCheckBoxCmd,"-i",",".join(tags),"-d",str(self.lineEditSearch.text()).rstrip().lstrip()],stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].rstrip().lstrip()
    if(outTags == ""):
      outTags = str(self.lineEditSearch.text()).rstrip().lstrip()
    self.lineEditSearch.setText(_fromUtf8(outTags))


  def setUsers(self):
    users = utilsPipe.getUsers()
    outUsers = subprocess.Popen([sys.executable,selectCheckBoxCmd,"-i",",".join(users),"-d",str(self.lineEditSearch.text()).rstrip().lstrip()],stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].rstrip().lstrip()
    if(outUsers == ""):
      outUsers = str(self.lineEditSearch.text()).rstrip().lstrip()
    self.lineEditSearch.setText(_fromUtf8(outUsers))


  def rbhusPipeSetProjDefault(self):
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
              debug.info(y +":"+ str(os.environ[y]))

          self.updateAll()
          self.saveFile = home.rstrip(os.sep) + os.sep +"rbhusSearch.default_"+ os.environ['rp_proj_projName']
          self.saveFileShortcut = home.rstrip(os.sep) + os.sep +"rbhusShort.default_"+ os.environ['rp_proj_projName']
          self.loadSearch()
          self.loadAssetShortcut()
          try:
            self.trayIcon.setToolTip(x)
          except:
            debug.error(sys.exc_info())
          break




  def rbhusPipeSetProject(self):
    projFile = open(home.rstrip(os.sep) + os.sep +"projSet.default","w")



    projNames = []
    projects = utilsPipe.getProjDetails(status="all")
    for x in projects:
      projNames.append(x['projName'])
    projN = subprocess.Popen([sys.executable,selectRadioBoxCmd,"-i",",".join(projNames)],stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].rstrip().lstrip()
    debug.info(projN)
    if(not projN):
      return(0)


    projFile.writelines(projN)
    projFile.close()

    utilsPipe.exportProj(projN)
    self.form.setWindowTitle(projN)
    self.actionSet_project.setText("set project ("+ projN +")")
    for x in os.environ.keys():
      if(x.find("rp_") >= 0):
        debug.info(x +":"+ str(os.environ[x]))

    self.updateAll()
    self.saveFile = home.rstrip(os.sep) + os.sep +"rbhusSearch.default_"+ os.environ['rp_proj_projName']
    self.saveFileShortcut = home.rstrip(os.sep) + os.sep +"rbhusShort.default_"+ os.environ['rp_proj_projName']
    self.loadSearch()
    self.loadAssetShortcut()
    try:
      self.trayIcon.setToolTip(projN)
    except:
      debug.error(sys.exc_info())



  def saveSearchItem(self):
    assetTypeSave = str(self.comboAssType.currentText())
    seqSave = str(self.comboSequence.currentText())
    scnSave = str(self.comboScene.currentText())
    stageSave = str(self.comboStageType.currentText())
    nodeSave = str(self.comboNodeType.currentText())
    fileTypeSave = str(self.comboFileType.currentText())
    isMineSave = str(self.radioMineAss.isChecked())
    isMineAssignedSave = str(self.mineAssignedAction.isChecked())
    isMineCreatedSave = str(self.mineCreatedAction.isChecked())
    isAllSave = str(self.radioAllAss.isChecked())
    isLinkedSave = str(self.checkLinkedProjects.isChecked())
    linkedProjSave = str(self.comboLinked.currentText())
    isTagsSave = str(self.checkTags.isChecked())
    isUsersSave = str(self.checkUsers.isChecked())
    searchBoxSave = str(self.lineEditSearch.text())
    isAssetNameSave = str(self.checkAssetName.isChecked())
    isAssetPathSave = str(self.checkAssetPath.isChecked())
    saveString = assetTypeSave +"###"+ \
                 seqSave +"###"+ \
                 scnSave +"###"+ \
                 stageSave +"###"+ \
                 nodeSave +"###"+ \
                 fileTypeSave +"###"+ \
                 isMineSave +"###"+ \
                 isMineAssignedSave +"###"+ \
                 isMineCreatedSave +"###"+ \
                 isAllSave +"###"+ \
                 isLinkedSave +"###"+ \
                 linkedProjSave +"###"+ \
                 isTagsSave +"###"+ \
                 isUsersSave +"###"+ \
                 searchBoxSave +"###"+ \
                 isAssetNameSave +"###"+ \
                 isAssetPathSave

    debug.info(saveString)
    if(not self.searchDict.has_key(saveString)):
      saveFileFd = open(self.saveFile,"w")
      self.searchDict[saveString] = 1
      searchSavedObj = saveSearch()
      searchSavedObj.searchPath = saveString
      searchSavedObj.searchName = "new fav"
      self.saveSearchArray.append(searchSavedObj)
      item = QtGui.QListWidgetItem()
      item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsEnabled)
      item.setText(searchSavedObj.searchName)
      self.listWidgetSearch.addItem(item)
      pickle.dump(self.saveSearchArray,saveFileFd)
      saveFileFd.flush()
      saveFileFd.close()

    #for x in range(0,self.listWidgetSearch.count()):
      #item = self.listWidgetSearch.item(x)
      #debug.info(":"+ str(item.text()))


  def searchItemChanged(self,item):
    debug.info(item.text())
    indexChanged = self.listWidgetSearch.indexFromItem(item).row()
    self.saveSearchArray[indexChanged].searchName = item.text()
    saveFileFd = open(self.saveFile,"w")
    pickle.dump(self.saveSearchArray,saveFileFd)
    saveFileFd.flush()
    saveFileFd.close()

  def searchItemActivate(self):
    indexChanged = self.listWidgetSearch.currentRow()
    debug.info(indexChanged)
    s = self.saveSearchArray[indexChanged].searchPath.split("###")
    debug.info(str(s) +":"+ str(len(s)))
    self.comboAssType.setEditText(s[0])
    self.comboSequence.setEditText(s[1])
    self.comboScene.setEditText(s[2])
    self.comboStageType.setEditText(s[3])
    self.comboNodeType.setEditText(s[4])
    self.comboFileType.setEditText(s[5])


    if(s[6] == "True"):
      self.radioMineAss.setChecked(True)
    else:
      self.radioMineAss.setChecked(False)

    if(s[7] == "True"):
      self.mineAssignedAction.setChecked(True)
    else:
      self.mineAssignedAction.setChecked(False)

    if(s[8] == "True"):
      self.mineCreatedAction.setChecked(True)
    else:
      self.mineCreatedAction.setChecked(False)

    if(s[9] == "True"):
      self.radioAllAss.setChecked(True)
    else:
      self.radioAllAss.setChecked(False)

    if(s[10] == "True"):
      self.checkLinkedProjects.setChecked(True)
    else:
      self.checkLinkedProjects.setChecked(False)

    self.comboLinked.setEditText(s[11])

    if(s[12] == "True"):
      self.checkTags.setChecked(True)
    else:
      self.checkTags.setChecked(False)

    if(s[13] == "True"):
      self.checkUsers.setChecked(True)
    else:
      self.checkUsers.setChecked(False)

    self.lineEditSearch.setText(s[14])

    if(s[15] == "True"):
      self.checkAssetName.setChecked(True)
    else:
      self.checkAssetName.setChecked(False)

    if(s[16] == "True"):
      self.checkAssetPath.setChecked(True)
    else:
      self.checkAssetPath.setChecked(False)

    self.listAssets()





  def loadSearch(self):
    debug.info(self.saveFile)
    self.listWidgetSearch.clear()
    self.saveSearchArray = []
    self.searchDict = {}
    if(os.path.exists(self.saveFile)):
      if(os.path.getsize(self.saveFile) > 0):
        saveFileFd = open(self.saveFile,"r")
        itemsForSaveSearch = pickle.load(saveFileFd)
        for x in range(0,len(itemsForSaveSearch)):
          debug.info("funcky : "+ str(itemsForSaveSearch[x]))
          item = QtGui.QListWidgetItem()
          item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsEnabled)
          item.setText(itemsForSaveSearch[x].searchName)
          self.listWidgetSearch.addItem(item)
          self.saveSearchArray.append(itemsForSaveSearch[x])
          self.searchDict[itemsForSaveSearch[x].searchPath] = 1

        saveFileFd.close()


  def deleteSearch(self):
    i = self.listWidgetSearch.currentRow()
    debug.info("current row selected :"+ str(i))
    poped = self.saveSearchArray.pop(i)
    del self.searchDict[poped.searchPath]
    saveFileFd = open(self.saveFile,"w")
    pickle.dump(self.saveSearchArray,saveFileFd)
    saveFileFd.flush()
    saveFileFd.close()
    self.loadSearch()


  def clearSearchFav(self):
    self.listWidgetSearch.clear()
    self.saveSearchArray = []
    self.searchDict = {}
    saveFileFd = open(self.saveFile,"w")
    pickle.dump(self.saveSearchArray,saveFileFd)


  def popUpSearchFav(self,pos):
    menu = QtGui.QMenu()
    filterSearchAction = menu.addAction("filter")
    deleteSearchAction = menu.addAction("delete")
    action = menu.exec_(self.listWidgetSearch.mapToGlobal(pos))

    if(action == filterSearchAction):
      self.searchItemActivate()

    if(action == deleteSearchAction):
      self.deleteSearch()


  def popUpAssetFav(self,pos):
    menu = QtGui.QMenu()
    openSearchAction = menu.addAction("open")
    deleteSearchAction = menu.addAction("delete")
    action = menu.exec_(self.listWidgetAssets.mapToGlobal(pos))

    if(action ==  openSearchAction):
      self.openFolderAss(favSearch = True)

    if(action == deleteSearchAction):
      self.deleteFavAss()



  def deleteFavAss(self):
    i = self.listWidgetAssets.currentRow()
    debug.info("current row selected :"+ str(i))
    poped = self.assSearchArray.pop(i)
    del self.assFavDict[poped]
    saveFileFd = open(self.saveFileShortcut,"w")
    pickle.dump(self.assSearchArray,saveFileFd)
    saveFileFd.flush()
    saveFileFd.close()
    self.loadAssetShortcut()



  def assetFavSave(self):
    asses = self.selectedAsses()
    if(asses):
      for x in range(0,len(asses)):
        debug.info(asses[x])
        if(not self.assFavDict.has_key(str(asses[x]))):
          self.assFavDict[str(asses[x])] = 1
          self.assSearchArray.append(str(asses[x]))
          assSaveFileFd = open(self.saveFileShortcut,"w")
          pickle.dump(self.assSearchArray,assSaveFileFd)
          assSaveFileFd.flush()
          assSaveFileFd.close()
          item = QtGui.QListWidgetItem()
          item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsEnabled)
          item.setText(str(asses[x]))
          self.listWidgetAssets.addItem(item)


  def loadAssetShortcut(self):
    self.listWidgetAssets.clear()
    self.assFavDict = {}
    self.assSearchArray = []
    if(os.path.exists(self.saveFileShortcut)):
      if(os.path.getsize(self.saveFileShortcut) > 0):
        assSaveFileFd = open(self.saveFileShortcut,"r")
        self.assSearchArray = pickle.load(assSaveFileFd)
        assSaveFileFd.close()
        for x in range(0,len(self.assSearchArray)):
          self.assFavDict[self.assSearchArray[x]] = 1
          item = QtGui.QListWidgetItem()
          item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsEnabled)
          item.setText(str(self.assSearchArray[x]))
          self.listWidgetAssets.addItem(item)









  def rbhusPipeProjCreateEnable(self,exitStatus):
    self.actionNew_project.setEnabled(True)
    self.updateAll()



  def updateAll(self):
    self.setLinkedProj()
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

  def rbhusPipeSeqSceEditEnable(self,exitStatus):
    self.actionEdit_seq_scn.setEnabled(True)
    # self.updateAll()



  def closeEvent(self,event):
    event.ignore()
    QtGui.QMessageBox.about(self.form,"QUITING?","Minimizing to Tray .\nPlease quit from the tray icon if you really want to quit!")
    self.form.setVisible(False)

  def hideEvent(self,event):

    # self.form.setVisible(False)
    self.form.showMinimized()
    # self.form.setWindowFlags(self.wFlag & QtCore.Qt.Tool)
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
