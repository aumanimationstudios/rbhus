#!/usr/bin/env python2
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys
import os
import time
import datetime

filedir = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-1])
print(filedir)
sys.path.append(filedir)
import rbhus.dbRbhus
import rbhus.debug
import rbhus.utils
import rbhus.WOL





timeformat = '%Y-%m-%d %H:%M:%S.%f'






def getMaccAddr(hostname):
  hdb = rbhus.dbRbhus.dbRbhusHost()

  try:
    row = hdb.execute("select * from main where name='"+ hostname +"'",dictionary=True)
  except:
    print (str(sys.exc_info()))
    return(None)
  if(row):
    det = row[-1]
    realName = det['macc']
    return(realName)

while(True):

  allActiveTasks = rbhus.dbRbhus.dbRbhus().getAllActiveTasks()
  # if(not allActiveTasks):
  if(not allActiveTasks):
    allActiveHosts = rbhus.dbRbhus.dbRbhus().getShutdownHosts()
    for activehost in allActiveHosts:
      # print(activehost['hostName'] + " : " + str(activehost['idleLast']))
      timeNow = datetime.datetime.now()
      timeDiff = timeNow - datetime.datetime.strptime(str(activehost['idleLast']),timeformat)
      timeDiffSecs = timeDiff.total_seconds()
      if(timeDiffSecs >= 7200):
        print("shuting down "+ activehost['hostName'] +" : "+ str(activehost['idleLast']) + " : "+ str(timeDiffSecs))
        hostDet = rbhus.utils.hosts(activehost['ip'])
        hostDet.shutdownSys()
  else:
    deadHosts = rbhus.dbRbhus.dbRbhus().getDeadHosts()
    for deadHost in deadHosts:
      macc = getMaccAddr(deadHost['hostName'])
      if(macc):
        print("trying to bring up "+ deadHost['hostName'] +"  :  "+ str(macc))
        rbhus.WOL.send_magic_packet(macc,ip_address=rbhus.WOL.BROADCAST_IP, port=rbhus.WOL.DEFAULT_PORT)
  time.sleep(10)




