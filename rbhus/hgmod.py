import sys
import os
from os.path import expanduser
import multiprocessing
import shutil
import subprocess






dirSelf = os.path.dirname(os.path.realpath(__file__))
etcMercurial = dirSelf.split(os.sep)[:-1]
etcMercurial.append("etc")
etcMercurial.append("mercurial")
hgrcHome = os.sep.join(etcMercurial) + os.sep +"home"+ os.sep +".hgrc"
hgrcLocalLinux = os.sep.join(etcMercurial) + os.sep +"local"+ os.sep +"hgrc.linux"
hgrcLocalWindows = os.sep.join(etcMercurial) + os.sep +"local"+ os.sep +"hgrc.windows"
hgignore = os.sep.join(etcMercurial) + os.sep +"local"+ os.sep +".hgignore"
localCacheLinux = "/crap/versionCache/"+ os.environ['rbhusPipe_acl_user'] +"/"
localCacheWindows = "D:/versionCache/"+ os.environ['rbhusPipe_acl_user'] +"/"

import dbPipe
import constantsPipe
import utilsPipe



class hg(object):
  
  def __init__(self,pipePath):
    self.pipepath = pipePath
    self.absPipePath = utilsPipe.getAbsPath(pipePath)
    self.assDets = utilsPipe.getAssDetails(assPath=pipePath)
    self.projDets = utilsPipe.getProjDetails(pipePath.split(":")[0])
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
      
    print(os.environ['rbhusPipe_acl_user'])
    print(self.projDets['admins'].split(","))
    print(self.assDets['createdUser'].split(","))
    print(self.assDets['assignedWorker'].split(","))
    
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
      self._add()
      self._commit()
      self._update()
      self._copyIgnore()
    else:
      self._init()
      self._add()
      self._commit()
      self._copyIgnore()
    print("initialization done")
    return(True)
  
  def initializeLocal(self):
    try:
      os.makedirs(self.localPath)
    except:
      print(sys.exc_info())
    os.chdir(self.localPath)
    if(self.isLocalInitialized()):
      print("already initialized")
    else:
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
  
  def _copyIgnore(self):
    userdir = expanduser("~") + os.sep
    try:
      if(sys.platform.find("linux") >= 0):
        shutil.copy(hgignore,self.absPipePath +"/.hgignore")
      elif(sys.platform.find("win") >= 0):
        shutil.copy(hgignore,self.absPipePath +"/.hgignore")
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
    
  
  def _deleteLock(self):
    try:
      os.remove(self.absPipePath +"/.hg/store/lock")
    except:
      print(str(sys.exc_info()))
  
  
  def _init(self):
    print(os.getcwd())
    p = subprocess.Popen(["hg","init"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.communicate()
    p.wait()
    print(out)
    self._copyMainConfig()
    
    
  
  def _merge(self):
    if(not ((os.environ['rbhusPipe_acl_user'] in self.projDets['admins'].split(",")) or (os.environ['rbhusPipe_acl_admin'] == "1") or (os.environ['rbhusPipe_acl_user'] in self.assDets['createdUser'].split(",")) or (os.environ['rbhusPipe_acl_user'] in self.assDets['assignedWorker'].split(",")))):
      return(0)
    p = subprocess.Popen(["hg","merge"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.communicate()
    p.wait()
    self._deleteLock()
    print("_merge"+ str(out))
    
    
  def _add(self):
    if(not ((os.environ['rbhusPipe_acl_user'] in self.projDets['admins'].split(",")) or (os.environ['rbhusPipe_acl_admin'] == "1") or (os.environ['rbhusPipe_acl_user'] in self.assDets['createdUser'].split(",")) or (os.environ['rbhusPipe_acl_user'] in self.assDets['assignedWorker'].split(",")))):
      return(0)
    #print(self.absPipePath)
    p = subprocess.Popen(["hg","add","--large"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.communicate()
    p.wait()
    self._deleteLock()
    print("_add"+ str(out))
    
  def _addremove(self):
    if(not ((os.environ['rbhusPipe_acl_user'] in self.projDets['admins'].split(",")) or (os.environ['rbhusPipe_acl_admin'] == "1") or (os.environ['rbhusPipe_acl_user'] in self.assDets['createdUser'].split(",")) or (os.environ['rbhusPipe_acl_user'] in self.assDets['assignedWorker'].split(",")))):
      return(0)
    p = subprocess.Popen(["hg","addremove"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.communicate()
    p.wait()
    self._deleteLock()
    print("_addremove"+ str(out))
    
    
  def _commit(self):
    if(not ((os.environ['rbhusPipe_acl_user'] in self.projDets['admins'].split(",")) or (os.environ['rbhusPipe_acl_admin'] == "1") or (os.environ['rbhusPipe_acl_user'] in self.assDets['createdUser'].split(",")) or (os.environ['rbhusPipe_acl_user'] in self.assDets['assignedWorker'].split(",")))):
      return(0)
    p = subprocess.Popen(["hg","commit","--message","\'ignore now\'","--user",os.environ['rbhusPipe_acl_user']])
    out = p.communicate()
    p.wait()
    self._deleteLock()
    print("_commit"+ str(out))
   
  def _push(self):
    if(not ((os.environ['rbhusPipe_acl_user'] in self.projDets['admins'].split(",")) or (os.environ['rbhusPipe_acl_admin'] == "1") or (os.environ['rbhusPipe_acl_user'] in self.assDets['createdUser'].split(",")) or (os.environ['rbhusPipe_acl_user'] in self.assDets['assignedWorker'].split(",")))):
      return(0)
    p = subprocess.Popen(["hg","push","-f",self.absPipePath])
    out = p.communicate()
    p.wait()
    self._deleteLock()
    print("_push"+ str(out))
  
  def _pull(self):
    if(not ((os.environ['rbhusPipe_acl_user'] in self.projDets['admins'].split(",")) or (os.environ['rbhusPipe_acl_admin'] == "1") or (os.environ['rbhusPipe_acl_user'] in self.assDets['createdUser'].split(",")) or (os.environ['rbhusPipe_acl_user'] in self.assDets['assignedWorker'].split(",")))):
      return(0)
    p = subprocess.Popen(["hg","pull",self.absPipePath],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.communicate()
    p.wait()
    print("_pull"+ str(out))
    
  def _clone(self):
    #if(not ((os.environ['rbhusPipe_acl_user'] in self.projDets['admins'].split(",")) or (os.environ['rbhusPipe_acl_admin'] == "1") or (os.environ['rbhusPipe_acl_user'] in self.assDets['createdUser'].split(",")) or (os.environ['rbhusPipe_acl_user'] in self.assDets['assignedWorker'].split(",")))):
      #return(0)
    p = subprocess.Popen(["hg","clone",self.absPipePath,"."],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.communicate()
    p.wait()
    print("_clone"+ str(out))
    
    
  def _update(self):
    if(not ((os.environ['rbhusPipe_acl_user'] in self.projDets['admins'].split(",")) or (os.environ['rbhusPipe_acl_admin'] == "1") or (os.environ['rbhusPipe_acl_user'] in self.assDets['createdUser'].split(",")) or (os.environ['rbhusPipe_acl_user'] in self.assDets['assignedWorker'].split(",")))):
      return(0)
    p = subprocess.Popen(["hg","update"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.communicate()
    p.wait()
    print("_updte"+ str(out))
    self._deleteLock()
  
  def _log(self):
    print("going into log")
    p = subprocess.Popen(["hg","log","--template","{rev}###{author}###{date}###{desc}@@@"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.communicate()
    p.wait()
    print(out)
    ret = []
    for t in out:
      if(t):
        for g in t.split("@@@"):
          if(g):
            ret.append(g.split("###"))
    self._deleteLock()        
    return(ret)
  
  
  def _archive(self,rev):
    if(not ((os.environ['rbhusPipe_acl_user'] in self.projDets['admins'].split(",")) or (os.environ['rbhusPipe_acl_admin'] == "1") or (os.environ['rbhusPipe_acl_user'] in self.assDets['createdUser'].split(",")) or (os.environ['rbhusPipe_acl_user'] in self.assDets['assignedWorker'].split(",")))):
      return(0)
    if(not rev):
      rev = 0
    os.chdir(self.absPipePath)
    if(os.path.exists("./publish/")):
      shutil.rmtree("./publish/")
    p = subprocess.Popen(["hg","archive","--rev",str(rev),"./publish/"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assdict = {}
    assdict["publishVersion"] = str(rev)
    utilsPipe.assEdit(asspath = self.pipepath , assdict=assdict)
    out = p.communicate()
    p.wait()
    print("_archive"+ str(out))
    self._deleteLock()
    os.chdir(self.localPath)
    
    
  def _archiveVersion(self,rev):
    if(not rev):
      rev = 0
    os.chdir(self.absPipePath)
    if(os.path.exists("./export_"+ str(rev) +"/")):
      shutil.rmtree("./export_"+ str(rev) +"/")
    p = subprocess.Popen(["hg","archive","--rev",str(rev),"./export_"+ str(rev) +"/"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assdict = {}
    print("_archive"+ str(rev))
    self._deleteLock()
    os.chdir(self.localPath)
    
  def _archiveVersionLocal(self,rev):
    if(not rev):
      rev = 0
    os.chdir(self.localPath)
    if(os.path.exists("./export_"+ str(rev) +"/")):
      shutil.rmtree("./export_"+ str(rev) +"/")
    p = subprocess.Popen(["hg","archive","--rev",str(rev),"./export_"+ str(rev) +"/"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assdict = {}
    print("_archive"+ str(rev))
    self._deleteLock()
    os.chdir(self.localPath)
  
  def _revert(self,rev):
    if(not rev):
      rev = 0
    os.chdir(self.localPath)
    p = subprocess.Popen(["hg","update","--rev",str(rev)],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.communicate()
    p.wait()
    print("_revert"+ str(out))
    self._deleteLock()
    os.chdir(self.localPath)
    
    
  
    
  def getVersionPath(self,rev):
    if(not rev):
      rev = 0
    if(not os.path.exists(self.absPipePath +"/export_"+ str(rev) +"/")):
      self._archiveVersionLocal(rev)
    return(self.localPath +"/export_"+ str(rev) +"/")
  
  
  def reInitLocal(self):
    if(os.path.exists(self.localPath)):
      try:
        shutil.rmtree(self.localPath)
        self.initializeLocal()
      except:
        return(0)
    return(1)
      
      
      
        
    
  
