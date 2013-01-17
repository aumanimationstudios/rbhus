#!/usr/bin/python
from PyQt4 import QtCore, QtGui
import glob
import os
import sys
import socket
import time



progPath =  sys.argv[0].split(os.sep)
print progPath
if(len(progPath) > 1):
  pwd = os.sep.join(progPath[0:-1])
  cwd = os.path.abspath(pwd)
else:
  cwd = os.path.abspath(os.getcwd())
  
sys.path.append(cwd.rstrip(os.sep) + os.sep + "lib")

rEc = "rbhusEdit.py"
  
editTaskCmd = cwd.rstrip(os.sep) + os.sep + rEc

print editTaskCmd
import rbhusListMod
print(cwd.rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")
sys.path.append(cwd.rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")
import db
import constants


try:
  _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
  _fromUtf8 = lambda s: s
  

class Ui_Form(rbhusListMod.Ui_mainRbhusList):
  def setupUi(self, Form):
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(_fromUtf8(cwd.rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/rbhus.svg")), QtGui.QIcon.Normal, QtGui.QIcon.On)
    Form.setWindowIcon(icon)
    
    self.colNamesTask = ["id","fileName","camera","outDir","outName","hostGroups","os","fileType","renderer","fRange","afterTasks","priority","submitTime","status","description"]
    self.colNamesFrames = ["id","frameId","batchId","hostName","ram","sTime","eTime","runCount","status"]
    
    
    self.selectedTaskList = []
    rbhusListMod.Ui_mainRbhusList.setupUi(self,Form)
    QtCore.QObject.connect(self.pushRefresh, QtCore.SIGNAL(_fromUtf8("clicked()")), self.popTableList)
    QtCore.QObject.connect(self.tableList, QtCore.SIGNAL(_fromUtf8("itemSelectionChanged()")), self.popTableFrames)
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
    self.tableList.customContextMenuRequested.connect(self.popupTask)
    self.taskHold.clicked.connect(self.holdTask)
    self.taskRerun.clicked.connect(self.rerunTask)
    self.taskActivate.clicked.connect(self.activateTask)
    self.taskEdit.clicked.connect(self.editTask)
    self.taskDelete.clicked.connect(self.delTask)
    
    
    self.frameStop.clicked.connect(self.stopFrame)
    self.frameRerun.clicked.connect(self.rerunFrame)
    self.frameHold.clicked.connect(self.holdFrame)
    
    #self.tableFrames.itemSelectionChanged.connect(self.stopFrame)
    self.timer = QtCore.QTimer()
    self.timer.timeout.connect(self.popTableFrames)
    self.checkRefresh.clicked.connect(self.timeCheck)
    self.lineEditSearch.textChanged.connect(self.popTableList)
    self.popTableList()
    
    
  def popupTask(self, pos):
    menu = QtGui.QMenu()
    test1Action = menu.addAction("test1")
    test2Action = menu.addAction("test2")
    test3Action = menu.addAction("test3")
    
    action = menu.exec_(self.tableList.mapToGlobal(pos))
    if(action == test1Action):
      print("test1")
    if(action == test2Action):
      print("test2")
    if(action == test3Action):
      print("test3")
      
  
  def stopFrame(self):
    selFramesDict = self.selectedFrames()
    selFrames = {}
    for x in selFramesDict:
      if(x['status'] == "running"):
        print self.getHostIp(x['hostName'])
        self.stopFrames(str(self.getHostIp(x['hostName'])),x['id'],x['frameId'])
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
          return()    
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

  def editTask(self):
    selTasksDict = self.selectedTasks()
    selTasks = []
    for x in selTasksDict:
      selTasks.append(x['id'].lstrip("0"))
      
    if(selTasks and (len(selTasks) == 1)):
      os.system(editTaskCmd +" "+ str(selTasks[0]) +"&")
    else:
      print "madness .. too many tasks selected"
  
  def holdTask(self):
    selTasksDict = self.selectedTasks()
    selTasks = []
    for x in selTasksDict:
      selTasks.append(x['id'])
    if(selTasks):
      ids = " or id = ".join(selTasks)
    else:
      return
    ids = " or id=".join(selTasks)
    print ids
    try:
      conn = db.connRbhus()
      cursor = conn.cursor()
      cursor.execute("update tasks set status = "+ str(constants.taskStopped) +" where (id="+ ids +") and ((status != "+ str(constants.taskWaiting) +") and (status != "+ str(constants.taskPending) +"))")
      cursor.close()
      conn.close()
    except:
      print("1 :Error connecting to db :"+ str(sys.exc_info()))
      return()    
    self.popTableList()
    
 
  def delTask(self):
    selTasksDict = self.selectedTasks()
    selTasks = []
    #self.showDialog()
    
    for x in selTasksDict:
      selTasks.append(x['id'])
    if(selTasks):
      ids = " or id = ".join(selTasks)
    else:
      return
    ids = " or id=".join(selTasks)
    print ids
    try:
      conn = db.connRbhus()
      cursor = conn.cursor()
      cursor.execute("delete from tasks where (id="+ ids +") and ((status != "+ str(constants.taskWaiting) +") and (status != "+ str(constants.taskPending) +") and (status != "+ str(constants.taskActive) +"))")
      cursor.close()
      conn.close()
    except:
      print("1 :Error connecting to db :"+ str(sys.exc_info()))
      return()    
    self.popTableList()
    
  
  #def showDialog(self):  
    #self._dialog = QtGui.QDialog()
    #self._dialog.resize(200, 100)
    
    #self._dialog.show()
      
      
    
  def activateTask(self):
    #selTasks = self.selectedTasks()
    selTasksDict = self.selectedTasks()
    selTasks = []
    for x in selTasksDict:
      selTasks.append(x['id'])
    if(selTasks):
      ids = " or id = ".join(selTasks)
    else:
      return
    ids = " or id=".join(selTasks)
    print ids
    try:
      conn = db.connRbhus()
      cursor = conn.cursor()
      cursor.execute("update tasks set status = "+ str(constants.taskActive) +" where (id="+ ids +") and status != "+ str(constants.taskActive))
      cursor.close()
      conn.close()
    except:
      print("1 :Error connecting to db :"+ str(sys.exc_info()))
      return()    
    self.popTableList()
    
    
  def rerunTask(self):
    selTasksDict = self.selectedTasks()
    selTasks = []
    for x in selTasksDict:
      selTasks.append(x['id'])
    if(selTasks):
      ids = " or id = ".join(selTasks)
    else:
      return
    #selTasks = self.selectedTasks()
    ids = " or id=".join(selTasks)
    print ids
    try:
      conn = db.connRbhus()
      cursor = conn.cursor()
      cursor.execute("delete from frames where (id="+ ids +")")
      cursor.execute("update tasks set status = "+ str(constants.taskWaiting) +" where (id="+ ids +")")
      cursor.close()
      conn.close()
    except:
      print("1 :Error connecting to db :"+ str(sys.exc_info()))
      return()    
    self.popTableList()

  
  def stopRunning(self,tableType):
    pass
    
  
  def timeCheck(self):
    cRefresh = self.checkRefresh.isChecked()
    if(cRefresh):
      self.startTimer()
    else:
      self.stopTimer()
  
  def startTimer(self):
    self.timer.start(2000)

  def stopTimer(self):
    self.timer.stop()
  
  def popTableList(self):
    self.tableList.clearContents()
    self.tableList.setSortingEnabled(False)
    self.tableList.resizeColumnsToContents()
    colCount = 0
    
    statusToCheck = []
    cTDone = self.checkTDone.isChecked()
    cTActive = self.checkTActive.isChecked()
    cTHold = self.checkTHold.isChecked()
    cTAutohold = self.checkTAutohold.isChecked()
    cTAll = self.checkTAll.isChecked()
    if(cTDone):
      statusToCheck.append(str(constants.taskDone))
    if(cTActive):
      statusToCheck.append(str(constants.taskActive))
    if(cTHold):
      statusToCheck.append(str(constants.taskStopped))
    if(cTAutohold):
      statusToCheck.append(str(constants.taskAutoStopped))
    
    print(statusToCheck) 
    
    try:
      conn = db.connRbhus()
      cursor = conn.cursor(db.dict)
      if(cTAll):
        cursor.execute("select "+ ",".join(self.colNamesTask) +" from tasks")
      else:
        statusCheck = " or status=".join(statusToCheck)
        cursor.execute("select "+ ",".join(self.colNamesTask) +" from tasks where status="+ statusCheck)
        
      rows = cursor.fetchall()
      cursor.close()
      conn.close()
    except:
      print("Error connecting to db")
      return()
      
    if(not rows):
      return()
    for row in rows:
      colCount = len(row)
      break
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


    indx = 0
    for row in rows:
      sFlag = 0
      for colName in self.colNamesTask:
        if(str(row[colName]).find(str(self.lineEditSearch.text())) >= 0):
          sFlag = 1
        
      if(sFlag):
        item = QtGui.QTableWidgetItem()
        self.tableList.setVerticalHeaderItem(indx, item)
        colIndx = 0
        for colName in self.colNamesTask:
          if(colName == "status"):
            item = QtGui.QTableWidgetItem()
            self.tableList.setItem(indx, colIndx, item)
            self.tableList.item(indx, colIndx).setText(QtGui.QApplication.translate("Form", constants.taskStatus[int(row[colName])], None, QtGui.QApplication.UnicodeUTF8))
            colIndx = colIndx + 1
            continue
          if(colName == "id"):
            item = QtGui.QTableWidgetItem()
            self.tableList.setItem(indx, colIndx, item)
            self.tableList.item(indx, colIndx).setText(QtGui.QApplication.translate("Form", str(row[colName]).zfill(4), None, QtGui.QApplication.UnicodeUTF8))
            colIndx = colIndx + 1
            continue
          
          item = QtGui.QTableWidgetItem()
          self.tableList.setItem(indx, colIndx, item)
          self.tableList.item(indx, colIndx).setText(QtGui.QApplication.translate("Form", str(row[colName]), None, QtGui.QApplication.UnicodeUTF8))
          colIndx = colIndx + 1
        indx = indx + 1

    self.labelTaskTotal.setText(QtGui.QApplication.translate("Form", str(len(rows)), None, QtGui.QApplication.UnicodeUTF8))
    self.tableList.resizeColumnsToContents()
    self.tableList.setSortingEnabled(True)
    
    
  def popTableFrames(self):
    
    self.tableFrames.clearContents()
    self.tableFrames.setSortingEnabled(False)
    self.tableFrames.resizeColumnsToContents()
    colCount = 0
    
    selTasksDict = self.selectedTasks()
    selTasks = []
    for x in selTasksDict:
      selTasks.append(x['id'])
    if(selTasks):
      ids = " or id = ".join(selTasks)
    else:
      return
    
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
    
    
    try:
      rows = []
      if(cAll):
        conn = db.connRbhus()
        cursor = conn.cursor(db.dict)
        cursor.execute("select "+ ",".join(self.colNamesFrames) +" from frames where id = "+ ids)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
      elif(statusToCheck):
        statusCheck = " or status=".join(statusToCheck)
        conn = db.connRbhus()
        cursor = conn.cursor(db.dict)
        cursor.execute("select "+ ",".join(self.colNamesFrames) +" from frames where (id = "+ ids +") and (status="+ statusCheck +")")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
      else:
        #print("please check status")
        self.labelTotal.setText(QtGui.QApplication.translate("Form", str(0), None, QtGui.QApplication.UnicodeUTF8))
        return()
    except:
      print(str(sys.exc_info()))
      self.labelTotal.setText(QtGui.QApplication.translate("Form", str(0), None, QtGui.QApplication.UnicodeUTF8))
      return()
      
    if(not rows):
      return()
    for row in rows:
      colCount = len(row)
      break
      
    self.tableFrames.setColumnCount(colCount)
    self.tableFrames.setRowCount(len(rows))
    
    for x in range(0,colCount):
      item = QtGui.QTableWidgetItem()
      self.tableFrames.setHorizontalHeaderItem(x, item)
    indx = 0
    for x in self.colNamesFrames:
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
          self.tableFrames.item(indx, colIndx).setText(QtGui.QApplication.translate("Form", str(row[colName]).zfill(4), None, QtGui.QApplication.UnicodeUTF8))
          colIndx = colIndx + 1
          continue
        item = QtGui.QTableWidgetItem()
        self.tableFrames.setItem(indx, colIndx, item)
        self.tableFrames.item(indx, colIndx).setText(QtGui.QApplication.translate("Form", str(row[colName]), None, QtGui.QApplication.UnicodeUTF8))
        print self.tableFrames.item(indx, colIndx).type()
        colIndx = colIndx + 1
      indx = indx + 1

    self.labelTotal.setText(QtGui.QApplication.translate("Form", str(len(rows)), None, QtGui.QApplication.UnicodeUTF8))
      
    self.tableFrames.resizeColumnsToContents()
    self.tableFrames.setSortingEnabled(True)
  
    
    
  def selectedTasks(self):
    rowstask=[]
    rowsSelected = []
    for idx in self.tableList.selectionModel().selectedRows():
      rowsSelected.append(idx.row())
    colCount = self.tableList.columnCount()

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
    colCount = self.tableFrames.columnCount()
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
      
      
  def stopFrames(self,hostIp, tId, fId):
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tryCount = 5 
    while(tryCount):
      time.sleep(1)
      try:
        clientSocket.connect((str(hostIp),6660))
        clientSocket.settimeout(30)
        clientSocket.send("MURDER:"+ str(tId).lstrip("0") +"%"+ str(fId).lstrip("0"))
        clientSocket.close()
        break
      except:
        print(str(sys.exc_info()))
        tryCount = tryCount - 1
        clientSocket.close()
        return(1)
    return(0)
      
    
if __name__ == "__main__":
  import sys
  app = QtGui.QApplication(sys.argv)
  Form = QtGui.QMainWindow()
  ui = Ui_Form()
  ui.setupUi(Form)
  Form.show()
  sys.exit(app.exec_())
