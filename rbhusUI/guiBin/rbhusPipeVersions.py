#!/usr/bin/python
from PyQt4 import QtCore, QtGui
import glob
import os
import sys
import time
import subprocess
import argparse


dirSelf = os.path.dirname(os.path.realpath(__file__))
print(dirSelf)
sys.path.append(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep) + os.sep + "lib")


scb = "selectCheckBox.py"
srb = "selectRadioBox.py"
selectCheckBoxCmd = dirSelf.rstrip(os.sep) + os.sep + scb
selectRadioBoxCmd = dirSelf.rstrip(os.sep) + os.sep + srb





import rbhusPipeVersionsMod
print(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")
sys.path.append(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")
import dbPipe
import constantsPipe
import authPipe
import utilsPipe






parser = argparse.ArgumentParser()
parser.add_argument("-i","--id",dest='assId',help='asset id')
parser.add_argument("-p","--path",dest='assPath',help='asset path')
args = parser.parse_args()




try:
  _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
  _fromUtf8 = lambda s: s
  

class Ui_Form(rbhusPipeVersionsMod.Ui_MainWindow):
  def setupUi(self, Form):
    self.form = Form
    rbhusPipeVersionsMod.Ui_MainWindow.setupUi(self,Form)
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(_fromUtf8(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/rbhusPipe.svg")), QtGui.QIcon.Normal, QtGui.QIcon.On)
    Form.setWindowIcon(icon)
    
    
    















if __name__ == "__main__":
  app = QtGui.QApplication(sys.argv)
  Form = QtGui.QMainWindow()
  ui = Ui_Form()
  ui.setupUi(Form)
  Form.show()
  sys.exit(app.exec_())
    