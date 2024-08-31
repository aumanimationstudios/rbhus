#!/usr/bin/env python3
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys
import os

file_dir = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-1])
base_dir = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-3])
ui_dir = os.path.join(base_dir,"rbhusUI","lib","qt5","rbhusPipe_assImporter")
rbhus_lib_dir = os.path.join(base_dir,"rbhus")

sys.path.append(base_dir)
import rbhus.dbPipe
import rbhus.constantsPipe
import rbhus.utilsPipe
import rbhus.debug

import time

from PyQt5 import QtWidgets, QtGui, QtCore, uic

projects = []
projectToImportTo = sys.argv[1]


ui_main = os.path.join(ui_dir,"ui_main.ui")
ui_ass_for_import = os.path.join(ui_dir,"ui_ass_for_import.ui")
ui_progress_list = os.path.join(ui_dir,"progress_list.ui")
ui_progress_list_dict = {}


updateAssThreads = []


def str_convert(text):
  if isinstance(text, bytes):
    return str(text, 'utf-8')
  return str(text)


class importAssQthread(QtCore.QThread):
  impStarted = QtCore.pyqtSignal()
  impFinished = QtCore.pyqtSignal()
  impAssetStart = QtCore.pyqtSignal(str,str,bool)
  impAssetResult = QtCore.pyqtSignal(str,bool,str)

  def __init__(self,projectToImportTo,assetList,parent=None):
    super(importAssQthread, self).__init__(parent)
    self.assets = assetList
    self.project = projectToImportTo

  def run(self):
    if (self.assets):
      self.impStarted.emit()
      for impAsset in self.assets:
        self.impAssetStart.emit(str(impAsset['assetPath']),str(impAsset['assetPathColor']),impAsset['getVersions'])
        returnStatus = rbhus.utilsPipe.importAssets(toProject=self.project, assetPath=impAsset['assetPath'], toAssetPath=impAsset['toAssetPath'], getVersions=impAsset['getVersions'],force=impAsset['force'])

        time.sleep(0.5)
        if(returnStatus == 1):
          self.impAssetResult.emit(str(impAsset['assetPath']),True,"done")
        elif (returnStatus == 3):
          self.impAssetResult.emit(str(impAsset['assetPath']), False, "no permission")
        elif (returnStatus == 4):
          self.impAssetResult.emit(str(impAsset['assetPath']), False, "asset exists. use force")
        else:
          self.impAssetResult.emit(str(impAsset['assetPath']), False, "fail")
      self.impFinished.emit()




class updateAssQthread(QtCore.QThread):
  assSignal = QtCore.pyqtSignal(str,str)
  progressSignal = QtCore.pyqtSignal(int,int,int)
  totalAssets = QtCore.pyqtSignal(int)

  def __init__(self,project,whereDict,parent=None):
    super(updateAssQthread, self).__init__(parent)
    self.projSelected = project
    self.dbcon = rbhus.dbPipe.dbPipe()
    self.whereDict = whereDict
    self.pleaseStop = False

  # def __del__(self):
  #
  #   self.dbcon.disconnect()

  def run(self):
    if(self.projSelected):
      rbhus.debug.debug("started thread")
      projWhere = []
      projWhereString = " where "
      assesUnsorted = []
      for x in self.projSelected:
        assesForProj = rbhus.utilsPipe.getProjAsses(x,whereDict=self.whereDict)
        if(assesForProj):
          assesUnsorted.extend(assesForProj)
      #   projWhere.append("projName = '" + x + "'")
      # projWhereString = "where " + " or ".join(projWhere)
      # print(projWhereString)


      # assesUnsorted = self.dbcon.execute("select * from assets " + projWhereString + " and status = " + str(rbhus.constantsPipe.assetStatusActive), dictionary=True)

      if (assesUnsorted):
        asses = sorted(assesUnsorted, key=lambda k: k['path'])
        minLength = 0
        maxLength = len(asses)
        self.totalAssets.emit(maxLength)
        current = 0
        for x in asses:
          if(self.pleaseStop == False):
            current = current + 1
            asset = rbhus.utilsPipe.assPathColorCoded(x)
            textAssArr = []
            for fc in asset.split(":"):
              textAssArr.append('<font color="' + fc.split("#")[1] + '">' + fc.split("#")[0] + '</font>')
            richAss = " " + "<b><i> : </i></b>".join(textAssArr)
            textAss = x['path']
            self.assSignal.emit(textAss,richAss)
            self.progressSignal.emit(minLength,maxLength,current)
            time.sleep(0.01)
          else:
            rbhus.debug.info("STOPPING THREAD")
            break
      else:
        minLength = 0
        maxLength = 1
        current = 1
        self.totalAssets.emit(0)
        self.progressSignal.emit(minLength, maxLength, current)



