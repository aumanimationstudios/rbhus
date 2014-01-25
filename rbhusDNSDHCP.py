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
#
# THIS SHOULD RUN ON YOUR DNSMASQ SERVER
#
#
#
#
#
# SERVER!!!!!!!!
import sys
import os
import logging
import logging.handlers
import time
import signal
import setproctitle
import tempfile
import rbhus.dbRbhus as dbRbhus
import rbhus.constants as constants
import rbhus.utils as rUtils
import multiprocessing
import socket


hostsFile = "/etc/hosts"
dnsmasqFile = "/etc/dnsmasq.conf"
pxelinux = "/srv/tftp/tftpboot/pxelinux.cfg/"
pxelinuxDefault = "/srv/tftp/tftpboot/pxelinux.cfg/default"
pxelinuxLinux = "/srv/tftp/tftpboot/pxelinux.cfg/default.linux"

def getCloneStatus():
  dbconn = dbRbhus.dbRbhusHost()
  try:
    rows = dbconn.execute("select * from clonedb", dictionary=True)
  except:
    print(sys.exc_info())
  try:
    mainrows = dbconn.execute("select * from main", dictionary=True)
  except:
    print(sys.exc_info())
    
  maccy = {}  
  
  if(mainrows):
    for mainrow in mainrows:
      maccy[mainrow['ip']] = mainrow['macc']
    
  if(rows):
    for row in rows:
      if(row['clone'] == constants.cloneGrubUpdate):
        if(row['cloneStatus'] == constants.cloneStatusInitiate):
          cpstatus = os.system("cp -v "+ pxelinuxLinux +" "+ maccy[row['ip']])
          if(not cpstatus):
            dbconn.execute("update clonedb set cloneStatus="+ str(constants.cloneStatusPending) +" where ip='"+ str(row['ip']) +"'")
            
        


def getPxeLabels():
  l = os.popen("cat "+ str(pxelinuxDefault) +" | grep -i label | gawk '{print $2}'")
  labels = [x.rstrip().lstrip() for x in l.readlines()]
  l.close()
  return(labels)
  

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
    setproctitle.setproctitle("DNSMASQ_atUrService")
  print(str(os.getpid()) + ": atUrService func")
  while(1):
    try:
      hostName,ipAddr = getHostNameIP()
      serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      serverSocket.bind(("", constantsPipe.projInitPort))
      serverSocket.listen(5)
      break
    except:
      print("socket failed 1 : "+ str(sys.exc_info()))
      pass
    time.sleep(1)
  
  while(1):
    clientSocket, address = serverSocket.accept()
    data = ""
    data = clientSocket.recv(4096)
    clientSocket.close()
    #data = data.rstrip()
    #data = data.lstrip()
    #msg = ""
    #value = ""
    #if(data.rfind(":") != -1):
      #msg, value = data.split(":")
    #else:
      #msg = data
    #print(data)  
    #if(msg == "CREATE"):
    admins = rUtils.getAdmins()
    
    hostDets = pickle.loads(data)
    if(hostDets['createdUser'] in admins):
      utilsPipe.setupProj(hostDets['projType'],hostDets['projName'],hostDets['directory'],hostDets['admins'],hostDets['rbhusRenderIntergration'],hostDets['rbhusRenderServer'],hostDets['aclUser'],hostDets['aclGroup'],hostDets['createdUser'],hostDets['dueDate'],hostDets['description'])
    else:
      print("user "+ str(hostDets['createdUser']) +" not allowed to create projects.")
  
  
  
if __name__=='__main__':
  atUrService()



    
  
  
  
