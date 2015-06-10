#!/usr/bin/python
from PyQt4 import QtCore, QtGui
import glob
import os
import sys
import time
import subprocess
import argparse


dirSelf = os.path.dirname(os.path.realpath(__file__))
print(dirSelf)
sys.path.append(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep) + os.sep + "lib")


scb = "selectCheckBox.py"
srb = "selectRadioBox.py"
selectCheckBoxCmd = dirSelf.rstrip(os.sep) + os.sep + scb
selectRadioBoxCmd = dirSelf.rstrip(os.sep) + os.sep + srb





import rbhusPipeVersionsMod
print(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")
sys.path.append(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")
import dbPipe
import constantsPipe
import authPipe
import utilsPipe
import hgmod






parser = argparse.ArgumentParser()
parser.add_argument("-i","--id",dest='assId',help='asset id')
parser.add_argument("-p","--path",dest='assPath',help='asset path')
args = parser.parse_args()




try:
  _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
  _fromUtf8 = lambda s: s
  

class Ui_Form(rbhusPipeVersionsMod.Ui_MainWindow):
  def setupUi(self, Form):
    self.form = Form
    rbhusPipeVersionsMod.Ui_MainWindow.setupUi(self,Form)
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(_fromUtf8(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/rbhusPipe.svg")), QtGui.QIcon.Normal, QtGui.QIcon.On)
    Form.setWindowIcon(icon)
    Form.setWindowTitle(args.assPath)
    self.updateAssDetails()
    print(str(self.assetDetails))
    
    
    self.pushWork.clicked.connect(self.openfolder)
    self.pushCommit.clicked.connect(self.commit)
    self.pushReInit.clicked.connect(self.reInit)
    
    
    self.tableVersions.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    self.tableVersions.customContextMenuRequested.connect(self.popupPublish)
    
    
    print("\nVERSIONING  :::::::::::: "+ str(self.assetDetails) +"\n")
    if(int(self.assetDetails['versioning']) == 0):
      sys.exit(1)
    
    self.versionsHg = hgmod.hg(args.assPath)
    self.initialize()
    
    self.hglog()

  
  def updateAssDetails(self):
    if(args.assId):
      self.assetDetails = utilsPipe.getAssDetails(assId=args.assId)
    if(args.assPath):
      self.assetDetails = utilsPipe.getAssDetails(assPath=args.assPath)
  
  
  def popupPublish(self, pos):
    menu = QtGui.QMenu()
    #openFileAction = menu.addAction("open file")
    publishAction = menu.addAction("publish")
    reviseAction = menu.addAction("revise")
    exportAction = menu.addAction("export")
    openVersionAction = menu.addAction("open version")
    action = menu.exec_(self.tableVersions.mapToGlobal(pos))
    #if(action == openFileAction):
      #self.openFileAss()
    if(action == publishAction):
      self.publishVersion()
    if(action == reviseAction):
      self.reviseVersion()
    if(action == exportAction):
      self.exportVeriosn()
    if(action == openVersionAction):
      self.openVersion()
    
  def reInit(self):
    self.versionsHg.reInitLocal()
    self.hglog()
  
  
  def openVersion(self):
    selvers = self.selectedVersions()
    if(selvers):
      sv = selvers[-1]
      verpath = self.versionsHg.getVersionPath(sv)
    assdets = utilsPipe.getAssDetails(assPath=self.versionsHg.pipepath)
    runCmd = utilsPipe.openAssetCmd(assdets,verpath)
    if(runCmd):
      runCmd = runCmd.rstrip().lstrip()
      subprocess.Popen(runCmd,shell=True)
    else:
      import webbrowser
      webbrowser.open(verpath)
  
  
  def exportVeriosn(self):
    selvers = self.selectedVersions()
    if(selvers):
      sv = selvers[-1]
      self.versionsHg._archiveVersion(sv)
    self.hglog()
    
  def exportVeriosn(self):
    selvers = self.selectedVersions()
    if(selvers):
      sv = selvers[-1]
      self.versionsHg._archiveVersion(sv)
    self.hglog()
  
  def publishVersion(self):
    selvers = self.selectedVersions()
    if(selvers):
      sv = selvers[-1]
      self.versionsHg._archive(sv)
    self.hglog()
        
    
    
  
  
  def reviseVersion(self):
    selvers = self.selectedVersions()
    if(selvers):
      sv = selvers[-1]
      self.versionsHg._revert(sv)
    
  
  def selectedVersions(self):
    rowstask=[]
    rowsSelected = []
    rowsModel = self.tableVersions.selectionModel().selectedRows()
    for idx in rowsModel:
      rowsSelected.append(idx)
    for rows in rowsSelected:
      rowstask.append(str(self.tableVersions.item(rows.row(), 0).text()).lstrip("0"))
    return(rowstask)
  
  
  def hglog(self):
    self.updateAssDetails()
    self.tableVersions.clearContents()
    self.tableVersions.setSortingEnabled(False)
    self.tableVersions.resizeColumnsToContents()
    tem = self.versionsHg._log()
    if(tem):
      self.tableVersions.setColumnCount(len(tem[0]))
      self.tableVersions.setRowCount(len(tem))
      indrow = 0
      
      for te in tem:
        indcol = 0
        for t in te:
          item = QtGui.QTableWidgetItem()
          brush = QtGui.QBrush()
          self.tableVersions.setItem(indrow, indcol, item)
          if(indcol == 2):
            self.tableVersions.item(indrow, indcol).setText(str(time.ctime(float(t.split("-")[0]))))
          elif(indcol == 0):
            if(str(t) == str(self.assetDetails['publishVersion'])):
              brush.setColor(QtGui.QColor(0, 200, 0))
              brush.setStyle(QtCore.Qt.SolidPattern)
              self.tableVersions.item(indrow, indcol).setBackground(brush)
            self.tableVersions.item(indrow, indcol).setText(str(t).zfill(4))
          else:
            self.tableVersions.item(indrow, indcol).setText(str(t))
          indcol = indcol + 1
        indrow = indrow + 1
        
        
    self.tableVersions.setSortingEnabled(True) 
    self.tableVersions.resizeColumnsToContents()
    print(tem)
  
  
  def push(self):
    pass
  
  def initialize(self):
    self.versionsHg.initialize()
    self.versionsHg.initializeLocal()
    self.hglog()
  
  def commit(self):
    self.versionsHg._add()
    self.versionsHg._commit()
    self.versionsHg._push()
    os.chdir(self.versionsHg.absPipePath)
    self.versionsHg._update()
    os.chdir(self.versionsHg.localPath)
    self.hglog()
    
    
    
  
  
  def openfolder(self):
    
    if(os.path.exists(self.versionsHg.localPath)):
      fila = QtGui.QFileDialog.getOpenFileNames(directory=self.versionsHg.localPath)
      print(fila)
      if(fila):
        print(str(fila[0]))
        filename = str(fila[0])
        assdets = utilsPipe.getAssDetails(assPath=self.versionsHg.pipepath)
        runCmd = utilsPipe.openAssetCmd(assdets,filename)
        if(runCmd):
          runCmd = runCmd.rstrip().lstrip()
          subprocess.Popen(runCmd,shell=True)
        else:
          import webbrowser
          webbrowser.open(filename)
    



if __name__ == "__main__":
  app = QtGui.QApplication(sys.argv)
  Form = QtGui.QMainWindow()
  ui = Ui_Form()
  ui.setupUi(Form)
  Form.show()
  sys.exit(app.exec_())
    