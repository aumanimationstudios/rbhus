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
import pathlib2
import tempfile

from PyQt5.QtWidgets import QApplication, QFileSystemModel, QListWidgetItem
from PyQt5 import QtCore, uic, QtGui, QtWidgets



# sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-1]))
progPath = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-3])
rbhusPath = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-4])


print(rbhusPath)
sys.path.append(rbhusPath)
import rbhus.utilsPipe
import rbhus.constantsPipe
import rbhus.dfl
import rbhus.debug


main_ui_file = os.path.join(rbhusPath, "tests", "qt5", "treeViewTest", "main.ui")

ROOTDIR = sys.argv[1]
CUR_ROOTDIR_POINTER = os.path.join(ROOTDIR,"-")

CUR_DIR_SELECTED = None
thumbsDbDir = "/crap/LOCAL.crap/.thumbz.db"
currentModelFiles = None
currentIconProvider = None


iconGenerateThreadCurrent = None

context = zmq.Context()

serverIPC = str(uuid.uuid4())
workerIPC = str(uuid.uuid4())



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
  def __init__(self,*arg):
    super(IconProvider, self).__init__(*arg)
    self.setOptions(QtWidgets.QFileIconProvider.DontUseCustomDirectoryIcons)

  def icon(self, fileInfo):
    filePath = fileInfo.absoluteFilePath()
    pathSelected = os.path.relpath(fileInfo.absolutePath(),ROOTDIR)
    if(os.path.isfile(filePath)):
      for mimeType in rbhus.constantsPipe.mimeTypes.keys():
        mimeExts = rbhus.constantsPipe.mimeTypes[mimeType]
        for mimeExt in mimeExts:

          if (filePath.endswith(mimeExt)):
            fSubPath = pathSelected
            if (not fSubPath):
              fSubPath = "-"


            fileDets = rbhus.utilsPipe.thumbz_db()
            fileDets.mainFile = filePath
            fileDets.absPath = filePath
            fileDets.subPath = fSubPath
            fileDets.mimeType = mimeType
            fileDets.mimeExt = mimeExt
            fAbsPath = fileDets.absPath
            fName = os.path.basename(fAbsPath)
            fThumbz = os.path.join(thumbsDbDir,pathSelected, fName + ".png")
            fJson = os.path.join(thumbsDbDir,pathSelected, fName + ".json")
            fileDets.thumbFile = fThumbz
            fileDets.fileName = fName
            fileDets.jsonFile = fJson





            # rbhus.debug.info(fileDets.thumbFile)
            # self.iconGenerate(fileDets)
            if(os.path.exists(fThumbz)):
              return QtGui.QIcon(fileDets.thumbFile)
            else:
              return QtWidgets.QFileIconProvider.icon(self, fileInfo)
      else:
        return QtWidgets.QFileIconProvider.icon(self, fileInfo)
    else:
      return QtWidgets.QFileIconProvider.icon(self, fileInfo)


  # def getIcon(self):
  #   return None




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
      rbhus.debug.debug(fileDets)
      fAbsPath = fileDets.absPath
      mimeType = fileDets.mimeType
      fThumbzDbDir = os.path.dirname(fileDets.thumbFile)
      fName = fileDets.fileName
      fThumbz = fileDets.thumbFile
      fJson = fileDets.jsonFile
      fLockPath = rbhus.dfl.LockFile(fThumbz, timeout=0, expiry=30)
      if (not os.path.exists(fThumbzDbDir)):
        try:
          os.makedirs(fThumbzDbDir,0777)
        except:
          pass
      fModifiedTime = os.path.getmtime(fAbsPath)
      # if (os.path.exists(fLockPath.lock_file)):
      #   if ((time.time() - os.path.getmtime(fLockPath.lock_file)) > 60):
      #     rbhus.debug.debug("locked file for more than 1 minute : " + str(fAbsPath))

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
                  rbhus.debug.debug(thumbzCmd)
                  p = subprocess.Popen(thumbzCmd, shell=True)
                  retcode = p.wait()
                  # print("generated thumb : "+ str(fThumbz))

                  if (retcode == 0):
                    fThumbzDetails = {fName: fModifiedTime}
                    jsonWrite(fJson, fThumbzDetails)
          except:
            rbhus.debug.debug("file is updated by someone : " + str(fAbsPath))
        else:
          fThumbzDetails = {fName: fModifiedTime}
          jsonWrite(fJson, fThumbzDetails)
          try:
            thumbzCmd = rbhus.constantsPipe.mimeConvertCmds[mimeType].format(fAbsPath, fThumbz)
          except:
            thumbzCmd = None
          if (thumbzCmd):
            rbhus.debug.debug(thumbzCmd)
            p = subprocess.Popen(thumbzCmd, shell=True)
            retcode = p.wait()

      iconQDoneSignal.put(fileDets)






  def _worker(self,worker_url,iconQ):

    worker_id = uuid.uuid4()
    setproctitle.setproctitle("server-worker : "+ str(worker_id))
    rbhus.debug.debug("running worker")
    rbhus.debug.debug (worker_url +" : "+ str(worker_id))
    context = zmq.Context()
    # Socket to talk to dispatcher
    socket = context.socket(zmq.REP)
    socket.poll(timeout=1)
    socket.connect(worker_url)


    while True:
      fileDets = socket.recv_pyobj()
      # setproctitle.setproctitle("server-worker : " + str(fileDets.absPath))
      socket.send_pyobj(fileDets)
      rbhus.debug.debug("Filepath recieved : [ {0} ]".format(str(fileDets.absPath)))
      iconQ.put(fileDets)

  def run(self):
    rbhus.debug.debug("server run")
    pool_size = 4
    worker_port = self._portWorker
    server_port = self._portServer
    url_worker = "ipc:///tmp/" + worker_port
    url_client = "ipc:///tmp/" + server_port
    clients = self._context.socket(zmq.ROUTER)
    try:
      clients.bind(url_client)
    except:
      rbhus.debug.debug (sys.exc_info())
      self._context.term()
      sys.exit(1)

    # Socket to talk to workers
    workers = self._context.socket(zmq.DEALER)
    try:
      workers.bind(url_worker)
    except:
      rbhus.debug.debug (sys.exc_info())
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




