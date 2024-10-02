#!/usr/bin/env python3
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"




import argparse
import glob
import multiprocessing
import os
import subprocess
import sys
import time
import uuid
try:
  import arrow
except:
  pass
import setproctitle
import simplejson
import zmq
import re
import shutil
import hashlib
import tempfile

# sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-1]))
progPath = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2])
rbhusPath = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-3])


busyIconGif = os.path.join(rbhusPath,"etc","icons","rbhusIconTray-BUSY.gif")

sys.path.append(rbhusPath)
import rbhus.debug
import rbhus.constantsPipe
import rbhus.utilsPipe
import rbhus.dfl
import rbhus.pyperclip
rbhus.debug.info("TREEVIEW PATH : "+ str(busyIconGif))
main_ui_file = os.path.join(rbhusPath, "rbhusUI", "lib", "qt5", "folderManager", "main01.ui")
mediaThumbz_ui_file = os.path.join(rbhusPath, "rbhusUI", "lib", "qt5", "folderManager", "mediaThumbz.ui")
rbhus.debug.info(main_ui_file)


from PyQt5.QtWidgets import QApplication, QFileSystemModel, QListWidgetItem
from PyQt5 import QtCore, uic, QtGui, QtWidgets
from PyQt5.QtCore import QSortFilterProxyModel



parser = argparse.ArgumentParser(description="Use the comand to open a sandboxed UI for folders in an Asset")
parser.add_argument("-a","--asset",dest="asset",help="colon separated Asset path")
parser.add_argument("-p","--path",dest="path",help="Absolute path of the asset on disk")
parser.add_argument("-c","--close",dest="close",action="store_true",help="Close the app after opening a file")
args = parser.parse_args()



app = None
assPath = args.asset
assDets = rbhus.utilsPipe.getAssDetails(assPath=assPath)
ROOTDIR_ASSET = rbhus.utilsPipe.getAbsPath(assPath)
if(args.path):
  ROOTDIR = args.path
else:
  ROOTDIR = ROOTDIR_ASSET


testhash = hashlib.sha1(assPath.encode('utf-8') + ROOTDIR.encode('utf-8'))
lockFile = os.path.join(tempfile.gettempdir(),rbhus.utilsPipe.username, str(testhash.hexdigest()))
rbhus.debug.info("HASH: "+ lockFile)







CUR_ROOTDIR_POINTER = os.path.join(ROOTDIR,"-")
COMPOUND_PATHS = rbhus.utilsPipe.getCompoundPaths(assPath)
CUR_DIR_SELECTED = None
print(COMPOUND_PATHS)

fileDetsDict = {}
# fileIconThreadRunning = None
fileIconThreads = []
fileThumbzWidget = {}
fileThumbzItems = {}

context = zmq.Context()

serverIPC = str(uuid.uuid4())
workerIPC = str(uuid.uuid4())


isCopying = []
isQuiting = False

thumbsDbDir = os.path.join("/crap/LOCAL.crap/",rbhus.utilsPipe.username, ".thumbz.db",assDets['assetId'])

filterList = []
currView = "ICON"

def jsonWrite(jFile, jData):
  try:
    fJsonFD = open(jFile, "w")
    simplejson.dump(jData, fJsonFD)
    fJsonFD.flush()
    fJsonFD.close()
    return (1)
  except:
    return (0)


def jsonRead(jFile):
  try:
    fJsonFD = open(jFile, "r")
    fThumbzDetails = simplejson.load(fJsonFD)
    fJsonFD.close()
    return (fThumbzDetails)
  except:
    return (0)


class IconProvider(QtWidgets.QFileIconProvider):
  # def __init__(self,*arg):
  #   super(IconProvider, self).__init__(*arg)
  #   rbhus.debug.info("Inside icon provider")
    # self.setOptions(QtWidgets.QFileIconProvider.DontUseCustomDirectoryIcons)

  def icon(self, fileInfo):
    filePath = fileInfo.absoluteFilePath()
    pathSelected = os.path.relpath(fileInfo.absolutePath(),ROOTDIR)
    fName = os.path.basename(filePath)
    fThumbz = os.path.join(thumbsDbDir, pathSelected, fName + ".png")


    if(os.path.exists(fThumbz)):
      pixmap = QtGui.QPixmap(fThumbz)
      return QtGui.QIcon(pixmap.scaled(64, 64, QtCore.Qt.KeepAspectRatio))
    else:
      return QtWidgets.QFileIconProvider.icon(self, fileInfo)


class DateItemDelegate(QtWidgets.QStyledItemDelegate):
  def __init__(self,parent=None):
    super(DateItemDelegate, self).__init__(parent=parent)

  def displayText(self,value,locale):
    try:
      arrowDate = arrow.get(str(value),'M/D/YY h:m A')
      return arrowDate.format('MMM DD, ddd, YYYY  hh:mm A')
    except:
      pass
    return super(DateItemDelegate, self).displayText(value,locale)

class syncThread(QtCore.QThread):
  syncing = QtCore.pyqtSignal(str,str)
  syncingDone = QtCore.pyqtSignal(str,str)

  def __init__(self,parent,fileParticles):
    super(syncThread, self).__init__(parent)
    self.fileParticles = fileParticles
    # rbhus.debug.info("SYNC THREAD :"+ str(fileParticles))

  def run(self):
    for fileParticle in self.fileParticles.keys():
      self.syncing.emit(fileParticle,self.fileParticles[fileParticle])
      # rbhus.debug.info("SYNC THREAD :"+ self.fileParticles[fileParticle])
      if(os.path.isdir(fileParticle)):
        status = os.system("rsync -av \""+ fileParticle + "/\" \""+ self.fileParticles[fileParticle] + "\"")
        rbhus.debug.info(status)
      else:
        status = os.system("rsync -av \""+ fileParticle + "\" \"" + self.fileParticles[fileParticle] + "\"")
        rbhus.debug.info(status)
      self.syncingDone.emit(fileParticle, self.fileParticles[fileParticle])


class QListWidgetItemSort(QListWidgetItem):

  def __lt__(self, other):
    return self.data(QtCore.Qt.UserRole) < other.data(QtCore.Qt.UserRole)

  def __ge__(self, other):
    return self.data(QtCore.Qt.UserRole) > other.data(QtCore.Qt.UserRole)



class getIconDoneEvent(QtCore.QThread):
  iconGenerated = QtCore.pyqtSignal(object)
  def __init__(self,iconQDoneSignal, parent=None):
    super(getIconDoneEvent,self).__init__(parent)
    self.iconQDoneSignal = iconQDoneSignal


  def run(self):
    while True:
      iconObj = self.iconQDoneSignal.get()
      # print('received python object:', iconObj.mainFile)
      try:
        self.iconGenerated.emit(iconObj)
      except:
        rbhus.debug.info(sys.exc_info())




