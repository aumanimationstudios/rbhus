#!/usr/bin/env python2
#!/usr/bin/python -m pdb
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
import rbhusUI.lib.qt5.customWidgets.checkBox_favorite
import rbhus.pyperclip
import rbhus.hgmod
import time

from PyQt5 import QtWidgets, QtGui, QtCore, uic

projects = []

ui_main = os.path.join(ui_dir,"ui_main.ui")

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
rbhusPipeAssetImportCmd = os.path.join(file_dir, assImporter)
selectRadioBoxCmd = os.path.join(file_dir, srb)


updateAssThreads = []
updateAssThreadsFav = []

assColumnList = ['','asset','assigned','reviewer','modified','v','review','publish','']

try:
  username = os.environ['rbhusPipe_acl_user'].rstrip().lstrip()
except:
  pass

favLock = QtCore.QReadWriteLock()
updateAssTimer = QtCore.QTimer()
updateAssFavTimer = QtCore.QTimer()


class QTableWidgetItemSort(QtWidgets.QTableWidgetItem):

    def __lt__(self, other):
        return self.data(QtCore.Qt.UserRole) < other.data(QtCore.Qt.UserRole)

    def __ge__(self, other):
        return self.data(QtCore.Qt.UserRole) > other.data(QtCore.Qt.UserRole)



class ImageWidget(QtWidgets.QPushButton):
  def __init__(self, imagePath, imageSize, parent=None):
    super(ImageWidget, self).__init__(parent)
    self.imagePath = imagePath
    self.picture = QtGui.QPixmap(imagePath)
    self.picture  = self.picture.scaledToHeight(imageSize,0)

  def paintEvent(self, event):
    painter = QtGui.QPainter(self)
    painter.setPen(QtCore.Qt.NoPen)
    painter.drawPixmap(0, 0, self.picture)

  def sizeHint(self):
    return(self.picture.size())




class updateAssQthreadFav(QtCore.QThread):
  assSignal = QtCore.pyqtSignal(str,str,object,int)
  progressSignal = QtCore.pyqtSignal(int,int,int)
  totalAssets = QtCore.pyqtSignal(int)

  def __init__(self, projects, parent=None):
    super(updateAssQthreadFav, self).__init__(parent)
    self.projSelected = copy.copy(projects)
    self.dbcon = rbhus.dbPipe.dbPipe()
    self.pleaseStop = False


  def exitshit(self):
    self.pleaseStop = True

  def run(self):
    if(self.projSelected):
      rbhus.debug.debug("started thread")
      assesUnsorted = []
      for x in self.projSelected:
        assesForProj = getAllFavorite(x)
        if(assesForProj):
          for ass in assesForProj:
            assdets = rbhus.utilsPipe.getAssDetails(assPath=ass)
            assesUnsorted.append(assdets)

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
            textAss = x['path']
            absPathAss = rbhus.utilsPipe.getAbsPath(x['path'])
            x['fav']  = isFavorite(x['path'])
            x['absPath'] = absPathAss
            if (sys.platform.find("linux") >= 0):
              try:
                x['modified'] = time.strftime("%Y/%m/%d # %I:%M %p", time.localtime(os.path.getctime(absPathAss)))
              except:
                x['modified'] = "not found"
            elif (sys.platform.find("win") >= 0):
              try:
                x['modified'] = time.strftime("%Y/%m/%d # %I:%M %p", time.localtime(os.path.getmtime(absPathAss)))
              except:
                x['modified'] = "not found"

            x['preview_low'] = os.path.join(absPathAss,'preview_low.png')
            x['preview'] = os.path.join(absPathAss, 'preview.png')
            if(not os.path.exists(x['preview_low'])):
              x['preview_low'] = None



            self.assSignal.emit(textAss,richAss,x,current-1)
            self.progressSignal.emit(minLength,maxLength,current)
            time.sleep(0.02)
          else:
            rbhus.debug.info("STOPPING THREAD")
            break
      else:
        minLength = 0
        maxLength = 1
        current = 1
        self.totalAssets.emit(0)
        self.progressSignal.emit(minLength, maxLength, current)
    self.finished.emit()



