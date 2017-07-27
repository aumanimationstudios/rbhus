#!/usr/bin/env python2
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

#todo : please complete this script asap

import sys
import os
import glob


path = os.path.abspath(sys.argv[1])

movs = glob.glob(os.path.join(path,"*.mov"))
movs.sort()
path1080 = os.path.join(path,"1080p")
try:
  os.makedirs(path1080)
except:
  pass

for mov in movs:
  only_mov = os.path.split(mov)[-1]
  final_mov = os.path.join(path1080,only_mov)
  os.system("ffmpeg -i "+ mov +" -vf scale=1920:-1 "+ final_mov +" -y")