# class server(QtCore.QThread):
#   def __init__(self,iconQDoneSignal,parent=None):
#     super(server,self).__init__(parent)
#     self.iconQDoneSignal = iconQDoneSignal
#     self._context = zmq.Context()
#     self._portServer = serverIPC
#     self._portWorker = workerIPC
#
#   def process(self, iconQ, iconQDoneSignal):
#     setproctitle.setproctitle("server-worker-process")
#
#
#     while(True):
#       fileDets = iconQ.get()
#       # rbhus.debug.info(fileDets)
#       fAbsPath = fileDets.absPath
#       mimeType = fileDets.mimeType
#       fDir = os.path.dirname(fAbsPath)
#       fName = fileDets.fileName
#       # fThumbzDbDir = os.path.join(fDir, ".thumbz.db")
#       fJson = fileDets.jsonFile
#       fThumbz = fileDets.thumbFile
#       fThumbzDir = os.path.dirname(fThumbz)
#       fLockPath = rbhus.dfl.LockFile(fThumbz,timeout=0,expiry=30)
#
#       # rbhus.debug.info(fThumbzDir)
#       try:
#         os.makedirs(fThumbzDir)
#       except:
#         pass
#       fModifiedTime = os.path.getmtime(fAbsPath)
#       # if (os.path.exists(fLockPath.lock_file)):
#       #   if ((time.time() - os.path.getmtime(fLockPath.lock_file)) > 60):
#       #     rbhus.debug.info("locked file for more than 1 minute : " + str(fAbsPath))
#
#       if (os.path.exists(fThumbzDir)):
#
#         if (os.path.exists(fJson)):
#           try:
#             with fLockPath:
#               fThumbzDetails = jsonRead(fJson)
#               if (fThumbzDetails[fName] < fModifiedTime):
#                 try:
#                   thumbzCmd = rbhus.constantsPipe.mimeConvertCmds[mimeType].format(fAbsPath, fThumbz)
#                 except:
#                   thumbzCmd = None
#                 if (thumbzCmd):
#                   rbhus.debug.info(thumbzCmd)
#                   p = subprocess.Popen(thumbzCmd, shell=True)
#                   retcode = p.wait()
#                   # print("generated thumb : "+ str(fThumbz))
#
#                   if (retcode == 0):
#                     fThumbzDetails = {fName: fModifiedTime}
#                     jsonWrite(fJson, fThumbzDetails)
#           except:
#             rbhus.debug.info("file is updated by someone : " + str(fAbsPath))
#         else:
#           fThumbzDetails = {fName: fModifiedTime}
#           jsonWrite(fJson, fThumbzDetails)
#           try:
#             thumbzCmd = rbhus.constantsPipe.mimeConvertCmds[mimeType].format(fAbsPath, fThumbz)
#           except:
#             thumbzCmd = None
#           if (thumbzCmd):
#             # rbhus.debug.info(thumbzCmd)
#             p = subprocess.Popen(thumbzCmd, shell=True)
#             retcode = p.wait()
#
#       # fileDets.thumbFile = fThumbz
#       # fileDets.mainFile = fAbsPath
#       # fileDets.subPath = fDir
#       iconQDoneSignal.put(fileDets)
#
#
#
#
#
#
#   def _worker(self,worker_url,iconQ):
#
#     worker_id = uuid.uuid4()
#     setproctitle.setproctitle("server-worker : "+ str(worker_id))
#     rbhus.debug.info("running worker")
#     rbhus.debug.info (worker_url +" : "+ str(worker_id))
#     context = zmq.Context()
#     # Socket to talk to dispatcher
#     socket = context.socket(zmq.REP)
#     socket.poll(timeout=1)
#     socket.connect(worker_url)
#
#
#     while True:
#       fileDets = socket.recv_pyobj()
#       # setproctitle.setproctitle("server-worker : " + str(fileDets.absPath))
#       socket.send_pyobj(fileDets)
#       # rbhus.debug.info("Filepath recieved : [ {0} ]".format(str(fileDets.absPath)))
#       iconQ.put(fileDets)
#
#   def run(self):
#     rbhus.debug.info("server run")
#     pool_size = 4
#     worker_port = self._portWorker
#     server_port = self._portServer
#     url_worker = "ipc:///tmp/" + worker_port
#     url_client = "ipc:///tmp/" + server_port
#     clients = self._context.socket(zmq.ROUTER)
#     try:
#       clients.bind(url_client)
#     except:
#       rbhus.debug.info (sys.exc_info())
#       self._context.term()
#       sys.exit(1)
#
#     # Socket to talk to workers
#     workers = self._context.socket(zmq.DEALER)
#     try:
#       workers.bind(url_worker)
#     except:
#       rbhus.debug.info (sys.exc_info())
#       self._context.term()
#       sys.exit(1)
#
#
#     iconQ = multiprocessing.Queue(pool_size)
#
#     multiprocessing.Pool(processes=pool_size, initializer=self.process, initargs = (iconQ,self.iconQDoneSignal))
#     # Launch pool of worker process
#     multiprocessing.Pool(processes=pool_size, initializer=self._worker, initargs=(url_worker,iconQ, ))
#     # p.daemon = False
#
#     zmq.proxy(clients, workers)
#
#     print("We never get here but clean up anyhow")
#     try:
#       clients.close()
#       workers.close()
#       self._context.term()
#     except:
#       print(sys.exc_info())
#     # self.finished.emit() # dont enable this . this will simply emit finished twice .. !!!


# class fileDirLoadedThread(QtCore.QThread):
#   fileIcon = QtCore.pyqtSignal(object)
#   iconProcessStarted = QtCore.pyqtSignal()
#   def __init__(self, filesLoaded,pathSelected):
#     super(fileDirLoadedThread, self).__init__()
#     self._ip = 'localhost'
#     self.filesLoaded = filesLoaded
#     self._pleaseStop = False
#     self.pathSelected = pathSelected
#     global context
#     self.socket = context.socket(zmq.REQ)
#     self.socket.connect("ipc:///tmp/"+ serverIPC)
#     # rbhus.debug.info("Sending request {0} ".format(fileDets))
#
#
#   def pleaseStop(self):
#     rbhus.debug.info("Stopping thread")
#     self._pleaseStop = True
#
#   def run(self):
#     for filePath in self.filesLoaded:
#       if(self._pleaseStop):
#         break
#       if(os.path.isfile(filePath)):
#         pathSelected = os.path.relpath(os.path.abspath(os.path.dirname(filePath)), ROOTDIR)
#         rbhus.debug.info(pathSelected)
#         for mimeType in rbhus.constantsPipe.mimeTypes.keys():
#           if (self._pleaseStop):
#             break
#           mimeExts = rbhus.constantsPipe.mimeTypes[mimeType]
#           for mimeExt in mimeExts:
#             if (self._pleaseStop):
#               break
#
#             rbhus.debug.info("reached here")
#
#             if (filePath.endswith(mimeExt)):
#               fileDets = rbhus.utilsPipe.thumbz_db()
#               fileDets.mainFile = filePath
#               fileDets.absPath = filePath
#               fileDets.subPath = pathSelected
#               fileDets.mimeType = mimeType
#               fileDets.mimeExt = mimeExt
#
#               fName = os.path.basename(filePath)
#               fileDets.fileName = fName
#
#               fThumbz = os.path.join(thumbsDbDir, pathSelected, fName + ".png")
#               fJson = os.path.join(thumbsDbDir, pathSelected, fName + ".json")
#               fileDets.thumbFile = fThumbz
#               fileDets.jsonFile = fJson
#
#               try:
#                 self.fileIcon.emit(fileDets)
#                 self.startIconGen(fileDets)
#               except:
#                 rbhus.debug.error(sys.exc_info())
#               time.sleep(0.02)
#     self.socket.close()
#
#   def startIconGen(self,fileDets):
#     if self._pleaseStop:
#       return
#
#     self.socket.send_pyobj(fileDets)
#     # rbhus.debug.info("sending filepath")
#     recvd_obj = self.socket.recv_pyobj()