class updateAssQthread(QtCore.QThread):
  assSignal = QtCore.pyqtSignal(str,str,object,int)
  progressSignal = QtCore.pyqtSignal(int,int,int)
  totalAssets = QtCore.pyqtSignal(int)

  def __init__(self,project,whereDict,parent=None):
    super(updateAssQthread, self).__init__(parent)
    self.projSelected = copy.copy(project)
    self.dbcon = rbhus.dbPipe.dbPipe()
    self.whereDict = whereDict
    self.pleaseStop = False

  def exitshit(self):
    self.pleaseStop = True

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
            if(len(self.projSelected) > 1):
              for fc in asset.split(":"):
                textAssArr.append('<font color="' + fc.split("#")[1] + '">' + fc.split("#")[0] + '</font>')
            else:
              for fc in asset.split(":")[1:]:
                textAssArr.append('<font color="' + fc.split("#")[1] + '">' + fc.split("#")[0] + '</font>')
            richAss = " " + "<b><i> : </i></b>".join(textAssArr)
            textAss = x['path']
            absPathAss = rbhus.utilsPipe.getAbsPath(x['path'])
            x['fav']  = isFavorite(x['path'])
            x['absPath'] = absPathAss
            if (sys.platform.find("linux") >= 0):
              try:
                x['modified'] = time.strftime("%Y/%m/%d # %I:%M %p", time.localtime(os.path.getctime(absPathAss)))
              except:
                x['modified'] = "not found"
            elif (sys.platform.find("win") >= 0):
              try:
                x['modified'] = time.strftime("%Y/%m/%d # %I:%M %p", time.localtime(os.path.getmtime(absPathAss)))
              except:
                x['modified'] = "not found"

            x['preview_low'] = os.path.join(absPathAss,'preview_low.png')
            x['preview'] = os.path.join(absPathAss, 'preview.png')
            if(not os.path.exists(x['preview_low'])):
              x['preview_low'] = None



            self.assSignal.emit(textAss,richAss,x,current-1)
            self.progressSignal.emit(minLength,maxLength,current)
            time.sleep(0.015)
          else:
            rbhus.debug.info("STOPPING THREAD")
            break
      else:
        minLength = 0
        maxLength = 1
        current = 1
        self.totalAssets.emit(0)
        self.progressSignal.emit(minLength, maxLength, current)
    self.finished.emit()



def updateFavorite(mainUid,assPath,starObj):
  proj = assPath.split(":")[0]

  fav_file = os.path.join(home_dir,".rbhusPipe__"+ str(proj) +".fav")
  fav_asses = []
  if(os.path.exists(fav_file)):
    favLock.lockForRead()
    fd = open(fav_file,"r")
    try:
      fav_asses = simplejson.load(fd)
    except:
      rbhus.debug.warning(sys.exc_info())
    fd.close()
    favLock.unlock()
  if(not starObj.isChecked()):
    if(assPath in fav_asses):
      try:
        fav_asses.remove(assPath)
      except:
        rbhus.debug.warning(sys.exc_info())
    else:
      return
  else:
    if(assPath not in fav_asses):
      fav_asses.append(assPath)
    else:
      return
  favLock.lockForWrite()
  fd = open(fav_file,"w")
  try:
    simplejson.dump(fav_asses,fd)
  except:
    rbhus.debug.warning(sys.exc_info())
  fd.flush()
  fd.close()
  favLock.unlock()
  updateAssetsForProjSelectFav(mainUid)


def isFavorite(assPath):
  proj = assPath.split(":")[0]
  fav_file = os.path.join(home_dir, ".rbhusPipe__" + str(proj) + ".fav")
  fav_asses = []
  if (os.path.exists(fav_file)):
    favLock.lockForRead()
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
    favLock.lockForRead()
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
  updateAssetsForProjSelectFav(mainUid)


def pushRefresh(mainUid):
  # updateProjSelect(mainUid)
  updateAssetsForProjSelect(mainUid)


def pushRefreshFav(mainUid):
  # updateProjSelect(mainUid)
  updateAssetsForProjSelectFav(mainUid)




def updateProjSelect(mainUid):
  global projects
  items = mainUid.listWidgetProj.selectedItems()

  projects = []
  for x in items:
    projects.append(str(x.text()))
  saveSelectedProjects(projects)





def updateAssetsForProjSelectFav(mainUid):
  updateAssFavTimer.stop()
  updateAssFavTimer.start(500)



def updateAssetsForProjSelectFavTimed(mainUid):
  updateAssFavTimer.stop()
  global updateAssThreadsFav
  global projects

  if(updateAssThreadsFav):
    for runingThread in updateAssThreadsFav:
      try:
        runingThread.disconnect()
      except:
        rbhus.debug.info(sys.exc_info())
      # try:
      #   runingThread.progressSignal.disconnect()
      # except:
      #   pass
      # try:
      #   runingThread.totalAssets.disconnect()
      # except:
      #   pass
      runingThread.exitshit()
      updateAssThreadsFav.remove(runingThread)

  updateAssThread = updateAssQthreadFav(projects,parent=mainUid)
  updateAssThread.totalAssets.connect(lambda total,mainUid=mainUid: updateTotalAssFav(mainUid,total))
  updateAssThread.assSignal.connect(lambda textAss,richAss,assetDets, current, mainUid=mainUid: updateAssSlotFav(mainUid, textAss, richAss,assetDets,current))
  updateAssThread.progressSignal.connect(lambda minLength, maxLength , current, mainUid = mainUid: updateProgressBarFav(minLength,maxLength,current,mainUid))
  updateAssThread.start()
  updateAssThreadsFav.append(updateAssThread)




def updateAssetsForProjSelect(mainUid):
  updateAssTimer.stop()
  updateAssTimer.start(1000)


