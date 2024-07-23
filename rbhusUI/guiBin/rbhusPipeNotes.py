#!/usr/bin/env python2
import argparse
import os
import socket
import sys
import tempfile
import uuid
import webbrowser
if(sys.platform.find("linux") >=0 ):
  import fcntl
import psutil

from PyQt4 import QtCore, QtGui, uic

parser = argparse.ArgumentParser()
parser.add_argument("-p","--assetpath",dest='assetpath',help='asset path (pipePath)')
parser.add_argument("-i","--assetid",dest='assetid',help='asset id')
args = parser.parse_args()

dirSelf = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep) + os.sep + "lib")
ui_file_path = dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep) + os.sep + "lib"
ui_left_msg = os.path.join(ui_file_path,"rbhusPipeNotesMod_textBox_left.ui")
ui_right_msg = os.path.join(ui_file_path,"rbhusPipeNotesMod_textBox_right.ui")
import rbhusPipeNotesMod

sys.path.append(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")

import constantsPipe
import utilsPipe
import utilsTray
import debug
import pyperclip



hostname = socket.gethostname()
tempDir = os.path.abspath(tempfile.gettempdir())
app_lock_file = os.path.join(tempfile.gettempdir(),str(args.assetpath).replace(":","_")) + ".notes"


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
  
  


def app_lock():
  if(os.path.exists(app_lock_file)):
    f = open(app_lock_file,"r")
    pid = f.read().strip()
    f.close()
    debug.info(pid)
    try:
      p = psutil.Process(int(pid))
      if (os.path.abspath(p.cmdline()[1]) == os.path.abspath(__file__)):
        debug.warning("already an instance of the app is running.")
        debug.warning("delete the file {0}".format(app_lock_file))
        QtCore.QCoreApplication.instance().quit()
        os._exit(1)
      else:
        raise Exception("seems like a different process has the same pid")
    except:
      debug.warn(sys.exc_info())
      f = open(app_lock_file,"w")
      if(sys.platform.find("linux") >= 0):
        try:
          fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except:
          debug.error(sys.exc_info())
          QtCore.QCoreApplication.instance().quit()
          os._exit(1)
      f.write(unicode(os.getpid()))
      f.flush()
      if (sys.platform.find("linux") >= 0):
        fcntl.flock(f, fcntl.LOCK_UN)
      f.close()
  else:
    f = open(app_lock_file,"w")
    if (sys.platform.find("linux") >= 0):
      try:
        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
      except:
        debug.error(sys.exc_info())
        QtCore.QCoreApplication.instance().quit()
        os._exit(1)
    f.write(unicode(os.getpid()))
    f.flush()
    if (sys.platform.find("linux") >= 0):
      fcntl.flock(f, fcntl.LOCK_UN)
    f.close()

  
class Ui_Form(rbhusPipeNotesMod.Ui_MainWindow):
  def setupUi(self, Form):
    app_lock()
    rbhusPipeNotesMod.Ui_MainWindow.setupUi(self,Form)

    self.spacerForMsgBox = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
    self.splitter.setStretchFactor(0, 10)
    self.assdets = {}
    self.msgboxes = []
    if(args.assetpath):
      self.assdets = utilsPipe.getAssDetails(assPath=args.assetpath)
    elif(args.assetid):
      self.assdets = utilsPipe.getAssDetails(assId=args.assetid)
    if(self.assdets):
      Form.setWindowTitle(self.assdets['path'])
    else:
      sys.exit(0)

    self.pushSend.clicked.connect(self.sendReview)
    self.scrollArea.verticalScrollBar().rangeChanged.connect(self.updateScroll)
    self.update()


  
  def updateScroll(self,min,max):
    self.scrollArea.verticalScrollBar().setValue(max)



  def update(self):
    self.assReviewDets = utilsPipe.notesDetails(assId=self.assdets['assetId'])
    if(self.assReviewDets):
      for x in self.assReviewDets:
        b = self.addMsgBox(x['notes'],x['username'],x['datetime'].ctime())
        self.msgboxes.append(b)

  
  def clearLayout(self):
    while self.verticalLayout_2.count():
      child = self.verticalLayout_2.takeAt(0)
      if(child.widget() is not None):
        child.widget().deleteLater()

  


  def sendReview(self):
    if(utilsPipe.isReviewUser(self.assdets) or utilsPipe.isStageAdmin(self.assdets) or utilsPipe.isAssAssigned(self.assdets) or utilsPipe.isProjAdmin(self.assdets)):
      if(str(self.textEdit.toPlainText()) == ""):
        self.textEdit.setText(str(self.comboProgress.currentText()))
        # debug.info("not updating since there is no message")
        # return(0)

      revdets = {}
      revdets['assetId'] = str(self.assdets['assetId'])
      revdets['notes'] = str(self.textEdit.toPlainText())
      revdets['username'] = str(username)
      utilsPipe.notesAdd(revdets)
      assedit = {}

      self.clearLayout()
      self.update()
      self.textEdit.clear()




    
  def addMsgBox(self,msg,user1,date1):
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
    ui_msg.labelUser.setText("Notes by : "+ str(user1))
    ui_msg.labelDate.setText("date : "+ str(date1))
    hdoc = QtGui.QTextDocument()
    hdoc.setPlainText(ui_msg.textEditContent.toPlainText())
    h = hdoc.size().height() + 40
    ui_msg.textEditContent.setMinimumHeight(h)
    debug.info("height : " + str(h))

    # ui_msg.textEditContent.setFixedHeight(height)

    self.verticalLayout_2.addWidget(ui_msg)
    self.verticalLayout_2.addItem(self.spacerForMsgBox)
    return(ui_msg)

    
    
    
    
    

    
    
    
    
    
    
    
    
    
if __name__ == "__main__":
  app = QtGui.QApplication(sys.argv)
  Form = QtGui.QMainWindow()
  ui = Ui_Form()
  ui.setupUi(Form)
  Form.show()
  Form.raise_()
  sys.exit(app.exec_())
    