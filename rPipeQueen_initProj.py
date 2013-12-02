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
import rbhus.utilsPipe as utilsPipe
import multiprocessing
import pickle


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
        serverSocket.bind(("", constantsPipe.projInitPort))
        serverSocket.listen(5)
        break
      except:
        pass
      time.sleep(1)
  
    while(1):
      clientSocket, address = serverSocket.accept()
      data = ""
      data = clientSocket.recv(4096)
      clientSocket.close()
      data = data.rstrip()
      data = data.lstrip()
      msg = ""
      value = ""
      if(data.rfind(":") != -1):
        msg, value = data.split(":")
      else:
        msg = data
        
      if(msg == "CREATE"):
        admins = utilsPipe.getAdmins()
        
        projdets = pickle.loads(value)
        if(projdets['createdUser'] in admins):
          utilsPipe.setupProj(projdets['projType'],projdets['projName'],projdets['directory'],projdets['admins'],projdets['rbhusRenderIntergration'],projdets['rbhusRenderServer'],projdets['aclUser'],projdets['aclGroup'],projdets['createdUser'],projdets['dueDate'],['description'])
        else:
          print("user "+ str(projdets['createdUser']) +" not allowed to create projects.")
      



    
  
  
  