def updateAssetsForProjSelectTimed(mainUid):
  updateAssTimer.stop()
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
      try:
        runingThread.disconnect()
      except:
        rbhus.debug.info(runingThread)
      # try:
      #   runingThread.progressSignal.disconnect()
      # except:
      #   pass
      # try:
      #   runingThread.totalAssets.disconnect()
      # except:
      #   pass
      runingThread.exitshit()
      updateAssThreads.remove(runingThread)

  updateAssThread = updateAssQthread(project = projects,whereDict=whereDict,parent=mainUid)
  updateAssThread.totalAssets.connect(lambda total,mainUid=mainUid: updateTotalAss(mainUid,total))
  updateAssThread.progressSignal.connect(lambda minLength, maxLength , current, mainUid = mainUid: updateProgressBar(minLength,maxLength,current,mainUid))
  updateAssThread.assSignal.connect(lambda textAss,richAss,assetDets, current, mainUid=mainUid: updateAssSlot(mainUid, textAss, richAss,assetDets,current))
  updateAssThread.start()
  updateAssThreads.append(updateAssThread)

  # for x in runingThreads:
  #   try:
  #     x.exitshit()
  #   except:
  #     rbhus.debug.warning(sys.exc_info())
  #   try:
  #     runingThreads.remove(x)
  #   except:
  #     rbhus.debug.warning(sys.exc_info())



def updateProgressBar(minLength,maxLength,current,mainUid):
  mainUid.progressBar.setMinimum(minLength)
  mainUid.progressBar.setMaximum(maxLength)
  mainUid.progressBar.setValue(current)


def updateProgressBarFav(minLength,maxLength,current,mainUid):
  mainUid.progressBarFav.setMinimum(minLength)
  mainUid.progressBarFav.setMaximum(maxLength)
  mainUid.progressBarFav.setValue(current)





def updateProgressBarFav(minLength,maxLength,current,mainUid):
  mainUid.progressBarFav.setMinimum(minLength)
  mainUid.progressBarFav.setMaximum(maxLength)
  mainUid.progressBarFav.setValue(current)




def updateTotalAss(mainUid,totalRows):
  # global assColumnList
  mainUid.labelTotal.setText(str(totalRows))
  # try:
  #   mainUid.tableWidgetAssets.disconnect()
  # except:
  #   pass

  # mainUid.tableWidgetAssets.clearContents()
  mainUid.tableWidgetAssets.setSortingEnabled(False)
  mainUid.tableWidgetAssets.clear()
  mainUid.tableWidgetAssets.setRowCount(totalRows)
  mainUid.tableWidgetAssets.setColumnCount(9)
  # mainUid.tableWidgetAssets.customContextMenuRequested.connect(lambda pos,mainUid=mainUid: popupAss(mainUid,pos))


  cn = 0
  for x in assColumnList:
    itemcn = QtWidgets.QTableWidgetItem()
    itemcn.setText(x)
    mainUid.tableWidgetAssets.setHorizontalHeaderItem(cn, itemcn)
    cn += 1


def updateTotalAssFav(mainUid,totalRows):
  # global assColumnList
  mainUid.labelTotalFav.setText(str(totalRows))
  # try:
  #   mainUid.tableWidgetAssetsFav.disconnect()
  # except:
  #   pass
  # mainUid.tableWidgetAssetsFav.clearContents()
  mainUid.tableWidgetAssetsFav.setSortingEnabled(False)
  mainUid.tableWidgetAssetsFav.clear()
  mainUid.tableWidgetAssetsFav.setRowCount(totalRows)
  mainUid.tableWidgetAssetsFav.setColumnCount(9)
  # mainUid.tableWidgetAssetsFav.customContextMenuRequested.connect(lambda pos,mainUid=mainUid: popupAss(mainUid,pos))


  cn = 0
  for x in assColumnList:
    itemcn = QtWidgets.QTableWidgetItem()
    itemcn.setText(x)
    mainUid.tableWidgetAssetsFav.setHorizontalHeaderItem(cn, itemcn)
    cn += 1