def getOriginalAsses(projectToImportTo):
  origWhereDict = {}
  origWhereDict['assignedWorker'] = os.environ['rbhusPipe_acl_user']

  originalAssets = rbhus.utilsPipe.getProjAsses(projectToImportTo, whereDict=origWhereDict)
  originalAssetsColord = []
  if(originalAssets):
    for x in originalAssets:
      originalAssetsColord.append(x['path'])
      # asset = rbhus.utilsPipe.assPathColorCoded(x)
      # textAssArr = []
      # for fc in asset.split(":"):
      #   textAssArr.append('<font color="' + fc.split("#")[1] + '">' + fc.split("#")[0] + '</font>')
      # richAss = " " + "<b><i> : </i></b>".join(textAssArr)
      # originalAssetsColord.append(richAss)
    originalAssetsColord.sort()
  originalAssetsColord.insert(0, "default")
  return(originalAssetsColord)



def updateAssets(mainUid):

  updateProjSelect(mainUid)
  setSequence(mainUid)
  updateAssetsForProjSelect(mainUid)

def pushRefresh(mainUid):
  updateProjSelect(mainUid)
  updateAssetsForProjSelect(mainUid)

def updateProjSelect(mainUid):
  global projects
  mainUid.listWidgetAssets.clear()
  items = mainUid.listWidgetProj.selectedItems()

  projects = []
  for x in items:
    projects.append(str(x.text()))


def updateAssetsForProjSelect(mainUid):
  global updateAssThreads
  global projects
  mainUid.listWidgetAssets.clear()
  whereDict = {}

  if str_convert(mainUid.comboStage.currentText()) and str_convert(mainUid.comboStage.currentText()) != "default":
    whereDict['stageType'] = str_convert(mainUid.comboStage.currentText())
  if str_convert(mainUid.comboNode.currentText()) and str_convert(mainUid.comboNode.currentText()) != "default":
    whereDict['nodeType'] = str_convert(mainUid.comboNode.currentText())
  if str_convert(mainUid.comboSeq.currentText()) and str_convert(mainUid.comboSeq.currentText()) != "default":
    whereDict['sequenceName'] = str_convert(mainUid.comboSeq.currentText())
  if str_convert(mainUid.comboScn.currentText()) and str_convert(mainUid.comboScn.currentText()) != "default":
    whereDict['sceneName'] = str_convert(mainUid.comboScn.currentText())
  if str_convert(mainUid.comboFile.currentText()) and str_convert(mainUid.comboFile.currentText()) != "default":
    whereDict['fileType'] = str_convert(mainUid.comboFile.currentText())
  if str_convert(mainUid.comboAssType.currentText()) and str_convert(mainUid.comboAssType.currentText()) != "default":
    whereDict['assetType'] = str_convert(mainUid.comboAssType.currentText())
  if(mainUid.checkTag.isChecked()):
    if(str(mainUid.lineEditSearch.text())):
      whereDict['tags'] = str_convert(mainUid.lineEditSearch.text())
  if (mainUid.checkAssName.isChecked()):
    if(str(mainUid.lineEditSearch.text())):
      whereDict['assName'] = str_convert(mainUid.lineEditSearch.text())
  if (mainUid.checkAssPath.isChecked()):
    if(str(mainUid.lineEditSearch.text())):
      whereDict['path'] = str_convert(mainUid.lineEditSearch.text())

  rbhus.debug.info(whereDict)

  if(updateAssThreads):
    for runingThread in updateAssThreads:
      if(runingThread.isRunning()):
        runingThread.assSignal.disconnect()
        runingThread.progressSignal.disconnect()
        runingThread.totalAssets.disconnect()
      updateAssThreads.remove(runingThread)

  updateAssThread = updateAssQthread(project = projects,whereDict=whereDict,parent=mainUid)
  updateAssThread.assSignal.connect(lambda textAss,richAss, mainUid=mainUid: updateAssSlot(mainUid, textAss, richAss))
  updateAssThread.progressSignal.connect(lambda minLength, maxLength , current, mainUid = mainUid: updateProgressBar(minLength,maxLength,current,mainUid))
  updateAssThread.totalAssets.connect(lambda total: mainUid.labelTotal.setText(str(total)))
  updateAssThread.start()
  updateAssThreads.append(updateAssThread)



