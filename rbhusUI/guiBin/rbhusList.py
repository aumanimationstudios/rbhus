#!/usr/bin/env python3
from PyQt5 import QtWidgets, QtCore, QtGui, uic
import glob
import os
import sys
import socket
import time
import subprocess
import re

base_dir = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-3])
sys.path.append(base_dir)
rbhus_dir = os.path.join(base_dir,"rbhus")

import rbhus.debug as debug

main_ui_file = os.path.join(base_dir, "rbhusUI", "lib", "rbhusListMod.ui")

dirSelf = os.path.dirname(os.path.realpath(__file__))
debug.info(dirSelf)
sys.path.append(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep) + os.sep + "lib")

toolsdir = dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep + "tools" + os.sep + "rbhus"

rEc = "rbhusEdit.py"
rEcM = "rbhusEditMulti.py"
rSubmit = "rbhusSubmit.py"

editTaskCmd = dirSelf.rstrip(os.sep) + os.sep + rEc
editTaskCmd = editTaskCmd.replace("\\","/")

editTaskMultiCmd = dirSelf.rstrip(os.sep) + os.sep + rEcM
editTaskMultiCmd = editTaskMultiCmd.replace("\\","/")

submitCmd = dirSelf.rstrip(os.sep) + os.sep + rSubmit
submitCmd = submitCmd.replace("\\","/")

exr2pngCmd = toolsdir + os.sep + "convert_exr_png.py"
png2flvCmd = toolsdir + os.sep + "convert_png_flv.py"
png2mp4Cmd = toolsdir + os.sep + "convert_png_mp4.py"
exr2rleCmd = toolsdir + os.sep + "convert_exr_mov_rle.py"
png2rleCmd = toolsdir + os.sep + "convert_png_mov_rle.py"

