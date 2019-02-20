#!/usr/bin/env python2
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys
import os
import subprocess
import tempfile
import simplejson
import copy
import yaml

tempDir = tempfile.gettempdir()
file_dir = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-1])
base_dir = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-3])
ui_dir = os.path.join(base_dir,"rbhusUI","lib","qt5","rbhusPipe_trak")
rbhus_lib_dir = os.path.join(base_dir,"rbhus")
custom_widget_dir = os.path.join(base_dir,"rbhusUI","lib","qt5","customWidgets")
home_dir = os.path.expanduser("~")
print(custom_widget_dir)

sys.path.append(base_dir)

import rbhus.dbPipe
import rbhus.constantsPipe
import rbhus.utilsPipe
import rbhus.debug
import rbhusUI.lib.qt5.customWidgets.checkBox_style
import rbhus.pyperclip
import rbhus.hgmod
import time
import zmq
from PyQt5 import QtWidgets, QtGui, QtCore, uic

projects = ["pipeTest1"]

ui_main = os.path.join(ui_dir,"ui_main.ui")
ui_asset_details = os.path.join(ui_dir,"assetDetailRow_new.ui")
ui_asset_media_list = os.path.join(ui_dir,"assetMediaList.ui")
ui_asset_media_Thumbz = os.path.join(ui_dir,"mediaThumbz.ui")

rpA = "rbhusPipeProjCreate.py"
rpAss = "rbhusPipeAssetCreate.py"
rpAssEdit = "rbhusPipeAssetEdit.py"
srb = "selectRadioBox.py"
rpS = "rbhusPipeSeqSceCreate.py"
rpSC = "rbhusPipeSeqSceEdit.py"
fileSelect = "fileSelectUI.py"
scb = "selectCheckBox.py"
vc = "rbhusPipeVersions.py"
rS = "rbhusPipeRenderSubmit.py"
rR = "rbhusPipeReview.py"
rN = "rbhusPipeNotes.py"
rNr = "rbhusPipeNotes_readonly.py"

assFolds = "qt5-treeview.py"
assImporter = "rbhusAssetImport.py"


autoLineUpCmd = os.path.join(base_dir,"tools","rbhus","autoLineUp","autoLineUp_anim.py")

selectCheckBoxCmd = os.path.join(file_dir, scb)
rbhusPipeProjCreateCmd = os.path.join(file_dir, rpA)
rbhusPipeAssetCreateCmd = os.path.join(file_dir, rpAss)
rbhusPipeAssetEditCmd = os.path.join(file_dir, rpAssEdit)
rbhusPipeSeqSceCreateCmd = os.path.join(file_dir, rpS)
rbhusPipeSeqSceEditCmd = os.path.join(file_dir, rpSC)
fileSelectCmd = os.path.join(file_dir, fileSelect)
versionCmd = os.path.join(file_dir, vc)
rbhusPipeRenderSubmitCmd = os.path.join(file_dir, rS)
rbhusPipeReviewCmd = os.path.join(file_dir, rR)
rbhusPipeNotesCmd = os.path.join(file_dir, rN)
rbhusPipeNotesReadonlyCmd = os.path.join(file_dir, rNr)
rbhusPipeAssetImportCmd = os.path.join(file_dir, assImporter)
selectRadioBoxCmd = os.path.join(file_dir, srb)
assFoldsCmd = os.path.join(file_dir,assFolds)
print(assFoldsCmd)
updateAssThreads = []
updateAssThreadsFav = []
# assDetsItems = []
assDetsItemsDict = {}
ImageWidgets = []
assDetsWidgetsDict = {}
mediaWidgets = {}
updateDetailsThreads = []
updateDetailsPanelMediaThreads = []
tableRowCount = 0


assColumnList = ['','','asset','assigned','reviewer','modified','v','review','publish','']

try:
  username = os.environ['rbhusPipe_acl_user'].rstrip().lstrip()
except:
  pass

favLock = QtCore.QMutex()
updateAssTimer = QtCore.QTimer()
updateAssFavTimer = QtCore.QTimer()
updateSortingTimer = QtCore.QTimer()
# updateMediaTabTimer = QtCore.QTimer()




class assetDetailRowClass(QtWidgets.QWidget):
  def __init__(self,parent=None):
    super(assetDetailRowClass, self).__init__(parent)
    uic.loadUi(ui_asset_details,baseinstance=self)


class QTableWidgetItemSort(QtWidgets.QTableWidgetItem):


  def __lt__(self, other):
    return self.data(QtCore.Qt.UserRole) < other.data(QtCore.Qt.UserRole)

  def __ge__(self, other):
    return self.data(QtCore.Qt.UserRole) > other.data(QtCore.Qt.UserRole)


class QListWidgetItemSort(QtWidgets.QListWidgetItem):


  def __lt__(self, other):
    return self.data(QtCore.Qt.UserRole) < other.data(QtCore.Qt.UserRole)

  def __ge__(self, other):
    return self.data(QtCore.Qt.UserRole) > other.data(QtCore.Qt.UserRole)



class ImageWidget(QtWidgets.QPushButton):
  def __init__(self, imagePath, imageSize, parent=None):
    super(ImageWidget, self).__init__(parent)
    self.imagePath = imagePath
    self.picture = QtGui.QPixmap(imagePath)
    # rbhus.debug.debug(self.imagePath)
    self.picture  = self.picture.scaledToHeight(imageSize,0)

  def paintEvent(self, event):
    painter = QtGui.QPainter(self)
    painter.setPen(QtCore.Qt.NoPen)
    painter.drawPixmap(0, 0, self.picture)

  def sizeHint(self):
    return(self.picture.size())