def updateProgressBar(minLength,maxLength,current,mainUid):
  mainUid.progressBar.setMinimum(minLength)
  mainUid.progressBar.setMaximum(maxLength)
  mainUid.progressBar.setValue(current)


def updateAssSlot(mainUid, textAss,richAss):
  label = QtWidgets.QLabel()
  item = QtWidgets.QListWidgetItem()
  label.setTextFormat(QtCore.Qt.RichText)
  label.setText(richAss)
  item.assetPath = textAss
  item.assetPathColor = richAss
  mainUid.listWidgetAssets.addItem(item)
  mainUid.listWidgetAssets.setItemWidget(item, label)



def setSequence(mainUid):
  global projects
  mainUid.comboSeq.clear()
  mainUid.comboSeq.model().clear()
  try:
    mainUid.comboSeq.view().clicked.disconnect()
  except:
    rbhus.debug.error(sys.exc_info())
  seq = {}
  indx =  0
  foundIndx = -1

  for proj in projects:
    rows = rbhus.utilsPipe.getSequenceScenes(proj)
    # print(rows)
    if(rows):
      for row in rows:
        seq[row['sequenceName']] = 1
  # print(seq)
  model = QtGui.QStandardItemModel(len(seq),1)

  if(seq):
    sortedsc = []
    for s in seq.keys():
      if(s):
        sortedsc.append(s)

    sortedsc.sort()
    for row in sortedsc:
      item = QtGui.QStandardItem(row)
      item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
      item.setData(QtCore.Qt.Unchecked, QtCore.Qt.CheckStateRole)
      model.setItem(indx,0,item)
      abrush = QtGui.QBrush()
      color = QtGui.QColor()
      color.setAlpha(0)
      abrush.setColor(color)
      model.item(indx).setForeground(abrush)
      indx = indx + 1
    mainUid.comboSeq.setModel(model)
    mainUid.comboSeq.lineEdit().clear()
    mainUid.comboSeq.view().clicked.connect(lambda modelIndex, mainUid=mainUid: itemChangedSequence(modelIndex, mainUid))
    return(1)
  return(0)


def itemChangedSequence(modelIndex, mainUid):
  item = mainUid.comboSeq.model().itemFromIndex(modelIndex)
  if(item.checkState() == QtCore.Qt.Checked):
    item.setCheckState(QtCore.Qt.Unchecked)
    abrush = QtGui.QBrush()
    color = QtGui.QColor()
    color.setAlpha(0)
    abrush.setColor(color)
    item.setForeground(abrush)
  else:
    item.setCheckState(QtCore.Qt.Checked)
    abrush = QtGui.QBrush()
    color = QtGui.QColor()
    color.setGreen(10)
    color.setBlue(125)
    color.setRed(225)
    abrush.setColor(color)
    item.setForeground(abrush)

  selectedStages = []

  for i in range(0,mainUid.comboSeq.model().rowCount()):
    if(mainUid.comboSeq.model().item(i).checkState() == QtCore.Qt.Checked):
      selectedStages.append(str_convert(mainUid.comboSeq.model().item(i).text()))

  if(selectedStages):
    mainUid.comboSeq.setEditText(",".join(selectedStages))
  else:
    mainUid.comboSeq.lineEdit().clear()

def updateAssetsSeq(mainUid):
  textSelected = str_convert(mainUid.comboSeq.lineEdit().text()).split(",")
  rbhus.debug.info(textSelected)
  updateAssetsForProjSelect(mainUid)


def setScene(mainUid):
  global projects
  mainUid.comboScn.clear()
  mainUid.comboScn.model().clear()
  try:
    mainUid.comboScn.view().clicked.disconnect()
  except:
    rbhus.debug.error(sys.exc_info())
  if(not projects):
    return
  seqNames = str_convert(mainUid.comboSeq.currentText()).split(",")



  # mainUid.comboScn.clear()
  scenes = {}
  indx =  0
  foundIndx = -1

  for proj in projects:
    for x in seqNames:
      rows = rbhus.utilsPipe.getSequenceScenes(proj,seq=x)
      if(rows):
        for x in rows:
          scenes[x['sceneName']] = 1
  if(scenes):
    sortedsc = []
    for s in scenes.keys():
      if(s):
        sortedsc.append(s)

    sortedsc.sort()
    model = QtGui.QStandardItemModel(len(scenes),1)
    for x in sortedsc:
      item = QtGui.QStandardItem(x)
      item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
      #item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
      item.setData(QtCore.Qt.Unchecked, QtCore.Qt.CheckStateRole)
      model.setItem(indx,0,item)
      abrush = QtGui.QBrush()
      color = QtGui.QColor()
      color.setAlpha(0)
      abrush.setColor(color)
      model.item(indx).setForeground(abrush)
      indx = indx + 1
    mainUid.comboScn.setModel(model)
    mainUid.comboScn.lineEdit().clear()
    mainUid.comboScn.view().clicked.connect(lambda modelIndex, mainUid=mainUid: itemChangedScenes(modelIndex, mainUid))
    return(1)
  return(0)


