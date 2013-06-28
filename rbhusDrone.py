#!/usr/bin/python
###
# Copyright (C) 2012  Shrinidhi Rao shrinidhi@clickbeetle.in
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
###

# CLIENT
import sys
import os
import multiprocessing
import socket
import logging
import time
import signal
import subprocess
import psutil
import re
if(sys.platform.find("linux") >= 0):
  import pwd

import pickle
import rbhus.dbRbhus as dbRbhus
import rbhus.constants as constants
if(sys.platform.find("linux") >= 0):
  import setproctitle
  setproctitle.setproctitle("rD")
import tempfile
import inspect

time.sleep(1)
hostname = socket.gethostname()
tempDir = tempfile.gettempdir()
mainPidFile = tempDir + os.sep +"rbusClient.pids"

db_conn = dbRbhus.dbRbhus()


if(sys.platform.find("linux") >=0):
  LOG_FILENAME = logging.FileHandler('/var/log/rbhusClient.log')
elif(sys.platform.find("win") >=0):
  LOG_FILENAME = logging.FileHandler(tempDir + os.sep + str(hostname) +".log")
  #LOG_FILENAME = logging.FileHandler('z:/pythonTestWindoze.DONOTDELETE/clientLogs/rbhusClient_'+ hostname +'.log')


#LOG_FILENAME = logging.FileHandler('/var/log/rbhusDb_module.log')
logClient = logging.getLogger("logClient")
logClient.setLevel(logging.DEBUG)

BASIC_FORMAT = logging.Formatter("%(asctime)s - %(funcName)s - %(levelname)s - %(lineno)s - %(message)s")
LOG_FILENAME.setFormatter(BASIC_FORMAT)
logClient.addHandler(LOG_FILENAME)

def sigHandle(sigNum, frame):
  myPid = os.getpid()
  logClient.debug("signal handler called with "+ str(sigNum) +" signal")
  logClient.debug("my pid "+ str(myPid))
  # run this only if linux?! .. omfg .. i dont know !!!!
  if(sys.platform.find("linux")):
    logClient.debug("starting to kill processes")
    killProcessKids(myPid)
  return(1)


def getProcessLastKids(ppid,lastKids):
  try:
    pidDets = psutil.Process(ppid)
  except:
    logClient.debug(str(sys.exc_info()))
    return(0)

  pidKids = pidDets.get_children(recursive=True)
  if(pidKids):
    for pidKid in pidKids:
      lastKids.append(pidKid.pid)
  lastKids.append(ppid)
  return(1)


def killProcessKids(ppid):
  try:
    pidDets = psutil.Process(ppid)
  except:
    logClient.debug(str(sys.exc_info()))
    return(0)

  pidKids = pidDets.get_children(recursive=True)
  if(pidKids):
    for pidKid in pidKids:
      logClient.debug("killing kid "+ str(pidKid.pid))
      os.kill(int(pidKid.pid),9)
  os.kill(int(ppid),9)

# Get the host info and update the database.
def init():

  hostname,ipAddr = getHostNameIP()
  totalCpus = multiprocessing.cpu_count()
  totalMem = totalMemInfo()
  ret = setHostInfo(db_conn,hostname,totalMem['MemTotal'],totalCpus,totalMem['SwapTotal'])
  if(ret == 1):
    return(1)
  return(0)


def hostUpdater():
  if(sys.platform.find("linux") >=0):
    setproctitle.setproctitle("rD_hostUpdater")
  db_conn = dbRbhus.dbRbhus()
  myPid = os.getpid()
  logClient.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) +" : "+ "hostUpdater : "+ str(myPid))
  while(1):
    time.sleep(5)
    hostname = socket.gethostname()
    try:
      freeMem = freeMeminfo()
      #logClient.debug("WTF0 : "+ str(freeMem))
      loads = loadAvg()
      #logClient.debug("WTF1 : "+ str(loads))
      setHostResMem(hostname, db_conn,freeMem['MemFree'],freeMem['SwapFree'], loads[0], loads[1], loads[2])
    except:
      logClient.debug(str(sys.exc_info()))
      continue
  sys.exit(0)

def loadAvg():
  loads = ['0','0','0']
  if(sys.platform.find("linux") >=0):
    try:
      loadFile = open("/proc/loadavg","r")
      load = loadFile.readline()
      loadFile.close()
      loads = []
      loads = load.split()
    except:
      logClient.debug(str(sys.exc_info()))
  elif(sys.platform.find("win") >=0):
    try:
      load = psutil.cpu_percent()
      if(load):
        loads = [str(load), '0', '0']
    except:
      logClient.debug(str(sys.exc_info()))
  return(loads)



def upHostAliveStatus(hostName, status, dbconn):
  hostname,ipAddr = getHostNameIP()
  try:
    dbconn.execute("UPDATE hostAlive SET status = "+ str(status) +" WHERE ip=\'"+ str(ipAddr) +"\'")
  except:
    return(0)
  return(1)

def getHostNameIP():
  while(1):
    try:
      hostname = socket.gethostname()
      ipAddr = socket.gethostbyname(socket.gethostname()).strip()
      return(hostname,ipAddr)
    except:
      logClient.debug(str(sys.exc_info()))
      time.sleep(1)
    

def getAssignedFrames(qAssigned):
  if(sys.platform.find("linux") >=0):
    setproctitle.setproctitle("rD_getAssignedFrames")
  db_conn = dbRbhus.dbRbhus()
  logClient.debug(str(os.getpid()) + ": getAssignedFrames func")
  while(1):
    hostname,ipAddr = getHostNameIP()
    rows = 0
    try:
      rows = db_conn.execute("SELECT frames.frameId, frames.fThreads,frames.batchId, tasks.* FROM frames, tasks \
                      WHERE frames.hostName=\'"+ str(hostname) +"\' \
                      AND tasks.id=frames.id \
                      AND frames.status="+ str(constants.framesAssigned) +" \
                      ORDER BY frames.frameId", dictionary=True)
    except:
      logClient.debug("1 : "+ str(sys.exc_info()[1]))
    if(rows):
      for row in rows:
        qAssigned.put(row)


        while(1):
          try:
            db_conn.execute("UPDATE frames SET status="+ str(constants.framesPending) +" \
                            WHERE frameId="+ str(row['frameId']) +" \
                            AND id="+ str(row['id']))
            break
          except:
            logClient.debug("2 : "+ str(sys.exc_info()[1]))
          time.sleep(1)
    time.sleep(1)

  sys.exit(0)


