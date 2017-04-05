#!/usr/bin/env python2
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys
import os

file_dir = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-1])
base_dir = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2])
ui_dir = os.path.join(base_dir,"rbhusUI","lib","qt5","rbhusPipe_assImporter")
rbhus_lib_dir = os.path.join(base_dir,"rbhus")

sys.path.append(base_dir)
import rbhus.dbPipe
import rbhus.constantsPipe
import rbhus.utilsPipe
import rbhus.debug
import copy

import time

from PyQt5 import QtWidgets, QtGui, QtCore, uic

projects = []

ui_main = os.path.join(ui_dir,"ui_main.ui")
ui_ass_icon = os.path.join(ui_dir,"ui_ass_icon.ui")



updateAssThreads = []


class updateAssQthread(QtCore.QThread):
  assSignal = QtCore.pyqtSignal(str,str)
  progressSignal = QtCore.pyqtSignal(int,int,int)
  totalAssets = QtCore.pyqtSignal(int)

  def __init__(self,project,whereDict,parent=None):
    super(updateAssQthread, self).__init__(parent)
    self.projSelected = project
    self.dbcon = rbhus.dbPipe.dbPipe()
    self.whereDict = whereDict

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
        minLength = 0
        maxLength = 1
        current = 1
        self.totalAssets.emit(0)
        self.progressSignal.emit(minLength, maxLength, current)





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

  if (mainUid.comboStage.currentText() and mainUid.comboStage.currentText() != "default"):
    whereDict['stageType'] = str(mainUid.comboStage.currentText())
  if (mainUid.comboNode.currentText() and mainUid.comboNode.currentText() != "default"):
    whereDict['nodeType'] = str(mainUid.comboNode.currentText())
  if (mainUid.comboSeq.currentText() and mainUid.comboSeq.currentText() != "default"):
    whereDict['sequenceName'] = str(mainUid.comboSeq.currentText())
  if (mainUid.comboScn.currentText() and mainUid.comboScn.currentText() != "default"):
    whereDict['sceneName'] = str(mainUid.comboScn.currentText())
  if (mainUid.comboFile.currentText() and mainUid.comboFile.currentText() != "default"):
    whereDict['fileType'] = str(mainUid.comboFile.currentText())
  if (mainUid.comboAssType.currentText() and mainUid.comboAssType.currentText() != "default"):
    whereDict['assetType'] = str(mainUid.comboAssType.currentText())
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
    print(rows)
    if(rows):
      for row in rows:
        seq[row['sequenceName']] = 1
  print(seq)
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
      selectedStages.append(str(mainUid.comboSeq.model().item(i).text()))

  #debug.info("EVENT CALLED : "+ str(index.row()))
  if(selectedStages):
    mainUid.comboSeq.setEditText(",".join(selectedStages))
  else:
    mainUid.comboSeq.lineEdit().clear()

def updateAssetsSeq(mainUid):
  textSelected = unicode(mainUid.comboSeq.lineEdit().text()).split(",")
  rbhus.debug.info(textSelected)
  # rbhus.debug.info(mainUid.comboSeq.model())
  # rbhus.debug.info(mainUid.comboSeq.model().rowCount())
  #
  # for i in range(0,mainUid.comboSeq.model().rowCount()):
  #   # mainUid.comboSeq.model().item(i).setCheckState(QtCore.Qt.Unchecked)
  #   rbhus.debug.info(mainUid.comboSeq.model().item(i).text())
  #   # if(mainUid.comboSeq.model().item(i).checkState() == QtCore.Qt.Checked):
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
  seqNames = str(mainUid.comboSeq.currentText()).split(",")

  try:
    mainUid.comboScn.view().clicked.disconnect()
  except:
    pass

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
      selectedStages.append(str(mainUid.comboScn.model().item(i).text()))

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
      selectedStages.append(str(mainUid.comboStage.model().item(i).text()))

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
      selectedStages.append(str(mainUid.comboNode.model().item(i).text()))

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
      selectedStages.append(str(mainUid.comboFile.model().item(i).text()))

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


def main():
  mainUid = uic.loadUi(ui_main)
  mainUid.listWidgetProj.clear()

  iconRefresh = QtGui.QIcon()
  iconRefresh.addPixmap(QtGui.QPixmap(os.path.join(base_dir,"etc/icons/ic_action_refresh.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
  mainUid.pushRefresh.setIcon(iconRefresh)
  mainUid.pushRefreshFilters.setIcon(iconRefresh)

  dbcon = rbhus.dbPipe.dbPipe()
  projects = dbcon.execute("select projName from proj",dictionary=True)


  icon = QtGui.QIcon()
  icon.addPixmap(QtGui.QPixmap(os.path.join(base_dir,"etc/icons/rbhusPipe.svg")), QtGui.QIcon.Normal, QtGui.QIcon.On)
  mainUid.setWindowIcon(icon)



  maxlen = 0
  for x in projects:
    item = QtWidgets.QListWidgetItem()
    item.setText(x['projName'])
    mylen = len(x['projName'])
    if(mylen >= maxlen):
      maxlen = mylen
    mainUid.listWidgetProj.addItem(item)

  mainUid.listWidgetProj.itemSelectionChanged.connect(lambda mainUid=mainUid : updateAssets(mainUid))
  mainUid.listWidgetProj.setSortingEnabled(True)
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
  mainUid.comboScn.lineEdit().setClearButtonEnabled(True)
  mainUid.comboScn.lineEdit().setPlaceholderText("default")
  mainUid.comboStage.lineEdit().setClearButtonEnabled(True)
  mainUid.comboStage.lineEdit().setPlaceholderText("default")
  mainUid.comboNode.lineEdit().setClearButtonEnabled(True)
  mainUid.comboNode.lineEdit().setPlaceholderText("default")
  mainUid.comboFile.lineEdit().setClearButtonEnabled(True)
  mainUid.comboFile.lineEdit().setPlaceholderText("default")
  mainUid.comboAssType.lineEdit().setClearButtonEnabled(True)
  mainUid.comboAssType.lineEdit().setPlaceholderText("default")

  mainUid.comboSeq.editTextChanged.connect(lambda textChanged, mainUid=mainUid: setScene(mainUid))
  mainUid.comboSeq.editTextChanged.connect(lambda textChanged, mainUid=mainUid: updateAssetsSeq(mainUid))
  mainUid.comboStage.editTextChanged.connect(lambda textChanged, mainUid=mainUid: updateAssetsForProjSelect(mainUid))
  mainUid.comboNode.editTextChanged.connect(lambda textChanged, mainUid=mainUid: updateAssetsForProjSelect(mainUid))
  mainUid.comboFile.editTextChanged.connect(lambda textChanged, mainUid=mainUid: updateAssetsForProjSelect(mainUid))
  mainUid.comboScn.editTextChanged.connect(lambda textChanged, mainUid=mainUid: updateAssetsForProjSelect(mainUid))
  mainUid.comboAssType.editTextChanged.connect(lambda textChanged, mainUid=mainUid: updateAssetsForProjSelect(mainUid))
  mainUid.pushRefresh.clicked.connect(lambda clicked,mainUid = mainUid: pushRefresh(mainUid))
  mainUid.pushRefreshFilters.clicked.connect(lambda clicked, mainUid=mainUid: refreshFilter(mainUid))







if __name__ == '__main__':
  app = QtWidgets.QApplication(sys.argv)
  main()
  os._exit((app.exec_()))