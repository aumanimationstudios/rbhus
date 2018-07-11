#!/usr/bin/env python2
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"




import sys
import os
import zmq
import uuid
import setproctitle
import multiprocessing
import subprocess
import time

# sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-1]))
progPath = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-1])
rbhusPath = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2])
sys.path.append(rbhusPath)
import rbhus.debug
import rbhus.constantsPipe
import rbhus.utilsPipe
import rbhus.dfl

main_ui_file = os.path.join(rbhusPath, "rbhusUI", "lib", "qt5", "folderManager", "main.ui")
rbhus.debug.info(main_ui_file)


import os
import simplejson
from PyQt5.QtWidgets import QApplication, QFileSystemModel, QTreeView, QWidget, QVBoxLayout, QFileIconProvider
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore, uic, QtGui




ROOTDIR = os.path.abspath(sys.argv[1])
CUR_ROOTDIR_POINTER = os.path.join(ROOTDIR,"-")

fileDetsDict = {}
fileIconThreads = {}


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



class fileIconProvider(QFileIconProvider):

  def __init__(self):
    super(fileIconProvider,self).__init__()
    self.mimeDatabase = QtCore.QMimeDatabase()

  def icon(self, info):
    mimeType = self.mimeDatabase.mimeTypeForFile(info)
    rbhus.debug.info("in icon : "+ str(info.absoluteFilePath()) + " : "+ mimeType.iconName())
    fAbsPath = info.absoluteFilePath()
    fDir = os.path.dirname(fAbsPath)
    fName = os.path.basename(fAbsPath)
    fThumbzDbDir = os.path.join(fDir, ".thumbz.db")
    fThumbz = os.path.join(fThumbzDbDir, fName + ".png")
    if(os.path.exists(fThumbz)):
      # rbhus.debug.info("THERT ID THUIMBS")
      return QtGui.QIcon(fThumbz)
    else:
      return QtGui.QIcon.fromTheme(mimeType.iconName())


class server(QtCore.QThread):
  def __init__(self,parent=None):

    self._context = zmq.Context()
    self._portServer = 55555
    self._portWorker = 55999
    super(server,self).__init__(parent)

  def process(self, iconQ):
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
                  print("generated thumb : "+ str(fThumbz))
                  # while(retcode == None):
                  #   retcode = p.poll()
                  #   time.sleep(0.01)

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

    # return (fileDets)




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
      toSend = {"status":"ack"}
      socket.send_pyobj(toSend)
      rbhus.debug.info("Filepath recieved : [ {0} ]".format(str(fileDets.absPath)))
      setproctitle.setproctitle("server-worker : "+ str(fileDets.absPath))
      iconQ.put(fileDets)

  def run(self):
    rbhus.debug.info("server run")
    pool_size = 4
    worker_port = self._portWorker
    server_port = self._portServer
    url_worker = "tcp://127.0.0.1:{0}".format(worker_port)
    url_client = "tcp://*:{0}".format(server_port)
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


    iconQ = multiprocessing.Queue(10000)

    multiprocessing.Pool(processes=pool_size*2, initializer=self.process, initargs = (iconQ,))
    # Launch pool of worker process
    multiprocessing.Pool(processes=pool_size, initializer=self._worker, initargs=(url_worker,iconQ, ))
    # p.daemon = False

    zmq.proxy(clients, workers)

    # We never get here but clean up anyhow
    clients.close()
    workers.close()
    self._context.term()
    self.finished.emit()

context = zmq.Context()