class fileDirLoadedThread(QtCore.QThread):
  thumbzSignal = QtCore.pyqtSignal(object)
  thumbzStarted = QtCore.pyqtSignal()
  thumbzTotal = QtCore.pyqtSignal(object)

  def __init__(self,parent=None,assPath=None, pathSelected=None):
    super(fileDirLoadedThread, self).__init__(parent)
    self.assPath = assPath
    self.pathSelected = pathSelected
    self.pleaseStop = False
    self.name = str(self.pathSelected).replace("/", ":").split(self.assPath)[1]

  def exitshit(self):
    self.pleaseStop = True

  def callback_stop(self):
    return self.pleaseStop

  def callback_media(self,obj):
    self.thumbzSignal.emit(obj)

  def callback_total(self,obj):
    self.thumbzTotal.emit(obj)

  def run(self):
    self.thumbzStarted.emit()
    rbhus.utilsPipe.getUpdatedMediaThumbz(self.assPath, pathSelected=self.pathSelected, QT_callback_signalThumbz=self.callback_media, QT_callback_isStopped=self.callback_stop, QT_callback_total=self.callback_total)


class FSM4Files(QFileSystemModel):

  def __init__(self,**kwargs):
    super(FSM4Files, self).__init__(**kwargs)

  def data(self, index, role):
    if (index.isValid()):
      if(index.column() == 0):
        if( role == QtCore.Qt.DecorationRole):
          filePath = os.path.abspath(str(self.filePath(index)))
          pathSelected = os.path.relpath(os.path.dirname(filePath), ROOTDIR)
          fName = os.path.basename(filePath)
          fThumbz = os.path.join(thumbsDbDir, pathSelected, fName + ".png")
          if (os.path.exists(fThumbz)):
            # rbhus.debug.info(fThumbz)
            pixmap = QtGui.QPixmap(fThumbz)
            return pixmap.scaled(64, 64, QtCore.Qt.KeepAspectRatio)

    return super(FSM4Files, self).data(index, role)



class ExtensionFilterProxyModel(QSortFilterProxyModel):
  def __init__(self, exclude_exts=None, filter=None, parent=None):
    super(ExtensionFilterProxyModel, self).__init__(parent)
    # List of extensions to exclude
    self.exclude_exts = exclude_exts if exclude_exts is not None else []
    self.filter = filter if filter is not None else []

  def filterAcceptsRow(self, source_row, source_parent):
    # Get the index of the item
    index = self.sourceModel().index(source_row, 0, source_parent)
    # Get the file name and extension
    file_name = self.sourceModel().fileName(index)
    file_ext = file_name.split(".")[-1].lower()

    # Show hidden files when the checkbox is checked
    if 'hidden' in self.filter:
      return True  # Show all files when checkbox is enabled

    # Hide files with extensions in the exclude list
    if file_ext in self.exclude_exts:
      return False

    return True


class FSM(QFileSystemModel):

  def __init__(self,**kwargs):
    super(FSM, self).__init__(**kwargs)
    self.fileDets = None



  def canFetchMore(self,idx):
    if (self.filePath(idx) == CUR_ROOTDIR_POINTER):
      rootIdx = self.index(ROOTDIR)
      return super(FSM, self).fetchMore(idx)
    elif (self.filePath(idx).endswith(".thumbz.db")):
      return False
    else:
      return super(FSM, self).canFetchMore(idx)

  # def rowCount(self,idx):
  #   rbhus.debug.info(idx.row())
  #   # return(idx.row() + 1)
  #   return super(FSM, self).rowCount(idx)

  def fetchMore(self,idx):
    if (self.filePath(idx) == CUR_ROOTDIR_POINTER):
      rootIdx = self.index(ROOTDIR)
      return super(FSM, self).fetchMore(idx)
    elif(self.filePath(idx).endswith(".thumbz.db")):
      return None
    else:
      return super(FSM, self).fetchMore(idx)

  def headerData(self,section,orientation,role):
    if(section == 0 and role == QtCore.Qt.DisplayRole):
      return "Folders"
    else:
      return super(FSM, self).headerData(section,orientation,role)

  def filePath(self, idx):
    rootIdx = self.index(CUR_ROOTDIR_POINTER)
    if(idx == rootIdx):
      return ROOTDIR
    else:
      return super(FSM, self).filePath(idx)

def listFilesFinished(main_ui):
  # main_ui.splitter.adjustSize()
  print("trying to fix vanishing items -- WTF!!!!")