debug.info (editTaskCmd)
import rbhusListMod
debug.info(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")
sys.path.append(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")
import db
import constants
import auth
import dbRbhus
import utilsPipe
import utils as rUtils
import simplejson

app = None

try:
  _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
  _fromUtf8 = lambda s: s


def str_convert(text):
  if isinstance(text, bytes):
    return str(text, 'utf-8')
  return str(text)


username = None
userProjIds = []
try:
  username = os.environ['rbhus_acl_user'].rstrip().lstrip()
except:
  pass
try:
  userProjIds = os.environ['rbhus_acl_projIds'].split()
except:
  pass

taskThreads = []
frameThreads = []
sFrames = ()

authL = auth.login()
colNamesTask = ["id","fileName","fRange","resolution","priority","fastAssign","user","outDir","hostGroups","afterTasks","submitTime","doneTime","afterTime","status"]
colNamesFrames = ["id","frameId","hostName","ram","sTime","eTime","runCount","status","fThreads","efficiency"]
colNamesFramesXtra = ["timeTaken"]
colNamesTaskXtra = ["pending"]

selectedTaskList = []

timer = QtCore.QTimer()
timerFramesRefresh = QtCore.QTimer()


class ImagePlayer(QtWidgets.QWidget):
  def __init__(self, filename, parent):
    super(ImagePlayer,self).__init__(parent)
    self.parent = parent

    # Load the file into a QMovie
    self.movie = QtGui.QMovie(filename, QtCore.QByteArray(), parent)
    self.newSize = QtCore.QSize(100,100)
    self.movie.setScaledSize(self.newSize)

    self.movie_screen = QtWidgets.QLabel()
    self.movie_screen.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
    self.movie_screen.setAlignment(QtCore.Qt.AlignCenter)

    # Add the QMovie object to the label
    self.movie.setCacheMode(QtGui.QMovie.CacheAll)
    self.movie.setSpeed(100)
    self.movie_screen.setMovie(self.movie)


    # Create the layout
    main_layout = QtWidgets.QVBoxLayout()
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



# class Ui_Form(rbhusListMod.Ui_mainRbhusList):
def mainGui(main_ui):
  # rbhusListMod.Ui_mainRbhusList.setupUi(self,Form)

  # username = None
  # userProjIds = []
  # try:
  #   username = os.environ['rbhus_acl_user'].rstrip().lstrip()
  # except:
  #   pass
  # try:
  #   userProjIds = os.environ['rbhus_acl_projIds'].split()
  # except:
  #   pass

  # self.form = Form




  icon = QtGui.QIcon()
  iconRefresh = QtGui.QIcon()
  iconTime = QtGui.QIcon()
  iconDate = QtGui.QIcon()
  iconTime.addPixmap(QtGui.QPixmap(str_convert(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/ic_action_time.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
  iconDate.addPixmap(QtGui.QPixmap(str_convert(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/ic_action_go_to_today.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
  iconRefresh.addPixmap(QtGui.QPixmap(str_convert(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/ic_action_refresh.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
  main_ui.taskRefresh.setIcon(iconRefresh)
  main_ui.framesRefresh.setIcon(iconRefresh)
  main_ui.checkRefresh.setIcon(iconTime)
  main_ui.checkDateTask.setIcon(iconDate)
  icon.addPixmap(QtGui.QPixmap(str_convert(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/rbhus.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
  main_ui.setWindowIcon(icon)

  # taskThreads = []
  # sFrames = ()
  main_ui.dockWidgetTasks.setTitleBarWidget(main_ui.titleBarWidgetTasks)
  main_ui.dockWidgetFrames.setTitleBarWidget(main_ui.titleBarWidgetFrames)
  # authL = auth.login()
  # colNamesTask = ["id","fileName","fRange","resolution","priority","fastAssign","user","outDir","hostGroups","afterTasks","submitTime","doneTime","afterTime","status"]
  # colNamesFrames = ["id","frameId","hostName","ram","sTime","eTime","runCount","status","fThreads","efficiency"]
  # colNamesFramesXtra = ["timeTaken"]
  # colNamesTaskXtra = ["pending"]
  # #self.checkTMine.setChecked(2)
  #
  # selectedTaskList = []

  # QtCore.QObject.connect(self.framesRefresh, QtCore.SIGNAL(str_convert("clicked()")), self.popTableFrames)
  # QtCore.QObject.connect(self.tableList, QtCore.SIGNAL(str_convert("itemSelectionChanged()")), self.timeFramesCheck)
  # QtCore.QObject.connect(self.checkAll, QtCore.SIGNAL(str_convert("clicked()")), self.popTableFrames)
  # QtCore.QObject.connect(self.checkDone, QtCore.SIGNAL(str_convert("clicked()")), self.popTableFrames)
  # QtCore.QObject.connect(self.checkAssigned, QtCore.SIGNAL(str_convert("clicked()")), self.popTableFrames)
  # QtCore.QObject.connect(self.checkAutohold, QtCore.SIGNAL(str_convert("clicked()")), self.popTableFrames)
  # QtCore.QObject.connect(self.checkFailed, QtCore.SIGNAL(str_convert("clicked()")), self.popTableFrames)
  # QtCore.QObject.connect(self.checkKilled, QtCore.SIGNAL(str_convert("clicked()")), self.popTableFrames)
  # QtCore.QObject.connect(self.checkRunning, QtCore.SIGNAL(str_convert("clicked()")), self.popTableFrames)
  # QtCore.QObject.connect(self.checkHold, QtCore.SIGNAL(str_convert("clicked()")), self.popTableFrames)
  # QtCore.QObject.connect(self.checkHung, QtCore.SIGNAL(str_convert("clicked()")), self.popTableFrames)

  main_ui.framesRefresh.clicked.connect(lambda : popTableFrames(main_ui))
  main_ui.tableList.itemSelectionChanged.connect(timeFramesCheck)
  main_ui.checkAll.clicked.connect(lambda : popTableFrames(main_ui))
  main_ui.checkDone.clicked.connect(lambda : popTableFrames(main_ui))
  main_ui.checkAssigned.clicked.connect(lambda : popTableFrames(main_ui))
  main_ui.checkAutohold.clicked.connect(lambda : popTableFrames(main_ui))
  main_ui.checkFailed.clicked.connect(lambda : popTableFrames(main_ui))
  main_ui.checkKilled.clicked.connect(lambda : popTableFrames(main_ui))
  main_ui.checkRunning.clicked.connect(lambda : popTableFrames(main_ui))
  main_ui.checkHold.clicked.connect(lambda : popTableFrames(main_ui))
  main_ui.checkHung.clicked.connect(lambda : popTableFrames(main_ui))

  main_ui.checkUnassigned.clicked.connect(lambda : popTableFrames(main_ui))
  main_ui.checkTAll.clicked.connect(lambda : popTableList(main_ui))
  main_ui.checkTActive.clicked.connect(lambda : popTableList(main_ui))
  main_ui.checkTAutohold.clicked.connect(lambda : popTableList(main_ui))
  main_ui.checkTDone.clicked.connect(lambda : popTableList(main_ui))
  main_ui.checkTHold.clicked.connect(lambda : popTableList(main_ui))
  main_ui.checkTMine.clicked.connect(lambda : popTableList(main_ui))
  main_ui.checkDateTask.clicked.connect(lambda : checkDateTaskFunc(main_ui))
  main_ui.radioAfter.clicked.connect(lambda : popTableList(main_ui))
  main_ui.radioDone.clicked.connect(lambda : popTableList(main_ui))
  main_ui.radioSubmit.clicked.connect(lambda : popTableList(main_ui))
  main_ui.dateEditTaskFrom.dateChanged.connect(lambda : popTableList(main_ui))
  main_ui.dateEditTaskTo.dateChanged.connect(lambda : popTableList(main_ui))
  main_ui.tableList.customContextMenuRequested.connect(lambda x: popupTask(main_ui, x))
  main_ui.tableFrames.customContextMenuRequested.connect(lambda x: popupFrames(main_ui, x))
  main_ui.taskRefresh.clicked.connect(lambda: popTableList(main_ui))
  # timer = QtCore.QTimer()
  # timerFramesRefresh = QtCore.QTimer()
  timerFramesRefresh.timeout.connect(lambda : popTableFrames(main_ui))
  timer.timeout.connect(lambda : popTableFrames(main_ui))
  main_ui.checkRefresh.clicked.connect(lambda : timeCheck(main_ui))
  main_ui.lineEditSearch.returnPressed.connect(lambda : popTableList(main_ui))
  main_ui.lineEditSearchFrames.returnPressed.connect(lambda : popTableFrames(main_ui))

  checkDateTaskFunc(main_ui)
  main_ui.labelUser.setText(os.environ['rbhus_acl_user'])
  taskSearchTime = 0.0
  main_ui.dateEditTaskFrom.setDate(QtCore.QDate.currentDate())
  main_ui.dateEditTaskTo.setDate(QtCore.QDate.currentDate())

  popTableList(main_ui)

  #self.centralwidget.resizeEvent  = self.resizeEvent
  #self.tableList.resizeEvent = self.resizeEvent


  #self.loadingGif = dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/loading.gif"
  #self.loader = ImagePlayer(self.loadingGif,parent=self.tableList)
  #self.loader.hide()


#def resizeEvent(self,event):
  #self.loader.resizeEvent(event)
  #self.tableList.resizeColumnsToContents()

  main_ui.show()
  main_ui.update()


def report_thread(self):
  selTasksDict = selectedTasks(main_ui)
  selTasks = []
  db_conn = dbRbhus.dbRbhus()
  tids = []
  doneFs = []
  pendingFs = []
  batchIds = []
  threadAvg = []

  for x in selTasksDict:
    try:
      rows = db_conn.execute("select * from frames where id="+ str(x['id']), dictionary=True)
    except:
      return(0)
    if(rows):
      for row in rows:
        if(row['status'] == constants.framesDone):
          doneFs.append(row)
        else:
          pendingFs.append(row)
      if(doneFs):
        for dfs in doneFs:
          try:
            batchIds[dfs['batchId']].append(dfs)
          except:
            batchIds[dfs['batchId']] = []
            batchIds[dfs['batchId']].append(dfs)
          try:
            threadAvg[dfs['fThreads']].append(dfs)
          except:
            threadAvg[dfs['fThreads']] = []
            threadAvg[dfs['fThreads']].append(dfs)







def checkDateTaskFunc(main_ui):
  if main_ui.checkDateTask.isChecked():
    main_ui.dateEditTaskFrom.setEnabled(True)
    main_ui.dateEditTaskTo.setEnabled(True)
    main_ui.groupBoxTaskDate.setVisible(True)
  else:
    main_ui.dateEditTaskFrom.setEnabled(False)
    main_ui.dateEditTaskTo.setEnabled(False)
    main_ui.groupBoxTaskDate.setVisible(False)



def previewTask(main_ui):
  selTasksDict = selectedTasks(main_ui)
  selTasks = []
  db_conn = dbRbhus.dbRbhus()
  if selTasksDict:
    for x in selTasksDict:
      tD = db_conn.getTaskDetails(x['id'])
      oDir = tD['outDir']
      fila = QtWidgets.QFileDialog.getOpenFileNames(directory=oDir,options=QtWidgets.QFileDialog.DontUseNativeDialog)
      if(fila):
        debug.info(fila)
        for fi in fila:
          if not fi:
            return
          if not os.path.isfile(fi[0]):
            return
          if(sys.platform.find("win") >= 0):
            subprocess.Popen(["x:/standard/template/djv-0.8.3-x64/bin/djv_view.exe -file_proxy 1/4 ",str(fi.replace("\\","/"))," -file_seq_auto ","true"," -file_cache ","true"])
          elif(sys.platform.find("linux") >= 0):
            # debug.info("djv_view -file_proxy 1/4 "+ str(fi[0]) +" -seq_auto False  -file_cache True")
            subprocess.Popen(["djv_view",str(fi[0]),"-seq_auto","True","-file_cache","True"])
          debug.info(fi)


def previewFrame(main_ui):
  selFramesDict = selectedFrames(main_ui)
  selFrames = {}
  db_conn = dbRbhus.dbRbhus()
  for x in selFramesDict:
    tD = db_conn.getTaskDetails(x['id'])
    oDir = tD['outDir']
    debug.info("*"+ str(x['frameId']).zfill(tD['pad']) +"*")
    fila = QtWidgets.QFileDialog.getOpenFileNames(directory=oDir,filter="*"+ str(x['frameId']).zfill(tD['pad']) +"*",options=QtWidgets.QFileDialog.DontUseNativeDialog)
    if(fila):
      debug.info(fila)
      for fi in fila:
        if not fi:
          return
        if not os.path.isfile(fi[0]):
          return
        if(sys.platform.find("win") >= 0):
          subprocess.Popen(["x:/standard/template/djv-0.8.3-x64/bin/djv_view.exe",str(fi.replace("\\","/")),"-file_seq_auto","false","-file_cache","true"])
        elif(sys.platform.find("linux") >= 0):
          subprocess.Popen(["djv_view",str(fi[0]),"-seq_auto","False","-file_cache","True"])
        debug.info(fi)


def popupTask(main_ui, pos):
  mainMenu = QtWidgets.QMenu()
  toolsMenu = QtWidgets.QMenu()
  toolsMenu.setTitle("tools")

  scriptMenu = QtWidgets.QMenu()
  scriptMenu.setTitle("create Scripts")

  test1Action = toolsMenu.addAction("activate")
  test2Action = toolsMenu.addAction("hold")
  test3Action = toolsMenu.addAction("rerun")
  test4Action = toolsMenu.addAction("edit")
  test5Action = mainMenu.addAction("open dir")
  # test10Action = toolsMenu.addAction("exr2png(linux)")
  # test11Action = toolsMenu.addAction("png2flv(linux)")
  # test12Action = toolsMenu.addAction("png2mp4(linux)")
  test13Action = toolsMenu.addAction("exr2movRle(linux)")
  test14Action = toolsMenu.addAction("png2movRle(linux)")
  test6Action = toolsMenu.addAction("copy/submit")
  test7Action = toolsMenu.addAction("fastAssign enable")
  test8Action = toolsMenu.addAction("fastAssign disable")
  test9Action = toolsMenu.addAction("delete")

  exrMovRleAction = scriptMenu.addAction("exr -> mov(rle)")
  pngMovRleAction = scriptMenu.addAction("png -> mov(rle)")

  mainMenu.addMenu(toolsMenu)
  toolsMenu.addMenu(scriptMenu)

  action = mainMenu.exec_(main_ui.tableList.mapToGlobal(pos))
  if action == test1Action:
    activateTask(main_ui)
  if action == test2Action:
    holdTask(main_ui)
  if action == test3Action:
    rerunTask(main_ui)
  if action == test4Action:
    editTask(main_ui)
  if action == test5Action:
    previewTask(main_ui)
  if action == test6Action:
    copySubmit(main_ui)
  if action == test7Action:
    fastAssignFunc(main_ui, e=1)
  if action == test8Action:
    fastAssignFunc(main_ui, e=0)
  if action == test9Action:
    delTask(main_ui)
  # if(action == test10Action):
  #   self.exr2png()
  # if(action == test11Action):
  #   self.png2flv()
  # if(action == test12Action):
  #   self.png2mp4()

  if action == exrMovRleAction:
    exrMovRle(main_ui)
  if action == test13Action:
    exrMovRle(main_ui, isScript=False)
  if action == pngMovRleAction:
    pngMovRle(main_ui)
  if action == test14Action:
    pngMovRle(main_ui, isScript=False)


def exrMovRle(main_ui, isScript = True):
  selTasksDict = selectedTasks(main_ui)
  selTasks = []
  db_conn = dbRbhus.dbRbhus()
  try:
    os.makedirs(os.path.join(os.path.expanduser("~"),"rbhusRenderGeneratedScripts"))
  except:
    debug.info("trying to create rbhusPipe directory : "+ str(sys.exc_info()))
  if(isScript):
    filenamepy = os.path.join(os.path.expanduser("~"),"rbhusRenderGeneratedScripts",("_".join(time.asctime().split()) +".py").replace(":","-"))
    fd = open(filenamepy,"w")
    fd.write("#!/bin/bash\n")
    debug.info(filenamepy)
  if (selTasksDict):
    for x in selTasksDict:
      tD = db_conn.getTaskDetails(x['id'])
      oDir = tD['outDir']
      convertCmd = exr2rleCmd +" "+ oDir +"\n"
      debug.info(convertCmd)
      if(isScript):
        fd.write(convertCmd)
      else:
        os.system(convertCmd.rstrip())
      if (tD['renExtEnv'] != "default"):
        renExtEnv = simplejson.loads(tD['renExtEnv'])
        if("assPath" in renExtEnv):
          assPath = renExtEnv['assPath']
          assProj = assPath.split(":")[0]
          copyAss = assProj +":output:Movs"
          copyAssAbsPath = utilsPipe.getAbsPath(copyAss)
          cpCmd = "cp -v "+ oDir +"/*.mov "+ copyAssAbsPath +"/\n"
          if(isScript):
            fd.write(cpCmd)
          else:
            os.system(cpCmd.rstrip())
      if(isScript):
        fd.write("\n\n")
  if(isScript):
    fd.flush()
    fd.close()
    os.chmod(filenamepy,0o777)
    msgbox = QtWidgets.QMessageBox()
    msgbox.setText(filenamepy)
    msgbox.exec_()

def pngMovRle(main_ui, isScript = True):
  selTasksDict = selectedTasks(main_ui)
  selTasks = []
  db_conn = dbRbhus.dbRbhus()
  try:
    os.makedirs(os.path.join(os.path.expanduser("~"),"rbhusRenderGeneratedScripts"))
  except:
    debug.info("trying to create rbhusPipe directory : "+ str(sys.exc_info()))
  if(isScript):
    filenamepy = os.path.join(os.path.expanduser("~"),"rbhusRenderGeneratedScripts",("_".join(time.asctime().split()) +".py").replace(":","-"))
    fd = open(filenamepy,"w")
    fd.write("#!/bin/bash\n")
    debug.info(filenamepy)
  if (selTasksDict):
    for x in selTasksDict:
      tD = db_conn.getTaskDetails(x['id'])
      oDir = tD['outDir']
      convertCmd = png2rleCmd +" "+ oDir +"\n"
      debug.info(convertCmd)
      if(isScript):
        fd.write(convertCmd)
      else:
        os.system(convertCmd.rstrip())
      if (tD['renExtEnv'] != "default"):
        renExtEnv = simplejson.loads(tD['renExtEnv'])
        if("assPath" in renExtEnv):
          assPath = renExtEnv['assPath']
          assProj = assPath.split(":")[0]
          copyAss = assProj +":output:Movs"
          copyAssAbsPath = utilsPipe.getAbsPath(copyAss)
          cpCmd = "cp -v "+ oDir +"/*.mov "+ copyAssAbsPath +"/\n"
          if(isScript):
            fd.write(cpCmd)
          else:
            os.system(cpCmd.rstrip())
      if(isScript):
        fd.write("\n\n")
  if(isScript):
    fd.flush()
    fd.close()
    os.chmod(filenamepy,0o777)
    msgbox = QtWidgets.QMessageBox()
    msgbox.setText(filenamepy)
    msgbox.exec_()



# def exrRleCreateScript(self):
#   selTasksDict = selectedTasks(main_ui)
#   selTasks = []
#   db_conn = dbRbhus.dbRbhus()
#   if (selTasksDict):
#     for x in selTasksDict:
#       tD = db_conn.getTaskDetails(x['id'])
#       oDir = tD['outDir']
#       renExtEnv = {}
#       if(tD['renExtEnv'] != "default"):
#
#
#
#       self.centralwidget.setCursor(QtCore.Qt.WaitCursor)
#
#       openP = subprocess.Popen(exr2pngCmd + " " + str(oDir), shell=True)
#       openP.wait()
#       self.centralwidget.setCursor(QtCore.Qt.ArrowCursor)


def exr2png(main_ui):
  selTasksDict = selectedTasks(main_ui)
  selTasks = []
  db_conn = dbRbhus.dbRbhus()
  if(selTasksDict):
    for x in selTasksDict:
      tD = db_conn.getTaskDetails(x['id'])
      oDir = tD['outDir']
      main_ui.centralwidget.setCursor(QtCore.Qt.WaitCursor)
      openP = subprocess.Popen(exr2pngCmd +" "+ str(oDir),shell=True)
      openP.wait()
      main_ui.centralwidget.setCursor(QtCore.Qt.ArrowCursor)


def png2flv(main_ui):
  selTasksDict = selectedTasks(main_ui)
  selTasks = []
  db_conn = dbRbhus.dbRbhus()
  if(selTasksDict):
    for x in selTasksDict:
      tD = db_conn.getTaskDetails(x['id'])
      oDir = tD['outDir']
      main_ui.centralwidget.setCursor(QtCore.Qt.WaitCursor)
      openP = subprocess.Popen(png2flvCmd +" "+ str(oDir),shell=True)
      openP.wait()
      main_ui.centralwidget.setCursor(QtCore.Qt.ArrowCursor)

def png2mp4(main_ui):
  selTasksDict = selectedTasks(main_ui)
  selTasks = []
  db_conn = dbRbhus.dbRbhus()
  if(selTasksDict):
    for x in selTasksDict:
      tD = db_conn.getTaskDetails(x['id'])
      oDir = tD['outDir']
      main_ui.centralwidget.setCursor(QtCore.Qt.WaitCursor)
      openP = subprocess.Popen(png2mp4Cmd +" "+ str(oDir),shell=True)
      openP.wait()
      main_ui.centralwidget.setCursor(QtCore.Qt.ArrowCursor)






def fastAssignFunc(main_ui, e=0):
  selTasksDict = selectedTasks(main_ui)
  selTasks = []
  if selTasksDict:
    for x in selTasksDict:
      selTasks.append(x['id'].lstrip("0"))
    if selTasks:
      for x in selTasks:
        debug.info(x)
        tsks = rUtils.tasks(tId=x)
        if(tsks):
          tsks.fastAssign(enable=e)
    return(1)
  return(0)




def popupFrames(main_ui, pos):
  selFramesDict = selectedFrames(main_ui)
  menu = QtWidgets.QMenu()
  db_conn = dbRbhus.dbRbhus()
  test1Action = menu.addAction("check log")
  test3Action = menu.addAction("hold")
  test4Action = menu.addAction("rerun")
  test5Action = menu.addAction("check frame")
  test10Action = menu.addAction("exr2png(linux)")
  test2Action = menu.addAction("kill")
  test6Action = menu.addAction("kill/hold")

  action = menu.exec_(main_ui.tableFrames.mapToGlobal(pos))
  if action == test1Action:
    for x in selFramesDict:

      fInfos = db_conn.getFrameInfo(x['id'],x['frameId'])
      if(fInfos):
        #debug.info(fInfos)
        debug.info("log file : "+ str(fInfos['logFile']))
        openP = subprocess.Popen([sys.executable,dirSelf.rstrip(os.sep) + os.sep + "rbhusReadText.py",fInfos['logFile']])

  if action == test2Action:
    stopFrame(main_ui)
  if action == test3Action:
    holdFrame(main_ui)
  if action == test4Action:
    rerunFrame(main_ui)
  if action == test5Action:
    previewFrame(main_ui)
  if action == test6Action:
    killHoldFrame(main_ui)
  if action == test10Action:
    exr2pngFrames(main_ui)

def exr2pngFrames(main_ui):
  selFramesDict = selectedFrames(main_ui)
  selFrames = {}
  db_conn = dbRbhus.dbRbhus()
  if(selFramesDict):
    for x in selFramesDict:
      tD = db_conn.getTaskDetails(x['id'])
      oDir = tD['outDir']
      debug.info("*"+ str(x['frameId']).zfill(tD['pad']) +"*")
      fila = QtWidgets.QFileDialog.getOpenFileNames(directory=oDir,filter="*"+ str(x['frameId']).zfill(tD['pad']) +"*",options=QtWidgets.QFileDialog.DontUseNativeDialog)
      debug.info(fila)
      if(fila):
        for f in fila:
          main_ui.centralwidget.setCursor(QtCore.Qt.WaitCursor)
          openP = subprocess.Popen(exr2pngCmd +" "+ str(f).rstrip().lstrip(),shell=True)
          openP.wait()
          main_ui.centralwidget.setCursor(QtCore.Qt.ArrowCursor)


def stopFrame(main_ui):
  selFramesDict = selectedFrames(main_ui)
  selFrames = {}
  db_conn = dbRbhus.dbRbhus()
  for x in selFramesDict:
    if(x['status'] == "running"):
      debug.info (getHostIp(x['hostName']))
      db_conn.stopFrames(str(getHostIp(x['hostName'])),x['id'],x['frameId'])
    else:
      debug.info(str(x['id']) +"%"+ str(x['frameId']) +" not able to murder since it is running")
  popTableFrames(main_ui)

def killHoldFrame(main_ui):
  selFramesDict = selectedFrames(main_ui)
  selFrames = {}
  db_conn = dbRbhus.dbRbhus()
  for x in selFramesDict:
    if(x['status'] == "running"):
      debug.info (getHostIp(x['hostName']))
      db_conn.stopHoldFrames(str(getHostIp(x['hostName'])),x['id'],x['frameId'])
    else:
      debug.info(str(x['id']) +"%"+ str(x['frameId']) +" not able to murder since it is running")
  popTableFrames(main_ui)

def rerunFrame(main_ui):
  selFramesDict = selectedFrames(main_ui)
  selFrames = {}
  for x in selFramesDict:
    if((x['status'] != "running") and (x['status'] != "assigned") and (x['status'] != "pending")):
      try:
        selFrames[x['id']].append(x['frameId'])
      except:
        selFrames[x['id']] = []
        selFrames[x['id']].append(x['frameId'])
    else:
      debug.info(str(x['id']) +"%"+ str(x['frameId']) +" cannot rerun frames that are already running. please stop and rerun them")
  if(selFrames):
    for x in selFrames.keys():
      ids = " or frameId=".join(selFrames[x])
      try:
        conn = db.connRbhus()
        cursor = conn.cursor()
        cursor.execute("update frames set status = "+ str(constants.framesUnassigned) +" where (id="+ str(x) +") and (frameId="+ str(ids) +")")
        cursor.close()
        conn.close()
      except:
        debug.info("1 :Error connecting to db :"+ str(sys.exc_info()))
        return(0)
  popTableFrames(main_ui)


def holdFrame(main_ui):
  selFramesDict = selectedFrames(main_ui)
  selFrames = {}
  for x in selFramesDict:
    if((x['status'] != "running") and (x['status'] != "assigned") and (x['status'] != "pending")):
      try:
        selFrames[x['id']].append(x['frameId'])
      except:
        selFrames[x['id']] = []
        selFrames[x['id']].append(x['frameId'])
    else:
      debug.info(str(x['id']) +"%"+ str(x['frameId']) +" cannot hold frames that are running. please stop them before holding them")

  if(selFrames):
    for x in selFrames.keys():
      ids = " or frameId=".join(selFrames[x])
      try:
        conn = db.connRbhus()
        cursor = conn.cursor()
        cursor.execute("update frames set status = "+ str(constants.framesHold) +" where (id="+ str(x) +") and (frameId="+ str(ids) +")")
        cursor.close()
        conn.close()
      except:
        debug.info("1 :Error connecting to db :"+ str(sys.exc_info()))
        return()
  popTableFrames(main_ui)


def copySubmit(main_ui):
  selTasksDict = selectedTasks(main_ui)
  selTasks = []
  for x in selTasksDict:
    selTasks.append(x['id'].lstrip("0"))


  if len(selTasks) == 1:
    try:
      subprocess.Popen([sys.executable,submitCmd,str(selTasks[0])])
    except:
      debug.info(str(sys.exc_info()))
  else:
    debug.info("wtf . cannot copy from multiple tasks!")


def editTask(main_ui):
  selTasksDict = selectedTasks(main_ui)
  selTasks = []
  for x in selTasksDict:
    selTasks.append(x['id'].lstrip("0"))
  if len(selTasks) > 1:
    try:
      subprocess.Popen([sys.executable,editTaskMultiCmd,str(",".join(selTasks))])
    except:
      debug.info(str(sys.exc_info()))
  else:
    try:
      subprocess.Popen([sys.executable,editTaskCmd,str(selTasks[0])])
    except:
      debug.info(str(sys.exc_info()))



def holdTask(main_ui):
  selTasksDict = selectedTasks(main_ui)
  selTasks = []
  db_conn = dbRbhus.dbRbhus()
  if selTasksDict:
    for x in selTasksDict:
      t = rUtils.tasks(str(x['id']).lstrip("0"))
      t.holdTask()
  popTableList(main_ui)


def delTask(main_ui):
  selTasksDict = selectedTasks(main_ui)
  selTasks = []
  #self.showDialog()
  db_conn = dbRbhus.dbRbhus()
  if selTasksDict:
    for x in selTasksDict:
      t = rUtils.tasks(str(x['id']).lstrip("0"))
      t.remove()
  popTableList(main_ui)


def activateTask(main_ui):
  selTasksDict = selectedTasks(main_ui)
  selTasks = []
  for x in selTasksDict:
    t = rUtils.tasks(str(x['id']).lstrip("0"))
    t.activateTask()
  popTableList(main_ui)


def rerunTask(main_ui):
  selTasksDict = selectedTasks(main_ui)
  selTasks = []
  #self.showDialog()
  db_conn = dbRbhus.dbRbhus()
  if selTasksDict:
    for x in selTasksDict:
      t = rUtils.tasks(str(x['id']).lstrip("0"))
      t.rerunTask()
  popTableList(main_ui)



def stopRunning(self,tableType):
  pass

def timeFramesCheck():
  if timerFramesRefresh.isActive():
    timerFramesRefresh.stop()
    timerFramesRefresh.start(2000)
  else:
    timerFramesRefresh.start(2000)



def timeCheck(main_ui):
  cRefresh = main_ui.checkRefresh.isChecked()
  if cRefresh:
    startTimer()
  else:
    stopTimer()

def startTimer():
  timer.start(5000)

def stopTimer():
  timer.stop()


class TaskThread(QtCore.QThread):
  taskFinished = QtCore.pyqtSignal(object)  # Custom signal to emit the result

  def __init__(self, parent=None):
    super().__init__(parent)
    self.main_ui = parent

  def run(self):
    result = selectTasks(self.main_ui)  # Call your task and store the result
    self.taskFinished.emit(result)  # Emit the result when the task is done


class FramesThread(QtCore.QThread):
  taskFinished = QtCore.pyqtSignal()  # Custom signal to emit the result

  def __init__(self, parent=None):
    super().__init__(parent)
    self.main_ui = parent

  def run(self):
    result = selectFrames(self.main_ui)  # Call your task and store the result
    self.taskFinished.emit()  # Emit the result when the task is done


def popTableList(main_ui):
  global taskThreads
  # taskThread = QtCore.QThread(parent=main_ui)
  #if(self.taskThreads):
    #tTs = self.taskThreads
    #for x in tTs:
      #if(x.isRunning()):
        #x.terminate()
        #try:
          #self.taskThreads.remove(x)
        #except:
          #debug.info(str(sys.exc_info()))
        #debug.info("terminating :"+ str(x))
    #self.taskThreads = []
    #time.sleep(0.5)

  taskThread = TaskThread(parent=main_ui)

  if taskThreads:
    debug.info(taskThreads)
    for thread in taskThreads:
      try:
        if thread.isRunning():
          # thread.terminate()
          thread.quit()
          thread.wait()
        if thread.isFinished():
          thread.deleteLater()
          taskThreads.remove(thread)
        debug.info("terminated :" + str(thread))
      except Exception as e:
        debug.info(str(e))
    # frameThreads = []
    debug.info(taskThreads)
    # time.sleep(0.5)


  # taskThread.run = selectTasks(main_ui)
  taskThread.taskFinished.connect(lambda result: popTableList_thread(result, main_ui))
  main_ui.tableList.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.WaitCursor))
  main_ui.groupBoxTask.setEnabled(False)
  main_ui.groupBoxTaskDate.setEnabled(False)
  taskThread.start()
  taskThreads.append(taskThread)


def selectTasks(main_ui):
  global username
  global colNamesTask

  pendFrames = {}
  selTasks = []
  statusToCheck = []
  cTDone = main_ui.checkTDone.isChecked()
  cTActive = main_ui.checkTActive.isChecked()
  cTHold = main_ui.checkTHold.isChecked()
  cTAutohold = main_ui.checkTAutohold.isChecked()
  cTAll = main_ui.checkTAll.isChecked()
  cTMine = main_ui.checkTMine.isChecked()
  timeS = ""
  if main_ui.checkDateTask.isChecked():
    fromT = "'"+ str(main_ui.dateEditTaskFrom.date().year()) +"-"+ str(main_ui.dateEditTaskFrom.date().month()) +"-"+ str(main_ui.dateEditTaskFrom.date().day()) +"'"
    toT = "'"+ str(main_ui.dateEditTaskTo.date().year()) +"-"+ str(main_ui.dateEditTaskTo.date().month()) +"-"+ str(main_ui.dateEditTaskTo.date().day()) +"'"
    if main_ui.radioSubmit.isChecked():
      timeS = "(submitTime between "+ fromT +" and "+ toT +")"
    elif main_ui.radioDone.isChecked():
      timeS = "(doneTime between "+ fromT +" and "+ toT +")"
    elif main_ui.radioAfter.isChecked():
      timeS = "(afterTime between "+ fromT +" and "+ toT +")"
  if(cTDone):
    statusToCheck.append(str(constants.taskDone))
  if(cTActive):
    statusToCheck.append(str(constants.taskActive))
  if(cTHold):
    statusToCheck.append(str(constants.taskStopped))
  if(cTAutohold):
    statusToCheck.append(str(constants.taskAutoStopped))
  db_conn = dbRbhus.dbRbhus()
  rows = []
  try:
    if(cTAll):
      if(cTMine):
        if(timeS):
          rows = db_conn.execute("select "+ ",".join(colNamesTask) +" from tasks where user='"+ str(username) +"' and "+ timeS,dictionary=True)
        else:
          rows = db_conn.execute("select "+ ",".join(colNamesTask) +" from tasks where user='"+ str(username) +"'",dictionary=True)
      else:
        if(timeS):
          rows = db_conn.execute("select "+ ",".join(colNamesTask) +" from tasks where "+ timeS,dictionary=True)
        else:
          rows = db_conn.execute("select "+ ",".join(colNamesTask) +" from tasks",dictionary=True)
    else:
      if(statusToCheck):
        statusCheck = " or status=".join(statusToCheck)
        if(cTMine):
          if(timeS):
            rows = db_conn.execute("select "+ ",".join(colNamesTask) +" from tasks where (status="+ statusCheck +") and user='"+ str(username) +"' and "+ timeS,dictionary=True)
          else:
            rows = db_conn.execute("select "+ ",".join(colNamesTask) +" from tasks where (status="+ statusCheck +") and user='"+ str(username) +"'",dictionary=True)
        else:
          if(timeS):
            rows = db_conn.execute("select "+ ",".join(colNamesTask) +" from tasks where (status="+ statusCheck +") and "+ timeS,dictionary=True)
          else:
            rows = db_conn.execute("select "+ ",".join(colNamesTask) +" from tasks where (status="+ statusCheck +")",dictionary=True)
  except:
    debug.info("Error connecting to db "+ str(sys.exc_info()))

  if(rows):
    for row in rows:
      pendFrames[row['id']] = db_conn.getUnassignedFramesCount(row['id'])
  selTasks = rows
  # debug.info(pendFrames)
  # debug.info(selTasks)
  return pendFrames, selTasks

  #self.tableList.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))


def popTableList_thread(pfst, main_ui):
  global colNamesTaskXtra
  global colNamesTask

  debug.info("popTableList called!")
  #self.tableList.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.WaitCursor))
  pendFrames, selTasks = pfst

  tSeletected = selectedTasks(main_ui)
  tSelect = []
  if tSeletected:
    for x in tSeletected:
      tSelect.append(x['id'])

  main_ui.tableList.clearContents()
  main_ui.tableList.setSortingEnabled(False)
  main_ui.tableList.resizeColumnsToContents()
  main_ui.tableList.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
  colCount = 0
  rows = selTasks

  if not rows:
    main_ui.tableList.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
    main_ui.tableList.setColumnCount(0)
    main_ui.tableList.setRowCount(0)
    main_ui.labelTaskTotal.setText(QtWidgets.QApplication.translate("Form", str(0), None))
    main_ui.groupBoxTask.setEnabled(True)
    main_ui.groupBoxTaskDate.setEnabled(True)
    return()
  colCount = len(colNamesTask) + len(colNamesTaskXtra)

  findRows = []

  for row in rows:
    sFlag = 0
    for colName in colNamesTask:
      if str(row[colName]).find(str_convert(main_ui.lineEditSearch.text())) >= 0:
        sFlag = 1
    if(sFlag):
      findRows.append(row)
  rows = findRows


  main_ui.labelTaskTotal.setText(QtWidgets.QApplication.translate("Form", str(len(rows)), None))
  main_ui.tableList.setColumnCount(colCount)
  main_ui.tableList.setRowCount(len(rows))

  for x in range(0,colCount):
    item = QtWidgets.QTableWidgetItem()
    main_ui.tableList.setHorizontalHeaderItem(x, item)
  indx = 0
  for x in colNamesTask:
    main_ui.tableList.horizontalHeaderItem(indx).setText(QtWidgets.QApplication.translate("Form", x, None))
    indx = indx + 1

  for x in colNamesTaskXtra:
    main_ui.tableList.horizontalHeaderItem(indx).setText(QtWidgets.QApplication.translate("Form", x, None))
    indx = indx + 1


  indx = 0
  for row in rows:
    #sFlag = 0
    #for colName in colNamesTask:
      #if(str(row[colName]).find(str(self.lineEditSearch.text())) >= 0):
        #sFlag = 1

    #if(sFlag):
    item = QtWidgets.QTableWidgetItem()
    main_ui.tableList.setVerticalHeaderItem(indx, item)
    colIndx = 0
    for colName in colNamesTask:
      item = QtWidgets.QTableWidgetItem()
      # item.setToolTip(str(row['fileName']))
      if(colName == "status"):
        main_ui.tableList.setItem(indx, colIndx, item)
        main_ui.tableList.item(indx, colIndx).setText(QtWidgets.QApplication.translate("Form", constants.taskStatus[int(row[colName])], None))
        colIndx = colIndx + 1
        continue
      if(colName == "id"):
        main_ui.tableList.setItem(indx, colIndx, item)
        main_ui.tableList.item(indx, colIndx).setText(QtWidgets.QApplication.translate("Form", str(row[colName]).zfill(4), None))
        if(str(row[colName]).zfill(4) in tSelect):
          main_ui.tableList.selectRow(indx)
        colIndx = colIndx + 1
        continue

      if (colName == "fileName"):
        main_ui.tableList.setItem(indx, colIndx, item)
        main_ui.tableList.item(indx, colIndx).setText(QtWidgets.QApplication.translate("Form", str(row[colName]).split(os.sep)[-1], None))
        colIndx = colIndx + 1
        continue

      main_ui.tableList.setItem(indx, colIndx, item)
      main_ui.tableList.item(indx, colIndx).setText(QtWidgets.QApplication.translate("Form", str(row[colName]), None))
      colIndx = colIndx + 1

    for colName in colNamesTaskXtra:
      item = QtWidgets.QTableWidgetItem()
      # item.setToolTip(str(row['id']) +":"+ str(row['fileName']))
      if(colName == "pending"):
        main_ui.tableList.setItem(indx, colIndx, item)
        totalPend = 0
        #pendFrames = dbconn.getUnassignedFramesCount(row['id'])
        try:
          totalPend = pendFrames[row['id']][-1]['count(*)']
        except:
          pass
        main_ui.tableList.item(indx, colIndx).setText(QtWidgets.QApplication.translate("Form", str(totalPend), None))
        colIndx = colIndx + 1
        continue
      main_ui.tableList.setItem(indx, colIndx, item)
      main_ui.tableList.item(indx, colIndx).setText(QtWidgets.QApplication.translate("Form", str(row[colName]), None))
      colIndx = colIndx + 1

    indx = indx + 1

  main_ui.labelTaskTotal.setText(QtWidgets.QApplication.translate("Form", str(len(rows)), None))
  main_ui.tableList.resizeColumnsToContents()
  main_ui.tableList.setSortingEnabled(True)

  main_ui.tableList.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
  main_ui.tableList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
  main_ui.groupBoxTask.setEnabled(True)
  main_ui.groupBoxTaskDate.setEnabled(True)
  #popTableFrames(main_ui)


def refresh(self):
  popTableList(main_ui)
  popTableFrames(main_ui)


def popTableFrames(main_ui):
  global frameThreads
  # hf = QtCore.QThread(parent=main_ui)
  hf = FramesThread(parent=main_ui)
  # hf.run = selectFrames(main_ui)

  if frameThreads:
    debug.info(frameThreads)
    for thread in frameThreads:
      try:
        if thread.isRunning():
          # thread.terminate()
          thread.quit()
          thread.wait()
        if thread.isFinished():
          thread.deleteLater()
          frameThreads.remove(thread)
        debug.info("terminated :" + str(thread))
      except Exception as e:
        debug.info(str(e))
    # frameThreads = []
    debug.info(frameThreads)
    # time.sleep(0.5)

  hf.taskFinished.connect(lambda : popTableFrames_thread(main_ui))
  main_ui.tableFrames.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.WaitCursor))
  hf.start()
  frameThreads.append(hf)


def selectFrames(main_ui):
  global sFrames
  global timerFramesRefresh
  selTasksDict = selectedTasks(main_ui)
  selTasks = []
  db_conn = dbRbhus.dbRbhus()
  padDict = {}
  for x in selTasksDict:
    selTasks.append(x['id'])
    padDict[re.sub("^0+","",x['id'])] = 4

  #debug.info(padDict)
  if(selTasks):
    ids = " or id = ".join(selTasks)
  else:
    timerFramesRefresh.stop()
    return()

  statusToCheck = []
  cDone = main_ui.checkDone.isChecked()
  cAssigned = main_ui.checkAssigned.isChecked()
  cUnassigned = main_ui.checkUnassigned.isChecked()
  cRun = main_ui.checkRunning.isChecked()
  cFailed = main_ui.checkFailed.isChecked()
  cHold = main_ui.checkHold.isChecked()
  cAutohold = main_ui.checkAutohold.isChecked()
  cKilled = main_ui.checkKilled.isChecked()
  cHung =  main_ui.checkHung.isChecked()
  cAll = main_ui.checkAll.isChecked()
  if(cDone):
    statusToCheck.append(str(constants.framesDone))
  if(cAssigned):
    statusToCheck.append(str(constants.framesAssigned))
  if(cRun):
    statusToCheck.append(str(constants.framesRunning))
  if(cFailed):
    statusToCheck.append(str(constants.framesFailed))
  if(cHold):
    statusToCheck.append(str(constants.framesHold))
  if(cAutohold):
    statusToCheck.append(str(constants.framesAutoHold))
  if(cKilled):
    statusToCheck.append(str(constants.framesKilled))
  if(cUnassigned):
    statusToCheck.append(str(constants.framesUnassigned))
  if(cHung):
    statusToCheck.append(str(constants.framesHung))

  #debug.info(statusToCheck)

  rows = []
  try:
    if(cAll):
      rows = db_conn.execute("select "+ ",".join(colNamesFrames) +" from frames where id = "+ ids,dictionary=True)
    elif(statusToCheck):
      statusCheck = " or status=".join(statusToCheck)
      rows = db_conn.execute("select "+ ",".join(colNamesFrames) +" from frames where (id = "+ ids +") and (status="+ statusCheck +")",dictionary=True)
    else:
      #debug.info("please check status")
      main_ui.labelTotal.setText(QtWidgets.QApplication.translate("Form", str(0), None))
      timerFramesRefresh.stop()
  except:
    debug.info(str(sys.exc_info()))
    main_ui.labelTotal.setText(QtWidgets.QApplication.translate("Form", str(0), None))
    timerFramesRefresh.stop()
  sFrames = rows
  return

def popTableFrames_thread(main_ui):
  global sFrames
  global timerFramesRefresh
  global colNamesFramesXtra

  debug.info("popTableFrames called!")
  main_ui.tableFrames.clearContents()
  main_ui.tableFrames.setSortingEnabled(False)
  main_ui.tableFrames.resizeColumnsToContents()
  main_ui.tableFrames.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)


  rows = sFrames
  if not rows:
    main_ui.tableFrames.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
    main_ui.tableFrames.setColumnCount(0)
    main_ui.tableFrames.setRowCount(0)
    main_ui.labelTotal.setText(QtWidgets.QApplication.translate("Form", "0", None))
    timerFramesRefresh.stop()
    return()
  selFramesDict = selectedFrames(main_ui)
  selFrames = {}
  for x in selFramesDict:
    try:
      selFrames[x['id']].append(x['frameId'])
    except:
      selFrames[x['id']] = []
      selFrames[x['id']].append(x['frameId'])

  selFramesTid = selFrames.keys()

  colCount = 0


  selTasksDict = selectedTasks(main_ui)
  selTasks = []
  #db_conn = dbRbhus.dbRbhus()
  padDict = {}
  for x in selTasksDict:
    selTasks.append(x['id'])
    padDict[re.sub("^0+","",x['id'])] = 4

  ##debug.info(padDict)
  if(selTasks):
    ids = " or id = ".join(selTasks)
  else:
    main_ui.tableFrames.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
    timerFramesRefresh.stop()
    return()

  findRows = []
  for row in rows:

    sFlag = 0
    for colName in colNamesFrames:
      if str(row[colName]).find(str_convert(main_ui.lineEditSearchFrames.text())) >= 0:
        sFlag = 1
    if(sFlag):
      findRows.append(row)
  rows = findRows


  if(not rows):
    main_ui.tableFrames.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
    timerFramesRefresh.stop()
    return()
  colCount = len(colNamesFrames) + len(colNamesFramesXtra)

  main_ui.tableFrames.setColumnCount(colCount)
  main_ui.tableFrames.setRowCount(len(rows))

  for x in range(0,colCount):
    item = QtWidgets.QTableWidgetItem()
    main_ui.tableFrames.setHorizontalHeaderItem(x, item)
  indx = 0
  for x in colNamesFrames:
    main_ui.tableFrames.horizontalHeaderItem(indx).setText(QtWidgets.QApplication.translate("Form", x, None))
    indx = indx + 1
  for x in colNamesFramesXtra:
    main_ui.tableFrames.horizontalHeaderItem(indx).setText(QtWidgets.QApplication.translate("Form", x, None))
    indx = indx + 1


  indx = 0
  for row in rows:
    item = QtWidgets.QTableWidgetItem()
    main_ui.tableFrames.setVerticalHeaderItem(indx, item)
    colIndx = 0
    for colName in colNamesFrames:
      if(colName == "status"):
        item = QtWidgets.QTableWidgetItem()
        main_ui.tableFrames.setItem(indx, colIndx, item)
        main_ui.tableFrames.item(indx, colIndx).setText(QtWidgets.QApplication.translate("Form", constants.framesStatus[int(row[colName])], None))
        colIndx = colIndx + 1
        continue
      if(colName == "id"):
        item = QtWidgets.QTableWidgetItem()
        main_ui.tableFrames.setItem(indx, colIndx, item)
        main_ui.tableFrames.item(indx, colIndx).setText(QtWidgets.QApplication.translate("Form", str(row[colName]).zfill(4), None))
        colIndx = colIndx + 1
        continue
      if(colName == "frameId"):
        item = QtWidgets.QTableWidgetItem()
        main_ui.tableFrames.setItem(indx, colIndx, item)
        main_ui.tableFrames.item(indx, colIndx).setText(QtWidgets.QApplication.translate("Form", str(row[colName]).zfill(int(padDict[str(row['id'])])), None))
        colIndx = colIndx + 1
        continue
      if(colName == "ram"):
        item = QtWidgets.QTableWidgetItem()
        main_ui.tableFrames.setItem(indx, colIndx, item)
        main_ui.tableFrames.item(indx, colIndx).setText(QtWidgets.QApplication.translate("Form", str(round(float(row[colName])/1024/1024/1024,2)) + "GB", None))
        colIndx = colIndx + 1
        continue
      item = QtWidgets.QTableWidgetItem()
      main_ui.tableFrames.setItem(indx, colIndx, item)
      main_ui.tableFrames.item(indx, colIndx).setText(QtWidgets.QApplication.translate("Form", str(row[colName]), None))
      #debug.info self.tableFrames.item(indx, colIndx).type()
      colIndx = colIndx + 1

    for colName in colNamesFramesXtra:
      if(colName == "timeTaken"):
        import datetime
        nowTemp = datetime.datetime.now()
        now = datetime.datetime(nowTemp.year,nowTemp.month,nowTemp.day,nowTemp.hour,nowTemp.minute,nowTemp.second,0)

        item = QtWidgets.QTableWidgetItem()
        main_ui.tableFrames.setItem(indx, colIndx, item)
        tT = 0
        if(not row['sTime']):
          row['sTime'] = 0
          tT = 0

        if(not row['eTime']):
          row['eTime'] = 0

        if(row['status'] == constants.framesRunning):

          if(row['sTime']):

            tT = now - row['sTime']
          # elif(row['sTime'] >= row['eTime'] ):
          #   import datetime
          #   tT = datetime.datetime.now() - row['sTime']
        else:
          debug.info(row['eTime'])
          debug.info(row['sTime'])
          try:
            if(row['eTime'] < row['sTime']):
              tT = 0
            else:
              tT = row['eTime'] - row['sTime']
          except:
            pass
        main_ui.tableFrames.item(indx, colIndx).setText(QtWidgets.QApplication.translate("Form", str(tT).zfill(int(padDict[str(row['id'])])), None))
        colIndx = colIndx + 1
        continue

      item = QtWidgets.QTableWidgetItem()
      main_ui.tableFrames.setItem(indx, colIndx, item)
      main_ui.tableFrames.item(indx, colIndx).setText(QtWidgets.QApplication.translate("Form", str(row[colName]), None))
      #debug.info self.tableFrames.item(indx, colIndx).type()
      colIndx = colIndx + 1

    if(str(row['id']).zfill(4) in selFramesTid):
      if(str(row['frameId']).zfill(int(padDict[str(row['id'])])) in selFrames[str(row['id']).zfill(int(padDict[str(row['id'])]))]):
        main_ui.tableFrames.selectRow(indx)
    indx = indx + 1
    #debug.info(row['eTime'] - row['sTime'])

  main_ui.labelTotal.setText(QtWidgets.QApplication.translate("Form", str(len(rows)), None))

  main_ui.tableFrames.resizeColumnsToContents()
  main_ui.tableFrames.setSortingEnabled(True)
  QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
  main_ui.tableFrames.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
  timerFramesRefresh.stop()


def selectedTasks(main_ui):
  rowstask=[]
  rowsSelected = []
  rowsModel = main_ui.tableList.selectionModel().selectedRows()

  for idx in rowsModel:
    rowsSelected.append(idx.row())
  colCount = len(colNamesTask)
  for row in rowsSelected:
    singleRow = {}
    for col in range(0,colCount):
      singleRow[colNamesTask[col]] = str_convert(main_ui.tableList.item(row,col).text())
    if(singleRow):
      rowstask.append(singleRow)

  return(rowstask)


def selectedFrames(main_ui):
  rowsframes=[]
  rowsSelected = []
  for idx in main_ui.tableFrames.selectionModel().selectedRows():
    rowsSelected.append(idx.row())
  colCount = len(colNamesFrames)
  for row in rowsSelected:
    singleRow = {}
    for col in range(0,colCount):
      singleRow[colNamesFrames[col]] = str_convert(main_ui.tableFrames.item(row,col).text())
    if(singleRow):
      rowsframes.append(singleRow)

  return(rowsframes)

def getHostIp(hostN):
  try:
    conn = db.connRbhus()
    cursor = conn.cursor(db.dict)
    cursor.execute("select ip from hostInfo where hostName = \'"+ str(hostN) +"\'")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return(rows[0]['ip'])
  except:
    debug.info(str(sys.exc_info()))
    return(0)





# if __name__ == "__main__":
#   import sys
#   app = QtWidgets.QApplication(sys.argv)
#   Form = QtWidgets.QMainWindow()
#   ui = Ui_Form()
#   ui.setupUi(Form)
#   Form.show()
#   sys.exit(app.exec_())


def main_func():
  global app
  app = QtWidgets.QApplication(sys.argv)
  main_ui = uic.loadUi(main_ui_file)
  mainGui(main_ui)
  sys.exit(app.exec_())


if __name__ == '__main__':
  main_func()