def updateAssSlot(mainUid, textAss,richAss,assetDets,currentRow):
  fav = rbhusUI.lib.qt5.customWidgets.checkBox_favorite.checkBox()
  fav.assetDets = assetDets
  fav.setParent(mainUid)
  fav.clicked.connect(lambda clicked,assPath=assetDets['path'], starObj = fav, mainUid=mainUid : updateFavorite(mainUid,assPath,starObj))

  if(assetDets['fav']):
    fav.setChecked(True)

  labelAss = QtWidgets.QLabel()
  labelAss.setTextFormat(QtCore.Qt.RichText)
  labelAss.setText(richAss)
  labelAss.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
  labelAss.setParent(mainUid)

  # itemAssPath = QTableWidgetItemSort()
  # itemAssPath.setData(QtCore.Qt.UserRole,assetDets['path'])
  # itemAssPath.setFlags(QtCore.Qt.NoItemFlags)

  itemModified = QtWidgets.QTableWidgetItem()
  itemModified.setText(assetDets['modified'])

  itemAssigned = QtWidgets.QTableWidgetItem()
  itemAssigned.setText(assetDets['assignedWorker'])
  # itemAssigned.setTextAlignment(QtCore.Qt.AlignCenter)

  itemReviewer = QtWidgets.QTableWidgetItem()
  itemReviewer.setText(assetDets['reviewUser'])
  # itemReviewer.setTextAlignment(QtCore.Qt.AlignCenter)

  itemVersion = QtWidgets.QTableWidgetItem()
  if (not assetDets['versioning']):
    brush1 = QtGui.QBrush()
    brush1.setColor(QtGui.QColor(250, 100, 100))
    brush1.setStyle(QtCore.Qt.SolidPattern)
    # itemVersion.setText("")
    # itemReviewStatus.setText("notDone")
    itemVersion.setBackground(brush1)
  else:
    brush1 = QtGui.QBrush()
    brush1.setColor(QtGui.QColor(0, 150, 100))
    brush1.setStyle(QtCore.Qt.SolidPattern)
    # itemVersion.setText(str(assetDets['reviewVersion']))
    itemVersion.setTextAlignment(QtCore.Qt.AlignCenter)
    # itemReviewStatus.setText("inProgress : " + str(assetDets['reviewVersion']))
    itemVersion.setBackground(brush1)

  itemReviewStatus = QtWidgets.QTableWidgetItem()
  if (assetDets['reviewStatus'] == rbhus.constantsPipe.reviewStatusNotDone):
    brush1 = QtGui.QBrush()
    brush1.setColor(QtGui.QColor(250, 100, 100))
    brush1.setStyle(QtCore.Qt.SolidPattern)
    itemReviewStatus.setText("")
    # itemReviewStatus.setText("notDone")
    itemReviewStatus.setBackground(brush1)
  elif (assetDets['reviewStatus'] == rbhus.constantsPipe.reviewStatusInProgress):
    brush1 = QtGui.QBrush()
    brush1.setColor(QtGui.QColor(0, 150, 250))
    brush1.setStyle(QtCore.Qt.SolidPattern)
    itemReviewStatus.setText(str(assetDets['reviewVersion']))
    itemReviewStatus.setTextAlignment(QtCore.Qt.AlignCenter)
    # itemReviewStatus.setText("inProgress : " + str(assetDets['reviewVersion']))
    itemReviewStatus.setBackground(brush1)
  else:
    brush1 = QtGui.QBrush()
    brush1.setColor(QtGui.QColor(0, 150, 100))
    brush1.setStyle(QtCore.Qt.SolidPattern)
    itemReviewStatus.setText(str(assetDets['reviewVersion']))
    itemReviewStatus.setTextAlignment(QtCore.Qt.AlignCenter)
    itemReviewStatus.setBackground(brush1)

  itemPublished = QtWidgets.QTableWidgetItem()
  if (assetDets['publishVersion']):
    brush1 = QtGui.QBrush()
    brush1.setColor(QtGui.QColor(0, 150, 100))
    brush1.setStyle(QtCore.Qt.SolidPattern)
    itemPublished.setText(str(assetDets['publishVersion']))
    itemPublished.setTextAlignment(QtCore.Qt.AlignCenter)
    # itemReviewStatus.setText("notDone")
    itemPublished.setBackground(brush1)
    if(assetDets['reviewVersion']):
      if(assetDets['publishVersion'] != assetDets['reviewVersion']):
        brush1 = QtGui.QBrush()
        brush1.setColor(QtGui.QColor(255,192,203))
        brush1.setStyle(QtCore.Qt.SolidPattern)
        itemPublished.setText(str(assetDets['publishVersion']))
        itemPublished.setTextAlignment(QtCore.Qt.AlignCenter)
        # itemReviewStatus.setText("notDone")
        itemPublished.setBackground(brush1)
  else:
    brush1 = QtGui.QBrush()
    brush1.setColor(QtGui.QColor(250, 100, 100))
    brush1.setStyle(QtCore.Qt.SolidPattern)
    itemPublished.setText("")
    itemPublished.setTextAlignment(QtCore.Qt.AlignCenter)
    itemPublished.setBackground(brush1)

  if(assetDets['preview_low']):
    # previewWidget = ImageWidget(assetDets['preview_low'],48)
    previewWidget = ImageWidget(assetDets['preview_low'],48,parent=mainUid)
    previewWidget.clicked.connect(lambda x, imagePath = assetDets['preview']: imageWidgetClicked(imagePath))
  else:
    previewWidget = None



  mainUid.tableWidgetAssets.setCellWidget(currentRow,0,fav)
  # mainUid.tableWidgetAssets.setItem(currentRow, 1, itemAssPath)
  mainUid.tableWidgetAssets.setCellWidget(currentRow, 1, labelAss)

  mainUid.tableWidgetAssets.setItem(currentRow, 2, itemAssigned)
  mainUid.tableWidgetAssets.setItem(currentRow, 3, itemReviewer)
  mainUid.tableWidgetAssets.setItem(currentRow, 4, itemModified)
  mainUid.tableWidgetAssets.setItem(currentRow, 5, itemVersion)
  mainUid.tableWidgetAssets.setItem(currentRow, 6, itemReviewStatus)
  mainUid.tableWidgetAssets.setItem(currentRow, 7, itemPublished)

  if(previewWidget):
    mainUid.tableWidgetAssets.setCellWidget(currentRow, 8, previewWidget)

  mainUid.tableWidgetAssets.resizeColumnsToContents()
  # mainUid.tableWidgetAssets.setItemWidget(item, label)