class updateAssQthread(QtCore.QThread):
  assSignal = QtCore.pyqtSignal(str,object,int)
  progressSignal = QtCore.pyqtSignal(int,int,int)
  totalAssets = QtCore.pyqtSignal(int)

  def __init__(self,project,whereDict,parent=None,isFav=False):
    super(updateAssQthread, self).__init__(parent)
    self.projSelected = copy.copy(project)
    self.dbcon = rbhus.dbPipe.dbPipe()
    self.whereDict = whereDict
    self.pleaseStop = False
    self.isFav = isFav

  def exitshit(self):
    self.pleaseStop = True

  def run(self):
    if(self.projSelected):
      rbhus.debug.debug("started thread")
      projWhere = []
      projWhereString = " where "
      assesUnsorted = []
      isGentoo = os.path.exists("/etc/gentoo-release")

      if(self.isFav):
        for x in self.projSelected:
          assesForProj = getAllFavorite(x)
          if (assesForProj):
            for ass in assesForProj:
              assdets = rbhus.utilsPipe.getAssDetails(assPath=ass)
              assesUnsorted.append(assdets)
      else:
        for x in self.projSelected:
          assesForProj = rbhus.utilsPipe.getProjAsses(x,whereDict=self.whereDict)
          if(assesForProj):
            assesUnsorted.extend(assesForProj)

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
            x['seqScnDets'] = None
            if((x['sequenceName'] != "default") and (x['sceneName'] != "default")):
              sqsc = rbhus.utilsPipe.getSequenceScenes(x['projName'],seq=x['sequenceName'],sce=x['sceneName'])
              if(sqsc):
                x['seqScnDets'] = sqsc[0]

            textAssArr = []
            if(len(self.projSelected) > 1):
              for fc in asset.split(":"):
                textAssArr.append('<font color="' + fc.split("#")[1] + '">' + fc.split("#")[0] + '</font>')
            else:
              for fc in asset.split(":")[1:]:
                textAssArr.append('<font color="' + fc.split("#")[1] + '">' + fc.split("#")[0] + '</font>')

            richAss = " " + "<b><i> : </i></b>".join(textAssArr)
            x['richAss'] = richAss
            textAss = x['path']
            absPathAss = rbhus.utilsPipe.getAbsPath(x['path'])
            notes = rbhus.utilsPipe.notesDetails(x['assetId'])
            if(notes):
              x['isNotes'] = True
            else:
              x['isNotes'] = False

            x['fav']  = isFavorite(x['path'])
            x['absPath'] = absPathAss
            try:
              x['modified'] = os.path.getmtime(absPathAss)
            except:
              x['modified'] = None

            x['preview_low'] = os.path.join(absPathAss,'preview_low.png')
            x['preview'] = os.path.join(absPathAss, 'preview.png')
            if(not os.path.exists(x['preview_low'])):
              x['preview_low'] = None



            self.assSignal.emit(richAss,x,current-1)
            self.progressSignal.emit(minLength,maxLength,current)
            if(isGentoo):
              time.sleep(0.01)
            else:
              time.sleep(0.05)
          else:
            rbhus.debug.debug("STOPPING THREAD")
            break
      else:
        minLength = 0
        maxLength = 1
        current = 1
        self.totalAssets.emit(0)
        self.progressSignal.emit(minLength, maxLength, current)
    rbhus.debug.debug("thread stopped")
    # self.finished.emit()


def updateFavorite(mainUid,assPath,starObj):
  proj = assPath.split(":")[0]

  fav_file = os.path.join(home_dir,".rbhusPipe__"+ str(proj) +".fav")
  fav_asses = []
  favLock.lock()
  if(os.path.exists(fav_file)):
    fd = open(fav_file,"r")
    try:
      fav_asses = simplejson.load(fd)
    except:
      rbhus.debug.error(sys.exc_info())
    fd.close()
  if(not starObj.isChecked()):
    if(assPath in fav_asses):
      try:
        fav_asses.remove(assPath)
      except:
        rbhus.debug.error(sys.exc_info())
    else:
      favLock.unlock()
      return
  else:
    if(assPath not in fav_asses):
      fav_asses.append(assPath)
    else:
      favLock.unlock()
      return
  fd = open(fav_file,"w")
  try:
    simplejson.dump(fav_asses,fd)
  except:
    rbhus.debug.error(sys.exc_info())
  fd.flush()
  fd.close()
  favLock.unlock()
  # updateAssetsForProjSelectFav(mainUid)


def isFavorite(assPath):
  proj = assPath.split(":")[0]
  fav_file = os.path.join(home_dir, ".rbhusPipe__" + str(proj) + ".fav")
  fav_asses = []
  if (os.path.exists(fav_file)):
    favLock.lock()
    fd = open(fav_file, "r")
    try:
      fav_asses = simplejson.load(fd)
    except:
      rbhus.debug.warning(sys.exc_info())
    fd.close()
    favLock.unlock()
    if(assPath in fav_asses):
      return True
    else:
      return False
  else:
    return False


