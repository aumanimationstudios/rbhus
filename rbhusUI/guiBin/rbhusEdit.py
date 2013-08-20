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


import rbhusEditMod
print(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")
sys.path.append(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")
import db
import constants
import utils as rUtils


try:
  _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
  _fromUtf8 = lambda s: s
  

class Ui_Form(rbhusEditMod.Ui_rbhusEdit):
    
    
  def setupUi(self, Form):
    
    self.task = rUtils.tasks(tId = sys.argv[1].rstrip().lstrip())
    self.taskValues = self.task.taskDetails
    
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(_fromUtf8(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/rbhus.svg")), QtGui.QIcon.Normal, QtGui.QIcon.On)
    Form.setWindowIcon(icon)
    
    rbhusEditMod.Ui_rbhusEdit.setupUi(self,Form)
    self.popEditItems()
    
    self.pushFileName.clicked.connect(self.selectFileName)
    self.pushOutPutDir.clicked.connect(self.selectOutPutDir)
    self.pushBfc.clicked.connect(self.selectBfc)
    self.pushAfc.clicked.connect(self.selectAfc)
    self.pushLogOpen.clicked.connect(self.selectLogBase)
    self.checkAfterTime.clicked.connect(self.afterTimeEnable)
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
    self.lineEditFileName.textChanged.connect(self.reset_fileName)
    self.lineEditFrange.textChanged.connect(self.reset_fRange)
    self.lineEditImageName.textChanged.connect(self.reset_imageName)
    self.lineEditLogbase.textChanged.connect(self.reset_logbase)
    self.lineEditOutPutDir.textChanged.connect(self.reset_outPutDir)
    self.lineEditDescription.textChanged.connect(self.reset_desc)
    self.lineEditResolution.textChanged.connect(self.reset_res)
    self.lineEditCamera.textChanged.connect(self.reset_cam)
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
    editDict = {}
    if(self.db_filetype):
      editDict["fileType"] = str(self.comboType.currentText())
      self.db_filetype = 0
    if(self.db_renderer):
      editDict["renderer"] = str(self.comboRenderer.currentText())
      self.db_renderer = 0
    if(self.db_hostgroup):
      editDict["hostGroups"] = str(self.lineEditHostGroups.text())
      self.db_hostgroup = 0
    if(self.db_filename):
      editDict["fileName"] = str(self.lineEditFileName.text().replace("\\","/"))
      self.db_filename = 0
    if(self.db_cam)  :
      editDict["camera"] = str(self.lineEditCamera.text())
      self.db_cam = 0
    if(self.db_res):
      editDict["resolution"] = str(self.lineEditResolution.text())
    if(self.db_imagename):
      editDict["outName"] = str(self.lineEditImageName.text())
      self.db_imagename = 0
    if(self.db_outputdir):
      editDict["outDir"] = str(self.lineEditOutPutDir.text().replace("\\","/"))
      self.db_outputdir = 0
    if(self.db_bfc):
      editDict["beforeFrameCmd"] = str(self.lineEditBfc.text().replace("\\","/"))
      self.db_bfc = 0
    if(self.db_afc):
      editDict["afterFrameCmd"] = str(self.lineEditAfc.text().replace("\\","/"))
      self.db_afc = 0
    if(self.db_logbase):
      editDict["logBase"] = str(self.lineEditLogbase.text().replace("\\","/"))
      self.db_logbase = 0
    if(self.db_aftertime):
      editDict["afterTime"] = str(self.afterTimeEdit.dateTime().date().year()) +"-"+ str(self.afterTimeEdit.dateTime().date().month()) +"-"+ str(self.afterTimeEdit.dateTime().date().day()) +" "+ str(self.afterTimeEdit.dateTime().time().hour()) +":"+ str(self.afterTimeEdit.dateTime().time().minute()) +":" + str(self.afterTimeEdit.dateTime().time().second())
    if(self.db_rerunthresh):
      editDict["rerunThresh"] = str(self.db_rerunthresh)
      self.db_rerunthresh = 0
    if(self.db_framerange):
      editDict["fRange"] = str(self.lineEditFrange.text())
      self.db_framerange = 0
    if(self.db_priority):
      editDict["priority"] = str(self.db_priority)
      self.db_priority = 0
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
    print(str(editDict))
    try:
      self.task.edit(editDict)
    except:
      print(str(sys.exc_info()))
      
    self.taskValues = self.task.taskDetails
    self.popEditItems()  
    
  
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
    if(self.taskValues):
      self.lineEditFileName.setText(self.taskValues['fileName'])
      self.lineEditOutPutDir.setText(self.taskValues['outDir'])
      self.lineEditImageName.setText(self.taskValues['outName'])
      self.lineEditFrange.setText(self.taskValues['fRange'])
      self.lineEditLogbase.setText(self.taskValues['logBase'])
      self.lineEditAfc.setText(self.taskValues['afterFrameCmd'])
      self.lineEditCamera.setText(self.taskValues['camera'])
      self.lineEditLayer.setText(self.taskValues['layer'])
      self.lineEditResolution.setText(self.taskValues['resolution'])
      self.lineEditBfc.setText(self.taskValues['beforeFrameCmd'])
      self.lineEditImageType.setText(self.taskValues['imageType'])
      self.spinRerunThresh.setValue(self.taskValues['rerunThresh'])
      self.spinMinBatch.setValue(self.taskValues['minBatch'])
      self.spinMaxBatch.setValue(self.taskValues['maxBatch'])
      self.spinPriority.setValue(self.taskValues['priority'])
      self.afterTimeEdit.setTime(QtCore.QTime(self.taskValues['afterTime'].hour, self.taskValues['afterTime'].minute, self.taskValues['afterTime'].second))
      self.afterTimeEdit.setDate(QtCore.QDate(self.taskValues['afterTime'].year, self.taskValues['afterTime'].month, self.taskValues['afterTime'].day))
      self.lineEditDescription.setText(self.taskValues['description'])
      self.lineEditAfterTask.setText(self.taskValues['afterTasks'])
      batchFF = self.taskValues['batch']
      self.comboBatching.setCurrentIndex(batchFF)
      batchAD = constants.batchStatus[batchFF]
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
    print(self.db_rerunthresh)
    
    
  def getMinBatch(self):
    self.db_minbatch = self.spinMinBatch.value()
    print(self.db_minbatch)

  def getMaxBatch(self):
    self.db_maxbatch = self.spinMaxBatch.value()
    print(self.db_maxbatch)
    
  def getPriority(self):
    self.db_priority = self.spinPriority.value()
    print(self.db_priority)
  
  def afterTimeEnable(self):
    cAT = self.checkAfterTime.isChecked()
    if(cAT):
      self.afterTimeEdit.setEnabled(True)
      self.db_aftertime = 1
    else:
      self.afterTimeEdit.setEnabled(False)

  
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
        print(str(self.taskValues['fileType']))
        if(row.endswith(str(self.taskValues['fileType']))):
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
        print(str(self.taskValues['os']))
        if(row.endswith(str(self.taskValues['os']))):
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
      for x in renders[str(self.comboType.currentText())]:
        self.comboRenderer.addItem(_fromUtf8(x))
        if(x.endswith(str(self.taskValues['renderer']))):
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
        #print(str(self.taskValues['renderer']))
        #if(row.endswith(str(self.taskValues['renderer']))):
          #setIndx = indx
        #indx = indx + 1
      
      #self.comboRenderer.setCurrentIndex(setIndx)
      #return(1)
    #else:
      #return(0)
      
    
  def setHostGroups(self):
    rows = rUtils.getHostGroups()
    self.lineEditHostGroups.setText(self.taskValues['hostGroups'])

  
  
  
  def updateTask(self, fieldName, fieldValue):
    try:
      conn = db.connRbhus()
      cursor = conn.cursor()
      cursor.execute("update tasks set "+ fieldName +" = "+ fieldValue +" where id="+ str(sys.argv[1].rstrip().lstrip()))
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