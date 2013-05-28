#!/usr/bin/python
from PyQt4 import QtCore, QtGui
import os
import sys


progPath =  sys.argv[0].split(os.sep)
textFile = sys.argv[1]
print progPath
if(len(progPath) > 1):
  pwd = os.sep.join(progPath[0:-1])
  cwd = os.path.abspath(pwd)
else:
  cwd = os.path.abspath(os.getcwd())
  
sys.path.append(cwd.rstrip(os.sep) + os.sep + "lib")


import rbhusTextReadMod
sys.path.append(cwd.rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")




try:
  _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
  _fromUtf8 = lambda s: s
  

class Ui_Form(rbhusTextReadMod.Ui_readText):
  def setupUi(self, Form):
    rbhusTextReadMod.Ui_readText.setupUi(self,Form)
    Form.setWindowTitle(textFile)
    self.popText(textFile)
    
  def popText(self,textFile):
    f = open(textFile,"r")
    for x in f.readlines():
      self.plainTextEdit.insertPlainText(x)
    self.plainTextEdit.setReadOnly(True)
  


if __name__ == "__main__":
  app = QtGui.QApplication(sys.argv)
  Form = QtGui.QMainWindow()
  ui = Ui_Form()
  ui.setupUi(Form)
  Form.show()
  sys.exit(app.exec_())