def updateAssSlotFav(mainUid, textAss,richAss,assetDets,currentRow):
  fav = rbhusUI.lib.qt5.customWidgets.checkBox_favorite.checkBox()
  fav.assetDets = assetDets
  fav.setParent(mainUid.tableWidgetAssetsFav)
  fav.clicked.connect(lambda clicked,assPath=assetDets['path'], starObj = fav, mainUid=mainUid : updateFavorite(mainUid,assPath,starObj))

  if(assetDets['fav']):
    fav.setChecked(True)

  labelAss = QtWidgets.QLabel()
  labelAss.setTextFormat(QtCore.Qt.RichText)
  labelAss.setText(richAss)
  labelAss.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
  labelAss.setParent(mainUid)

  itemModified = QtWidgets.QTableWidgetItem()
  itemModified.setText(assetDets['modified'])

  itemAssigned = QtWidgets.QTableWidgetItem()
  itemAssigned.setText(assetDets['assignedWorker'])
  # itemAssigned.setTextAlignment(QtCore.Qt.AlignCenter)

  itemReviewer = QtWidgets.QTableWidgetItem()
  itemReviewer.setText(assetDets['reviewUser'])
  # itemReviewer.setTextAlignment(QtCore.Qt.AlignCenter)

  itemVersion = QtWidgets.QTableWidgetItem()
  if (not assetDets['versioning']):
    brush1 = QtGui.QBrush()
    brush1.setColor(QtGui.QColor(250, 100, 100))
    brush1.setStyle(QtCore.Qt.SolidPattern)
    # itemVersion.setText("")
    # itemReviewStatus.setText("notDone")
    itemVersion.setBackground(brush1)
  else:
    brush1 = QtGui.QBrush()
    brush1.setColor(QtGui.QColor(0, 150, 100))
    brush1.setStyle(QtCore.Qt.SolidPattern)
    # itemVersion.setText(str(assetDets['reviewVersion']))
    itemVersion.setTextAlignment(QtCore.Qt.AlignCenter)
    # itemReviewStatus.setText("inProgress : " + str(assetDets['reviewVersion']))
    itemVersion.setBackground(brush1)

  itemReviewStatus = QtWidgets.QTableWidgetItem()
  if (assetDets['reviewStatus'] == rbhus.constantsPipe.reviewStatusNotDone):
    brush1 = QtGui.QBrush()
    brush1.setColor(QtGui.QColor(250, 100, 100))
    brush1.setStyle(QtCore.Qt.SolidPattern)
    itemReviewStatus.setText("")
    # itemReviewStatus.setText("notDone")
    itemReviewStatus.setBackground(brush1)
  elif (assetDets['reviewStatus'] == rbhus.constantsPipe.reviewStatusInProgress):
    brush1 = QtGui.QBrush()
    brush1.setColor(QtGui.QColor(0, 150, 250))
    brush1.setStyle(QtCore.Qt.SolidPattern)
    itemReviewStatus.setText(str(assetDets['reviewVersion']))
    itemReviewStatus.setTextAlignment(QtCore.Qt.AlignCenter)
    # itemReviewStatus.setText("inProgress : " + str(assetDets['reviewVersion']))
    itemReviewStatus.setBackground(brush1)
  else:
    brush1 = QtGui.QBrush()
    brush1.setColor(QtGui.QColor(0, 150, 100))
    brush1.setStyle(QtCore.Qt.SolidPattern)
    itemReviewStatus.setText(str(assetDets['reviewVersion']))
    itemReviewStatus.setTextAlignment(QtCore.Qt.AlignCenter)
    itemReviewStatus.setBackground(brush1)

  itemPublished = QtWidgets.QTableWidgetItem()
  if (assetDets['publishVersion']):
    brush1 = QtGui.QBrush()
    brush1.setColor(QtGui.QColor(0, 150, 100))
    brush1.setStyle(QtCore.Qt.SolidPattern)
    itemPublished.setText(str(assetDets['publishVersion']))
    itemPublished.setTextAlignment(QtCore.Qt.AlignCenter)
    # itemReviewStatus.setText("notDone")
    itemPublished.setBackground(brush1)
    if(assetDets['reviewVersion']):
      if(assetDets['publishVersion'] != assetDets['reviewVersion']):
        brush1 = QtGui.QBrush()
        brush1.setColor(QtGui.QColor(255,192,203))
        brush1.setStyle(QtCore.Qt.SolidPattern)
        itemPublished.setText(str(assetDets['publishVersion']))
        itemPublished.setTextAlignment(QtCore.Qt.AlignCenter)
        # itemReviewStatus.setText("notDone")
        itemPublished.setBackground(brush1)
  else:
    brush1 = QtGui.QBrush()
    brush1.setColor(QtGui.QColor(250, 100, 100))
    brush1.setStyle(QtCore.Qt.SolidPattern)
    itemPublished.setText("")
    itemPublished.setTextAlignment(QtCore.Qt.AlignCenter)
    itemPublished.setBackground(brush1)

  if(assetDets['preview_low']):
    previewWidget = ImageWidget(assetDets['preview_low'],48,mainUid.tableWidgetAssetsFav)
    previewWidget.clicked.connect(lambda x, imagePath = assetDets['preview']: imageWidgetClicked(imagePath))
  else:
    previewWidget = None



  mainUid.tableWidgetAssetsFav.setCellWidget(currentRow,0,fav)
  mainUid.tableWidgetAssetsFav.setCellWidget(currentRow, 1, labelAss)
  mainUid.tableWidgetAssetsFav.setItem(currentRow, 2, itemAssigned)
  mainUid.tableWidgetAssetsFav.setItem(currentRow, 3, itemReviewer)
  mainUid.tableWidgetAssetsFav.setItem(currentRow, 4, itemModified)
  mainUid.tableWidgetAssetsFav.setItem(currentRow, 5, itemVersion)
  mainUid.tableWidgetAssetsFav.setItem(currentRow, 6, itemReviewStatus)
  mainUid.tableWidgetAssetsFav.setItem(currentRow, 7, itemPublished)

  if(previewWidget):
    mainUid.tableWidgetAssetsFav.setCellWidget(currentRow, 8, previewWidget)

  mainUid.tableWidgetAssetsFav.resizeColumnsToContents()
  # mainUid.tableWidgetAssets.setItemWidget(item, label)