def dirSelected(idx, modelDirs, main_ui):
  global filterList
  global fileThumbzWidget
  global  fileThumbzItems
  # global fileIconThreadRunning
  global fileIconThreads
  global CUR_DIR_SELECTED

  fileThumbzWidget.clear()
  fileThumbzItems.clear()
  main_ui.listFiles.clear()

  pathSelected = modelDirs.filePath(idx)
  main_ui.labelFile.setText(str(pathSelected).replace(ROOTDIR,"-"))
  CUR_DIR_SELECTED = pathSelected

  if fileIconThreads:
    rbhus.debug.info(fileIconThreads)
    try:
      for thread in fileIconThreads:
        rbhus.debug.info("Stopping thread")
        thread.exitshit()
        thread.wait()
        try:
          thread.disconnect()
        except:
          rbhus.debug.debug(thread)
        try:
          thread.deleteLater()
        except:
          rbhus.debug.debug(sys.exc_info())
        fileIconThreads.remove(thread)
    except:
      rbhus.debug.info(sys.exc_info())

  # fileThumbzWidget = {}
  # fileThumbzItems = {}

  directory_path = ROOTDIR if pathSelected == CUR_ROOTDIR_POINTER else pathSelected

  fileGlob = []
  # directory_path = ""
  mimeExts = []

  # if (pathSelected == CUR_ROOTDIR_POINTER):
  #   directory_path = ROOTDIR
  # else:
  #   directory_path = pathSelected
  
  if filterList:
    for filter in filterList:
      mimeExts.extend(rbhus.constantsPipe.mimeTypes[filter])
    for mime in mimeExts:
      fileGlob.extend(glob.glob(directory_path + os.sep + "*{0}".format(mime)))
  else:
    fileGlob = glob.glob(directory_path + os.sep + "*")

  rbhus.debug.info(filterList)
  rbhus.debug.info(mimeExts)
  # rbhus.debug.info(fileGlob)

  # if(pathSelected == CUR_ROOTDIR_POINTER):

  #   fileGlob = glob.glob(ROOTDIR + os.sep + "*")
  # else:
  #   fileGlob = glob.glob(pathSelected + os.sep + "*")

  try:
    fileGlob.remove("-")
  except:
    pass

  totalFiles = len([x for x in fileGlob if(os.path.isfile(x))])
  main_ui.labelTotal.setText(str(totalFiles))
  if(fileGlob):
    fileGlob.sort()
    # rbhus.debug.info(fileGlob)
    # fileIconThreadRunning = fileDirLoadedThread(fileGlob,CUR_DIR_SELECTED)
    # fileIconThreadRunning.fileIcon.connect(lambda fileIconDets, pathSelected = pathSelected, main_ui=main_ui :fileIconActivate(fileIconDets,pathSelected,main_ui))
    # fileIconThreadRunning.finished.connect(lambda main_ui= main_ui : listFilesFinished(main_ui))
    # ass_path_selected = assPath+main_ui.labelFile.text().lstrip("-").replace("/",":")
    # rbhus.debug.info(ass_path_selected)
    fileIconThreadRunning = fileDirLoadedThread(assPath=assPath, pathSelected=pathSelected, parent=main_ui)
    # fileIconThreadRunning.thumbzStarted.connect(lambda mainUid=mainUid: clearListWidgetSubDir(mainUid))
    fileIconThreadRunning.thumbzSignal.connect(lambda mediaObj, pathSelected = pathSelected, main_ui=main_ui :fileIconActivate(mediaObj,pathSelected,main_ui))
    fileIconThreadRunning.finished.connect(lambda main_ui=main_ui : fileIconsFinished(main_ui))
    fileIconThreads.append(fileIconThreadRunning)
    rbhus.debug.info("Starting thread")
    fileIconThreadRunning.start()

  searchTerm = main_ui.lineEditSearch.text().strip()
  exclude_extensions = [ext.lstrip('.') for ext in rbhus.constantsPipe.mimeTypes["hidden"]]
  modelFiles = FSM4Files(parent=main_ui)
  modelFiles.setRootPath(CUR_DIR_SELECTED)
  modelFiles.setFilter(QtCore.QDir.Files | QtCore.QDir.NoDotAndDotDot)
  if searchTerm:
    if mimeExts:
      modelFiles.setNameFilters([searchTerm + "*" + ext for ext in mimeExts])
    else:
      modelFiles.setNameFilters([searchTerm + "*"])
  else:
    modelFiles.setNameFilters(["*" + ext for ext in mimeExts])
  modelFiles.setNameFilterDisables(False)
  rootIdx = modelFiles.index(CUR_DIR_SELECTED)
  proxy_model = ExtensionFilterProxyModel(exclude_exts=exclude_extensions,filter=filterList)
  proxy_model.setSourceModel(modelFiles)
  # main_ui.tableFiles.setModel(modelFiles)
  # main_ui.tableFiles.setRootIndex(rootIdx)
  main_ui.tableFiles.setModel(proxy_model)
  main_ui.tableFiles.setRootIndex(proxy_model.mapFromSource(rootIdx))
  # main_ui.tableFiles.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
  header = main_ui.tableFiles.horizontalHeader()
  header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
  header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
  header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)




def fileIconActivate(fileIconDets,pathSelected, main_ui):
  # print("recvd preview : "+ str(fileIconDets.subPath))
  global filterList
  global fileThumbzWidget
  global fileThumbzItems

  # fileSelectedIdx = main_ui.tableFiles.model().index(fileIconDets.mainFile)
  # try:
  #   main_ui.tableFiles.update()
  #   app.processEvents()
  # except:
  #   rbhus.debug.info(sys.exc_info())
  # icon = QtGui.QIcon(fileIconDets.thumbFile)
  # main_ui.tableFiles.model().setData(fileSelectedIdx, icon, QtCore.Qt.DecorationRole)
  # main_ui.tableFiles.resizeColumnsToContents()
  # rbhus.debug.info(fileIconDets.subPath)
  # rbhus.debug.info(main_ui.labelFile.text().lstrip("-/"))

  if filterList:
    if not fileIconDets.mimeType in filterList:
      return

  if fileIconDets.subPath == ".":
    pass
  else:
    if not fileIconDets.subPath in pathSelected:
      return
    if not fileIconDets.subPath == main_ui.labelFile.text().lstrip("-/"):
      return

  if fileIconDets.mainFile in fileThumbzWidget:
    imageWidgetUpdated(fileIconDets)
    return

  itemWidget = uic.loadUi(mediaThumbz_ui_file)
  fileThumbzWidget[fileIconDets.mainFile] = itemWidget
  itemWidget.labelImageName.setText(os.path.basename(fileIconDets.mainFile))
  itemWidget.labelLogo.setParent(itemWidget.labelImage)

  try:
    modifiedT = os.path.getmtime(fileIconDets.mainFile)
  except:
    modifiedT = 0
  # print(time.ctime(modifiedT))
  itemWidget.setToolTip("fileName: " + os.path.basename(fileIconDets.mainFile) + "\nmodified : " + str(time.ctime(modifiedT)))
  # itemWidget.pushButtonImage.clicked.connect(lambda x, imagePath=fileIconDets.mainFile, mimeType=fileIconDets.mimeType: imageWidgetClicked(imagePath, mimeType=mimeType))

  item = QListWidgetItemSort()
  fileThumbzItems[fileIconDets.mainFile] = item
  item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)


  logoIcon = QtGui.QPixmap(rbhus.constantsPipe.mimeLogos[fileIconDets.mimeType])
  logoIconScaled = logoIcon.scaled(20,20,QtCore.Qt.KeepAspectRatio)
  itemWidget.labelLogo.setPixmap(logoIconScaled)

  # item.setSizeHint(QtCore.QSize(96,96))
  item.setData(QtCore.Qt.UserRole, os.path.basename(fileIconDets.mainFile))
  item.setToolTip(os.path.basename(fileIconDets.mainFile))
  item.media = fileIconDets
  item.setSizeHint(itemWidget.sizeHint() + QtCore.QSize(10, 10))
  main_ui.listFiles.addItem(item)
  main_ui.listFiles.setItemWidget(item, itemWidget)
  # print("thumbz added :: "+ fileIconDets.mainFile)
  imageWidgetUpdated(fileIconDets)