def itemChangedScenes(modelIndex,mainUid):
  item = mainUid.comboScn.model().itemFromIndex(modelIndex)
  if(item.checkState() == QtCore.Qt.Checked):
    item.setCheckState(QtCore.Qt.Unchecked)
    abrush = QtGui.QBrush()
    color = QtGui.QColor()
    color.setAlpha(0)
    abrush.setColor(color)
    item.setForeground(abrush)
  else:
    item.setCheckState(QtCore.Qt.Checked)
    abrush = QtGui.QBrush()
    color = QtGui.QColor()
    color.setGreen(10)
    color.setBlue(125)
    color.setRed(225)
    abrush.setColor(color)
    item.setForeground(abrush)



  selectedStages = []

  for i in range(0,mainUid.comboScn.model().rowCount()):
    if(mainUid.comboScn.model().item(i).checkState() == QtCore.Qt.Checked):
      selectedStages.append(str_convert(mainUid.comboScn.model().item(i).text()))

  #debug.info("EVENT CALLED : "+ str(index.row()))
  if(selectedStages):
    mainUid.comboScn.setEditText(",".join(selectedStages))
  else:
    mainUid.comboScn.lineEdit().clear()

def setStageTypes(mainUid):
  rows = rbhus.utilsPipe.getStageTypes()
  #defStage = utilsPipe.getDefaults("stageTypes")
  mainUid.comboStage.clear()
  mainUid.comboStage.model().clear()
  try:
    mainUid.comboStage.view().clicked.disconnect()
  except:
    rbhus.debug.error(sys.exc_info())
  indx = 0
  model = QtGui.QStandardItemModel(len(rows),1)
  if(rows):
    for row in rows:
      item = QtGui.QStandardItem(row['type'])
      item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
      item.setData(QtCore.Qt.Unchecked, QtCore.Qt.CheckStateRole)
      model.setItem(indx,0,item)
      abrush = QtGui.QBrush()
      color = QtGui.QColor()
      color.setAlpha(0)
      abrush.setColor(color)
      model.item(indx).setForeground(abrush)
      indx = indx + 1
    mainUid.comboStage.setModel(model)
    mainUid.comboStage.lineEdit().clear()
    mainUid.comboStage.view().clicked.connect(lambda modelIndex, mainUid=mainUid : itemChangedStageType(modelIndex, mainUid))
    return(1)
  return(0)


def itemChangedStageType(modelIndex, mainUid):
  item = mainUid.comboStage.model().itemFromIndex(modelIndex)
  if (item.checkState() == QtCore.Qt.Checked):
    item.setCheckState(QtCore.Qt.Unchecked)
    abrush = QtGui.QBrush()
    color = QtGui.QColor()
    color.setAlpha(0)
    abrush.setColor(color)
    item.setForeground(abrush)

  else:
    item.setCheckState(QtCore.Qt.Checked)
    abrush = QtGui.QBrush()
    color = QtGui.QColor()
    color.setGreen(10)
    color.setBlue(125)
    color.setRed(225)
    abrush.setColor(color)
    item.setForeground(abrush)


  selectedStages = []

  for i in range(0, mainUid.comboStage.model().rowCount()):
    if (mainUid.comboStage.model().item(i).checkState() == QtCore.Qt.Checked):
      selectedStages.append(str_convert(mainUid.comboStage.model().item(i).text()))

  # debug.info("EVENT CALLED : "+ str(index.row()))
  if (selectedStages):
    mainUid.comboStage.setEditText(",".join(selectedStages))
  else:
    mainUid.comboStage.lineEdit().clear()