def getAllFavorite(proj):
  fav_file = os.path.join(home_dir, ".rbhusPipe__" + str(proj) + ".fav")
  fav_asses = []
  if (os.path.exists(fav_file)):
    favLock.lock()
    fd = open(fav_file, "r")
    try:
      fav_asses = simplejson.load(fd)
    except:
      rbhus.debug.warning(sys.exc_info())
    fd.close()
    favLock.unlock()
  return fav_asses


def changeProject(mainUid):

  updateProjSelect(mainUid)
  setSequence(mainUid)
  updateAssetsForProjSelect(mainUid)
  # updateAssetsForProjSelectFav(mainUid)


def pushRefresh(mainUid):
  # updateProjSelect(mainUid)
  updateAssetsForProjSelect(mainUid)



def updateProjSelect(mainUid):
  global projects
  items = mainUid.listWidgetProj.selectedItems()

  projects = []
  for x in items:
    projects.append(str(x.text()))
  saveSelectedProjects(projects)
  try:
    rbhus.utilsPipe.exportProj(projects[-1])
  except:
    rbhus.debug.warning("no project to export .. new user")

def clearProjSelect(mainUid):
  global projects
  items = mainUid.listWidgetProj.selectedItems()
  projects = []
  for x in items:
    projects.append(str(x.text()))
  saveSelectedProjects(projects)
  rbhus.utilsPipe.exportProj(projects[-1])





def updateAssetsForProjSelect(mainUid):
  updateAssTimer.stop()
  updateAssTimer.setSingleShot(True)
  updateAssTimer.start(1000)


def updateAssetsForProjSelectTimed(mainUid):
  # updateAssTimer.stop()
  global updateAssThreads
  global projects
  whereDict = {}

  if (mainUid.comboStage.currentText()):
    whereDict['stageType'] = str(mainUid.comboStage.currentText())
  if (mainUid.comboNode.currentText()):
    whereDict['nodeType'] = str(mainUid.comboNode.currentText())
  if (mainUid.comboSeq.currentText()):
    whereDict['sequenceName'] = str(mainUid.comboSeq.currentText())
  if (mainUid.comboScn.currentText()):
    whereDict['sceneName'] = str(mainUid.comboScn.currentText())
  if (mainUid.comboFile.currentText()):
    whereDict['fileType'] = str(mainUid.comboFile.currentText())
  if (mainUid.comboAssType.currentText()):
    whereDict['assetType'] = str(mainUid.comboAssType.currentText())
  # if (mainUid.comboAssType.currentText() and mainUid.comboAssType.currentText() != "default"):
  #   whereDict['assetType'] = str(mainUid.comboAssType.currentText())



  if (str(mainUid.lineEditSearch.text())):
    if (mainUid.checkUsers.isChecked()):
      whereDict['assignedWorker'] = str(mainUid.lineEditSearch.text())
    if (mainUid.checkTag.isChecked()):
      whereDict['tags'] = str(mainUid.lineEditSearch.text())
    if (mainUid.checkAssName.isChecked()):
      whereDict['assName'] = str(mainUid.lineEditSearch.text())
    if (mainUid.checkAssPath.isChecked()):
      whereDict['path'] = str(mainUid.lineEditSearch.text())
  else:
    if(mainUid.radioMineAss.isChecked()):
      whereDict['assignedWorker'] = username

  rbhus.debug.debug(whereDict)

  if(updateAssThreads):
    for runingThread in updateAssThreads:
      runingThread.exitshit()
      runingThread.wait()
      try:
        runingThread.disconnect()
      except:
        rbhus.debug.debug(runingThread)
      try:
        runingThread.deleteLater()
      except:
        rbhus.debug.debug(sys.exc_info())
      updateAssThreads.remove(runingThread)

  updateAssThread = updateAssQthread(project = projects,whereDict=whereDict,parent=mainUid,isFav=False)
  updateAssThread.totalAssets.connect(lambda total,mainUid=mainUid: updateTotalAss(mainUid,total))
  updateAssThread.progressSignal.connect(lambda minLength, maxLength , current, mainUid = mainUid: updateProgressBar(minLength,maxLength,current,mainUid))
  updateAssThread.assSignal.connect(lambda richAss,assetDets, current, mainUid=mainUid: updateAssSlot(mainUid, richAss, assetDets))
  updateAssThread.finished.connect(lambda mainUid=mainUid: updateAssFinished(mainUid))
  updateAssThread.start()
  updateAssThreads.append(updateAssThread)



def updateProgressBar(minLength,maxLength,current,mainUid):
  mainUid.progressBar.setMinimum(minLength)
  mainUid.progressBar.setMaximum(maxLength)
  mainUid.progressBar.setValue(current)


def updateAssFinished(mainUid):
  rbhus.debug.debug("calling updateFinished")
  mainUid.tableWidgetAssets.update()
  mainUid.tableWidgetAssets.resizeColumnsToContents()
  updateSorting(mainUid)


def updateSorting(mainUid):
  updateSortingTimer.stop()
  updateSortingTimer.setSingleShot(True)
  updateSortingTimer.start(100)






def updateTotalAss(mainUid,totalRows):
  global assDetsItemsDict
  global ImageWidgets
  global assDetsWidgetsDict
  global tableRowCount
  tableRowCount = 0
  mainUid.labelTotal.setText(str(totalRows))
  mainUid.tableWidgetAssets.clearContents()




