#!/usr/bin/python
import os
import sys
import datetime
import re
import argparse
import logging
import logging.handlers
import socket
import tempfile
import copy
from PyQt4 import QtCore, QtGui, uic
import uuid
import webbrowser



dirSelf = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep) + os.sep + "lib")
ui_file_path = dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep) + os.sep + "lib"
ui_left_msg = os.path.join(ui_file_path,"rbhusPipeReviewMod_textBox_left.ui")
ui_right_msg = os.path.join(ui_file_path,"rbhusPipeReviewMod_textBox_right.ui")
import rbhusPipeReviewMod

sys.path.append(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")

import dbPipe
import constantsPipe
import authPipe
import utilsPipe
import debug


parser = argparse.ArgumentParser()

hostname = socket.gethostname()
tempDir = os.path.abspath(tempfile.gettempdir())

if(sys.platform.find("win") >= 0):
  try:
    username = os.environ['rbhusPipe_acl_user']
  except:
    username = "nobody"
if(sys.platform.find("linux") >= 0):
  try:
    username = os.environ['rbhusPipe_acl_user']
  except:
    username = "nobody"
    

try:
  _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
  _fromUtf8 = lambda s: s
  

try:
  _encoding = QtGui.QApplication.UnicodeUTF8
  def _translate(context, text, disambig):
    return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
  def _translate(context, text, disambig):
    return QtGui.QApplication.translate(context, text, disambig)
  
  
parser = argparse.ArgumentParser()
parser.add_argument("-p","--assetpath",dest='assetpath',help='asset path (pipePath)')
parser.add_argument("-i","--assetid",dest='assetid',help='asset id')
args = parser.parse_args()



  
class Ui_Form(rbhusPipeReviewMod.Ui_MainWindow):
  def setupUi(self, Form):
    rbhusPipeReviewMod.Ui_MainWindow.setupUi(self,Form)
    self.spacerForMsgBox = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
    self.splitter.setStretchFactor(0, 10)
    self.assdets = {}
    self.msgboxes = []
    self.isReferenceAdded = False
    self.referenceFolder = str(uuid.uuid4())
    if(args.assetpath):
      self.assdets = utilsPipe.getAssDetails(assPath=args.assetpath)
    elif(args.assetid):
      self.assdets = utilsPipe.getAssDetails(assId=args.assetid)
    if(self.assdets):
      Form.setWindowTitle(self.assdets['path'])
    else:
      sys.exit(0)
    if(self.assdets['reviewStatus'] == constantsPipe.reviewStatusDone):
      self.comboProgress.setCurrentIndex(1)
    else:
      self.comboProgress.setCurrentIndex(0)

    self.reviewVersion.setText("review for version : "+ str(self.assdets['reviewVersion']))
    
    self.pushOpenReferenceReview.clicked.connect(lambda item,ver=str(self.assdets['reviewVersion']),refFolder=str(self.referenceFolder) : self.openReferenceFolder(item,ver,refFolder))
    self.pushOpenVersion.clicked.connect(lambda item,ver=str(self.assdets['reviewVersion']) : self.openVersionFolder(item,ver))
    self.pushSend.clicked.connect(self.sendReview)
    self.scrollArea.verticalScrollBar().rangeChanged.connect(self.updateScroll)
    self.update()


  
  def updateScroll(self,min,max):
    self.scrollArea.verticalScrollBar().setValue(max)



  def update(self):
    self.assReviewDets = utilsPipe.reviewDetails(assId=self.assdets['assetId'])
    if(self.assReviewDets):
      for x in self.assReviewDets:
        b = self.addMsgBox(x['message'],x['username'],x['datetime'],x['reviewVersion'],x['referenceFolder'])
        self.msgboxes.append(b)

  
  def clearLayout(self):
    while self.verticalLayout_2.count():
      child = self.verticalLayout_2.takeAt(0)
      if(child.widget() is not None):
        child.widget().deleteLater()

  
  def openReferenceFolder(self,*args):
    abspath  = utilsPipe.getAbsPath(self.assdets['path'])
    verFolder = abspath + "/review_" + str(args[1]) + "/"
    refFolder = verFolder + ".ref/"+ str(args[2])
    if(utilsPipe.isReviewUser(self.assdets) or utilsPipe.isStageAdmin(self.assdets) or utilsPipe.isAssAssigned(self.assdets)):
      try:
        os.makedirs(refFolder)
      except:
        pass
      webbrowser.open(refFolder)
      self.isReferenceAdded = True


  def openVersionFolder(self,*args):
    abspath  = utilsPipe.getAbsPath(self.assdets['path'])
    verFolder = abspath +"/review_"+ str(args[1]) +"/"
    if(os.path.exists(verFolder)):
      webbrowser.open(verFolder)
    

  def sendReview(self):
    if(utilsPipe.isReviewUser(self.assdets) or utilsPipe.isStageAdmin(self.assdets) or utilsPipe.isAssAssigned(self.assdets) or utilsPipe.isProjAdmin(self.assdets)):
      if(self.assdets['reviewStatus'] == constantsPipe.reviewStatusDone):
        debug.info("review done")
      if(str(self.textEdit.toPlainText()) == ""):
        debug.info("not updating since there is no message")
        return(0)

      revdets = {}
      revdets['assetId'] = str(self.assdets['assetId'])
      revdets['reviewVersion'] = str(self.assdets['reviewVersion'])
      revdets['message'] = str(self.textEdit.toPlainText())
      revdets['username'] = str(username)
      if(self.isReferenceAdded):
        revdets['referenceFolder'] = str(self.referenceFolder)
        self.isReferenceAdded = False
      else:
        revdets['referenceFolder'] = ""
      utilsPipe.reviewAdd(revdets)
      assedit = {}

      if(str(self.comboProgress.currentText()) == "inProgress"):
        assedit['reviewStatus'] = constantsPipe.reviewStatusInProgress
      else:
        assedit['reviewStatus'] = constantsPipe.reviewStatusDone

      utilsPipe.assEdit(assid=str(self.assdets['assetId']),assdict=assedit)
      self.referenceFolder = str(uuid.uuid4())
      self.clearLayout()
      self.update()
      self.pushOpenReferenceReview.clicked.disconnect()
      self.pushOpenReferenceReview.clicked.connect(lambda item,ver=str(self.assdets['reviewVersion']),refFolder=str(self.referenceFolder) : self.openReferenceFolder(item,ver,refFolder))
      self.textEdit.clear()




    
  def addMsgBox(self,msg,user1,date1,ver,rFolder):
    try:
      self.verticalLayout_2.removeItem(self.spacerForMsgBox)
    except:
      pass

    if(username == user1):
      ui_msg = uic.loadUi(ui_left_msg)
    else:
      ui_msg = uic.loadUi(ui_right_msg)
    ui_msg.textEditContent.setText(msg)
    ui_msg.textEditContent.setReadOnly(True)
    ui_msg.labelUser.setText("user : "+ str(user1))
    ui_msg.labelDate.setText("date : "+ str(date1))
    ui_msg.labelVersion.setText("version : "+ str(ver))
    self.verticalLayout_2.addWidget(ui_msg)
    self.verticalLayout_2.addItem(self.spacerForMsgBox)
    debug.info("reference folder : {0}".format(len(rFolder)))
    if(not len(rFolder)):
      ui_msg.pushReference.setEnabled(False)
    else:
      ui_msg.pushReference.clicked.connect(lambda item, ver=str(ver),refFolder=str(rFolder) : self.openReferenceFolder(item,ver,refFolder))
    ui_msg.pushVersion.clicked.connect(lambda item, ver=str(ver) : self.openVersionFolder(item,ver))
    return(ui_msg)

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
if __name__ == "__main__":
  app = QtGui.QApplication(sys.argv)
  Form = QtGui.QMainWindow()
  ui = Ui_Form()
  ui.setupUi(Form)
  Form.show()
  sys.exit(app.exec_())
    