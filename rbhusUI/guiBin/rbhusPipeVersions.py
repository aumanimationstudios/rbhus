#!/usr/bin/python
from PyQt4 import QtCore, QtGui
import glob
import os
import sys
import time
import subprocess
import argparse
import tempfile
import psutil
if(sys.platform.find("linux") >=0 ):
  import fcntl


dirSelf = os.path.dirname(os.path.realpath(__file__))
print(dirSelf)
sys.path.append(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep) + os.sep + "lib")


scb = "selectCheckBox.py"
srb = "selectRadioBox.py"
selectCheckBoxCmd = dirSelf.rstrip(os.sep) + os.sep + scb
selectRadioBoxCmd = dirSelf.rstrip(os.sep) + os.sep + srb





import rbhusPipeVersionsMod
print(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")
sys.path.append(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")
import dbPipe
import constantsPipe
import authPipe
import utilsPipe
import hgmod
import debug






parser = argparse.ArgumentParser()
parser.add_argument("-i","--id",dest='assId',help='asset id')
parser.add_argument("-p","--path",dest='assPath',help='asset path')
args = parser.parse_args()

app_lock_file = os.path.join(tempfile.gettempdir(),str(args.assPath).replace(":","_"))
preview_files = ["preview.png"]

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
      assetDetails = utilsPipe.getAssDetails(assPath=self.versionPath)
      versionsHg = hgmod.hg(self.versionPath)
      versionsHg.initialize()
      versionsHg.initializeLocal()
      # print("EEEEEE :"+ str(versionsHg._log()))
      self.dataReady.emit(versionsHg,assetDetails)
    else:
      self.dataNotAvailable.emit()


try:
  _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
  _fromUtf8 = lambda s: s



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

    #self.versionsHg = hgmod.hg(args.assPath)
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
    reviewAction = menu.addAction("send for review")
    publishAction = menu.addAction("publish")
    reviseAction = menu.addAction("revise")
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
    assdets = utilsPipe.getAssDetails(assPath=self.versionsHg.pipepath)
    runCmd = utilsPipe.openAssetCmd(assdets,verpath)
    if(runCmd):
      runCmd = runCmd.rstrip().lstrip()
      subprocess.Popen(runCmd,shell=True)
    else:
      import webbrowser
      webbrowser.open(verpath)
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
      self.versionsHg._archive(sv)
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
  
  def noData(self):
    sys.exit(0)


  def messageBoxWarn(self, hard=False):
    msgbox = QtGui.QMessageBox()
    msgbox.setText(unicode("NOT COMMITING ! \nAsset is not in your name!!!\nPLEASE CHECK"))
    msgbox.setIconPixmap(QtGui.QPixmap(_fromUtf8(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/danger_128.png")))
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

    self.versionsHg._addremove()
    self.versionsHg._pull()
    self.versionsHg._merge()
    self.versionsHg._commit()
    self.versionsHg._push()
    os.chdir(self.versionsHg.absPipePath)
    self.versionsHg._purge()
    self.versionsHg._update()
    os.chdir(self.versionsHg.localPath)
    self.hglog()
    self.centralwidget.setCursor(QtCore.Qt.ArrowCursor)
    
    
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


  
  
  def openfolder(self):
    if(os.path.exists(self.versionsHg.localPath)):
      fila = QtGui.QFileDialog.getOpenFileNames(directory=self.versionsHg.localPath)
      print(fila)
      if(fila):
        print(str(fila[0]))
        filename = str(fila[0])
        assdets = utilsPipe.getAssDetails(assPath=self.versionsHg.pipepath)
        runCmd = utilsPipe.openAssetCmd(assdets,filename)
        if(runCmd):
          runCmd = runCmd.rstrip().lstrip()
          subprocess.Popen(runCmd,shell=True)
        else:
          import webbrowser
          webbrowser.open(filename)
    
    



if __name__ == "__main__":
  app = QtGui.QApplication(sys.argv)
  Form = QtGui.QMainWindow()
  ui = Ui_Form()
  ui.setupUi(Form)
  Form.show()
  sys.exit(app.exec_())
    