#!/usr/bin/env python3
from PyQt5 import QtWidgets, QtCore, QtGui
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
import debug


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


def str_convert(text):
  if isinstance(text, bytes):
    return str(text, 'utf-8')
  return str(text)


class Ui_Form(rbhusPipeProjCreateMod.Ui_MainWindow):
  def setupUi(self, Form):
    rbhusPipeProjCreateMod.Ui_MainWindow.setupUi(self,Form)
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(str_convert(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/rbhusPipe.svg")), QtGui.QIcon.Normal, QtGui.QIcon.On)
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
    Form.move(QtWidgets.QApplication.desktop().screen().rect().center()- Form.rect().center())

  
  def setLinked(self):
    projNames = []
    projects = utilsPipe.getProjDetails(status="all")
    for x in projects:
      projNames.append(x['projName'])
      
    outLinked = subprocess.Popen([sys.executable,selectCheckBoxCmd,"-i",",".join(projNames),"-d",str_convert(self.lineEditLinked.text()).rstrip().lstrip()],stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].rstrip().lstrip()
    outLinked = str_convert(outLinked)
    if(outLinked == ""):
      outLinked = str_convert(self.lineEditLinked.text()).rstrip().lstrip()
    self.lineEditLinked.setText(str_convert(outLinked))
  
  
  
  def updateStatus(self):
    if(self.lineEditName.text()):
      pDets = utilsPipe.getProjDetails(projName=str_convert(self.lineEditName.text()))
      if(pDets):
        self.wtf = constantsPipe.createStatus[pDets['createStatus']]
      else:
        self.wtf = "new"
    self.statusBar.showMessage("status : "+ str(self.wtf))
  
  def cProj(self):
    pType = str_convert(self.comboProjType.currentText()).rstrip().lstrip()
    pName = str_convert(self.lineEditName.text()) if(str_convert(self.lineEditName.text()).rstrip().lstrip()) else None
    pDir = str_convert(self.comboDirectory.currentText()).rstrip().lstrip()
    pDueDate = str(self.dateEditDue.dateTime().date().year()) +"-"+ str(self.dateEditDue.dateTime().date().month()) +"-"+ str(self.dateEditDue.dateTime().date().day()) +" "+ str(self.dateEditDue.dateTime().time().hour()) +":"+ str(self.dateEditDue.dateTime().time().minute()) +":" + str(self.dateEditDue.dateTime().time().second())
    pAdmins = str_convert(self.lineEditAdmins.text()).rstrip().lstrip() if(str_convert(self.lineEditAdmins.text())) else None
    pAclUser = str_convert(self.lineEditAclUser.text()).rstrip().lstrip() if(str_convert(self.lineEditAclUser.text())) else None
    pAclGroup = str_convert(self.lineEditAclGroup.text()).rstrip().lstrip() if(str_convert(self.lineEditAclGroup.text())) else None
    pRI = 1 if(self.checkRI.isChecked()) else 0
    pDesc = str_convert(self.lineEditDesc.text()).rstrip().lstrip() if(str_convert(self.lineEditDesc.text())) else None
    linked = str_convert(self.lineEditLinked.text()).rstrip().lstrip()
    createdUser = os.environ['rbhusPipe_acl_user']
    self.wtf = "connecting"
    utilsPipe.setupProj(projType=str_convert(pType),
                            projName=str_convert(pName),
                            directory=str_convert(pDir),
                            admins=str_convert(pAdmins),
                            rbhusRenderIntegration=pRI,
                            rbhusRenderServer=None,
                            aclUser=str_convert(pAclUser),
                            aclGroup=str_convert(pAclGroup),
                            dueDate=pDueDate,
                            description=str_convert(pDesc),
                            createdUser=str_convert(createdUser))
    
    
  def setUsers(self):
    users = utilsPipe.getUsers()
    outUsers = subprocess.Popen([sys.executable,selectCheckBoxCmd,"-i",",".join(users),"-d",str_convert(self.lineEditAdmins.text()).rstrip().lstrip()],stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].rstrip().lstrip()
    outUsers = str_convert(outUsers)
    if(outUsers == ""):
      outUsers = str_convert(self.lineEditAdmins.text()).rstrip().lstrip()
    self.lineEditAdmins.setText(str_convert(outUsers))
  

  def setProjTypes(self):
    rows = utilsPipe.getProjTypes()
    self.comboProjType.clear()
    if(rows):
      for row in rows:
        self.comboProjType.addItem(str_convert(row['type']))
      
      return(1)
    return(0)     
  
  
  def setDirectory(self):
    dirs = utilsPipe.getDirMaps()
    self.comboDirectory.clear()
    if(dirs):
      for d in dirs:
        self.comboDirectory.addItem(str_convert(d['directory']))
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
    