def imageWidgetUpdated(fileDets):
  global fileThumbzWidget
  global fileThumbzItems
  # print("updated icon : "+ fileDets.mainFile)
  try:
    fileIcon = QtGui.QPixmap(fileDets.thumbFile)
    scaledIcon = fileIcon.scaled(80,80,QtCore.Qt.KeepAspectRatio )
    fileThumbzWidget[fileDets.mainFile].labelImage.setPixmap(scaledIcon)
    fileThumbzWidget[fileDets.mainFile].labelImage.setMinimumSize(QtCore.QSize(100, 100))
    # fileThumbzWidget[fileDets.mainFile].pushButtonImage.setIconSize(QtCore.QSize(94, 94))
    fileThumbzWidget[fileDets.mainFile].adjustSize()
    fileThumbzItems[fileDets.mainFile].setSizeHint(fileThumbzWidget[fileDets.mainFile].sizeHint()  + QtCore.QSize(10, 10))

  except:
    rbhus.debug.info(str(sys.exc_info()))


# def filesSelected(modelFiles, main_ui):
#   selectedIdx = main_ui.listFiles.selectedIndexes()
#   rbhus.debug.info(selectedIdx)
#   for idx in selectedIdx:
#     print("--------")
#     print(modelFiles.filePath(idx))


def fileIconsFinished(main_ui):
  global fileIconThreads
  for thread in fileIconThreads:
    if thread.isFinished():
      rbhus.debug.info(f"Thread <{thread.name}> is finished. Deleting...")
      thread.deleteLater()
      fileIconThreads.remove(thread)


def popUpFolders(main_ui,pos):

  menu = QtWidgets.QMenu()

  ioMenu = QtWidgets.QMenu("IO")
  folderMenu = QtWidgets.QMenu("folder")
  clipboardMenu = QtWidgets.QMenu("clipboard")
  createFolderAction = ioMenu.addAction("new")
  deleteFolderAction = ioMenu.addAction("delete")
  deleteFolderAction.setEnabled(False)

  copyFolderPathAction = clipboardMenu.addAction("copy path to clipboard")
  renameFolderAction = folderMenu.addAction("rename")

  menu.addMenu(folderMenu)
  menu.addMenu(clipboardMenu)
  menu.addMenu(ioMenu)
  action = menu.exec_(main_ui.treeDirs.mapToGlobal(pos))

  if (action == createFolderAction):
    createFolder(main_ui)
  if(action == deleteFolderAction):
    deleteFolder(main_ui)
  if(action == copyFolderPathAction):
    copyPathToClipboard(main_ui)
  if (action == renameFolderAction):
    folderRenameDialog(main_ui)


def createFolder(main_ui):
  global CUR_DIR_SELECTED
  dialog = QtWidgets.QInputDialog(main_ui.treeDirs)
  dialog.setInputMode(QtWidgets.QInputDialog.TextInput)
  dialog.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
  dialog.setWindowTitle("Create Folder")
  dialog.setLabelText("Folder Name :")
  # (pathRoot, ext) = os.path.splitext(os.path.basename(selected.media.mainFile))
  # if(ext):
  # dialog.setTextValue(pathRoot)
  # else:
  #   dialog.setTextValue(os.path.basename(selected.media.mainFile))
  dialog.adjustSize()
  dialog.resize(500, 80)
  # dialog.adjustSize()

  dialog.exec_()
  newFolder = os.path.join(CUR_DIR_SELECTED,dialog.textValue())
  if(newFolder):
    rbhus.debug.info("CREATING FOLDERS : "+ newFolder)
    try:
      os.makedirs(newFolder)
    except:
      msgBox = QtWidgets.QMessageBox(parent=main_ui.treeDirs)
      msgBox.adjustSize()
      msgBox.setIcon(QtWidgets.QMessageBox.Warning)
      msgBox.setText(str(sys.exc_info()))


      msgBox.exec_()





def deleteFolder(main_ui):
  global CUR_DIR_SELECTED
  if(CUR_DIR_SELECTED == ROOTDIR):
    msgBox = QtWidgets.QMessageBox(parent=main_ui.treeDirs)
    msgBox.adjustSize()
    msgBox.setIcon(QtWidgets.QMessageBox.Warning)
    msgBox.setText("Cannot remove base asset directory")
    msgBox.exec_()
    return(0)

  try:
    thrashPath = os.path.join(rbhus.utilsPipe.rbhusTrash, assDets['assetId'])
    try:
      os.makedirs(thrashPath)
    except:
      rbhus.debug.warning(sys.exc_info())
    os.system("mv -v --force "+ CUR_DIR_SELECTED +" "+ thrashPath + os.sep)
    rbhus.utilsPipe.updateAssModifies(assDets['assetId'], "deleted : " + CUR_DIR_SELECTED)
  except:
    msgBox = QtWidgets.QMessageBox(parent=main_ui.treeDirs)
    msgBox.adjustSize()
    msgBox.setIcon(QtWidgets.QMessageBox.Warning)
    msgBox.setText(str(sys.exc_info()))

    msgBox.exec_()


def on_selection_changed(main_ui):
  try:
    for index in range(main_ui.listFiles.count()):
      item = main_ui.listFiles.item(index)
      fileThumbzWidget[item.media.mainFile].setStyleSheet("background-color: white;")
    selectedItems = main_ui.listFiles.selectedItems()
    for selectedItem in selectedItems:
      fileThumbzWidget[selectedItem.media.mainFile].setStyleSheet("background-color: orange;")
  except Exception as e:
    rbhus.debug.info(f"item not found: {e}")


def getSelectedFiles(main_ui):
  files =[]
  # if(main_ui.checkDetails.isChecked()):
  if currView == "LIST":
    selectedIdxs = main_ui.tableFiles.selectionModel().selectedRows()
    modelFiles = main_ui.tableFiles.model()
    for selectedIdx in selectedIdxs:
      files.append(modelFiles.filePath(selectedIdx))
  # else:
  if currView == "ICON":
    selectedItems = main_ui.listFiles.selectedItems()
    for selectedItem in selectedItems:
      files.append(selectedItem.media.mainFile)


  return(files)


