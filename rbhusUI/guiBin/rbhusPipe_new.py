#!/usr/bin/env python2 -d
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
ui_dir = os.path.join(base_dir,"rbhusUI","lib","qt5","rbhusPipe_main")
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


projects = []

ui_main = os.path.join(ui_dir,"ui_main.ui")
ui_asset_details = os.path.join(ui_dir,"assetDetailRow.ui")
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

assImporter = "rbhusAssetImport.py"


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
rbhusPipeAssetImportCmd = os.path.join(file_dir, assImporter)
selectRadioBoxCmd = os.path.join(file_dir, srb)


updateAssThreads = []
updateAssThreadsFav = []
assDetsItems = []
ImageWidgets = []
assDetsWidgetsDict = {}
mediaWidgets = {}
updateDetailsThreads = []
updateDetailsPanelMediaThreads = []


assColumnList = ['','','asset','assigned','reviewer','modified','v','review','publish','']

try:
  username = os.environ['rbhusPipe_acl_user'].rstrip().lstrip()
except:
  pass

favLock = QtCore.QMutex()
updateAssTimer = QtCore.QTimer()
updateAssFavTimer = QtCore.QTimer()
updateSortingTimer = QtCore.QTimer()
updateMediaTabTimer = QtCore.QTimer()


class api_serv(QtCore.QThread):
  msg_recved = QtCore.pyqtSignal(object)
  def __init__(self,parent):
    super(api_serv, self).__init__(parent)

    self.context = zmq.Context()

    # Define the socket using the "Context"
    self.sock = self.context.socket(zmq.REP)
    self.sock.bind("tcp://127.0.0.1:8989")
    rbhus.debug.debug("API-SERV")
  def run(self):
    while True:
      (id, msg) = self.sock.recv_multipart()
      self.msg_recved.emit(msg)
      self.sock.send_multipart([bytes(id), "ack"])



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



class QListWidgetItemSortAsses(QtWidgets.QListWidgetItem):
  def __init__(self,assetDets):
    super(QListWidgetItemSortAsses, self).__init__()
    self.assetDets = assetDets
    self.sortby = None
    # self.setData(QtCore.Qt.UserRole,self.assetDets)

  def update_assetDets(self,assetDets):
    self.assetDets = assetDets

  def sortby_asset(self):
    self.setData(QtCore.Qt.UserRole,self.assetDets['path'])
    self.sortby = "asset"

  def sortby_review(self):
    self.setData(QtCore.Qt.UserRole,self.assetDets['reviewStatus'])
    self.sortby = "review"

  def sortby_modified(self):
    self.setData(QtCore.Qt.UserRole,self.assetDets['modified'])
    self.sortby = "modified"

  def sortby_published(self):
    self.setData(QtCore.Qt.UserRole,self.assetDets['publishVersion'])
    self.sortby = "published"

  def sortby_version(self):
    self.setData(QtCore.Qt.UserRole,self.assetDets['versioning'])
    self.sortby = "version"

  def sortby_assigned(self):
    self.setData(QtCore.Qt.UserRole,self.assetDets['assignedWorker'])
    self.sortby = "assigned"

  def sortby_reviewer(self):
    self.setData(QtCore.Qt.UserRole,self.assetDets['reviewUser'])
    self.sortby = "reviewer"

  def sortby_creator(self):
    self.setData(QtCore.Qt.UserRole,self.assetDets['createdUser'])
    self.sortby = "creator"


  def __lt__(self, other):
    return self.data(QtCore.Qt.UserRole) < other.data(QtCore.Qt.UserRole)

  def __ge__(self, other):
    return self.data(QtCore.Qt.UserRole) > other.data(QtCore.Qt.UserRole)

  def __eq__(self, other):
    return self.data(QtCore.Qt.UserRole) == other.data(QtCore.Qt.UserRole)


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

class updateDetailsPanelMediaQthread(QtCore.QThread):
  mediaSignal = QtCore.pyqtSignal(object)
  mediaStarted = QtCore.pyqtSignal()
  mediaCountCurrent = QtCore.pyqtSignal(int)
  mediaCountMax = QtCore.pyqtSignal(int)


  def __init__(self,parent=None,mediaObjList=None):
    super(updateDetailsPanelMediaQthread, self).__init__(parent)
    self.mediaObjList = mediaObjList
    self.pleaseStop = False

  def exitshit(self):
    self.pleaseStop = True

  def run(self):
    self.mediaStarted.emit()
    if(self.mediaObjList):
      self.mediaCountMax.emit(len(self.mediaObjList))
      i = 0
      for x in self.mediaObjList:
        if(self.pleaseStop == False):
          self.mediaSignal.emit(x)
          i = i+1
          self.mediaCountCurrent.emit(i)
          time.sleep(0.01)
        else:
          break
    # self.finished.emit()


class updateDetailsPanelQthread(QtCore.QThread):
  thumbzSignal = QtCore.pyqtSignal(object)
  thumbzStarted = QtCore.pyqtSignal()
  thumbzTotal = QtCore.pyqtSignal(object)

  def __init__(self,parent=None,assPath=None):
    super(updateDetailsPanelQthread, self).__init__(parent)
    self.assPath = assPath
    self.pleaseStop = False

  def exitshit(self):
    self.pleaseStop = True

  def callback_stop(self):
    return(self.pleaseStop)

  def callback_media(self,obj):
    self.thumbzSignal.emit(obj)

  def callback_total(self,obj):
    self.thumbzTotal.emit(obj)

  def run(self):
    self.thumbzStarted.emit()
    rbhus.utilsPipe.getUpdatedMediaThumbz(self.assPath, QT_callback_signalThumbz=self.callback_media, QT_callback_isStopped=self.callback_stop, QT_callback_total=self.callback_total)
    # self.finished.emit()



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
            if(os.path.exists("/etc/gentoo-release")):
              time.sleep(0.05)
            else:
              time.sleep(0.1)
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
  rbhus.utilsPipe.exportProj(projects[-1])

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

  updateAssThread = updateAssQthread(project = projects,whereDict=whereDict,parent=mainUid,isFav=mainUid.radioStarred.isChecked())
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
  updateSorting(mainUid)


