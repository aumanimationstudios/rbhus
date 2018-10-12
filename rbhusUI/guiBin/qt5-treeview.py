#!/usr/bin/env python2
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

import setproctitle
import simplejson
import zmq

# sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-1]))
progPath = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2])
rbhusPath = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-3])

busyIconGif = os.path.join(rbhusPath,"etc","icons","rbhusIconTray-BUSY.gif")

sys.path.append(rbhusPath)
import rbhus.debug
import rbhus.constantsPipe
import rbhus.utilsPipe
import rbhus.dfl

main_ui_file = os.path.join(rbhusPath, "rbhusUI", "lib", "qt5", "folderManager", "main.ui")
mediaThumbz_ui_file = os.path.join(rbhusPath, "rbhusUI", "lib", "qt5", "folderManager", "mediaThumbz.ui")
rbhus.debug.info(main_ui_file)


from PyQt5.QtWidgets import QApplication, QFileSystemModel, QListWidgetItem
from PyQt5 import QtCore, uic, QtGui, QtWidgets



parser = argparse.ArgumentParser(description="Use the comand to open a sandboxed UI for folders in an Asset")
parser.add_argument("-a","--asset",dest="asset",help="colon separated Asset path")
parser.add_argument("-p","--path",dest="path",help="Absolute path of the asset on disk")
parser.add_argument("-c","--close",dest="close",action="store_true",help="Close the app after opening a file")
# parser.add_argument("-e","--end",dest="end",help="end number")
# parser.add_argument("-p","--pad",dest="pad",help="padding for number")
args = parser.parse_args()


assPath = args.asset
assDets = rbhus.utilsPipe.getAssDetails(assPath=assPath)
if(args.path):
  ROOTDIR = args.path
else:
  ROOTDIR = rbhus.utilsPipe.getAbsPath(assPath)
CUR_ROOTDIR_POINTER = os.path.join(ROOTDIR,"-")
COMPOUND_PATHS = rbhus.utilsPipe.getCompoundPaths(assPath)
CUR_DIR_SELECTED = None
print(COMPOUND_PATHS)

fileDetsDict = {}
fileIconThreadRunning = None
fileThumbzWidget = {}
fileThumbzItems = {}

context = zmq.Context()

serverIPC = str(uuid.uuid4())
workerIPC = str(uuid.uuid4())


isCopying = []
isQuiting = False


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



class syncThread(QtCore.QThread):
  syncing = QtCore.pyqtSignal(str,str)
  syncingDone = QtCore.pyqtSignal(str,str)

  def __init__(self,parent,fileParticles):
    super(syncThread, self).__init__(parent)
    self.fileParticles  = fileParticles

  def run(self):
    for fileParticle in self.fileParticles.keys():
      self.syncing.emit(fileParticle,self.fileParticles[fileParticle])
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
        pass