def popUpFiles(main_ui,context,pos):
  global fileThumbzItems
  clip = QtWidgets.QApplication.clipboard()
  pasteUrls = clip.mimeData().urls()
  # print(pasteUrls)

  menu = QtWidgets.QMenu()
  openMenu = QtWidgets.QMenu()
  openMenu.setTitle("open with")
  fileMenu  = QtWidgets.QMenu()
  fileMenu.setTitle("file")
  ioMenu = QtWidgets.QMenu()
  ioMenu.setTitle("IO")


  clipboardMenu = QtWidgets.QMenu()
  clipboardMenu.setTitle("clipboard")

  fileImageCopyAction = clipboardMenu.addAction("copy image to clipboard")
  # filePathCopyAction = clipboardMenu.addAction("copy project path to clipboard")
  fileImageCopyAction.setEnabled(False)
  # filePathCopyAction.setEnabled(False)



  selectedFiles = getSelectedFiles(main_ui)
  rbhus.debug.info(selectedFiles)

  openWithCmdActions = {}
  if(selectedFiles):
    try:
      sel = re.sub("~$", "", selectedFiles[0])
      rbhus.debug.info(sel)
      selected = fileThumbzItems[sel]
      rbhus.debug.info(selected)
    except:
      rbhus.debug.info(sys.exc_info())
      selected = None
    if(selected):
      if selected.media.mimeType in rbhus.constantsPipe.mimeTypesOpenCmds:
        cmds = rbhus.constantsPipe.mimeTypesOpenCmds[selected.media.mimeType]["linux"]
        for cmd in cmds:
          if cmd in rbhus.constantsPipe.mimeCmdsLinux:
            openWithCmdActions[openMenu.addAction(cmd)] = rbhus.constantsPipe.mimeCmdsLinux[cmd]
          else:
            openWithCmdActions[openMenu.addAction(cmd)] = cmd
      if(selected.media.mimeType == "image"):
        fileImageCopyAction.setEnabled(True)


    else:
      openWithCmdActions[openMenu.addAction("system_assigned_application")] = "system_assigned_application"
    # filePathCopyAction.setEnabled(True)




    ioCopyAction = ioMenu.addAction("copy")
    ioDeleteAction = ioMenu.addAction("delete")
    # ioDeleteAction.setEnabled(False)

    fileNameRenameAction = fileMenu.addAction("rename")

    # fileCopyPathAction

  ioPasteAction = ioMenu.addAction("paste")

  if(pasteUrls):
    ioPasteAction.setEnabled(True)
  else:
    ioPasteAction.setEnabled(False)




  menu.addMenu(openMenu)
  menu.addMenu(fileMenu)
  menu.addMenu(clipboardMenu)
  menu.addMenu(ioMenu)

  action = menu.exec_(context.mapToGlobal(pos))




  if(action in openWithCmdActions.keys()):
    runCmd = openWithCmdActions[action]
    try:
      openFile(main_ui,runCmd)
    except:
      rbhus.debug.error(sys.exc_info)

  if(action == ioPasteAction):
    pasteFilesFromClipboard(main_ui,pasteUrls)

  if(selectedFiles):
    if(action == ioCopyAction):
      copyToClipboard(main_ui)

    if(action == fileNameRenameAction):
      try:
        fileRenameDialog(main_ui)
      except:
        print("rename failed : " + str(sys.exc_info()))
    if(action == ioDeleteAction):
      deleteFiles(main_ui)
    if(action == fileImageCopyAction):
      copyImageToClipboard(main_ui)




def openFile(main_ui,cmd):
  global assDets
  global isCopying
  global isQuiting
  selectedFiles = getSelectedFiles(main_ui)
  selected = []
  for x in selectedFiles:
    selected.append("\""+ x +"\"")

  rbhus.debug.info("cmd : "+ str(cmd))
  rbhus.debug.info(selected)
  if(cmd.startswith("project_")):
    cmdToRun = rbhus.utilsPipe.openAssetCmd(assDets, selected[0])
    rbhus.debug.info("command to run :"+ str(cmdToRun))
    if(cmdToRun):
      cmdFull = cmdToRun
    else:
      cmdFull = cmd.format(selected)
  elif(cmd.startswith("system_")):
    # import webbrowser
    cmdFull = "xdg-open "+ " ".join(selected)
  else:
    cmdFull = cmd.format(" ".join(selected))
  rbhus.debug.info(cmdFull)
  subprocess.Popen(cmdFull,shell=True)
  # rbhus.debug.info(p.communicate())


  if(args.close):
    if(isCopying):
      isQuiting = True
    else:
      QApplication.quit()

