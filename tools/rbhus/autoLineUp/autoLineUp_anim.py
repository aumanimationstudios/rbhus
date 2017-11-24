#!/usr/bin/env python2
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys
import os
import re

print(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-4]))

sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-4]))
import rbhus.utilsPipe
import rbhus.constantsPipe

try:
  projName = sys.argv[1]
except:
  projName = "AndePirki_se01_ep013_fruitCause"
seqScns = rbhus.utilsPipe.getSequenceScenes(projName)


autoLineUpAssPath = projName +":share:autoLineUp"

autoLineUpAbsPath = rbhus.utilsPipe.getAbsPath(autoLineUpAssPath)
if(autoLineUpAbsPath):
  autoLineUpFile_inProgress = os.path.join(autoLineUpAbsPath,".anim_autoLineUp_inprogress.mp4")
  autoLineUpFile = os.path.join(autoLineUpAbsPath,"anim_autoLineUp.mp4")
  ffmpegFile = os.path.join(autoLineUpAbsPath,"anim_autoLineUp.ffmpeg")
  ffmpegFileFd = open(ffmpegFile,"w")

  for x in seqScns:
    # print(x['sequenceName'],x['sceneName'])
    if (not re.search("^default$", x['sequenceName'])):
      if (not re.search("^default$", x['sceneName'])):
        asset = {
          "projName"    : projName,
          "assetType"   : "default",
          "sequenceName": x['sequenceName'],
          "sceneName"   : x['sceneName'],
          "stageType"   : "anim",
          "nodeType"    : "primary",
          "fileType"    : "blend"
        }
        assPath = rbhus.utilsPipe.getAssPath(asset)
        status = rbhus.utilsPipe.getAssStatus(assPath)
        if(status == rbhus.constantsPipe.assetStatusActive):

          assAbsPath = rbhus.utilsPipe.getAbsPath(assPath)
          assFIleName = rbhus.utilsPipe.getAssFileName(asset)
          finalMov = os.path.join(assAbsPath, assFIleName + ".mp4")
          if (os.path.exists(finalMov)):
            print(finalMov)
            ffmpegFileFd.write(finalMov + "\n")
          else:
            # print(finalMov,"not found")
            asset["nodeType"] = "previz"
            assPath = rbhus.utilsPipe.getAssPath(asset)
            assAbsPath = rbhus.utilsPipe.getAbsPath(assPath)
            assFIleName = rbhus.utilsPipe.getAssFileName(asset)
            finalMov = os.path.join(assAbsPath, assFIleName + ".mp4")
            if (os.path.exists(finalMov)):
              print(finalMov)
              ffmpegFileFd.write(finalMov + "\n")
            else:
              print(finalMov, "not found")

  ffmpegFileFd.flush()
  ffmpegFileFd.close()

  print(autoLineUpFile)


  ffmpegCmd = "melt melt_file:"+ ffmpegFile +" -consumer avformat:"+ autoLineUpFile_inProgress +" vcodec=libx264 r=24"
  out = os.system(ffmpegCmd)
  os.system("mv " + autoLineUpFile_inProgress + " " + autoLineUpFile)
  print(out)
  exit(out)
else:
  print(autoLineUpAssPath +" NOT FOUND")
  exit(666)