def setNodeTypes(mainUid):
  rows = rbhus.utilsPipe.getNodeTypes()
  #defStage = utilsPipe.getDefaults("stageTypes")
  mainUid.comboNode.clear()
  mainUid.comboNode.model().clear()
  try:
    mainUid.comboNode.view().clicked.disconnect()
  except:
    rbhus.debug.error(sys.exc_info())
  indx = 0
  model = QtGui.QStandardItemModel(len(rows),1)
  if(rows):
    for row in rows:
      item = QtGui.QStandardItem(row['type'])
      item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
      item.setData(QtCore.Qt.Unchecked, QtCore.Qt.CheckStateRole)
      model.setItem(indx,0,item)
      abrush = QtGui.QBrush()
      color = QtGui.QColor()
      color.setAlpha(0)
      abrush.setColor(color)
      model.item(indx).setForeground(abrush)
      indx = indx + 1
    mainUid.comboNode.setModel(model)
    mainUid.comboNode.lineEdit().clear()
    mainUid.comboNode.view().clicked.connect(lambda modelIndex, mainUid=mainUid : itemChangedNodeType(modelIndex, mainUid))
    return(1)
  return(0)


def itemChangedNodeType(modelIndex, mainUid):
  item = mainUid.comboNode.model().itemFromIndex(modelIndex)
  if (item.checkState() == QtCore.Qt.Checked):
    item.setCheckState(QtCore.Qt.Unchecked)
    abrush = QtGui.QBrush()
    color = QtGui.QColor()
    color.setAlpha(0)
    abrush.setColor(color)
    item.setForeground(abrush)

  else:
    item.setCheckState(QtCore.Qt.Checked)
    abrush = QtGui.QBrush()
    color = QtGui.QColor()
    color.setGreen(10)
    color.setBlue(125)
    color.setRed(225)
    abrush.setColor(color)
    item.setForeground(abrush)


  selectedStages = []

  for i in range(0, mainUid.comboNode.model().rowCount()):
    if (mainUid.comboNode.model().item(i).checkState() == QtCore.Qt.Checked):
      selectedStages.append(str_convert(mainUid.comboNode.model().item(i).text()))

  # debug.info("EVENT CALLED : "+ str(index.row()))
  if (selectedStages):
    mainUid.comboNode.setEditText(",".join(selectedStages))
  else:
    mainUid.comboNode.lineEdit().clear()



def setFileTypes(mainUid):
  rows = rbhus.utilsPipe.getFileTypes()
  #defStage = utilsPipe.getDefaults("stageTypes")
  mainUid.comboFile.clear()
  mainUid.comboFile.model().clear()
  try:
    mainUid.comboFile.view().clicked.disconnect()
  except:
    rbhus.debug.error(sys.exc_info())
  indx = 0
  model = QtGui.QStandardItemModel(len(rows),1)
  if(rows):
    for row in rows:
      item = QtGui.QStandardItem(row['type'])
      item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
      item.setData(QtCore.Qt.Unchecked, QtCore.Qt.CheckStateRole)
      model.setItem(indx,0,item)
      abrush = QtGui.QBrush()
      color = QtGui.QColor()
      color.setAlpha(0)
      abrush.setColor(color)
      model.item(indx).setForeground(abrush)
      indx = indx + 1

    mainUid.comboFile.setModel(model)
    mainUid.comboFile.lineEdit().clear()
    mainUid.comboFile.view().clicked.connect(lambda modelIndex, mainUid=mainUid : itemChangedFileType(modelIndex, mainUid))
    return(1)
  return(0)


def itemChangedFileType(modelIndex, mainUid):
  item = mainUid.comboFile.model().itemFromIndex(modelIndex)
  if (item.checkState() == QtCore.Qt.Checked):
    item.setCheckState(QtCore.Qt.Unchecked)
    abrush = QtGui.QBrush()
    color = QtGui.QColor()
    color.setAlpha(0)
    abrush.setColor(color)
    item.setForeground(abrush)

  else:
    item.setCheckState(QtCore.Qt.Checked)
    abrush = QtGui.QBrush()
    color = QtGui.QColor()
    color.setGreen(10)
    color.setBlue(125)
    color.setRed(225)
    abrush.setColor(color)
    item.setForeground(abrush)


  selectedStages = []

  for i in range(0, mainUid.comboFile.model().rowCount()):
    if (mainUid.comboFile.model().item(i).checkState() == QtCore.Qt.Checked):
      selectedStages.append(str_convert(mainUid.comboFile.model().item(i).text()))

  # debug.info("EVENT CALLED : "+ str(index.row()))
  if (selectedStages):
    mainUid.comboFile.setEditText(",".join(selectedStages))
  else:
    mainUid.comboFile.lineEdit().clear()

def setAssTypes(mainUid):
  rows = rbhus.utilsPipe.getAssTypes()
  mainUid.comboAssType.clear()
  mainUid.comboAssType.model().clear()
  try:
    mainUid.comboAssType.view().clicked.disconnect()
  except:
    rbhus.debug.error(sys.exc_info())
  indx = 0
  foundIndx = -1
  if(rows):
    for row in rows:
      mainUid.comboAssType.addItem(row['type'])
      indx = indx + 1
    mainUid.comboAssType.lineEdit().clear()
    return(1)
  return(0)


