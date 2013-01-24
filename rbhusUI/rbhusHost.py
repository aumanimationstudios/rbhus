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

if(sys.platform.find("win") >= 0):
  rEc = "rbhusHostEdit.py"
elif(sys.platform.find("linux") >= 0):
  rEc = "rbhusHostEdit"
  
editHostCmd = cwd.rstrip(os.sep) + os.sep + rEc

print editHostCmd
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
    self.colNamesHost = ["hostInfo.hostName","hostInfo.ip","hostInfo.totalRam","hostInfo.totalCpus","hostInfo.status as status","hostInfo.os","hostAlive.status as alive","hostResource.freeCpus","hostResource.load1","hostInfo.groups"]
    self.popTableHost()
    self.pushDisable.clicked.connect(self.hostDisable)
    self.pushEnable.clicked.connect(self.hostEnable)
    self.pushRefresh.clicked.connect(self.popTableHost)
  
  
  def hostEnable(self):
    hosts =  self.selectedHosts()
    if(hosts):
      for h in hosts:
        dbconn.execute("update hostInfo set status = "+ str(constants.hostInfoEnable) +" where hostName=\'"+ str(h['hostInfo.hostName']) +"\'")
    self.popTableHost()


  def hostDisable(self):
    hosts = self.selectedHosts() 
    if(hosts):
      for h in hosts:
        dbconn.execute("update hostInfo set status = "+ str(constants.hostInfoDisable) +" where hostName=\'"+ str(h['hostInfo.hostName']) +"\'")
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
    self.tableHost.clearContents()
    self.tableHost.setSortingEnabled(False)
    self.tableHost.resizeColumnsToContents()
    colCount = 0
    
    try:
      rows = dbconn.execute("select "+ ",".join(self.colNamesHost) +" from hostInfo, hostAlive, hostResource where hostInfo.hostName=hostAlive.hostName and hostAlive.hostName=hostResource.hostName", dictionary=True)
    except:
      print("Error connecting to db")
      return(0)
      
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
            brush.setColor(QtGui.QColor(200, 0, 0))
            brush.setStyle(QtCore.Qt.SolidPattern)
          else:
            brush.setColor(QtGui.QColor(0, 200, 0))
            brush.setStyle(QtCore.Qt.SolidPattern)
          item.setBackground(brush)
          self.tableHost.setItem(indx, colIndx, item)
          self.tableHost.item(indx, colIndx).setText(QtGui.QApplication.translate("Form", constants.hostInfoStatus[int(row[colName])], None, QtGui.QApplication.UnicodeUTF8))
          colIndx = colIndx + 1
          continue
        if(colName == "alive"):
          if(row[colName] == constants.hostInfoDisable):
            brush.setColor(QtGui.QColor(200, 0, 0))
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