def updateSorting(mainUid):
  updateSortingTimer.stop()
  updateSortingTimer.setSingleShot(True)
  updateSortingTimer.start(100)



def updateSortingTimed(mainUid):
  global assDetsItems
  if (mainUid.comboBoxSort.currentText() == "review"):
    rbhus.debug.debug("sorting for asset review")
    for x in assDetsItems:
      x.sortby_review()

  elif (mainUid.comboBoxSort.currentText() == "modified"):
    rbhus.debug.debug("sorting for asset modified")
    for x in assDetsItems:
      x.sortby_modified()

  elif (mainUid.comboBoxSort.currentText() == "published"):
    rbhus.debug.debug("sorting for asset published")
    for x in assDetsItems:
      x.sortby_published()

  elif (mainUid.comboBoxSort.currentText() == "version"):
    rbhus.debug.debug("sorting for asset version")
    for x in assDetsItems:
      x.sortby_version()

  elif (mainUid.comboBoxSort.currentText() == "assigned"):
    rbhus.debug.debug("sorting for asset assigned")
    for x in assDetsItems:
      x.sortby_assigned()

  elif (mainUid.comboBoxSort.currentText() == "reviewer"):
    rbhus.debug.debug("sorting for asset reviewer")
    for x in assDetsItems:
      x.sortby_reviewer()

  elif (mainUid.comboBoxSort.currentText() == "creator"):
    rbhus.debug.debug("sorting for asset creator")
    for x in assDetsItems:
      x.sortby_creator()

  else:
    rbhus.debug.debug("sorting for asset")
    for x in assDetsItems:
      x.sortby_asset()


  if(mainUid.radioAsc.isChecked()):
    mainUid.listWidgetAssets.sortItems(QtCore.Qt.AscendingOrder)
  else:
    mainUid.listWidgetAssets.sortItems(QtCore.Qt.DescendingOrder)

  # for x in assDetsWidgets:
  #   x.updateGeometry()
  # mainUid.listWidgetAssets.update()



def updateTotalAss(mainUid,totalRows):
  global assDetsItems
  global ImageWidgets
  global assDetsWidgetsDict
  mainUid.labelTotal.setText(str(totalRows))
  mainUid.listWidgetAssets.clear()
  # mainUid.listWidgetAssets.setMinimumHeight(56)
  # mainUid.listWidgetAssets.setSortingEnabled(False)

  # for x in assDetsItems:
  #   try:
  #     x.deleteLater()
  #   except:
  #     rbhus.debug.debug(sys.exc_info())

  for x in ImageWidgets:
    try:
      x.deleteLater()
    except:
      rbhus.debug.debug(sys.exc_info())

  for x in assDetsWidgetsDict:
    try:
      assDetsWidgetsDict[x].deleteLater()
    except:
      rbhus.debug.debug(sys.exc_info())

  del assDetsItems[:]
  del ImageWidgets[:]
  assDetsWidgetsDict.clear()



def updateAssSlot(mainUid, richAss, assetDets):
  global ImageWidgets
  global assDetsWidgetsDict
  global assDetsItems


  assDetsWidget = uic.loadUi(ui_asset_details)
  # assDetsWidget.labelAsset.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True)

  assDetsWidget.checkBoxStar.setStyleSheet(rbhusUI.lib.qt5.customWidgets.checkBox_style.styleStarCheckBox)
  if (assetDets['fav']):
    assDetsWidget.checkBoxStar.setChecked(True)
  assDetsWidget.checkBoxStar.clicked.connect(lambda clicked, assPath=assetDets['path'], starObj=assDetsWidget.checkBoxStar, mainUid=mainUid: updateFavorite(mainUid, assPath, starObj))

  assDetsWidget.checkBoxNotes.setStyleSheet(rbhusUI.lib.qt5.customWidgets.checkBox_style.styleNotesCheckBox)
  if (assetDets['isNotes']):
    assDetsWidget.checkBoxNotes.setChecked(True)

  assDetsWidget.checkBoxReview.setStyleSheet(rbhusUI.lib.qt5.customWidgets.checkBox_style.styleReviewCheckBox)
  if (assetDets['reviewStatus'] == rbhus.constantsPipe.reviewStatusNotDone):
    assDetsWidget.checkBoxReview.setCheckState(QtCore.Qt.Unchecked)
  elif(assetDets['reviewStatus'] == rbhus.constantsPipe.reviewStatusInProgress):
    assDetsWidget.checkBoxReview.setCheckState(QtCore.Qt.PartiallyChecked)
  else:
    assDetsWidget.checkBoxReview.setCheckState(QtCore.Qt.Checked)

  assDetsWidget.checkBoxPublish.setStyleSheet(rbhusUI.lib.qt5.customWidgets.checkBox_style.stylePublishCheckBox)
  if (assetDets['publishVersion']):
    assDetsWidget.checkBoxPublish.setChecked(True)
  else:
    assDetsWidget.checkBoxPublish.setChecked(False)

  assDetsWidget.checkBoxVersion.setStyleSheet(rbhusUI.lib.qt5.customWidgets.checkBox_style.styleVersioningCheckBox)
  if (assetDets['versioning']):
    assDetsWidget.checkBoxVersion.setChecked(True)
  else:
    assDetsWidget.checkBoxVersion.setChecked(False)


  assDetsWidget.labelAsset.setTextFormat(QtCore.Qt.RichText)
  assDetsWidget.labelAsset.setText(richAss)

  if(assetDets['preview_low']):
    previewWidget = ImageWidget(assetDets['preview_low'],40,parent=mainUid)
    previewWidget.clicked.connect(lambda x, imagePath = assetDets['preview']: imageWidgetClicked(imagePath))
    ImageWidgets.append(previewWidget)
  else:
    previewWidget = None

  if(previewWidget):
    assDetsWidget.horizontalLayoutPreview.addWidget(previewWidget)


  item = QListWidgetItemSortAsses(assetDets)
  item.setSizeHint(assDetsWidget.sizeHint())

  mainUid.listWidgetAssets.addItem(item)
  mainUid.listWidgetAssets.setItemWidget(item, assDetsWidget)

  # assDetsWidgets.append(assDetsWidget)
  assDetsWidgetsDict[assetDets['path']] = assDetsWidget
  assDetsItems.append(item)
  # mainUid.listWidgetAssets.update()