def updateAssSlot(mainUid, richAss, assetDets):
  global ImageWidgets
  global assDetsWidgetsDict
  global assDetsItemsDict
  global tableRowCount


  mainUid.tableWidgetAssets.setRowCount(tableRowCount+1)
  assetLabel = QtWidgets.QLabel()
  assetPathItem = QTableWidgetItemSort()
  assetPathItem.setData(QtCore.Qt.UserRole,assetDets['path'])
  assetLabel.setTextFormat(QtCore.Qt.RichText)
  assetLabel.setText(richAss)
  mainUid.tableWidgetAssets.setCellWidget(tableRowCount,0,assetLabel)
  mainUid.tableWidgetAssets.setItem(tableRowCount,0,assetPathItem)

  if(assetDets['seqScnDets']):
    descItem = QTableWidgetItemSort()
    descItem.setText(assetDets['seqScnDets']['description'])
    descItem.setData(QtCore.Qt.UserRole,assetDets['seqScnDets']['description'])
    mainUid.tableWidgetAssets.setItem(tableRowCount, 1, descItem)



  tableRowCount = tableRowCount + 1
  mainUid.tableWidgetAssets.resizeColumnsToContents()
  # rbhus.debug.info("asset : "+ assetDets['path'])





def eatEvents(e):
  # print(dir(e))
  e.ignore()
  rbhus.debug.info("dropping : "+ str(e) +" : "+ str(e.source()))


def imageWidgetClicked(imagePath,mimeType=None):
  cmdFull = None
  if(mimeType):
    if(mimeType != "blender"):
      cmdFull = "xdg-open \"" + imagePath + "\""
  else:
    cmdFull = "xdg-open \"" + imagePath + "\""
  if(cmdFull):
    subprocess.Popen(cmdFull, shell=True)





def selectedAsses(mainUid,isFav=False):
  items = mainUid.tableWidgetAssets.selectedItems()
  rowstask = []
  for x in items:
    rowstask.append(x.assetDets)
  return(rowstask)


def setSequence(mainUid):
  global projects
  try:
    mainUid.comboSeq.view().clicked.disconnect()
  except:
    pass
  mainUid.comboSeq.clear()
  mainUid.comboSeq.model().clear()
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
      selectedStages.append(str(mainUid.comboSeq.model().item(i).text()))

  if(selectedStages):
    mainUid.comboSeq.setEditText(",".join(selectedStages))
  else:
    mainUid.comboSeq.lineEdit().clear()

def updateAssetsSeq(mainUid):
  # textSelected = mainUid.comboSeq.lineEdit().text().split(",")
  # rbhus.debug.debug(textSelected)
  updateAssetsForProjSelect(mainUid)


def setScene(mainUid):
  global projects
  try:
    mainUid.comboScn.view().clicked.disconnect()
  except:
    pass
  mainUid.comboScn.clear()
  mainUid.comboScn.model().clear()
  if(not projects):
    return
  seqNames = str(mainUid.comboSeq.currentText()).split(",")



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
  try:
    mainUid.comboStage.view().clicked.disconnect()
  except:
    pass
  #defStage = utilsPipe.getDefaults("stageTypes")
  mainUid.comboStage.clear()
  mainUid.comboStage.model().clear()
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
  try:
    mainUid.comboNode.view().clicked.disconnect()
  except:
    pass
  #defStage = utilsPipe.getDefaults("stageTypes")
  mainUid.comboNode.clear()
  mainUid.comboNode.model().clear()
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
  try:
    mainUid.comboFile.view().clicked.disconnect()
  except:
    pass
  #defStage = utilsPipe.getDefaults("stageTypes")
  mainUid.comboFile.clear()
  mainUid.comboFile.model().clear()
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
  try:
    mainUid.comboAssType.view().clicked.disconnect()
  except:
    pass
  mainUid.comboAssType.clear()
  mainUid.comboAssType.model().clear()
  indx = 0
  model = QtGui.QStandardItemModel(len(rows), 1)
  if (rows):
    for row in rows:
      item = QtGui.QStandardItem(row['type'])
      item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
      item.setData(QtCore.Qt.Unchecked, QtCore.Qt.CheckStateRole)
      model.setItem(indx, 0, item)
      abrush = QtGui.QBrush()
      color = QtGui.QColor()
      color.setAlpha(0)
      abrush.setColor(color)
      model.item(indx).setForeground(abrush)
      indx = indx + 1

    mainUid.comboAssType.setModel(model)
    mainUid.comboAssType.lineEdit().clear()
    mainUid.comboAssType.view().clicked.connect(lambda modelIndex, mainUid=mainUid: itemChangedAssType(modelIndex, mainUid))
    return (1)
  return (0)
  # indx = 0
  # foundIndx = -1
  # if(rows):
  #   for row in rows:
  #     mainUid.comboAssType.addItem(row['type'])
  #     indx = indx + 1
  #   mainUid.comboAssType.lineEdit().clear()
  #   return(1)
  # return(0)
  #


def itemChangedAssType(modelIndex, mainUid):
  item = mainUid.comboAssType.model().itemFromIndex(modelIndex)
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

  for i in range(0, mainUid.comboAssType.model().rowCount()):
    if (mainUid.comboAssType.model().item(i).checkState() == QtCore.Qt.Checked):
      selectedStages.append(str(mainUid.comboAssType.model().item(i).text()))

  # debug.info("EVENT CALLED : "+ str(index.row()))
  if (selectedStages):
    mainUid.comboAssType.setEditText(",".join(selectedStages))
  else:
    mainUid.comboAssType.lineEdit().clear()