def refreshFilter(mainUid):
  setStageTypes(mainUid)
  setNodeTypes(mainUid)
  setFileTypes(mainUid)
  setAssTypes(mainUid)
  setSequence(mainUid)
  setScene(mainUid)

def impProgressStart(mainUid):
  mainUid.pushImport.setEnabled(False)
  mainUid.progressLeft.setMinimum(0)
  mainUid.progressLeft.setMaximum(0)
  mainUid.progressLeft.setValue(0)

  mainUid.progressRight.setMinimum(0)
  mainUid.progressRight.setMaximum(0)
  mainUid.progressRight.setValue(0)


def impProgressEnd(mainUid):
  mainUid.pushImport.setEnabled(True)
  mainUid.progressLeft.setMinimum(0)
  mainUid.progressLeft.setMaximum(1)
  mainUid.progressLeft.setValue(0)

  mainUid.progressRight.setMinimum(0)
  mainUid.progressRight.setMaximum(1)
  mainUid.progressRight.setValue(0)





def importAssetsWithImportWidget(mainUid,importUid):
  global projectToImportTo
  originalAssetsColord = getOriginalAsses(projectToImportTo)
  items = mainUid.listWidgetAssets.selectedItems()
  importUid.tableWidget.clear()
  importUid.tableWidget.setRowCount(len(items))
  importUid.tableWidget.setColumnCount(4)
  impAssets = []
  row = 0
  for x in items:
    impAssets.append(str(x.assetPathColor))
    label = QtWidgets.QLabel()
    checkVersion = QtWidgets.QCheckBox()
    checkVersion.setText("import versions")

    checkForce = QtWidgets.QCheckBox()
    checkForce.setText("force")

    # checkAssName = QtWidgets.QCheckBox()
    # checkAssName.setText("disable assName")
    comboBox = QtWidgets.QComboBox()
    comboBox.addItems(originalAssetsColord)
    label.setTextFormat(QtCore.Qt.RichText)
    label.setText(x.assetPathColor)
    label.assetPath = str(x.assetPath)
    importUid.tableWidget.setCellWidget(row,0,label)
    importUid.tableWidget.setCellWidget(row, 1, comboBox)
    importUid.tableWidget.setCellWidget(row, 2, checkVersion)
    importUid.tableWidget.setCellWidget(row, 3, checkForce)
    # importUid.tableWidget.setCellWidget(row, 3, checkAssName)
    importUid.tableWidget.resizeColumnsToContents()
    # header = importUid.tableWidget.horizontalHeader()
    # # header.setResizeMode(0, QtGui.QHeaderView.Stretch)
    # # header.setResizeMode(1, QtGui.QHeaderView.ResizeToContents)
    # header.setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
    row = row + 1
  rbhus.debug.info(impAssets)
  importUid.move(QtWidgets.QApplication.desktop().screen().rect().center() - importUid.rect().center())
  importUid.show()


def importAssets(mainUid):
  items = mainUid.listWidgetAssets.selectedItems()

  impAssets = []
  for x in items:
    impAssets.append(str(x.assetPath))


  assImpThread = importAssQthread(projectToImportTo,impAssets,parent=mainUid)
  assImpThread.impStarted.connect(lambda mainUid=mainUid: impProgressStart(mainUid))
  assImpThread.impFinished.connect(lambda mainUid=mainUid: impProgressEnd(mainUid))
  assImpThread.start()

def importingStart(mainUid, text,textColor,version):
  ui_progress = uic.loadUi(ui_progress_list)
  ui_progress.setParent(mainUid.scrollArea)
  ui_progress.labelAssetName.setTextFormat(QtCore.Qt.RichText)
  ui_progress.labelAssetName.setText(textColor)

  # item = QtWidgets.QListWidgetItem()
  mainUid.verticalLayout_4.addWidget(ui_progress)
  # mainUid.listWidgetProgress.setItemWidget(item, ui_progress)
  ui_progress_list_dict[text] = ui_progress
  vsb = mainUid.scrollArea.verticalScrollBar()
  vsb.setValue(vsb.maximum())


def importingResult(mainUid,ass,toColor,progText):
  if ass in ui_progress_list_dict:
    ui_progress_list_dict[ass].labelStatus.setText(progText)
    ui_progress_list_dict[ass].progressBar.setMinimum(0)
    ui_progress_list_dict[ass].progressBar.setMaximum(1)
    ui_progress_list_dict[ass].progressBar.setValue(1)

