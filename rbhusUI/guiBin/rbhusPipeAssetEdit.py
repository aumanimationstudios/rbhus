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





import rbhusPipeAssetEditMod
print(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")
sys.path.append(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")
import dbPipe
import constantsPipe
import authPipe
import utilsPipe






parser = argparse.ArgumentParser()
parser.add_argument("-i","--id",dest='assId',help='comma seperated asset id list')
parser.add_argument("-p","--path",dest='assPath',help='comma seperated asset path list')
args = parser.parse_args()




try:
  _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
  _fromUtf8 = lambda s: s
  

class Ui_Form(rbhusPipeAssetEditMod.Ui_MainWindow):
  def setupUi(self, Form):
    self.form = Form
    rbhusPipeAssetEditMod.Ui_MainWindow.setupUi(self,Form)
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(_fromUtf8(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/rbhusPipe.svg")), QtGui.QIcon.Normal, QtGui.QIcon.On)
    Form.setWindowIcon(icon)
    
    self.idList = []
    self.pathList = []
    self.updateLine = []
    
    if(args.assId):
      self.idList = args.assId.split(",")
    if(args.assPath):
      self.pathList = args.assPath.split(",")
    
    self.username = None
    self.project = None
    self.directory = None
    try:
      self.username = os.environ['rbhusPipe_acl_user'].rstrip().lstrip()
    except:
      pass
    try:
      self.project = os.environ['rp_proj_projName']
    except:
      pass
    try:
      self.directory = os.environ['rp_proj_directory']
    except:
      pass
    
    self.center()
    #self.setProjTypes()
    self.dateEditDue.setDateTime(QtCore.QDateTime.currentDateTime())
    self.pushEdit.clicked.connect(self.eAss)
    self.pushTags.clicked.connect(self.setTags)
    self.pushUsers.clicked.connect(self.setUsers)
    self.checkTags.clicked.connect(self.enableTags)
    self.checkFRange.clicked.connect(self.enableFRange)
    self.checkDueDate.clicked.connect(self.enableDueDate)
    self.checkAssign.clicked.connect(self.enableAssignTo)
    self.checkDesc.clicked.connect(self.enableDesc)
    self.checkAssignSelf.clicked.connect(self.setAssignedWorker)
    self.enableAssignTo()
    self.enableDesc()
    self.enableDueDate()
    self.enableFRange()
    self.enableTags()
    
    
    
    
    
  def center(self):
    Form.move(QtGui.QApplication.desktop().screen().rect().center()- Form.rect().center())

  
  def enableTags(self):
    if(self.checkTags.isChecked()):
      self.lineEditTags.setEnabled(True)
    else:
      self.lineEditTags.setEnabled(False)
      
  def enableFRange(self):
    if(self.checkFRange.isChecked()):
      self.lineEditFRange.setEnabled(True)
    else:
      self.lineEditFRange.setEnabled(False)


  def enableDueDate(self):
    if(self.checkDueDate.isChecked()):
      self.dateEditDue.setEnabled(True)
    else:
      self.dateEditDue.setEnabled(False)
      
      
  def enableAssignTo(self):
    if(self.checkAssign.isChecked()):
      self.lineEditWorkers.setEnabled(True)
      self.checkAssignSelf.setEnabled(True)
      self.pushUsers.setEnabled(True)
    else:
      self.lineEditWorkers.setEnabled(False)
      self.checkAssignSelf.setEnabled(False)
      self.pushUsers.setEnabled(False)
      
  def enableDesc(self):
    if(self.checkDesc.isChecked()):
      self.lineEditDesc.setEnabled(True)
    else:
      self.lineEditDesc.setEnabled(False)


      


  
  def setAssignedWorker(self):
    if(self.checkAssignSelf.isChecked()):
      self.lineEditWorkers.setText(str(self.username))
  
  
  def setUsers(self):
    users = utilsPipe.getUsers()
    outUsers = subprocess.Popen([sys.executable,selectRadioBoxCmd,"-i",",".join(users),"-d",str(self.lineEditWorkers.text()).rstrip().lstrip()],stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].rstrip().lstrip()
    if(outUsers == ""):
      outTags = str(self.lineEditWorkers.text()).rstrip().lstrip()
    self.lineEditWorkers.setText(_fromUtf8(outUsers))
  
  
  def eAss(self):
    self.centralwidget.setCursor(QtCore.Qt.WaitCursor)
    if(self.idList):
      for xid in self.idList:
        assdets = utilsPipe.getAssDetails(assId=xid)
        assdict = {}
        if(self.checkDueDate.isChecked()):
          assdict['dueDate'] = str(self.dateEditDue.dateTime().date().year()) +"-"+ str(self.dateEditDue.dateTime().date().month()) +"-"+ str(self.dateEditDue.dateTime().date().day()) +" "+ str(self.dateEditDue.dateTime().time().hour()) +":"+ str(self.dateEditDue.dateTime().time().minute()) +":" + str(self.dateEditDue.dateTime().time().second())
        if(self.checkAssign.isChecked()):
          assdict['assignedWorker'] = str(self.lineEditWorkers.text())
        if(self.checkDesc.isChecked()):
          assdict['description'] = str(self.lineEditDesc.text())
        if(self.checkTags.isChecked()):
          assdict['tags'] = str(self.lineEditTags.text())
        if(self.checkFRange.isChecked()):
          assdict['fRange'] = str(self.lineEditFRange.text())
          
        if(not (self.project in os.environ['rbhusPipe_acl_projIds'].split() or assdets['createdUser'] == self.username)):
          print("user not allowed to edit . not an admin or an asset founder!!")
          self.cetralwidget.setCursor(QtCore.Qt.ArrowCursor)
          return(0)

        if(assdict):
          utilsPipe.assEdit(assid = xid , assdict=assdict)
    if(self.pathList):
      for xpath in self.pathList:
        assdets = utilsPipe.getAssDetails(assPath=xpath)
        assdict = {}
        if(self.checkDueDate.isChecked()):
          assdict['dueDate'] = str(self.dateEditDue.dateTime().date().year()) +"-"+ str(self.dateEditDue.dateTime().date().month()) +"-"+ str(self.dateEditDue.dateTime().date().day()) +" "+ str(self.dateEditDue.dateTime().time().hour()) +":"+ str(self.dateEditDue.dateTime().time().minute()) +":" + str(self.dateEditDue.dateTime().time().second())
        if(self.checkAssign.isChecked()):
          assdict['assignedWorker'] = str(self.lineEditWorkers.text())
        if(self.checkDesc.isChecked()):
          assdict['description'] = str(self.lineEditDesc.text())
        if(self.checkTags.isChecked()):
          assdict['tags'] = str(self.lineEditTags.text())
        if(self.checkFRange.isChecked()):
          assdict['fRange'] = str(self.lineEditFRange.text())
          
        if(not (self.project in os.environ['rbhusPipe_acl_projIds'].split() or assdets['createdUser'] == self.username)):
          print("user not allowed to edit . not an admin or an asset founder!!")
          self.cetralwidget.setCursor(QtCore.Qt.ArrowCursor)
          return(0)
        
        if(assdict):
          utilsPipe.assEdit(asspath = xpath , assdict=assdict)
    self.centralwidget.setCursor(QtCore.Qt.ArrowCursor)
    return(1)
    
    
    
  def setTags(self):
    tags = utilsPipe.getTags(projName=os.environ['rp_proj_projName'])
    outTags = subprocess.Popen([sys.executable,selectCheckBoxCmd,"-i",",".join(tags),"-d",str(self.lineEditTags.text()).rstrip().lstrip()],stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].rstrip().lstrip()
    if(outTags == ""):
      outTags = "default"
    self.lineEditTags.setText(_fromUtf8(outTags))
  
  
  
  
  
  
  
  def setDefaults(self):
    defs = utilsPipe.getProjDefaults()
    




if __name__ == "__main__":
  app = QtGui.QApplication(sys.argv)
  Form = QtGui.QMainWindow()
  ui = Ui_Form()
  ui.setupUi(Form)
  Form.show()
  sys.exit(app.exec_())
    