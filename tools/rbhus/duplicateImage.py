#!/usr/bin/env python2
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys
import os
import argparse
import shutil

parser = argparse.ArgumentParser(description="Command should be run on master")
parser.add_argument("-i","--image",dest="image",help="image to duplicate")
parser.add_argument("-s","--start",dest="start",help="start number")
parser.add_argument("-e","--end",dest="end",help="end number")
parser.add_argument("-p","--pad",dest="pad",help="padding for number")
args = parser.parse_args()


imagePath = os.path.abspath(args.image)
imageDir = os.path.split(imagePath)[0]
imageExt = imagePath.split(".")[-1]
print(imageExt)
startNum = int(args.start)
endNum = int(args.end)
pad = int(args.pad)


for x in range(startNum,endNum+1):
  imageName = str(x).zfill(pad)
  dest = os.path.join(imageDir,imageName +"."+ imageExt)
  cmd = "cp -v "+ imagePath +" "+ dest
  os.system(cmd)






