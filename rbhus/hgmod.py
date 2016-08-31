import sys
import os
from os.path import expanduser
import multiprocessing
import shutil
import subprocess
import debug






dirSelf = os.path.dirname(os.path.realpath(__file__))
etcMercurial = dirSelf.split(os.sep)[:-1]
etcMercurial.append("etc")
etcMercurial.append("mercurial")
hgrcHome = os.sep.join(etcMercurial) + os.sep +"home"+ os.sep +".hgrc"
hgrcLocalLinux = os.sep.join(etcMercurial) + os.sep +"local"+ os.sep +"hgrc.linux"
hgrcLocalWindows = os.sep.join(etcMercurial) + os.sep +"local"+ os.sep +"hgrc.windows"
hgignore = os.sep.join(etcMercurial) + os.sep +"local"+ os.sep +".hgignore"
localCacheLinuxMain = "/crap/versionCache/"
localCacheWindowsMain = "D:/versionCache/"
localCacheLinux = localCacheLinuxMain + os.environ['rbhusPipe_acl_user'] +"/"
localCacheWindows = localCacheWindowsMain + os.environ['rbhusPipe_acl_user'] +"/"

import dbPipe
import constantsPipe
import utilsPipe



class hg(object):

  def __init__(self,pipePath):
    if(sys.platform.find("win") >= 0):
      try:
        self.username = os.environ['USERNAME']
      except:
        self.username = "nobody"
      try:
        os.makedirs(localCacheWindowsMain)
      except:
        debug.info(sys.exc_info())

    if(sys.platform.find("linux") >= 0):
      try:
        self.username = os.environ['USER']
      except:
        self.username = "nobody"
      try:
        os.makedirs(localCacheLinuxMain)
      except:
        debug.info(sys.exc_info())
      try:
        os.chmod(localCacheLinuxMain, 0777)
      except:
        debug.info(sys.exc_info())

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
    debug.info(self.localPath)
    try:
      os.makedirs(self.localPath)
    except:
      debug.info(sys.exc_info())

    debug.info(os.environ['rbhusPipe_acl_user'])
    debug.info(self.projDets['admins'].split(","))
    debug.info(self.assDets['createdUser'].split(","))
    debug.info(self.assDets['assignedWorker'].split(","))

    #self.initialize()
    #os.chdir(self.localPath)
    #self.initializeLocal()







  def isMainInitialized(self):
    if(os.path.exists(self.absPipePath +"/.hg")):
      debug.info("versioning main : true")
      return(True)
    else:
      debug.info("versioning main : false")
      return(False)


  def isLocalInitialized(self):
    if(os.path.exists(self.localPath +"/.hg")):
      debug.info("versioning  local : true")
      return(True)
    else:
      debug.info("versioning local : false")
      return(False)

  def initialize(self):
    os.chdir(self.absPipePath)
    if(self.isMainInitialized()):
      debug.info("already initialized")
      self._add()
      self._commit()
      self._update()
      self._copyIgnore()
    else:
      self._init()
      self._add()
      self._commit()
      self._copyIgnore()
    debug.info("initialization done")
    return(True)

  def initializeLocal(self):
    try:
      os.makedirs(self.localPath)
    except:
      debug.info(sys.exc_info())
    os.chdir(self.localPath)
    if(self.isLocalInitialized()):
      debug.info("already initialized")
    else:
      self._clone()
    self._pull()
    self._update()
    debug.info("cloning done")
    return(True)




  def _copyHomeConfig(self):
    userdir = expanduser("~") + os.sep
    try:
      if(sys.platform.find("linux") >= 0):
        shutil.copy(hgrcLocalLinux,userdir + os.sep +".hgrc")
      elif(sys.platform.find("win") >= 0):
        shutil.copy(hgrcLocalWindows,userdir + os.sep +".hgrc")
    except:
      debug.info("copying hgrc to home : fail")
      debug.info(str(sys.exc_info()))
    debug.info("copying hgrc to home : done")


  def _copyMainConfig(self):
    userdir = expanduser("~") + os.sep
    try:
      if(sys.platform.find("linux") >= 0):
        shutil.copy(hgrcLocalLinux,self.absPipePath +"/.hg/hgrc")
      elif(sys.platform.find("win") >= 0):
        shutil.copy(hgrcLocalWindows,self.absPipePath +"/.hg/hgrc")
    except:
      debug.info("copying hgrc to main : fail")
      debug.info(str(sys.exc_info()))
    debug.info("copying hgrc to main : done")

  def _copyIgnore(self):
    userdir = expanduser("~") + os.sep
    try:
      if(sys.platform.find("linux") >= 0):
        shutil.copy(hgignore,self.absPipePath +"/.hgignore")
      elif(sys.platform.find("win") >= 0):
        shutil.copy(hgignore,self.absPipePath +"/.hgignore")
    except:
      debug.info("copying hgrc to main : fail")
      debug.info(str(sys.exc_info()))
    debug.info("copying hgrc to main : done")


  def _copyLocalConfig(self):
    userdir = expanduser("~") + os.sep
    try:
      if(sys.platform.find("linux") >= 0):
        shutil.copy(hgrcLocalLinux,self.localPath +"/.hg/hgrc")
      elif(sys.platform.find("win") >= 0):
        shutil.copy(hgrcLocalWindows,self.localPath +"/.hg/hgrc")
    except:
      debug.info("copying hgrc to local : fail")
      debug.info(str(sys.exc_info()))
    debug.info("copying hgrc to local : done")


  def _deleteLock(self):
    pass
    # try:
    #   os.remove(self.absPipePath +"/.hg/store/lock")
    # except:
    #   debug.info(str(sys.exc_info()))


  def _init(self):
    debug.info(os.getcwd())
    if(sys.platform.lower().find("linux") >= 0):
      p = subprocess.Popen("hg init",shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
      p = subprocess.Popen(["hg","init"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.communicate()
    p.wait()
    debug.info(out)
    self._copyMainConfig()



  def _merge(self):
    if(not (utilsPipe.isAssCreated(self.assDets) or utilsPipe.isAssAssigned(self.assDets) or utilsPipe.isStageAdmin(self.assDets) or utilsPipe.isProjAdmin(self.assDets) or utilsPipe.isNodeAdmin(self.assDets))):
      return(0)
    if(sys.platform.lower().find("linux") >= 0):
      p = subprocess.Popen("hg merge",shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
      p = subprocess.Popen(["hg","merge"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.communicate()
    p.wait()
    self._deleteLock()
    debug.info("_merge"+ str(out))


  def _add(self):
    if(not (utilsPipe.isAssCreated(self.assDets) or utilsPipe.isAssAssigned(self.assDets) or utilsPipe.isStageAdmin(self.assDets) or utilsPipe.isProjAdmin(self.assDets) or utilsPipe.isNodeAdmin(self.assDets))):
      return(0)
    #debug.info(self.absPipePath)
    if(sys.platform.lower().find("linux") >= 0):
      p = subprocess.Popen("hg add --large",shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
      p = subprocess.Popen(["hg","add","--large"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.communicate()
    p.wait()
    self._deleteLock()
    debug.info("_add"+ str(out))

  def _addremove(self):
    if(not (utilsPipe.isAssCreated(self.assDets) or utilsPipe.isAssAssigned(self.assDets) or utilsPipe.isStageAdmin(self.assDets) or utilsPipe.isProjAdmin(self.assDets) or utilsPipe.isNodeAdmin(self.assDets))):
      return(0)
    if(sys.platform.lower().find("linux") >= 0):
      p = subprocess.Popen("hg addremove",shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
      p = subprocess.Popen(["hg","addremove"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.communicate()
    p.wait()
    self._deleteLock()
    debug.info("_addremove"+ str(out))


  def _commit(self):
    if(not (utilsPipe.isAssCreated(self.assDets) or utilsPipe.isAssAssigned(self.assDets) or utilsPipe.isStageAdmin(self.assDets) or utilsPipe.isProjAdmin(self.assDets) or utilsPipe.isNodeAdmin(self.assDets))):
      return(0)
    if(sys.platform.lower().find("linux") >= 0):
      p = subprocess.Popen("hg commit -A --message \'ignore for now\' --user {0}".format(os.environ['rbhusPipe_acl_user']),shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
      p = subprocess.Popen(["hg","commit","-A","--message","\'ignore now\'","--user",os.environ['rbhusPipe_acl_user']], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.communicate()
    p.wait()
    self._deleteLock()
    debug.info("_commit"+ str(out))

  def _push(self):
    if(not (utilsPipe.isAssCreated(self.assDets) or utilsPipe.isAssAssigned(self.assDets) or utilsPipe.isStageAdmin(self.assDets) or utilsPipe.isProjAdmin(self.assDets) or utilsPipe.isNodeAdmin(self.assDets))):
      return(0)
    if(sys.platform.lower().find("linux") >= 0):
      p = subprocess.Popen("hg push -f {0}".format(self.absPipePath),shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
      p = subprocess.Popen(["hg","push","-f",self.absPipePath],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.communicate()
    p.wait()
    self._deleteLock()
    debug.info("_push"+ str(out))

  def _pull(self):
    if(sys.platform.lower().find("linux") >= 0):
      p = subprocess.Popen("hg pull {0}".format(self.absPipePath),shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
      p = subprocess.Popen(["hg","pull",self.absPipePath],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.communicate()
    p.wait()
    debug.info("_pull"+ str(out))

  def _clone(self):
    #if(not ((os.environ['rbhusPipe_acl_user'] in self.projDets['admins'].split(",")) or (os.environ['rbhusPipe_acl_admin'] == "1") or (os.environ['rbhusPipe_acl_user'] in self.assDets['createdUser'].split(",")) or (os.environ['rbhusPipe_acl_user'] in self.assDets['assignedWorker'].split(",")))):
      #return(0)
    if(sys.platform.lower().find("linux") >= 0):
      p = subprocess.Popen("hg clone {0} {1}".format(self.absPipePath,"."),shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
      p = subprocess.Popen(["hg","clone",self.absPipePath,"."],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.communicate()
    p.wait()
    debug.info("_clone"+ str(out))


  def _update(self):
    if(not (utilsPipe.isAssCreated(self.assDets) or utilsPipe.isAssAssigned(self.assDets) or utilsPipe.isStageAdmin(self.assDets) or utilsPipe.isProjAdmin(self.assDets) or utilsPipe.isNodeAdmin(self.assDets))):
      return(0)
    if(sys.platform.lower().find("linux") >= 0):
      p = subprocess.Popen("hg update",shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
      p = subprocess.Popen(["hg","update"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.communicate()
    p.wait()
    debug.info("_updte"+ str(out))
    self._deleteLock()

  def _log(self):
    if(sys.platform.lower().find("linux") >= 0):
      p = subprocess.Popen("hg log --template {rev}###{author}###{date}###{desc}@@@",shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
      p = subprocess.Popen(["hg","log","--template","{rev}###{author}###{date}###{desc}@@@"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.communicate()
    p.wait()
    debug.info(out)
    ret = []
    for t in out:
      if(t):
        for g in t.split("@@@"):
          if(g):
            ret.append(g.split("###"))
    self._deleteLock()
    return(ret)


  def _archive(self,rev):
    if(not (utilsPipe.isAssCreated(self.assDets) or utilsPipe.isAssAssigned(self.assDets) or utilsPipe.isStageAdmin(self.assDets) or utilsPipe.isProjAdmin(self.assDets) or utilsPipe.isNodeAdmin(self.assDets))):
      return(0)
    if(not rev):
      rev = 0
    os.chdir(self.absPipePath)
    if(os.path.exists("./publish/")):
      shutil.rmtree("./publish/")
    if(sys.platform.lower().find("linux") >= 0):
      p = subprocess.Popen("hg archive --rev {0} ./publish/".format(rev),shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
      p = subprocess.Popen(["hg","archive","--rev",str(rev),"./publish/"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assdict = {}
    assdict["publishVersion"] = str(rev)
    utilsPipe.assEdit(asspath = self.pipepath , assdict=assdict)
    out = p.communicate()
    p.wait()
    debug.info("_archive"+ str(out))
    self._deleteLock()
    os.chdir(self.localPath)



  def _review(self,rev):
    if(not (utilsPipe.isAssAssigned(self.assDets) or utilsPipe.isAssCreated(self.assDets) or utilsPipe.isStageAdmin(self.assDets) or utilsPipe.isProjAdmin(self.assDets) or utilsPipe.isNodeAdmin(self.assDets))):
      return(0)
    if(not rev):
      rev = 0
    os.chdir(self.absPipePath)
    # if(os.path.exists("./review_"+ str(rev) +"/")):
    #   shutil.rmtree("./review_"+ str(rev) +"/")
    if(sys.platform.lower().find("linux") >= 0):
      p = subprocess.Popen("hg archive --rev {0} ./review_{0}/".format(rev),shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
      p = subprocess.Popen(["hg","archive","--rev",str(rev),"./review_"+ str(rev) +"/"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # assdict = {}
    # assdict["reviewVersion"] = str(rev)
    # assdict['assetId'] = self.assDets['assetId']
    # assdict['username'] = self.username
    utilsPipe.reviewVersion(self.assDets['path'], rev)

    out = p.communicate()
    p.wait()
    debug.info(str(out))
    self._deleteLock()
    os.chdir(self.localPath)

  def _archiveVersion(self,rev):
    if(not rev):
      rev = 0
    os.chdir(self.absPipePath)
    if(os.path.exists("./export_"+ str(rev) +"/")):
      shutil.rmtree("./export_"+ str(rev) +"/")
    if(sys.platform.lower().find("linux") >= 0):
      p = subprocess.Popen("hg archive --rev {0} ./export_{0}/".format(rev),stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
      p = subprocess.Popen(["hg","archive","--rev",str(rev),"./export_"+ str(rev) +"/"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assdict = {}
    debug.info("_archive"+ str(rev))
    self._deleteLock()
    os.chdir(self.localPath)

  def _archiveVersionLocal(self,rev):
    if(not rev):
      rev = 0
    os.chdir(self.localPath)
    if(os.path.exists("./export_"+ str(rev) +"/")):
      shutil.rmtree("./export_"+ str(rev) +"/")
    if(sys.platform.lower().find("linux") >= 0):
      p = subprocess.Popen("hg archive --rev {0} /export_{0}/".format(rev),stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
      p = subprocess.Popen(["hg","archive","--rev",str(rev),"./export_"+ str(rev) +"/"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assdict = {}
    debug.info(str(rev))
    self._deleteLock()
    os.chdir(self.localPath)


  def _revert(self,rev):
    if(not rev):
      rev = 0
    os.chdir(self.localPath)
    if(sys.platform.lower().find("linux") >= 0):
      p = subprocess.Popen("hg update --rev {0}".format(rev),stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
      p = subprocess.Popen(["hg","update","--rev",str(rev)],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.communicate()
    p.wait()
    debug.info("_revert"+ str(out))
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