class modelFileClass(QFileSystemModel):
  pass



class FSM(QFileSystemModel):

  def __init__(self,**kwargs):
    super(FSM, self).__init__(**kwargs)




  def canFetchMore(self,idx):
    if (self.filePath(idx) == CUR_ROOTDIR_POINTER):
      rootIdx = self.index(ROOTDIR)
      return super(FSM, self).fetchMore(idx)
    elif (self.filePath(idx).endswith(".thumbz.db")):
      return False
    else:
      return super(FSM, self).canFetchMore(idx)

  # def rowCount(self,idx):
  #   rbhus.debug.debug(idx.row())
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


class iconGenerateThread(QtCore.QThread):
  def __init__(self,parent=None):
    super(iconGenerateThread, self).__init__(parent=parent)
    global context
    global CUR_DIR_SELECTED
    global ROOTDIR

    self.rootdir = ROOTDIR
    self.currentDirSelected = str(CUR_DIR_SELECTED)

    self.socket = context.socket(zmq.REQ)
    self.socket.connect("ipc:///tmp/"+ serverIPC)
    self._pleaseStop = False

  def pleaseStop(self):
    self._pleaseStop = True

  def run(self):
    files = glob.glob(os.path.join(self.currentDirSelected,"*"))
    for filePath in files:
      if(self._pleaseStop):
        break
      if(os.path.isfile(filePath)):
        pathSelected = os.path.relpath(os.path.abspath(os.path.dirname(filePath)), self.rootdir)
        # rbhus.debug.info(pathSelected)
        for mimeType in rbhus.constantsPipe.mimeTypes.keys():
          if (self._pleaseStop):
            break
          mimeExts = rbhus.constantsPipe.mimeTypes[mimeType]
          for mimeExt in mimeExts:
            if (self._pleaseStop):
              break
            if (filePath.endswith(mimeExt)):
              fSubPath = pathSelected
              if (not fSubPath):
                fSubPath = "-"
              if (self._pleaseStop):
                break

              fileDets = rbhus.utilsPipe.thumbz_db()
              fileDets.mainFile = filePath
              fileDets.absPath = filePath
              fileDets.subPath = pathSelected
              fileDets.mimeType = mimeType
              fileDets.mimeExt = mimeExt
              fAbsPath = fileDets.absPath
              fName = os.path.basename(fAbsPath)
              fThumbz = os.path.join(thumbsDbDir, pathSelected, fName + ".png")
              fJson = os.path.join(thumbsDbDir, pathSelected, fName + ".json")
              fileDets.thumbFile = fThumbz
              fileDets.fileName = fName
              fileDets.jsonFile = fJson
              self.generate(fileDets)
              time.sleep(0.01)

    self.socket.close()


  def generate(self,fileDets):

    self.socket.send_pyobj(fileDets)
    # rbhus.debug.debug("sending filepath")
    recvd_obj = self.socket.recv_pyobj()







