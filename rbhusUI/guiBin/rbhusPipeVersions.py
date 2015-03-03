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
    if(args.assId):
      self.assetDetails = utilsPipe.getAssDetails(assId=args.assId)
    if(args.assPath):
      self.assetDetails = utilsPipe.getAssDetails(assPath=args.assPath)
    print(self.assetDetails)
    
    
    self.pushInit.clicked.connect(self.initialize)
    self.pushWork.clicked.connect(self.openfolder)
    self.pushCommit.clicked.connect(self.commit)
    
    self.versionsHg = hgmod.hg(args.assPath)
    
    
  def push(self):
    pass
  
  def initialize(self):
    self.versionsHg.initialize()
  
  def commit(self):
    self.versionsHg._add()
    self.versionsHg._commit()
    self.versionsHg._push()
    os.chdir(self.versionsHg.absPipePath)
    self.versionsHg._update()
    self.versionsHg._log()
    os.chdir(self.versionsHg.localPath)
    
    
  
  
  def openfolder(self):
    self.versionsHg.initializeLocal()
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
    