def imageWidgetClicked(imagePath,mimeType=None):
  if(mimeType):
    if(mimeType != "blender"):
      import webbrowser
      webbrowser.open(imagePath)
  else:
    import webbrowser
    webbrowser.open(imagePath)






def detailsPanelThread(mainUid):
  items = mainUid.listWidgetAssets.selectedItems()
  if(len(items) == 1):
    assetDets = items[0].assetDets
    mainUid.labelRichAss.setText(assetDets['richAss'])
    mainUid.labelAssigned.setText(assetDets['assignedWorker'])
    mainUid.labelReviewer.setText(assetDets['reviewUser'])
    mainUid.labelCreator.setText(assetDets['createdUser'])
    mainUid.labelImportedFrom.setText(assetDets['importedFrom'])
    mainUid.labelDescription.setText(assetDets['description'])
    mainUid.labelTags.setText(assetDets['tags'])
    mainUid.labelGroup.setText(assetDets['assetGroups'])

    if(assetDets['modified']):
      mainUid.labelModified.setText(time.strftime("%Y %B %d %A # %I:%M %p", time.localtime(assetDets['modified'])))
    else:
      mainUid.labelModified.setText("NOT FOUND")

    updateMediaTab(mainUid)
  else:
    stopMediaThreads(mainUid)


def stopMediaThreads(mainUid):
  global updateDetailsThreads
  if (updateDetailsThreads):
    for runningThread in updateDetailsThreads:
      runningThread.exitshit()
      runningThread.wait()
      try:
        runningThread.disconnect()
      except:
        rbhus.debug.debug(runningThread)
      try:
        runningThread.deleteLater()
      except:
        rbhus.debug.debug(sys.exc_info())
      updateDetailsThreads.remove(runningThread)

def updateMediaTab(mainUid):
  updateMediaTabTimer.stop
  updateMediaTabTimer.setSingleShot(True)
  updateMediaTabTimer.start(500)



def updateMediaTabTimed(mainUid):
  items = mainUid.listWidgetAssets.selectedItems()
  stopMediaThreads(mainUid)
  if(len(items) == 1):
    assetDets = items[0].assetDets
    currentTab = mainUid.tabWidget.currentIndex()
    if(currentTab == 1):
      startMediaThread(assetDets,mainUid)





def startMediaThread(assetDets,mainUid):
  global updateDetailsThreads
  updateDetailsThread = updateDetailsPanelQthread(assPath=assetDets['path'], parent=mainUid)
  updateDetailsThread.thumbzStarted.connect(lambda mainUid=mainUid: clearListWidgetSubDir(mainUid))
  updateDetailsThread.thumbzTotal.connect(lambda totalObj, mainUid=mainUid: getTotalMedia(mainUid, totalObj))
  updateDetailsThread.finished.connect(lambda mainUid=mainUid: mediaUpdateDone(mainUid))
  updateDetailsThread.thumbzSignal.connect(lambda mediaObj, mainUid=mainUid: updateDetailsPanel(mainUid, mediaObj))
  updateDetailsThreads.append(updateDetailsThread)
  updateDetailsThread.start()


def clearListWidgetSubDir(mainUid):
  global mediaWidgets
  mediaWidgets.clear()
  mainUid.listWidgetSubDir.clear()
  mainUid.progressBarMedia.setMinimum(0)
  mainUid.progressBarMedia.setMaximum(0)
  mainUid.progressBarMedia.setValue(0)

  mainUid.progressBarMediaThumbz.setMinimum(0)
  mainUid.progressBarMediaThumbz.setMaximum(1)
  mainUid.progressBarMediaThumbz.setValue(0)

def getTotalMedia(mainUid,totalObj):
  # rbhus.debug.debug(totalObj)
  mainUid.progressBarMediaThumbz.totalObj = totalObj


def mediaUpdateDone(mainUid):
  mainUid.progressBarMedia.setMinimum(0)
  mainUid.progressBarMedia.setMaximum(1)
  mainUid.progressBarMedia.setValue(0)
  item = mainUid.listWidgetSubDir.item(0)
  if(item):
    mainUid.listWidgetSubDir.setCurrentItem(item)
  detailsPanelMediaThread(mainUid)

def updateDetailsPanel(mainUid,mediaObj):
  global mediaWidgets
  # print(mediaObj.mimeType, mediaObj.subPath, mediaObj.mainFile, mediaObj.thumbFile)
  if (not mediaWidgets.has_key(mediaObj.subPath)):

    item = QtWidgets.QListWidgetItem()
    item.subPath = mediaObj.subPath
    if (mediaObj.subPath):
      item.setText(mediaObj.subPath)
      item.setToolTip(mediaObj.subPath)
    else:
      item.setText("-")
      item.setToolTip("-")
    try:
      item.medias.append(mediaObj)
    except:
      item.medias = []
      item.medias.append(mediaObj)


    mainUid.listWidgetSubDir.addItem(item)
    mediaWidgets[mediaObj.subPath] = item
  else:
    mediaWidgets[mediaObj.subPath].medias.append(mediaObj)


