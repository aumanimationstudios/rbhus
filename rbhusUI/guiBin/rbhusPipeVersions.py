#!/usr/bin/python
from PyQt4 import QtCore, QtGui, uic
import glob
import os
import sys
import time
import subprocess
import argparse
import tempfile
import psutil
import tempfile
if(sys.platform.find("linux") >=0 ):
  import fcntl


tempDir = tempfile.gettempdir()

dirSelf = os.path.dirname(os.path.realpath(__file__))
print(dirSelf)
sys.path.append(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep) + os.sep + "lib")

base_dir = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-3])
ui_dir = os.path.join(base_dir,"rbhusUI","lib")
relatedAsset_ui = os.path.join(ui_dir,"rbhusPipeVersionsMod_relatedAsset.ui")
pop_ui = os.path.join(ui_dir,"rbhusPipeVersionsMod_popAsset.ui")

scb = "selectCheckBox.py"
srb = "selectRadioBox.py"
selectCheckBoxCmd = dirSelf.rstrip(os.sep) + os.sep + scb
selectRadioBoxCmd = dirSelf.rstrip(os.sep) + os.sep + srb
assFoldsCmd = os.path.join(dirSelf,"qt5-treeview.py")

try:
  username = os.environ['rbhusPipe_acl_user'].rstrip().lstrip()
except:
  pass