class server(QtCore.QThread):
  def __init__(self,iconQDoneSignal,parent=None):
    super(server,self).__init__(parent)
    self.iconQDoneSignal = iconQDoneSignal
    self._context = zmq.Context()
    self._portServer = serverIPC
    self._portWorker = workerIPC

  def process(self, iconQ, iconQDoneSignal):
    setproctitle.setproctitle("server-worker-process")


    while(True):
      fileDets = iconQ.get()
      rbhus.debug.info(fileDets)
      fAbsPath = fileDets.absPath
      mimeType = fileDets.mimeType
      fLockPath = rbhus.dfl.LockFile(fAbsPath,timeout=0,expiry=30)
      fDir = os.path.dirname(fAbsPath)
      fName = os.path.basename(fAbsPath)
      fThumbzDbDir = os.path.join(fDir, ".thumbz.db")
      try:
        os.mkdir(fThumbzDbDir)
      except:
        pass
      fJson = os.path.join(fThumbzDbDir,fName + ".json")
      fThumbz = os.path.join(fThumbzDbDir,fName + ".png")
      fModifiedTime = os.path.getmtime(fAbsPath)
      # if (os.path.exists(fLockPath.lock_file)):
      #   if ((time.time() - os.path.getmtime(fLockPath.lock_file)) > 60):
      #     rbhus.debug.info("locked file for more than 1 minute : " + str(fAbsPath))

      if (os.path.exists(fThumbzDbDir)):

        if (os.path.exists(fJson)):
          try:
            with fLockPath:
              fThumbzDetails = jsonRead(fJson)
              if (fThumbzDetails[fName] < fModifiedTime):
                try:
                  thumbzCmd = rbhus.constantsPipe.mimeConvertCmds[mimeType].format(fAbsPath, fThumbz)
                except:
                  thumbzCmd = None
                if (thumbzCmd):
                  rbhus.debug.info(thumbzCmd)
                  p = subprocess.Popen(thumbzCmd, shell=True)
                  retcode = p.wait()
                  # print("generated thumb : "+ str(fThumbz))

                  if (retcode == 0):
                    fThumbzDetails = {fName: fModifiedTime}
                    jsonWrite(fJson, fThumbzDetails)
          except:
            rbhus.debug.info("file is updated by someone : " + str(fAbsPath))
        else:
          fThumbzDetails = {fName: fModifiedTime}
          jsonWrite(fJson, fThumbzDetails)
          try:
            thumbzCmd = rbhus.constantsPipe.mimeConvertCmds[mimeType].format(fAbsPath, fThumbz)
          except:
            thumbzCmd = None
          if (thumbzCmd):
            rbhus.debug.info(thumbzCmd)
            p = subprocess.Popen(thumbzCmd, shell=True)
            retcode = p.wait()

      fileDets.thumbFile = fThumbz
      fileDets.mainFile = fAbsPath
      fileDets.subPath = fDir
      iconQDoneSignal.put(fileDets)






  def _worker(self,worker_url,iconQ):

    worker_id = uuid.uuid4()
    setproctitle.setproctitle("server-worker : "+ str(worker_id))
    rbhus.debug.info("running worker")
    rbhus.debug.info (worker_url +" : "+ str(worker_id))
    context = zmq.Context()
    # Socket to talk to dispatcher
    socket = context.socket(zmq.REP)
    socket.poll(timeout=1)
    socket.connect(worker_url)


    while True:
      fileDets = socket.recv_pyobj()
      # setproctitle.setproctitle("server-worker : " + str(fileDets.absPath))
      socket.send_pyobj(fileDets)
      rbhus.debug.info("Filepath recieved : [ {0} ]".format(str(fileDets.absPath)))
      iconQ.put(fileDets)

  def run(self):
    rbhus.debug.info("server run")
    pool_size = 4
    worker_port = self._portWorker
    server_port = self._portServer
    url_worker = "ipc:///tmp/" + worker_port
    url_client = "ipc:///tmp/" + server_port
    clients = self._context.socket(zmq.ROUTER)
    try:
      clients.bind(url_client)
    except:
      rbhus.debug.info (sys.exc_info())
      self._context.term()
      sys.exit(1)

    # Socket to talk to workers
    workers = self._context.socket(zmq.DEALER)
    try:
      workers.bind(url_worker)
    except:
      rbhus.debug.info (sys.exc_info())
      self._context.term()
      sys.exit(1)


    iconQ = multiprocessing.Queue(pool_size)

    multiprocessing.Pool(processes=pool_size, initializer=self.process, initargs = (iconQ,self.iconQDoneSignal))
    # Launch pool of worker process
    multiprocessing.Pool(processes=pool_size, initializer=self._worker, initargs=(url_worker,iconQ, ))
    # p.daemon = False

    zmq.proxy(clients, workers)

    print("We never get here but clean up anyhow")
    try:
      clients.close()
      workers.close()
      self._context.term()
    except:
      print(sys.exc_info())
    # self.finished.emit() # dont enable this . this will simply emit finished twice .. !!!


