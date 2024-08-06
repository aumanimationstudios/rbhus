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
    self.pushCreate.clicked.connect(self.createSeqScn)
    self.pushSelectSeq.clicked.connect(self.rbhusPipeSeqSet)
    self.lineEditProjName.setText(os.environ['rp_proj_projName'])
    
    
    self.timer = QtCore.QTimer()
    self.timer.timeout.connect(self.updateStatus)
    self.timer.start(1000)
    self.wtf = ""
    
    
    
  def createSeqScn(self):
    self.centralwidget.setCursor(QtCore.Qt.WaitCursor)
    
    seqScnDict = {}
    seqScnDict['projName'] = os.environ['rp_proj_projName']
    if(not self.lineEditSequenceName.text()):
      return(0)
    seqScnDict['sequenceName'] = str(self.lineEditSequenceName.text())
    if(not self.lineEditSceneName.text()):
      return(0)
    self.centralwidget.setEnabled(False)
    for x in str(self.lineEditSceneName.text()).split(","):
      if(x.rstrip().lstrip()):
        seqScnDict['sceneName'] = str(x.rstrip().lstrip())
        seqScnDict['dueDate'] = str(self.dateEditDue.dateTime().date().year()) +"-"+ str(self.dateEditDue.dateTime().date().month()) +"-"+ str(self.dateEditDue.dateTime().date().day()) +" "+ str(self.dateEditDue.dateTime().time().hour()) +":"+ str(self.dateEditDue.dateTime().time().minute()) +":" + str(self.dateEditDue.dateTime().time().second())
        seqScnDict['sFrame'] = str(self.spinStartFrame.value())
        seqScnDict['eFrame'] = str(self.spinEndFrame.value())
        seqScnDict['admins'] = str(self.lineEditAdmins.text())
        seqScnDict['description'] = str(self.lineEditDesc.text())
        utilsPipe.setupSequenceScene(seqScnDict)
    self.centralwidget.setEnabled(True)
    self.centralwidget.setCursor(QtCore.Qt.ArrowCursor)
  
  
  def rbhusPipeSeqSet(self):
    seqs = utilsPipe.getSequenceScenes(os.environ["rp_proj_projName"])
    uniqSeq = {}
    if(seqs):
      for x in seqs:
        uniqSeq[x['sequenceName']] = 1
    if(uniqSeq):
      seqNames = uniqSeq.keys()
      seqToDisp = subprocess.Popen([sys.executable,selectRadioBoxCmd,"-i",",".join(seqNames)],stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].rstrip().lstrip()
      print(seqToDisp)
      self.lineEditSequenceName.setText(seqToDisp)
      return(1)
    else:
      return(0)
    
  
  
  
  def inputDiag(self, title="New File Name"):
    fS = QtWidgets.QWidget()
    fS.setGeometry(300, 300, 350, 80)
    fS.setWindowTitle('New File Name')
    text, ok = QtWidgets.QInputDialog.getText(fS, 'New', 'Enter Name:')
    if(ok):
      print(str(text))
      return(str(text))
    else:
      return(0)
    
    
  def center(self):
    Form.move(QtWidgets.QApplication.desktop().screen().rect().center()- Form.rect().center())

  
  def updateStatus(self):
    newStatus = utilsPipe.getSequenceScenes(os.environ["rp_proj_projName"],seq=str(self.lineEditSequenceName.text()),sce=str(self.lineEditSceneName.text()))
    if(newStatus):
      if(len(newStatus) > 0):
        self.wtf = constantsPipe.createStatus[newStatus[-1]['createStatus']]
      else:
        self.wtf = "new"
    else:
      self.wtf = "new"
    self.statusBar.showMessage("status : "+ str(self.wtf))
    newStatus = 0
  
  
    
    
  
  
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
  app = QtWidgets.QApplication(sys.argv)
  Form = QtWidgets.QMainWindow()
  ui = Ui_Form()
  ui.setupUi(Form)
  Form.show()
  sys.exit(app.exec_())
    