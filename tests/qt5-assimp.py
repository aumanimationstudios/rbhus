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

import time

from PyQt5 import QtWidgets, QtGui, QtCore, uic

projects = []

ui_main = os.path.join(ui_dir,"ui_main.ui")
ui_ass_icon = os.path.join(ui_dir,"ui_ass_icon.ui")



updateAssThreads = None


class updateAssQthread(QtCore.QThread):
  assSignal = QtCore.pyqtSignal(str,str)
  progressSignal = QtCore.pyqtSignal(int,int,int)
  totalAssets = QtCore.pyqtSignal(int)

  def __init__(self,project,parent=None):
    super(updateAssQthread, self).__init__(parent)
    self.projSelected = project
    self.dbcon = rbhus.dbPipe.dbPipe()

  def __del__(self):
    self.dbcon.disconnect()

  def run(self):
      if(self.projSelected):
        print("started thread")
        projWhere = []
        projWhereString = " where "
        for x in self.projSelected:
          projWhere.append("projName = '" + x + "'")
        projWhereString = "where " + " or ".join(projWhere)
        print(projWhereString)

        assesUnsorted = self.dbcon.execute("select * from assets " + projWhereString + " and status = " + str(rbhus.constantsPipe.assetStatusActive), dictionary=True)

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
            #



def updateAssets(mainUid):
  global updateAssThreads
  global project
  mainUid.listWidgetAssets.clear()
  items = mainUid.listWidgetProj.selectedItems()

  project = []
  for x in items:
    project.append(str(x.text()))
  setSequence(mainUid)
  if(updateAssThreads):
    updateAssThreads.assSignal.disconnect()
    updateAssThreads.progressSignal.disconnect()
    updateAssThreads.totalAssets.disconnect()
    updateAssThreads.terminate()
    updateAssThreads.wait()
    del(updateAssThreads)
  updateAssThreads = updateAssQthread(project = project,parent=mainUid)
  updateAssThreads.start()
  updateAssThreads.assSignal.connect(lambda textAss,richAss, mainUid=mainUid: updateAssSlot(mainUid, textAss, richAss))
  updateAssThreads.progressSignal.connect(lambda minLength, maxLength , current, mainUid = mainUid: updateProgressBar(minLength,maxLength,current,mainUid))
  updateAssThreads.totalAssets.connect(lambda total: mainUid.labelTotal.setText(str(total)))



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
  global project
  mainUid.comboSeq.clear()
  seq = {}
  indx =  0
  foundIndx = -1

  for proj in project:
    rows = rbhus.utilsPipe.getSequenceScenes(proj)
    print(rows)
    if(rows):
      for row in rows:
        seq[row['sequenceName']] = 1

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
      #item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
      item.setData(QtCore.Qt.Unchecked, QtCore.Qt.CheckStateRole)
      model.setItem(indx,0,item)
      abrush = QtGui.QBrush()
      color = QtGui.QColor()
      color.setAlpha(0)
      abrush.setColor(color)
      model.item(indx).setForeground(abrush)
      indx = indx + 1
    mainUid.comboSeq.setModel(model)
    mainUid.comboSeq.setEditText("default")
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
    mainUid.comboSeq.setEditText("default")


def setStageTypes(mainUid):
  rows = rbhus.utilsPipe.getStageTypes()
  #defStage = utilsPipe.getDefaults("stageTypes")
  mainUid.comboStage.clear()
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
    mainUid.comboStage.setEditText("default")
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
    mainUid.comboStage.setEditText("default")


def setNodeTypes(mainUid):
  rows = rbhus.utilsPipe.getNodeTypes()
  #defStage = utilsPipe.getDefaults("stageTypes")
  mainUid.comboNode.clear()
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
    mainUid.comboNode.setEditText("default")
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

  for i in range(0, mainUid.comboStage.model().rowCount()):
    if (mainUid.comboNode.model().item(i).checkState() == QtCore.Qt.Checked):
      selectedStages.append(str(mainUid.comboNode.model().item(i).text()))

  # debug.info("EVENT CALLED : "+ str(index.row()))
  if (selectedStages):
    mainUid.comboNode.setEditText(",".join(selectedStages))
  else:
    mainUid.comboNode.setEditText("default")



def setFileTypes(mainUid):
  rows = rbhus.utilsPipe.getFileTypes()
  #defStage = utilsPipe.getDefaults("stageTypes")
  mainUid.comboFile.clear()
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
    mainUid.comboFile.setEditText("default")
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
    mainUid.comboFile.setEditText("default")




def main():

  # projects = dbcon.execute("select projName from proj where projName like '%pipe%'",dictionary=True)
  dbcon = rbhus.dbPipe.dbPipe()
  projects = dbcon.execute("select projName from proj",dictionary=True)
  mainUid = uic.loadUi(ui_main)
  mainUid.listWidgetProj.clear()
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







if __name__ == '__main__':
  app = QtWidgets.QApplication(sys.argv)
  main()
  os._exit((app.exec_()))