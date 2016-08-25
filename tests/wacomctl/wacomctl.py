#/usr/bin/python2.7
import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import threading
import subprocess
import time

def main():
  poll_thread = threading.Thread(target=poll,args=())
  poll_thread.start()
  app = QtWidgets.QApplication(sys.argv)

  trayIcon = QtWidgets.QSystemTrayIcon(QtGui.QIcon("./scalable-icons.png"), app)
  menu = QtWidgets.QMenu()
  exitAction = menu.addAction("Exit")

  trayIcon.setContextMenu(menu)
  exitAction.triggered.connect(quit)
  trayIcon.show()
  sys.exit(app.exec_())



def quit():
  QtCore.QCoreApplication.instance().quit()

def poll():
  active_window_cmd = "xprop -root"
  while(True):
    p = subprocess.Popen(active_window_cmd,shell=True,stderr=subprocess.PIPE, stdout=subprocess.PIPE).communicate()[0].split("\n")
    for x in p:
      if(x.startswith("_NET_ACTIVE_WINDOW(WINDOW)")):
        window_name_cmd = "xprop -id {0}".format(x.split("#")[-1].strip())
        q = subprocess.Popen(window_name_cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE).communicate()[0].split("\n")
        for y in q:
          if(y.startswith("WM_CLASS(STRING)")):
            print (y)
    time.sleep(1)


if __name__ == '__main__':

  main()
