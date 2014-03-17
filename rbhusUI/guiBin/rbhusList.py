#!/usr/bin/python
from PyQt4 import QtCore, QtGui
import glob
import os
import sys
import socket
import time
import subprocess
import re

dirSelf = os.path.dirname(os.path.realpath(__file__))
print(dirSelf)
sys.path.append(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep) + os.sep + "lib")

rEc = "rbhusEdit.py"
rEcM = "rbhusEditMulti.py"
rSubmit = "rbhusSubmit.py"
  
editTaskCmd = dirSelf.rstrip(os.sep) + os.sep + rEc
editTaskCmd = editTaskCmd.replace("\\","/")

editTaskMultiCmd = dirSelf.rstrip(os.sep) + os.sep + rEcM
editTaskMultiCmd = editTaskMultiCmd.replace("\\","/")

submitCmd = dirSelf.rstrip(os.sep) + os.sep + rSubmit
submitCmd = submitCmd.replace("\\","/")

print editTaskCmd
import rbhusListMod
print(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")
sys.path.append(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")
import db
import constants
import auth
import dbRbhus
import utils as rUtils

try:
  _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
  _fromUtf8 = lambda s: s
  

class Ui_Form(rbhusListMod.Ui_mainRbhusList):
  def setupUi(self, Form):
    rbhusListMod.Ui_mainRbhusList.setupUi(self,Form)
    
    self.username = None
    self.userProjIds = []
    try:
      self.username = os.environ['rbhus_acl_user'].rstrip().lstrip()
    except:
      pass
    try:
      self.userProjIds = os.environ['rbhus_acl_projIds'].split()
    except:
      pass
    
    self.form = Form
    
    
    icon = QtGui.QIcon()
    iconRefresh = QtGui.QIcon()
    iconTime = QtGui.QIcon()
    iconDate = QtGui.QIcon()
    iconTime.addPixmap(QtGui.QPixmap(_fromUtf8(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/ic_action_time.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
    iconDate.addPixmap(QtGui.QPixmap(_fromUtf8(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/ic_action_go_to_today.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
    iconRefresh.addPixmap(QtGui.QPixmap(_fromUtf8(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/ic_action_refresh.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
    self.taskRefresh.setIcon(iconRefresh)
    self.framesRefresh.setIcon(iconRefresh)
    self.checkRefresh.setIcon(iconTime)
    self.checkDateTask.setIcon(iconDate)
    icon.addPixmap(QtGui.QPixmap(_fromUtf8(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/rbhus.svg")), QtGui.QIcon.Normal, QtGui.QIcon.On)
    Form.setWindowIcon(icon)

    self.taskThreads = []
    
    self.dockWidgetTasks.setTitleBarWidget(self.titleBarWidgetTasks)
    self.dockWidgetFrames.setTitleBarWidget(self.titleBarWidgetFrames)
    self.authL = auth.login()
    self.colNamesTask = ["id","fileName","user","camera","resolution","outDir","outName","hostGroups","os","fileType","layer","renderer","fRange","pad","afterTasks","afterTaskSloppy","priority","submitTime","doneTime","afterTime","status","batch","description","fastAssign"]
    self.colNamesFrames = ["id","frameId","hostName","ram","sTime","eTime","runCount","status","fThreads","efficiency"]
    self.colNamesFramesXtra = ["timeTaken"]
    self.colNamesTaskXtra = ["pending"]
    #self.checkTMine.setChecked(2)
    
    self.selectedTaskList = []
    
    QtCore.QObject.connect(self.framesRefresh, QtCore.SIGNAL(_fromUtf8("clicked()")), self.popTableFrames)
    QtCore.QObject.connect(self.tableList, QtCore.SIGNAL(_fromUtf8("itemSelectionChanged()")), self.timeFramesCheck)
    QtCore.QObject.connect(self.checkAll, QtCore.SIGNAL(_fromUtf8("clicked()")), self.popTableFrames)
    QtCore.QObject.connect(self.checkDone, QtCore.SIGNAL(_fromUtf8("clicked()")), self.popTableFrames)
    QtCore.QObject.connect(self.checkAssigned, QtCore.SIGNAL(_fromUtf8("clicked()")), self.popTableFrames)
    QtCore.QObject.connect(self.checkAutohold, QtCore.SIGNAL(_fromUtf8("clicked()")), self.popTableFrames)
    QtCore.QObject.connect(self.checkFailed, QtCore.SIGNAL(_fromUtf8("clicked()")), self.popTableFrames)
    QtCore.QObject.connect(self.checkKilled, QtCore.SIGNAL(_fromUtf8("clicked()")), self.popTableFrames)
    QtCore.QObject.connect(self.checkRunning, QtCore.SIGNAL(_fromUtf8("clicked()")), self.popTableFrames)
    QtCore.QObject.connect(self.checkHold, QtCore.SIGNAL(_fromUtf8("clicked()")), self.popTableFrames)
    QtCore.QObject.connect(self.checkHung, QtCore.SIGNAL(_fromUtf8("clicked()")), self.popTableFrames)
    self.checkUnassigned.clicked.connect(self.popTableFrames)
    self.checkTAll.clicked.connect(self.popTableList)
    self.checkTActive.clicked.connect(self.popTableList)
    self.checkTAutohold.clicked.connect(self.popTableList)
    self.checkTDone.clicked.connect(self.popTableList)
    self.checkTHold.clicked.connect(self.popTableList)
    self.checkTMine.clicked.connect(self.popTableList)
    self.checkDateTask.clicked.connect(self.checkDateTaskFunc)
    self.radioAfter.clicked.connect(self.popTableList)
    self.radioDone.clicked.connect(self.popTableList)
    self.radioSubmit.clicked.connect(self.popTableList)
    self.dateEditTaskFrom.dateChanged.connect(self.popTableList)
    self.dateEditTaskTo.dateChanged.connect(self.popTableList)
    self.tableList.customContextMenuRequested.connect(self.popupTask)
    self.tableFrames.customContextMenuRequested.connect(self.popupFrames)
    self.taskRefresh.clicked.connect(self.popTableList)
    self.timer = QtCore.QTimer()
    self.timerFramesRefresh = QtCore.QTimer()
    self.timerFramesRefresh.timeout.connect(self.popTableFrames)
    self.timer.timeout.connect(self.popTableFrames)
    self.checkRefresh.clicked.connect(self.timeCheck)
    self.lineEditSearch.returnPressed.connect(self.popTableList)
    self.lineEditSearchFrames.returnPressed.connect(self.popTableFrames)
    
    self.checkDateTaskFunc()
    self.labelUser.setText(os.environ['rbhus_acl_user'])
    self.taskSearchTime = 0.0
    self.dateEditTaskFrom.setDate(QtCore.QDate.currentDate())
    self.dateEditTaskTo.setDate(QtCore.QDate.currentDate())
    
    self.popTableList()
  
  
  
  
  def report_thread(self):
    selTasksDict = self.selectedTasks()
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
        
          
              
              
    
    
  
  def checkDateTaskFunc(self):
    if(self.checkDateTask.isChecked()):
      self.dateEditTaskFrom.setEnabled(True)
      self.dateEditTaskTo.setEnabled(True)
      self.groupBoxTaskDate.setVisible(True)
    else:
      self.dateEditTaskFrom.setEnabled(False)
      self.dateEditTaskTo.setEnabled(False)
      self.groupBoxTaskDate.setVisible(False)
  
  
  
  def previewTask(self):
    selTasksDict = self.selectedTasks()
    selTasks = []
    db_conn = dbRbhus.dbRbhus()
    if(selTasksDict):
      for x in selTasksDict:
        tD = db_conn.getTaskDetails(x['id'])
        oDir = tD['outDir']
        fila = QtGui.QFileDialog.getOpenFileNames(directory=oDir,options=QtGui.QFileDialog.DontUseNativeDialog)
        if(fila):
          for fi in fila:
            if(sys.platform.find("win") >= 0):
              subprocess.Popen(["x:/standard/template/djv-0.8.3-x64/bin/djv_view.exe",str(fi.replace("\\","/")),"-file_seq_auto","true","-file_cache","true"])
            elif(sys.platform.find("linux") >= 0):
              subprocess.Popen(["/usr/local/bin/djv_view",str(fi),"-file_seq_auto","true","-file_cache","true"])
            print(fi)
          
        
  def previewFrame(self):
    selFramesDict = self.selectedFrames()
    selFrames = {}
    db_conn = dbRbhus.dbRbhus()
    for x in selFramesDict:
      tD = db_conn.getTaskDetails(x['id'])
      oDir = tD['outDir']
      print("*"+ str(x['frameId']).zfill(tD['pad']) +"*")
      fila = QtGui.QFileDialog.getOpenFileNames(directory=oDir,filter="*"+ str(x['frameId']).zfill(tD['pad']) +"*",options=QtGui.QFileDialog.DontUseNativeDialog)
      if(fila):
        print(fila)
        for fi in fila:
          if(sys.platform.find("win") >= 0):
            subprocess.Popen(["x:/standard/template/djv-0.8.3-x64/bin/djv_view.exe",str(fi.replace("\\","/")),"-file_seq_auto","false","-file_cache","true"])
          elif(sys.platform.find("linux") >= 0):
            subprocess.Popen(["/usr/local/bin/djv_view",str(fi),"-file_seq_auto","false","-file_cache","true"])
          print(fi)
            
  
  def popupTask(self, pos):
    menu = QtGui.QMenu()
    test1Action = menu.addAction("activate")
    test2Action = menu.addAction("hold")
    test3Action = menu.addAction("rerun")
    test4Action = menu.addAction("edit")
    test5Action = menu.addAction("open dir")
    test6Action = menu.addAction("copy/submit")
    test7Action = menu.addAction("fastAssign enable")
    test8Action = menu.addAction("fastAssign disable")
    test9Action = menu.addAction("delete")
    
    action = menu.exec_(self.tableList.mapToGlobal(pos))
    if(action == test1Action):
      self.activateTask()
    if(action == test2Action):
      self.holdTask()
    if(action == test3Action):
      self.rerunTask()
    if(action == test4Action):
      self.editTask()
    if(action == test5Action):
      self.previewTask()
    if(action == test6Action):
      self.copySubmit()
    if(action == test7Action):
      self.fastAssignFunc(e=1)
    if(action == test8Action):
      self.fastAssignFunc(e=0)
    if(action == test9Action):
      self.delTask()
      
      
      
  def fastAssignFunc(self,e=0):
    selTasksDict = self.selectedTasks()
    selTasks = []
    if(selTasksDict):
      for x in selTasksDict:
        selTasks.append(x['id'].lstrip("0"))
      if(selTasks):
        for x in selTasks:
          print(x)
          tsks = rUtils.tasks(tId=x)
          if(tsks):
            tsks.fastAssign(enable=e)
      return(1)
    return(0)
        
        
      

  def popupFrames(self, pos):
    selFramesDict = self.selectedFrames()
    menu = QtGui.QMenu()
    db_conn = dbRbhus.dbRbhus()
    test1Action = menu.addAction("check log")
    test3Action = menu.addAction("hold")
    test4Action = menu.addAction("rerun")
    test5Action = menu.addAction("check frame")
    test2Action = menu.addAction("kill")
    test6Action = menu.addAction("kill/hold")
    
    action = menu.exec_(self.tableFrames.mapToGlobal(pos))
    if(action == test1Action):
      for x in selFramesDict:
        
        fInfos = db_conn.getFrameInfo(x['id'],x['frameId'])
        if(fInfos):
          #print(fInfos)
          print("log file : "+ str(fInfos['logFile']))
          openP = subprocess.Popen([sys.executable,dirSelf.rstrip(os.sep) + os.sep + "rbhusReadText.py",fInfos['logFile']])
          
    if(action == test2Action):
      self.stopFrame()
    if(action == test3Action):
      self.holdFrame()
    if(action == test4Action):
      self.rerunFrame()
    if(action == test5Action):
      self.previewFrame()
    if(action == test6Action):
      self.killHoldFrame()
  
  def stopFrame(self):
    selFramesDict = self.selectedFrames()
    selFrames = {}
    db_conn = dbRbhus.dbRbhus()
    for x in selFramesDict:
      if(x['status'] == "running"):
        print self.getHostIp(x['hostName'])
        db_conn.stopFrames(str(self.getHostIp(x['hostName'])),x['id'],x['frameId'])
      else:
        print(str(x['id']) +"%"+ str(x['frameId']) +" not able to murder since it is running")
    self.popTableFrames()
        
  def killHoldFrame(self):
    selFramesDict = self.selectedFrames()
    selFrames = {}
    db_conn = dbRbhus.dbRbhus()
    for x in selFramesDict:
      if(x['status'] == "running"):
        print self.getHostIp(x['hostName'])
        db_conn.stopHoldFrames(str(self.getHostIp(x['hostName'])),x['id'],x['frameId'])
      else:
        print(str(x['id']) +"%"+ str(x['frameId']) +" not able to murder since it is running")
    self.popTableFrames()
  
  def rerunFrame(self):
    selFramesDict = self.selectedFrames()
    selFrames = {}
    for x in selFramesDict:
      if((x['status'] != "running") and (x['status'] != "assigned") and (x['status'] != "pending")):
        try:
          selFrames[x['id']].append(x['frameId'])
        except:
          selFrames[x['id']] = []
          selFrames[x['id']].append(x['frameId'])
      else:
        print(str(x['id']) +"%"+ str(x['frameId']) +" cannot rerun frames that are already running. please stop and rerun them")
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
          print("1 :Error connecting to db :"+ str(sys.exc_info()))
          return(0)    
    self.popTableFrames()
    
  
  def holdFrame(self):
    selFramesDict = self.selectedFrames()
    selFrames = {}
    for x in selFramesDict:
      if((x['status'] != "running") and (x['status'] != "assigned") and (x['status'] != "pending")):
        try:
          selFrames[x['id']].append(x['frameId'])
        except:
          selFrames[x['id']] = []
          selFrames[x['id']].append(x['frameId'])
      else:
        print(str(x['id']) +"%"+ str(x['frameId']) +" cannot hold frames that are running. please stop them before holding them")
        
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
          print("1 :Error connecting to db :"+ str(sys.exc_info()))
          return()    
    self.popTableFrames()

  
  def copySubmit(self):
    selTasksDict = self.selectedTasks()
    selTasks = []
    for x in selTasksDict:
      selTasks.append(x['id'].lstrip("0"))
    
    
    if(len(selTasks) == 1):
      try:
        subprocess.Popen([sys.executable,submitCmd,str(selTasks[0])])
      except:
        print(str(sys.exc_info()))
    else:
      print("wtf . cannot copy from multiple tasks!")
  
  
  def editTask(self):
    selTasksDict = self.selectedTasks()
    selTasks = []
    for x in selTasksDict:
      selTasks.append(x['id'].lstrip("0"))
    if(len(selTasks) > 1):
      try:
        subprocess.Popen([sys.executable,editTaskMultiCmd,str(",".join(selTasks))])
      except:
        print(str(sys.exc_info()))
    else:
      try:
        subprocess.Popen([sys.executable,editTaskCmd,str(selTasks[0])])
      except:
        print(str(sys.exc_info()))
  


  def holdTask(self):
    selTasksDict = self.selectedTasks()
    selTasks = []
    db_conn = dbRbhus.dbRbhus()
    if(selTasksDict):
      for x in selTasksDict:
        t = rUtils.tasks(str(x['id']).lstrip("0"))
        t.holdTask()
    self.popTableList()
    
 
  def delTask(self):
    selTasksDict = self.selectedTasks()
    selTasks = []
    #self.showDialog()
    db_conn = dbRbhus.dbRbhus()
    if(selTasksDict):
      for x in selTasksDict:
        t = rUtils.tasks(str(x['id']).lstrip("0"))
        t.remove()
    self.popTableList()
    
      
  def activateTask(self):
    selTasksDict = self.selectedTasks()
    selTasks = []
    for x in selTasksDict:
      t = rUtils.tasks(str(x['id']).lstrip("0"))
      t.activateTask()
    self.popTableList()
    
    
  def rerunTask(self):
    selTasksDict = self.selectedTasks()
    selTasks = []
    #self.showDialog()
    db_conn = dbRbhus.dbRbhus()
    if(selTasksDict):
      for x in selTasksDict:
        t = rUtils.tasks(str(x['id']).lstrip("0"))
        t.rerunTask()
    self.popTableList()
    

  
  def stopRunning(self,tableType):
    pass
    
  def timeFramesCheck(self):
    if(self.timerFramesRefresh.isActive()):
      self.timerFramesRefresh.stop()
      self.timerFramesRefresh.start(2000)
    else:
      self.timerFramesRefresh.start(2000)
      
      
  
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
  
  
  def popTableList(self):
    taskThread = QtCore.QThread(parent=self.form)
    #if(self.taskThreads):
      #tTs = self.taskThreads
      #for x in tTs:
        #if(x.isRunning()):
          #x.terminate()
          #try:
            #self.taskThreads.remove(x)
          #except:
            #print(str(sys.exc_info()))
          #print("terminating :"+ str(x))
      #self.taskThreads = []
      #time.sleep(0.5)
          
      
    taskThread.run = self.selectTasks
    taskThread.finished.connect(self.popTableList_thread)
    self.tableList.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.WaitCursor))
    self.groupBoxTask.setEnabled(False)
    self.groupBoxTaskDate.setEnabled(False)
    taskThread.start()
    #self.taskThreads.append(taskThread)
  
  
  def selectTasks(self):
    self.pendFrames = {}
    self.selTasks = []
    statusToCheck = []
    cTDone = self.checkTDone.isChecked()
    cTActive = self.checkTActive.isChecked()
    cTHold = self.checkTHold.isChecked()
    cTAutohold = self.checkTAutohold.isChecked()
    cTAll = self.checkTAll.isChecked()
    cTMine = self.checkTMine.isChecked()
    timeS = ""
    if(self.checkDateTask.isChecked()):
      fromT = "'"+ str(self.dateEditTaskFrom.date().year()) +"-"+ str(self.dateEditTaskFrom.date().month()) +"-"+ str(self.dateEditTaskFrom.date().day()) +"'"
      toT = "'"+ str(self.dateEditTaskTo.date().year()) +"-"+ str(self.dateEditTaskTo.date().month()) +"-"+ str(self.dateEditTaskTo.date().day()) +"'"
      if(self.radioSubmit.isChecked()):
        timeS = " and (submitTime between "+ fromT +" and "+ toT +")"
      elif(self.radioDone.isChecked()):
        timeS = " and (doneTime between "+ fromT +" and "+ toT +")"
      elif(self.radioAfter.isChecked()):
        timeS = " and (afterTime between "+ fromT +" and "+ toT +")"
    if(cTDone):
      statusToCheck.append(str(constants.taskDone))
    if(cTActive):
      statusToCheck.append(str(constants.taskActive))
    if(cTHold):
      statusToCheck.append(str(constants.taskStopped))
    if(cTAutohold):
      statusToCheck.append(str(constants.taskAutoStopped))
    print("FUCK U 4")
    db_conn = dbRbhus.dbRbhus()
    rows = []
    try:
      if(cTAll):
        if(cTMine):
          rows = db_conn.execute("select "+ ",".join(self.colNamesTask) +" from tasks where user='"+ str(self.username) +"'"+ timeS,dictionary=True)
        else:
          rows = db_conn.execute("select "+ ",".join(self.colNamesTask) +" from tasks"+ timeS,dictionary=True)
      else:
        statusCheck = " or status=".join(statusToCheck)
        if(cTMine):
          rows = db_conn.execute("select "+ ",".join(self.colNamesTask) +" from tasks where (status="+ statusCheck +") and user='"+ str(self.username) +"'"+ timeS,dictionary=True)
        else:
          rows = db_conn.execute("select "+ ",".join(self.colNamesTask) +" from tasks where (status="+ statusCheck +")"+ timeS,dictionary=True)
    except:
      print("Error connecting to db "+ str(sys.exc_info()))
    
    if(rows):
      for row in rows:
        self.pendFrames[row['id']] = db_conn.getUnassignedFramesCount(row['id'])
    self.selTasks = rows
    
    #self.tableList.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
  
  
  def popTableList_thread(self):
    #self.tableList.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.WaitCursor))
    
    tSeletected = self.selectedTasks()
    tSelect = []
    if(tSeletected):
      for x in tSeletected:
        tSelect.append(x['id'])
    
    self.tableList.clearContents()
    self.tableList.setSortingEnabled(False)
    self.tableList.resizeColumnsToContents()
    self.tableList.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
    colCount = 0
    rows = self.selTasks
    
    if(not rows):
      self.tableList.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
      self.tableList.setColumnCount(0)
      self.tableList.setRowCount(0)
      self.labelTaskTotal.setText(QtGui.QApplication.translate("Form", str(0), None, QtGui.QApplication.UnicodeUTF8))
      self.groupBoxTask.setEnabled(True)
      self.groupBoxTaskDate.setEnabled(True)
      return()
    colCount = len(self.colNamesTask) + len(self.colNamesTaskXtra)
      
    findRows = []
    
    for row in rows:
      sFlag = 0
      for colName in self.colNamesTask:
        if(str(row[colName]).find(str(self.lineEditSearch.text())) >= 0):
          sFlag = 1
      if(sFlag):
        findRows.append(row)
    rows = findRows
     
    
    self.labelTaskTotal.setText(QtGui.QApplication.translate("Form", str(len(rows)), None, QtGui.QApplication.UnicodeUTF8)) 
    self.tableList.setColumnCount(colCount)
    self.tableList.setRowCount(len(rows))
    
    for x in range(0,colCount):
      item = QtGui.QTableWidgetItem()
      self.tableList.setHorizontalHeaderItem(x, item)
    indx = 0
    for x in self.colNamesTask:
      self.tableList.horizontalHeaderItem(indx).setText(QtGui.QApplication.translate("Form", x, None, QtGui.QApplication.UnicodeUTF8))
      indx = indx + 1
      
    for x in self.colNamesTaskXtra:
      self.tableList.horizontalHeaderItem(indx).setText(QtGui.QApplication.translate("Form", x, None, QtGui.QApplication.UnicodeUTF8))
      indx = indx + 1


    indx = 0
    for row in rows:
      #sFlag = 0
      #for colName in self.colNamesTask:
        #if(str(row[colName]).find(str(self.lineEditSearch.text())) >= 0):
          #sFlag = 1
        
      #if(sFlag):
      item = QtGui.QTableWidgetItem()
      self.tableList.setVerticalHeaderItem(indx, item)
      colIndx = 0
      for colName in self.colNamesTask:
        item = QtGui.QTableWidgetItem()
        item.setToolTip(str(row['id']) +":"+ str(row['fileName']))
        if(colName == "status"):
          self.tableList.setItem(indx, colIndx, item)
          self.tableList.item(indx, colIndx).setText(QtGui.QApplication.translate("Form", constants.taskStatus[int(row[colName])], None, QtGui.QApplication.UnicodeUTF8))
          colIndx = colIndx + 1
          continue
        if(colName == "id"):
          self.tableList.setItem(indx, colIndx, item)
          self.tableList.item(indx, colIndx).setText(QtGui.QApplication.translate("Form", str(row[colName]).zfill(4), None, QtGui.QApplication.UnicodeUTF8))
          if(str(row[colName]).zfill(4) in tSelect):
            self.tableList.selectRow(indx)
          colIndx = colIndx + 1
          continue
        
        
        self.tableList.setItem(indx, colIndx, item)
        self.tableList.item(indx, colIndx).setText(QtGui.QApplication.translate("Form", str(row[colName]), None, QtGui.QApplication.UnicodeUTF8))
        colIndx = colIndx + 1
      for colName in self.colNamesTaskXtra:
        item = QtGui.QTableWidgetItem()
        item.setToolTip(str(row['id']) +":"+ str(row['fileName']))
        if(colName == "pending"):
          self.tableList.setItem(indx, colIndx, item)
          totalPend = 0
          #pendFrames = dbconn.getUnassignedFramesCount(row['id'])
          try:
            totalPend = self.pendFrames[row['id']][-1]['count(*)'] 
          except:
            pass
          self.tableList.item(indx, colIndx).setText(QtGui.QApplication.translate("Form", str(totalPend), None, QtGui.QApplication.UnicodeUTF8))
          colIndx = colIndx + 1
          continue
        self.tableList.setItem(indx, colIndx, item)
        self.tableList.item(indx, colIndx).setText(QtGui.QApplication.translate("Form", str(row[colName]), None, QtGui.QApplication.UnicodeUTF8))
        colIndx = colIndx + 1
      
      indx = indx + 1

    self.labelTaskTotal.setText(QtGui.QApplication.translate("Form", str(len(rows)), None, QtGui.QApplication.UnicodeUTF8))
    self.tableList.resizeColumnsToContents()
    self.tableList.setSortingEnabled(True)
    
    self.tableList.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
    self.tableList.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
    self.groupBoxTask.setEnabled(True)
    self.groupBoxTaskDate.setEnabled(True)
    #self.popTableFrames()
    
    
  def refresh(self):
    self.popTableList()
    self.popTableFrames()
    
  
  def popTableFrames(self):
    hf = QtCore.QThread(parent=self.form)
    hf.run = self.selectFrames
    hf.finished.connect(self.popTableFrames_thread)
    self.tableFrames.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.WaitCursor))
    hf.start()
    
  
  def selectFrames(self):
    selTasksDict = self.selectedTasks()
    selTasks = []
    db_conn = dbRbhus.dbRbhus()
    padDict = {}
    for x in selTasksDict:
      selTasks.append(x['id'])
      padDict[re.sub("^0+","",x['id'])] = 4
      
    #print(padDict)  
    if(selTasks):
      ids = " or id = ".join(selTasks)
    else:
      self.timerFramesRefresh.stop()
      return()
    
    statusToCheck = []
    cDone = self.checkDone.isChecked()
    cAssigned = self.checkAssigned.isChecked()
    cUnassigned = self.checkUnassigned.isChecked()
    cRun = self.checkRunning.isChecked()
    cFailed = self.checkFailed.isChecked()
    cHold = self.checkHold.isChecked()
    cAutohold = self.checkAutohold.isChecked()
    cKilled = self.checkKilled.isChecked()
    cHung =  self.checkHung.isChecked()
    cAll = self.checkAll.isChecked()
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
    
    #print(statusToCheck)
    
    rows = []
    try:
      if(cAll):
        rows = db_conn.execute("select "+ ",".join(self.colNamesFrames) +" from frames where id = "+ ids,dictionary=True)
      elif(statusToCheck):
        statusCheck = " or status=".join(statusToCheck)
        rows = db_conn.execute("select "+ ",".join(self.colNamesFrames) +" from frames where (id = "+ ids +") and (status="+ statusCheck +")",dictionary=True)
      else:
        #print("please check status")
        self.labelTotal.setText(QtGui.QApplication.translate("Form", str(0), None, QtGui.QApplication.UnicodeUTF8))
        self.timerFramesRefresh.stop()
    except:
      print(str(sys.exc_info()))
      self.labelTotal.setText(QtGui.QApplication.translate("Form", str(0), None, QtGui.QApplication.UnicodeUTF8))
      self.timerFramesRefresh.stop()
    self.sFrames = rows 
  
  
  def popTableFrames_thread(self):
    print("popTableFrames called!")
    self.tableFrames.clearContents()
    self.tableFrames.setSortingEnabled(False)
    self.tableFrames.resizeColumnsToContents()
    self.tableFrames.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
    
    
    rows = self.sFrames
    if(not rows):
      self.tableFrames.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
      self.tableFrames.setColumnCount(0)
      self.tableFrames.setRowCount(0)
      self.labelTotal.setText(QtGui.QApplication.translate("Form", "0", None, QtGui.QApplication.UnicodeUTF8))
      self.timerFramesRefresh.stop()
      return()
    selFramesDict = self.selectedFrames()
    selFrames = {}
    for x in selFramesDict:
      try:
        selFrames[x['id']].append(x['frameId'])
      except:
        selFrames[x['id']] = []
        selFrames[x['id']].append(x['frameId'])
    
    selFramesTid = selFrames.keys()
    
    colCount = 0
    

    selTasksDict = self.selectedTasks()
    selTasks = []
    #db_conn = dbRbhus.dbRbhus()
    padDict = {}
    for x in selTasksDict:
      selTasks.append(x['id'])
      padDict[re.sub("^0+","",x['id'])] = 4
      
    ##print(padDict)  
    if(selTasks):
      ids = " or id = ".join(selTasks)
    else:
      self.tableFrames.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
      self.timerFramesRefresh.stop()
      return()
    
    findRows = []
    for row in rows:
      
      sFlag = 0
      for colName in self.colNamesFrames:
        if(str(row[colName]).find(str(self.lineEditSearchFrames.text())) >= 0):
          sFlag = 1
      if(sFlag):
        findRows.append(row)
    rows = findRows   
    
    
    if(not rows):
      self.tableFrames.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
      self.timerFramesRefresh.stop()
      return()
    colCount = len(self.colNamesFrames) + len(self.colNamesFramesXtra)
      
    self.tableFrames.setColumnCount(colCount)
    self.tableFrames.setRowCount(len(rows))
    
    for x in range(0,colCount):
      item = QtGui.QTableWidgetItem()
      self.tableFrames.setHorizontalHeaderItem(x, item)
    indx = 0
    for x in self.colNamesFrames:
      self.tableFrames.horizontalHeaderItem(indx).setText(QtGui.QApplication.translate("Form", x, None, QtGui.QApplication.UnicodeUTF8))
      indx = indx + 1
    for x in self.colNamesFramesXtra:
      self.tableFrames.horizontalHeaderItem(indx).setText(QtGui.QApplication.translate("Form", x, None, QtGui.QApplication.UnicodeUTF8))
      indx = indx + 1


    indx = 0
    for row in rows:
      item = QtGui.QTableWidgetItem()
      self.tableFrames.setVerticalHeaderItem(indx, item)
      colIndx = 0
      for colName in self.colNamesFrames:
        if(colName == "status"):
          item = QtGui.QTableWidgetItem()
          self.tableFrames.setItem(indx, colIndx, item)
          self.tableFrames.item(indx, colIndx).setText(QtGui.QApplication.translate("Form", constants.framesStatus[int(row[colName])], None, QtGui.QApplication.UnicodeUTF8))
          colIndx = colIndx + 1
          continue
        if(colName == "id"):
          item = QtGui.QTableWidgetItem()
          self.tableFrames.setItem(indx, colIndx, item)
          self.tableFrames.item(indx, colIndx).setText(QtGui.QApplication.translate("Form", str(row[colName]).zfill(4), None, QtGui.QApplication.UnicodeUTF8))
          colIndx = colIndx + 1
          continue
        if(colName == "frameId"):
          item = QtGui.QTableWidgetItem()
          self.tableFrames.setItem(indx, colIndx, item)
          self.tableFrames.item(indx, colIndx).setText(QtGui.QApplication.translate("Form", str(row[colName]).zfill(int(padDict[str(row['id'])])), None, QtGui.QApplication.UnicodeUTF8))
          colIndx = colIndx + 1
          continue
        if(colName == "ram"):
          item = QtGui.QTableWidgetItem()
          self.tableFrames.setItem(indx, colIndx, item)
          self.tableFrames.item(indx, colIndx).setText(QtGui.QApplication.translate("Form", str(round(float(row[colName])/1024/1024/1024,2)) + "GB", None, QtGui.QApplication.UnicodeUTF8))
          colIndx = colIndx + 1
          continue
        item = QtGui.QTableWidgetItem()
        self.tableFrames.setItem(indx, colIndx, item)
        self.tableFrames.item(indx, colIndx).setText(QtGui.QApplication.translate("Form", str(row[colName]), None, QtGui.QApplication.UnicodeUTF8))
        #print self.tableFrames.item(indx, colIndx).type()
        colIndx = colIndx + 1
        
      for colName in self.colNamesFramesXtra:
        if(colName == "timeTaken"):
          item = QtGui.QTableWidgetItem()
          self.tableFrames.setItem(indx, colIndx, item)
          tT = 0
          if(not row['sTime']):
            tT = 0
          if(not row['eTime']):
            row['eTime'] = 0
            
          elif(not row['eTime'] and row['sTime'] and (row['status'] == constants.framesRunning)):
            tT = 0
          elif(row['sTime'] >= row['eTime']):
            tT = 0
          else:
            tT = row['eTime'] - row['sTime']
          self.tableFrames.item(indx, colIndx).setText(QtGui.QApplication.translate("Form", str(tT).zfill(int(padDict[str(row['id'])])), None, QtGui.QApplication.UnicodeUTF8))
          colIndx = colIndx + 1
          continue
        
        item = QtGui.QTableWidgetItem()
        self.tableFrames.setItem(indx, colIndx, item)
        self.tableFrames.item(indx, colIndx).setText(QtGui.QApplication.translate("Form", str(row[colName]), None, QtGui.QApplication.UnicodeUTF8))
        #print self.tableFrames.item(indx, colIndx).type()
        colIndx = colIndx + 1
        
      if(str(row['id']).zfill(4) in selFramesTid):
        if(str(row['frameId']).zfill(int(padDict[str(row['id'])])) in selFrames[str(row['id']).zfill(int(padDict[str(row['id'])]))]):
          self.tableFrames.selectRow(indx)
      indx = indx + 1
      #print(row['eTime'] - row['sTime'])

    self.labelTotal.setText(QtGui.QApplication.translate("Form", str(len(rows)), None, QtGui.QApplication.UnicodeUTF8))
    
    self.tableFrames.resizeColumnsToContents()
    self.tableFrames.setSortingEnabled(True)
    QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
    self.tableFrames.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
    self.timerFramesRefresh.stop()
    
    
  def selectedTasks(self):
    rowstask=[]
    rowsSelected = []
    rowsModel = self.tableList.selectionModel().selectedRows()
    
    for idx in rowsModel:
      rowsSelected.append(idx.row())
    colCount = len(self.colNamesTask)
    for row in rowsSelected:
      singleRow = {}
      for col in range(0,colCount):
        singleRow[self.colNamesTask[col]] = str(self.tableList.item(row,col).text())
      if(singleRow):
        rowstask.append(singleRow)

    return(rowstask)
    
    
  def selectedFrames(self):
    rowsframes=[]
    rowsSelected = []
    for idx in self.tableFrames.selectionModel().selectedRows():
      rowsSelected.append(idx.row())
    colCount = len(self.colNamesFrames)
    for row in rowsSelected:
      singleRow = {}
      for col in range(0,colCount):
        singleRow[self.colNamesFrames[col]] = str(self.tableFrames.item(row,col).text())
      if(singleRow):
        rowsframes.append(singleRow)

    return(rowsframes)
    
  def getHostIp(self, hostN):
    try:
      conn = db.connRbhus()
      cursor = conn.cursor(db.dict)
      cursor.execute("select ip from hostInfo where hostName = \'"+ str(hostN) +"\'")
      rows = cursor.fetchall()
      cursor.close()
      conn.close()
      return(rows[0]['ip'])
    except:
      print(str(sys.exc_info()))
      return(0)
      
      
  
      
    
if __name__ == "__main__":
  import sys
  app = QtGui.QApplication(sys.argv)
  Form = QtGui.QMainWindow()
  ui = Ui_Form()
  ui.setupUi(Form)
  Form.show()
  sys.exit(app.exec_())