import rbhusPipeVersionsMod
print(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")
sys.path.append(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")
import dbPipe
import constantsPipe
import authPipe
import utilsPipe
import hgmod
import debug
import pyperclip




try:
  _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
  _fromUtf8 = lambda s: s


parser = argparse.ArgumentParser()
parser.add_argument("-i","--id",dest='assId',help='asset id')
parser.add_argument("-p","--path",dest='assPath',help='asset path')
args = parser.parse_args()

app_lock_file = os.path.join(tempfile.gettempdir(),str(args.assPath).replace(":","_"))
preview_files = ["preview.png"]

class ImagePlayer(QtGui.QWidget):
  def __init__(self, filename, parent):
    # Create the layout
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


    main_layout = QtGui.QVBoxLayout()
    main_layout.addWidget(self.movie_screen)
    self.setLayout(main_layout)
    self.movie.start()


  def resizeEvent(self, event):
    self.move((self.parent.geometry().width()-100)/2,(self.parent.geometry().height()-100)/2)

  def showEvent(self,event):
    #self.show()
    #self.movie.setEnabled(True)
    self.movie.start()


  def hideEvent(self,event):
    #self.hide()
    #self.movie.setEnabled(False)
    self.movie.stop()




class workerInitialize(QtCore.QObject):
  dataPending = QtCore.pyqtSignal()
  dataReady = QtCore.pyqtSignal(object,dict)
  dataNotAvailable = QtCore.pyqtSignal()

  def __init__(self):
    super(workerInitialize, self).__init__()
    self.versionPath = None


  def initialize(self):
    self.dataPending.emit()
    if(self.versionPath):
      # print("EEEEEE :"+ str(versionsHg._log()))
      assetDetails = utilsPipe.getAssDetails(assPath=self.versionPath)
      versionsHg = hgmod.hg(self.versionPath)
      versionsHg.initialize()
      versionsHg.initializeLocal()
      self.dataReady.emit(versionsHg,assetDetails)
    else:
      self.dataNotAvailable.emit()





def app_lock():
  if(os.path.exists(app_lock_file)):
    f = open(app_lock_file,"r")
    pid = f.read().strip()
    f.close()
    debug.info(pid)
    try:
      p = psutil.Process(int(pid))
      if (os.path.abspath(p.cmdline()[1]) == os.path.abspath(__file__)):
        debug.warning("already an instance of the app is running.")
        debug.warning("delete the file {0}".format(app_lock_file))
        QtCore.QCoreApplication.instance().quit()
        os._exit(1)
      else:
        raise Exception("seems like a different process has the same pid")
    except:
      debug.warn(sys.exc_info())
      f = open(app_lock_file,"w")
      if(sys.platform.find("linux") >= 0):
        try:
          fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except:
          debug.error(sys.exc_info())
          QtCore.QCoreApplication.instance().quit()
          os._exit(1)
      f.write(unicode(os.getpid()))
      f.flush()
      if (sys.platform.find("linux") >= 0):
        fcntl.flock(f, fcntl.LOCK_UN)
      f.close()
  else:
    f = open(app_lock_file,"w")
    if (sys.platform.find("linux") >= 0):
      try:
        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
      except:
        debug.error(sys.exc_info())
        QtCore.QCoreApplication.instance().quit()
        os._exit(1)
    f.write(unicode(os.getpid()))
    f.flush()
    if (sys.platform.find("linux") >= 0):
      fcntl.flock(f, fcntl.LOCK_UN)
    f.close()


class Ui_Form(rbhusPipeVersionsMod.Ui_MainWindow):
  def setupUi(self, Form):
    app_lock()

    self.form = Form
    rbhusPipeVersionsMod.Ui_MainWindow.setupUi(self,Form)
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(_fromUtf8(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/rbhusPipe.svg")), QtGui.QIcon.Normal, QtGui.QIcon.On)
    Form.setWindowIcon(icon)
    Form.setWindowTitle(args.assPath)
    self.assetDetails = None

    self.centralwidget.resizeEvent  = self.resizeEvent
    # self.tableVersions.resizeEvent = self.resizeEvent
    self.splitter.setStretchFactor(1, 100)
    self.splitter.setStretchFactor(0, 100)

    self.initThread = None

    self.loadingGif = dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/loading.gif"

    self.loader = ImagePlayer(self.loadingGif,parent=self.tableVersions)
    self.loader.hide()

    self.pushWork.clicked.connect(self.openfolder)
    self.pushCommit.clicked.connect(self.commit)
    self.pushReInit.clicked.connect(self.reInit)


    self.tableVersions.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    self.tableVersions.customContextMenuRequested.connect(self.popupPublish)


    self.versionsHg = None
    self.relatedAssetWidgets = {}
    self.popAssetWidgets = {}

    self.splitter.setSizes((1000, 1000))

    #self.versionsHg = hgmod.hg(args.assPath)
    self.toolButton.setMenu(self.popupToolButton())
    self.toolButton.triggered.connect(self.popupToolButtonTriggered)
    self.initialize()

    #self.hglog()


  def updateAssDetails(self):
    if(args.assId):
      self.assetDetails = utilsPipe.getAssDetails(assId=args.assId)
    if(args.assPath):
      self.assetDetails = utilsPipe.getAssDetails(assPath=args.assPath)


  def popupPublish(self, pos):
    menu = QtGui.QMenu()
    #openFileAction = menu.addAction("open file")
    punkaction1 = menu.addAction("-")
    publishAction = menu.addAction("publish")
    reviseAction = menu.addAction("revise")
    reviewAction = menu.addAction("send for review")
    exportAction = menu.addAction("export")
    openVersionAction = menu.addAction("open version")
    action = menu.exec_(self.tableVersions.mapToGlobal(pos))
    #if(action == openFileAction):
    #self.openFileAss()
    if(action == publishAction):
      self.publishVersion()
    if(action == reviseAction):
      self.reviseVersion()
    if(action == exportAction):
      self.exportVersion()
    if(action == openVersionAction):
      self.openVersion()
    if(action == reviewAction):
      self.reviewVersion()

  def popupToolButton(self):
    menu = QtGui.QMenu()
    copyVersionPath = menu.addAction("version path")
    copyPublishPath = menu.addAction("publish path")
    copyAssetPath = menu.addAction("asset path")
    copyPath = menu.addAction("path")
    return(menu)

  def popupToolButtonTriggered(self,action):
    if(action.text() == "version path"):
      versionPath = self.versionsHg.localPath

      pyperclip.copy(versionPath)
    if(action.text() == "publish path"):
      publishPath = os.path.join(self.versionsHg.absPipePath, "publish")
      pyperclip.copy(publishPath)
    if(action.text() == "path"):
      pyperclip.copy(self.versionsHg.absPipePath)
    if(action.text() == "asset path"):
      pyperclip.copy(self.versionsHg.pipepath)



  def reInit(self):
    self.versionsHg.reInitLocal()
    self.hglog()

  def reviewVersion(self):
    self.centralwidget.setCursor(QtCore.Qt.WaitCursor)
    selvers = self.selectedVersions()
    if(selvers):
      sv = selvers[-1]
      self.versionsHg._review(sv)
    self.hglog()
    self.centralwidget.setCursor(QtCore.Qt.ArrowCursor)


  def openVersion(self):
    self.centralwidget.setCursor(QtCore.Qt.WaitCursor)
    selvers = self.selectedVersions()
    if(selvers):
      sv = selvers[-1]
      verpath = self.versionsHg.getVersionPath(sv)
    # assdets = utilsPipe.getAssDetails(assPath=self.versionsHg.pipepath)
    # runCmd = utilsPipe.openAssetCmd(assdets,verpath)
    # if(runCmd):
    #   runCmd = runCmd.rstrip().lstrip()
    #   subprocess.Popen(runCmd,shell=True)
    # else:
    self.openfolder(verpath)
    self.centralwidget.setCursor(QtCore.Qt.ArrowCursor)




  def exportVersion(self):
    self.centralwidget.setCursor(QtCore.Qt.WaitCursor)
    selvers = self.selectedVersions()
    if(selvers):
      sv = selvers[-1]
      self.versionsHg._archiveVersion(sv)
    self.hglog()
    self.centralwidget.setCursor(QtCore.Qt.ArrowCursor)

  def publishVersion(self):
    self.centralwidget.setCursor(QtCore.Qt.WaitCursor)
    selvers = self.selectedVersions()
    if(selvers):
      sv = selvers[-1]
      retValue = self.versionsHg._archive(sv)
      if(retValue != 111):
        self.popRelated()


    self.hglog()
    self.centralwidget.setCursor(QtCore.Qt.ArrowCursor)





  def reviseVersion(self):
    self.centralwidget.setCursor(QtCore.Qt.WaitCursor)
    selvers = self.selectedVersions()
    if(selvers):
      sv = selvers[-1]
      self.versionsHg._revert(sv)
    self.centralwidget.setCursor(QtCore.Qt.ArrowCursor)

  def selectedVersions(self):
    rowstask=[]
    rowsSelected = []
    rowsModel = self.tableVersions.selectionModel().selectedRows()
    for idx in rowsModel:
      rowsSelected.append(idx)
    for rows in rowsSelected:
      rowstask.append(str(self.tableVersions.item(rows.row(), 0).text()).lstrip("0"))
    return(rowstask)


  def hglog(self):
    self.centralwidget.setCursor(QtCore.Qt.WaitCursor)
    self.updateAssDetails()
    self.tableVersions.clearContents()
    self.tableVersions.setSortingEnabled(False)
    self.tableVersions.resizeColumnsToContents()
    tem = self.versionsHg._log()
    colorSize = QtCore.QSize()
    colorSize.setWidth(10)
    colorSize.setHeight(10)
    if(tem):
      self.tableVersions.setColumnCount(len(tem[0]) + 2)
      self.tableVersions.setRowCount(len(tem))
      indrow = 0
      for te in tem:
        indcol = 0
        for t in te:
          item = QtGui.QTableWidgetItem()
          brush = QtGui.QBrush()
          self.tableVersions.setItem(indrow, indcol, item)
          if(indcol == 4):
            self.tableVersions.item(indrow, indcol).setText(str(time.ctime(float(t.split("-")[0]))))
          elif(indcol == 0):
            if(str(t) == str(self.assetDetails['publishVersion'])):
              item1 = QtGui.QTableWidgetItem()
              brush1 = QtGui.QBrush()
              self.tableVersions.setItem(indrow, indcol+1, item1)
              brush1.setColor(QtGui.QColor(0, 200, 0))
              brush1.setStyle(QtCore.Qt.SolidPattern)
              self.tableVersions.item(indrow, indcol+1).setBackground(brush1)
            if(str(t) == str(self.assetDetails['reviewVersion'])):
              item2 = QtGui.QTableWidgetItem()
              brush2 = QtGui.QBrush()
              self.tableVersions.setItem(indrow, indcol + 2, item2)
              brush2.setColor(QtGui.QColor(150, 150, 200))
              brush2.setStyle(QtCore.Qt.SolidPattern)
              self.tableVersions.item(indrow, indcol+2).setBackground(brush2)
            self.tableVersions.item(indrow, indcol).setText(str(t).zfill(4))
            indcol = indcol + 2
          else:
            self.tableVersions.item(indrow, indcol).setText(str(t))
          indcol = indcol + 1

        indrow = indrow + 1
    self.tableVersions.setSortingEnabled(True)
    self.tableVersions.resizeColumnsToContents()
    self.centralwidget.setCursor(QtCore.Qt.ArrowCursor)


  def push(self):
    pass

  def resizeEvent(self,event):
    self.loader.resizeEvent(event)
    self.tableVersions.resizeColumnsToContents()


  def initialize(self):
    if(self.initThread):
      if(self.initThread.isRunning()):
        return(0)
    self.initThread = QtCore.QThread(parent=self.tableVersions)

    initVers = workerInitialize()
    initVers.dataPending.connect(self.loader.show)
    initVers.dataReady.connect(self.iniLog)
    initVers.dataNotAvailable.connect(self.noData)

    initVers.versionPath = args.assPath

    self.initThread.setTerminationEnabled(True)
    self.initThread.run = initVers.initialize
    self.initThread.start()

    #self.versionsHg.initialize()
    #self.versionsHg.initializeLocal()
    #self.hglog()

  def iniLog(self,versionHgReturned,assdets):
    self.assetDetails = assdets
    self.versionsHg = versionHgReturned
    self.loader.hide()
    self.hglog()
    self.updateRelatedAssets()
    self.updatePopAssets()


  def updateRelatedAssets(self):
    assGroups = utilsPipe.getGroupedAssets(self.assetDetails['path'])
    selectedForAutoCommit = utilsPipe.getGroupedForAutoCommit(self.assetDetails['path'])
    debug.info(selectedForAutoCommit)
    self.relatedAssetWidgets.clear()
    self.listWidgetAutoCommit.clear()
    if(assGroups):
      for x in assGroups:
        debug.info(x)
        assDets = utilsPipe.getAssDetails(assPath=x)
        assLog = hgmod.hg(x)._log()
        relatedAssetWidget = uic.loadUi(relatedAsset_ui)
        self.relatedAssetWidgets[x] = relatedAssetWidget
        if(assLog):
          relatedAssetWidget.labelVersion.setText(str(assLog[0][0]).zfill(4))
          relatedAssetWidget.labelDate.setText(str(time.ctime(float(assLog[0][2].split("-")[0]))))
        assColored = utilsPipe.assPathColorCoded(assDets)
        if(selectedForAutoCommit):
          if(x in selectedForAutoCommit):
            relatedAssetWidget.checkBox.setCheckState(QtCore.Qt.Checked)
        relatedAssetWidget.checkBox.clicked.connect(lambda clicked,assDets=assDets,checkBox=relatedAssetWidget.checkBox : self.updateAutoCommitFile(assDets,checkBox))
        textAssArr = []
        for fc in assColored.split(":")[1:]:
          textAssArr.append('<font color="' + fc.split("#")[1] + '">' + fc.split("#")[0] + '</font>')
        richAss = " " + "<b><i> : </i></b>".join(textAssArr)
        relatedAssetWidget.label.setText(richAss)
        item = QtGui.QListWidgetItem()
        item.assPath = x
        self.listWidgetAutoCommit.addItem(item)
        self.listWidgetAutoCommit.setItemWidget(item, relatedAssetWidget)
        item.setSizeHint(relatedAssetWidget.sizeHint())

  def updatePopAssets(self):
    assGroups = utilsPipe.getGroupedAssets(self.assetDetails['path'])
    selectedForPop = utilsPipe.getGroupedForPoP(self.assetDetails['path'])
    debug.info(selectedForPop)
    self.popAssetWidgets.clear()
    self.listWidgetPoP.clear()
    if(assGroups):
      for x in assGroups:
        debug.info(x)
        assDets = utilsPipe.getAssDetails(assPath=x)
        popAssetWidget = uic.loadUi(pop_ui)
        self.popAssetWidgets[x] = popAssetWidget
        assColored = utilsPipe.assPathColorCoded(assDets)
        if(selectedForPop):
          if(x in selectedForPop):
            popAssetWidget.checkBox.setCheckState(QtCore.Qt.Checked)
        popAssetWidget.checkBox.clicked.connect(lambda clicked,assDets=assDets,checkBox=popAssetWidget.checkBox : self.updatePopFile(assDets,checkBox))
        textAssArr = []
        for fc in assColored.split(":")[1:]:
          textAssArr.append('<font color="' + fc.split("#")[1] + '">' + fc.split("#")[0] + '</font>')
        richAss = " " + "<b><i> : </i></b>".join(textAssArr)
        popAssetWidget.label.setText(richAss)
        item = QtGui.QListWidgetItem()
        item.assPath = x
        self.listWidgetPoP.addItem(item)
        self.listWidgetPoP.setItemWidget(item, popAssetWidget)
        item.setSizeHint(popAssetWidget.sizeHint())


  def updateAutoCommitFile(self,assDets,checkBox):
    add = False
    if(checkBox.checkState() == QtCore.Qt.Checked):
      add = True
    utilsPipe.setGroupedForAutoCommit(self.assetDetails['path'],assDets['path'],add=add)


  def updatePopFile(self,assDets,checkBox):
    add = False
    if(checkBox.checkState() == QtCore.Qt.Checked):
      add = True
    utilsPipe.setGroupedForPoP(self.assetDetails['path'],assDets['path'],add=add)


  def noData(self):
    sys.exit(0)


  def messageBoxWarn(self, hard=False, assPath=None):
    msgbox = QtGui.QMessageBox()
    if(assPath):
      msgbox.setText(unicode(assPath +"\nNOT COMMITING !Asset not assigned to you!!!"))
    else:
      msgbox.setText(unicode("NOT COMMITING !\nAsset not assigned to you!!!"))
    msgbox.setIconPixmap(QtGui.QPixmap(_fromUtf8(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/poop.png")))
    #noBut = QtGui.QPushButton("cancel")
    #yesBut = QtGui.QPushButton("yes")
    noBut = msgbox.addButton("cancel",QtGui.QMessageBox.NoRole)
    msgbox.setDefaultButton(noBut)
    msgbox.exec_()


  def commit(self):
    self.centralwidget.setCursor(QtCore.Qt.WaitCursor)
    self.convertPreview()
    perm = self.versionsHg._add()
    debug.info("returned : "+ str(perm))
    if(perm == 111):
      self.messageBoxWarn()
      return(0)

    self.versionsHg._addremove()
    self.versionsHg._pull()
    self.versionsHg._merge()
    commit_status, versionCommited = self.versionsHg._commit()
    if(not commit_status):
      debug.info("NOTHING TO COMMIT")
      self.hglog()
      self.commitRelated()
      self.centralwidget.setCursor(QtCore.Qt.ArrowCursor)
      return(0)
    self.versionsHg._push()
    os.chdir(self.versionsHg.absPipePath)
    self.versionsHg._purge()
    self.versionsHg._update(rev=versionCommited)
    os.chdir(self.versionsHg.localPath)
    self.commitRelated()
    self.hglog()
    utilsPipe.updateProjModifies(self.assetDetails['projName'], "commit:"+ str(self.assetDetails['path']), isModified=True)
    self.centralwidget.setCursor(QtCore.Qt.ArrowCursor)

  def commitRelated(self):
    selectedForAutoCommit = utilsPipe.getGroupedForAutoCommit(self.assetDetails['path'])
    if (selectedForAutoCommit):
      for x in selectedForAutoCommit:
        debug.info("commiting : " + x)
        xver = hgmod.hg(x)
        utilsPipe.updateAssModifies(xver.assDets['assetId'],"commit_auto:start")
        retValue, versionNumber = xver.commitAbsPath(commitmsg="from autoCommit")
        debug.info(versionNumber)
        if (retValue == 111):
          self.messageBoxWarn(assPath=x)
          utilsPipe.updateAssModifies(xver.assDets['assetId'],"commit_auto:end:fail:permission_denied")
        else:
          assLog = xver._log()
          if(versionNumber):
            self.relatedAssetWidgets[x].labelVersion.setText(str(versionNumber).zfill(4))
          self.relatedAssetWidgets[x].labelDate.setText(str(time.ctime(float(assLog[0][2].split("-")[0]))))
          utilsPipe.updateAssModifies(xver.assDets['assetId'],"commit_auto:end:success")



  def popRelated(self):
    selectedForPop = utilsPipe.getGroupedForPoP(self.assetDetails['path'])
    if (selectedForPop):
      for x in selectedForPop:
        debug.info("PoPing : " + x)
        retValue = utilsPipe.importAssets(args.assPath.split(":")[0],args.assPath,x,force=True,pop=True)
        debug.info(retValue)
        if (retValue == 111):
          self.messageBoxWarn(assPath=x)
        else:
          self.popAssetWidgets[x].labelStatus.setText("done")


  def convertPreview(self):
    files = glob.glob(os.path.join(self.versionsHg.localPath,"*"))
    for x in files:
      debug.info(x)
      if(x.split(os.sep)[-1] in preview_files):
        low_png = x.replace(".png","_low.png")
        if(os.path.exists(low_png)):
          debug.info("preview_low.png exists . deleting it now")
          try:
            os.remove(low_png)
          except:
            debug.error(sys.exc_info())
        cmd = "/usr/bin/convert -resize 128x128 {0} {1}".format(x,low_png)
        debug.info(cmd)
        try:
          p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
          debug.info(p.communicate())
        except:
          debug.info(sys.exc_info())




  def openfolder(self,path=None):
    if(not path):
      path = self.versionsHg.localPath
    if(os.path.exists(path)):
      p = QtCore.QProcess(parent=self.centralwidget)
      p.setStandardOutputFile(tempDir + os.sep + "rbhusAssFoldsVersion_" + username + ".log")
      p.setStandardErrorFile(tempDir + os.sep + "rbhusAssFoldsVersion_" + username + ".err")
      p.start(sys.executable, [assFoldsCmd, "-c", "--asset", self.assetDetails['path'], "--path", path])



    # if(os.path.exists(self.versionsHg.localPath)):
    #   fila = QtGui.QFileDialog.getOpenFileNames(directory=self.versionsHg.localPath)
    #   print(fila)
    #   if(fila):
    #     print(str(fila[0]))
    #     filename = str(fila[0])
    #     assdets = utilsPipe.getAssDetails(assPath=self.versionsHg.pipepath)
    #     runCmd = utilsPipe.openAssetCmd(assdets,filename)
    #     if(runCmd):
    #       utilsPipe.updateProjModifies(self.assetDetails['projName'], "open_version_ui:"+ self.assetDetails['path'],isAccessed=True)
    #       runCmd = runCmd.rstrip().lstrip()
    #       subprocess.Popen(runCmd,shell=True)
    #     else:
    #       utilsPipe.updateProjModifies(self.assetDetails['projName'], "open_version_ui:"+ self.assetDetails['path'],isAccessed=True)
    #       import webbrowser
    #       webbrowser.open(filename)
    #
    



if __name__ == "__main__":
  app = QtGui.QApplication(sys.argv)
  Form = QtGui.QMainWindow()
  ui = Ui_Form()
  ui.setupUi(Form)
  Form.show()
  sys.exit(app.exec_())
    