class fileDirLoadedThread(QtCore.QThread):
  fileIcon = QtCore.pyqtSignal(object)
  iconProcessStarted = QtCore.pyqtSignal()
  def __init__(self, filesLoaded,pathSelected):
    super(fileDirLoadedThread, self).__init__()
    self._ip = 'localhost'
    self.filesLoaded = filesLoaded
    self._pleaseStop = False
    self.pathSelected = pathSelected
    global context
    self.socket = context.socket(zmq.REQ)
    self.socket.connect("ipc:///tmp/"+ serverIPC)
    # rbhus.debug.info("Sending request {0} ".format(fileDets))


  def pleaseStop(self):
    self._pleaseStop = True

  def run(self):
    for filePath in self.filesLoaded:
      if(self._pleaseStop):
        break
      if(os.path.isfile(filePath)):
        for mimeType in rbhus.constantsPipe.mimeTypes.keys():
          if (self._pleaseStop):
            break
          mimeExts = rbhus.constantsPipe.mimeTypes[mimeType]
          for mimeExt in mimeExts:
            if (self._pleaseStop):
              break


            if (filePath.endswith(mimeExt)):

              fSubPath = self.pathSelected

              if (not fSubPath):
                fSubPath = "-"


              fileDets = rbhus.utilsPipe.thumbz_db()
              fileDets.mainFile = filePath
              fileDets.absPath = filePath
              fileDets.subPath = fSubPath
              fileDets.mimeType = mimeType
              fileDets.mimeExt = mimeExt
              fAbsPath = fileDets.absPath
              fDir = os.path.dirname(fAbsPath)
              fName = os.path.basename(fAbsPath)
              fThumbzDbDir = os.path.join(fDir, ".thumbz.db")
              fThumbz = os.path.join(fThumbzDbDir, fName + ".png")
              fileDets.thumbFile = fThumbz



              try:
                self.startIconGen(fileDets)
                self.fileIcon.emit(fileDets)
              except:
                rbhus.debug.error(sys.exc_info())
              time.sleep(0.05)
    self.socket.close()
    # self.finished.emit() # dont enable this . this will simply emit finished twice .. !!!

  def startIconGen(self,fileDets):



    self.socket.send_pyobj(fileDets)
    # rbhus.debug.info("sending filepath")
    recvd_obj = self.socket.recv_pyobj()



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
  global fileThumbzWidget
  global  fileThumbzItems
  global fileIconThreadRunning
  global CUR_DIR_SELECTED



  pathSelected = modelDirs.filePath(idx)
  main_ui.labelFile.setText(str(pathSelected).replace(ROOTDIR,"-"))
  CUR_DIR_SELECTED = pathSelected
  if(fileIconThreadRunning):
    try:
      fileIconThreadRunning.disconnect()
      fileIconThreadRunning.pleaseStop()
      fileIconThreadRunning.wait()
      fileIconThreadRunning = None
    except:
      pass


  fileThumbzWidget.clear()
  fileThumbzItems.clear()
  main_ui.listFiles.clear()






  if(pathSelected == CUR_ROOTDIR_POINTER):

    fileGlob = glob.glob(ROOTDIR + os.sep + "*")
  else:
    fileGlob = glob.glob(pathSelected + os.sep + "*")
  try:
    fileGlob.remove("-")
  except:
    pass
  if(fileGlob):
    fileGlob.sort()
    fileIconThreadRunning = fileDirLoadedThread(fileGlob,pathSelected)
    fileIconThreadRunning.fileIcon.connect(lambda fileIconDets, pathSelected = pathSelected, main_ui=main_ui :fileIconActivate(fileIconDets,pathSelected,main_ui))
    # fileIconThreadRunning.finished.connect(lambda main_ui= main_ui : listFilesFinished(main_ui))
    fileIconThreadRunning.start()




def fileIconActivate(fileIconDets,pathSelected, main_ui):
  # print("recvd preview : "+ str(fileIconDets.subPath))
  global fileThumbzWidget
  global fileThumbzItems
  if(fileThumbzWidget.has_key(fileIconDets.mainFile)):
    imageWidgetUpdated(fileIconDets)
    return
  itemWidget = uic.loadUi(mediaThumbz_ui_file)
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
  fileThumbzWidget[fileIconDets.mainFile] = itemWidget
  fileThumbzItems[fileIconDets.mainFile] = item
  # print("thumbz added :: "+ fileIconDets.mainFile)



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
    return
  except:
    print("wtf :: "+ str(sys.exc_info()))


# def filesSelected(modelFiles, main_ui):
#   selectedIdx = main_ui.listFiles.selectedIndexes()
#   rbhus.debug.info(selectedIdx)
#   for idx in selectedIdx:
#     print("--------")
#     print(modelFiles.filePath(idx))