def detailsPanelMediaThread(mainUid):
  global updateDetailsPanelMediaThreads
  items = selectedSubDir(mainUid)



  mediasToLoad = []

  if (updateDetailsPanelMediaThreads):
    for runningThread in updateDetailsPanelMediaThreads:
      runningThread.exitshit()
      runningThread.wait()
      try:
        runningThread.disconnect()
      except:
        rbhus.debug.debug(runningThread)
      try:
        runningThread.deleteLater()
      except:
        rbhus.debug.debug(sys.exc_info())
      updateDetailsPanelMediaThreads.remove(runningThread)

  mainUid.listWidgetMedia.clear()

  # clear the subdir thumbnails progress bar
  mainUid.progressBarMediaThumbz.setMinimum(0)
  mainUid.progressBarMediaThumbz.setMaximum(1)
  mainUid.progressBarMediaThumbz.setValue(0)
  mainUid.labelTotalThumbz.setText("0")

  # mainUid.listWidgetMedia.setSortingEnabled(False)

  if(items):
    maxThumbzTrueValue = 0
    for item in items:
      maxThumbzTrueValue = maxThumbzTrueValue + mainUid.progressBarMediaThumbz.totalObj[str(item.text())]
      for media in item.medias:
        mediasToLoad.append(media)
    mainUid.progressBarMediaThumbz.setMaximum(maxThumbzTrueValue)
    mainUid.labelTotalThumbz.setText(str(maxThumbzTrueValue))

    updateDetailsPanelMediaThread = updateDetailsPanelMediaQthread(mediaObjList=mediasToLoad,parent=mainUid)
    updateDetailsPanelMediaThread.mediaSignal.connect(lambda mediaObj, mainUid=mainUid: updateThumbz(mainUid,mediaObj))
    updateDetailsPanelMediaThread.mediaCountCurrent.connect(lambda value, mainUid=mainUid : updateThumbzProgress(mainUid, value))
    # updateDetailsPanelMediaThread.mediaCountMax.connect(lambda value, mainUid=mainUid : updateThumbzProgressMax(mainUid, value))
    # updateDetailsPanelMediaThread.thumbzTotal.connect(lambda totalObj, mainUid=mainUid: getTotalMedia(mainUid, totalObj))
    # updateDetailsPanelMediaThread.mediaStarted.connect(lambda mainUid=mainUid: listWidgetMediaSortDisable(mainUid))
    # updateDetailsPanelMediaThread.finished.connect(lambda mainUid=mainUid: listWidgetMediaSortEnable(mainUid))
    # updateDetailsPanelMediaThread.finished.connect(lambda mainUid=mainUid: updateMediaTab(mainUid))
    # updateDetailsPanelMediaThread.thumbzSignal.connect(lambda mediaObj, mainUid=mainUid: updateDetailsPanel(mainUid, mediaObj))
    updateDetailsPanelMediaThreads.append(updateDetailsPanelMediaThread)
    updateDetailsPanelMediaThread.start()


def updateThumbzProgress(mainUid,value):
  mainUid.progressBarMediaThumbz.setValue(value)

def updateThumbzProgressMax(mainUid,value):
  mainUid.progressBarMediaThumbz.setMaximum(value)
  mainUid.labelTotalThumbz.setText(str(value))



def listWidgetMediaSortEnable(mainUid):
  mainUid.listWidgetMedia.setSortingEnabled(True)

def listWidgetMediaSortDisable(mainUid):
  mainUid.listWidgetMedia.setSortingEnabled(False)


def updateThumbz(mainUid,mediaObj):
  # print(mediaObj.mimeType, mediaObj.subPath, mediaObj.mainFile, mediaObj.thumbFile)
  itemWidget = uic.loadUi(ui_asset_media_Thumbz)
  itemWidget.labelImageName.setText(os.path.basename(mediaObj.mainFile))
  imageThumb = ImageWidget(mediaObj.thumbFile,64,parent=itemWidget.widgetImage)
  imageThumb.clicked.connect(lambda x, imagePath = mediaObj.mainFile,mimeType=mediaObj.mimeType: imageWidgetClicked(imagePath,mimeType=mimeType))
  itemWidget.imageLayout.addWidget(imageThumb)
  item = QListWidgetItemSort()
  icon = QtGui.QIcon(rbhus.constantsPipe.mimeLogos[mediaObj.mimeType])
  itemWidget.pushButtonLogo.setIcon(icon)
  # item.setSizeHint(QtCore.QSize(96,96))
  item.setData(QtCore.Qt.UserRole,os.path.basename(mediaObj.mainFile))
  item.setToolTip(mediaObj.subPath + os.sep + os.path.basename(mediaObj.mainFile))
  item.media = mediaObj
  item.setSizeHint(itemWidget.sizeHint() + QtCore.QSize(10,10))
  mainUid.listWidgetMedia.addItem(item)
  mainUid.listWidgetMedia.setItemWidget(item,itemWidget)


def selectedMedia(mainUid):
  items = mainUid.listWidgetMedia.selectedItems()
  for x in items:
    print(x.media.mainFile)
  return (items)







def selectedSubDir(mainUid):
  items = mainUid.listWidgetSubDir.selectedItems()
  return (items)




def selectedAsses(mainUid,isFav=False):
  items = mainUid.listWidgetAssets.selectedItems()
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


def popupMedia(mainUid,pos):
  menu = QtWidgets.QMenu()
  openAction = menu.addAction("open with")
  # compareAction = menu.addAction("compare")


def popupSubDir(mainUid,pos):
  menu = QtWidgets.QMenu()
  openAction = menu.addAction("copy path ")
  # compareAction = menu.addAction("compare")