def imageWidgetClicked(imagePath):
  import webbrowser
  webbrowser.open(imagePath)


def selectedAsses(mainUid,isFav=False):
  rowstask=[]
  rowsSelected = []
  if(isFav):
    rowsModel = mainUid.tableWidgetAssetsFav.selectionModel().selectedRows()
  else:
    rowsModel = mainUid.tableWidgetAssets.selectionModel().selectedRows()

  for idx in rowsModel:
    #debug.info(dir(idx.model()))
    rowsSelected.append(idx.row())
  for row in rowsSelected:
    try:
      if(isFav):
        rowstask.append(mainUid.tableWidgetAssetsFav.cellWidget(row,0).assetDets)
      else:
        rowstask.append(mainUid.tableWidgetAssets.cellWidget(row,0).assetDets)

    except:
      rbhus.debug.info(sys.exc_info())
  # rbhus.debug.info("1 : "+ str(rowstask))

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
  # rbhus.debug.info(textSelected)
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
  # try:
  #   mainUid.comboSeq.disconnect()
  # except:
  #   pass
  #
  # try:
  #   mainUid.comboSeq.disconnect()
  # except:
  #   pass
  #
  # try:
  #   mainUid.comboStage.disconnect()
  # except:
  #   pass
  #
  # try:
  #   mainUid.comboNode.disconnect()
  # except:
  #   pass
  #
  # try:
  #   mainUid.comboFile.disconnect()
  # except:
  #   pass
  #
  # try:
  #   mainUid.comboScn.disconnect()
  # except:
  #   pass
  #
  # try:
  #   mainUid.comboAssType.disconnect()
  # except:
  #   pass

  setStageTypes(mainUid)
  setNodeTypes(mainUid)
  setFileTypes(mainUid)
  setAssTypes(mainUid)
  setSequence(mainUid)
  setScene(mainUid)

  # mainUid.comboSeq.editTextChanged.connect(lambda textChanged, mainUid=mainUid: setScene(mainUid))
  # mainUid.comboSeq.editTextChanged.connect(lambda textChanged, mainUid=mainUid: updateAssetsSeq(mainUid))
  # mainUid.comboStage.editTextChanged.connect(lambda textChanged, mainUid=mainUid: updateAssetsForProjSelect(mainUid))
  # mainUid.comboNode.editTextChanged.connect(lambda textChanged, mainUid=mainUid: updateAssetsForProjSelect(mainUid))
  # mainUid.comboFile.editTextChanged.connect(lambda textChanged, mainUid=mainUid: updateAssetsForProjSelect(mainUid))
  # mainUid.comboScn.editTextChanged.connect(lambda textChanged, mainUid=mainUid: updateAssetsForProjSelect(mainUid))
  # mainUid.comboAssType.editTextChanged.connect(lambda textChanged, mainUid=mainUid: updateAssetsForProjSelect(mainUid))
  # updateAssetsForProjSelect(mainUid)



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