def refreshFilter(mainUid):

  setStageTypes(mainUid)
  setNodeTypes(mainUid)
  setFileTypes(mainUid)
  setAssTypes(mainUid)
  setSequence(mainUid)
  setScene(mainUid)




def comboClear(comboBox):
  for i in range(0, comboBox.model().rowCount()):
    if (comboBox.model().item(i).checkState() == QtCore.Qt.Checked):
      comboBox.model().item(i).setCheckState(QtCore.Qt.Unchecked)
      abrush = QtGui.QBrush()
      color = QtGui.QColor()
      color.setAlpha(0)
      abrush.setColor(color)
      comboBox.model().item(i).setForeground(abrush)

def messageBoxDelete(hard=False):
  msgbox = QtWidgets.QMessageBox()
  if(hard == True):
    delmsg = "DELETE (database and disk)?!?!?!"
  else:
    delmsg = "DELETE (database only)?!?!?!"
  msgbox.setText(delmsg +"\nDo you want to really delete this asset?!")
  msgbox.setIconPixmap(QtGui.QPixmap(os.path.join(base_dir, "etc", "icons", "danger_128.png")))
  #noBut = QtGui.QPushButton("cancel")
  #yesBut = QtGui.QPushButton("yes")
  yesBut = msgbox.addButton("yes",QtWidgets.QMessageBox.YesRole)
  noBut = msgbox.addButton("cancel",QtWidgets.QMessageBox.NoRole)
  msgbox.setDefaultButton(noBut)
  msgbox.exec_()
  if(msgbox.clickedButton() == yesBut):
    return(1)
  else:
    return(0)

def messageBoxTemplateHard():
  msgbox = QtWidgets.QMessageBox()
  delmsg = "Replace the current asset file from template??!!!"
  msgbox.setWindowTitle("WTF!!!")
  msgbox.setText(delmsg + "\nYour time and effort used on this asset WILL be WASTED!!!!")
  msgbox.setIconPixmap(QtGui.QPixmap(os.path.join(base_dir,"etc","icons","danger_128.png")))
  # noBut = QtGui.QPushButton("cancel")
  # yesBut = QtGui.QPushButton("yes")
  yesBut = msgbox.addButton("yes", QtWidgets.QMessageBox.YesRole)
  noBut = msgbox.addButton("cancel", QtWidgets.QMessageBox.NoRole)
  msgbox.setDefaultButton(noBut)
  msgbox.exec_()
  if (msgbox.clickedButton() == yesBut):
    return (1)
  else:
    return (0)



def notesAss(mainUid,assetList=None):
  # rbhus.debug.info(assetList)
  # if(assetList):
  #   listAsses = assetList
  if(isinstance(assetList,str)):
    assPath = assetList
    listAsses = [assetList]
  else:
    listAsses = [assetList[0]['path']]
    assPath = assetList[0]['path']
  rbhusPipeNotesCmdFinal = rbhusPipeNotesCmd + " --assetpath "+ assPath
  p = QtCore.QProcess(parent=mainUid)
  p.setStandardOutputFile(tempDir + os.sep + "rbhusPipeNotes_" + username + ".log")
  p.setStandardErrorFile(tempDir + os.sep + "rbhusPipeNotes_" + username + ".err")
  p.start(sys.executable, rbhusPipeNotesCmdFinal.split())
  p.finished.connect(lambda a, b, mainUid=mainUid, assList=listAsses: updateAssetDetails(mainUid, assList))

  # if(sys.platform.find("win") >= 0):
  #   subprocess.Popen([rbhusPipeNotesCmd,"--assetpath",assPath],shell = True)
  # elif(sys.platform.find("linux") >= 0):
  #   subprocess.Popen(rbhusPipeNotesCmd +" --assetpath "+ assPath,shell = True)



def notesAssRO(mainUid,assetList=None):
  # rbhus.debug.info(assetList)
  # if(assetList):
  #   listAsses = assetList
  if(isinstance(assetList,str)):
    assPath = assetList
    listAsses = [assetList]
  else:
    listAsses = [assetList[0]['path']]
    assPath = assetList[0]['path']
  rbhusPipeNotesCmdFinal = rbhusPipeNotesReadonlyCmd + " --assetpath "+ assPath
  p = QtCore.QProcess(parent=mainUid)
  p.setStandardOutputFile(tempDir + os.sep + "rbhusPipeNotesRO_" + username + ".log")
  p.setStandardErrorFile(tempDir + os.sep + "rbhusPipeNotesRO_" + username + ".err")
  p.start(sys.executable, rbhusPipeNotesCmdFinal.split())
  p.waitForFinished()






def setUsers(mainUid):
  users = rbhus.utilsPipe.getUsers()
  outUsers = subprocess.Popen([sys.executable,selectRadioBoxCmd,"-i",",".join(users),"-d",str(mainUid.lineEditSearch.text()).rstrip().lstrip()],stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].rstrip().lstrip()
  # if(outUsers == ""):
  #   outUsers = str(self.lineEditSearch.text()).rstrip().lstrip()
  mainUid.lineEditSearch.setText(outUsers)



