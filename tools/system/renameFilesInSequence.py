#!/usr/bin/env python2
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys
import os
import collections


import glob

dir = os.path.abspath(sys.argv[1])
extention = sys.argv[2]
finalDir = sys.argv[3]
print(dir, extention)
globedFiles = glob.glob(os.path.join(dir, "*." + extention))
# print(globedFiles)

fileDict = {}

for x in globedFiles:
  file1 = os.path.relpath(x, dir)
  file2 = file1.split(".")
  file3 = ".".join(file2[:-1])
  fileDict[int(file3)] = x

fileKeysSorted = fileDict.keys()
fileKeysSorted.sort()
i = 1
for x in fileKeysSorted:
  cmd = "cp -v " + fileDict[x] +" " + os.path.join(finalDir, str(i).rjust(4, "0") + "." + extention)
  print(cmd)
  os.system(cmd)

  i += 1
