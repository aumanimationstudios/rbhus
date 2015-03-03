import sys
import os
from os.path import expanduser
import multiprocessing
import shutil
import subprocess

from xml.dom import minidom





dirSelf = os.path.dirname(os.path.realpath(__file__))
etcMercurial = dirSelf.split(os.sep)[:-1]
etcMercurial.append("etc")
etcMercurial.append("mercurial")
hgrcHome = os.sep.join(etcMercurial) + os.sep +"home"+ os.sep +".hgrc"
hgrcLocalLinux = os.sep.join(etcMercurial) + os.sep +"local"+ os.sep +"hgrc.linux"
hgrcLocalWindows = os.sep.join(etcMercurial) + os.sep +"local"+ os.sep +"hgrc.windows"
localCacheLinux = "/crap/versionCache/"+ os.environ['rbhusPipe_acl_user'] +"/"
localCacheWindows = "D:/versionCache/"+ os.environ['rbhusPipe_acl_user'] +"/"

import dbPipe
import constantsPipe
import utilsPipe



class hg(object):
  
  def __init__(self,pipePath):
    self.pipepath = pipePath
    self.absPipePath = utilsPipe.getAbsPath(pipePath)
    
    self.localPath = None
    if(sys.platform.find("linux") >= 0):
      self.localPath =  localCacheLinux + "/".join(str(pipePath).split(":"))
    elif(sys.platform.find("win") >= 0):
      self.localPath = localCacheWindows + "/".join(str(pipePath).split(":"))
    
    self._copyHomeConfig()
    self.isMainInitialized()
    print(self.localPath)
    try:
      os.makedirs(self.localPath)
    except:
      print(sys.exc_info())
    #self.initialize()
    #os.chdir(self.localPath)
    #self.initializeLocal()
    
    
    
    
  
  
  def isMainInitialized(self):
    if(os.path.exists(self.absPipePath +"/.hg")):
      print("versioning main : true")
      return(True)
    else:
      print("versioning main : false")
      return(False)
    
    
  def isLocalInitialized(self):
    if(os.path.exists(self.localPath +"/.hg")):
      print("versioning  local : true")
      return(True)
    else:
      print("versioning local : false")
      return(False)
    
  def initialize(self):
    os.chdir(self.absPipePath)
    if(self.isMainInitialized()):
      print("already initialized")
      self._update()
    else:
      self._init()
      self._add()
      self._commit()
    print("initialization done")
    return(True)
  
  def initializeLocal(self):
    os.chdir(self.localPath)
    if(self.isLocalInitialized()):
      print("already initialized")
    self._clone()
    self._pull()
    self._update()
    print("cloning done")
    return(True)
    
  
  
    
  def _copyHomeConfig(self):
    userdir = expanduser("~") + os.sep
    try:
      if(sys.platform.find("linux") >= 0):
        shutil.copy(hgrcLocalLinux,userdir + os.sep +".hgrc")
      elif(sys.platform.find("win") >= 0):
        shutil.copy(hgrcLocalWindows,userdir + os.sep +".hgrc")
    except:
      print("copying hgrc to home : fail")
      print(str(sys.exc_info()))
    print("copying hgrc to home : done")
  
  
  def _copyMainConfig(self):
    userdir = expanduser("~") + os.sep
    try:
      if(sys.platform.find("linux") >= 0):
        shutil.copy(hgrcLocalLinux,self.absPipePath +"/.hg/hgrc")
      elif(sys.platform.find("win") >= 0):
        shutil.copy(hgrcLocalWindows,self.absPipePath +"/.hg/hgrc")
    except:
      print("copying hgrc to main : fail")
      print(str(sys.exc_info()))
    print("copying hgrc to main : done")
    
  def _copyLocalConfig(self):
    userdir = expanduser("~") + os.sep
    try:
      if(sys.platform.find("linux") >= 0):
        shutil.copy(hgrcLocalLinux,self.localPath +"/.hg/hgrc")
      elif(sys.platform.find("win") >= 0):
        shutil.copy(hgrcLocalWindows,self.localPath +"/.hg/hgrc")
    except:
      print("copying hgrc to local : fail")
      print(str(sys.exc_info()))
    print("copying hgrc to local : done")  
    
  def _init(self):
    print(os.getcwd())
    p = subprocess.Popen(["hg","init"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.communicate()
    p.wait()
    print(out)
    self._copyMainConfig()
    
    
    
    
    
  def _add(self):
    #print(self.absPipePath)
    p = subprocess.Popen(["hg","add","--large"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.communicate()
    p.wait()
    print(out)
    
  def _commit(self):
    p = subprocess.Popen(["hg","commit","--addremove","--message","wtf","--user",os.environ['rbhusPipe_acl_user']],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.communicate()
    p.wait()
    print(out)
   
  def _push(self):
    p = subprocess.Popen(["hg","push",self.absPipePath],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.communicate()
    p.wait()
    print(out)
  
  def _pull(self):
    p = subprocess.Popen(["hg","pull",self.absPipePath],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.communicate()
    p.wait()
    print(out)
    
  def _clone(self):
    p = subprocess.Popen(["hg","clone",self.absPipePath,"."],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.communicate()
    p.wait()
    print(out)
    
    
  def _update(self):
    p = subprocess.Popen(["hg","update"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.communicate()
    p.wait()
    print(out)
  
  def _log(self):
    p = subprocess.Popen(["hg","log","--style","xml"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.communicate()
    dom = minidom.parseString(out[0])
    p.wait()
    #for node in dom.getElementsByTagName('logentry'):  # visit every node <bar />
      #print node.childNodes[0].localName
    print(dom.toxml())