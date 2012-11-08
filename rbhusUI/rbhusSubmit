#!/usr/bin/python
from PyQt4 import QtCore, QtGui
import glob
import os
import sys
import datetime

progPath =  sys.argv[0].split(os.sep)
print progPath
if(len(progPath) > 1):
  pwd = os.sep.join(progPath[0:-1])
  cwd = os.path.abspath(pwd)
else:
  cwd = os.path.abspath(os.getcwd())
  
sys.path.append(cwd.rstrip(os.sep) + os.sep + "lib")
import rbhusSubmitMod
print(cwd.rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")
sys.path.append(cwd.rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")
import db
import constants
import utils as rUtils


try:
  _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
  _fromUtf8 = lambda s: s
  

class Ui_Form(rbhusSubmitMod.Ui_rbhusSubmit):
  def setupUi(self, Form):
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(_fromUtf8(cwd.rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/rbhus.svg")), QtGui.QIcon.Normal, QtGui.QIcon.On)
    Form.setWindowIcon(icon)
    
    rbhusSubmitMod.Ui_rbhusSubmit.setupUi(self,Form)
    self.pushFileName.clicked.connect(self.selectFileName)
    self.pushOutDir.clicked.connect(self.selectOutDir)
    self.pushSubmit.clicked.connect(self.submitTasks)
    self.comboHostGroup.currentIndexChanged.connect(self.printGroupSel)
    self.comboPrio.currentIndexChanged.connect(self.printPrioSel)
    self.comboFileType.currentIndexChanged.connect(self.fileTypePrint)
    self.comboOsType.currentIndexChanged.connect(self.osTypePrint)
    groups = rUtils.getHostGroups()
    ostypes = rUtils.getOsTypes()
    ftypes = rUtils.getFileTypes()
    for group in groups:
      self.comboHostGroup.addItem(_fromUtf8(group))
    for ft in ftypes:
      self.comboFileType.addItem(_fromUtf8(ft))
    for ost in ostypes:
      self.comboOsType.addItem(_fromUtf8(ost))
      
    
    
  def printGroupSel(self):
    print self.comboHostGroup.currentText()
    
    
  def printPrioSel(self):
    print self.comboPrio.currentText()
    
  
  
  def fileTypePrint(self):
    print(self.comboFileType.currentText())
    renders = rUtils.getRenderers()
    self.comboRenderer.clear()
    for x in renders[str(self.comboFileType.currentText())]:
      self.comboRenderer.addItem(_fromUtf8(x))

    
  
  def osTypePrint(self):
    print(self.comboOsType.currentText())
  
  
  def setFileTypes(self):
    rows = rUtils.getFileTypes()
      
    if(rows):
      for row in rows:
        self.comboFileType.addItem(_fromUtf8(row))
      
      return(1)
    else:
      return(0)
      
      
  def setOsTypes(self):
    rows = rUtils.getOsTypes()
      
    if(rows):
      for row in rows:
        self.comboOsType.addItem(_fromUtf8(row))
      
      return(1)
    else:
      return(0)     
  
  def selectFileName(self):
    fila = QtGui.QFileDialog.getOpenFileName()
    if(fila):
      self.lineEditFileName.setText(fila)
      
  def selectOutDir(self):
    dirac = QtGui.QFileDialog()
    dirac.FileMode(QtGui.QFileDialog.Directory)
    dira = dirac.getExistingDirectory()
    if(dira):
      self.lineEditOutDir.setText(dira)
      
      
  def submitTasks(self):
    fileName = self.lineEditFileName.text()
    fRange = self.lineEditFrange.text()
    if(fileName and fRange):
      print fileName
      print fRange
      
      prios = str(self.comboPrio.currentText())
      ostype = str(self.comboOsType.currentText())
      filetype = str(self.comboFileType.currentText())
      if(prios == "low"):
        p = 1
      if(prios == "high"):
        p = 9000
      if(prios == "normal"):
        p = 5000
      if((filetype == "3dsmax") and ((ostype == "default") or (ostype == "win"))):
        logB = "z:\\\\vajram essenza\\\\isomatrics\\\\logs\\\\"
        afterFrameC = "Z:\\\\pythonTestWindoze.DONOTDELETE\\\\rbhus\\\\etc\\\\3dsmax\\\\afterFrame.py"
        beforeFrameC = "Z:\\\\pythonTestWindoze.DONOTDELETE\\\\rbhus\\\\etc\\\\3dsmax\\\\beforeFrame.py"
      else:
        logB = "default"
        afterFrameC = "default"
        beforeFrameC = "default"
      try:
        conn = db.connRbhus()
        cursor = conn.cursor()
        cursor.execute("insert into tasks (fileName, logBase, \
                        fRange, fileType, afterFrameCmd, beforeFrameCmd, \
                        hostGroups, submitTime, priority, afterTasks, \
                        renderer, imageType, outDir, outName, layer, os) \
                        values (\'"+ str(fileName) +"\', \'"+ str(logB) +"\', \
                        \'"+ str(fRange) +"\', \'"+ str(filetype) +"\', \'"+ str(afterFrameC) +"\', \'"+ str(beforeFrameC) +"\', \
                        \'"+ str(self.comboHostGroup.currentText()) +"\', now(), "+ str(p) +", \'"+ str(self.lineEditAfterTask.text())  +"\', \
                        \'"+ str(self.comboRenderer.currentText()) +"\', \'"+ str(self.lineEditImageType.text()) +"\', \'"+ str(self.lineEditOutDir.text()) +"\', \'"+ str(self.lineEditOutName.text()) +"\', \'" +str(self.lineEditLayer.text()) +"\', \'"+ str(self.comboOsType.currentText()) +"\')")
        cursor.close()
        cursor = conn.cursor(db.dict)
        cursor.execute("select last_insert_id()")
        rows = cursor.fetchall()
        lastID =  rows[0]['last_insert_id()']
        cursor.close()
        conn.close()
      except:
        print("Error connecting to db : "+ str(sys.exc_info()))
        return()
    
    QtGui.qApp.closeAllWindows()
    
    
    
    
    
    
if __name__ == "__main__":
  app = QtGui.QApplication(sys.argv)
  Form = QtGui.QMainWindow()
  ui = Ui_Form()
  ui.setupUi(Form)
  Form.show()
  sys.exit(app.exec_())
    
    