def getImportUidAssets(mainUid,importUid):
  rows = importUid.tableWidget.rowCount()
  rbhus.debug.info(rows)
  assetsToImport = []
  for row in range(0,rows):
    assetToImport = {}
    label = importUid.tableWidget.cellWidget(row,0)
    toAsset = str_convert(importUid.tableWidget.cellWidget(row,1).currentText())
    if(importUid.tableWidget.cellWidget(row,2).checkState() == QtCore.Qt.Checked):
      version = True
    else:
      version = False

    if (importUid.tableWidget.cellWidget(row, 3).checkState() == QtCore.Qt.Checked):
      force = True
    else:
      force = False

    assetToImport['assetPath'] = str(label.assetPath)
    assetToImport['assetPathColor'] = str_convert(label.text())
    assetToImport['toAssetPath'] = str(toAsset)
    assetToImport['getVersions'] = version
    assetToImport['force'] = force
    assetsToImport.append(assetToImport)

  if(assetsToImport):
    assImpThread = importAssQthread(projectToImportTo, assetsToImport, parent=mainUid)
    assImpThread.impStarted.connect(lambda mainUid=mainUid: impProgressStart(mainUid))
    assImpThread.impFinished.connect(lambda mainUid=mainUid: impProgressEnd(mainUid))
    assImpThread.impAssetStart.connect(lambda text, textColor,version, mainUid=mainUid: importingStart(mainUid, text,textColor,version))
    assImpThread.impAssetResult.connect(lambda ass, color, text, mainUid=mainUid: importingResult(mainUid, ass, color, text))
    assImpThread.start()

  rbhus.debug.info(assetsToImport)
  importUid.hide()


def comboClear(comboBox):
  rbhus.debug.info("testing clear button shit")
  for i in range(0, comboBox.model().rowCount()):
    if (comboBox.model().item(i).checkState() == QtCore.Qt.Checked):
      comboBox.model().item(i).setCheckState(QtCore.Qt.Unchecked)
      abrush = QtGui.QBrush()
      color = QtGui.QColor()
      color.setAlpha(0)
      abrush.setColor(color)
      comboBox.model().item(i).setForeground(abrush)