def popupAss(mainUid,pos,isFav=False):
  listAssesFull = selectedAsses(mainUid,isFav=isFav)
  listAsses = []
  for x in listAssesFull:
    if(x):
      listAsses.append(x)
  # rbhus.debug.debug("selected asses : "+ str(len(listAsses)))
  if(len(listAsses) == 0):
    return(0)

  menu = QtWidgets.QMenu()
  menuTools = QtWidgets.QMenu()
  menuProgress = QtWidgets.QMenu()
  menuCopy = QtWidgets.QMenu()
  menuTemplate = QtWidgets.QMenu()
  menuCopy.setTitle("copy to clipboard")
  # menuProgress.setTitle("progress status")
  menuTemplate.setTitle("template tools")
  menuTools.setTitle("tools")


  # inProgressAction = menuProgress.addAction("set to inProgress")
  # inProgressDoneAction = menuProgress.addAction("set to done")

  assCopyToClip = menuCopy.addAction("path")
  assCopyPathToClip = menuCopy.addAction("asset path")
  assPublishPath = menuCopy.addAction("publish path")
  assVersionPath = menuCopy.addAction("version path")


  openFolderAction = menu.addAction("open")
  # addToFavAction = menuTools.addAction("add to shortcuts")
  assEditAction = menuTools.addAction("edit")

  assReviewAction = menuTools.addAction("check review")
  assNotesAction = menuTools.addAction("asset notes")

  menuTools.addMenu(menuCopy)
  # menuTools.addMenu(menuProgress)
  menuTools.addMenu(menuTemplate)
  assGetTemplate = menuTemplate.addAction("reset from templates")
  assGetTemplateUpdate = menuTemplate.addAction("update to templates")
  hardAssGetTemplate = menuTemplate.addAction("hard reset from templates")
  assRender = menuTools.addAction("submit to render")
  assDeleteAction = menuTools.addAction("delete - database only")

  menu.addMenu(menuTools)
  if(isFav):
    action = menu.exec_(mainUid.tableWidgetAssetsFav.mapToGlobal(pos))
  else:
    action = menu.exec_(mainUid.listWidgetAssets.mapToGlobal(pos))


  if(action == openFolderAction):
    openFolderAss(mainUid,assetList=listAsses)
  if(action == assCopyToClip):
    copyPathToClip(mainUid,assetList=listAsses)
  if(action == assCopyPathToClip):
    copyPipePathToClip(mainUid,assetList=listAsses)
  if(action == assEditAction):
    editAss(mainUid,assetList=listAsses)
  if(action == assDeleteAction):
    delAss(mainUid,assetList=listAsses)
  if(action == assRender):
    renderAss(mainUid,assetList=listAsses)
  if(action == assGetTemplate):
    resetTemplateFiles(mainUid,assetList=listAsses)

  if(action == hardAssGetTemplate):
    resetTemplateFiles(mainUid,hard=True,assetList=listAsses)


  if(action == assReviewAction):
    reviewAss(mainUid,assetList=listAsses)

  if(action == assNotesAction):
    notesAss(mainUid,assetList=listAsses)

  if(action == assPublishPath):
    copyPublishPath(mainUid,assetList=listAsses)
  if(action == assVersionPath):
    copyVersionPathToClip(mainUid, assetList=listAsses)

  # if(action == inProgressAction):
  #   self.setInProgress()
  # if(action == inProgressDoneAction):
  #   self.setDone()
  if(action == assGetTemplateUpdate):
    resetAssToTemplateFiles(mainUid, assetList=listAsses)


def reviewAss(mainUid,assetList=None):
  if(assetList):
    listAsses = assetList
  if(isinstance(assetList,str)):
    assPath = assetList
  else:
    listedAss = listAsses[0]
    assPath = listedAss['path']

  if(sys.platform.find("win") >= 0):
    a = subprocess.Popen([rbhusPipeReviewCmd,"--assetpath",assPath],shell = True)
  elif(sys.platform.find("linux") >= 0):
    a = subprocess.Popen(rbhusPipeReviewCmd +" --assetpath "+ assPath,shell = True)
  a.wait()
  if(assDetsWidgetsDict.has_key(assPath)):
    assetDets = rbhus.utilsPipe.getAssDetails(assPath=assPath)
    if (assetDets['reviewStatus'] == rbhus.constantsPipe.reviewStatusNotDone):
      assDetsWidgetsDict[assPath].checkBoxReview.setCheckState(QtCore.Qt.Unchecked)
    elif (assetDets['reviewStatus'] == rbhus.constantsPipe.reviewStatusInProgress):
      assDetsWidgetsDict[assPath].checkBoxReview.setCheckState(QtCore.Qt.PartiallyChecked)
    else:
      assDetsWidgetsDict[assPath].checkBoxReview.setCheckState(QtCore.Qt.Checked)



def notesAss(mainUid,assetList=None):
  if(assetList):
    listAsses = assetList
  if(isinstance(assetList,str)):
    assPath = assetList
  else:
    listedAss = listAsses[0]
    assPath = listedAss['path']

  if(sys.platform.find("win") >= 0):
    subprocess.Popen([rbhusPipeNotesCmd,"--assetpath",assPath],shell = True)
  elif(sys.platform.find("linux") >= 0):
    subprocess.Popen(rbhusPipeNotesCmd +" --assetpath "+ assPath,shell = True)



def resetTemplateFiles(mainUid,hard=False,assetList=None):
  yn = False
  if(hard):
    yn = messageBoxTemplateHard()
  else:
    yn = True
  if(yn):
    selass = assetList
    for x in selass:
      assDets = rbhus.utilsPipe.getAssDetails(assPath = x['path'])
      rbhus.utilsPipe.setAssTemplate(assDets,hard=hard)


#todo : allow only for projAdmin . dangerous activity
def resetAssToTemplateFiles(mainUid,assetList=None):
  if(assetList):
    selass = assetList
  for x in selass:
    # debug.info(selass[x])
    assDets = rbhus.utilsPipe.getAssDetails(assPath = x['path'])
    rbhus.utilsPipe.setTemplateAss(assDets)


def renderAss(mainUid, assetList=None):
  if(assetList):
    listAsses = assetList

  filesTorender = getFileAss(mainUid,assetList=assetList)
  listedAss = listAsses[0]['path']
  renderFiles = []
  if(not isinstance(filesTorender,int)):
    for x in filesTorender:
      if(x):
        renderFiles.append(str(x))
        rbhus.debug.debug(x)
  if(renderFiles):
    subprocess.Popen(rbhusPipeRenderSubmitCmd +" --file \""+ renderFiles[0] +"\" --path \""+ listedAss +"\"",shell=True)      #os.system(versionCmd +" --path \""+ selass[-1] +"\"")
    return(1)
  else:
    return(0)

