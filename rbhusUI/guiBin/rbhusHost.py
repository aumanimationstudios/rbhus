#!/usr/bin/python
from PyQt4 import QtCore, QtGui
import glob
import os
import sys
import socket
import time
import subprocess

hName = socket.gethostname()
ipAddr = socket.gethostbyname(socket.gethostname()).strip()

dirSelf = os.path.dirname(os.path.realpath(__file__))
print(dirSelf)
sys.path.append(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep) + os.sep + "lib")


  
sys.path.append(dirSelf.rstrip(os.sep) + os.sep + "lib")

rEc = "rbhusHostEdit.py"
rEcM = "rbhusHostEditMulti.py"
  
hostEditCmd = dirSelf.rstrip(os.sep) + os.sep + rEc
hostEditMultiCmd = dirSelf.rstrip(os.sep) + os.sep + rEcM

print hostEditCmd
import rbhusHostMod
print(dirSelf.rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")


sys.path.append(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")
import db
import constants
import utils as rUtils
import dbRbhus



try:
  _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
  _fromUtf8 = lambda s: s
  

class Ui_Form(rbhusHostMod.Ui_MainWindow):
  def setupUi(self, Form):
    rbhusHostMod.Ui_MainWindow.setupUi(self,Form)
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(_fromUtf8(dirSelf.rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/rbhus.svg")), QtGui.QIcon.Normal, QtGui.QIcon.On)
    Form.setWindowIcon(icon)
    self.dbconn = dbRbhus.dbRbhus()
    self.colNamesHost = ["hostInfo.ip","hostInfo.hostName","hostInfo.totalRam","hostInfo.totalCpus","hostEffectiveResource.eCpus","hostInfo.status as status","hostInfo.os","hostAlive.status as alive","hostResource.freeCpus","hostResource.load1","hostInfo.groups"]
    self.popTableHost()
    #self.pushDisable.clicked.connect(self.hostDisable)
    #self.pushEnable.clicked.connect(self.hostEnable)
    self.pushRefresh.clicked.connect(self.popTableHost)
    self.pushLocalStop.clicked.connect(self.hostLocalStop)
    self.pushLocalEnable.clicked.connect(self.hostLocalEnable)
    self.tableHost.customContextMenuRequested.connect(self.popupHost)
  
  
  
  def popupHost(self, pos):
    menu = QtGui.QMenu()
    
    test2Action = menu.addAction("disable")
    test3Action = menu.addAction("enable")
    test4Action = menu.addAction("stop")
    test1Action = menu.addAction("edit")
    test5Action = menu.addAction("restart Rbhus")
    
    
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
    if(action == test5Action):
      self.hostClientKill()
      self.hostClientStart()
      
      
  def hostEdit(self):
    selHostsDict = self.selectedHosts()
    selHosts = []
    for x in selHostsDict:
      selHosts.append(x['hostInfo.ip'].lstrip("0"))
    
    
    if(selHosts):
      if(len(selHosts) > 1):
        try:
          subprocess.Popen([sys.executable,hostEditMultiCmd,str(",".join(selHosts))])
        except:
          print(str(sys.exc_info()))
      else:
        try:
          subprocess.Popen([sys.executable,hostEditCmd,str(selHosts[0])])
        except:
          print(str(sys.exc_info()))

          
  def hostClientKill(self):
    hosts = self.selectedHosts()
    for h in hosts:
      hst = rUtils.hosts(h['hostInfo.ip'])
      hst.killClient()
    self.popTableHost()
    return(1)

  
  def hostClientStart(self):
    hosts = self.selectedHosts()
    for h in hosts:
      hst = rUtils.hosts(h['hostInfo.ip'])
      hst.startClient()
    self.popTableHost()
    return(1)


  def hostStop(self):
    hosts = self.selectedHosts()
    for h in hosts:
      hst = rUtils.hosts(h['hostInfo.ip'])
      hst.hStop()
    self.popTableHost()
    return(1)
      
      
          
          
  def hostLocalStop(self):
    self.hostLocalDisable()
    try:
      rFrames = self.dbconn.execute("select * from frames where status = "+ str(constants.framesRunning) +" and hostName = \'"+ str(hName) +"\'", dictionary=True)
    except:
      print(str(sys.exc_info()))
      return(0)
    if(rFrames):
      for rF in rFrames:
        self.dbconn.stopFrames(hName,rF['id'],rF['frameId'])
        print(str(hName) +" : "+ str(rF['id']) +" : "+ str(rF['frameId']))
    self.popTableHost()
    return(1)
   
  
  
  
  def hostEnable(self):
    hosts =  self.selectedHosts()
    if(hosts):
      for h in hosts:
        hst = rUtils.hosts(h['hostInfo.ip'])
        hst.hEnable()
      self.popTableHost()
    return(1)


  def hostLocalEnable(self):
    try:
      self.dbconn.execute("update hostInfo set status = "+ str(constants.hostInfoEnable) +" where hostName=\'"+ str(hName) +"\'")
    except:
      print(str(sys.exc_info()))
      return(0)
    self.popTableHost()
    return(1)



  def hostDisable(self):
    hosts =  self.selectedHosts()
    print(hosts)
    if(hosts):
      for h in hosts:
        hst = rUtils.hosts(h['hostInfo.ip'])
        a = hst.hDisable()
      if(a):
        print("host disabled")
      else:
        print("host NOT disabled")
    self.popTableHost()
    return(1)
    
  def hostLocalDisable(self):
    try:
      self.dbconn.execute("update hostInfo set status = "+ str(constants.hostInfoDisable) +" where hostName=\'"+ str(hName) +"\'")
    except:
      print(str(sys.exc_info()))
      return(0)
    self.popTableHost()
    return(1)
      
    
  
    
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
    self.tableHost.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
    colCount = 0
    
    try:
      rows = self.dbconn.execute("select "+ ",".join(self.colNamesHost) +" from hostInfo, hostAlive, hostResource, hostEffectiveResource where hostInfo.hostName=hostAlive.hostName and hostInfo.hostName=hostResource.hostName and hostInfo.hostName=hostEffectiveResource.hostName", dictionary=True)
    except:
      print("Error connecting to db")
      return(0)
    
    hostsAll = [x['hostName'] for x in rows]
    #print(hostsAll)
      
      
    try:
      rowsRunning = self.dbconn.getRunningFrames()
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
    self.LabelTotal.setText(QtGui.QApplication.translate("Form", "TOTAL : "+ str(len(rows)), None, QtGui.QApplication.UnicodeUTF8))
    
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
    self.tableHost.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
    
    
    
    
    
    
if __name__ == "__main__":
  import sys
  app = QtGui.QApplication(sys.argv)
  Form = QtGui.QMainWindow()
  ui = Ui_Form()
  ui.setupUi(Form)
  Form.show()
  sys.exit(app.exec_())