def runFrames(qRun,frameScrutiny):
  if(sys.platform.find("linux") >=0):
    setproctitle.setproctitle("rD_runFrames")
  db_conn = dbRbhus.dbRbhus()
  logClient.debug(str(os.getpid()) + ": runFrames func")
  processFrames = []
  cpuAffi = []
  cpuMax = 0
  while(1):
    time.sleep(0.2)
    hostEff = getEffectiveDetails(db_conn)

    totalPids = multiprocessing.cpu_count()
    for y in range(0,totalPids):
      cpuAffi.append(y)
    if(hostEff):
      eCpus = hostEff['eCpus']
      if(eCpus == 0):
        totalPids = multiprocessing.cpu_count()
      elif(eCpus != 0):
        totalPids = eCpus
      else:
        totalPids = 1
    
    
    

    while(1):
      a = 1
      if(len(processFrames) > 0):
        for i in range(0,len(processFrames)):
          if(processFrames[i].is_alive()):
            continue
          else:
            del(processFrames[i])
            a = 0
            break
      else:
        break
      if(a):
        break

    while(1):
      if(len(processFrames) >= totalPids):
        for i in range(0,len(processFrames)):
          if(processFrames[i].is_alive()):
            continue
          else:
            del(processFrames[i])
            break
        if(len(processFrames) < totalPids):
          break
      else:
        break
      time.sleep(0.2)


    while(1):
      try:
        frameInfo = qRun.get(timeout=1)
        break
      except:
        while(1):
          a = 1
          if(len(processFrames) > 0):
            for i in range(0,len(processFrames)):
              if(processFrames[i].is_alive()):
                continue
              else:
                del(processFrames[i])
                a = 0
                break
          else:
            break
          if(a):
            break
    frameThreads = frameInfo['fThreads']

    cpuAffiToSend = []
    #if(max(cpuAffi) >= totalPids):
      #cpuAffi = [0]
    #cpuAMax = max(cpuAffi)
    if(cpuMax >= totalPids):
      cpuMax = 0
    u = 0
    for u in range(cpuMax,cpuMax + int(frameThreads)):
      if(u >= totalPids):
        u = 0
      cpuAffiToSend.append(u)
    cpuMax = u + 1
      #cpuAffi.append(x)
      
    processFrames.append(multiprocessing.Process(target=_execFrames,args=(frameInfo,frameScrutiny,cpuAffiToSend,)))
    processFrames[-1].start()
    
    while(1):
      a = 1
      if(len(processFrames) > 0):
        for i in range(0,len(processFrames)):
          if(processFrames[i].is_alive()):
            continue
          else:
            del(processFrames[i])
            a = 0
            break
      else:
        break
      if(a):
        break

def _execFrames(frameInfo,frameScrutiny,cpuAffi):
  proc = multiprocessing.Process(target=execFrames,args=(frameInfo,frameScrutiny,))
  proc.start()
  
  processFramesId = psutil.Process(proc.pid)
  #cpuAffi = []
  #for ca in range(0,int(frameInfo['fThreads'])):
    #cpuAffi.append(ca)
  logClient.debug("CPU AFFINITY : "+ str(cpuAffi))
  processFramesId.set_cpu_affinity(cpuAffi)
  proc.join()