def popupAss(mainUid,pos,isFav=False):
  listAssesFull = selectedAsses(mainUid,isFav=isFav)
  listAsses = []
  for x in listAssesFull:
    if(x):
      listAsses.append(x)
  # rbhus.debug.info("selected asses : "+ str(len(listAsses)))
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
    action = menu.exec_(mainUid.tableWidgetAssets.mapToGlobal(pos))


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

  listedAss = listAsses[0]
  if(sys.platform.find("win") >= 0):
    subprocess.Popen([rbhusPipeReviewCmd,"--assetpath",listedAss['path']],shell = True)
  elif(sys.platform.find("linux") >= 0):
    subprocess.Popen(rbhusPipeReviewCmd +" --assetpath "+ listedAss['path'],shell = True)



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
        rbhus.debug.info(x)
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
      rbhus.debug.info(fila)
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
        rbhus.debug.info(fila)
        if(fila):
          rbhus.debug.info(str(fila[0]))
          filename = str(fila[0])
          rbhus.debug.info(filename.split("."))
          assdets = rbhus.utilsPipe.getAssDetails(assPath=x['path'])
          runCmd = rbhus.utilsPipe.openAssetCmd(assdets,filename)
          if(runCmd):
            runCmd = runCmd.rstrip().lstrip()
            if(sys.platform.find("win") >= 0):
              rbhus.debug.info(runCmd)
              subprocess.Popen(runCmd,shell=True)
            elif(sys.platform.find("linux") >= 0):
              rbhus.debug.info(runCmd)
              subprocess.Popen(runCmd,shell=True)
          else:
            import webbrowser
            webbrowser.open(filename)
      else:
        rbhus.debug.info("wtf : opening version cmd ")
        if(sys.platform.find("win") >= 0):
          subprocess.Popen([versionCmd,"--path",x['path']],shell = True)
        elif(sys.platform.find("linux") >= 0):
          subprocess.Popen(versionCmd +" --path "+ x['path'],shell = True)
  # self.centralwidget.setCursor(QtCore.Qt.ArrowCursor)
  for x in os.environ.keys():
    if(x.find("rp_") >= 0):
      rbhus.debug.info(x +" : "+os.environ[x])

def editAss(mainUid,assetList=None):
  if(assetList):
    listAssesFull = assetList
    listAsses = []
  for x in listAssesFull:
    listAsses.append(x['path'])
  if(listAsses):
    rbhusAssetEditCmdMod = rbhusPipeAssetEditCmd +" -p "+ ",".join(listAsses)
    rbhus.debug.info(rbhusAssetEditCmdMod)

    p = QtCore.QProcess(parent=mainUid)
    p.setStandardOutputFile(tempDir + os.sep + "rbhusPipeAssetEdit_" + username + ".log")
    p.setStandardErrorFile(tempDir + os.sep + "rbhusPipeAssetEdit_" + username + ".err")
    p.start(sys.executable, rbhusAssetEditCmdMod.split())
    p.finished.connect(lambda a ,b, mainUid=mainUid : updateAssetsForProjSelect(mainUid))



def setUsers(mainUid):
  users = rbhus.utilsPipe.getUsers()
  outUsers = subprocess.Popen([sys.executable,selectRadioBoxCmd,"-i",",".join(users),"-d",str(mainUid.lineEditSearch.text()).rstrip().lstrip()],stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].rstrip().lstrip()
  # if(outUsers == ""):
  #   outUsers = str(self.lineEditSearch.text()).rstrip().lstrip()
  mainUid.lineEditSearch.setText(outUsers)



def saveSearchItem(mainUid):
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
               isAssetPathSave


  isSaveStringPresent = searchItemPresent(saveString)


  if(not isSaveStringPresent):
    saveDict = {saveString:'name this'}
    searchItemSave(saveDict)
    item = QtWidgets.QListWidgetItem()
    item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled)
    item.setText(saveDict[saveString])
    item.assFilter = saveString
    mainUid.listWidgetSearch.addItem(item)

  testDict = searchItemLoad()
  rbhus.debug.info(testDict)

def searchItemPresent(assFilter):
  savedDict = searchItemLoad()
  if(savedDict):
    for x in savedDict:
      if(x):
        if(x.has_key(assFilter)):
          return(True)
  return(False)

def searchItemLoad():
  searchItems = None
  filterFile = os.path.join(home_dir,".rbhusPipe.filters")
  if(os.path.exists(filterFile)):
    fd = open(filterFile,"r")
    searchItems = yaml.safe_load(fd)
    fd.close()
  return (searchItems)



def loadSearch(mainUid):
  mainUid.listWidgetSearch.clear()
  saveSearchArray = searchItemLoad()
  for x in saveSearchArray:
    item = QtWidgets.QListWidgetItem()
    item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsEnabled)
    item.setText(x[x.keys()[-1]])
    item.assFilter = x.keys()[-1]
    mainUid.listWidgetSearch.addItem(item)


def searchItemSave(itemDict):
  searchItems = []
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
  rbhus.debug.info(item.text())
  rbhus.debug.info(item.assFilter)
  filterFile = os.path.join(home_dir, ".rbhusPipe.filters")

  savedDict = searchItemLoad()
  for x in savedDict:
    if(x):
      if(x.has_key(item.assFilter)):
        x[item.assFilter] = str(item.text())
  rbhus.debug.info(savedDict)
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
  rbhus.debug.info(item.assFilter)
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
    mainUid.checkAssPath.setChecked(True)
  else:
    mainUid.checkAssPath.setChecked(False)



def saveSelectedProjects(project):
  projFile = open(os.path.join(home_dir,".projSet.default"),"w")
  simplejson.dump(project,projFile)
  projFile.flush()
  projFile.close()