def saveSearchItem(mainUid,filterFile=None,noUi = False):
  assetTypeSave = str(mainUid.comboAssType.currentText())
  seqSave = str(mainUid.comboSeq.currentText())
  scnSave = str(mainUid.comboScn.currentText())
  stageSave = str(mainUid.comboStage.currentText())
  nodeSave = str(mainUid.comboNode.currentText())
  fileTypeSave = str(mainUid.comboFile.currentText())
  isMineAssignedSave = str(mainUid.radioMineAss.isChecked())
  isAllSave = str(mainUid.radioAllAss.isChecked())
  isTagsSave = str(mainUid.checkTag.isChecked())
  isUsersSave = str(mainUid.checkUsers.isChecked())
  searchBoxSave = str(mainUid.lineEditSearch.text())
  isAssetNameSave = str(mainUid.checkAssName.isChecked())
  isAssetPathSave = str(mainUid.checkAssPath.isChecked())
  isStarred = str(False)
  saveString = assetTypeSave +"###"+ \
               seqSave +"###"+ \
               scnSave +"###"+ \
               stageSave +"###"+ \
               nodeSave +"###"+ \
               fileTypeSave +"###"+ \
               isMineAssignedSave +"###"+ \
               isAllSave +"###"+ \
               isTagsSave +"###"+ \
               isUsersSave +"###"+ \
               searchBoxSave +"###"+ \
               isAssetNameSave +"###"+ \
               isStarred +"###"+ \
               isAssetPathSave


  isSaveStringPresent = searchItemPresent(saveString,filterFile=filterFile)

  if(not noUi):
    if(not isSaveStringPresent):
      saveDict = {saveString:'name this'}
      searchItemSave(saveDict,filterFile=filterFile)
      item = QtWidgets.QListWidgetItem()
      item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled)
      item.setText(saveDict[saveString])
      item.assFilter = saveString
      mainUid.listWidgetSearch.addItem(item)

  testDict = searchItemLoad(filterFile=filterFile)
  rbhus.debug.debug(testDict)

def searchItemPresent(assFilter,filterFile=None):
  savedDict = searchItemLoad(filterFile=filterFile)
  if(savedDict):
    for x in savedDict:
      if(x):
        if(x.has_key(assFilter)):
          return(True)
  return(False)

def searchItemLoad(filterFile=None):
  searchItems = None
  if (filterFile):
    filterFile = os.path.abspath(filterFile)
  else:
    filterFile = os.path.join(home_dir, ".rbhusPipe.filters")
  # filterFile = os.path.join(home_dir,".rbhusPipe.filters")
  if(os.path.exists(filterFile)):
    fd = open(filterFile,"r")
    searchItems = yaml.safe_load(fd)
    fd.close()
  return (searchItems)



def loadSearch(mainUid):
  mainUid.listWidgetSearch.clear()
  saveSearchArray = searchItemLoad()
  if(saveSearchArray):
    for x in saveSearchArray:
      item = QtWidgets.QListWidgetItem()
      item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsEnabled)
      item.setText(x[x.keys()[-1]])
      item.assFilter = x.keys()[-1]
      mainUid.listWidgetSearch.addItem(item)


def searchItemSave(itemDict,filterFile=None):
  searchItems = []
  if(filterFile):
    filterFile = os.path.abspath(filterFile)
  else:
    filterFile = os.path.join(home_dir,".rbhusPipe.filters")
  if(os.path.exists(filterFile)):
    fd = open(filterFile,"r")
    searchItems = yaml.safe_load(fd)
    fd.close()
    searchItems.append(itemDict)
  else:
    searchItems.append(itemDict)
  if(searchItems):
    fd = open(filterFile,"w")
    yaml.dump(searchItems,fd)
    fd.flush()
    fd.close()


  return (searchItems)




def searchItemChanged(mainUid,item):
  rbhus.debug.debug(item.text())
  rbhus.debug.debug(item.assFilter)
  filterFile = os.path.join(home_dir, ".rbhusPipe.filters")

  savedDict = searchItemLoad()
  for x in savedDict:
    if(x):
      if(x.has_key(item.assFilter)):
        x[item.assFilter] = str(item.text())
  rbhus.debug.debug(savedDict)
  fd = open(filterFile,"w")
  yaml.dump(savedDict,fd)
  fd.flush()
  fd.close()


def popUpSearchFav(mainUid,pos):
  menu = QtWidgets.QMenu()
  filterSearchAction = menu.addAction("filter")
  waste1 = menu.addAction("")
  waste2 = menu.addAction("")
  deleteSearchAction = menu.addAction("delete")
  action = menu.exec_(mainUid.listWidgetSearch.mapToGlobal(pos))

  if(action == filterSearchAction):
    searchItemActivate(mainUid)

  if(action == deleteSearchAction):
    deleteSearch(mainUid)


def deleteSearch(mainUid):
  item = mainUid.listWidgetSearch.currentItem()
  savedFilter = searchItemLoad()
  rbhus.debug.debug(item.assFilter)
  index  = 0
  indexToDelete = None
  for x in savedFilter:
    if(x):
      if(x.has_key(item.assFilter)):
        indexToDelete = index
    index = index + 1
  del savedFilter[indexToDelete]
  filterFile = os.path.join(home_dir, ".rbhusPipe.filters")
  fd = open(filterFile, "w")
  yaml.dump(savedFilter, fd)
  fd.flush()
  fd.close()
  loadSearch(mainUid)