def execFrames(frameInfo,frameScrutiny):
  db_conn = dbRbhus.dbRbhus()
  batchedFrames = db_conn.getBatchedFrames(frameInfo['batchId'])
  hostname,ipAddr = getHostNameIP()
  
  if(sys.platform.find("linux") >=0):
    setproctitle.setproctitle("rD_"+ str(frameInfo['id']) +" : "+ "-".join(batchedFrames))
  
  logClient.debug(str(os.getpid()) + ": execFrames func : "+ str(frameInfo['fileName']))
  hostEff = getEffectiveDetails(db_conn)
  if(hostEff != 0):
    while(1):
      if(setFramesStatus(frameInfo['id'],batchedFrames,constants.framesRunning,db_conn) == 1):
        break
      time.sleep(0.1)

    os.environ['rbhus_washmybutt'] = tempDir + os.sep + str(frameInfo['id']).lstrip().rstrip() +"_"+ str(frameInfo['frameId']).lstrip().rstrip() +".butt"
    os.environ['rbhus_frames']    = ",".join(batchedFrames)
    os.environ['rbhus_taskId']    = str(frameInfo['id']).lstrip().rstrip()
    os.environ['rbhus_frameId']   = str(frameInfo['frameId']).lstrip().rstrip()
    os.environ['rbhus_user']      = str(frameInfo['user']).lstrip().rstrip()
    os.environ['rbhus_fileName']  = str(frameInfo['fileName']).lstrip().rstrip()
    os.environ['rbhus_btCmd']     = str(frameInfo['beforeTaskCmd']).lstrip().rstrip()
    os.environ['rbhus_fileType']  = str(frameInfo['fileType']).lstrip().rstrip()
    os.environ['rbhus_renderer']  = str(frameInfo['renderer']).lstrip().rstrip()
    os.environ['rbhus_renExtArgs']= str(frameInfo['renExtArgs']).lstrip().rstrip()
    os.environ['rbhus_minRam']    = str(frameInfo['minRam']).lstrip().rstrip()
    os.environ['rbhus_maxRam']    = str(frameInfo['maxRam']).lstrip().rstrip()
    os.environ['rbhus_outDir']    = str(frameInfo['outDir']).lstrip().rstrip()
    os.environ['rbhus_outName']   = str(frameInfo['outName']).lstrip().rstrip()
    os.environ['rbhus_logBase']   = str(frameInfo['logBase']).lstrip().rstrip()
    os.environ['rbhus_pad']       = str(frameInfo['pad']).lstrip().rstrip()
    os.environ['rbhus_atCmd']     = str(frameInfo['afterTaskCmd']).lstrip().rstrip()
    os.environ['rbhus_bfCmd']     = str(frameInfo['beforeFrameCmd']).lstrip().rstrip()
    os.environ['rbhus_afCmd']     = str(frameInfo['afterFrameCmd']).lstrip().rstrip()
    os.environ['rbhus_threads']   = str(frameInfo['fThreads']).lstrip().rstrip()
    os.environ['rbhus_layer']      = str(frameInfo['layer']).lstrip().rstrip()
    os.environ['rbhus_camera']    = str(frameInfo['camera']).lstrip().rstrip()
    os.environ['rbhus_resolution'] = str(frameInfo['resolution']).lstrip().rstrip()
    os.environ['rbhus_imageType']   = str(frameInfo['imageType']).lstrip().rstrip()
    if((frameInfo['logBase'] == "default") and (frameInfo['outDir'] != "default")):
      lb = frameInfo['outDir'].rstrip(os.sep) + os.sep + "logs"
      frameInfo['logBase'] = lb
    else:
      frameInfo['logBase'] = tempDir
    os.environ['rbhus_logBase']   = str(frameInfo['logBase']).lstrip().rstrip()
    runScript = getDefaultScript(frameInfo['fileType'], db_conn)
    logClient.debug("runScript : "+ str(runScript))
    os.environ['rbhus_runScript'] = runScript


    logFile = str(frameInfo['logBase']).rstrip(os.sep) + os.sep + str(frameInfo['id']).lstrip().rstrip() +"_"+ frameInfo['batchId'] +".log"
    try:
      db_conn.execute("update frames set logFile=\'"+ str(logFile) +"\' where batchId=\'"+ str(frameInfo['batchId']) +"\'")
    except:
      logClient.debug("update logFile  : "+ str(sys.exc_info()))
      
    os.environ['rbhus_logFile'] = str(logFile).lstrip().rstrip()
    if(sys.platform.find("linux") >=0):
      ruid = pwd.getpwnam(str(frameInfo['user']).lstrip().rstrip())[2]
      rgid = pwd.getpwnam(str(frameInfo['user']).lstrip().rstrip())[3]

    try:
      os.makedirs(str(frameInfo['outDir']),0777)
    except:
      logClient.debug("MKDIR : "+ str(sys.exc_info()[1]))
    if(sys.platform.find("linux") >= 0):
      try:
        os.chmod(str(frameInfo['outDir']),0777)
        os.chown(str(frameInfo['outDir']),ruid,rgid)
      except:
        logClient.debug("MKDIR : "+ str(sys.exc_info()[1]))


    try:
      os.makedirs(str(frameInfo['logBase']),0777)
    except:
      logClient.debug("MKDIR : "+ str(sys.exc_info()[1]))
    try:
      os.chmod(str(frameInfo['logBase']),0777)
      os.chown(str(frameInfo['logBase']),ruid,rgid)
    except:
      logClient.debug("MKDIR : "+ str(sys.exc_info()[1]))


    #Run the beforeFrame shits
    if(str(frameInfo['beforeFrameCmd']) != 'default'):
      logClient.debug("running beforeFrameCmd :"+ str(frameInfo['beforeFrameCmd']))
      runCommand(str(frameInfo['beforeFrameCmd']))



    
    try:
      if(sys.platform.find("win") >= 0):
        runCmd = os.popen('python.exe '+ runScript +' 2>&1','r').read().strip().split("\r\n")[0]
      elif(sys.platform.find("linux") >= 0):
        runCmd = os.popen('python '+ runScript +' 2>&1','r').read().strip().split("\r\n")[0]
    except:
      os.environ['rbhus_exit']   = "1"
      logClient.debug(str(sys.exc_info()))
      while(1):
        if(setFramesStatus(frameInfo['id'],batchedFrames,constants.framesFailed,db_conn) == 1):
          logClient.debug("run cmd failed !! ")
          break
        time.sleep(0.5)

      #Run the afterFrame shits
      if(str(frameInfo['afterFrameCmd']) != 'default'):
        logClient.debug("running afterFrameCmd :"+ str(frameInfo['afterFrameCmd']))
        runCommand(str(frameInfo['afterFrameCmd']))

      while(1):
        if(setFreeCpus(frameInfo, db_conn) ==  1):
          break
        time.sleep(0.5)
      washMyButt(frameInfo['id'],frameInfo['frameId'])
      db_conn.delBatchId(frameInfo['batchId'])
      sys.exit(0)


    logClient.debug("RUN CMD :"+ runCmd)


    logClient.debug("logFile : "+ str(logFile))
    try:
      logD = open(logFile,"a+",0)
      logD.write("START \n"+ hostname +" : "+ time.asctime() +"\n")
      logD.write("FRAMES : "+ " ".join(batchedFrames) +"\n")
    except:
      pass

    while(1):
      if(setFramesStime(frameInfo, db_conn) == 1):
        break
      time.sleep(0.5)


    retryThres = 5
    retryCount = 0
    if(sys.platform.find("linux") >=0):
      while(1):
        try:
          logD.write("/bin/su "+ frameInfo['user'] +" -c \'"+ runCmd +"\' "+ str(logD) +"\n\n")
          fProcess = subprocess.Popen("/bin/su "+ frameInfo['user'] +" -c \'"+ runCmd +"\'",shell=True,stdout=logD,stderr=logD)
          break
        except:
          os.environ['rbhus_exit']   = "2"
          logClient.debug(str(sys.exc_info()))
          retryCount = retryCount + 1
          if(retryCount >= retryThres):
            while(1):
              if(setFramesEtime(frameInfo, db_conn) == 1):
                break
              time.sleep(0.2)
            logClient.debug("retryCount : "+ str(retryCount))

            while(1):
              if(setFramesStatus(frameInfo['id'],batchedFrames,constants.framesFailed,db_conn) == 1):
                break
              time.sleep(0.2)

            #Run the afterFrame shits
            if(str(frameInfo['afterFrameCmd']) != 'default'):
              logClient.debug("running afterFrameCmd :"+ str(frameInfo['afterFrameCmd']))
              runCommand(str(frameInfo['afterFrameCmd']))

            while(1):
              if(setFreeCpus(frameInfo, db_conn) ==  1):
                break
              time.sleep(0.2)
            washMyButt(frameInfo['id'],frameInfo['frameId'])
            db_conn.delBatchId(frameInfo['batchId'])
            sys.exit(0)
        time.sleep(1)

    elif(sys.platform.find("win") >=0):
      logClient.warning("PLATFORM : windoze!")

      logClient.debug(str(runCmd.split()))
      while(1):
        try:
          logClient.debug(str(runCmd.split())+" : "+str(logD))
          fProcess = subprocess.Popen(runCmd.split(),stdout=logD,stderr=logD)
          break
        except:
          os.environ['rbhus_exit']   = "2"
          logClient.debug(str(sys.exc_info()))
          retryCount = retryCount + 1
          if(retryCount >= retryThres):
            while(1):
              if(setFramesEtime(frameInfo, db_conn) == 1):
                break
              time.sleep(0.2)

            while(1):
              if(setFramesStatus(frameInfo['id'],batchedFrames,constants.framesFailed,db_conn) == 1):
                logClient.debug("Break point ZERO")
                break
              time.sleep(0.2)

            #Run the afterFrame shits
            if(str(frameInfo['afterFrameCmd']) != 'default'):
              logClient.debug("running afterFrameCmd :"+ str(frameInfo['afterFrameCmd']))
              runCommand(str(frameInfo['afterFrameCmd']))

            while(1):
              if(setFreeCpus(frameInfo, db_conn) ==  1):
                break
              time.sleep(0.2)
            washMyButt(frameInfo['id'],frameInfo['frameId'])
            db_conn.delBatchId(frameInfo['batchId'])
            sys.exit(0)
        time.sleep(1)

    fProcessPid = [fProcess.pid]

    fProcessPid.insert(0,frameInfo) #send the frameInfo in the first
    #logClient.debug("Frame pid : "+ str(fProcessPid))
    forScrutiny = fProcessPid
    frameScrutiny.put(forScrutiny)

    time.sleep(1)
    kidsForStatus = []
    pidfileLock = multiprocessing.Lock()
    writeFramePidFile(pidfileLock,frameInfo['id'],frameInfo['frameId'],[fProcess.pid])
    while(1):
      kidsForStatus = []
      if(getProcessLastKids(fProcess.pid,kidsForStatus) == 0):
        break
      if(len(kidsForStatus) > 1):
        #logClient.debug("kidsForStatus : "+ str(kidsForStatus))
        while(1):
          if(writeFramePidFile(pidfileLock,frameInfo['id'],frameInfo['frameId'],kidsForStatus) == 1):
            break
          time.sleep(1)

        ### THE BELOW CODE IS WRITTEN FOR A STUPID USECASE WHEN THERE ARE NETWORK PROBLEMS
        fInfo = getFrameInfo(frameInfo['id'],frameInfo['frameId'], db_conn)
        #if((fInfo[0]['status'] == constants.framesHung) or (fInfo[0]['status'] == constants.framesDone)):
        if(isinstance(fInfo, int)):
          continue

        if(fInfo[0]['status'] == constants.framesHung):
          while(1):
            if(setFramesStatus(frameInfo['id'],batchedFrames,constants.framesRunning,db_conn) == 1):
              logClient.debug("Break point MADNESS")
              break
            time.sleep(1)
      else:
        break
      time.sleep(1)

    logClient.debug("-------------------------------")
    logClient.debug("kidsForStatus : "+ str(kidsForStatus))

    try:
      fProcess.wait()
    except:
      logClient.debug(" PROCESS wait!! : "+ str(sys.exc_info()))
    status = fProcess.returncode
    logClient.debug("frame status of pid :"+ str(fProcess.pid) +": "+ str(status))

    fStatus = getFrameStatus(frameInfo['id'],frameInfo['frameId'],db_conn)
    logClient.debug("Frame status afterdone 1: "+ str(fStatus[0]['status']))



    while(1):
      if(setFramesEtime(frameInfo, db_conn) == 1):
        logClient.debug("Break point THREE")
        break
      time.sleep(0.2)



    #DOING THIS FOR WINDOWS.. fucking 3dsmax-server doesnt close after rendering!!!! dont know y 3dsmax is still making bussiness!
    #time.sleep(0.5)
    if(sys.platform.find("win") >= 0):
      killFrame(db_conn,frameInfo['id'],frameInfo['frameId'],pidfileLock,-1)
    try:
      logD.write(hostname +" : "+ time.asctime() +"\nEND\n\n")
      logD.close()
    except:
      pass


    if((status == 0) and (fStatus[0]['status'] != constants.framesKilled)):
      os.environ['rbhus_exit']   = "0"
      while(1):
        if(setFramesStatus(frameInfo['id'],batchedFrames,constants.framesDone,db_conn) == 1):
          logClient.debug("Break point ONE")
          break
        time.sleep(0.2)
    elif(fStatus[0]['status'] != constants.framesKilled):
      os.environ['rbhus_exit']   = str(constants.framesKilled)
      while(1):
        if(setFramesStatus(frameInfo['id'],batchedFrames,constants.framesFailed,db_conn) == 1):
          logClient.debug("Break point TWO")
          break
        time.sleep(0.2)

    #Run the afterFrame shits
    if(str(frameInfo['afterFrameCmd']) != 'default'):
      logClient.debug("running afterFrameCmd :"+ str(frameInfo['afterFrameCmd']))
      runCommand(str(frameInfo['afterFrameCmd']))

    while(1):
      if(setFreeCpus(frameInfo, db_conn) ==  1):
        logClient.debug("Break point FOUR")
        break
      time.sleep(0.2)
    washMyButt(frameInfo['id'],frameInfo['frameId'])
    db_conn.delBatchId(frameInfo['batchId'])
    delFramePidFile(pidfileLock,frameInfo['id'],frameInfo['frameId'])
    sys.exit(0)


