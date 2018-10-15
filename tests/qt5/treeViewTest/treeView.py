#!/usr/bin/env python2
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"




import argparse
import glob
import multiprocessing
import os
import subprocess
import sys
import time
import uuid

import setproctitle
import simplejson
import zmq

from PyQt5.QtWidgets import QApplication, QFileSystemModel, QListWidgetItem
from PyQt5 import QtCore, uic, QtGui, QtWidgets



# sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-1]))
progPath = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-3])
rbhusPath = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-4])


print(rbhusPath)


main_ui_file = os.path.join(rbhusPath, "tests", "qt5", "treeViewTest", "main.ui")

ROOTDIR = sys.argv[1]
CUR_ROOTDIR_POINTER = os.path.join(ROOTDIR,"-")

CUR_DIR_SELECTED = None

class FSM(QFileSystemModel):

  def __init__(self,**kwargs):
    super(FSM, self).__init__(**kwargs)
    self.fileDets = None



  def canFetchMore(self,idx):
    if (self.filePath(idx) == CUR_ROOTDIR_POINTER):
      rootIdx = self.index(ROOTDIR)
      return super(FSM, self).fetchMore(idx)
    elif (self.filePath(idx).endswith(".thumbz.db")):
      return False
    else:
      return super(FSM, self).canFetchMore(idx)

  # def rowCount(self,idx):
  #   rbhus.debug.info(idx.row())
  #   # return(idx.row() + 1)
  #   return super(FSM, self).rowCount(idx)

  def fetchMore(self,idx):
    if (self.filePath(idx) == CUR_ROOTDIR_POINTER):
      rootIdx = self.index(ROOTDIR)
      return super(FSM, self).fetchMore(idx)
    elif(self.filePath(idx).endswith(".thumbz.db")):
      return None
    else:
      return super(FSM, self).fetchMore(idx)

  def headerData(self,section,orientation,role):
    if(section == 0 and role == QtCore.Qt.DisplayRole):
      return "Folders"
    else:
      return super(FSM, self).headerData(section,orientation,role)

  def filePath(self, idx):
    rootIdx = self.index(CUR_ROOTDIR_POINTER)
    if(idx == rootIdx):
      return ROOTDIR
    else:
      return super(FSM, self).filePath(idx)



def dirSelected(idx, modelDirs, modelFiles, main_ui):
  global CUR_DIR_SELECTED
  pathSelected = modelDirs.filePath(idx)
  CUR_DIR_SELECTED = pathSelected
  print(pathSelected)
  modelFiles.setRootPath(CUR_DIR_SELECTED)
  modelFiles.setFilter(QtCore.QDir.Files | QtCore.QDir.NoDotAndDotDot)
  main_ui.treeFiles.setModel(modelFiles)
  rootIdx = modelFiles.index(CUR_DIR_SELECTED)
  main_ui.treeFiles.setRootIndex(rootIdx)












def mainGui(main_ui):
  modelDirs = FSM()
  modelDirs.setFilter(QtCore.QDir.Dirs | QtCore.QDir.NoDotAndDotDot)
  modelDirs.setRootPath(ROOTDIR)
  main_ui.treeDirs.setModel(modelDirs)
  rootIdx = modelDirs.index(ROOTDIR)
  main_ui.treeDirs.setRootIndex(rootIdx)

  modelDirs.mkdir(rootIdx, "-")
  curRootIdx = modelDirs.index(CUR_ROOTDIR_POINTER)
  main_ui.treeDirs.setCurrentIndex(curRootIdx)


  modelFiles = QFileSystemModel()
  modelFiles.setFilter(QtCore.QDir.Files | QtCore.QDir.NoDotAndDotDot)

  main_ui.treeDirs.clicked.connect(lambda idnx, modelDirs=modelDirs, modelFiles=modelFiles, main_ui=main_ui: dirSelected(idnx, modelDirs, modelFiles, main_ui))




  main_ui.show()








if __name__ == '__main__':
  app = QApplication(sys.argv)
  main_ui = uic.loadUi(main_ui_file)
  mainGui(main_ui)
  # ex = App()
  sys.exit(app.exec_())