def main():
  mainUid = uic.loadUi(ui_main)
  mainUid.listWidgetProj.clear()


  importUid = uic.loadUi(ui_ass_for_import)

  iconRefresh = QtGui.QIcon()
  iconRefresh.addPixmap(QtGui.QPixmap(os.path.join(base_dir,"etc/icons/ic_action_refresh.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
  mainUid.pushRefresh.setIcon(iconRefresh)
  mainUid.pushRefreshFilters.setIcon(iconRefresh)

  dbcon = rbhus.dbPipe.dbPipe()
  projects = dbcon.execute("select projName from proj",dictionary=True)


  icon = QtGui.QIcon()
  icon.addPixmap(QtGui.QPixmap(os.path.join(base_dir,"etc/icons/rbhusPipe.svg")), QtGui.QIcon.Normal, QtGui.QIcon.On)
  mainUid.setWindowIcon(icon)
  importUid.setWindowIcon(icon)
  importUid.setWindowTitle("Import List")



  maxlen = 0
  for x in projects:
    item = QtWidgets.QListWidgetItem()
    item.setText(x['projName'])
    mylen = len(x['projName'])
    if(mylen >= maxlen):
      maxlen = mylen
    mainUid.listWidgetProj.addItem(item)

  mainUid.pushImport.setText("IMPORT TO PROJECT : "+ str(projectToImportTo))
  mainUid.listWidgetProj.itemSelectionChanged.connect(lambda mainUid=mainUid : updateAssets(mainUid))
  mainUid.listWidgetProj.setSortingEnabled(True)
  mainUid.move(QtWidgets.QApplication.desktop().screen().rect().center() - mainUid.rect().center())
  mainUid.showMaximized()
  mainUid.show()

  font = mainUid.listWidgetProj.font()
  mainUid.groupBoxProjects.setMinimumSize(QtCore.QSize(maxlen*font.pointSize(),0))
  mainUid.groupBoxProjects.updateGeometry()
  setStageTypes(mainUid)
  setNodeTypes(mainUid)
  setFileTypes(mainUid)
  setAssTypes(mainUid)
  mainUid.comboSeq.lineEdit().setClearButtonEnabled(True)
  mainUid.comboSeq.lineEdit().setPlaceholderText("default")
  for kids in mainUid.comboSeq.lineEdit().children():
    if(type(kids) == QtWidgets.QToolButton):
      kids.triggered.connect(lambda action, comboBox = mainUid.comboSeq:comboClear(comboBox))


  mainUid.comboScn.lineEdit().setClearButtonEnabled(True)
  mainUid.comboScn.lineEdit().setPlaceholderText("default")
  for kids in mainUid.comboScn.lineEdit().children():
    if(type(kids) == QtWidgets.QToolButton):
      kids.triggered.connect(lambda action, comboBox = mainUid.comboScn:comboClear(comboBox))


  mainUid.comboStage.lineEdit().setClearButtonEnabled(True)
  mainUid.comboStage.lineEdit().setPlaceholderText("default")
  for kids in mainUid.comboStage.lineEdit().children():
    if(type(kids) == QtWidgets.QToolButton):
      kids.triggered.connect(lambda action, comboBox = mainUid.comboStage:comboClear(comboBox))


  mainUid.comboNode.lineEdit().setClearButtonEnabled(True)
  mainUid.comboNode.lineEdit().setPlaceholderText("default")
  for kids in mainUid.comboNode.lineEdit().children():
    if(type(kids) == QtWidgets.QToolButton):
      kids.triggered.connect(lambda action, comboBox = mainUid.comboNode:comboClear(comboBox))


  mainUid.comboFile.lineEdit().setClearButtonEnabled(True)
  mainUid.comboFile.lineEdit().setPlaceholderText("default")
  for kids in mainUid.comboFile.lineEdit().children():
    if(type(kids) == QtWidgets.QToolButton):
      kids.triggered.connect(lambda action, comboBox = mainUid.comboFile:comboClear(comboBox))


  mainUid.comboAssType.lineEdit().setClearButtonEnabled(True)
  mainUid.comboAssType.lineEdit().setPlaceholderText("default")
  for kids in mainUid.comboAssType.lineEdit().children():
    if(type(kids) == QtWidgets.QToolButton):
      kids.triggered.connect(lambda action, comboBox = mainUid.comboAssType:comboClear(comboBox))


  mainUid.comboSeq.editTextChanged.connect(lambda textChanged, mainUid=mainUid: setScene(mainUid))
  mainUid.comboSeq.editTextChanged.connect(lambda textChanged, mainUid=mainUid: updateAssetsSeq(mainUid))
  mainUid.comboStage.editTextChanged.connect(lambda textChanged, mainUid=mainUid: updateAssetsForProjSelect(mainUid))
  mainUid.comboNode.editTextChanged.connect(lambda textChanged, mainUid=mainUid: updateAssetsForProjSelect(mainUid))
  mainUid.comboFile.editTextChanged.connect(lambda textChanged, mainUid=mainUid: updateAssetsForProjSelect(mainUid))
  mainUid.comboScn.editTextChanged.connect(lambda textChanged, mainUid=mainUid: updateAssetsForProjSelect(mainUid))
  mainUid.comboAssType.editTextChanged.connect(lambda textChanged, mainUid=mainUid: updateAssetsForProjSelect(mainUid))
  mainUid.pushRefresh.clicked.connect(lambda clicked, mainUid=mainUid: pushRefresh(mainUid))
  mainUid.pushRefreshFilters.clicked.connect(lambda clicked, mainUid=mainUid: refreshFilter(mainUid))
  mainUid.checkTag.clicked.connect(lambda clicked, mainUid=mainUid: updateAssetsForProjSelect(mainUid))
  mainUid.checkAssName.clicked.connect(lambda clicked, mainUid=mainUid: updateAssetsForProjSelect(mainUid))
  mainUid.checkAssPath.clicked.connect(lambda clicked, mainUid=mainUid: updateAssetsForProjSelect(mainUid))

  mainUid.lineEditSearch.textChanged.connect(lambda textChanged, mainUid=mainUid: updateAssetsForProjSelect(mainUid))
  # mainUid.pushImport.clicked.connect(lambda clicked, mainUid=mainUid: importAssets(mainUid))
  mainUid.pushImport.clicked.connect(lambda clicked,importUid=importUid, mainUid=mainUid: importAssetsWithImportWidget(mainUid,importUid))


  importUid.pushButtonOk.clicked.connect(lambda clicked, importUid=importUid, mainUid=mainUid: getImportUidAssets(mainUid, importUid))

  # mainUid.lineEditSearch.textChanged.connect(lambda clicked, mainUid=mainUid: updateAssetsForProjSelect(mainUid))








if __name__ == '__main__':
  app = QtWidgets.QApplication(sys.argv)
  main()
  os._exit((app.exec_()))