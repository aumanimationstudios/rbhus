#!/usr/bin/env python2
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys
import os
import re
import time
import argparse

fileDir = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-1])
baseDir = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-4])

sys.path.append(baseDir)

import rbhus.utilsPipe
import rbhus.debug
import rbhus.constantsPipe
import rbhus.dbPipe



parser = argparse.ArgumentParser()
parser.add_argument("-a","--all",dest='all',action="store_true")
parser.add_argument("-p","--projects",dest='projects',help="comma seperated list of projects to backup")
args = parser.parse_args()

dbproj = rbhus.dbPipe.dbPipe()
projs = dbproj.execute("select * from projModifies where date(modified) > DATE_SUB(CURDATE(), INTERVAL 7 DAY)",dictionary=True)

if(projs):
  for x in projs:
    print(x)
# getProjForBackup = rbhus.
sys.exit(0)

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


def setAssetDone(assPath):
  project = assPath.split(":")[0]
  asspathfd = open("/tmp/"+ project,"a+")
  asspathfd.write(assPath +"\n")
  asspathfd.flush()
  asspathfd.close()


def isAssetDone(assPath):
  project = assPath.split(":")[0]
  if(os.path.exists("/tmp/" + project)):
    asspathfd = open("/tmp/" + project, "r")
    for x in asspathfd.readlines():
      # print(x.strip())
      if(x.strip() == assPath):
        return(True)
    asspathfd.close()
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
  allProj = []
  checkIfBackup = False
  if(args.projects):
    # print(args.projects)
    projects = args.projects.split(",")
    for p in projects:
      projDet = rbhus.utilsPipe.getProjDetails(p.strip())
      if(projDet):
        allProj.append(projDet)
      else:
        rbhus.debug.warning("bad project name : "+ str(p))
  else:
    allProj = rbhus.utilsPipe.getAllProjects(status=rbhus.constantsPipe.projActive)
    checkIfBackup = True

  for proj in allProj:
    doBackup = False
    if(checkIfBackup):
      if(proj['backup']):
        doBackup = True
    else:
      doBackup = True
    print(proj['projName'] +" : "+ str(doBackup))

    if(doBackup):
      allAssets = rbhus.utilsPipe.getProjAsses(proj['projName'])
      if(allAssets):

        for x in allAssets:
          if(isAssetDone(x['path'])):
            continue
          toBackup = False
          if(x['assetType'] == "output"):
            if(args.all):
              toBackup = True
            else:
              if(x['assName'] == "Rendered_SF" or x['assName'] == "Movs"):
                toBackup = True
          else:
            toBackup = True
          if(toBackup):
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
              setAssetDone(x['path'])
              rbhus.debug.info(x['path'] +" "+ str(exitValue))
except:
  rbhus.debug.error(str(sys.exc_info()))
