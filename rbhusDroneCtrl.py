#!/usr/bin/python
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
              clientSocket.send("CLIENTKILLED")
            except:
              clientSocket.send("CLIENTKILLFAILED")
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
            clientSocket.send("CLIENTKILLED")
        except:
          logClientCrtl.debug(str(sys.exc_info()))
          clientSocket.send("CLIENTKILLFAILED")
          pass

def UPDATE(clientSocket):
  if(sys.platform.find("linux") >= 0):
    try:
      os.system("cd /opt/rbhus/ ; git pull")
    except:
      logClient.debug(msg)


def RESTARTSYS(clientSocket):
  time.sleep(5)
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
  
def CLIENTSTART(clientSocket):
  time.sleep(15)
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


def CLEANUPPIDS(clientSocket):
  try:
    os.remove(mainPidFile)
  except:
    logClientCrtl.debug(str(sys.exc_info()))
  try:
    os.remove(pidOnlyFile)
  except:
    logClientCrtl.debug(str(sys.exc_info()))

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
      ckillThread = threading.Thread(target=CLIENTKILL,args=(clientSocket,))
      ckillThread.start()
      #if(os.path.exists(pidOnlyFile)):
        #pOf = open(pidOnlyFile,"r")
        #pOfiles = pOf.readlines()
        #pOfilestmp = []
        #pOf.close()
        #if(pOfiles):
          #for x in pOfiles:
            #pOfilestmp.append(x.rstrip().lstrip())
        #pOfiles = pOfilestmp
        #for x in pOfiles:
          #logClientCrtl.debug("trying to kill : "+ str(x))
          #if(x):
            #try:
              #if(sys.platform.find("linux") >= 0):
                #try:
                  #os.kill(int(x),signal.SIGTERM)
                  #clientSocket.send("CLIENTKILLED")
                #except:
                  #clientSocket.send("CLIENTKILLFAILED")
              #if(sys.platform.find("win") >= 0):
                #os.system("taskkill /t /f /pid "+ str(x))
                #time.sleep(5)
                #try:
                  #os.remove(mainPidFile)
                #except:
                  #logClientCrtl.debug(str(sys.exc_info()))
                #try:
                  #os.remove(pidOnlyFile)
                #except:
                  #logClientCrtl.debug(str(sys.exc_info()))
                #clientSocket.send("CLIENTKILLED")
            #except:
              #logClientCrtl.debug(str(sys.exc_info()))
              #clientSocket.send("CLIENTKILLFAILED")
              #pass
      
    if(msg == "UPDATE"):
      updateThread = threading.Thread(target=UPDATE,args=(clientSocket))
      updateThread.start()
      #if(sys.platform.find("linux") >= 0):
        #try:
          #os.system("cd /opt/rbhus/ ; git pull")
        #except:
          #logClient.debug(msg)
      
      
    if(msg == "RESTARTSYS"):
      restartThread = threading.Thread(target=RESTARTSYS,args=(clientSocket))
      restartThread.start()
      #time.sleep(5)
      #if(sys.platform.find("linux") >= 0):
        #try:
          #os.system("reboot >& /dev/null &")
        #except:
          #logClient.debug(msg)
      #elif(sys.platform.find("win") >= 0):
        #try:
          #os.system("shutdown /r /t 1")
        #except:
          #logClient.debug(msg)        
            
    if(msg == "CLIENTSTART"):
      cstartThread = threading.Thread(target=CLIENTSTART,args=(clientSocket))
      cstartThread.start()
      #time.sleep(15)
      #if(sys.platform.find("linux") >= 0):
        #try:
          #subprocess.Popen(str(rbhusMainDir +"rbhusDrone.py").split())
        #except:
          #logClientCrtl.debug(str(sys.exc_info()))
      #if(sys.platform.find("win") >= 0):
        #try:
          #subprocess.Popen([sys.executable, str(rbhusMainDir) +"rbhusDrone.py"])
        #except:
          #logClientCrtl.debug(str(sys.exc_info()))
          
    if(msg == "CLEANUPPIDS"):
      cleanThread = threading.Thread(target=CLEANUPPIDS,args=(clientSocket))
      cleanThread.start()
      #try:
        #os.remove(mainPidFile)
      #except:
        #logClientCrtl.debug(str(sys.exc_info()))
      #try:
        #os.remove(pidOnlyFile)
      #except:
        #logClientCrtl.debug(str(sys.exc_info()))
      
      
    
    while(1):
      try:
        clientSocket.close()
        break
      except:
        pass
    
      
      
if(__name__ == "__main__"):
  atUrService()