def washMyButt(taskid, frameid):
  buttFile = tempDir + os.sep + str(taskid).lstrip().rstrip() +"_"+ str(frameid).lstrip().rstrip() +".butt"
  try:
    bfd = open(buttFile,"r")
  except:
    logClient.debug(str(sys.exc_info()))
    return(0)
  for x in bfd.readlines():
    try:
      os.remove(x.rstrip().lstrip())
    except:
      logClient.debug(str(sys.exc_info()))
  bfd.close()
  try:
    os.remove(buttFile)
  except:
    logClient.debug(str(sys.exc_info()))
  return(1)

def runCommand(rcmd):
  try:
    if(sys.platform.find("win") >= 0):
      runCmd = os.popen('python.exe '+ rcmd +' 2>&1','r')
    elif(sys.platform.find("linux") >= 0):
      runCmd = os.popen('python '+ rcmd +' 2>&1','r')
    retCode = runCmd.close()
    if(retCode == None):
      return(0)
    else:
      return(retCode)
  except:
    logClient.debug("runCmd  : "+ rcmd +" : "+ str(sys.exc_info()))

def getFrameStatus(taskId,frameId, dbconn):
  try:
    rows = dbconn.execute("SELECT frames.status FROM frames \
                    WHERE frames.id = "+ str(taskId) +" \
                    AND frames.frameId = "+ str(frameId), dictionary=True)
    return(rows)
  except:
    logClient.debug(str(sys.exc_info()))
    return(0)