def getFileAss(mainUid,assetList=None):
  if(assetList):
    listAsses = assetList
  x = str(listAsses[0]['path'])
  if(x): # and (len(listAsses) == 1)
    p = rbhus.utilsPipe.getAbsPath(x)
    if(os.path.exists(p)):
      fila = QtWidgets.QFileDialog.getOpenFileNames(directory=p)
      rbhus.debug.debug(fila)
      if(fila):
        return(fila[0])
      else:
        return(0)
    else:
      return(0)

def delAss(mainUid,hard=False,assetList=None):
  if(assetList):
    listAsses = assetList

  wtf = messageBoxDelete(hard=hard)
  if(wtf):
    for x in listAsses:
      if(str(x)):
        rbhus.utilsPipe.assMarkForDelete(assPath=str(x['path']))
    updateAssetsForProjSelect(mainUid)


def copyPathToClip(mainUid,assetList=None):
  if(assetList):
    listAsses = assetList
  # debug.info(listAsses)
  if(listAsses):
    x = listAsses[0]['path']
    abspath =  rbhus.utilsPipe.getAbsPath(x)
    rbhus.pyperclip.copy(abspath)

def copyPublishPath(mainUid,assetList=None):
  if(assetList):
    listAsses = assetList

  if(listAsses):
    x = listAsses[0]['path']
    abspath =  rbhus.utilsPipe.getAbsPath(x)
    abspath = abspath + "/publish"
    rbhus.pyperclip.copy(abspath)




def copyPipePathToClip(mainUid, assetList=None):
  if(assetList):
    listAsses = assetList
  if(listAsses):
    x = listAsses[0]['path']
    rbhus.pyperclip.copy(x)



def copyVersionPathToClip(mainUid,assetList=None):
  if(assetList):
    listAsses = assetList

  if(listAsses):
    x = listAsses[0]['path']
    versionPath =  rbhus.hgmod.hg(x).localPath
    rbhus.pyperclip.copy(versionPath)


def openFolderAss(mainUid,assetList=None):
  if(assetList):
    x = assetList[0]


  if(x):
    # debug.info(x)
    p = rbhus.utilsPipe.getAbsPath(x['path'])
    assdets = x
    if(os.path.exists(p)):
      if(assdets['versioning'] == 0):
        fila = QtWidgets.QFileDialog.getOpenFileNames(directory=p)[0]
        rbhus.debug.debug(fila)
        if(fila):
          rbhus.debug.debug(str(fila[0]))
          filename = str(fila[0])
          rbhus.debug.debug(filename.split("."))
          assdets = rbhus.utilsPipe.getAssDetails(assPath=x['path'])
          runCmd = rbhus.utilsPipe.openAssetCmd(assdets,filename)
          if(runCmd):
            runCmd = runCmd.rstrip().lstrip()
            if(sys.platform.find("win") >= 0):
              rbhus.debug.debug(runCmd)
              subprocess.Popen(runCmd,shell=True)
            elif(sys.platform.find("linux") >= 0):
              rbhus.debug.debug(runCmd)
              subprocess.Popen(runCmd,shell=True)
          else:
            import webbrowser
            webbrowser.open(filename)
      else:
        rbhus.debug.debug("wtf : opening version cmd ")
        if(sys.platform.find("win") >= 0):
          subprocess.Popen([versionCmd,"--path",x['path']],shell = True)
        elif(sys.platform.find("linux") >= 0):
          subprocess.Popen(versionCmd +" --path "+ x['path'],shell = True)
  # self.centralwidget.setCursor(QtCore.Qt.ArrowCursor)
  for x in os.environ.keys():
    if(x.find("rp_") >= 0):
      rbhus.debug.debug(x +" : "+os.environ[x])

def editAss(mainUid,assetList=None):
  if(assetList):
    listAssesFull = assetList
    listAsses = []
  for x in listAssesFull:
    listAsses.append(x['path'])
  if(listAsses):
    rbhusAssetEditCmdMod = rbhusPipeAssetEditCmd +" -p "+ ",".join(listAsses)
    rbhus.debug.debug(rbhusAssetEditCmdMod)

    p = QtCore.QProcess(parent=mainUid)
    p.setStandardOutputFile(tempDir + os.sep + "rbhusPipeAssetEdit_" + username + ".log")
    p.setStandardErrorFile(tempDir + os.sep + "rbhusPipeAssetEdit_" + username + ".err")
    p.start(sys.executable, rbhusAssetEditCmdMod.split())
    # p.finished.connect(lambda a ,b, mainUid=mainUid : updateAssetsForProjSelect(mainUid))



def rbhusPipeSeqSceCreate(mainUid):
  p = QtCore.QProcess(parent=mainUid)
  p.setStandardOutputFile(tempDir + os.sep +"rbhusPipeSeqSceCreate_"+ username +".log")
  p.setStandardErrorFile(tempDir + os.sep +"rbhusPipeSeqSceCreate_"+ username +".err")
  mainUid.actionNew_seq_scn.setEnabled(False)
  p.start(sys.executable,rbhusPipeSeqSceCreateCmd.split())
  p.finished.connect(lambda exitstatus ,test, mainUid=mainUid:rbhusPipeSeqSceCreateEnable(mainUid,exitstatus))

def rbhusPipeSeqSceCreateEnable(mainUid,exitStatus):
  mainUid.actionNew_seq_scn.setEnabled(True)


def rbhusPipeSeqSceEdit(mainUid):
  p = QtCore.QProcess(parent=mainUid)
  p.setStandardOutputFile(tempDir + os.sep +"rbhusPipeSeqSceEdit_"+ username +".log")
  p.setStandardErrorFile(tempDir + os.sep +"rbhusPipeSeqSceEdit_"+ username +".err")
  mainUid.actionEdit_seq_scn.setEnabled(False)
  p.start(sys.executable,rbhusPipeSeqSceEditCmd.split())
  p.finished.connect(lambda exitstatus , test, mainUid=mainUid:rbhusPipeSeqSceEditEnable(mainUid,exitstatus))

def rbhusPipeSeqSceEditEnable(mainUid,exitStatus):
  mainUid.actionEdit_seq_scn.setEnabled(True)



