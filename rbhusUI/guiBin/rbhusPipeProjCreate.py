#!/usr/bin/env python2
from PyQt4 import QtCore, QtGui
import glob
import os
import sys
import subprocess


dirSelf = os.path.dirname(os.path.realpath(__file__))
print(dirSelf)
sys.path.append(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep) + os.sep + "lib")


import rbhusPipeProjCreateMod
print(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")
sys.path.append(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")
import dbPipe
import constantsPipe
import authPipe
import utilsPipe


scb = "selectCheckBox.py" 
scbc = "selectCheckBoxCombo.py"
srb = "selectRadioBox.py"

selectCheckBoxCmd = dirSelf.rstrip(os.sep) + os.sep + scb
selectRadioBoxCmd = dirSelf.rstrip(os.sep) + os.sep + srb
selectCheckBoxComboCmd = dirSelf.rstrip(os.sep) + os.sep + scbc



print(selectCheckBoxCmd)

try:
  _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
  _fromUtf8 = lambda s: s
  

class Ui_Form(rbhusPipeProjCreateMod.Ui_MainWindow):
  def setupUi(self, Form):
    rbhusPipeProjCreateMod.Ui_MainWindow.setupUi(self,Form)
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(_fromUtf8(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/rbhusPipe.svg")), QtGui.QIcon.Normal, QtGui.QIcon.On)
    Form.setWindowIcon(icon)
    
    self.dbpipe = dbPipe.dbPipe()
    self.username = None
    try:
      self.username = os.environ['rbhusPipe_acl_user'].rstrip().lstrip()
    except:
      pass
    
    self.center()
    self.setProjTypes()
    self.setDirectory()
    self.dateEditDue.setDateTime(QtCore.QDateTime.currentDateTime())
    self.pushCreate.clicked.connect(self.cProj)
    self.pushLinked.clicked.connect(self.setLinked)
    self.pushUsers.clicked.connect(self.setUsers)
    
    self.timer = QtCore.QTimer()
    self.timer.timeout.connect(self.updateStatus)
    self.timer.start(100)
    self.wtf = "new"
    
    
    
    
    
  def center(self):
    Form.move(QtGui.QApplication.desktop().screen().rect().center()- Form.rect().center())

  
  def setLinked(self):
    projNames = []
    projects = utilsPipe.getProjDetails(status="all")
    for x in projects:
      projNames.append(x['projName'])
      
    outLinked = subprocess.Popen([sys.executable,selectCheckBoxCmd,"-i",",".join(projNames),"-d",str(self.lineEditLinked.text()).rstrip().lstrip()],stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].rstrip().lstrip()
    if(outLinked == ""):
      outLinked = str(self.lineEditLinked.text()).rstrip().lstrip()
    self.lineEditLinked.setText(_fromUtf8(outLinked))
  
  
  
  def updateStatus(self):
    if(self.lineEditName.text()):
      pDets = utilsPipe.getProjDetails(projName=str(self.lineEditName.text()))
      if(pDets):
        self.wtf = constantsPipe.createStatus[pDets['createStatus']]
      else:
        self.wtf = "new"
    self.statusBar.showMessage("status : "+ str(self.wtf))
  
  def cProj(self):
    pType = str(self.comboProjType.currentText()).rstrip().lstrip()
    pName = str(self.lineEditName.text()) if(str(self.lineEditName.text()).rstrip().lstrip()) else None
    pDir = str(self.comboDirectory.currentText()).rstrip().lstrip()
    pDueDate = str(self.dateEditDue.dateTime().date().year()) +"-"+ str(self.dateEditDue.dateTime().date().month()) +"-"+ str(self.dateEditDue.dateTime().date().day()) +" "+ str(self.dateEditDue.dateTime().time().hour()) +":"+ str(self.dateEditDue.dateTime().time().minute()) +":" + str(self.dateEditDue.dateTime().time().second())
    pAdmins = str(self.lineEditAdmins.text()).rstrip().lstrip() if(self.lineEditAdmins.text()) else None
    pAclUser = str(self.lineEditAclUser.text()).rstrip().lstrip() if(self.lineEditAclUser.text()) else None
    pAclGroup = str(self.lineEditAclGroup.text()).rstrip().lstrip() if(self.lineEditAclGroup.text()) else None
    pRI = 1 if(self.checkRI.isChecked()) else 0
    pDesc = str(self.lineEditDesc.text()).rstrip().lstrip() if(self.lineEditDesc.text()) else None
    linked = str(self.lineEditLinked.text()).rstrip().lstrip()
    createdUser = os.environ['rbhusPipe_acl_user']
    self.wtf = "connecting"
    utilsPipe.setupProj(projType=pType,
                            projName=pName,
                            directory=pDir,
                            admins=pAdmins,
                            rbhusRenderIntegration=pRI,
                            rbhusRenderServer=None,
                            aclUser=pAclUser,
                            aclGroup=pAclGroup,
                            dueDate=pDueDate,
                            description=pDesc,
                            createdUser=createdUser)
    
    
  def setUsers(self):
    users = utilsPipe.getUsers()
    outUsers = subprocess.Popen([sys.executable,selectCheckBoxCmd,"-i",",".join(users),"-d",str(self.lineEditAdmins.text()).rstrip().lstrip()],stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].rstrip().lstrip()
    if(outUsers == ""):
      outUsers = str(self.lineEditAdmins.text()).rstrip().lstrip()
    self.lineEditAdmins.setText(_fromUtf8(outUsers))
  

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
    