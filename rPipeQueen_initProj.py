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
import logging.handlers
import time
import signal
import setproctitle
import tempfile
import rbhus.dbPipe as dbPipe
import rbhus.constantsPipe as constantsPipe
import multiprocessing


def getHostNameIP():
  while(1):
    try:
      hostname = socket.gethostname()
      ipAddr = socket.gethostbyname(socket.gethostname()).strip()
      return(hostname,ipAddr)
    except:
      time.sleep(1)


def atUrService():
  if(sys.platform.find("linux") >=0):
      setproctitle.setproctitle("pD_atUrService")
    print(str(os.getpid()) + ": atUrService func")
    while(1):
      try:
        hostName,ipAddr = getHostNameIP()
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.bind(("", constants.projInitPort))
        serverSocket.listen(5)
        break
      except:
        pass
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
        
      if(msg == "CREATE"):
        projId = int(value)
        createProject(projId)


def createProject(projId):
  db_conn = dbPipe.dbPipe()
  projDets = db_conn.execute("select * from proj where projId="+ str(projId),dictionary=True)
  if(projDets):
    projDet = projDets[-1]
    if(sys.platform.find("win") >= 0):
      dirMaps = db_conn.execute("select windowsMapping from dirMaps where directory='"+ str(projDet['directory']) +"'",dictionary=True)
    if(sys.platform.find("linux") >= 0):
      dirMaps = db_conn.execute("select linuxMapping from dirMaps where directory='"+ str(projDet['directory']) +"'",dictionary=True)
    dirMap = dirMaps[-1][dirMaps[-1].keys()[-1]]
    createScript = db_conn.execute("select createScript from projTypes where type='"+ str(projDet['type']) +"'",dictionary=True)
    script = createScript[-1][createScript[-1].keys()[-1]]
    os.system("python "+ script +" --directory "+ projDir)
        
    
    
    
    
  
  
  