def rbhusPipeAssetCreate(mainUid):
  p = QtCore.QProcess(parent=mainUid)
  p.setStandardOutputFile(tempDir + os.sep +"rbhusPipeAssetCreate_"+ username +".log")
  p.setStandardErrorFile(tempDir + os.sep +"rbhusPipeAssetCreate_"+ username +".err")
  mainUid.pushNewAsset.setEnabled(False)
  rbhus.debug.debug("wtf1 : "+ rbhusPipeAssetCreateCmd)
  p.start(sys.executable,rbhusPipeAssetCreateCmd.split())
  p.finished.connect(lambda exitstatus,test, mainUid=mainUid: rbhusPipeAssCreateEnable(exitstatus,mainUid))


def rbhusPipeAssCreateEnable(exitStatus,mainUid):
  mainUid.pushNewAsset.setEnabled(True)


def rbhusAssImport(mainUid):
  global rbhusPipeAssetImportCmd
  p = QtCore.QProcess(parent=mainUid)
  p.setStandardOutputFile(tempDir + os.sep + "rbhusPipeAssetImport_" + username + ".log")
  p.setStandardErrorFile(tempDir + os.sep + "rbhusPipeAssetImport_" + username + ".err")
  mainUid.pushAssImport.setEnabled(False)
  rbhusPipeAssetImportCmdExe = rbhusPipeAssetImportCmd +" "+ os.environ['rp_proj_projName']
  p.start(sys.executable, rbhusPipeAssetImportCmdExe.split())
  p.finished.connect(lambda exitstatus,test, mainUid=mainUid: rbhusPipeAssImportEnable(mainUid))


def rbhusPipeAssImportEnable(mainUid):
  mainUid.pushAssImport.setEnabled(True)


def setUsers(mainUid):
  users = rbhus.utilsPipe.getUsers()
  outUsers = subprocess.Popen([sys.executable,selectRadioBoxCmd,"-i",",".join(users),"-d",str(mainUid.lineEditSearch.text()).rstrip().lstrip()],stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].rstrip().lstrip()
  # if(outUsers == ""):
  #   outUsers = str(self.lineEditSearch.text()).rstrip().lstrip()
  mainUid.lineEditSearch.setText(outUsers)



def saveSearchItem(mainUid,filterFile=None):
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
  isStarred = str(mainUid.radioStarred.isChecked())
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
    mainUid.radioStarred.setChecked(True)
  else:
    mainUid.radioStarred.setChecked(False)



  if(s[13] == "True"):
    mainUid.checkAssPath.setChecked(True)
  else:
    mainUid.checkAssPath.setChecked(False)
  updateAssetsForProjSelect(mainUid)


def saveSelectedProjects(project):
  projFile = open(os.path.join(home_dir,".projSet.default"),"w")
  simplejson.dump(project,projFile)
  projFile.flush()
  projFile.close()


def loadDefaultProject(mainUid):

  projFile = os.path.join(home_dir, ".projSet.default")
  if(os.path.exists(projFile)):
    pfd = open(projFile, "r")
    projectSelected = simplejson.load(pfd)
    pfd.close()
    rbhus.debug.debug(projectSelected)
    if(projectSelected):
      totalItems = mainUid.listWidgetProj.count()
      for x in range(0,totalItems):
        if(mainUid.listWidgetProj.item(x).text() in projectSelected):
          mainUid.listWidgetProj.setCurrentItem(mainUid.listWidgetProj.item(x))



def run_api(mainUid,inputDict):
  inputs = simplejson.loads(inputDict)
  temp_project = inputs['project']
  # old_project = self.set_project
  temp_asset = inputs['asset']
  temp_run = inputs['run']
  # if(temp_project != self.set_project):
  #   rbhusPipeSetProject_temp(temp_project)
  if(temp_run == rbhus.constantsPipe.run_api_cmd_review):
    reviewAss(mainUid,assetList= temp_asset)
  # if (temp_project != self.set_project):
  #   rbhusPipeSetProject_temp(old_project)

def updateProjectsLists(mainUid):
  mainUid.listWidgetProj.clear()
  dbcon = rbhus.dbPipe.dbPipe()
  projects = dbcon.execute("select projName from proj where status=\""+ str(rbhus.constantsPipe.projActive) +"\"",dictionary=True)
  maxlen = 0
  for x in projects:
    item = QtWidgets.QListWidgetItem()
    item.setText(x['projName'])
    mylen = len(x['projName'])
    if(mylen >= maxlen):
      maxlen = mylen
    mainUid.listWidgetProj.addItem(item)
  loadDefaultProject(mainUid)
  changeProject(mainUid)
  return(maxlen)