def deleteFiles(main_ui):
  global fileThumbzWidget
  global CUR_DIR_SELECTED
  # global fileIconThreadRunning
  selected = getSelectedFiles(main_ui)
  # selected = main_ui.listFiles.selectedItems()

  for item in selected:
    if(os.path.exists(item)):
      thrashPath  = os.path.join(rbhus.utilsPipe.rbhusTrash,assDets['assetId'])
      try:
        os.makedirs(thrashPath)
      except:
        rbhus.debug.warning(sys.exc_info())
      mvCmd = "mv \""+ item +"\" \""+ thrashPath +"\""
      reply = QtWidgets.QMessageBox.question(main_ui.listFiles, "WARNING", "Do you want to delete the selected files?!!", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
      if(reply == QtWidgets.QMessageBox.Yes):
        os.system(mvCmd)
        try:
          fileThumbzWidget[item].deleteLater()
          del fileThumbzWidget[item]
          delIndex = main_ui.listFiles.indexFromItem(fileThumbzItems[item])
          main_ui.listFiles.takeItem(delIndex.row())
        except:
          pass
        rbhus.utilsPipe.updateAssModifies(assDets['assetId'], "deleted : " + item)


def tray_icon_change(icon_anim,tray_icon):
  tray_icon.setIcon(QtGui.QIcon(icon_anim.currentPixmap()))


def setToolTip(tray_icon,src,dest,main_ui):

  tray_icon.showMessage("COPYING",src +"->"+ dest)


def syncingDoneEvent(src,dest,main_ui):
  global CUR_DIR_SELECTED
  # global fileIconThreadRunning
  global fileIconThreads
  if(not os.path.isdir(src)):
    fileGlob = [dest]
    # fileIconThreadRunning = fileDirLoadedThread(fileGlob,CUR_DIR_SELECTED)
    # fileIconThreadRunning.fileIcon.connect(lambda fileIconDets, pathSelected = CUR_DIR_SELECTED, main_ui=main_ui :fileIconActivate(fileIconDets,pathSelected,main_ui))
    #  # fileIconThreadRunning.finished.connect(lambda main_ui= main_ui : listFilesFinished(main_ui))
    # fileIconThreads.append(fileIconThreadRunning)
    # fileIconThreadRunning.start()
    # fileIconThreadRunning.wait()
    # rbhus.debug.info("created ICON FOR : "+ dest)

    fileIconThreadRunning = fileDirLoadedThread(assPath=assPath, parent=main_ui)
    # fileIconThreadRunning.thumbzStarted.connect(lambda mainUid=mainUid: clearListWidgetSubDir(mainUid))
    fileIconThreadRunning.thumbzSignal.connect(lambda mediaObj, pathSelected=CUR_DIR_SELECTED, main_ui=main_ui: fileIconActivate(mediaObj, pathSelected, main_ui))
    fileIconThreads.append(fileIconThreadRunning)
    rbhus.debug.info("Starting thread")
    fileIconThreadRunning.start()
    fileIconThreadRunning.wait()


def copyingFinished(tray_icon,tray_icon_anim):
  global isCopying
  tray_icon_anim.disconnect()
  tray_icon_anim.deleteLater()
  tray_icon.deleteLater()
  try:
    isCopying.pop()
  except:
    rbhus.debug.error(sys.exc_info())
  if(not isCopying):
    if(isQuiting):
      QApplication.quit()



def pasteFilesFromClipboard(main_ui,urls):
  global fileThumbzWidget
  global CUR_DIR_SELECTED
  # global fileIconThreadRunning
  global isCopying
  # rbhus.debug.info("COPYING FILE")
  tray_icon_anim = QtGui.QMovie(busyIconGif)
  tray_icon_anim.start()

  # rbhus.debug.info("COPYING FILE : tray icon start")
  tray_icon = QtWidgets.QSystemTrayIcon(QtGui.QIcon(busyIconGif), main_ui)
  tray_icon_anim.frameChanged.connect(lambda frameNumber, icon_anim=tray_icon_anim, tray_icon=tray_icon: tray_icon_change(icon_anim, tray_icon))
  tray_icon.show()
  # rbhus.debug.info("COPYING FILE : tray icon end")

  applyOption = QtCore.Qt.Unchecked
  rewriteReply = QtWidgets.QMessageBox.No
  fileParticles = {}

  for url in urls:
    # applyOptionLocal = False
    sourceFile = url.toLocalFile()
    # rbhus.debug.info("COPYING FILE : "+ str(sourceFile))
    isDir = os.path.isdir(sourceFile)
    sourceFileBaseName = os.path.basename(sourceFile)
    sourceDir = os.path.dirname(sourceFile)
    destFile = os.path.join(CUR_DIR_SELECTED,sourceFileBaseName)
    reply = QtWidgets.QMessageBox.No
    if(os.path.exists(destFile)):
      if(applyOption == QtCore.Qt.Unchecked):
        msgBox = QtWidgets.QMessageBox()
        applyToAll = QtWidgets.QCheckBox("apply to all")
        msgBox.setText("Overwrite : " + sourceFileBaseName)
        msgBox.addButton(QtWidgets.QMessageBox.Yes)
        msgBox.addButton(QtWidgets.QMessageBox.No)
        msgBox.setDefaultButton(QtWidgets.QMessageBox.No)
        msgBox.setCheckBox(applyToAll)
        # applyToAll.stateChanged.connect(lambda stateChanged, applyOption = applyOption :rewriteFunc(stateChanged,applyOption))
        reply = msgBox.exec_()
        applyOption = applyToAll.checkState()
        if(applyOption == QtCore.Qt.Checked):
          rewriteReply = reply
      else:
        reply = rewriteReply



      rbhus.debug.info(applyOption)
      # reply = QtWidgets.QMessageBox.question(main_ui.listFiles, "WARNING", "Overwrite : " + sourceFileBaseName, QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
      if (reply == QtWidgets.QMessageBox.No):
        rbhus.debug.info("skipping : "+ sourceFile)
        continue
      else:
        fileParticles[sourceFile] = destFile
    else:
      fileParticles[sourceFile] = destFile

  if (fileParticles):
    isCopying.append(1)
    sT = syncThread(main_ui, fileParticles)
    sT.syncing.connect(lambda src, dest, tray_icon=tray_icon,main_ui=main_ui: setToolTip(tray_icon, src,dest,main_ui))
    sT.syncingDone.connect(lambda src, dest, main_ui=main_ui: syncingDoneEvent(src,dest,main_ui))
    sT.finished.connect(lambda tray_icon = tray_icon, tray_icon_anim= tray_icon_anim : copyingFinished(tray_icon,tray_icon_anim))
    sT.start()
  else:
    tray_icon_anim.disconnect()
    tray_icon_anim.deleteLater()
    tray_icon.deleteLater()



def copyPathToClipboard(main_ui):
  global CUR_DIR_SELECTED
  rbhus.debug.info(CUR_DIR_SELECTED)
  rbhus.pyperclip.copy(CUR_DIR_SELECTED)
  rbhus.utilsPipe.updateAssModifies(assDets['assetId'], "clipboard : " + CUR_DIR_SELECTED)




def copyToClipboard(main_ui):
  selectedFiles = getSelectedFiles(main_ui)
  urlList = []
  mimeData = QtCore.QMimeData()
  for x in selectedFiles:
    urlList.append(QtCore.QUrl().fromLocalFile(x))
    rbhus.utilsPipe.updateAssModifies(assDets['assetId'], "clipboard : " + x)
  mimeData.setUrls(urlList)

  QtWidgets.QApplication.clipboard().setMimeData(mimeData)


def copyImageToClipboard(main_ui):
  global fileThumbzItems
  selectedFiles = getSelectedFiles(main_ui)
  if(selectedFiles):
    try:
      fileSelected = fileThumbzItems[selectedFiles[0]]
      mimeType = fileSelected.media.mimeType
      if(mimeType == "image"):
        pixMapToCopy = QtGui.QPixmap(fileSelected.media.mainFile)
        QtWidgets.QApplication.clipboard().setPixmap(pixMapToCopy)
    except:
      rbhus.debug.error(sys.exc_info())


def folderRenameDialog(main_ui):
  global CUR_DIR_SELECTED
  global ROOTDIR
  if(CUR_DIR_SELECTED == ROOTDIR):
    return
  dirSelected = CUR_DIR_SELECTED
  dialog = QtWidgets.QInputDialog(main_ui.listFiles)
  dialog.setInputMode(QtWidgets.QInputDialog.TextInput)
  dialog.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,QtWidgets.QSizePolicy.MinimumExpanding)
  dialog.setWindowTitle("Rename Dialog")
  dialog.setLabelText("file:")
  (pathRoot , ext) = os.path.splitext(os.path.basename(dirSelected))
  # if(ext):
  dialog.setTextValue(pathRoot)
  # else:
  #   dialog.setTextValue(os.path.basename(selectedFile))
  dialog.adjustSize()
  dialog.resize(500,80)
  # dialog.adjustSize()

  dialog.exec_()
  fileRenamed  =  dialog.textValue() + ext
  newFile = os.path.join(ROOTDIR,os.path.relpath(os.path.abspath(os.path.dirname(dirSelected)), ROOTDIR),fileRenamed)
  rbhus.debug.info(newFile)
  copyStatus = QtCore.QFile().rename(dirSelected, newFile)
  rbhus.debug.info(newFile + " : " + str(copyStatus))
  rbhus.utilsPipe.updateAssModifies(assDets['assetId'], "renamed : " + dirSelected + " -> " + newFile)




