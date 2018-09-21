#!/usr/bin/env python2
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys
import os
import argparse

from PyQt5 import QtCore, uic, QtGui, QtWidgets


rbhusPath = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-3])

sys.path.append(rbhusPath)


import rbhus.debug




busyIconGif = os.path.join(rbhusPath,"etc","icons","rbhusIconTray-BUSY.gif")
parser = argparse.ArgumentParser(description="Use the comand to copy whatever u copied from rbhus to any folder")
parser.add_argument("-d","--directory",dest="directory",help="paste into given directory")
args = parser.parse_args()



class syncThread(QtCore.QThread):
  syncing = QtCore.pyqtSignal(str)

  def __init__(self,parent,fileParticles):
    super(syncThread, self).__init__(parent)
    self.fileParticles  = fileParticles

  def run(self):
    for fileParticle in self.fileParticles.keys():
      if(os.path.isdir(fileParticle)):
        self.syncing.emit("\""+ fileParticle + "/\" -> \""+ self.fileParticles[fileParticle] + "\"")
        status = os.system("rsync -av \""+ fileParticle + "/\" \""+ self.fileParticles[fileParticle] + "\"")
        rbhus.debug.info(status)
      else:
        self.syncing.emit("\""+ fileParticle + "\" -> \"" + self.fileParticles[fileParticle] + "\"")
        status = os.system("rsync -av \""+ fileParticle + "\" \"" + self.fileParticles[fileParticle] + "\"")
        rbhus.debug.info(status)



def tray_icon_change(icon_anim,tray_icon):
  tray_icon.setIcon(QtGui.QIcon(icon_anim.currentPixmap()))


def setToolTip(tray_icon,msg):
  tray_icon.showMessage("COPYING",msg)


def main(app):



  tray_icon_anim = QtGui.QMovie(busyIconGif)
  tray_icon_anim.start()

  tray_icon = QtWidgets.QSystemTrayIcon(QtGui.QIcon(busyIconGif),app)
  tray_icon_anim.frameChanged.connect(lambda frameNumber, icon_anim= tray_icon_anim, tray_icon=tray_icon: tray_icon_change(icon_anim,tray_icon))
  tray_icon.show()
  clip = QtWidgets.QApplication.clipboard()
  pasteUrls = clip.mimeData().urls()

  fileParticles = {}
  applyOption = QtCore.Qt.Unchecked
  for url in pasteUrls:
    sourceFile = url.toLocalFile()


    isDir = os.path.isdir(sourceFile)
    sourceFileBaseName = os.path.basename(sourceFile)
    sourceDir = os.path.dirname(sourceFile)
    destFile = os.path.join(args.directory,sourceFileBaseName)
    rbhus.debug.info(sourceFile +" -> "+ destFile)

    if(os.path.exists(destFile)):
      if(applyOption == QtCore.Qt.Unchecked):
        msgBox = QtWidgets.QMessageBox()
        applyToAll = QtWidgets.QCheckBox("apply to all")
        msgBox.setText("Overwrite : " + sourceFileBaseName)
        msgBox.addButton(QtWidgets.QMessageBox.Yes)
        msgBox.addButton(QtWidgets.QMessageBox.No)
        msgBox.setDefaultButton(QtWidgets.QMessageBox.No)
        msgBox.setCheckBox(applyToAll)
        # applyToAll.stateChanged.connect(lambda stateChanged, applyOption = applyOption :rewriteFunc(stateChanged,applyOption))
        reply = msgBox.exec_()
        applyOption = applyToAll.checkState()
        if(applyOption == QtCore.Qt.Checked):
          rewriteReply = reply
      else:
        reply = rewriteReply



      rbhus.debug.info(applyOption)
      # reply = QtWidgets.QMessageBox.question(main_ui.listFiles, "WARNING", "Overwrite : " + sourceFileBaseName, QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
      if (reply == QtWidgets.QMessageBox.No):
        rbhus.debug.info("skipping : "+ sourceFile)
      else:
        fileParticles[sourceFile] = destFile
    else:
      fileParticles[sourceFile] = destFile

  if(fileParticles):
    sT = syncThread(app,fileParticles)
    sT.syncing.connect(lambda msg, tray_icon = tray_icon : setToolTip(tray_icon,msg))
    sT.finished.connect(sys.exit)
    sT.start()
  else:
    sys.exit(1)

  # tray_icon_anim.frameChanged.disconnect()







if __name__ == '__main__':

  app = QtWidgets.QApplication(sys.argv)

  main(app)
  sys.exit(app.exec_())