def searchItemActivate(mainUid):
  indexChanged = mainUid.listWidgetSearch.currentRow()
  savedFilter = searchItemLoad()
  s = savedFilter[indexChanged].keys()[-1].split("###")
  mainUid.comboAssType.setEditText(s[0])
  mainUid.comboSeq.setEditText(s[1])
  mainUid.comboScn.setEditText(s[2])
  mainUid.comboStage.setEditText(s[3])
  mainUid.comboNode.setEditText(s[4])
  mainUid.comboFile.setEditText(s[5])


  if(s[6] == "True"):
    mainUid.radioMineAss.setChecked(True)
  else:
    mainUid.radioMineAss.setChecked(False)

  if(s[7] == "True"):
    mainUid.radioAllAss.setChecked(True)
  else:
    mainUid.radioAllAss.setChecked(False)


  if(s[8] == "True"):
    mainUid.checkTag.setChecked(True)
  else:
    mainUid.checkTag.setChecked(False)

  if(s[9] == "True"):
    mainUid.checkUsers.setChecked(True)
  else:
    mainUid.checkUsers.setChecked(False)

  mainUid.lineEditSearch.setText(s[10])

  if(s[11] == "True"):
    mainUid.checkAssName.setChecked(True)
  else:
    mainUid.checkAssName.setChecked(False)

  if(s[12] == "True"):
    pass
  else:
    pass



  if(s[13] == "True"):
    mainUid.checkAssPath.setChecked(True)
  else:
    mainUid.checkAssPath.setChecked(False)
  updateAssetsForProjSelect(mainUid)




def closeEvent(event):
    rbhus.debug.debug("QUITTING")
    event.accept()


