#!/usr/bin/python
from PyQt4 import QtCore, QtGui
import glob
import os
import sys
import socket
import time
import subprocess

hName = socket.gethostname()
progPath =  sys.argv[0].split(os.sep)
print progPath
if(len(progPath) > 1):
  pwd = os.sep.join(progPath[0:-1])
  cwd = os.path.abspath(pwd)
else:
  cwd = os.path.abspath(os.getcwd())
  
sys.path.append(cwd.rstrip(os.sep) + os.sep + "lib")

if(sys.platform.find("win") >= 0):
  rEc = "rbhusHostEdit.py"
elif(sys.platform.find("linux") >= 0):
  rEc = "rbhusHostEdit.py"
  
hostEditCmd = cwd.rstrip(os.sep) + os.sep + rEc

print hostEditCmd
import rbhusHostMod
print(cwd.rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")
sys.path.append(cwd.rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")
import db
import dbRbhus
import constants

dbconn = dbRbhus.dbRbhus()

try:
  _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
  _fromUtf8 = lambda s: s
  

class Ui_Form(rbhusHostMod.Ui_MainWindow):
  def setupUi(self, Form):
    rbhusHostMod.Ui_MainWindow.setupUi(self,Form)
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(_fromUtf8(cwd.rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/rbhus.svg")), QtGui.QIcon.Normal, QtGui.QIcon.On)
    Form.setWindowIcon(icon)
    self.colNamesHost = ["hostInfo.ip","hostInfo.hostName","hostInfo.totalRam","hostInfo.totalCpus","hostInfo.status as status","hostInfo.os","hostAlive.status as alive","hostResource.freeCpus","hostResource.load1","hostInfo.groups"]
    self.popTableHost()
    #self.pushDisable.clicked.connect(self.hostDisable)
    #self.pushEnable.clicked.connect(self.hostEnable)
    self.pushRefresh.clicked.connect(self.popTableHost)
    self.pushLocalStop.clicked.connect(self.hostLocalStop)
    self.pushLocalEnable.clicked.connect(self.hostLocalEnable)
    self.tableHost.customContextMenuRequested.connect(self.popupHost)
  
  
  
  def popupHost(self, pos):
    menu = QtGui.QMenu()
    test1Action = menu.addAction("edit")
    test2Action = menu.addAction("disable")
    test3Action = menu.addAction("enable")
    test4Action = menu.addAction("stop")
    
    
    action = menu.exec_(self.tableHost.mapToGlobal(pos))
    if(action == test1Action):
      #print("test1")
      self.hostEdit()
    if(action == test2Action):
      #print("test2")
      self.hostDisable()
    if(action == test3Action):
      #print("test3")
      self.hostEnable()
    if(action == test4Action):
      #print("test4")
      self.hostStop()
      
      
  def hostEdit(self):
    selHostsDict = self.selectedHosts()
    selHosts = []
    for x in selHostsDict:
      selHosts.append(x['hostInfo.ip'].lstrip("0"))
    
    
    if(selHosts):
      for sT in selHosts:
        try:
          subprocess.Popen([sys.executable,hostEditCmd,str(sT)])
        except:
          print(str(sys.exc_info()))
          
          
  def hostStop(self):
    hosts = self.selectedHosts()
    for h in hosts:
      try:
        rFrames = dbconn.execute("select * from frames where status = "+ str(constants.framesRunning) +" and hostName = \'"+ str(h['hostInfo.hostName']) +"\'", dictionary=True)
      except:
        print(str(sys.exc_info()))
        continue
      if(rFrames):
        for rF in rFrames:
          dbconn.stopFrames(h['hostInfo.hostName'],rF['id'],rF['frameId'])
          print(str(h['hostInfo.hostName']) +" : "+ str(rF['id']) +" : "+ str(rF['frameId']))
          
          
  def hostLocalStop(self):
    try:
      rFrames = dbconn.execute("select * from frames where status = "+ str(constants.framesRunning) +" and hostName = \'"+ str(hName) +"\'", dictionary=True)
    except:
      print(str(sys.exc_info()))
      return(0)
    if(rFrames):
      for rF in rFrames:
        dbconn.stopFrames(hName,rF['id'],rF['frameId'])
        print(str(hName) +" : "+ str(rF['id']) +" : "+ str(rF['frameId']))
    self.hostLocalDisable()
   
  
  
  
  def hostEnable(self):
    hosts =  self.selectedHosts()
    if(hosts):
      for h in hosts:
        dbconn.execute("update hostInfo set status = "+ str(constants.hostInfoEnable) +" where hostName=\'"+ str(h['hostInfo.hostName']) +"\'")
    self.popTableHost()


  def hostLocalEnable(self):
    try:
      dbconn.execute("update hostInfo set status = "+ str(constants.hostInfoEnable) +" where hostName=\'"+ str(hName) +"\'")
    except:
      print(str(sys.exc_info()))
    self.popTableHost()



  def hostDisable(self):
    hosts = self.selectedHosts() 
    if(hosts):
      for h in hosts:
        dbconn.execute("update hostInfo set status = "+ str(constants.hostInfoDisable) +" where hostName=\'"+ str(h['hostInfo.hostName']) +"\'")
    self.popTableHost()
    
  def hostLocalDisable(self):
    try:
      dbconn.execute("update hostInfo set status = "+ str(constants.hostInfoDisable) +" where hostName=\'"+ str(hName) +"\'")
    except:
      print(str(sys.exc_info()))
    self.popTableHost()
      
    
  
    
  def selectedHosts(self):
    rowsHosts=[]
    rowsSelected = []
    for idx in self.tableHost.selectionModel().selectedRows():
      rowsSelected.append(idx.row())
    colCount = self.tableHost.columnCount()
    for row in rowsSelected:
      singleRow = {}
      for col in range(0,colCount):
        singleRow[self.colNamesHost[col]] = str(self.tableHost.item(row,col).text())
      if(singleRow):
        rowsHosts.append(singleRow)

    return(rowsHosts)
  
  def popTableHost(self):
    rSelected = self.selectedHosts()
    hostSelected = []
    if(rSelected):
      for x in rSelected:
        hostSelected.append(x['hostInfo.hostName'])
    print(hostSelected)
        
    self.tableHost.clearContents()
    self.tableHost.setSortingEnabled(False)
    self.tableHost.resizeColumnsToContents()
    colCount = 0
    
    try:
      rows = dbconn.execute("select "+ ",".join(self.colNamesHost) +" from hostInfo, hostAlive, hostResource where hostInfo.hostName=hostAlive.hostName and hostAlive.hostName=hostResource.hostName", dictionary=True)
    except:
      print("Error connecting to db")
      return(0)
    
    hostsAll = [x['hostName'] for x in rows]
    #print(hostsAll)
      
      
    try:
      rowsRunning = dbconn.getRunningFrames()
    except:
      print("Error getting running frames")
      return(0)
    if(rowsRunning):
      hostsRunning = [x['hostName'] for x in rowsRunning]
    else:
      hostsRunning = []
    #print(hostsRunning)
    self.LabelRunning.setText(QtGui.QApplication.translate("Form", "RUNNING : "+ str(len(hostsRunning)), None, QtGui.QApplication.UnicodeUTF8))
      
    if(not rows):
      return()
    for row in rows:
      colCount = len(row)
      break
      
    self.tableHost.setColumnCount(colCount)
    self.tableHost.setRowCount(len(rows))
    
    for x in range(0,colCount):
      item = QtGui.QTableWidgetItem()
      self.tableHost.setHorizontalHeaderItem(x, item)
    indx = 0
    for x in self.colNamesHost:
      y = x.split(" as ")
      x = y[-1].split(".")[-1]
      self.tableHost.horizontalHeaderItem(indx).setText(QtGui.QApplication.translate("Form", x, None, QtGui.QApplication.UnicodeUTF8))
      indx = indx + 1


    indx = 0
    for row in rows:
      item = QtGui.QTableWidgetItem()
      #brush = QtGui.QBrush()
      self.tableHost.setVerticalHeaderItem(indx, item)
      colIndx = 0
      for colName in self.colNamesHost:
        colName = colName.split(" as ")[-1].split(".")[-1]
        item = QtGui.QTableWidgetItem()
        brush = QtGui.QBrush()
        if(colName == "status"):
          if(row[colName] == constants.hostInfoDisable):
            brush.setColor(QtGui.QColor(255, 100, 100))
            brush.setStyle(QtCore.Qt.SolidPattern)
          else:
            brush.setColor(QtGui.QColor(0, 200, 0))
            brush.setStyle(QtCore.Qt.SolidPattern)
          item.setBackground(brush)
          self.tableHost.setItem(indx, colIndx, item)
          self.tableHost.item(indx, colIndx).setText(QtGui.QApplication.translate("Form", constants.hostInfoStatus[int(row[colName])], None, QtGui.QApplication.UnicodeUTF8))
          colIndx = colIndx + 1
          continue
        
        if(colName == "hostName"):
          if(row[colName] in hostsRunning):
            brush.setColor(QtGui.QColor(0, 200, 0))
            brush.setStyle(QtCore.Qt.SolidPattern)
          else:
            brush.setColor(QtGui.QColor(255, 100, 100))
            brush.setStyle(QtCore.Qt.SolidPattern)
          item.setBackground(brush)
          self.tableHost.setItem(indx, colIndx, item)
          self.tableHost.item(indx, colIndx).setText(QtGui.QApplication.translate("Form", str(row[colName]), None, QtGui.QApplication.UnicodeUTF8))
          if(row[colName] in hostSelected):
            self.tableHost.selectRow(indx)
          colIndx = colIndx + 1
          continue
        
        
        if(colName == "alive"):
          if(row[colName] == constants.hostInfoDisable):
            brush.setColor(QtGui.QColor(255, 100, 100))
            brush.setStyle(QtCore.Qt.SolidPattern)
          else:
            brush.setColor(QtGui.QColor(0, 200, 0))
            brush.setStyle(QtCore.Qt.SolidPattern)
          item.setBackground(brush)
          self.tableHost.setItem(indx, colIndx, item)
          self.tableHost.item(indx, colIndx).setText(QtGui.QApplication.translate("Form", constants.hostAliveStatus[int(row[colName])], None, QtGui.QApplication.UnicodeUTF8))
          colIndx = colIndx + 1
          continue
        
        item.setBackground(brush)
        self.tableHost.setItem(indx, colIndx, item)
        self.tableHost.item(indx, colIndx).setText(QtGui.QApplication.translate("Form", str(row[colName]), None, QtGui.QApplication.UnicodeUTF8))
        colIndx = colIndx + 1
        
      indx = indx + 1

 
    self.tableHost.resizeColumnsToContents()
    self.tableHost.setSortingEnabled(True)
    
    
    
    
    
    
if __name__ == "__main__":
  import sys
  app = QtGui.QApplication(sys.argv)
  Form = QtGui.QMainWindow()
  ui = Ui_Form()
  ui.setupUi(Form)
  Form.show()
  sys.exit(app.exec_())