def popUpFolders(main_ui,pos):

  menu = QtWidgets.QMenu()

  ioMenu = QtWidgets.QMenu("IO")
  createFolderAction = ioMenu.addAction("new")
  deleteFolderAction = ioMenu.addAction("delete")

  menu.addMenu(ioMenu)
  action = menu.exec_(main_ui.treeDirs.mapToGlobal(pos))

  if (action == createFolderAction):
    createFolder(main_ui)
  if(action == deleteFolderAction):
    deleteFolder(main_ui)


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
    os.removedirs(CUR_DIR_SELECTED)
  except:
    msgBox = QtWidgets.QMessageBox(parent=main_ui.treeDirs)
    msgBox.adjustSize()
    msgBox.setIcon(QtWidgets.QMessageBox.Warning)
    msgBox.setText(str(sys.exc_info()))

    msgBox.exec_()





def popUpFiles(main_ui,pos):
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




  openWithCmdActions = {}
  try:
    selected = main_ui.listFiles.selectedItems()[0]
  except:
    selected = None
  if(selected):
    if(rbhus.constantsPipe.mimeTypesOpenCmds.has_key(selected.media.mimeType)):
      cmds = rbhus.constantsPipe.mimeTypesOpenCmds[selected.media.mimeType]["linux"]
      for cmd in cmds:
        if(rbhus.constantsPipe.mimeCmdsLinux.has_key(cmd)):
          openWithCmdActions[openMenu.addAction(cmd)] = rbhus.constantsPipe.mimeCmdsLinux[cmd]
        else:
          openWithCmdActions[openMenu.addAction(cmd)] = cmd



    ioCopyAction = ioMenu.addAction("copy")
    ioDeleteAction = ioMenu.addAction("delete")
    # ioDeleteAction.setEnabled(False)

    fileNameRenameAction = fileMenu.addAction("rename")
    fileImageCopyAction = fileMenu.addAction("copy to clipboard")
    # fileCopyPathAction

  ioPasteAction = ioMenu.addAction("paste")

  if(pasteUrls):
    ioPasteAction.setEnabled(True)
  else:
    ioPasteAction.setEnabled(False)




  menu.addMenu(openMenu)
  menu.addMenu(fileMenu)
  menu.addMenu(ioMenu)

  action = menu.exec_(main_ui.listFiles.mapToGlobal(pos))




  if(action in openWithCmdActions.keys()):
    runCmd = openWithCmdActions[action]
    try:
      openFile(main_ui,runCmd)
    except:
      rbhus.debug.error(sys.exc_info)

  if(action == ioPasteAction):
    pasteFilesFromClipboard(main_ui,pasteUrls)

  if(selected):
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
  selected = main_ui.listFiles.currentItem()
  print(selected.media.mainFile)
  print("cmd : "+ str(cmd))
  if(cmd.startswith("project_")):
    cmdToRun = rbhus.utilsPipe.openAssetCmd(assDets, selected.media.mainFile)
    print("command to run :"+ str(cmdToRun))
    if(cmdToRun):
      cmdFull = cmdToRun
    else:
      cmdFull = cmd.format(selected.media.mainFile)
  elif(cmd.startswith("system_")):
    import webbrowser
    webbrowser.open(selected.media.mainFile)
  else:
    cmdFull = cmd.format(selected.media.mainFile)
  subprocess.Popen(cmdFull,shell=True,stderr=subprocess.PIPE,stdout=subprocess.PIPE)
  # rbhus.debug.info(p.communicate())


  if(args.close):
    if(isCopying):
      isQuiting = True
    else:
      QApplication.quit()

