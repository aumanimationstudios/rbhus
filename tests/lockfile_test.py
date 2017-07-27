#!/usr/bin/env python2
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys
import os

sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-1]))

import lockfile
import time

locky = lockfile.LockFile("/tmp/testinglock_file",timeout=0)
try:
  with locky:
    fd = open("/tmp/testinglock_file","w")
    fd.write(str(time.time()))
    fd.flush()
    fd.close()
    time.sleep(5)
except:
  print("wtf timeout")

