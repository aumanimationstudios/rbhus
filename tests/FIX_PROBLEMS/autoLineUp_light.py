#!/usr/bin/env python2
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys
import os
import re

mainPath = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-3])
convert_to_prores = os.path.join(mainPath,"tools","rbhus","convert_exr_mov_prores.py")

sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-3]))
import rbhus.utilsPipe

try:
  projName = sys.argv[1]
except:
  projName = "AndePirki_se01_ep013_fruitCause"
seqScns = rbhus.utilsPipe.getSequenceScenes(projName)



def getLatestDirsSorted(dirPath):
  all_subdirs = [os.path.join(dirPath,x) for x in os.listdir(dirPath) if(os.path.isdir(os.path.join(dirPath,x)) and x.isdigit())]
  if(all_subdirs):
    latest_subdir = sorted(all_subdirs, key=os.path.getmtime)
    # print(latest_subdir)
    return(latest_subdir)
  else:
    return(False)


def getLatestDir(dirPath):
  all_subdirs = [os.path.join(dirPath,x) for x in os.listdir(dirPath) if(os.path.isdir(os.path.join(dirPath,x)))]
  if(all_subdirs):
    latest_subdir = max(all_subdirs, key=os.path.getmtime)
    return(latest_subdir)
  else:
    return(False)

for x in seqScns:
  # print(x['sequenceName'],x['sceneName'])
  if (not re.search("^default$", x['sequenceName'])) and (not re.search("^default$", x['sceneName'])):
    asset = {
      "projName"    : projName,
      "assetType"   : "output",
      "sequenceName": x['sequenceName'],
      "sceneName"   : x['sceneName'],
      "stageType"   : "light",
      "nodeType"    : "main",
      "fileType"    : "blend"
    }
    assPath = rbhus.utilsPipe.getAssPath(asset)
    assAbsPath = rbhus.utilsPipe.getAbsPath(assPath)
    isLightMain = True
    if(assAbsPath):
      assFIleName = rbhus.utilsPipe.getAssFileName(asset)
      outputDir1 = os.path.join(assAbsPath, assFIleName)
      # print(outputDir1)
      outputDir2 = getLatestDir(outputDir1)
      # print(outputDir2)
      if(os.path.exists(outputDir2)):
        latestDir = getLatestDirsSorted(outputDir2)
        latestDir.reverse()
        Mov = None
        latestMovDir = None
        for x in latestDir:
          if(x):
            Mov = os.path.join(x, assFIleName + ".mov")
            if(os.path.exists(Mov)):
              latestMovDir = x
              break
            else:
              Mov = None
              continue

        if(latestMovDir):

          os.system(convert_to_prores +" "+latestMovDir)