def iconGenerate(main_ui):
  global CUR_DIR_SELECTED
  global iconGenerateThreadCurrent
  if(iconGenerateThreadCurrent):
    iconGenerateThreadCurrent.pleaseStop()
    iconGenerateThreadCurrent.wait()

    try:
      iconGenerateThreadCurrent.disconnect()
    except:
      rbhus.debug.debug(iconGenerateThreadCurrent)
    try:
      iconGenerateThreadCurrent.deleteLater()
    except:
      rbhus.debug.debug(sys.exc_info())

  iconGenerateThreadCurrent = iconGenerateThread()
  iconGenerateThreadCurrent.finished.connect(lambda main_ui=main_ui:finishedIconGenerate(main_ui))
  iconGenerateThreadCurrent.start()



def finishedIconGenerate(main_ui):
  global CUR_DIR_SELECTED
  fileIconProvider = IconProvider()
  # currentIconProvider = fileIconProvider
  main_ui.tableFiles.model().setIconProvider(fileIconProvider)




def imageWidgetUpdated(fileDets,modelDirs,main_ui):
  global CUR_DIR_SELECTED

  fileSelectedIdx = main_ui.tableFiles.model().index(fileDets.mainFile)
  icon = QtGui.QIcon(fileDets.thumbFile)
  main_ui.tableFiles.model().setData(fileSelectedIdx,icon,QFileSystemModel.FileIconRole)
  # main_ui.tableFiles.model().endResetModel()
  # main_ui.tableFiles.model().setRootPath(CUR_DIR_SELECTED)
  #
  
  # fileIconProvider = IconProvider()
  # currentIconProvider = fileIconProvider
  # main_ui.tableFiles.model().setIconProvider(fileIconProvider)
  # if (main_ui.radioDetail.isChecked()):
  #   rootIdx = main_ui.tableFiles.model().index(CUR_DIR_SELECTED)
  #   main_ui.tableFiles.setRootIndex(rootIdx)
  #   main_ui.tableFiles.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
  # else:
  #   rootIdx = main_ui.listFiles.model().index(CUR_DIR_SELECTED)
  #   main_ui.listFiles.setRootIndex(rootIdx)
  main_ui.tableFiles.update()
  # print("updated : "+ str(fileDets.thumbFile))





