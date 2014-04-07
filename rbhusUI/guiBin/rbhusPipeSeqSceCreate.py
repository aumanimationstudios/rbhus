#!/usr/bin/python
from PyQt4 import QtCore, QtGui
import glob
import os
import sys


dirSelf = os.path.dirname(os.path.realpath(__file__))
print(dirSelf)
sys.path.append(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep) + os.sep + "lib")


import rbhusPipeSeqSceCreateMod
print(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")
sys.path.append(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")
import dbPipe
import constantsPipe
import authPipe
import utilsPipe


try:
  _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
  _fromUtf8 = lambda s: s
  

class Ui_Form(rbhusPipeSeqSceCreateMod.Ui_MainWindow):
  def setupUi(self, Form):
    rbhusPipeSeqSceCreateMod.Ui_MainWindow.setupUi(self,Form)
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(_fromUtf8(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/rbhusPipe.svg")), QtGui.QIcon.Normal, QtGui.QIcon.On)
    Form.setWindowIcon(icon)
    self.form = Form
    self.dbpipe = dbPipe.dbPipe()
    self.username = None
    try:
      self.username = os.environ['rbhusPipe_acl_user'].rstrip().lstrip()
    except:
      pass
    
    self.center()
    self.dateEditDue.setDateTime(QtCore.QDateTime.currentDateTime())
    #self.pushCreate.clicked.connect(self.cProj)
    
    self.timer = QtCore.QTimer()
    self.timer.timeout.connect(self.updateStatus)
    self.timer.start(100)
    self.wtf = "new"
    
    self.lineEditProjName.setText(os.environ['rp_proj_projName'])
    
    
    
  def modelChanged(self):
    modelSelected = self.comboModel.currentText()
    stageSelected = str(self.comboStage.currentText()).rstrip().lstrip()
    Form.setWindowTitle(modelSelected +"::"+ stageSelected)
    print(str(modelSelected))
    if(str(modelSelected) == "__NEW__"):
      nDir = self.inputDiag()
      if(nDir and (nDir != "__NEW__") and (nDir != "")):
        projSelected = str(self.comboProj.currentText()).rstrip().lstrip()
        filePath = "/proj/"+ projSelected +"/library/model/"+ nDir
        if(not os.path.exists(filePath)):
          os.makedirs(filePath,0777)
        else:
          print("Model dir already available!")
        projSelected = self.comboProj.currentText()
        self.updateModel(projSelected,focus=nDir)
  
  
  
  
  def inputDiag(self, title="New File Name"):
    fS = QtGui.QWidget()
    fS.setGeometry(300, 300, 350, 80)
    fS.setWindowTitle('New File Name')
    text, ok = QtGui.QInputDialog.getText(fS, 'New', 'Enter Name:')
    if(ok):
      print(str(text))
      return(str(text))
    else:
      return(0)
    
    
  def center(self):
    Form.move(QtGui.QApplication.desktop().screen().rect().center()- Form.rect().center())

  
  def updateStatus(self):
    if((str(self.comboSequence.currentText()) != "__NEW__") and (str(self.comboScene.currentText()) != "__NEW__")):
      pDets = utilsPipe.getSequenceScenes(projName=str(os.environ['rp_proj_projName']))
      if(pDets):
        for p in pDets:
          if((p['sequenceName'] == str(self.comboSequence.currentText())) and (p['sceneName'] == str(self.comboScene.currentText()))):
            self.wtf = constantsPipe.createStatus[p['createStatus']]
      else:
        self.wtf = "new"
    self.statusBar.showMessage("status : "+ str(self.wtf))
  
  
    
    
  
  
  def setProjTypes(self):
    rows = utilsPipe.getProjTypes()
    self.comboProjType.clear()  
    if(rows):
      for row in rows:
        self.comboProjType.addItem(_fromUtf8(row['type']))
      
      return(1)
    return(0)     
  
  
  def setDirectory(self):
    dirs = utilsPipe.getDirMaps()
    self.comboDirectory.clear()
    if(dirs):
      for d in dirs:
        self.comboDirectory.addItem(_fromUtf8(d['directory']))
      return(1)
    return(0)
    
    
  def setDefaults(self):
    defs = utilsPipe.getDefaults("proj")
    




if __name__ == "__main__":
  app = QtGui.QApplication(sys.argv)
  Form = QtGui.QMainWindow()
  ui = Ui_Form()
  ui.setupUi(Form)
  Form.show()
  sys.exit(app.exec_())
    