def deleteFiles(main_ui):
  global fileThumbzWidget
  global CUR_DIR_SELECTED
  global fileIconThreadRunning
  selected = main_ui.listFiles.selectedItems()

  for item in selected:
    fileToDelete = item.media.mainFile
    if(os.path.exists(item.media.mainFile)):
      thrashPath  = os.path.join(rbhus.utilsPipe.rbhusTrash,assDets['assetId'])
      try:
        os.makedirs(thrashPath)
      except:
        rbhus.debug.warning(sys.exc_info())
      mvCmd = "mv "+ item.media.mainFile +" "+ thrashPath
      reply = QtWidgets.QMessageBox.question(main_ui.listFiles, "WARNING", "Do you want to delete the selected files?!!", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
      if(reply == QtWidgets.QMessageBox.Yes):
        os.system(mvCmd)

        fileThumbzWidget[item.media.mainFile].deleteLater()
        del fileThumbzWidget[item.media.mainFile]
        delIndex = main_ui.listFiles.indexFromItem(fileThumbzItems[item.media.mainFile])
        main_ui.listFiles.takeItem(delIndex.row())
        rbhus.utilsPipe.updateAssModifies(assDets['assetId'], "deleted : " + item.media.mainFile)


def tray_icon_change(icon_anim,tray_icon):
  tray_icon.setIcon(QtGui.QIcon(icon_anim.currentPixmap()))


def setToolTip(tray_icon,src,dest,main_ui):

  tray_icon.showMessage("COPYING",src +"->"+ dest)


def syncingDoneEvent(src,dest,main_ui):
  global CUR_DIR_SELECTED
  global fileIconThreadRunning
  if(not os.path.isdir(src)):
    fileGlob = [dest]
    fileIconThreadRunning = fileDirLoadedThread(fileGlob,CUR_DIR_SELECTED)
    fileIconThreadRunning.fileIcon.connect(lambda fileIconDets, pathSelected = CUR_DIR_SELECTED, main_ui=main_ui :fileIconActivate(fileIconDets,pathSelected,main_ui))
     # fileIconThreadRunning.finished.connect(lambda main_ui= main_ui : listFilesFinished(main_ui))
    fileIconThreadRunning.start()
    fileIconThreadRunning.wait()
    rbhus.debug.info("created ICON FOR : "+ dest)

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
  global fileIconThreadRunning
  global isCopying

  tray_icon_anim = QtGui.QMovie(busyIconGif)
  tray_icon_anim.start()

  tray_icon = QtWidgets.QSystemTrayIcon(QtGui.QIcon(busyIconGif), app)
  tray_icon_anim.frameChanged.connect(lambda frameNumber, icon_anim=tray_icon_anim, tray_icon=tray_icon: tray_icon_change(icon_anim, tray_icon))
  tray_icon.show()


  applyOption = QtCore.Qt.Unchecked
  rewriteReply = QtWidgets.QMessageBox.No
  fileParticles = {}

  for url in urls:
    # applyOptionLocal = False
    sourceFile = url.toLocalFile()
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
        print("skipping : "+ sourceFile)
        continue
      else:
        fileParticles[sourceFile] = destFile
    else:
      fileParticles[sourceFile] = destFile

  if (fileParticles):
    isCopying.append(1)
    sT = syncThread(app, fileParticles)
    sT.syncing.connect(lambda src, dest, tray_icon=tray_icon,main_ui=main_ui: setToolTip(tray_icon, src,dest,main_ui))
    sT.syncingDone.connect(lambda src, dest, main_ui=main_ui: syncingDoneEvent(src,dest,main_ui))
    sT.finished.connect(lambda tray_icon = tray_icon, tray_icon_anim= tray_icon_anim : copyingFinished(tray_icon,tray_icon_anim))
    sT.start()
  else:
    tray_icon_anim.disconnect()
    tray_icon_anim.deleteLater()
    tray_icon.deleteLater()




def copyToClipboard(main_ui):
  selected = main_ui.listFiles.selectedItems()
  urlList = []
  mimeData = QtCore.QMimeData()

  for x in selected:
    # if(os.path.exists("/usr/bin/thunar-no-more")):
    #   urlList.append(x.media.mainFile)
    # elif(os.path.exists("/usr/bin/dolphin-no-more")):
    urlList.append(QtCore.QUrl().fromLocalFile(x.media.mainFile))
    rbhus.utilsPipe.updateAssModifies(assDets['assetId'], "clipboard : " + x.media.mainFile)

  # if(os.path.exists("/usr/bin/thunar-no-more")):
  #   byteArray = QtCore.QByteArray("copy\n")
  #   for url in urlList:
  #     byteArray.append(url.toEncoded())
  #     byteArray.append("\n")
  #   mimeData.setData("x-special/gnome-copied-files",byteArray)
  # elif (os.path.exists("/usr/bin/dolphin-no-more")):
  mimeData.setUrls(urlList)

  QtWidgets.QApplication.clipboard().setMimeData(mimeData)


def copyImageToClipboard(main_ui):
  selected = main_ui.listFiles.currentItem()
  if(selected):
    fileSelected = selected.media.mainFile
    mimeType = selected.media.mimeType
    if(mimeType == "image"):
      pixMapToCopy = QtGui.QPixmap(selected.media.mainFile)
      QtWidgets.QApplication.clipboard().setPixmap(pixMapToCopy)



def fileRenameDialog(main_ui):
  global fileThumbzWidget

  selected = main_ui.listFiles.currentItem()
  dialog = QtWidgets.QInputDialog(main_ui.listFiles)
  dialog.setInputMode(QtWidgets.QInputDialog.TextInput)
  dialog.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,QtWidgets.QSizePolicy.MinimumExpanding)
  dialog.setWindowTitle("Rename Dialog")
  dialog.setLabelText("file:")
  (pathRoot , ext) = os.path.splitext(os.path.basename(selected.media.mainFile))
  # if(ext):
  dialog.setTextValue(pathRoot)
  # else:
  #   dialog.setTextValue(os.path.basename(selected.media.mainFile))
  dialog.adjustSize()
  dialog.resize(500,80)
  # dialog.adjustSize()

  dialog.exec_()
  fileRenamed  =  dialog.textValue() + ext
  newFile = os.path.join(selected.media.subPath,fileRenamed)
  copyStatus = QtCore.QFile().rename(selected.media.mainFile,newFile)
  print(newFile +" : "+ str(copyStatus))
  if(copyStatus):
    fileThumbzWidget[selected.media.mainFile].labelImageName.setText(os.path.basename(newFile))
    mainFileWidget = fileThumbzWidget[selected.media.mainFile]
    del(fileThumbzWidget[selected.media.mainFile])
    selected.media.mainFile = newFile
    fileThumbzWidget[selected.media.mainFile] = mainFileWidget
    rbhus.utilsPipe.updateAssModifies(assDets['assetId'], "renamed : " + selected.media.mainFile + " -> " + newFile)
    try:
      modifiedT = os.path.getmtime(selected.media.mainFile)
    except:
      modifiedT = 0
    # print(time.ctime(modifiedT))
    fileThumbzWidget[selected.media.mainFile].setToolTip("fileName: " + os.path.basename(selected.media.mainFile) + "\nmodified : " + str(time.ctime(modifiedT)))



