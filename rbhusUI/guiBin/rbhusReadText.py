#!/usr/bin/env python2
from PyQt4 import QtCore, QtGui
import os
import sys


dirSelf = os.path.dirname(os.path.realpath(__file__))
print(dirSelf)
sys.path.append(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep) + os.sep + "lib")


import rbhusTextReadMod
sys.path.append(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")


textFile = sys.argv[1]
if(not textFile):
  sys.exit(1)
print(textFile)

try:
  _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
  _fromUtf8 = lambda s: s
  

class Ui_Form(rbhusTextReadMod.Ui_readText):
  def setupUi(self, Form):
    rbhusTextReadMod.Ui_readText.setupUi(self,Form)
    Form.setWindowTitle(textFile)
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(_fromUtf8(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/rbhus.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
    Form.setWindowIcon(icon)
    self.popText(textFile)
    
    self.timer = QtCore.QTimer()
    self.timer.timeout.connect(lambda who=textFile: self.popText(who))
    self.checkRefresh.clicked.connect(self.timeCheck)
    
  def popText(self,textFile):
    f = open(textFile,"r")
    self.plainTextEdit.clear()
    
    for x in f.readlines():
      self.plainTextEdit.insertPlainText(x)
    self.plainTextEdit.setReadOnly(True)
    self.plainTextEdit.moveCursor(QtGui.QTextCursor.End)
    
    f.close()
    
  def timeCheck(self):
    cRefresh = self.checkRefresh.isChecked()
    if(cRefresh):
      self.startTimer()
    else:
      self.stopTimer()
  
  def startTimer(self):
    self.timer.start(5000)

  def stopTimer(self):
    self.timer.stop()
  


if __name__ == "__main__":
  app = QtGui.QApplication(sys.argv)
  Form = QtGui.QMainWindow()
  ui = Ui_Form()
  ui.setupUi(Form)
  Form.show()
  sys.exit(app.exec_())

