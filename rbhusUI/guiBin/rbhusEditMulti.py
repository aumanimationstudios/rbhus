#!/usr/bin/python

from PyQt4 import QtCore, QtGui
import glob
import os
import sys
import datetime
import subprocess

dirSelf = os.path.dirname(os.path.realpath(__file__))
print(dirSelf)
sys.path.append(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep) + os.sep + "lib")


scb = "selectCheckBox.py"

selectCheckBoxCmd = dirSelf.rstrip(os.sep) + os.sep + scb
selectCheckBoxCmd = selectCheckBoxCmd.replace("\\","/")



import rbhusEditMultiMod
print(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")
sys.path.append(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")
import db
import constants
import utils as rUtils


try:
  _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
  _fromUtf8 = lambda s: s
  

class Ui_Form(rbhusEditMultiMod.Ui_rbhusEdit):
    
    
  def setupUi(self, Form):
    
    
    
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(_fromUtf8(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/rbhus.svg")), QtGui.QIcon.Normal, QtGui.QIcon.On)
    Form.setWindowIcon(icon)
    
    rbhusEditMultiMod.Ui_rbhusEdit.setupUi(self,Form)
    self.taskDValues = rUtils.getDefaults("tasks")
    self.popEditItems()
    
    self.pushBfc.clicked.connect(self.selectBfc)
    self.pushAfc.clicked.connect(self.selectAfc)
    self.checkAfterTime.clicked.connect(self.afterTimeEnable)
    self.checkSloppy.clicked.connect(self.sloppyEnable)
    self.spinRerunThresh.valueChanged.connect(self.getSpinRerunThresh)
    self.spinPriority.valueChanged.connect(self.getPriority)
    self.spinMinBatch.valueChanged.connect(self.getMinBatch)
    self.spinMaxBatch.valueChanged.connect(self.getMaxBatch)
    self.afterTimeEdit.dateTimeChanged.connect(self.afePrint)
    self.pushSelectHostGroups.clicked.connect(self.hostGroupPrint)
    self.comboBatching.currentIndexChanged.connect(self.batchStatus)
    self.comboOsType.currentIndexChanged.connect(self.osTypesPrint)
    self.comboType.currentIndexChanged.connect(self.fileTypePrint)
    self.comboRenderer.currentIndexChanged.connect(self.rendererPrint)
    self.pushApply.clicked.connect(self.applyNew)
    self.pushCancel.clicked.connect(self.popEditItems)
    self.lineEditAfc.textChanged.connect(self.reset_afc)
    self.lineEditBfc.textChanged.connect(self.reset_bfc)
    self.lineEditFrange.textChanged.connect(self.reset_fRange)
    self.lineEditDescription.textChanged.connect(self.reset_desc)
    self.lineEditAfterTask.textChanged.connect(self.reset_afterTask)
    print self.afterTimeEdit.dateTime().toString()
    
    
    self.db_filetype = 0
    self.db_hostgroup = 0
    self.db_filename = 0
    self.db_imagename = 0
    self.db_outputdir = 0
    self.db_bfc = 0
    self.db_afc = 0
    self.db_logbase = 0
    self.db_aftertime = 0
    self.db_rerunthresh = 0
    self.db_priority = 0
    self.db_framerange = 0
    self.db_minbatch = 0
    self.db_maxbatch = 0
    self.db_batch = -1
    self.db_desc = 0
    self.db_cam = 0
    self.db_res = 0
    self.db_imageType = 0
    self.db_outname = 0
    self.db_os = 0
    self.db_afterTask = 0
    self.db_layer = 0
    self.db_renderer = 0
    self.db_afterTaskSloppy = 0
    
  def reset_variables(self):
    self.db_filetype = 0
    self.db_hostgroup = 0
    self.db_filename = 0
    self.db_imagename = 0
    self.db_outputdir = 0
    self.db_bfc = 0
    self.db_afc = 0
    self.db_logbase = 0
    self.db_aftertime = 0
    self.db_rerunthresh = 0
    self.db_priority = 0
    self.db_framerange = 0
    self.db_minbatch = 0
    self.db_maxbatch = 0
    self.db_batch = -1
    self.db_desc = 0
    self.db_cam = 0
    self.db_res = 0
    self.db_imageType = 0
    self.db_outname = 0
    self.db_os = 0
    self.db_afterTask = 0
    self.db_layer = 0
    self.db_renderer = 0
    self.db_afterTaskSloppy = 0
    
  def reset_cam(self):
    self.db_cam = 1
    
  def reset_res(self):
    self.db_res = 1
    
  def reset_outPutDir(self):
    self.db_outputdir = 1
  
  def reset_logbase(self):
    self.db_logbase = 1
  
  def reset_imageName(self):
    self.db_imagename = 1
  
  def reset_fRange(self):
    self.db_framerange = 1
  
  def reset_fileName(self):
    self.db_filename = 1
  
  def reset_bfc(self):
    self.db_bfc = 1
    
    
  def reset_desc(self):
    self.db_desc = 1
    
  def reset_afc(self):
    self.db_afc = 1
  
  def reset_afterTask(self):
    self.db_afterTask = 1
    
    
  def applyNew(self):
    for t in sys.argv[1].rstrip().lstrip().split(","):
      editDict = {}
      self.task = rUtils.tasks(tId = t)
      if(self.db_filetype):
        editDict["fileType"] = str(self.comboType.currentText())
      if(self.db_renderer):
        editDict["renderer"] = str(self.comboRenderer.currentText())
      if(self.db_hostgroup):
        editDict["hostGroups"] = str(self.lineEditHostGroups.text())
      if(self.db_bfc):
        editDict["beforeFrameCmd"] = str(self.lineEditBfc.text().replace("\\","/"))
      if(self.db_afc):
        editDict["afterFrameCmd"] = str(self.lineEditAfc.text().replace("\\","/"))
      if(self.db_aftertime):
        editDict["afterTime"] = str(self.afterTimeEdit.dateTime().date().year()) +"-"+ str(self.afterTimeEdit.dateTime().date().month()) +"-"+ str(self.afterTimeEdit.dateTime().date().day()) +" "+ str(self.afterTimeEdit.dateTime().time().hour()) +":"+ str(self.afterTimeEdit.dateTime().time().minute()) +":" + str(self.afterTimeEdit.dateTime().time().second())
      if(self.db_rerunthresh):
        editDict["rerunThresh"] = str(self.db_rerunthresh)
      if(self.db_framerange):
        editDict["fRange"] = str(self.lineEditFrange.text())
      if(self.db_priority):
        editDict["priority"] = str(self.db_priority)
      if(self.db_batch != -1):
        editDict['batch'] = str(self.db_batch)
      if(self.db_maxbatch):
        editDict['maxBatch'] = str(self.db_maxbatch)
      if(self.db_minbatch):
        editDict['minBatch'] = str(self.db_minbatch)
      if(self.db_desc):
        editDict['description'] = str(self.db_desc)
      if(self.db_os):
        editDict['os'] = str(self.comboOsType.currentText())
      if(self.db_afterTask):
        editDict['afterTasks'] = str(self.lineEditAfterTask.text())
      if(self.db_afterTaskSloppy):
        editDict['afterTaskSloppy'] = 1 & self.checkSloppy.isChecked()
        
      print(editDict)
      try:
        self.task.edit(editDict)
      except:
        print(str(sys.exc_info()))
        
      
    #self.popEditItems()  
    
  
  def hostGroupPrint(self):
    groups = rUtils.getHostGroups()
    outGroups = subprocess.Popen([sys.executable,selectCheckBoxCmd,"-i",",".join(groups),"-d",str(self.lineEditHostGroups.text()).rstrip().lstrip()],stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].rstrip().lstrip()
    if(outGroups == ""):
      return
    print(outGroups)
    self.lineEditHostGroups.setText(_fromUtf8(outGroups))
    self.db_hostgroup = 1
  
  def osTypesPrint(self):
    print(self.comboOsType.currentText())
    self.db_os = 1
  
  def rendererPrint(self):
    print(self.comboRenderer.currentText())
    self.db_renderer = 1
  
  def fileTypePrint(self):
    print(self.comboType.currentText())
    self.setRenderer()
    self.db_filetype = 1
    
  def batchStatus(self):
    print(self.comboBatching.currentText())
    self.db_batch = constants.batchStatus[str(self.comboBatching.currentText())]
    
    
  def afePrint(self):
    print(self.afterTimeEdit.dateTime().date().month())
    print(self.afterTimeEdit.dateTime().date().day())
    print(self.afterTimeEdit.dateTime().date().year())
    print(self.afterTimeEdit.dateTime().time().hour())
    print(self.afterTimeEdit.dateTime().time().minute())
    print(self.afterTimeEdit.dateTime().time().second())
    
  def popEditItems(self):
    if(self.taskDValues):
      self.lineEditFrange.setText(self.taskDValues['fRange'])
      self.lineEditAfc.setText(self.taskDValues['afterFrameCmd'])
      self.lineEditBfc.setText(self.taskDValues['beforeFrameCmd'])
      self.spinRerunThresh.setValue(int(self.taskDValues['rerunThresh']))
      self.spinMinBatch.setValue(int(self.taskDValues['minBatch']))
      self.spinMaxBatch.setValue(int(self.taskDValues['maxBatch']))
      self.spinPriority.setValue(int(self.taskDValues['priority']))
      #self.afterTimeEdit.setTime(QtCore.QTime(self.taskDValues['afterTime'].hour, self.taskDValues['afterTime'].minute, self.taskDValues['afterTime'].second))
      #self.afterTimeEdit.setDate(QtCore.QDate(self.taskDValues['afterTime'].year, self.taskDValues['afterTime'].month, self.taskDValues['afterTime'].day))
      self.lineEditDescription.setText(self.taskDValues['description'])
      self.lineEditAfterTask.setText(self.taskDValues['afterTasks'])
      
      self.checkSloppy.blockSignals(True)
      if(self.taskDValues['afterTaskSloppy'] == constants.afterTaskSloppyEnable):
        self.checkSloppy.setChecked(True)
      else:
        self.checkSloppy.setChecked(False)
      self.checkSloppy.blockSignals(False)
      
      batchFF = self.taskDValues['batch']
      self.comboBatching.setCurrentIndex(int(batchFF))
      batchAD = constants.batchStatus[int(batchFF)]
      self.setFileTypes()
      self.setHostGroups()
      self.setOsTypes()
      #self.setRenderer()
      self.reset_variables()
      return(1)
    else:
      return(0)
  
  
  
  def getSpinRerunThresh(self):
    self.db_rerunthresh = self.spinRerunThresh.value()
    
    
  def getMinBatch(self):
    self.db_minbatch = self.spinMinBatch.value()

  def getMaxBatch(self):
    self.db_maxbatch = self.spinMaxBatch.value()
    
  def getPriority(self):
    self.db_priority = self.spinPriority.value()
  
  def afterTimeEnable(self):
    cAT = self.checkAfterTime.isChecked()
    if(cAT):
      self.afterTimeEdit.setEnabled(True)
      self.db_aftertime = 1
    else:
      self.afterTimeEdit.setEnabled(False)

  
  def sloppyEnable(self):
    self.db_afterTaskSloppy = 1
  
  
  def selectFileName(self):
    fila = QtGui.QFileDialog.getOpenFileName()
    if(fila):
      self.lineEditFileName.setText(fila.replace("\\","/"))
      self.db_filename = fila

  def selectOutPutDir(self):
    fila = QtGui.QFileDialog.getExistingDirectory()
    if(fila):
      self.lineEditOutPutDir.setText(fila.replace("\\","/"))
      self.db_outputdir = fila
      

  def selectLogBase(self):
    fila = QtGui.QFileDialog.getExistingDirectory()
    if(fila):
      self.lineEditLogbase.setText(fila)
      self.db_logbase = fila
  
  def selectBfc(self):
    fila = QtGui.QFileDialog.getOpenFileName()
    if(fila):
      self.lineEditBfc.setText(fila)
      self.db_bfc = fila

  def selectAfc(self):
    fila = QtGui.QFileDialog.getOpenFileName()
    if(fila):
      self.lineEditAfc.setText(fila)
      self.db_afc = fila
      
      
  def setFileTypes(self):
    rows = rUtils.getFileTypes()
    self.comboType.clear()  
    if(rows):
      indx = 0
      setIndx = 0
      for row in rows:
        self.comboType.addItem(_fromUtf8(row))
        print(str(self.taskDValues['fileType']))
        if(row.endswith(str(self.taskDValues['fileType']))):
          setIndx = indx
        indx = indx + 1
      
      self.comboType.setCurrentIndex(setIndx)
      self.setRenderer()
      return(1)
    else:
      return(0)
      
    
  def setOsTypes(self):
    rows = rUtils.getOsTypes()
    self.comboOsType.clear()  
    if(rows):
      indx = 0
      setIndx = 0
      for row in rows:
        self.comboOsType.addItem(_fromUtf8(row))
        print(str(self.taskDValues['os']))
        if(row.endswith(str(self.taskDValues['os']))):
          setIndx = indx
        indx = indx + 1
      
      self.comboOsType.setCurrentIndex(setIndx)
      return(1)
    else:
      return(0)
      
      
  def setRenderer(self):
    renders = rUtils.getRenderers()
    self.comboRenderer.clear()
    indx = 0
    setIndx = 0
    try:
      for x in renders:
        if(x['fileType'] == str(self.comboType.currentText())):
          self.comboRenderer.addItem(_fromUtf8(x['renderer']))
          if(x.endswith(str(self.taskDValues['renderer']))):
            setIndx = indx
          indx = indx + 1
        self.comboRenderer.setCurrentIndex(setIndx)
      return(1)
    except:
      return(0)
      
    #rows = rUtils.getRenderers()
    #self.comboRenderer.clear()  
    #if(rows):
      #indx = 0
      #setIndx = 0
      #for row in rows:
        #self.comboRenderer.addItem(_fromUtf8(row))
        #print(str(self.taskDValues['renderer']))
        #if(row.endswith(str(self.taskDValues['renderer']))):
          #setIndx = indx
        #indx = indx + 1
      
      #self.comboRenderer.setCurrentIndex(setIndx)
      #return(1)
    #else:
      #return(0)
      
    
  def setHostGroups(self):
    rows = rUtils.getHostGroups()
    self.lineEditHostGroups.setText(self.taskDValues['hostGroups'])

  
  
  
  def updateTask(self, fieldName, fieldValue):
    try:
      conn = db.connRbhus()
      cursor = conn.cursor()
      cursor.execute("update tasks set "+ fieldName +" = "+ fieldValue +" where id="+ str(" or id=".join(a.split(","))))
      cursor.close()
      conn.close()
      print("updated "+ str(fieldName) +" with value "+ str(fieldValue))
    except:
      print("Error connecting to db")
      return(0)
  
    
if __name__ == "__main__":
  app = QtGui.QApplication(sys.argv)
  Form = QtGui.QMainWindow()
  ui = Ui_Form()
  ui.setupUi(Form)
  Form.show()
  sys.exit(app.exec_())