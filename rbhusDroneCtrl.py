#!/usr/bin/env python3
import sys
import os
import time
import socket
import logging
import tempfile
import signal
import subprocess
import threading
import rbhus.dbRbhus as dbRbhus
import rbhus.utils as rUtils
import rbhus.constants as constants
if(sys.platform.find("linux") >= 0):
  import setproctitle
  setproctitle.setproctitle("rD")

tempDir = tempfile.gettempdir()
hostname,ipAddr = rUtils.getLocalNameIP()

if(sys.platform.find("linux") >=0):
  LOG_FILENAME = logging.FileHandler('/var/log/rbhusClientCtrl.log')
  #rbhusMainDir = "/projdump/pythonTestWindoze.DONOTDELETE/rbhus/"
  rbhusMainDir = "/opt/rbhus/"
elif(sys.platform.find("win") >=0):
  LOG_FILENAME = logging.FileHandler(tempDir + os.sep + "rbhusClientCtrl.log")
  rbhusMainDir = "z:/pythonTestWindoze.DONOTDELETE/rbhus/"
logClientCrtl = logging.getLogger("logClientCrtl")
logClientCrtl.setLevel(logging.DEBUG)

BASIC_FORMAT = logging.Formatter("%(asctime)s - %(funcName)s - %(levelname)s - %(lineno)s - %(message)s")
#ROTATE_FILENAME = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=20480, backupCount=3)
LOG_FILENAME.setFormatter(BASIC_FORMAT)
logClientCrtl.addHandler(LOG_FILENAME)





mainPidFile = tempDir + os.sep +"rbhusDrone.pids"
pidOnlyFile = tempDir + os.sep +"rbhusDroneMain.pid"
singular = tempDir + os.sep + "singularity"


def CLIENTKILL(clientSocket):
  if(os.path.exists(pidOnlyFile)):
    pOf = open(pidOnlyFile,"r")
    pOfiles = pOf.readlines()
    pOfilestmp = []
    pOf.close()
    if(pOfiles):
      for x in pOfiles:
        pOfilestmp.append(x.rstrip().lstrip())
    pOfiles = pOfilestmp
    for x in pOfiles:
      logClientCrtl.debug("trying to kill : "+ str(x))
      if(x):
        try:
          if(sys.platform.find("linux") >= 0):
            try:
              os.kill(int(x),signal.SIGTERM)
              logClientCrtl.debug("killed : "+ str(x))
            except:
              logClientCrtl.debug("kill failed : "+ str(x))
          if(sys.platform.find("win") >= 0):
            os.system("taskkill /t /f /pid "+ str(x))
            time.sleep(5)
          try:
            os.remove(mainPidFile)
          except:
            logClientCrtl.debug(str(sys.exc_info()))
          try:
            os.remove(pidOnlyFile)
          except:
            logClientCrtl.debug(str(sys.exc_info()))
          try:
            os.remove(singular)
          except:
            logClientCrtl.debug(str(sys.exc_info()))
          logClientCrtl.debug("CLIENTKILLED")
        except:
          logClientCrtl.debug(str(sys.exc_info()))
          logClientCrtl.debug("CLIENTKILLFAILED")
          
  clientSocket.close()
  time.sleep(2)

def UPDATE(clientSocket = None):
  if(sys.platform.find("linux") >= 0):
    try:
      os.system("cd /opt/rbhus/ ; git pull")
    except:
      logClient.debug(msg)
  if(clientSocket != None):
    clientSocket.close()
  


def RESTARTSYS(clientSocket):
  time.sleep(5)
  if(sys.platform.find("linux") >= 0):
    try:
      os.system("sync ; /sbin/reboot -f &> /dev/null &")
    except:
      logClient.debug(msg)
  elif(sys.platform.find("win") >= 0):
    try:
      os.system("shutdown /r /f /t 1")
    except:
      logClient.debug(msg)        
  clientSocket.close()
  
  
def SHUTDOWNSYS(clientSocket):
  time.sleep(5)
  if(sys.platform.find("linux") >= 0):
    try:
      os.system("sync ; halt -f -p &>  /dev/null &")
    except:
      logClient.debug(msg)
  elif(sys.platform.find("win") >= 0):
    try:
      os.system("shutdown /s /f /t 1")
    except:
      logClient.debug(msg)        
  clientSocket.close()



  
  
def CLIENTSTART(clientSocket):
  time.sleep(10)
  if(sys.platform.find("linux") >= 0):
    try:
      subprocess.Popen(str(rbhusMainDir +"rbhusDrone.py").split())
    except:
      logClientCrtl.debug(str(sys.exc_info()))
  if(sys.platform.find("win") >= 0):
    try:
      subprocess.Popen([sys.executable, str(rbhusMainDir) +"rbhusDrone.py"])
    except:
      logClientCrtl.debug(str(sys.exc_info()))
  clientSocket.close()   
  


def CLEANUPPIDS(clientSocket):
  try:
    os.remove(mainPidFile)
  except:
    logClientCrtl.debug(str(sys.exc_info()))
  try:
    os.remove(pidOnlyFile)
  except:
    logClientCrtl.debug(str(sys.exc_info()))
  try:
    os.remove(singular)
  except:
    logClientCrtl.debug(str(sys.exc_info()))
  clientSocket.close()



def atUrService():
  if(sys.platform.find("linux") >=0):
    setproctitle.setproctitle("rD_Control")
  db_conn = dbRbhus.dbRbhus()
  logClientCrtl.debug(str(os.getpid()) + ": atUrService func")
  try:
    if(sys.platform.find("linux") >=0):
      os.makedirs("/crap/versionCache/")
      os.chmod("/crap/versionCache/",0o777)
      os.makedirs("/crap/mercurial/")
      os.chmod("/crap/mercurial/",0o777)
    elif(sys.platform.find("linux") >=0):
      os.makedirs("d:/versionCache/")
      os.makedirs("d:/mercurial/")
  except:
    pass
  
  while(1):
    try:
      hostName,ipAddr = rUtils.getLocalNameIP()
      serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      serverSocket.bind(("", constants.clientCtrlListenPort))
      serverSocket.listen(5)
      break
    except:
      logClientCrtl.debug(str(sys.exc_info()))
      if(str(sys.exc_info()).find('Address already in use') >= 0):
        break
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
      CLIENTKILL(clientSocket)
    if(msg == "UPDATE"):
      UPDATE(clientSocket)
    if(msg == "RESTARTSYS"):
      RESTARTSYS(clientSocket)
    if(msg == "CLIENTSTART"):
      pass
      # CLIENTSTART(clientSocket)
    if(msg == "CLEANUPPIDS"):
      CLEANUPPIDS(clientSocket)
    if(msg == "SHUTDOWNSYS"):
      SHUTDOWNSYS(clientSocket)
    
      
      
if(__name__ == "__main__"):
  UPDATE()
  atUrService()