def writeFramePidFile(pidLock,taskId,frameId,pids):
  taskPidF = tempDir + os.sep + "rbhus_"+ str(taskId).rstrip().lstrip() +"_"+ str(frameId).rstrip().lstrip()
  pidDict = {}
  try:
    pidLock.acquire()
    try:
      taskPidD = open(taskPidF,"r+")
      for inPid in taskPidD.readlines():
        pidDict[str(inPid).rstrip().lstrip()] = 0
      taskPidD.close()
    except IOError:
      pass

    for pid in pids:
      if(str(pid).rstrip().lstrip() and str(pid).rstrip().lstrip() != str(os.getpid())):
        pidDict[str(pid).rstrip().lstrip()] = 0

    taskPidD = open(taskPidF,"w")
    if(pidDict):
      for inPid in pidDict.keys():
        taskPidD.writelines(str(inPid) +"\n\r")
    taskPidD.close()
    pidLock.release()
  except:
    logClient.debug(str(sys.exc_info()))
    return(0)
  return(1)

def delFramePidFile(pidLock,taskId,frameId):
  taskPidF = tempDir + os.sep + "rbhus_"+ str(taskId).rstrip().lstrip() +"_"+ str(frameId).rstrip().lstrip()
  try:
    if(isinstance(pidLock, int)):
      if(pidLock != 0):
        pidLock.acquire()
    os.remove(taskPidF)
    if(isinstance(pidLock, int)):
      if(pidLock != 0):
        pidLock.release()
    return(1)
  except:
    logClient.debug(str(sys.exc_info()))
    return(0)


def getFrameInfo(taskid, frameid, dbconn):
  try:
    rows = dbconn.execute("SELECT * FROM frames \
                    WHERE frames.id="+ str(taskid) +" \
                    AND frames.frameId="+ str(frameid), dictionary=True)
  except:
    logClient.debug("1 : "+ str(sys.exc_info()[1]))
    rows = 0
  return(rows)

#error = 1 ; success = 0
def killFrame(dbconn,taskId,frameId,pidLock = 0,statusAfterKill = -1):
  taskPidF = tempDir + os.sep + "rbhus_"+ str(taskId).rstrip().lstrip() +"_"+ str(frameId).rstrip().lstrip()
  batchId = dbconn.getBatchId(taskId,frameId)
  if(batchId):
    batchedFrames = dbconn.getBatchedFrames(batchId)
  else:
    return(0)
  try:
    if(pidLock != 0):
      pidLock.acquire()
    taskPidD = open(taskPidF,"r")
  except:
    if(pidLock != 0):
      pidLock.release()
    return(1)
  kpids = []
  kpidsAll = {}
  for kpid in taskPidD.readlines():
    if(kpid):
      kpidsAll[kpid.rstrip().lstrip()] = 0
  if(kpidsAll):
    kpids = kpidsAll.keys()
  taskPidD.close()

  mainPids = getMainPids()
  logClient.debug("MAIN PIDS : "+ str(mainPids))

  if(pidLock != 0):
    pidLock.release()
  numPids = len(kpids)
  killFail = 0
  fCount = 0
  for kpid in kpids:
    try:
      kpid.rstrip().lstrip()
      #Check if the pid belongs to any mother process . (i think i need to check this only when running on windows .. damn Y WINDOZE)
      if(mainPids):
        if(kpid in mainPids):
          print("Opps .. killing mother process is not allowed .its against humanity!!!")
          continue
      allKids = []
      getProcessLastKids(int(kpid),allKids)
      if(allKids):
        for x in allKids:
          try:
            if(sys.platform.find("linux") >= 0):
              os.kill(int(x),9)
            elif(sys.platform.find("win") >= 0):
              os.system("taskkill /t /f /pid "+ str(x))
          except:
            fCount = fCount + 1
            logClient.debug("killing problem .. please help me murder this")
    except:
      logClient.debug(str(sys.exc_info()))
      killFail += 1
  if((killFail < numPids) and (statusAfterKill != -1)):
    while(1):
      if(setFramesStatus(taskId,batchedFrames,statusAfterKill,dbconn) == 1):
        break
      time.sleep(0.5)
      
  washMyButt(taskId,frameId)
  db_conn.delBatchId(batchId)
  return(0)

def getMainPids():
  mainPids = []
  try:
    mainPidD = open(mainPidFile,"r")
    for x in mainPidD.readlines():
      mainPids.append(x.rstrip().lstrip())
  except:
    logClient.debug("mainPidFile not found : "+ str(sys.exc_info()))
  if(mainPids):
    return(mainPids)
  else:
    return(0)