def loadDefaultProject(mainUid):

  projFile = os.path.join(home_dir, ".projSet.default")
  if(os.path.exists(projFile)):
    pfd = open(projFile, "r")
    totalItems = mainUid.listWidgetProj.count()
    projectSelected = simplejson.load(pfd)
    pfd.close()
    rbhus.debug.info(projectSelected)
    for x in range(0,totalItems):
      if(mainUid.listWidgetProj.item(x).text() in projectSelected):
        mainUid.listWidgetProj.setCurrentItem(mainUid.listWidgetProj.item(x))






def main():
  mainUid = uic.loadUi(ui_main)
  mainUid.listWidgetProj.clear()


  # importUid = uic.loadUi(ui_ass_for_import)

  iconRefresh = QtGui.QIcon()
  iconRefresh.addPixmap(QtGui.QPixmap(os.path.join(base_dir,"etc/icons/ic_action_refresh.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)

  iconNew = QtGui.QIcon()
  iconNew.addPixmap(QtGui.QPixmap(os.path.join(base_dir, "etc/icons/ic_action_new.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)

  mainUid.pushRefresh.setIcon(iconRefresh)
  mainUid.pushRefreshFav.setIcon(iconRefresh)
  mainUid.pushRefreshFilters.setIcon(iconRefresh)
  mainUid.pushSaveFilters.setIcon(iconNew)


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

  mainUid.listWidgetProj.itemSelectionChanged.connect(lambda mainUid=mainUid : changeProject(mainUid))
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




  mainUid.checkTag.clicked.connect(lambda clicked, mainUid=mainUid: updateAssetsForProjSelect(mainUid))
  mainUid.checkAssName.clicked.connect(lambda clicked, mainUid=mainUid: updateAssetsForProjSelect(mainUid))
  mainUid.checkAssPath.clicked.connect(lambda clicked, mainUid=mainUid: updateAssetsForProjSelect(mainUid))

  mainUid.checkUsers.clicked.connect(lambda clicked, mainUid=mainUid: setUsers(mainUid))

  mainUid.lineEditSearch.textChanged.connect(lambda textChanged, mainUid=mainUid: updateAssetsForProjSelect(mainUid))



  mainUid.pushRefresh.clicked.connect(lambda clicked, mainUid=mainUid: pushRefresh(mainUid))
  mainUid.pushRefreshFav.clicked.connect(lambda clicked, mainUid=mainUid: pushRefreshFav(mainUid))


  mainUid.pushRefreshFilters.clicked.connect(lambda clicked, mainUid=mainUid: refreshFilter(mainUid))

  mainUid.radioMineAss.clicked.connect(lambda clicked, mainUid=mainUid: updateAssetsForProjSelect(mainUid))
  mainUid.radioAllAss.clicked.connect(lambda clicked, mainUid=mainUid: updateAssetsForProjSelect(mainUid))

  mainUid.pushSaveFilters.clicked.connect(lambda clicked,mainUid=mainUid: saveSearchItem(mainUid))

  mainUid.listWidgetSearch.itemChanged.connect(lambda item,mainUid=mainUid: searchItemChanged(mainUid,item))
  loadSearch(mainUid)

  mainUid.listWidgetSearch.customContextMenuRequested.connect(lambda pos, mainUid=mainUid: popUpSearchFav(mainUid, pos))


  updateAssTimer.timeout.connect(lambda mainUid=mainUid: updateAssetsForProjSelectTimed(mainUid))
  updateAssFavTimer.timeout.connect(lambda mainUid=mainUid: updateAssetsForProjSelectFavTimed(mainUid))


  mainUid.comboSeq.editTextChanged.connect(lambda textChanged, mainUid=mainUid: setScene(mainUid))
  mainUid.comboSeq.editTextChanged.connect(lambda textChanged, mainUid=mainUid: updateAssetsSeq(mainUid))
  mainUid.comboStage.editTextChanged.connect(lambda textChanged, mainUid=mainUid: updateAssetsForProjSelect(mainUid))
  mainUid.comboNode.editTextChanged.connect(lambda textChanged, mainUid=mainUid: updateAssetsForProjSelect(mainUid))
  mainUid.comboFile.editTextChanged.connect(lambda textChanged, mainUid=mainUid: updateAssetsForProjSelect(mainUid))
  mainUid.comboScn.editTextChanged.connect(lambda textChanged, mainUid=mainUid: updateAssetsForProjSelect(mainUid))
  mainUid.comboAssType.editTextChanged.connect(lambda textChanged, mainUid=mainUid: updateAssetsForProjSelect(mainUid))

  mainUid.tableWidgetAssetsFav.customContextMenuRequested.connect(lambda pos, mainUid=mainUid,isFav = True: popupAss(mainUid, pos,isFav))
  mainUid.tableWidgetAssets.customContextMenuRequested.connect(lambda pos, mainUid=mainUid: popupAss(mainUid, pos))



  loadDefaultProject(mainUid)

  mainUid.splitter.setStretchFactor(0,10)








if __name__ == '__main__':
  app = QtWidgets.QApplication(sys.argv)
  main()
  os._exit((app.exec_()))