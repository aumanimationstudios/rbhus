#!/usr/bin/python
from PyQt4 import QtCore, QtGui
import os
import sys
import tempfile
import time


dirSelf = os.path.dirname(os.path.realpath(__file__))
print(dirSelf)
sys.path.append(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep) + os.sep + "lib")

tempDir = tempfile.gettempdir()

rL = "rbhusList.py"
rS = "rbhusSubmit.py"
rH = "rbhusHost.py"

rbhuslistCmd = dirSelf.rstrip(os.sep) + os.sep + rL
rbhuslistCmd = rbhuslistCmd.replace("\\","/")

rbhusSubmitCmd = dirSelf.rstrip(os.sep) + os.sep + rS
rbhusSubmitCmd = rbhusSubmitCmd.replace("\\","/")

rbhusHostCmd = dirSelf.rstrip(os.sep) + os.sep + rH
rbhusHostCmd = rbhusHostCmd.replace("\\","/")

print rbhuslistCmd
import rbhusRenderMain
print(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")
sys.path.append(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")
import db
import constants
import auth
import dbRbhus
import utils as rUtils

try:
  _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
  _fromUtf8 = lambda s: s


class Ui_Form(rbhusRenderMain.Ui_MainWindow):
  def setupUi(self, Form):
    rbhusRenderMain.Ui_MainWindow.setupUi(self,Form)
    self.authL = auth.login()
    self.username = None
    self.userProjIds = []
    self.center()
    try:
      self.username = os.environ['rbhus_acl_user'].rstrip().lstrip()
    except:
      pass
    try:
      self.userProjIds = os.environ['rbhus_acl_projIds'].split()
    except:
      pass

    self.hostDets = rUtils.hosts()

    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(_fromUtf8(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/rbhus.svg")), QtGui.QIcon.Normal, QtGui.QIcon.On)
    Form.setWindowIcon(icon)
    self.pushLogout.setText("logout : "+ str(self.username))
    self.pushList.clicked.connect(self.rbhusList)
    self.pushSubmit.clicked.connect(self.rbhusSubmit)
    self.pushHosts.clicked.connect(self.rbhusHost)
    self.pushLogout.clicked.connect(self.logout)

    self.form = Form
    self.wFlag = self.form.windowFlags()


    self.trayIcon = QtGui.QSystemTrayIcon(QtGui.QIcon(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/rbhus.svg"))
    self.trayIcon.show()

    self.trayMenu = QtGui.QMenu()
    self.hostMenu = QtGui.QMenu()
    self.listAction = self.trayMenu.addAction("list")
    self.newAction = self.trayMenu.addAction("new")
    self.hostAction = self.trayMenu.addAction("hosts")
    self.quitAction = self.trayMenu.addAction("quit")

    self.hostOpen = self.hostMenu.addAction("open")
    self.hostEnableAction = self.hostMenu.addAction("enable")
    self.hostDisableAction = self.hostMenu.addAction("stop")
    self.hostEnableAction.triggered.connect(self.hostDets.hEnable)
    self.hostDisableAction.triggered.connect(self.hostStop)
    self.hostOpen.triggered.connect(self.rbhusHost)


    self.trayIcon.setContextMenu(self.trayMenu)
    self.trayIcon.activated.connect(self.showMain)
    self.listAction.triggered.connect(self.rbhusList)
    self.newAction.triggered.connect(self.rbhusSubmit)
    self.hostAction.setMenu(self.hostMenu)
    self.quitAction.triggered.connect(self.quitFunc)
    # self.form.hideEvent = self.hideEventt
    self.form.closeEvent = self.closeEventt
    self.processes = []




  def hideEventt(self,event):
    #event.ignore()
    self.form.setVisible(False)
    #self.form.setWindowState(QtCore.Qt.WindowMinimized)

    self.form.setWindowFlags(self.wFlag & QtCore.Qt.Tool)
    #self.form.hide()


  def closeEventt(self,event):
    event.ignore()
    self.closeRunning()
    event.accept()




  def hostStop(self):
    self.hostDets.hDisable()
    self.hostDets.hStop()


  def showMain(self,actReason):
    if(actReason == 2):
      self.form.setVisible(True)
      self.form.setWindowFlags(self.wFlag)

  def rbhusList(self):
    self.pushList.setText("opening")
    p = QtCore.QProcess(parent=self.form)
    p.setStandardOutputFile(tempDir + os.sep +"rbhusList_"+ self.username +".log")
    p.setStandardErrorFile(tempDir + os.sep +"rbhusList_"+ self.username +".err")
    self.pushList.setEnabled(False)
    self.listAction.setEnabled(False)
    p.start(sys.executable,rbhuslistCmd.split())
    p.finished.connect(self.rbhusListEnable)
    p.started.connect(self.rbhusListWait)
    self.processes.append(p)


  def rbhusListWait(self):
    self.pushList.setText("list open")


  def rbhusListEnable(self,exitStatus):
    self.pushList.setText("list")
    self.pushList.setEnabled(True)
    self.listAction.setEnabled(True)


  def rbhusSubmit(self):
    self.pushSubmit.setText("opening")
    p = QtCore.QProcess(parent=self.form)
    p.setStandardOutputFile(tempDir + os.sep +"rbhusSubmit_"+ self.username +".log")
    p.setStandardErrorFile(tempDir + os.sep +"rbhusSubmit_"+ self.username +".err")
    self.pushSubmit.setEnabled(False)
    self.newAction.setEnabled(False)
    p.start(sys.executable,rbhusSubmitCmd.split())
    p.finished.connect(self.rbhusSubmitEnable)
    p.started.connect(self.rbhusSubmitWait)
    self.processes.append(p)

  def rbhusSubmitWait(self):
    self.pushSubmit.setText("new open")


  def closeRunning(self):
    if(self.processes):
      for x in self.processes:
        if(x.state() == QtCore.QProcess.NotRunning):
          self.processes.remove(x)
    if(self.processes):
      for x in self.processes:
        if(x.state() == QtCore.QProcess.Running):
          x.terminate()


  def rbhusSubmitEnable(self,exitStatus):
    self.pushSubmit.setText("new")
    self.pushSubmit.setEnabled(True)
    self.newAction.setEnabled(True)


  def rbhusHost(self):
    self.pushHosts.setText("opening")
    p = QtCore.QProcess(parent=self.form)
    p.setStandardOutputFile(tempDir + os.sep +"rbhusHost_"+ self.username +".log")
    p.setStandardErrorFile(tempDir + os.sep +"rbhusHost_"+ self.username +".err")
    self.pushHosts.setEnabled(False)
    self.hostOpen.setEnabled(False)
    p.start(sys.executable,rbhusHostCmd.split())
    p.finished.connect(self.rbhusHostEnable)
    p.started.connect(self.rbhusHostWait)
    self.processes.append(p)


  def rbhusHostWait(self):
    self.pushHosts.setText("hosts open")


  def rbhusHostEnable(self,exitStatus):
    self.pushHosts.setText("hosts")
    self.pushHosts.setEnabled(True)
    self.hostOpen.setEnabled(True)


  def logout(self):
    self.authL.logout()
    QtCore.QCoreApplication.instance().quit()

  def quitFunc(self):
    QtCore.QCoreApplication.instance().quit()


  def center(self):
    Form.move(QtGui.QApplication.desktop().screen().rect().center()- Form.rect().center())


if __name__ == "__main__":
  import sys
  app = QtGui.QApplication(sys.argv)
  Form = QtGui.QMainWindow()
  ui = Ui_Form()
  ui.setupUi(Form)
  Form.show()
  sys.exit(app.exec_())
