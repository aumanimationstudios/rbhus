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

try:
  projName = sys.argv[1]
except:
  projName = "AndePirki_se01_ep013_fruitCause"
seqScns = rbhus.utilsPipe.getSequenceScenes(projName)


autoLineUpAssPath = projName +":share:autoLineUp"


autoLineUpAbsPath = rbhus.utilsPipe.getAbsPath(autoLineUpAssPath)

def getTimeSortedDirs(dirPath):
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


if(autoLineUpAbsPath):
  autoLineUpFile_inProgress = os.path.join(autoLineUpAbsPath,".light_autoLineUp_inprogress.mp4")
  autoLineUpFile = os.path.join(autoLineUpAbsPath,"light_autoLineUp.mp4")
  ffmpegFile = os.path.join(autoLineUpAbsPath,"light_autoLineUp.ffmpeg")
  ffmpegFileFd = open(ffmpegFile,"w")

  for x in seqScns:
    # print(x['sequenceName'],x['sceneName'])
    if (not re.search("^default$", x['sequenceName'])):
      if (not re.search("^default$", x['sceneName'])):
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
        status = rbhus.utilsPipe.getAssStatus(assPath)
        if (status == rbhus.constantsPipe.assetStatusActive):
          assAbsPath = rbhus.utilsPipe.getAbsPath(assPath)
          isLightMain = True
          if(assAbsPath):
            assFIleName = rbhus.utilsPipe.getAssFileName(asset)
            outputDir1 = os.path.join(assAbsPath, assFIleName)
            outputDir2 = getLatestDir(outputDir1)
            if(os.path.exists(outputDir2)):
              latestDir = getTimeSortedDirs(outputDir2)
              latestDir.reverse()
              Mov = None
              for x in latestDir:
                if(x):
                  Mov = os.path.join(x, assFIleName + ".mp4")
                  if(os.path.exists(Mov)):
                    break
                  else:
                    Mov = None
                    continue

              if(Mov):
                # finalMov = os.path.join(latestDir, assFIleName + ".mp4")
                finalMov = Mov
                # MovMp4Cmd = "ffmpeg -y -r 24 -i "+ Mov +" -vcodec h264 -vf scale=1280:720 "+ finalMov
                # os.system(MovMp4Cmd)
                if (os.path.exists(finalMov)):
                  print(finalMov)
                  ffmpegFileFd.write("file\t\'" + finalMov + "\'\n")
                else:
                  isLightMain = False
              else:
                isLightMain = False
            else:
              isLightMain = False
          else:
            isLightMain = False
        else:
          isLightMain = False

        if(not isLightMain):
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
          if (status == rbhus.constantsPipe.assetStatusActive):
            assAbsPath = rbhus.utilsPipe.getAbsPath(assPath)
            assFIleName = rbhus.utilsPipe.getAssFileName(asset)
            finalMov = os.path.join(assAbsPath, assFIleName + ".mp4")
            if (os.path.exists(finalMov)):
              print(finalMov)
              ffmpegFileFd.write("file\t\'" + finalMov + "\'\n")
            else:
              print(finalMov,"not found")
              asset["nodeType"] = "previz"
              assPath = rbhus.utilsPipe.getAssPath(asset)
              assAbsPath = rbhus.utilsPipe.getAbsPath(assPath)
              assFIleName = rbhus.utilsPipe.getAssFileName(asset)
              finalMov = os.path.join(assAbsPath, assFIleName + ".mp4")
              if (os.path.exists(finalMov)):
                print(finalMov)
                ffmpegFileFd.write("file\t\'" + finalMov + "\'\n")
              else:
                print(finalMov, "not found")

  ffmpegFileFd.flush()
  ffmpegFileFd.close()
  print(ffmpegFile)


  ffmpegCmd = "ffmpeg -y -f concat -safe 0 -auto_convert 1 -i "+ ffmpegFile +" -an -vcodec h264 -vf scale=1280:720 "+ autoLineUpFile_inProgress
  out = os.system(ffmpegCmd)
  os.system("mv "+ autoLineUpFile_inProgress +" "+ autoLineUpFile)
  print(out)
  exit(out)
else:
  print(autoLineUpAssPath +" NOT FOUND")
  exit(666)
#