def frameScrutinizer(frameScrutiny):
  if(sys.platform.find("linux") >=0):
    setproctitle.setproctitle("rD_frameScrutinizer")
  db_conn = dbRbhus.dbRbhus()
  logClient.debug(str(os.getpid()) + ": frameScrutinizer func")
  snoopFramesProcess = []
  while(1):


    while(1):
      a = 1
      if(len(snoopFramesProcess) > 0):
        for i in range(0,len(snoopFramesProcess)):
          if(snoopFramesProcess[i].is_alive()):
            continue
          else:
            del(snoopFramesProcess[i])
            a = 0
            break
      else:
        break
      if(a):
        break

    while(1):
      try:
        frameDets = frameScrutiny.get(timeout=1)
        break
      except:
        while(1):
          a = 1
          if(len(snoopFramesProcess) > 0):
            for i in range(0,len(snoopFramesProcess)):
              if(snoopFramesProcess[i].is_alive()):
                continue
              else:
                del(snoopFramesProcess[i])
                a = 0
                break
          else:
            break
          if(a):
            break



    snoopFramesProcess.append(multiprocessing.Process(target=_snoopFrames,args=(frameDets,)))
    snoopFramesProcess[-1].start()
    time.sleep(0.5)


    while(1):
      a = 1
      if(len(snoopFramesProcess) > 0):
        for i in range(0,len(snoopFramesProcess)):
          if(snoopFramesProcess[i].is_alive()):
            continue
          else:
            del(snoopFramesProcess[i])
            a = 0
            break
      else:
        break
      if(a):
        break


#this should inteligently snoop on any more pids that are spawned by the given pids
#
#welll... yes !!! . INTELIGENTLY!!!! :|
#

def _snoopFrames(fDets):
  proc = multiprocessing.Process(target=snoopFrames,args=(fDets,))
  proc.start()
  proc.join()

def snoopFrames(fDets):
  db_conn = dbRbhus.dbRbhus()
  logClient.debug(str(os.getpid()) + ": snoopFrames func")
  frameInfo = fDets.pop(0)
  ProcessPid = fDets.pop(0)

  if(sys.platform.find("linux") >=0):
    setproctitle.setproctitle("rD_"+ str(frameInfo['id']) +" : "+ str(frameInfo['frameId']))

  maxMemUsed = 0
  logClient.debug(str(frameInfo['id']) +" : "+ str(frameInfo['frameId']))
  try:
    while(1):
      lastKids = []
      vmSize = 0
      getProcessLastKids(ProcessPid,lastKids)
      if(len(lastKids) != 0):
        for framePid in lastKids:
          vmSize = vmSize + int(getProcessVmSize(framePid))
        if(vmSize > maxMemUsed):
          setFramesVmSize(frameInfo,vmSize, db_conn)
          maxMemUsed = vmSize
      else:
        break
      time.sleep(5)
    while(1):
      if(setFramesVmSize(frameInfo,maxMemUsed, db_conn) == 1):
        break
      time.sleep(1)
  except:
    logClient.debug(str(sys.exc_info()))
  sys.exit(0)


def getProcessVmSize(pid):
  vmSizeRet = 0
  try:
    pidDets = psutil.Process(pid)
    vmSizeRet = pidDets.get_memory_info().rss
  except:
    logClient.debug(str(sys.exc_info()))
  if(vmSizeRet < 0):
    vmSizeRet = 0
  return(vmSizeRet)


def setFramesVmSize(frameInfo,vmSize, dbconn):
  try:
    dbconn.execute("UPDATE frames SET ram="+ str(vmSize) +" \
                    WHERE frameId="+ str(frameInfo['frameId']) +" \
                    AND id="+ str(frameInfo['id']))
  except:
    return(0)
  return(1)


def setFramesStime(frameInfo, dbconn):
  try:
    dbconn.execute("UPDATE frames SET sTime=NOW() \
                    WHERE frameId="+ str(frameInfo['frameId']) +" \
                    AND id="+ str(frameInfo['id']))
  except:
    return(0)
  return(1)


def setFramesEtime(frameInfo, dbconn):
  try:
    dbconn.execute("UPDATE frames SET eTime=NOW() \
                    WHERE frameId="+ str(frameInfo['frameId']) +" \
                    AND id="+ str(frameInfo['id']))
  except:
    logClient.debug(str(sys.exc_info()))
    return(0)
  return(1)


def getDefaultScript(fileType, dbconn):
  rows = 0
  try:
    rows = dbconn.execute("SELECT defScript FROM fileType WHERE fileType.fileType=\'"+ str(fileType) +"\'", dictionary=True)
  except:
    return(0)
  if(rows):
    return(rows[0]['defScript'].rstrip().lstrip())
  else:
    logClient.debug("NO SCRIPT")
    return(0)

def setFramesStatus(taskId, frames, status, dbconn):
  if(frames):
    framesStr = " or frames.frameId=".join(str(x) for x in frames)
  else:
    return(1)
  try:
    dbconn.execute("UPDATE frames SET frames.status="+ str(status) +" \
                    WHERE (frames.frameId="+ str(framesStr) +") \
                    AND frames.id="+ str(taskId))
  except:
    return(0)
  logClient.debug("STATUS CHANGED to "+ constants.framesStatus[int(status)] +" : "+ str(taskId) +"_"+ str(frames))
  return(1)


def getEffectiveDetails(db_conn):
  hostname,ipAddr = getHostNameIP()
  try:
    rows = db_conn.execute("SELECT * FROM hostEffectiveResource WHERE ip=\'"+ str(ipAddr) +"\'", dictionary=True)
  except:
    return(0)
  if(isinstance(rows,int)):
    return(0) 
  return(rows[0])



#If not used remove