class fileDirLoadedThread(QtCore.QThread):
  fileIcon = QtCore.pyqtSignal(object)
  def __init__(self, fileDets):
    super(fileDirLoadedThread, self).__init__()
    self._ip = 'localhost'
    self._port = 55555
    self.fileDets = fileDets


  def process(self, recvd_obj):
    rbhus.debug.info(recvd_obj)
    self.fileIcon.emit(recvd_obj)
    return

  def run(self):
    global context
    rbhus.debug.info("running client ")
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://{0}:{1}".format(self._ip, self._port))
    # socket.poll(timeout=1)
    # poller = zmq.Poller()
    # poller.register(socket, zmq.POLLIN)
    rbhus.debug.info("Sending request {0} ".format(self.fileDets))

    socket.send_pyobj(self.fileDets)
    rbhus.debug.info("sending filepath")
    # while(True):
    #   sockets = dict(poller.poll(10000))
    rbhus.debug.info("trying to recv icon")
    # try:
    # recvd_obj = socket.recv_pyobj()
    print(recvd_obj)
    #   print("recieved obj : " + str(recvd_obj))
    #   self.process(recvd_obj)
    #   # rbhus.debug.info("Received reply %s : %s [ %s ]" % ()
    # except:
    #   rbhus.debug.info(sys.exc_info())

    # if(sockets):
    #   for s in sockets.keys():
    #     if(sockets[s] == zmq.POLLIN):
    #       try:
    #         recvd_obj = s.recv_pyobj()
    #         print("recieved obj : " + str(recvd_obj))
    #         self.process(recvd_obj)
    #         # rbhus.debug.info("Received reply %s : %s [ %s ]" % ()
    #       except:
    #         rbhus.debug.info (sys.exc_info())
    #       break
    #   break
    # rbhus.debug.info ("Reciever Timeout error : Check if the server is running")



    socket.close()
    # context.term()
    self.finished.emit()




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
    
  # def data(self,idx,role):
  #   if(idx.isValid() and role == QtCore.Qt.DecorationRole):
  #     fAbsPath = self.filePath(idx)
  #
  #
  #     if(os.path.isdir(fAbsPath)):
  #       return super(FSM, self).data(idx, role)
  #     else:
  #       try:
  #         fDir = os.path.dirname(fAbsPath)
  #         fName = os.path.basename(fAbsPath)
  #         fThumbzDbDir = os.path.join(fDir, ".thumbz.db")
  #         fThumbz = os.path.join(fThumbzDbDir, fName + ".png")
  #
  #         if(fThumbz):
  #           if(os.path.exists(fThumbz)):
  #             rbhus.debug.info("DATA : thumbfile : "+ fThumbz)
  #             return QtGui.QIcon(QtGui.QPixmap(fThumbz))
  #       except:
  #         return super(FSM, self).data(idx, role)
  #   else:
  #     return super(FSM, self).data(idx,role)










def dirSelected(idx, modelDirs, modelFiles, main_ui):
  pathSelected = modelDirs.filePath(idx)
  if(pathSelected == CUR_ROOTDIR_POINTER):

    modelFiles.setRootPath(ROOTDIR)
    rootFilesIdx = modelFiles.index(ROOTDIR)
  else:
    modelFiles.setRootPath(pathSelected)
    rootFilesIdx = modelFiles.index(pathSelected)
  main_ui.listFiles.setRootIndex(rootFilesIdx)
  # rows = modelFiles.rowCount(rootFilesIdx)
  # rbhus.debug.info("files : "+ str(rows))
  # for x in range(0,rows):
  #   idx = modelFiles.index(x,0,rootFilesIdx)
  #   rbhus.debug.info(modelFiles.filePath(idx))


def fileRootPathChanged(pathLoaded, modelFiles, main_ui, timer):
  try:
    modelFiles.directoryLoaded.disconnect()
  except:
    print(sys.exc_info())


  modelFiles.directoryLoaded.connect(lambda changedPath, modelFiles=modelFiles, main_ui=main_ui, timer = timer: filesDirLoadedThread(changedPath, modelFiles, main_ui, timer))

def filesDirLoadedThread(pathLoaded, modelFiles, main_ui, timer):
  if (timer.isActive()):
    timer.stop()

  try:
    timer.disconnect()
  except:
    print(sys.exc_info())

  timer.timeout.connect(lambda changedPath = pathLoaded, modelFiles=modelFiles, main_ui=main_ui, timer = timer: filesDirLoaded(changedPath, modelFiles, main_ui, timer))
  timer.start(3000)

def filesDirLoaded(pathLoaded, modelFiles, main_ui, timer):
  print("dir loaded : "+ str(pathLoaded))
  try:
    modelFiles.directoryLoaded.disconnect()
  except:
    print(sys.exc_info())
  try:
    timer.stop()
  except:
    print(sys.exc_info())
  rootFilesIdx = modelFiles.index(pathLoaded)
  main_ui.listFiles.setRootIndex(rootFilesIdx)
  rows = modelFiles.rowCount(rootFilesIdx)
  rbhus.debug.info("files : "+ str(rows))
  for x in range(0,rows):
    idx = modelFiles.index(x,0,rootFilesIdx)
    filePath = modelFiles.filePath(idx)
    for mimeType in rbhus.constantsPipe.mimeTypes.keys():
      mimeExts =  rbhus.constantsPipe.mimeTypes[mimeType]
      for mimeExt in mimeExts:
        if(filePath.endswith(mimeExt)):
          fileDets = rbhus.utilsPipe.thumbz_db()
          fileDets.absPath = filePath

          fileDets.mimeType = mimeType
          fileDets.mimeExt = mimeExt

          fileIconThreadStart(fileDets, modelFiles)

  # map(lambda filePath, modelFIles = modelFiles : fileIconThreadStart(filePath,modelFiles), filePaths)