def dirSelected(idx, modelDirs, main_ui, passive=False):
  global CUR_DIR_SELECTED

  if(passive == False):
    CUR_DIR_SELECTED = modelDirs.filePath(idx)

  modelFiles = modelFileClass()
  modelFiles.setFilter(QtCore.QDir.Files | QtCore.QDir.NoDotAndDotDot)
  fileIconProvider = IconProvider()
  fileIconProvider.setOptions(QtWidgets.QFileIconProvider.DontUseCustomDirectoryIcons)
  modelFiles.setIconProvider(fileIconProvider)
  main_ui.tableFiles.setModel(modelFiles)
  main_ui.listFiles.setModel(modelFiles)


  modelFiles.setRootPath(CUR_DIR_SELECTED)
  # fileIconProvider = IconProvider()
  # modelFiles.setIconProvider(fileIconProvider)


  if(main_ui.radioDetail.isChecked()):
    rootIdx = main_ui.tableFiles.model().index(CUR_DIR_SELECTED)
    main_ui.tableFiles.setRootIndex(rootIdx)
    main_ui.tableFiles.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
  else:
    rootIdx = main_ui.listFiles.model().index(CUR_DIR_SELECTED)
    main_ui.listFiles.setRootIndex(rootIdx)

  iconGenerate(main_ui)

    # if(currentModelFiles):
    #   currentModelFiles.deleteLater()

  # currentIconProvider = fileIconProvider



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



def togleFileView(modelDirs, main_ui):
  global CUR_DIR_SELECTED

  if(main_ui.radioDetail.isChecked()):
    main_ui.listFiles.hide()
    main_ui.tableFiles.setEnabled(True)
    main_ui.listFiles.setEnabled(False)

    dirSelected(None, modelDirs, main_ui, passive=True)
    main_ui.tableFiles.show()
  else:
    main_ui.tableFiles.hide()
    main_ui.tableFiles.setEnabled(False)
    main_ui.listFiles.setEnabled(True)

    dirSelected(None, modelDirs, main_ui, passive=True)
    main_ui.listFiles.show()


def mainGui(main_ui):
  iconQDoneSignal = multiprocessing.Queue(1)
  iconServer = server(iconQDoneSignal=iconQDoneSignal,parent=main_ui)
  iconServer.start()


  main_ui.splitter.setStretchFactor(1,10)

  modelDirs = FSM()
  modelDirs.setRootPath(ROOTDIR)
  modelDirs.setFilter(QtCore.QDir.Dirs | QtCore.QDir.NoDotAndDotDot)
  main_ui.treeDirs.setModel(modelDirs)
  rootIdx = modelDirs.index(ROOTDIR)
  main_ui.treeDirs.setRootIndex(rootIdx)

  modelDirs.mkdir(rootIdx, "-")
  curRootIdx = modelDirs.index(CUR_ROOTDIR_POINTER)
  main_ui.treeDirs.setCurrentIndex(curRootIdx)

  main_ui.treeDirs.hideColumn(1)
  main_ui.treeDirs.hideColumn(2)
  main_ui.treeDirs.hideColumn(3)





  main_ui.treeDirs.clicked.connect(lambda idnx, modelDirs=modelDirs,  main_ui=main_ui: dirSelected(idnx, modelDirs, main_ui))
  togleFileView(modelDirs, main_ui)

  main_ui.radioDetail.clicked.connect(lambda click, modelDirs=modelDirs,  main_ui=main_ui: togleFileView(modelDirs, main_ui))
  main_ui.radioIcon.clicked.connect(lambda click, modelDirs=modelDirs,  main_ui=main_ui: togleFileView(modelDirs, main_ui))

  main_ui.treeDirs.customContextMenuRequested.connect(lambda pos, main_ui=main_ui: popUpFolders(main_ui, pos))

  dirSelected(curRootIdx, modelDirs, main_ui)
  iconEventEater = getIconDoneEvent(iconQDoneSignal,parent=main_ui)
  iconEventEater.iconGenerated.connect(lambda fileDets , modelDirs=modelDirs, main_ui=main_ui: imageWidgetUpdated(fileDets,modelDirs,main_ui))
  iconEventEater.start()

  main_ui.show()








if __name__ == '__main__':
  app = QApplication(sys.argv)
  main_ui = uic.loadUi(main_ui_file)
  mainGui(main_ui)
  # ex = App()
  sys.exit(app.exec_())