def mainGui(main_ui):
  iconQDoneSignal = multiprocessing.Queue(1)
  iconServer = server(iconQDoneSignal=iconQDoneSignal,parent=main_ui)
  iconServer.start()
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




  curRootIdx = modelDirs.index(CUR_ROOTDIR_POINTER)
  main_ui.treeDirs.setCurrentIndex(curRootIdx)
  iconEventEater = getIconDoneEvent(iconQDoneSignal,parent=main_ui)
  iconEventEater.iconGenerated.connect(imageWidgetUpdated)
  iconEventEater.start()



  main_ui.treeDirs.clicked.connect(lambda idnx, modelDirs=modelDirs, main_ui = main_ui : dirSelected(idnx, modelDirs, main_ui))
  # main_ui.listFiles.clicked.connect(lambda idnx, main_ui = main_ui :filesSelected(modelFiles,main_ui))

  main_ui.listFiles.customContextMenuRequested.connect(lambda pos, main_ui = main_ui: popUpFiles(main_ui, pos))
  main_ui.treeDirs.customContextMenuRequested.connect(lambda pos, main_ui = main_ui: popUpFolders(main_ui, pos))

  main_ui.show()
  main_ui.update()
  dirSelected(curRootIdx, modelDirs, main_ui)






if __name__ == '__main__':
  app = QApplication(sys.argv)
  main_ui = uic.loadUi(main_ui_file)
  mainGui(main_ui)
  # ex = App()
  sys.exit(app.exec_())