def atUrService():
  if(sys.platform.find("linux") >=0):
    setproctitle.setproctitle("rD_atUrService")
  db_conn = dbRbhus.dbRbhus()
  logClient.debug(str(os.getpid()) + ": atUrService func")
  while(1):
    try:
      hostName,ipAddr = getHostNameIP()
      serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      serverSocket.bind(("", 6660))
      serverSocket.listen(5)
      break
    except:
      pass
    time.sleep(1)

  while(1):
    clientSocket, address = serverSocket.accept()
    logClient.debug("I got a connection from "+ str(address))
    data = ""
    data = clientSocket.recv(1024)
    data = data.rstrip()
    data = data.lstrip()
    msg = ""
    value = ""
    if(data.rfind(":") != -1):
      msg, value = data.split(":")
    else:
      msg = data
    if(msg == "ALIVE"):
      clientSocket.send("ALIVE")
    elif(msg == "MURDER"):
      try:
        taskId, frameId = value.split("%")
      except:
        continue
      frameInfos = getFrameInfo(taskId, frameId, db_conn)
      killFrame(db_conn,taskId,frameId,0,constants.framesKilled)
      #washMyButt(taskId,frameId)
      #delFramePidFile(0,taskId,frameId)
      
    elif(msg == "RESTART"):
      if(sys.platform.find("linux") >= 0):
        try:
          os.system("reboot >& /dev/null &")
        except:
          logClient.debug(msg)
      elif(sys.platform.find("win") >= 0):
        try:
          os.system("shutdown /r /t 1")
        except:
          logClient.debug(msg)
    elif(msg == "DELETE"):
      if(os.path.isfile(value)):
        try:
          os.remove(value)
        except:
          logClient.debug(msg)
      else:
          logClient.debug(msg)
    while(1):
      try:
        clientSocket.close()
        break
      except:
        pass



# Return a dict of totalSwap and totalMem
def totalMemInfo():
  memDetails = {}
  if(sys.platform.find("linux") >=0):
    meminfo = open("/proc/meminfo","r")
    for x in meminfo.readlines():
      if(x.find("MemTotal") != -1):
        memDetails[x.rstrip().split(":")[0].strip().split()[0]] = x.rstrip().split(":")[1].strip().split()[0]
      if(x.find("SwapTotal") != -1):
        memDetails[x.rstrip().split(":")[0].strip().split()[0]] = x.rstrip().split(":")[1].strip().split()[0]
    meminfo.close()
  elif(sys.platform.find("win") >=0):
    try:
      memDetails["MemTotal"] = psutil.virtual_memory().total
    except:
      memDetails["MemTotal"] ='0'
    try:
      memDetails["SwapTotal"] = psutil.swap_memory().total
    except:
      memDetails["SwapTotal"] = '0'
  logClient.debug(str(memDetails))
  return(memDetails)


# Return a dict of freeSwap and freeMem
def freeMeminfo():
  memDetails = {}
  if(sys.platform.find("linux") >=0):
    meminfo = open("/proc/meminfo","r")
    for x in meminfo.readlines():
      if(x.find("MemFree") != -1):
        memDetails[x.rstrip().split(":")[0].strip().split()[0]] = x.rstrip().split(":")[1].strip().split()[0]
      if(x.find("SwapFree") != -1):
        memDetails[x.rstrip().split(":")[0].strip().split()[0]] = x.rstrip().split(":")[1].strip().split()[0]
    meminfo.close()
  elif(sys.platform.find("win") >=0):
    try:
      memDetails["MemFree"] = psutil.virtual_memory().free
    except:
      memDetails["MemFree"] = '0'
    try:
      memDetails["SwapFree"] = psutil.swap_memory().free
    except:
      memDetails["SwapFree"] = '0'


  return(memDetails)


def getHostGroups(dbconn):
  hostname,ipAddr = getHostNameIP()
  try:
    rows = dbconn.execute("select groups from hostInfo where ip=\""+ str(ipAddr) +"\" group by groups", dictionary=True)
  except:
    raise
  gtr = {}
  retRows = []
  if(rows):
    for row in rows:
      tmpRow = row['groups'].split(",")
      for tr in tmpRow:
        gtr[tr.rstrip().lstrip()] = 1
    for gt in gtr.keys():
      retRows.append(gt)
    return(retRows)
  else:
    return(0)

