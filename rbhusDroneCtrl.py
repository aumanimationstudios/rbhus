import sys
import os
import time
import socket
import logging
import rbhus.dbRbhus as dbRbhus
import rbhus.utils as rUtils
if(sys.platform.find("linux") >= 0):
  import setproctitle
  setproctitle.setproctitle("rD")


hostname,ipAddr = rUtils.getLocalNameIP()

if(sys.platform.find("linux") >=0):
  LOG_FILENAME = logging.FileHandler('/var/log/rbhusClientCtrl.log')
elif(sys.platform.find("win") >=0):
  LOG_FILENAME = logging.FileHandler(tempDir + os.sep + "rbhusClientCtrl.log")
  #LOG_FILENAME = logging.FileHandler('z:/pythonTestWindoze.DONOTDELETE/clientLogs/rbhusClient_'+ hostname +'.log')


#LOG_FILENAME = logging.FileHandler('/var/log/rbhusDb_module.log')
logClientCrtl = logging.getLogger("logClientCrtl")
logClientCrtl.setLevel(logging.DEBUG)

BASIC_FORMAT = logging.Formatter("%(asctime)s - %(funcName)s - %(levelname)s - %(lineno)s - %(message)s")
LOG_FILENAME.setFormatter(BASIC_FORMAT)
logClientCrtl.addHandler(LOG_FILENAME)





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
      serverSocket.bind(("", 6661))
      serverSocket.listen(5)
      break
    except:
      logClientCrtl.debug(str(sys.exc_info()))
      sys.exit(1)
    time.sleep(1)

  while(1):
    clientSocket, address = serverSocket.accept()
    logClientCrtl.debug("I got a connection from "+ str(address))
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
      
    if(msg == "CLIENTKILL"):
      if(os.path.exists(pidOnlyFile)):
        pOf = open(pidOnlyFile,"r")
        for x in pOf.readlines():
          if(x):
            try:
              os.kill(int(x),signal.SIGTERM)
            except:
              pass
      
    
    while(1):
      try:
        clientSocket.close()
        break
      except:
        pass
      
      
if(__name__ == "__main__"):
  atUrService()