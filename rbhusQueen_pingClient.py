#!/usr/bin/python
###
# Copyright (C) 2012  Shrinidhi Rao shrinidhi@clickbeetle.in
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
###

# SERVER!!!!!!!!
import sys
import os
import logging
import time
import signal
import setproctitle
import tempfile
import rbhus.dbRbhus as dbRbhus
import rbhus.constants as constants
import multiprocessing
import socket

LOG_FILENAME = '/var/log/rbhusQueen_pingClient.log'
logging.BASIC_FORMAT = "%(asctime)s - %(funcName)s - %(levelname)s - %(message)s"
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)


tempDir = tempfile.gettempdir()
mainPidFile = tempDir + os.sep +"rbusServer.pids"

setproctitle.setproctitle("rQ_pingClient")


def checkClientAlive():
  db_conn = dbRbhus.dbRbhus()
  maxPids = 100
  pIds = []
  while(1):
    logging.debug("WTF4")
    hostInfos = {}
    hostInfos = db_conn.getHostInfo(status="ALL")
    logging.debug("WTF5 : "+ str(hostInfos))
    if(not hostInfos):
      logging.debug("WTF6")
      continue
    logging.debug("WTF7")
    if(len(pIds) > 0):
      while(1):
        logging.debug("WTF0")
        for i in range(0,len(pIds)):
          if(pIds[i].is_alive()):
            pass
          else:
            logging.debug("GONE1 -WTF3: "+ str(pIds[i].pid))
            del(pIds[i])
            break
        if(len(pIds) < maxPids):
          break
        if(not pIds):
          break
        time.sleep(1)
    
    for hostInfo in hostInfos:
      logging.debug("WTF3")
      hostName = hostInfo['hostName']
      ipAddr = hostInfo['ip']
      logging.debug("Pinging "+ hostName + " with ip : "+ str(ipAddr))
      
      pingClientProcess_proc = multiprocessing.Process(target=pingClientProcess, args=(hostName,ipAddr,))
      pIds.append(pingClientProcess_proc)
      pingClientProcess_proc.start()
      time.sleep(1)
      
      if(len(pIds) >= maxPids):
        while(1):
          logging.debug("WTF1")
          for i in range(0,len(pIds)):
            if(pIds[i].is_alive()):
              pass
            else:
              logging.debug("GONE2 -WTF3: "+ str(pIds[i].pid))
              del(pIds[i])
              break
          if(len(pIds) < maxPids):
            break
          if(not pIds):
            break
          time.sleep(1)
    
    if(len(pIds) > 0):      
      while(1):
        logging.debug("WTF2")
        for i in range(0,len(pIds)):
          if(pIds[i].is_alive()):
            pass
          else:
            logging.debug("GONE3 -WTF3: "+ str(pIds[i].pid))
            del(pIds[i])
            break
        if(len(pIds) < maxPids):
          break
        if(not pIds):
          break
        time.sleep(1)
    time.sleep(35)
    

def pingClientProcess(client,ipAddr):
  setproctitle.setproctitle("rQ_ping_"+ str(client))
  db_conn = dbRbhus.dbRbhus()
  status = os.system("ping -c 1 -W 15 "+ str(ipAddr) +" >& /dev/null")
  pingstatus = 0
  sockstatus = 0
  if(status == 0):
    logging.debug("Connected to "+ client)
    pingstatus = 1
  else:
    logging.debug("Not able to connect to "+ client)
    while(1):
      if((db_conn.setHostAliveStatus(client,constants.hostAliveDead) == 1) and (db_conn.resetAssignedFrame(client, constants.framesHung) == 1)):
        break
      time.sleep(0.3)
    sys.exit(1)

  clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:
    clientSocket.settimeout(15)
    clientSocket.connect((ipAddr,6660))
    logging.debug("Connected to "+ client)
    sockstatus = 1
  except:
    logging.error("Screwed pingClientProcess sock connect : "+ client +" : "+ str(sys.exc_info()))
    sockstatus = 0
    try:
      clientSocket.close()
    except:
      pass
    db_conn.setHostAliveStatus(client,constants.hostAliveDead)
    db_conn.resetAssignedFrame(client, constants.framesHung)
    sys.exit(1)

  clientSocket.send("ALIVE")
  reply = ""
  try:
    reply = clientSocket.recv(1024)
    clientSocket.close()
    sockstatus = 1
  except:
    logging.error("Screwed pingClientProcess sock send : "+ client +" : "+ str(sys.exc_info()))
    sockstatus = 0
    clientSocket.close()
    #exit(1)
  if((sockstatus == 1) and (pingstatus == 1)):
    db_conn.setHostAliveStatus(client,constants.hostAliveAlive)
  else:
    db_conn.setHostAliveStatus(client,constants.hostAliveDead)
    db_conn.resetAssignedFrame(client, constants.framesHung)
  sys.exit(0)
  
  
if __name__=="__main__":
  checkClientAlive()
