#!/usr/bin/python
import sys
import os
import time
import socket
import logging
import tempfile
import signal
import subprocess
import rbhus.dbRbhus as dbRbhus
import rbhus.utils as rUtils
import rbhus.constants as constants
if(sys.platform.find("linux") >= 0):
  import setproctitle
  setproctitle.setproctitle("rD")

tempDir = tempfile.gettempdir()
hostname,ipAddr = rUtils.getLocalNameIP()

if(sys.platform.find("linux") >=0):
  LOG_FILENAME = '/var/log/rbhusClientCtrl.log'
  rbhusMainDir = "/projdump/pythonTestWindoze.DONOTDELETE/rbhus/"
elif(sys.platform.find("win") >=0):
  LOG_FILENAME = tempDir + os.sep + "rbhusClientCtrl.log"
  rbhusMainDir = "z:/pythonTestWindoze.DONOTDELETE/rbhus/"
logClientCrtl = logging.getLogger("logClientCrtl")
logClientCrtl.setLevel(logging.DEBUG)

BASIC_FORMAT = logging.Formatter("%(asctime)s - %(funcName)s - %(levelname)s - %(lineno)s - %(message)s")
ROTATE_FILENAME = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=2048, backupCount=3)
ROTATE_FILENAME.setFormatter(BASIC_FORMAT)
logClientCrtl.addHandler(ROTATE_FILENAME)





mainPidFile = tempDir + os.sep +"rbhusDrone.pids"
pidOnlyFile = tempDir + os.sep +"rbhusDroneMain.pid"

def atUrService():
  if(sys.platform.find("linux") >=0):
    setproctitle.setproctitle("rD_Control")
  db_conn = dbRbhus.dbRbhus()
  logClientCrtl.debug(str(os.getpid()) + ": atUrService func")
  while(1):
    try:
      hostName,ipAddr = rUtils.getLocalNameIP()
      serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      serverSocket.bind(("", constants.clientCtrlListenPort))
      serverSocket.listen(5)
      break
    except:
      logClientCrtl.debug(str(sys.exc_info()))
      sys.exit(1)
    time.sleep(1)

  while(1):
    clientSocket, address = serverSocket.accept()
    
    data = ""
    data = clientSocket.recv(1024)
    data = data.rstrip()
    data = data.lstrip()
    msg = ""
    value = ""
    if(data.rfind(":") != -1):
      msg, value = data.split(":")
    else:
      msg = data
    logClientCrtl.debug("I got a connection from "+ str(address) +" : "+ str(data))
    if(msg == "CLIENTKILL"):
      if(os.path.exists(pidOnlyFile)):
        pOf = open(pidOnlyFile,"r")
        for x in pOf.readlines():
          logClientCrtl.debug("trying to kill : "+ str(x))
          if(x):
            try:
              os.kill(int(x),signal.SIGTERM)
            except:
              logClientCrtl.debug(str(sys.exc_info()))
              pass
    
    if(msg == "RESTARTSYS"):
      if(sys.platform.find("linux") >= 0):
        try:
          os.system("reboot >& /dev/null &")
        except:
          logClient.debug(msg)
      elif(sys.platform.find("win") >= 0):
        try:
          os.system("shutdown /r /t 1")
        except:
          logClient.debug(msg)        
            
    if(msg == "CLIENTSTART"):
      if(sys.platform.find("linux") >= 0):
        try:
          subprocess.Popen(str(rbhusMainDir +"rbhusDrone.py").split())
        except:
          logClientCrtl.debug(str(sys.exc_info()))
      elif(sys.platform.find("win") >= 0):
        try:
          subprocess.Popen(str("start C:/Python27/pythonw.exe "+ str(rbhusMainDir) +"rbhusDrone.py").split())
        except:
          logClientCrtl.debug(str(sys.exc_info()))
      
    
    while(1):
      try:
        clientSocket.close()
        break
      except:
        pass
      
      
if(__name__ == "__main__"):
  atUrService()