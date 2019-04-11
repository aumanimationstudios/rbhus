#!/usr/bin/env python2
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys
import os
import time

filedir = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-1])
print(filedir)
sys.path.append(filedir)
import rbhus.dbRbhus
import rbhus.debug
import rbhus.utils

while(True):
  allActiveHosts = rbhus.dbRbhus.dbRbhus().getPotentHosts()
  for activehost in allActiveHosts:
    print(activehost['idleLast'])
  time.sleep(2)

