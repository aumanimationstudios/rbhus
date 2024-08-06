#!/usr/bin/env python3

import glob
import os
import posix
import pwd
import time
import fcntl
import shutil
import sys
from collections import OrderedDict

class _versionInfo:
  def __init__(self,verNum=None,verUser=None,verDesc=None,verDate=None,verTag=None):
    self.vNum = verNum
    self.vDesc = verDesc
    self.vUser = verUser
    self.vDate = verDate
    self.vTag = verTag

class polymorph:
  def __init__(self,pathName):
    #self._rsync = '/usr/bin/rsync'
    self._initPath = os.path.abspath(pathName)+ os.sep
    self._pmBaseDir = self._initPath + ".pm"
    self._pmVerDir = self._pmBaseDir + os.sep +"v"+ os.sep
    self._pmTags = self._pmBaseDir + os.sep +"tags"+ os.sep
    self._pmParent = self._pmBaseDir + os.sep +"parent"
    self._pmBranch = self._pmBaseDir + os.sep +"branch"
    self._pmExcludePaths = self._pmBaseDir + os.sep +"exclude"
    self._pmTip = self._pmBaseDir + os.sep +"tip"
    self._pmLock = self._pmBaseDir + os.sep +"lock"
    self._verDetails = self._vPopulate()
    self._excludePaths = (".pm*","publish*","import*")
    self.getExcludepaths()
    self._tip = self._readTip()
    
    
  def getTip(self):
    return(self._tip)
    
  
  def getVersions(self):
    return(self._verDetails)
    
  def getExcludepaths(self):
    ep = open(self._pmExcludePaths,"r")
    exp = {}
    for x in ep.readlines():
      if(x.rstrip().lstrip()):
        exp[x] = 1
    for y in self._excludePaths:
      if(y.rstrip().lstrip()):
        exp[y] = 1
      
    print("wtf 1")
    self._excludePaths = tuple(OrderedDict.fromkeys([z.rstrip().lstrip() for z in exp]))
    print("wtf 2")
    
  
  def getBranchName(self):
    return(self._readBranchName())
    
  def create(self,branch="default"):
    try:
      os.makedirs(self._pmVerDir,mode=0o777)
      os.makedirs(self._pmTags,mode=0o777)
      lockFD = open(self._pmLock,"w",0)
      lockFD.close()
    except:
      print(str(sys.exc_info()))
      #self._createCleanUp()
      return(0)
    try:
      self._writeBranchName(branch)
    except:
      print(str(sys.exc_info()))
      #self._createCleanUp()
      return(0)
    return(1)
    
  def commit(self,msg="No comments!!",cUser=pwd.getpwuid(os.getuid()).pw_name):
    if(os.path.exists(self._pmBaseDir)):
      if(self._getLock()):
        vTip = self._readTip()
        if(vTip == None):
          vTip = 1
        else:
          vTip = int(vTip) + 1
        try:
          self._versionUp(vTip)
          self._writeVerDate(vTip,time.asctime())
          self._writeVerDesc(vTip,msg)
          self._writeVerUser(vTip,cUser)
        except:
          print(str(sys.exc_info()))
          try:
            self._delVer(vTip)
          except:
            pass
          self._freeLock()
          return(0)
        self._freeLock()
        self._updateDetails()
        return(vTip)
        
        
  def work(self,vNum):
    verNum = str(vNum)
    if(self._verExists(vNum)):
      wVerUp = self.commit(msg="work_autocommit:"+ str(vNum))
      if(wVerUp):
        if(self._getLock()):
          try:
            vNumDir = self._pmVerDir + str(vNum)
            vNumDirFiles = glob.glob(vNumDir + os.sep + "*")
            if(vNumDirFiles):
              for f in vNumDirFiles:
                if(os.path.exists(f)):
                  lastFile = f.split(os.sep)[-1]
                  #shutil.move(self._initPath + lastFile,self._initPath + lastFile + ".bak")
                  if(os.path.isdir(f)):
                    shutil.rmtree(self._initPath + lastFile)
                    shutil.copytree(f + os.sep,self._initPath + lastFile,ignore=shutil.ignore_patterns(self._excludePaths))
                  else:
                    shutil.copy(f,self._initPath + lastFile)
          except:
            print(str(sys.exc_info()))
            self._freeLock()
            return(0)
          self._freeLock()
      self._updateDetails()
      return(1)
    else:
      print("No valid version : "+ str(vNum))
      return(0)
        
        
  def publish(self,vNum,pDir=None):
    if(self._getLock()):
      try:
        self._writeVerTag(vNum,tag="publish")
      except:
        print(str(sys.exc_info()))
        self._freeLock()
        return(0)
      self._freeLock()
    if(pDir):
      try:
        self._export(vNum,pDir)
      except:
        print(str(sys.exc_info()))
        return(0)
    self._updateDetails()
    return(1)
    
  
  def delVersion(self,vNum):
    if(self._verExists(vNum)):
      print("pass1")
      if(self._getLock()):
        print("pass2")
        try:
          self._delVer(vNum)
        except:
          return(0)
        print("pass3")
        try:
          self._delVerTag(vNum)
        except:
          return(0)
        print("pass4")
        self._freeLock()
        self._updateDetails()
        return(1)
    else:
      print("No valid version : "+ str(vNum))
      return(0)
        
        
  def tag(self,vNum,tagName):
    try:
      self._writeVerTag(vNum,tagName)
    except:
      print(str(sys.exc_info()))
      return(0)
    self._updateDetails()
    return(1)
    
    
  def delTag(self,tagName):
    try:
      self._delTag(tagName)
    except:
      print(str(sys.exc_info()))
      self._updateDetails()
      return(0)
    self._updateDetails()
    return(1)
    
    
  def _verExists(self,ver):
    vers = self._vPopulate()
    try:
      test = vers[int(ver)]
      return(1)
    except:
      return(0)
   
  
  def _updateDetails(self):
    self._tip = self._getTip()
    if(self._tip):
      try:
        self._writeTip(self._tip)
      except:
        return(0)
    self._verDetails = self._vPopulate()
    return(1)
    
    
  
  def _export(self,ver,eDir):
    absDir = os.path.abspath(eDir)+ os.sep
    if(os.path.exists(absDir)):
      try:
        shutil.rmtree(absDir)
      except:
        pass
    try:
      shutil.copytree(self._pmVerDir + str(ver),absDir,ignore=shutil.ignore_patterns(self._excludePaths))
    except:
      raise
    return(1)
  
  def _versionUp(self,vTip):
    verUpDir = self._pmVerDir + str(vTip)
    try:
      print("wtf 3")
      shutil.copytree(self._initPath,verUpDir,ignore=shutil.ignore_patterns(self._excludePaths))
      print("wtf 4")
      self._writeTip(vTip)
    except:
      print(str(sys.exc_info()))
      raise
    return(1)


  def _delVer(self,ver):
    verPath = self._pmVerDir + str(ver)
    print(verPath)
    try:
      shutil.rmtree(verPath + os.sep)
      os.remove(verPath +".desc")
      os.remove(verPath +".user")
      os.remove(verPath +".date")
    except:
      print(str(sys.exc_info()))
      raise
    return(1)
  
  
  def _createCleanUp(self):
    try:
      shutil.rmtree(self._pmBaseDir)
    except:
      print(str(sys.exc_info()))
      return(0)
    return(1)
  
  
  def _getLock(self):
    lockFD = open(self._pmLock)
    fcntl.flock(lockFD,fcntl.LOCK_EX)
    return(1)
    
    
    
  def _freeLock(self):
    lockFD = open(self._pmLock)
    fcntl.flock(lockFD,fcntl.LOCK_UN)
    return(1)
      
    
  # Return a dict with version number as the key
  def _vPopulate(self):
    if(os.path.exists(self._pmBaseDir)):
      versions = glob.glob(self._pmVerDir +"*")
      vS = {}
      if(versions):
        for version in versions:
          if(os.path.isdir(version)):
            verNum = int(version.split(os.sep)[-1])
            verDesc = self._readVerDesc(str(verNum))
            verTag = self._readVerTag(str(verNum))
            verDate = self._readVerDate(str(verNum))
            verUser = self._readVerUser(str(verNum))
            vS[verNum] = _versionInfo(verNum,verUser,verDesc,verDate,verTag)
        return(vS)
      else:
        return(None)
    return(None)
    
          
      
  def _writeTip(self,ver):
    try:
      verTipFD = open(self._pmTip,"w",0)
    except:
      raise
    try:
      verTipFD.write(str(ver))
    except:
      verTipFD.close()
      raise
    verTipFD.close()
    return(1)
    
    
  def _readTip(self):
    try:
      verTipFD = open(self._pmTip,"r")
    except:
      return(None)
    try:
      tVer = verTipFD.readline()
    except:
      verTipFD.close()
      return(None)
    verTipFD.close()
    return(tVer)
    
    
  def _getTip(self):
    verDets = self._vPopulate()
    if(verDets):
      tip = max(verDets.keys())
      return(tip)
    else:
      return(None)
   
    
  def _writeVerUser(self,ver,vUser):
    try:
      verUserFD = open(self._pmVerDir + str(ver) +".user","w",0)
    except:
      raise
    try:
      verUserFD.write(vUser)
    except:
      verUserFD.close()
      raise
    verUserFD.close()
    return(1)
    
    
  def _readVerUser(self,ver):
    try:
      verUserFD = open(self._pmVerDir + str(ver) +".user","r")
    except:
      return(None)
    try:
      vUser = verUserFD.readline()
    except:
      verUserFD.close()
      return(None)
    verUserFD.close()
    return(vUser)
  
  
  def _writeVerDate(self,ver,vDate):
    try:
      verDateFD = open(self._pmVerDir + str(ver) +".date","w",0)
    except:
      raise
    try:
      verDateFD.write(vDate)
    except:
      verDateFD.close()
      raise
    verDateFD.close()
    return(1)
  
  
  def _readVerDate(self,ver):
    try:
      verDateFD = open(self._pmVerDir + str(ver) +".date","r")
    except:
      return(None)
    try:
      vDate = verDateFD.readline()
    except:
      verDateFD.close()
      return(None)
    verDateFD.close()
    return(vDate)
  
  
  def _writeVerTag(self,ver,tag):
    try:
      verTagFD = open(self._pmTags + tag,"w",0)
    except:
      raise
    try:
      verTagFD.write(str(ver))
    except:
      verTagFD.close()
      raise
    verTagFD.close()
    return(1)
    
    
  def _readVerTag(self,ver):
    tags = glob.glob(self._pmTags +"*")
    tTag = []
    rTag = None
    if(tags):
      for tag in tags:
        try:
          verTagFD = open(tag,"r")
        except:
          continue
        try:
          vNum = verTagFD.readline()
        except:
          verTagFD.close()
          continue
        verTagFD.close()
        if(int(vNum) == int(ver)):
          tTag.append(tag.rsplit(os.sep)[-1])
      if(tTag):
        rTag = ",".join(tTag)
    return(rTag)
    
    
  def _readTagVer(self,tag):
    tagFile = self._pmTags + tag
    try:
      tagFD = open(tagFile,"r")
    except:
      raise
    try:
      ver = tagFD.readline()
    except:
      tagFD.close()
      raise
    return(ver)
    
    
  def _delTag(self,tag):
    tagFile = self._pmTags + tag
    if(os.path.exists(tagFile)):
      try:
        os.remove(tagFile)
      except:
        raise
    else:
      return(0)
    return(1)
    
    
  def _delVerTag(self,ver):
    tags = glob.glob(self._pmTags +"*")
    if(tags):
      for tag in tags:
        try:
          verTagFD = open(tag,"r")
        except:
          continue
        try:
          vNum = verTagFD.readline()
        except:
          verTagFD.close()
          continue
        verTagFD.close()
        if(int(vNum) == int(ver)):
          try:
            self._delTag(tag.rsplit(os.sep)[-1])
          except:
            raise
    return(1)
    
    
  def _writeVerDesc(self,ver,desc):
    try:
      verDescFD = open(self._pmVerDir + str(ver) +".desc","w",0)
    except:
      raise
    try:
      verDescFD.write(desc)
    except:
      verDescFD.close()
      raise
    verDescFD.close()
    return(1)
    
    
  def _readVerDesc(self,ver):
    try:
      verDescFD = open(self._pmVerDir + str(ver) +".desc","r")
    except:
      return(None)
    try:
      desc = verDescFD.readline()
    except:
      verDescFD.close()
      return(None)
    verDescFD.close()
    return(desc)
    
      
  def _writeBranchName(self,branchName):
    try:
      branchFd = open(self._pmBranch,"w",0)
    except:
      raise
    try:
      branchFd.write(branchName)
    except:
      branchFd.close()
      raise
    branchFd.close()
    return(1)

    
  def _readBranchName(self):
    try:
      branchFd = open(self._pmBranch,"r",0)
    except:
      return(None)
    try:
      branchName = branchFd.readline()
    except:
      branchFd.close()
      return(None)
    branchFd.close()
    return(branchName)
    
    
  def _writeParent(self,parentPath):
    try:
      parentFd = open(self._pmParent,"w",0)
    except:
      raise
    try:
      parentFd.write(parentPath)
    except:
      parentFd.close()
      raise
    parentFd.close()
    return(1)
    

  def _readParent(self):
    try:
      parentFd = open(self._pmParent,"r")
    except:
      return(None)
    try:
      parentPath = parentFd.readline()
    except:
      parentFd.close
      return(None)
    parentFd.close
    return(parentPath)
      
    
    
    
  