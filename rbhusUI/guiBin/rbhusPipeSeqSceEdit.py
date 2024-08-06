#!/usr/bin/env python3
from PyQt5 import QtWidgets, QtCore, QtGui
import glob
import os
import sys
import tempfile
import subprocess


dirSelf = os.path.dirname(os.path.realpath(__file__))
print(dirSelf)
sys.path.append(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep) + os.sep + "lib")


tempDir = tempfile.gettempdir()
srb = "selectRadioBox.py"




selectRadioBoxCmd = dirSelf.rstrip(os.sep) + os.sep + srb
selectRadioBoxCmd = selectRadioBoxCmd.replace("\\","/")





import rbhusPipeSeqSceEditMod
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
  

class Ui_Form(rbhusPipeSeqSceEditMod.Ui_MainWindow):
  def setupUi(self, Form):
    rbhusPipeSeqSceEditMod.Ui_MainWindow.setupUi(self,Form)
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
    self.pushEdit.clicked.connect(self.editSeqScn)
    self.lineEditProjName.setText(os.environ['rp_proj_projName'])
    self.comboSequence.currentIndexChanged.connect(self.setScene)
    self.comboScene.currentIndexChanged.connect(self.setDefaults)
    self.checkAdmins.clicked.connect(self.checkTest)
    self.checkStartFrame.clicked.connect(self.checkTest)
    self.checkEndFrame.clicked.connect(self.checkTest)
    self.checkDueDate.clicked.connect(self.checkTest)
    self.checkDesc.clicked.connect(self.checkTest)
    
    
    #self.timer = QtCore.QTimer()
    #self.timer.timeout.connect(self.updateStatus)
    #self.timer.start(1000)
    self.wtf = ""
    self.setSequence()
    self.checkTest()
    self.setDefaults()
    
  def setSequence(self):
    rows = utilsPipe.getSequenceScenes(os.environ['rp_proj_projName'])
    self.comboSequence.clear()  
    seq = {}
    if(rows):
      for row in rows:
        if(row['projName'] == os.environ['rp_proj_projName']):
          seq[row['sequenceName']] = 1
      if(seq):
        for x in seq.keys():
          self.comboSequence.addItem(_fromUtf8(x))
      return(1)
    return(0)      
    
  def editSeqScn(self):
    self.centralwidget.setCursor(QtCore.Qt.WaitCursor)
    self.centralwidget.setEnabled(False)
    seqScnDict = {}
    seqScnDict['projName'] = str(self.lineEditProjName.text()) 
    seqScnDict['sequenceName'] = str(self.comboSequence.currentText())
    seqScnDict['sceneName'] = str(self.comboScene.currentText())
    if (self.checkDueDate.isChecked()):
      seqScnDict['dueDate'] = str(self.dateEditDue.dateTime().date().year()) +"-"+ str(self.dateEditDue.dateTime().date().month()) +"-"+ str(self.dateEditDue.dateTime().date().day()) +" "+ str(self.dateEditDue.dateTime().time().hour()) +":"+ str(self.dateEditDue.dateTime().time().minute()) +":" + str(self.dateEditDue.dateTime().time().second())
    if (self.checkStartFrame.isChecked()):
      seqScnDict['sFrame'] = str(self.spinStartFrame.value()) 
    if (self.checkEndFrame.isChecked()):
      seqScnDict['eFrame'] = str(self.spinEndFrame.value())
    if (self.checkAdmins.isChecked()):
      seqScnDict['admins'] = str(self.lineEditAdmins.text()) 
    if (self.checkDesc.isChecked()):
      seqScnDict['description'] = str(self.lineEditDesc.text()) 
    utilsPipe.editSequenceScene(seqScnDict)
    self.centralwidget.setEnabled(True)
    self.centralwidget.setCursor(QtCore.Qt.ArrowCursor)
  
  
  
  def setScene(self):
    seqNames = str(self.comboSequence.currentText())
    self.comboScene.clear()
    scenes = {}
    rows = utilsPipe.getSequenceScenes(os.environ['rp_proj_projName'],seq=seqNames)
    if(rows):
      for x in rows:
        self.comboScene.addItem(x['sceneName'])
        
  
  
    
  
  
  
  def checkTest(self):
    if(self.checkStartFrame.isChecked() == True):
      self.spinStartFrame.setEnabled(True)
    else:
      self.spinStartFrame.setEnabled(False)
      
    if(self.checkEndFrame.isChecked() == True):
      self.spinEndFrame.setEnabled(True)
    else:
      self.spinEndFrame.setEnabled(False)
    
    if(self.checkDueDate.isChecked() == True):
      self.dateEditDue.setEnabled(True)
    else:
      self.dateEditDue.setEnabled(False)
    
    if(self.checkAdmins.isChecked() == True):
      self.lineEditAdmins.setEnabled(True)
    else:
      self.lineEditAdmins.setEnabled(False)
      
    if(self.checkDesc.isChecked() == True):
      self.lineEditDesc.setEnabled(True)
    else:
      self.lineEditDesc.setEnabled(False)
      
    
    
  
  def center(self):
    Form.move(QtWidgets.QApplication.desktop().screen().rect().center()- Form.rect().center())

  
 
  
  
    
    
  def setDefaults(self):
    defs = utilsPipe.getDefaults("proj")
    seqscness = utilsPipe.getSequenceScenes(os.environ["rp_proj_projName"],seq=str(self.comboSequence.currentText()),sce=str(self.comboScene.currentText()))
    seqscnes = seqscness[0]
    print(seqscnes)
    if(seqscnes):
      if(seqscnes['dueDate']):
        self.dateEditDue.setTime(QtCore.QTime(seqscnes['dueDate'].hour, seqscnes['dueDate'].minute, seqscnes['dueDate'].second))
        self.dateEditDue.setDate(QtCore.QDate(seqscnes['dueDate'].year, seqscnes['dueDate'].month, seqscnes['dueDate'].day))
        self.spinStartFrame.setValue(seqscnes['sFrame'])
        self.spinEndFrame.setValue(seqscnes['eFrame'])
        self.lineEditAdmins.setText(seqscnes['admins'])
        self.lineEditDesc.setText(seqscnes['description'])
      




if __name__ == "__main__":
  app = QtWidgets.QApplication(sys.argv)
  Form = QtWidgets.QMainWindow()
  ui = Ui_Form()
  ui.setupUi(Form)
  Form.show()
  sys.exit(app.exec_())
    