def main_func(mainUid):
  mainUid.listWidgetProj.clear()

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




  mainUid.pushNewAsset.setIcon(iconNewAsset)

  mainUid.pushAssImport.setIcon(iconImportAsset)

  mainUid.pushRefresh.setIcon(iconRefresh)
  mainUid.pushRefreshMedia.setIcon(iconRefresh)
  mainUid.pushRefreshMediaThumbz.setIcon(iconRefresh)
  mainUid.pushRefreshFilters.setIcon(iconRefresh)
  mainUid.pushRefreshProjects.setIcon(iconRefresh)
  mainUid.pushSaveFilters.setIcon(iconNew)
  mainUid.radioStarred.setStyleSheet(rbhusUI.lib.qt5.customWidgets.checkBox_style.styleStarRadioButton)
  mainUid.radioAsc.setStyleSheet(rbhusUI.lib.qt5.customWidgets.checkBox_style.styleSortCheckBox)







  # mainUid.listWidgetProj.itemSelectionChanged.connect(lambda mainUid=mainUid : changeProject(mainUid))
  mainUid.listWidgetProj.itemClicked.connect(lambda iotem ,mainUid=mainUid : changeProject(mainUid))
  maxlen = updateProjectsLists(mainUid)


  # mainUid.listWidgetProj.setSortingEnabled(True)
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




  mainUid.checkTag.clicked.connect(lambda clicked, mainUid=mainUid: updateAssetsForProjSelect(mainUid))
  mainUid.checkAssName.clicked.connect(lambda clicked, mainUid=mainUid: updateAssetsForProjSelect(mainUid))
  mainUid.checkAssPath.clicked.connect(lambda clicked, mainUid=mainUid: updateAssetsForProjSelect(mainUid))

  mainUid.checkUsers.clicked.connect(lambda clicked, mainUid=mainUid: setUsers(mainUid))

  mainUid.lineEditSearch.textChanged.connect(lambda textChanged, mainUid=mainUid: updateAssetsForProjSelect(mainUid))



  mainUid.pushRefresh.clicked.connect(lambda clicked, mainUid=mainUid: pushRefresh(mainUid))
  mainUid.pushRefreshMedia.clicked.connect(lambda clicked, mainUid=mainUid: detailsPanelThread(mainUid))
  mainUid.pushRefreshMediaThumbz.clicked.connect(lambda clicked, mainUid=mainUid: detailsPanelMediaThread(mainUid))
  mainUid.pushRefreshProjects.clicked.connect(lambda clicked, mainUid=mainUid: updateProjectsLists(mainUid))
  mainUid.pushRefreshFilters.clicked.connect(lambda clicked, mainUid=mainUid: refreshFilter(mainUid))

  mainUid.radioMineAss.clicked.connect(lambda clicked, mainUid=mainUid: updateAssetsForProjSelect(mainUid))
  mainUid.radioAllAss.clicked.connect(lambda clicked, mainUid=mainUid: updateAssetsForProjSelect(mainUid))
  mainUid.radioStarred.clicked.connect(lambda clicked, mainUid=mainUid: updateAssetsForProjSelect(mainUid))




  mainUid.pushSaveFilters.clicked.connect(lambda clicked,mainUid=mainUid: saveSearchItem(mainUid))

  mainUid.listWidgetSearch.itemChanged.connect(lambda item,mainUid=mainUid: searchItemChanged(mainUid,item))
  loadSearch(mainUid)

  mainUid.listWidgetSearch.customContextMenuRequested.connect(lambda pos, mainUid=mainUid: popUpSearchFav(mainUid, pos))


  updateAssTimer.timeout.connect(lambda mainUid=mainUid: updateAssetsForProjSelectTimed(mainUid))
  updateSortingTimer.timeout.connect(lambda mainUid=mainUid: updateSortingTimed(mainUid))
  updateMediaTabTimer.timeout.connect(lambda mainUid=mainUid: updateMediaTabTimed(mainUid))


  mainUid.comboSeq.editTextChanged.connect(lambda textChanged, mainUid=mainUid: setScene(mainUid))
  mainUid.comboSeq.editTextChanged.connect(lambda textChanged, mainUid=mainUid: updateAssetsSeq(mainUid))
  mainUid.comboStage.editTextChanged.connect(lambda textChanged, mainUid=mainUid: updateAssetsForProjSelect(mainUid))
  mainUid.comboNode.editTextChanged.connect(lambda textChanged, mainUid=mainUid: updateAssetsForProjSelect(mainUid))
  mainUid.comboFile.editTextChanged.connect(lambda textChanged, mainUid=mainUid: updateAssetsForProjSelect(mainUid))
  mainUid.comboScn.editTextChanged.connect(lambda textChanged, mainUid=mainUid: updateAssetsForProjSelect(mainUid))
  mainUid.comboAssType.editTextChanged.connect(lambda textChanged, mainUid=mainUid: updateAssetsForProjSelect(mainUid))

  mainUid.listWidgetAssets.customContextMenuRequested.connect(lambda pos, mainUid=mainUid: popupAss(mainUid, pos))


  mainUid.pushAssImport.clicked.connect(lambda clicked, mainUid=mainUid: rbhusAssImport(mainUid))
  mainUid.pushNewAsset.clicked.connect(lambda clicked, mainUid=mainUid: rbhusPipeAssetCreate(mainUid))
  mainUid.actionNew_seq_scn.triggered.connect(lambda clicked, mainUid=mainUid: rbhusPipeSeqSceCreate(mainUid))
  mainUid.actionEdit_seq_scn.triggered.connect(lambda clicked, mainUid=mainUid: rbhusPipeSeqSceEdit(mainUid))

  mainUid.radioAsc.clicked.connect(lambda clicked, mainUid=mainUid: updateSorting(mainUid))
  mainUid.comboBoxSort.currentTextChanged.connect(lambda textChanged, mainUid=mainUid: updateSorting(mainUid))

  mainUid.listWidgetAssets.itemSelectionChanged.connect(lambda mainUid=mainUid: detailsPanelThread(mainUid))
  mainUid.listWidgetSubDir.itemSelectionChanged.connect(lambda mainUid=mainUid: detailsPanelMediaThread(mainUid))
  # mainUid.listWidgetMedia.itemSelectionChanged.connect(lambda mainUid=mainUid: selectedMedia(mainUid))
  mainUid.tabWidget.currentChanged.connect(lambda index,mainUid=mainUid: updateMediaTab(mainUid))

  loadDefaultProject(mainUid)

  mainUid.splitter.setStretchFactor(0,10)
  # mainUid.splitterAssetDetails.setStretchFactor(0,0.75)
  # mainUid.splitterAssetDetails.setStretchFactor(2,0.25)
  mainUid.splitterAssetDetails.setSizes((1000,50))
  mainUid.splitterMedia.setSizes((1,200))

  mainUid.groupBoxShowOnly.hide()

  # mainUid.groupBoxUpdates.hide()

  api = api_serv(mainUid)
  api.msg_recved.connect(lambda inputDict,mainUid=mainUid :run_api(mainUid,inputDict))
  api.start()


app = None


if __name__ == '__main__':
  global app
  app = QtWidgets.QApplication(sys.argv)
  mainUid = uic.loadUi(ui_main)
  main_func(mainUid)
  os._exit((app.exec_()))
