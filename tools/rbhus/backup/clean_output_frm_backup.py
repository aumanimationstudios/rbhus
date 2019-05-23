#!/usr/bin/env python2
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys
import os

sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-1]))


fileDir = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-1])
baseDir = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-4])

sys.path.append(baseDir)

import rbhus.utilsPipe
import rbhus.debug
import rbhus.constantsPipe
import rbhus.dbPipe


def isValidBackupDir(directory):
  allDirMaps = rbhus.utilsPipe.getDirMaps(dirType="backup")
  if(allDirMaps):
    for x in allDirMaps:
      if(x['directory'] == directory):
        return(True)
  return(False)


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
      print(x)
      # os.system("rm -fr "+ x)

    print("PRESERVING : "+ str(len(toPreserve)))
    # for x in toPreserve:
      # print(x)


dbcon = rbhus.dbPipe.dbPipe()

rows = dbcon.execute("select * from assets where assetType=\'output\'",dictionary=True)
for x in rows:
  if (isValidBackupDir(x['backupDir'])):
    dirMapDets = rbhus.utilsPipe.getDirMapsDetails(x['backupDir'])
    pathSrcBackup = rbhus.utilsPipe.getAbsPath(x['path']).rstrip(os.sep) + os.sep
    pathDestBackup = os.path.join(dirMapDets['linuxMapping'], x['projName'], x['assetId']).rstrip(os.sep) + os.sep
    if(os.path.exists(pathDestBackup)):
      print(pathDestBackup)