def setHostInfo(dbconn,hostName,totalRam=0,totalCpus=0,totalSwap=0):
  while(1):
    time.sleep(0.1)
    if(sys.platform.find("linux") >=0):
      plat = "linux"
    elif(sys.platform.find("win") >= 0):
      plat = "win"

    try:
      hostname,ipAddr = getHostNameIP()
      logClient.debug("ipaddr : "+ str(ipAddr))

      try:
        rowss = dbconn.execute("SELECT * FROM hostInfo WHERE ip = \'" + ipAddr + "\'", dictionary=True)
        logClient.debug("hostInfo : "+ str(rowss))
        if(isinstance(rowss,int)):
          rowss = []
      except:
        logClient.debug(str(sys.exc_info()))
        continue
      if(len(rowss) == 0):
        logClient.debug("Hostname is new :)")
        try:
          dbconn.execute("INSERT INTO hostInfo \
                        (hostName,groups,totalRam,totalCpus,totalSwap,ip,os) \
                        VALUES ('" \
                        + str(hostName) + "', '" \
                        + str("default,"+ hostName) + "', " \
                        + str(totalRam) + ", " \
                        + str(totalCpus) + ", " \
                        + str(totalSwap) + ", '" \
                        + str(ipAddr) + "', '" \
                        + str("default,"+ plat) +"')")
        except:
          logClient.debug(str(sys.exc_info()))
      else:
        logClient.debug(str(sys.exc_info()))
        grps = 0
        try:
          grps = getHostGroups(db_conn)
        except:
          logClient.debug(str(sys.exc_info()))

        if(grps):
          try:
            grps.remove(hostName)
          except:
            pass
          try:
            grps.remove("default")
          except:
            pass
          grps.append("default")
          grps.append(hostName)

        try:
          dbconn.execute("UPDATE hostInfo SET \
                          totalRam='"+ str(totalRam) +"', \
                          totalCpus='"+ str(totalCpus) +"', \
                          totalSwap='"+ str(totalSwap) +"' ,\
                          hostName='"+ str(hostName) +"' ,\
                          os='"+ str("default,"+ plat) +"' ,\
                          groups='"+ ",".join(grps) +"' \
                          WHERE ip = \'"+ str(ipAddr) +"\'")
        except:
          logClient.debug(str(sys.exc_info()))


      try:
        rowss = dbconn.execute("SELECT * FROM hostResource WHERE ip = \'" + str(ipAddr) + "\'", dictionary=True)
        if(isinstance(rowss,int)):
          rowss = []
      except:
        logClient.debug(str(sys.exc_info()))
      if(len(rowss) == 0):
        try:
          logClient.debug(" : Trying to insert hostResource")
          dbconn.execute("INSERT INTO hostResource (hostName,ip,freeCpus) VALUES (\'"
                        + hostName +"\',\'" \
                        + ipAddr +"\'," \
                        + str(totalCpus) +")")
        except:
          logClient.debug(str(sys.exc_info()))
      else:
        try:
          logClient.debug(" : Trying to update hostResource")
          dbconn.execute("UPDATE hostResource SET freeCpus=\'"+ str(totalCpus) +"\' WHERE ip=\'"+ str(ipAddr) +"\'")
        except:
          logClient.debug(str(sys.exc_info()))

      try:
        rowss = dbconn.execute("SELECT * FROM hostAlive WHERE ip=\'" + ipAddr + "\'", dictionary=True)
        if(isinstance(rowss,int)):
          rowss = []
      except:
        logClient.debug(str(sys.exc_info()))
      if(len(rowss) == 0):
        try:
          logClient.debug(" : Trying to insert hostAlive")
          dbconn.execute("INSERT INTO hostAlive (hostName,ip) VALUES (\'"+ str(hostName) +"\',\'"+ str(ipAddr) +"\')")
        except:
          logClient.debug(str(sys.exc_info()))
          try:
            logClient.dead(" : Trying to update hostAlive")
            dbconn.execute("UPDATE hostAlive SET ip=\'"+ str(ipAddr) +"\' WHERE hostName=\'"+ str(hostName) +"\'")
          except:
            logClient.debug(str(sys.exc_info()))
          


      try:
        rowss = dbconn.execute("SELECT * FROM hostEffectiveResource WHERE hostName=\'" + str(hostName) + "\'", dictionary=True)
        if(isinstance(rowss,int)):
          rowss = []
      except:
        logClient.debug(str(sys.exc_info()))
      if(len(rowss) == 0):
        try:
          dbconn.execute("INSERT INTO hostEffectiveResource (hostName,ip) VALUES (\'"+ str(hostName) +"\',\'"+ str(ipAddr) +"\')")
        except:
          logClient.debug(str(sys.exc_info()))
          try:
            logClient.dead(" : Trying to update hostEffectiveResource")
            dbconn.execute("UPDATE hostEffectiveResource SET ip=\'"+ str(ipAddr) +"\' WHERE hostName=\'"+ str(hostName) +"\'")
          except:
            logClient.debug(str(sys.exc_info()))
      #upHostAliveStatus(hostName, 1)
      break
    except:
      logClient.debug(str(sys.exc_info()))
      pass


def setHostResMem(hostName, dbconn,freeRam='0',freeSwap='0', load1='0', load5='0', load10='0'):
  hostname,ipAddr = getHostNameIP()
  try:
    dbconn.execute("UPDATE hostResource SET freeRam=\'" + str(freeRam) +"\' \
          , freeSwap=\'"+ str(freeSwap) +"\' \
          , load1=\'"+ str(load1) +"\' \
          , load5=\'"+ str(load5) +"\' \
          , load10=\'"+ str(load10) +"\' \
          WHERE ip=\'"+ str(ipAddr) +"\'")
  except:
    logClient.debug(str(sys.exc_info()))
    return(0)
  return(1)

def setFreeCpus(frameInfo, dbconn):
  hostname,ipAddr = getHostNameIP()
  try:
    dbconn.execute("UPDATE hostResource SET freeCpus=freeCpus+"+ str(frameInfo['fThreads']) +" WHERE ip=\'"+ str(ipAddr) +"\'")
    logClient.debug(" : freeing CPUs : "+ str(hostname) +":"+ str(frameInfo['fThreads']))
  except:
    logClient.debug(str(sys.exc_info()))
    return(0)
  return(1)


def mainFunc():
  logClient.debug(str(os.getpid()) + ": main func")
  signal.signal(signal.SIGTERM,sigHandle)
  myPid = os.getpid()
  logClient.debug("Rbhus : "+ str(myPid))
  p = []
  init()

  frameFcuk = multiprocessing.Queue()
  frameScrutiny = multiprocessing.Queue()

  hostUpdaterProcess = multiprocessing.Process(target=hostUpdater)
  p.append(hostUpdaterProcess)
  hostUpdaterProcess.start()

  getAssignedFramesProcess = multiprocessing.Process(target=getAssignedFrames,args=(frameFcuk,))
  p.append(getAssignedFramesProcess)
  getAssignedFramesProcess.start()

  runFramesProcess = multiprocessing.Process(target=runFrames,args=(frameFcuk,frameScrutiny,))
  p.append(runFramesProcess)
  runFramesProcess.start()

  atUrServiceProcess = multiprocessing.Process(target=atUrService)
  p.append(atUrServiceProcess)
  atUrServiceProcess.start()

  frameScrutinizerProcess = multiprocessing.Process(target=frameScrutinizer,args=(frameScrutiny,))
  p.append(frameScrutinizerProcess)
  frameScrutinizerProcess.start()


  mainPidD = open(mainPidFile,"w",0)
  for i in range(0,len(p)):
    try:
      mainPidD.write(str(p[i].pid) +"\n")
    except:
      print("Couldnt write mainPidFile : "+ str(sys.exc_info()))
  mainPidD.close()



  while(1):
    time.sleep(0.5)
    for i in range(0,len(p)):
      if(p[i].is_alive()):
        time.sleep(0.5)
      else:
        logClient.debug("MAIN Process dead : "+ str(p[i].pid))
        try:
          del(p[i])
        except:
          logClient.debug("MAIN Process dead . cannot delete index")
        break
    if(not p):
      break

  time.sleep(10)


if __name__ == "__main__":
  mainFunc()