def fileRenameDialog(main_ui):
  global fileThumbzWidget
  global fileThumbzItems

  selectedFiles = getSelectedFiles(main_ui)

  if(selectedFiles):
    selectedFile = selectedFiles[0]
  dialog = QtWidgets.QInputDialog(main_ui.listFiles)
  dialog.setInputMode(QtWidgets.QInputDialog.TextInput)
  dialog.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,QtWidgets.QSizePolicy.MinimumExpanding)
  dialog.setWindowTitle("Rename Dialog")
  dialog.setLabelText("file:")
  (pathRoot , ext) = os.path.splitext(os.path.basename(selectedFile))
  # if(ext):
  dialog.setTextValue(pathRoot)
  # else:
  #   dialog.setTextValue(os.path.basename(selectedFile))
  dialog.adjustSize()
  dialog.resize(500,80)
  # dialog.adjustSize()

  dialog.exec_()
  fileRenamed  =  dialog.textValue() + ext
  newFile = os.path.join(ROOTDIR,os.path.relpath(os.path.abspath(os.path.dirname(selectedFile)), ROOTDIR),fileRenamed)
  rbhus.debug.info(newFile)
  copyStatus = QtCore.QFile().rename(selectedFile,newFile)
  rbhus.debug.info(newFile +" : "+ str(copyStatus))
  if(copyStatus):

    try:
      fileThumbzWidget[selectedFile].labelImageName.setText(os.path.basename(newFile))
      mainFileWidget = fileThumbzWidget[selectedFile]
      del(fileThumbzWidget[selectedFile])
      # fileThumbzItems[selectedFile].media.mainFile = newFile
      fileThumbzWidget[newFile] = mainFileWidget
    except:
      rbhus.debug.info(sys.exc_info())
    rbhus.utilsPipe.updateAssModifies(assDets['assetId'], "renamed : " + selectedFile + " -> " + newFile)
    try:
      modifiedT = os.path.getmtime(newFile)
    except:
      modifiedT = 0
    # print(time.ctime(modifiedT))
    fileThumbzWidget[newFile].setToolTip("fileName: " + os.path.basename(newFile) + "\nmodified : " + str(time.ctime(modifiedT)))


def toggleView(main_ui):
  global currView

  if currView == "LIST":
    main_ui.changeViewButt.setIcon(QtGui.QIcon(os.path.join(rbhusPath,"etc","icons","list.svg")))
    currView = "ICON"
    main_ui.listFiles.show()
    main_ui.tableFiles.hide()
  elif currView == "ICON":
    main_ui.changeViewButt.setIcon(QtGui.QIcon(os.path.join(rbhusPath,"etc","icons","grid.svg")))
    currView = "LIST"
    main_ui.tableFiles.show()
    main_ui.listFiles.hide()

  # if(main_ui.checkDetails.isChecked()):
  #   main_ui.listFiles.hide()
  #   main_ui.tableFiles.show()
  # else:
  #   main_ui.tableFiles.hide()
  #   main_ui.listFiles.show()


def updateFilterList(state, main_ui, ui, modelDirs):
  rbhus.debug.info("updating filter list")
  if state == QtCore.Qt.Checked:
  # if ui.isChecked():
    filterList.append(str(ui.text()))
  else:
    try:
      filterList.remove(str(ui.text()))
    except:
      pass
  # rbhus.debug.info(filterList)
  dirSelected(main_ui.treeDirs.currentIndex(), modelDirs, main_ui)

def search(modelDirs, main_ui):
  dirSelected(main_ui.treeDirs.currentIndex(), modelDirs, main_ui)

def mainGui(main_ui):
  # iconQDoneSignal = multiprocessing.Queue(4)
  # iconServer = server(iconQDoneSignal=iconQDoneSignal,parent=main_ui)
  # iconServer.start()
  main_ui.setWindowTitle(assPath)
  main_ui.splitter.setStretchFactor(1,10)



  modelDirs = FSM()
  modelDirs.setFilter( QtCore.QDir.Dirs | QtCore.QDir.NoDotAndDotDot)
  modelDirs.setRootPath(ROOTDIR)
  filterList = COMPOUND_PATHS
  # modelDirs.setNameFilters(filterList)
  # modelDirs.setNameFilterDisables(False)


  main_ui.treeDirs.setModel(modelDirs)



  main_ui.treeDirs.hideColumn(1)
  main_ui.treeDirs.hideColumn(2)
  main_ui.treeDirs.hideColumn(3)

  rootIdx = modelDirs.index(ROOTDIR)
  main_ui.treeDirs.setRootIndex(rootIdx)
  modelDirs.mkdir(rootIdx,"-")
  for x in COMPOUND_PATHS:
    xIdx = modelDirs.index(x)
    main_ui.treeDirs.setRowHidden(xIdx.row(),xIdx.parent(),True)

  main_ui.tableFiles.setItemDelegate(DateItemDelegate())


  curRootIdx = modelDirs.index(CUR_ROOTDIR_POINTER)
  main_ui.treeDirs.setCurrentIndex(curRootIdx)
  # iconEventEater = getIconDoneEvent(iconQDoneSignal,parent=main_ui)
  # iconEventEater.iconGenerated.connect(imageWidgetUpdated)
  # iconEventEater.start()

  main_ui.lineEditSearch.textChanged.connect(lambda x, modelDirs=modelDirs, main_ui = main_ui : search(modelDirs, main_ui))

  main_ui.treeDirs.clicked.connect(lambda idnx, modelDirs=modelDirs, main_ui = main_ui : dirSelected(idnx, modelDirs, main_ui))
  # main_ui.listFiles.clicked.connect(lambda idnx, main_ui = main_ui :filesSelected(modelFiles,main_ui))
  main_ui.listFiles.itemSelectionChanged.connect(lambda main_ui = main_ui: on_selection_changed(main_ui))
  main_ui.listFiles.customContextMenuRequested.connect(lambda pos, context = main_ui.listFiles, main_ui = main_ui: popUpFiles(main_ui, context, pos))
  main_ui.tableFiles.customContextMenuRequested.connect(lambda pos, context = main_ui.tableFiles, main_ui = main_ui: popUpFiles(main_ui, context, pos))
  main_ui.treeDirs.customContextMenuRequested.connect(lambda pos, main_ui = main_ui: popUpFolders(main_ui, pos))

  # main_ui.checkDetails.clicked.connect(lambda click, main_ui=main_ui: toggleView(main_ui))
  # main_ui.checkDetails.setChecked(True)
  main_ui.changeViewButt.setIcon(QtGui.QIcon(os.path.join(rbhusPath,"etc","icons","list.svg")))
  main_ui.changeViewButt.clicked.connect(lambda click, main_ui=main_ui: toggleView(main_ui))

  toggleView(main_ui)

  layV = QtWidgets.QVBoxLayout()
  main_ui.frame.setLayout(layV)
  for mimeType in rbhus.constantsPipe.mimeTypes.keys():
    chkbx = QtWidgets.QCheckBox(mimeType)
    chkbx.stateChanged.connect(lambda state, main_ui=main_ui, ui=chkbx, modelDirs=modelDirs: updateFilterList(state, main_ui, ui, modelDirs))
    layV.addWidget(chkbx)
  vSpacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
  layV.addItem(vSpacer)

  main_ui.show()
  main_ui.update()
  dirSelected(curRootIdx, modelDirs, main_ui)



def mainfunc():
  global app
  app = QApplication(sys.argv)
  main_ui = uic.loadUi(main_ui_file)
  mainGui(main_ui)
  # ex = App()
  sys.exit(app.exec_())


if __name__ == '__main__':
  mainfunc()
