#!/usr/bin/python
from PyQt4 import QtCore, QtGui
import glob
import os
import sys


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
    
    
  def center(self):
    Form.move(QtGui.QApplication.desktop().screen().rect().center()- Form.rect().center())

  
  def cProj(self):
    pType = self.comboProjType.currentText()
    pName = self.lineEditName.text() if(self.lineEditName.text()) else None
    pDir = self.comboDirectory.currentText() 
    pDueDate = str(self.dateEditDue.dateTime().date().year()) +"-"+ str(self.dateEditDue.dateTime().date().month()) +"-"+ str(self.dateEditDue.dateTime().date().day()) +" "+ str(self.dateEditDue.dateTime().time().hour()) +":"+ str(self.dateEditDue.dateTime().time().minute()) +":" + str(self.dateEditDue.dateTime().time().second())
    pAdmins = self.lineEditAdmins.text() if(self.lineEditAdmins.text()) else None
    pAclUser = self.lineEditAclUser.text() if(self.lineEditAclUser.text()) else None
    pAclGroup = self.lineEditAclGroup.text() if(self.lineEditAclGroup.text()) else None
    pRI = 1 if(self.checkRI.isChecked()) else 0
    pDesc = self.lineEditDesc.text() if(self.lineEditDesc.text()) else None
    pCUser = self.username
    utilsPipe.createProject(projType=pType,
                            projName=pName,
                            directory=pDir,
                            admins=pAdmins,
                            rbhusRenderIntergration=pRI,
                            rbhusRenderServer=None,
                            aclUser=pAclUser,
                            aclGroup=pAclGroup,
                            createdUser=pCUser,
                            dueDate=pDueDate,
                            description=pDesc)
  
  
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
    defs = utilsPipe.getProjDefaults()
    




if __name__ == "__main__":
  app = QtGui.QApplication(sys.argv)
  Form = QtGui.QMainWindow()
  ui = Ui_Form()
  ui.setupUi(Form)
  Form.show()
  sys.exit(app.exec_())
    