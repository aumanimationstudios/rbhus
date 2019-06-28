#!/usr/bin/env python2
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import os
import time
import logging
import sys
from threading import Thread
FORMAT = "%(asctime)s : %(pathname)s : %(funcName)s - %(levelname)s - %(lineno)d - %(message)s"
logging.basicConfig(format=FORMAT)
logDfl = logging.getLogger("dfl")


username = os.environ['USER']



class dflError(Exception):
  pass


class lockAcquireError(dflError):
  pass

class lockTimeOutError(dflError):
  pass

class lockNotExpiredError(dflError):
  pass

class lockBadValuesError(dflError):
  pass


class _updateMtimeThread(Thread):
  def __init__(self,path):
    super(_updateMtimeThread, self).__init__()
    self._pleaseStop = False
    self._path = path

  def pleaseStop(self):
    self._pleaseStop = True

  def run(self):
    while(True):
      if(self._pleaseStop):
        break
      try:
        os.utime(self._path,None)
      except:
        pass
      time.sleep(1)
      # logDfl.debug("updated utime")



class LockFile(object):
  timeout = 0
  expiry = 0
  lock_file = None



  def __init__(self,filePath,debug=False,timeout=0,expiry=0):
    if(debug):
      logDfl.setLevel(logging.DEBUG)
    self.expiry = expiry
    self.timeout = timeout
    self._filePath = os.path.abspath(filePath)
    self._lockfile = self._filePath + ".lock"
    self._lockfileFd = None
    self._lockThread = None
    self.lock_file = self._lockfile
    logDfl.debug(os.getpid())

  def __enter__(self):
    if(self.timeout > 0 and self.expiry > 0):
      if(self.timeout >= self.expiry):
        logging.info("timeout SHOULD be less than expiry")
        raise lockBadValuesError

    if(self.expiry > 0):
      self._cleanExpired()

    self._acquireLock()
    logDfl.debug("entered lock state")
    self._lockThread = _updateMtimeThread(self._lockfile)
    self._lockThread.start()

  def __exit__(self, type, value, traceback):
    self._closeLockfileFd()
    self._lockThread.pleaseStop()
    os.unlink(self._lockfile)
    logDfl.debug("exited lock state")

  def _closeLockfileFd(self):
    if (self._lockfileFd):
      try:
        os.close(self._lockfileFd)
      except:
        logDfl.error(sys.exc_info())


  def _cleanExpired(self):
    logDfl.debug("searching for old lockfile")
    try:
      mTimeLock = os.path.getmtime(self._lockfile)
      totalTimeOfLock = time.time() - mTimeLock
      logDfl.debug(totalTimeOfLock)
      if (totalTimeOfLock >= self.expiry):
        try:
          os.unlink(self._lockfile)
          logDfl.debug("cleanup old lockfile")
        except:
          logDfl.debug("no file to cleanup")
      else:
        if(self.timeout == 0):
          raise lockNotExpiredError
        else:
          logDfl.debug("lockfile not expired")
    except lockNotExpiredError:
      raise
    except:
      logDfl.debug("nothing to clean")


  def _waitTimedout(self):
    mTimeLock = time.time()
    totalTimeOfLock = time.time() - mTimeLock
    while (totalTimeOfLock < self.timeout):
      totalTimeOfLock = time.time() - mTimeLock
      logDfl.debug(totalTimeOfLock)
      if (os.path.exists(self._lockfile)):
        time.sleep(1)
      else:
        return
    raise lockTimeOutError


  def _acquireLock(self):
    logDfl.debug("TRYING TO ACQUIRE LOCK")
    try:
      self._lockfileFd = os.open(self._lockfile,os.O_CREAT | os.O_EXCL)
      logDfl.debug("ACQUIRED LOCK")
    except:
      if(self.timeout > 0):
        self._waitTimedout()
        try:
          self._lockfileFd = os.open(self._lockfile, os.O_CREAT | os.O_EXCL)
          self._lockfileFd.write(username)
          self._lockfileFd.flush()
          logDfl.debug("ACQUIRED LOCK")
        except:
          raise lockAcquireError
      else:
        raise lockAcquireError







#TESTING
if(__name__ == '__main__'):
  import setproctitle
  setproctitle.setproctitle("dfl")
  lckf = LockFile("/tmp/", debug=True)
  lckf.expiry = 10
  lckf.timeout = 5
  # lckf.timeout = 19
  with lckf:
    # a rubbish logic to waste time
    logDfl.debug("testing locking body")
    timestarted = time.time()
    while(True):
      if((time.time() - timestarted) > 20):
        break
      else:
        logDfl.debug("INSIDE testing locking body")
        time.sleep(1)

