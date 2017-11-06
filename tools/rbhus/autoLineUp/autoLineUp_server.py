#!/usr/bin/env python2
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys
import os
import time
projDir = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-4])


sys.path.append(projDir)

import rbhus.dbPipe
import rbhus.constantsPipe


autoLineUp_anim_cmd = os.path.join(projDir,"tools","rbhus","autoLineUp","autoLineUp_anim.py")
autoLineUp_light_cmd = os.path.join(projDir,"tools","rbhus","autoLineUp","autoLineUp_light.py")

while(True):
  dbcon = rbhus.dbPipe.dbPipe()
  rows = dbcon.execute("select * from proj where status='{0}' and (autoLineUpAnim=1 or autoLineUpLight=1)".format(rbhus.constantsPipe.projActive),dictionary=True)
  # print(rows)
  if(rows):
    for x in rows:
      if(x["autoLineUpAnim"] == 1):
        cmd = autoLineUp_anim_cmd +" "+ x["projName"]
        cmdRet = os.system(cmd)
        print(cmdRet)
      if (x["autoLineUpLight"] == 1):
        cmd = autoLineUp_light_cmd + " " + x["projName"]
        cmdRet = os.system(cmd)
        print(cmdRet)

  time.sleep(900)






