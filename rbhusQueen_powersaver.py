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

timeformat = '%Y-%m-%d %H:%M:%S.%f'
while(True):
  allActiveHosts = rbhus.dbRbhus.dbRbhus().getPotentHosts()
  allActiveTasks = rbhus.dbRbhus.dbRbhus().getAllActiveTasks()
  # if(not allActiveTasks):
  if(not allActiveTasks):
    for activehost in allActiveHosts:
      # print(activehost['hostName'] + " : " + str(activehost['idleLast']))
      timeNow = datetime.datetime.now()
      timeDiff = timeNow - datetime.datetime.strptime(str(activehost['idleLast']),timeformat)
      timeDiffSecs = timeDiff.total_seconds()
      if(timeDiffSecs >= 7200):
        print(activehost['hostName'] +" : "+ str(activehost['idleLast']) + " : "+ str(timeDiffSecs))
        hostDet = rbhus.utils.hosts(activehost['ip'])
        hostDet.shutdownSys()
  time.sleep(2)

