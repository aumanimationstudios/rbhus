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
import utilsTray



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
    # self.isMainInitialized()
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
      self._copyIgnore()
      self._add()
      self._commit()
      self._update()
    else:
      self._copyIgnore()
      self._init()
      self._add()
      self._commit()
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
    self._update(local=True)
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
      p = subprocess.Popen("hg --verbose init",shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
      p = subprocess.Popen(["hg","--verbose","init"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.communicate()[0]
    if (p.returncode != 0):
      debug.error(str(out))
    else:
      debug.info(str(out))
    self._copyMainConfig()



  def _merge(self):
    if(not (utilsPipe.isAssCreated(self.assDets) or utilsPipe.isAssAssigned(self.assDets) or utilsPipe.isStageAdmin(self.assDets) or utilsPipe.isProjAdmin(self.assDets) or utilsPipe.isNodeAdmin(self.assDets))):
      debug.warn("user not allowed")
      return(111)
    if(sys.platform.lower().find("linux") >= 0):
      p = subprocess.Popen("hg --verbose merge --tool=\":local\"",shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
      p = subprocess.Popen(["hg","--verbose","merge","--tool",":local"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.communicate()[0]
    if(p.returncode != 0):
      debug.error(str(out))
    else:
      debug.info(str(out))


  def _add(self):
    if(not (utilsPipe.isAssAssigned(self.assDets) or utilsPipe.isStageAdmin(self.assDets) or utilsPipe.isProjAdmin(self.assDets) or utilsPipe.isNodeAdmin(self.assDets))):
      debug.warn("user not allowed")
      return(111)
    #debug.info(self.absPipePath)
    if(sys.platform.lower().find("linux") >= 0):
      p = subprocess.Popen("hg --verbose add --large",shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
      p = subprocess.Popen(["hg","--verbose","add","--large"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.communicate()[0]
    if (p.returncode != 0):
      debug.error(str(out))
    else:
      debug.info(str(out))

  def _addremove(self):
    if(not (utilsPipe.isAssAssigned(self.assDets) or utilsPipe.isStageAdmin(self.assDets) or utilsPipe.isProjAdmin(self.assDets) or utilsPipe.isNodeAdmin(self.assDets))):
      debug.warn("user not allowed")
      return(111)
    if(sys.platform.lower().find("linux") >= 0):
      p = subprocess.Popen("hg --verbose addremove",shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
      p = subprocess.Popen(["hg","--verbose","addremove"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.communicate()[0]
    if (p.returncode != 0):
      debug.error(str(out))
    else:
      debug.info(str(out))


  def _commit(self):
    if(not (utilsPipe.isAssAssigned(self.assDets) or utilsPipe.isStageAdmin(self.assDets) or utilsPipe.isProjAdmin(self.assDets) or utilsPipe.isNodeAdmin(self.assDets))):
      debug.warn("user not allowed")
      return(111)
    if(sys.platform.lower().find("linux") >= 0):
      p = subprocess.Popen("hg --verbose commit -A --message \'ignore now\' --user {0}".format(os.environ['rbhusPipe_acl_user']),shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
      p = subprocess.Popen(["hg","--verbose","commit","-A","--message","\'ignore now\'","--user",os.environ['rbhusPipe_acl_user']], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.communicate()[0]
    if (p.returncode != 0):
      debug.error(str(out))
      return(0)
    else:
      debug.info(str(out))
      return(1)


  def _push(self):
    if(not (utilsPipe.isAssAssigned(self.assDets) or utilsPipe.isStageAdmin(self.assDets) or utilsPipe.isProjAdmin(self.assDets) or utilsPipe.isNodeAdmin(self.assDets))):
      debug.warn("user not allowed")
      return(111)
    if(sys.platform.lower().find("linux") >= 0):
      p = subprocess.Popen("hg --verbose push -f {0}".format(self.absPipePath),shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
      p = subprocess.Popen(["hg","--verbose","push","-f",self.absPipePath],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.communicate()[0]
    if (p.returncode != 0):
      debug.error(str(out))
    else:
      debug.info(str(out))


  def _pull(self):
    if(sys.platform.lower().find("linux") >= 0):
      p = subprocess.Popen("hg --verbose pull --force {0}".format(self.absPipePath),shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
      p = subprocess.Popen(["hg","--verbose","pull","--force",self.absPipePath],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.communicate()[0]
    if (p.returncode != 0):
      debug.error(str(out))
    else:
      debug.info(str(out))


  def _clone(self):
    if(sys.platform.lower().find("linux") >= 0):
      p = subprocess.Popen("hg --verbose clone {0} {1}".format(self.absPipePath,"."),shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
      p = subprocess.Popen(["hg","--verbose","clone",self.absPipePath,"."],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.communicate()[0]
    p.wait()
    debug.info("_clone"+ str(out))


  def _update(self,local=False):
    if(not local):
      if(not (utilsPipe.isAssAssigned(self.assDets) or utilsPipe.isStageAdmin(self.assDets) or utilsPipe.isProjAdmin(self.assDets) or utilsPipe.isNodeAdmin(self.assDets))):
        debug.warn("user not allowed")
        return(111)
    if(sys.platform.lower().find("linux") >= 0):
      p = subprocess.Popen("hg --verbose update --check",shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
      p = subprocess.Popen(["hg","--verbose","update","--check"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.communicate()[0]
    if (p.returncode != 0):
      debug.error(str(out))
    else:
      debug.info(str(out))

  def _purge(self):
    if(not (utilsPipe.isAssAssigned(self.assDets) or utilsPipe.isStageAdmin(self.assDets) or utilsPipe.isProjAdmin(self.assDets) or utilsPipe.isNodeAdmin(self.assDets))):
      debug.warn("user not allowed")
      return(111)
    if(sys.platform.lower().find("linux") >= 0):
      p = subprocess.Popen("hg --verbose purge",shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
      p = subprocess.Popen(["hg","--verbose","purge"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.communicate()[0]
    if (p.returncode != 0):
      debug.error(str(out))
    else:
      debug.info(str(out))

  def _log(self):
    if(sys.platform.lower().find("linux") >= 0):
      p = subprocess.Popen("hg --verbose log --template {rev}###{author}###{date}###{desc}@@@ --cwd "+ self.absPipePath,shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
      p = subprocess.Popen(["hg","--verbose","log","--template","{rev}###{author}###{date}###{desc}@@@","--cwd",self.absPipePath],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.communicate()[0]
    p.wait()
    # debug.info(out)
    ret = []
    # for t in out:
    #   if(t):
    for g in out.split("@@@"):
      if(g):
        ret.append(g.split("###"))
    # self._deleteLock()
    return(ret)


  def _archive(self,rev):
    if(not (utilsPipe.isAssAssigned(self.assDets) or utilsPipe.isStageAdmin(self.assDets) or utilsPipe.isProjAdmin(self.assDets) or utilsPipe.isNodeAdmin(self.assDets))):
      debug.warn("user not allowed")
      return(0)

    pubpath = os.path.join(self.absPipePath,"publish")
    if(not rev):
      rev = 0
    os.chdir(self.absPipePath)
    if(os.path.exists(pubpath)):
      try:
        shutil.rmtree(pubpath)
      except:
        debug.warn(sys.exc_info())
    try:
      os.makedirs(pubpath)
    except:
      debug.warn(sys.exc_info())
    if(sys.platform.lower().find("linux") >= 0):
      p = subprocess.Popen("hg --verbose archive --rev {0} ./publish/".format(rev),shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
      p = subprocess.Popen(["hg","--verbose","archive","--rev",str(rev),"./publish/"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    out = p.communicate()[0]
    p.wait()
    if (p.returncode != 0):
      debug.error(str(out))
    else:
      debug.info(str(out))
      assdict = {}
      assdict["publishVersion"] = str(rev)
      utilsPipe.assEdit(asspath=self.pipepath, assdict=assdict)
    os.chdir(self.localPath)



  def _review(self,rev):
    if(not (utilsPipe.isAssAssigned(self.assDets) or utilsPipe.isStageAdmin(self.assDets) or utilsPipe.isProjAdmin(self.assDets) or utilsPipe.isNodeAdmin(self.assDets))):
      debug.warn("user not allowed")
      return(111)
    if(not rev):
      rev = 0

    if(self.assDets['reviewStatus'] == constantsPipe.reviewStatusDone):
      debug.warn("asset already approved. cannot send for review unless the reviewer sets the status to inProgress")
      return(0)

    os.chdir(self.absPipePath)
    try:
      os.makedirs(os.path.join(self.absPipePath, "review_{0}".format(rev)))
    except:
      debug.warn(sys.exc_info())

    if(sys.platform.lower().find("linux") >= 0):
      p = subprocess.Popen("hg --verbose archive --rev {0} ./review_{0}/".format(rev),shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
      p = subprocess.Popen(["hg","--verbose","archive","--rev",str(rev),"./review_"+ str(rev) +"/"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.communicate()[0]
    if (p.returncode != 0):
      debug.error(str(out))
    else:
      debug.info(str(out))
      utilsPipe.reviewVersion(self.assDets['path'], rev)
      revdets = {}
      revdets['assetId'] = str(self.assDets['assetId'])
      revdets['reviewVersion'] = str(rev)
      revdets['message'] = "please review the given version."
      revdets['username'] = str(self.username)
      utilsPipe.reviewAdd(revdets)

      assetColor = utilsPipe.assPathColorCoded(self.assDets)
      textAssArr = []
      for fc in assetColor.split(":"):
        textAssArr.append('<font color=' + fc.split("#")[1] + '>' + fc.split("#")[0] + '</font>')
      richAss = " " + "<b><i> : </i></b>".join(textAssArr)

      reviewmsg = str(richAss) +"\n\nstatus : inProgress"



      if (self.username != self.assDets['assignedWorker']):
        reviewID = self.assDets['path'] + ":" + self.assDets['assignedWorker']
        utilsTray.addNotifications(self.assDets['assignedWorker'], "rbhusReview", reviewmsg, "rbhusPipe_review.py", "-p " + self.assDets['projName'] + " -a " + self.assDets['path'],reviewID)

      if (self.username != self.assDets['reviewUser']):
        reviewID = self.assDets['path'] + ":" + self.assDets['reviewUser']
        utilsTray.addNotifications(self.assDets['reviewUser'], "rbhusReview", reviewmsg, "rbhusPipe_review.py", "-p " + self.assDets['projName'] + " -a " + self.assDets['path'],reviewID)

      if (self.assDets['reviewNotifyUsers'] != "default"):
        for ru in self.assDets['reviewNotifyUsers'].split(","):
          reviewID = self.assDets['path'] + ":" + ru
          debug.info(ru)
          utilsTray.addNotifications(ru, "rbhusReview", reviewmsg, "rbhusPipe_review.py", "-p " + self.assDets['projName'] + " -a " + self.assDets['path'], reviewID)


    os.chdir(self.localPath)


  def _archiveVersion(self,rev):
    if(not rev):
      rev = 0
    os.chdir(self.absPipePath)
    if(os.path.exists("./export_"+ str(rev) +"/")):
      try:
        shutil.rmtree("./export_"+ str(rev) +"/")
      except:
        debug.warn(sys.exc_info())
    try:
      os.makedirs(os.path.join(self.absPipePath, "export_{0}".format(rev)))
    except:
      debug.warn(sys.exc_info())

    if(sys.platform.lower().find("linux") >= 0):
      p = subprocess.Popen("hg --verbose archive --rev {0} ./export_{0}/".format(rev),shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
      p = subprocess.Popen(["hg","--verbose","archive","--rev",str(rev),"./export_"+ str(rev) +"/"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.communicate()[0]
    assdict = {}
    if (p.returncode != 0):
      debug.error(str(out))
    else:
      debug.info(str(out))
    os.chdir(self.localPath)

  def _archiveVersionLocal(self,rev):
    if(not rev):
      rev = 0
    os.chdir(self.localPath)
    if(os.path.exists("./export_"+ str(rev) +"/")):
      try:
        shutil.rmtree("./export_"+ str(rev) +"/")
      except:
        debug.error(sys.exc_info())

    try:
      os.makedirs(os.path.join(self.localPath, "export_{0}".format(rev)))
    except:
      debug.warn(sys.exc_info())

    if(sys.platform.lower().find("linux") >= 0):
      p = subprocess.Popen("hg --verbose archive --rev {0} ./export_{0}/".format(rev),shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
      p = subprocess.Popen(["hg","--verbose","archive","--rev",str(rev),"./export_"+ str(rev) +"/"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.communicate()[0]
    assdict = {}
    if (p.returncode != 0):
      debug.error(str(out))
    else:
      debug.info(str(out))
    os.chdir(self.localPath)


  def _revert(self,rev):
    if(not rev):
      rev = 0
    os.chdir(self.localPath)
    if(sys.platform.lower().find("linux") >= 0):
      p = subprocess.Popen("hg --verbose update --rev {0}".format(rev),shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
      p = subprocess.Popen(["hg","--verbose","update","--rev",str(rev)],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.communicate()[0]
    if (p.returncode != 0):
      debug.error(str(out))
    else:
      debug.info(str(out))
    os.chdir(self.localPath)




  def getVersionPath(self,rev):
    if(not rev):
      rev = 0
    if(not os.path.exists(self.localPath +"/export_"+ str(rev) +"/")):
      debug.info("version path does not exists . creating it now ")
      self._archiveVersionLocal(rev)
    return(self.localPath +"/export_"+ str(rev) +"/")


  def reInitLocal(self):
    if(os.path.exists(self.localPath)):
      try:
        shutil.rmtree(self.localPath)
        self.initializeLocal()
      except:
        debug.error(sys.exc_info())
        return(0)
    return(1)
