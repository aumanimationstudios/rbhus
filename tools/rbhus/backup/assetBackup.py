#!/usr/bin/env python2
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys
import os
import re
import time

fileDir = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-1])
baseDir = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-4])

sys.path.append(baseDir)

import rbhus.utilsPipe
import rbhus.debug
import rbhus.constantsPipe


def isValidBackupDir(directory):
  allDirMaps = rbhus.utilsPipe.getDirMaps(dirType="backup")
  if(allDirMaps):
    for x in allDirMaps:
      if(x['directory'] == directory):
        return(True)
  return(False)


def getCompoundPaths(assPath,allAssets,isVersion=False):
  pathSrcBackup = rbhus.utilsPipe.getAbsPath(assPath)
  retpaths = []
  for x in allAssets:
    pathToX = rbhus.utilsPipe.getAbsPath(x['path'])
    if(pathSrcBackup != pathToX):
      if(os.path.exists(pathToX)):
        if(re.search(pathSrcBackup,pathToX)):
          if(isVersion):
            if(isVersioning(pathToX)):
              retpaths.append(pathToX)
          else:
            retpaths.append(pathToX)
  return(retpaths)


def sortKey(value):
  try:
    # print(value.split(os.sep)[-1])
    return(float(value.split(os.sep)[-1]))
  except:
    print("wtf")
    return(0.0)


def getTimeSortedDirs(dirPath):
  all_subdirs = [os.path.join(dirPath,x) for x in os.listdir(dirPath) if(os.path.isdir(os.path.join(dirPath,x)))]

  if(all_subdirs):
    # latest_subdir = sorted(all_subdirs, key=os.path.getmtime,reverse=True)
    latest_subdir = sorted(all_subdirs, key=sortKey, reverse=True)
    # latest_subdir = all_subdirs.sort()

    # rbhus.debug.info(latest_subdir)
    return(latest_subdir)
  else:
    return(False)

def cleanBackUp(assDets):
  dirMapDets = rbhus.utilsPipe.getDirMapsDetails(assDets['backupDir'])
  pathDestBackupBase = os.path.join(dirMapDets['linuxMapping'],assDets['projName'],assDets['assetId'])
  sortedPaths = getTimeSortedDirs(pathDestBackupBase)
  if(sortedPaths):
    totalBacked = len(sortedPaths)
    toPreserve = sortedPaths[:int(assDets['backupCountToRetain'])]
    toDelLen = totalBacked - int(assDets['backupCountToRetain'])
    if(toDelLen <= 0):
      toDelete = []
    else:
      toDelete = sortedPaths[-toDelLen:]
    print("DELETING : "+ str(len(toDelete)))
    for x in toDelete:
      # print(x)
      os.system("rm -fr "+ x)

    print("PRESERVING : "+ str(len(toPreserve)))
    # for x in toPreserve:
      # print(x)



def isVersioning(absPath):
  if (os.path.exists(absPath + "/.hg")):
    rbhus.debug.info("versioning main : true")
    return (True)
  else:
    rbhus.debug.info("versioning main : false")
    return (False)

try:
  allProj = rbhus.utilsPipe.getAllProjects(status=rbhus.constantsPipe.projActive)
  for proj in allProj:
    if(proj['backup']):

      allAssets = rbhus.utilsPipe.getProjAsses(proj['projName'])

      for x in allAssets:
        if(x['assetType'] != "output"):
          if(isValidBackupDir(x['backupDir'])):
            dirMapDets = rbhus.utilsPipe.getDirMapsDetails(x['backupDir'])
            pathSrcBackup = rbhus.utilsPipe.getAbsPath(x['path']).rstrip(os.sep) + os.sep
            pathDestBackup = os.path.join(dirMapDets['linuxMapping'],x['projName'],x['assetId'],str(time.time())).rstrip(os.sep) + os.sep
            # cmdStr = "rsync -a "+ pathSrcBackup +" {0} "+ pathDestBackup
            cmpdAsses = getCompoundPaths(x['path'],allAssets)
            if(cmpdAsses):
              cmpdAssesStr ="--exclude=.hg* --exclude=.thumbz.db --exclude="+" --exclude=".join(cmpdAsses)
              cmdFinal = "rsync -a "+ pathSrcBackup +" "+ cmpdAssesStr +" "+ pathDestBackup
            else:
              cmdFinal = "rsync -a "+ pathSrcBackup +" --exclude=.hg* --exclude=.thumbz.db "+ pathDestBackup
              os.makedirs(pathDestBackup)
              try:
                exitValue = os.system(cmdFinal)
                # exitValue = 666
              except:
                exitValue = 666
            # print(cmdFinal)
            # print(x)
            try:
              cleanBackUp(x)
            except:
              print(sys.exc_info())

            rbhus.debug.info(x['path'] +" "+ str(exitValue))
except:
  rbhus.debug.error(str(sys.exc_info()))