def main_func(mainUid):
  # mainUid.listWidgetProj.clear()

  # mainUid.tableLogs.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignLeft)

  icon = QtGui.QIcon()
  icon.addPixmap(QtGui.QPixmap(os.path.join(base_dir, "etc/icons/rbhusPipe.svg")), QtGui.QIcon.Normal, QtGui.QIcon.On)
  mainUid.setWindowIcon(icon)


  iconRefresh = QtGui.QIcon()
  iconRefresh.addPixmap(QtGui.QPixmap(os.path.join(base_dir,"etc/icons/ic_loop_black_48dp_2x.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)

  iconNew = QtGui.QIcon()
  iconNew.addPixmap(QtGui.QPixmap(os.path.join(base_dir, "etc/icons/ic_forward_black_48dp_2x.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)

  iconNewAsset = QtGui.QIcon()
  iconNewAsset.addPixmap(QtGui.QPixmap(os.path.join(base_dir, "etc/icons/ic_add_box_black_48dp_2x.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)



  iconImportAsset = QtGui.QIcon()
  iconImportAsset.addPixmap(QtGui.QPixmap(os.path.join(base_dir, "etc/icons/ic_move_to_inbox_black_48dp_2x.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)




  # mainUid.pushNewAsset.setIcon(iconNewAsset)

  # mainUid.pushAssImport.setIcon(iconImportAsset)

  mainUid.pushRefresh.setIcon(iconRefresh)
  # mainUid.pushRefreshMedia.setIcon(iconRefresh)
  # mainUid.pushRefreshMediaThumbz.setIcon(iconRefresh)
  mainUid.pushRefreshFilters.setIcon(iconRefresh)
  # mainUid.pushRefreshProjects.setIcon(iconRefresh)
  mainUid.pushSaveFilters.setIcon(iconNew)
  # mainUid.radioStarred.setStyleSheet(rbhusUI.lib.qt5.customWidgets.checkBox_style.styleStarRadioButton)
  # mainUid.radioAsc.setStyleSheet(rbhusUI.lib.qt5.customWidgets.checkBox_style.styleSortCheckBox)







  # mainUid.listWidgetProj.itemSelectionChanged.connect(lambda mainUid=mainUid : changeProject(mainUid))
  # mainUid.listWidgetProj.itemClicked.connect(lambda iotem ,mainUid=mainUid : changeProject(mainUid))
  # maxlen = updateProjectsLists(mainUid)


  # mainUid.listWidgetProj.setSortingEnabled(True)
  mainUid.move(QtWidgets.QApplication.desktop().screen().rect().center() - mainUid.rect().center())
  # mainUid.showMaximized()
  mainUid.show()

  # font = mainUid.listWidgetProj.font()
  # mainUid.groupBoxProjects.setMinimumSize(QtCore.QSize(maxlen*font.pointSize(),0))
  # mainUid.groupBoxProjects.updateGeometry()
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




  mainUid.checkTag.clicked.connect(lambda clicked, mainUid=mainUid: updateAssetsForProjSelect(mainUid))
  mainUid.checkAssName.clicked.connect(lambda clicked, mainUid=mainUid: updateAssetsForProjSelect(mainUid))
  mainUid.checkAssPath.clicked.connect(lambda clicked, mainUid=mainUid: updateAssetsForProjSelect(mainUid))

  mainUid.checkUsers.clicked.connect(lambda clicked, mainUid=mainUid: setUsers(mainUid))

  mainUid.lineEditSearch.textChanged.connect(lambda textChanged, mainUid=mainUid: updateAssetsForProjSelect(mainUid))



  mainUid.pushRefresh.clicked.connect(lambda clicked, mainUid=mainUid: pushRefresh(mainUid))
  # mainUid.pushRefreshMedia.clicked.connect(lambda clicked, mainUid=mainUid: detailsPanelThread(mainUid))
  # mainUid.pushRefreshMediaThumbz.clicked.connect(lambda clicked, mainUid=mainUid: detailsPanelMediaThread(mainUid))
  # mainUid.pushRefreshProjects.clicked.connect(lambda clicked, mainUid=mainUid: updateProjectsLists(mainUid))
  mainUid.pushRefreshFilters.clicked.connect(lambda clicked, mainUid=mainUid: refreshFilter(mainUid))

  mainUid.radioMineAss.clicked.connect(lambda clicked, mainUid=mainUid: updateAssetsForProjSelect(mainUid))
  mainUid.radioAllAss.clicked.connect(lambda clicked, mainUid=mainUid: updateAssetsForProjSelect(mainUid))
  # mainUid.radioStarred.clicked.connect(lambda clicked, mainUid=mainUid: updateAssetsForProjSelect(mainUid))




  mainUid.pushSaveFilters.clicked.connect(lambda clicked,mainUid=mainUid: saveSearchItem(mainUid))

  mainUid.listWidgetSearch.itemChanged.connect(lambda item,mainUid=mainUid: searchItemChanged(mainUid,item))
  loadSearch(mainUid)

  mainUid.listWidgetSearch.customContextMenuRequested.connect(lambda pos, mainUid=mainUid: popUpSearchFav(mainUid, pos))


  updateAssTimer.timeout.connect(lambda mainUid=mainUid: updateAssetsForProjSelectTimed(mainUid))
  # updateSortingTimer.timeout.connect(lambda mainUid=mainUid: updateSortingTimed(mainUid))
  # updateMediaTabTimer.timeout.connect(lambda mainUid=mainUid: updateMediaTabTimed(mainUid))


  mainUid.comboSeq.editTextChanged.connect(lambda textChanged, mainUid=mainUid: setScene(mainUid))
  mainUid.comboSeq.editTextChanged.connect(lambda textChanged, mainUid=mainUid: updateAssetsSeq(mainUid))
  mainUid.comboStage.editTextChanged.connect(lambda textChanged, mainUid=mainUid: updateAssetsForProjSelect(mainUid))
  mainUid.comboNode.editTextChanged.connect(lambda textChanged, mainUid=mainUid: updateAssetsForProjSelect(mainUid))
  mainUid.comboFile.editTextChanged.connect(lambda textChanged, mainUid=mainUid: updateAssetsForProjSelect(mainUid))
  mainUid.comboScn.editTextChanged.connect(lambda textChanged, mainUid=mainUid: updateAssetsForProjSelect(mainUid))
  mainUid.comboAssType.editTextChanged.connect(lambda textChanged, mainUid=mainUid: updateAssetsForProjSelect(mainUid))

  # mainUid.listWidgetAssets.customContextMenuRequested.connect(lambda pos, mainUid=mainUid: popupAss(mainUid, pos))
  # mainUid.listWidgetProj.customContextMenuRequested.connect(lambda pos, mainUid=mainUid: popupProjects(mainUid, pos))


  # mainUid.pushAssImport.clicked.connect(lambda clicked, mainUid=mainUid: rbhusAssImport(mainUid))
  # mainUid.pushNewAsset.clicked.connect(lambda clicked, mainUid=mainUid: rbhusPipeAssetCreate(mainUid))
  mainUid.actionNew_seq_scn.triggered.connect(lambda clicked, mainUid=mainUid: rbhusPipeSeqSceCreate(mainUid))
  mainUid.actionEdit_seq_scn.triggered.connect(lambda clicked, mainUid=mainUid: rbhusPipeSeqSceEdit(mainUid))

  # mainUid.radioAsc.clicked.connect(lambda clicked, mainUid=mainUid: updateSorting(mainUid))
  # mainUid.comboBoxSort.currentTextChanged.connect(lambda textChanged, mainUid=mainUid: updateSorting(mainUid))

  # mainUid.listWidgetAssets.itemSelectionChanged.connect(lambda mainUid=mainUid: detailsPanelThread(mainUid))
  # mainUid.listWidgetSubDir.itemSelectionChanged.connect(lambda mainUid=mainUid: detailsPanelMediaThread(mainUid))
  # mainUid.listWidgetMedia.itemSelectionChanged.connect(lambda mainUid=mainUid: selectedMedia(mainUid))
  # mainUid.tabWidget.currentChanged.connect(lambda index,mainUid=mainUid: updateMediaTab(mainUid))

  # loadDefaultProject(mainUid)

  mainUid.splitter.setStretchFactor(0,10)
  # mainUid.splitterAssetDetails.setStretchFactor(0,0.75)
  # mainUid.splitterProj.setSizes((10,500))
  # mainUid.splitterAssetDetails.setStretchFactor(2,0.25)
  # mainUid.splitterAssetDetails.setSizes((1000,50))
  # mainUid.splitterMedia.setSizes((1,200))

  #hide unwanted events
  # mainUid.listWidgetAssets.dropEvent = eatEvents
  # mainUid.listWidgetAssets.dragEnterEvent = eatEvents
  # mainUid.listWidgetAssets.dragMoveEvent = eatEvents

  # mainUid.listWidgetMedia.dropEvent = eatEvents
  # mainUid.listWidgetMedia.dragEnterEvent = eatEvents
  # mainUid.listWidgetMedia.dragMoveEvent = eatEvents


  mainUid.closeEvent = closeEvent
  updateAssetsForProjSelect(mainUid)
  refreshFilter(mainUid)

  # mainUid.groupBoxShowOnly.hide()

  # mainUid.groupBoxUpdates.hide()




if __name__ == '__main__':
  app = QtWidgets.QApplication(sys.argv)
  mainUid = uic.loadUi(ui_main)
  main_func(mainUid)
  os._exit((app.exec_()))