def fileIconThreadStart(fileDets, modelFiles):
  # pass
  # context = zmq.Context()
  global context
  socket = context.socket(zmq.REQ)
  socket.connect("tcp://{0}:{1}".format("localhost", "55555"))
  rbhus.debug.info("Sending request {0} ".format(fileDets))

  socket.send_pyobj(fileDets)
  rbhus.debug.info("sending filepath")
  rbhus.debug.info("trying to recv icon")
  recvd_obj = socket.recv_pyobj()
  socket.close()
  # context.term()
  # print(recvd_obj)


def fileIconThreadsClean(filePath):
  global fileIconThreads
  print("cleaning : "+ filePath)
  try:
    del(fileIconThreads[filePath])
  except:
    rbhus.debug.error(sys.exc_info())


def fileIconActivate(fileIconDets):
  print("recvd preview : "+ str(fileIconDets.thumbFile))
  global fileIconThreads
  fileIconThreads[fileIconDets.absPath] = fileIconDets


def filesSelected(modelFiles, main_ui):
  selectedIdx = main_ui.listFiles.selectedIndexes()
  rbhus.debug.info(selectedIdx)
  for idx in selectedIdx:
    print("--------")
    print(modelFiles.filePath(idx))


def mainGui(main_ui):
  iconServer = server()
  iconServer.start()
  # iconReqThreadPool = QtCore.QThreadPool()
  # iconReqThreadPool.setMaxThreadCount(2)
  # rbhus.debug.info("max thread count = " + str(iconReqThreadPool.maxThreadCount()))
  main_ui.setWindowTitle("Ass Folds")

  fileDirTimer = QtCore.QTimer()

  modelFiles = FSM()
  fileIcons = fileIconProvider()
  modelFiles.setFilter(QtCore.QDir.Files | QtCore.QDir.NoDotAndDotDot)
  modelFiles.setRootPath(ROOTDIR)
  modelFiles.setIconProvider(fileIcons)

  main_ui.listFiles.setModel(modelFiles)

  modelFiles.rootPathChanged.connect(lambda changedPath, modelFiles = modelFiles, main_ui = main_ui, timer = fileDirTimer  : fileRootPathChanged(changedPath, modelFiles, main_ui, timer))

  modelDirs = FSM()
  modelDirs.setFilter(QtCore.QDir.Dirs | QtCore.QDir.NoDotAndDotDot)
  modelDirs.setRootPath(ROOTDIR)
  main_ui.treeDirs.setModel(modelDirs)



  main_ui.treeDirs.hideColumn(1)
  main_ui.treeDirs.hideColumn(2)
  main_ui.treeDirs.hideColumn(3)

  rootIdx = modelDirs.index(ROOTDIR)
  main_ui.treeDirs.setRootIndex(rootIdx)
  modelDirs.mkdir(rootIdx,"-")



  curRootIdx = modelDirs.index(CUR_ROOTDIR_POINTER)
  main_ui.treeDirs.setCurrentIndex(curRootIdx)

  rootFilesIdx = modelFiles.index(ROOTDIR)
  main_ui.listFiles.setRootIndex(rootFilesIdx)

  # main_ui.listFiles.hideColumn(1)
  # main_ui.listFiles.hideColumn(2)
  # main_ui.listFiles.hideColumn(3)



  main_ui.treeDirs.clicked.connect(lambda idnx, modelDirs=modelDirs, modelFiles = modelFiles ,main_ui = main_ui :dirSelected(idnx, modelDirs, modelFiles, main_ui))
  main_ui.listFiles.clicked.connect(lambda idnx, modelFiles = modelFiles, main_ui = main_ui :filesSelected(modelFiles,main_ui))


  main_ui.show()






if __name__ == '__main__':
  app = QApplication(sys.argv)
  main_ui = uic.loadUi(main_ui_file)
  mainGui(main_ui)
  # ex = App()
  sys.exit(app.exec_())