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
import logging.handlers
import time
import signal
import subprocess
import psutil
import re
import hashlib
if(sys.platform.find("linux") >= 0):
  import pwd

import pickle
import rbhus.dbRbhus as dbRbhus
import rbhus.constants as constants
import rbhus.utils as rUtils
if(sys.platform.find("linux") >= 0):
  import setproctitle
  setproctitle.setproctitle("rD")
import tempfile
import inspect
import zmq
import MySQLdb


hostname = socket.gethostname()
tempDir = tempfile.gettempdir()
mainPidFile = tempDir + os.sep +"rbhusDrone.pids"
pidOnlyFile = tempDir + os.sep +"rbhusDroneMain.pid"

db_conn = dbRbhus.dbRbhus()

if(sys.platform.find("win") >= 0):
  try:
    username = os.environ['USERNAME']
  except:
    username = "nobody"
if(sys.platform.find("linux") >= 0):
  try:
    username = os.environ['USER']
  except:
    username = "nobody"

LOG_FILENAME = logging.FileHandler(tempDir + os.sep +"rbhusClient_"+ username +"_"+ str(hostname) +".log")

if(sys.platform.find("win") >= 0):
  LOG_FILENAME = logging.FileHandler("z:/pythonTestWindoze.DONOTDELETE/logs/rbhusClient_"+ username +"_"+ str(hostname) +".log")

singular = tempDir + os.sep + "singularity"

logClient = logging.getLogger("logClient")
logClient.setLevel(logging.DEBUG)
BASIC_FORMAT = logging.Formatter("%(asctime)s - %(funcName)s - %(levelname)s - %(lineno)s - %(message)s")
#ROTATE_FILENAME = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=104857600, backupCount=3)
LOG_FILENAME.setFormatter(BASIC_FORMAT)
logClient.addHandler(LOG_FILENAME)


def sigHandle(sigNum, frame):
  myPid = os.getpid()
  logClient.debug("signal handler called with "+ str(sigNum) +" signal")
  logClient.debug("my pid "+ str(myPid))
  # run this only if linux?! .. omfg .. i dont know !!!!
  logClient.debug("starting to kill processes")
  try:
    os.remove(mainPidFile)
    logClient.debug("removed mainPidFile")
  except:
    pass
  try:
    os.remove(pidOnlyFile)
    logClient.debug("removed pidOnlyFile")
  except:
    pass
  clientQuit(myPid)
  os._exit(0)



def getProcessLastKids(ppid,lastKids):
  try:
    pidDets = psutil.Process(ppid)
  except:
    logClient.debug(str(sys.exc_info()))
    return(0)

  try:
    pidKids = pidDets.children(recursive=True)
  except:
    logClient.debug(str(sys.exc_info()))
    return(0)
  if(pidKids):
    for pidKid in pidKids:
      lastKids.append(pidKid.pid)
  lastKids.append(ppid)
  return(1)


def getallkids(mpid,leafPids,branchPids):
  mmpid = psutil.Process(int(mpid))
  mylasts = mmpid.children()
  if(not mylasts):
    leafPids.append(mpid)
    return()
  else:
    branchPids.append(mpid)
    for x in mylasts:
      getallkids(int(x.pid),leafPids,branchPids)

def clientQuit(ppid):
  lkids = []
  pparents = []
  getallkids(ppid,lkids,pparents)
  try:
    pparents.remove(ppid)
  except:
    pass

  if(lkids):
    for x in lkids:
      try:
        os.kill(int(x),signal.SIGTERM)
        logClient.debug("pid : "+ str(x) +" : killed")
      except:
        logClient.debug(str(sys.exc_info()))
  if(pparents):
    for x in pparents:
      try:
        os.kill(int(x),signal.SIGTERM)
        logClient.debug("pid : "+ str(x) +" : killed")
      except:
        logClient.debug(str(sys.exc_info()))
  return()


# Get the host info and update the database.
def init():
  # checkHostNameDb()
  totalCpus = multiprocessing.cpu_count()
  totalMem = totalMemInfo()
  ret = setHostInfo(db_conn,totalMem['MemTotal'],totalCpus,totalMem['SwapTotal'])
  updateIdle()
  updateHostNameDb()
  if(ret == 1):
    return(1)
  return(0)

def updateIdle():
  hostname, ipAddr = getHostNameIP()
  db_conn = dbRbhus.dbRbhus()
  try:
    db_conn.execute("update hostInfo set idleLast = \"" + str(MySQLdb.Timestamp.now()) + "\" where ip=\'" + str(ipAddr) + "\'")
  except:
    logClient.debug(sys.exc_info())
    return (0)


def getMacAddress():
  mac = ""
  if(sys.platform.find('win') >= 0):
    for line in os.popen("ipconfig /all"):
      if line.lstrip().startswith('Physical Address'):
        mac = line.split(':')[1].strip().replace('-',':')
        break
  else:
    for line in os.popen("ifconfig"):
      b = re.search("(([0-9]|[a-z]|[A-Z]){2}|:){11}", line)
      if (b):
        mac = str(b.group())
        break
  return(mac)


def checkHostNameDb():
  hdb = dbRbhus.dbRbhusHost()
  maccy =  getMacAddress().lower()
  try:
    row = hdb.execute("select * from main where macc='"+ maccy +"'",dictionary=True)
  except:
    logClient.debug(str(sys.exc_info()))
    return(0)
  if(row):
    det = row[-1]
    realName = det['name']
    if(sys.platform.find("win") >= 0):
      os.system("wmic computersystem where name=\"%COMPUTERNAME%\" call rename name=\""+ str(realName) +"\"")

def updateHostNameDb():
  hdb = dbRbhus.dbRbhusHost()
  maccy = getMacAddress().lower()
  hostname, ipaddr = getHostNameIP()
  try:
    hdb.execute("delete from main where macc='"+ maccy +"'")
  except:
    logClient.debug(sys.exc_info())

  try:
    hdb.execute("insert into main (macc,ip,name) values ('{0}', '{1}', '{2}')".format(maccy,ipaddr,hostname))
  except:
    logClient.debug(sys.exc_info())

def hostUpdater():
  if(sys.platform.find("linux") >=0):
    setproctitle.setproctitle("rD_hostUpdater")
  db_conn = dbRbhus.dbRbhus()
  myPid = os.getpid()
  logClient.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) +" : "+ "hostUpdater : "+ str(myPid))
  while(1):
    time.sleep(5)
    try:
      freeMem = freeMeminfo()
      #logClient.debug("WTF0 : "+ str(freeMem))
      loads = loadAvg()
      #logClient.debug("WTF1 : "+ str(loads))
      setHostResMem(db_conn,freeMem['MemFree'],freeMem['SwapFree'], loads[0], loads[1], loads[2])
    except:
      logClient.debug(str(sys.exc_info()))
      continue
  sys.exit(0)


def hostUpdaterSys():
  if(sys.platform.find("linux") >=0):
    setproctitle.setproctitle("rD_hostUpdaterSys")
  db_conn = dbRbhus.dbRbhus()
  db_log = dbRbhus.dbRbhusLog()
  hostname,ipAddr = getHostNameIP()
  myPid = os.getpid()
  logClient.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) +" : "+ "hostUpdaterSys : "+ str(myPid))
  while(1):
    time.sleep(5)
    try:
      rows = db_conn.execute("select * from hostSystem where ip='"+ str(ipAddr) +"' and hostName='"+ str(hostname) +"'", dictionary=True)
      if(rows):
        hostdets = rows[-1]
        if(hostdets['systemUpdateStatus'] == constants.hostSystemUpdateScheduled):
          if(sys.platform.find("linux") >= 0):
            db_conn.execute("update hostSystem set systemUpdateStatus="+ str(constants.hostSystemUpdateRunning) +" where ip='"+ str(ipAddr) +"' and hostName='"+ str(hostname) +"'")
            os.environ['masterSystem'] = hostdets['masterSystem']
            db_conn.execute("update hostSystem set sTimeUpdate=now() where ip='"+ str(ipAddr) +"' and hostName='"+ str(hostname) +"'")
            up = subprocess.Popen("/opt/rbhus/etc/system/linuxUpdate.py")
            up.wait()
            db_conn.execute("update hostSystem set eTimeUpdate=now() where ip='"+ str(ipAddr) +"' and hostName='"+ str(hostname) +"'")
            status = up.returncode
            if(not status):
              db_conn.execute("update hostSystem set systemUpdateStatus="+ str(constants.hostSystemUpdateDone) +" where ip='"+ str(ipAddr) +"' and hostName='"+ str(hostname) +"'")
            else:
              db_conn.execute("update hostSystem set systemUpdateStatus="+ str(constants.hostSystemUpdateFail) +" where ip='"+ str(ipAddr) +"' and hostName='"+ str(hostname) +"'")

    except:
      logClient.debug(str(sys.exc_info()))
      db_conn.execute("update hostSystem set systemUpdateStatus="+ str(constants.hostSystemUpdateFail) +" where ip='"+ str(ipAddr) +"' and hostName='"+ str(hostname) +"'")
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
                      WHERE frames.hostName='"+ str(hostname) +"' \
                      AND tasks.id=frames.id \
                      AND frames.ip='"+ str(ipAddr) +"' \
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
      time.sleep(1)
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
  processFramesId.cpu_affinity(cpuAffi)
  proc.join()


def execFrames(frameInfo,frameScrutiny):
  db_conn = dbRbhus.dbRbhus()
  batchedFrames = db_conn.getBatchedFrames(frameInfo['batchId'])
  hostname,ipAddr = getHostNameIP()

  #create a zmq socket and get a random port for communi ation with the plugin scripts
  context = zmq.Context()
  socket = context.socket(zmq.REP)
  port = socket.bind_to_random_port("tcp://127.0.0.1")
  os.environ['rbhus_ipc_port'] = str(port)
  socket.poll(timeout=1)
  poller = zmq.Poller()
  poller.register(socket, zmq.POLLIN)


  if(sys.platform.find("linux") >=0):
    setproctitle.setproctitle("rD_"+ str(frameInfo['id']) +" : "+ "-".join(batchedFrames))

  logClient.debug(str(os.getpid()) + ": execFrames func : "+ str(frameInfo['fileName']))
  hostEff = getEffectiveDetails(db_conn)
  if(hostEff != 0):
    while(1):
      if(setFramesStatus(frameInfo['id'],batchedFrames,constants.framesRunning,db_conn) == 1):
        break
      time.sleep(0.1)
    os.environ['rbhus_isRendering'] = "1"
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
    os.environ['rbhus_renExtEnv'] = str(frameInfo['renExtEnv']).lstrip().rstrip()
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


    logFile = str(frameInfo['logBase']).rstrip(os.sep) + os.sep + str(frameInfo['batchId']) +".log"
    try:
      db_conn.execute("update frames set logFile=\'"+ str(logFile) +"\' where batchId=\'"+ str(frameInfo['batchId']) +"\'")
    except:
      logClient.debug("update logFile  : "+ str(sys.exc_info()))
    try:
      logD = open(logFile,"a+",0)
    except:
      logClient.debug(sys.exc_info())
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

    runCmd = None
    try:
      if(sys.platform.find("win") >= 0):
        runScriptProc = subprocess.Popen(['python.exe',runScript],stderr=logD,stdout=logD)
      elif(sys.platform.find("linux") >= 0):
        runScriptProc = subprocess.Popen("python \"{0}\"".format(runScript),shell=True,stderr=logD,stdout=logD)
      runCmd = socket.recv_unicode()
      logClient.debug("run cmd :  "+ str(runCmd))
      # while True:
      #   sockets = dict(poller.poll(10000))
      #   if (sockets):
      #     for s in sockets.keys():
      #       if (sockets[s] == zmq.POLLIN):
      #         try:
      #           runCmd = s.recv_unicode()
      #           # s.send_unicode("ack")
      #         except:
      #           logClient.debug(sys.exc_info())
      #         break
      #     break
      #   logClient.debug(runScriptProc.communicate())
      #   runScriptProcPoll = runScriptProc.poll()
      #   logClient.debug("poll : "+ str(runScriptProcPoll))

      try:
        msg = runScriptProc.communicate()
        logClient.debug("socket closed "+ str(msg))
        socket.close()
        context.term()
      except:
        logClient.debug(sys.exc_info())
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
      #db_conn.setTaskDone(frameInfo['id'])
      rbhusLog(frameInfo)
      sys.exit(0)


    logClient.debug("RUN CMD :"+ str(runCmd))


    logClient.debug("logFile : "+ str(logFile))
    try:
      logD.write("\n")
      logD.write("RUN CMD :"+ str(runCmd))
      logD.write("\n")
      logD.write("START : "+ str(frameInfo['batchId']) + " : "+ str(hostname) +" : "+ str(time.asctime()) +"\n")
      logD.write("\n")
      logD.write("FRAMES : "+ " ".join(batchedFrames) +"\n")
    except:
      pass

    while(1):
      if(setFramesStime(frameInfo, db_conn) == 1):
        break
      time.sleep(0.5)


    retryThres = 5
    retryCount = 0
    if(sys.platform.find("linux") >= 0):
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
              time.sleep(0.5)
            washMyButt(frameInfo['id'],frameInfo['frameId'])
            db_conn.delBatchId(frameInfo['batchId'])
            #db_conn.setTaskDone(frameInfo['id'])
            rbhusLog(frameInfo)
            sys.exit(0)
        time.sleep(1)

    elif(sys.platform.find("win") >= 0):
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
              time.sleep(0.5)
            washMyButt(frameInfo['id'],frameInfo['frameId'])
            db_conn.delBatchId(frameInfo['batchId'])
            #db_conn.setTaskDone(frameInfo['id'])
            rbhusLog(frameInfo)
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
              #logClient.debug("Break point MADNESS")
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
      logD.write("FRAMES : "+ " ".join(batchedFrames) +"\n")
      logD.write("\n")
      logD.write("END : "+ str(frameInfo['batchId']) + " : "+ str(hostname) +" : "+ str(time.asctime()) +"\n")
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
      time.sleep(0.5)
    rbhusLog(frameInfo)
    washMyButt(frameInfo['id'],frameInfo['frameId'])
    db_conn.delBatchId(frameInfo['batchId'])
    #db_conn.setTaskDone(frameInfo['id'])
    delFramePidFile(pidfileLock,frameInfo['id'],frameInfo['frameId'])
    sys.exit(0)


def rbhusLog(lframeInfo):
  try:
    dbconnLog = dbRbhus.dbRbhusLog()
    dbconn = dbRbhus.dbRbhus()
    fIns = dbconn.getFrameInfo(lframeInfo['id'],lframeInfo['frameId'])
    fIn = 0
    tDelta = 0
    hostname,ipAddr = getHostNameIP()
    if(fIns):
      fIn = fIns
    if(fIn):
      eT = fIn['eTime']
      sT = fIn['sTime']
      tDelta = int((eT - sT).total_seconds())

    sha256 = hashlib.sha256(lframeInfo['fileName'])
    try:
      dbconnLog.execute("insert into tasksLog \
                         (sha256,projId,avgEfficiency,fileName,date,timeSpentOnResource,ip) \
                         values ('"+ str(sha256.hexdigest()) +"',"+ \
                         str(fIns['projId']) +","+ \
                         str(fIns['efficiency'] if(fIns['efficiency']) else 100) +",'"+ \
                         str(lframeInfo['fileName']).lstrip().rstrip() +"',date(now()),"+ \
                         str(tDelta) +",'"+ str(ipAddr) +"') \
                         on duplicate key \
                         update timeSpentOnResource=timeSpentOnResource+"+ str(tDelta) +",avgEfficiency=(avgEfficiency+"+ str(fIns['efficiency'] if(fIns['efficiency']) else 100) +")/2")
    except:
      logClient.debug("1 : "+ str(sys.exc_info()))
    try:
      dbconnLog.execute("insert into hostLog \
                           (ip,timeOnRender,date,avgEfficiency) \
                           values ('"+ str(ipAddr) +"',"+ str(tDelta) +",date(now()),"+ str(fIns['efficiency'] if(fIns['efficiency']) else 100) +") \
                           on duplicate key update \
                           timeOnRender=timeOnRender+"+ str(tDelta) +",totalJobs=totalJobs+1,avgEfficiency=(avgEfficiency+"+ str(fIns['efficiency'] if(fIns['efficiency']) else 100) +")/2")
    except:
      logClient.debug("2 : "+ str(sys.exc_info()))
    return(1)
  except:
    logClient.debug(str(sys.exc_info()))
    return(0)



def washMyButt(taskid, frameid):
  buttFile = tempDir + os.sep + str(taskid).lstrip().rstrip() +"_"+ str(frameid).lstrip().rstrip() +".butt"
  try:
    bfd = open(buttFile,"r")
  except:
    logClient.debug(str(sys.exc_info()))
    return(0)
  for x in bfd.readlines():
    if(len(x.rstrip().lstrip()) > 0):
      logClient.debug("washMyButt : : : "+ x.rstrip().lstrip())
      logClient.debug(str(sys.exc_info()))
      try:
        os.remove(x.rstrip().lstrip())
      except:
        logClient.debug(str(sys.exc_info()))
  try:
    bfd.close()
  except:
    logClient.debug(str(sys.exc_info()))
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
      try:
        taskPidD = open(taskPidF,"r+")
        for inPid in taskPidD.readlines():
          if(inPid):
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
          if(inPid):
            taskPidD.writelines(str(inPid) +"\n\r")
      taskPidD.close()
    except:
      logClient.debug(str(sys.exc_info()))
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
  #logClient.debug("WSB 30")
  washMyButt(taskId,frameId)
  #logClient.debug("WSB 31")
  dbconn.delBatchId(batchId)
  #logClient.debug("WSB 32")
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
    time.sleep(1)


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
    time.sleep(1)
  sys.exit(0)

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
    cpuEmax = 100 * frameInfo['fThreads']
  elif(sys.platform.find("win") >= 0):
    cpuEmax = 100

  maxMemUsed = 0
  cpuE = 0
  count = 1
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
      cpuEff = getCPUeffeciency(ProcessPid)
      if(cpuEff):
        cpuE = cpuE + cpuEff
      cpuEE = cpuE/count
      cpuEEE = (100*cpuEE)/cpuEmax
      setCpuEffeciency(frameInfo,cpuEEE,db_conn)
      count = count + 1
      time.sleep(1)
    while(1):
      if(setFramesVmSize(frameInfo,maxMemUsed,db_conn) == 1):
        break
      time.sleep(2)
  except:
    logClient.debug(str(sys.exc_info()))
  sys.exit(0)


def getCPUeffeciency(pid):
  leafs = []
  everythingelse = []
  getallkids(pid,leafs,everythingelse)
  cpu_percent = 0
  if(leafs):
    for x in leafs:
      try:
        p = psutil.Process(x)
        cpu_percent = cpu_percent + int(p.cpu_percent(interval=2))
      except:
        logClient.debug(str(sys.exc_info()))
        pass
  return(cpu_percent)





def getProcessVmSize(pid):
  vmSizeRet = 0
  try:
    pidDets = psutil.Process(pid)
    if(sys.platform.find("win") >= 0):
      vmSizeRet = pidDets.memory_info().rss + pidDets.memory_info().vms
    if(sys.platform.find("linux") >= 0):
      vmSizeRet = pidDets.memory_info().rss
  except:
    logClient.debug(str(sys.exc_info()))
  if(vmSizeRet < 0):
    vmSizeRet = 0
  return(vmSizeRet)


def setFramesVmSize(frameInfo,vmSize,dbconn):
  try:
    dbconn.execute("UPDATE frames SET ram="+ str(vmSize) +" \
                    WHERE batchId='"+ str(frameInfo['batchId']) +"' \
                    AND id="+ str(frameInfo['id']))
  except:
    logClient.debug(str(sys.exc_info()))
    return(0)
  return(1)


def setCpuEffeciency(frameInfo,cpuEff,dbconn):
  try:
    dbconn.execute("UPDATE frames SET efficiency="+ str(cpuEff) +" \
                    WHERE batchId='"+ str(frameInfo['batchId']) +"' \
                    AND id="+ str(frameInfo['id']))
  except:
    logClient.debug(str(sys.exc_info()))
    return(0)
  return(1)



def setFramesStime(frameInfo, dbconn):
  try:
    dbconn.execute("UPDATE frames SET sTime=NOW() \
                    WHERE batchId='"+ str(frameInfo['batchId']) +"' \
                    AND id="+ str(frameInfo['id']))
  except:
    return(0)
  return(1)


def setFramesEtime(frameInfo, dbconn):
  try:
    dbconn.execute("UPDATE frames SET eTime=NOW() \
                    WHERE batchId='"+ str(frameInfo['batchId']) +"' \
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



def singularity():
  if(os.path.exists(singular)):
    logClient.debug("CLIENT STILL RUNNING!")
    sys.exit(1)
  else:
    f = open(singular,"w")
    if(sys.platform.find("linux") >= 0):
      import fcntl
      flags = fcntl.LOCK_EX
      fcntl.lockf(f,flags)

    if(sys.platform.find("win") >= 0):
      import msvcrt
      op = msvcrt.LK_LOCK
      f.seek(0)
      msvcrt.locking(f,op,1)
    return(0)



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
      serverSocket.bind(("", constants.clientListenPort))
      serverSocket.listen(5)
      break
    except:
      pass
    time.sleep(1)

  while(1):
    clientSocket, address = serverSocket.accept()
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
    logClient.debug("I got a connection from "+ str(address) +" : "+ str(data))
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
    elif(msg == "MURDERNHOLD"):
      try:
        taskId, frameId = value.split("%")
      except:
        continue
      frameInfos = getFrameInfo(taskId, frameId, db_conn)
      killFrame(db_conn,taskId,frameId,0,constants.framesHold)

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
  #if(sys.platform.find("linux") >=0):
    #meminfo = open("/proc/meminfo","r")
    #for x in meminfo.readlines():
      #if(x.find("MemTotal") != -1):
        #memDetails[x.rstrip().split(":")[0].strip().split()[0]] = x.rstrip().split(":")[1].strip().split()[0]
      #if(x.find("SwapTotal") != -1):
        #memDetails[x.rstrip().split(":")[0].strip().split()[0]] = x.rstrip().split(":")[1].strip().split()[0]
    #meminfo.close()
  #elif(sys.platform.find("win") >=0):
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
  #if(sys.platform.find("linux") >=0):
    #meminfo = open("/proc/meminfo","r")
    #for x in meminfo.readlines():
      #if(x.find("MemFree") != -1):
        #memDetails[x.rstrip().split(":")[0].strip().split()[0]] = x.rstrip().split(":")[1].strip().split()[0]
      #if(x.find("SwapFree") != -1):
        #memDetails[x.rstrip().split(":")[0].strip().split()[0]] = x.rstrip().split(":")[1].strip().split()[0]
    #meminfo.close()
  #elif(sys.platform.find("win") >=0):
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
    rows = dbconn.execute("select groups from hostGroups where ip='"+ str(ipAddr) +"' group by groups", dictionary=True)
  except:
    raise
  gtr = {}
  retRows = []
  if(rows):
    for row in rows:
      tmpRow = row['groups'].split()
      for tr in tmpRow:
        gtr[tr.rstrip().lstrip()] = 1
    for gt in gtr.keys():
      if(gt):
        retRows.append(gt)
    return(retRows)
  else:
    return(0)


def getHostState(db_conn):
  hostname,ipAddr = getHostNameIP()
  try:
    rows = db_conn.execute("select * from hostStates where ip='"+ str(ipAddr) +"'",dictionary=True)
    if(rows):
      return(rows[-1])
    else:
      return(0)
  except:
    logClient.debug(str(sys.exc_info()))
    return(0)



def setHostInfo(dbconn,totalRam=0,totalCpus=0,totalSwap=0):
  while(1):
    time.sleep(1)
    if(sys.platform.find("linux") >=0):
      plat = "linux"
    elif(sys.platform.find("win") >= 0):
      plat = "win"

    try:
      hostname,ipAddr = getHostNameIP()
      logClient.debug("trying to insert hostInfo")
      if(ipAddr == "127.0.0.1"):
        time.sleep(5)
        continue
      logClient.debug("step 1")
      oldState = getHostState(dbconn)
      grps = []
      oldstatus = constants.hostInfoDisable
      oldweight = 1
      if(oldState):
        grps = oldState['groups'].split(",")
        oldstatus = oldState['status']
        oldweight = oldState['weight']
      try:
        grps.append("default")
        grps.append(hostname)
        grps.append(str(totalCpus) +"-core")
        grps = list(set(grps))
        # dbconn.execute("delete from hostInfo where ip='"+ str(ipAddr) +"'")
        dbconn.execute("INSERT INTO hostInfo \
                      (hostName,status,groups,totalRam,totalCpus,totalSwap,ip,weight,os) \
                      VALUES ('" \
                      + str(hostname) + "', '" \
                      + str(oldstatus) + "', '" \
                      + str(",".join(grps)) + "', " \
                      + str(totalRam) + ", " \
                      + str(totalCpus) + ", " \
                      + str(totalSwap) + ", '" \
                      + str(ipAddr) + "', '" \
                      + str(oldweight) + "', '" \
                      + str("default,"+ plat) +"') \
                        ON DUPLICATE KEY UPDATE \
                        totalRam="+ str(totalRam) +", \
                        totalCpus="+ str(totalCpus) +", \
                        totalSwap="+ str(totalSwap) +" ,\
                        weight="+ str(oldweight) +" ,\
                        hostName='"+ str(hostname) +"' ,\
                        ip='"+ str(ipAddr) +"' , \
                        os='"+ str("default,"+ plat) +"' ,\
                        groups='"+ str(",".join(grps)) +"'")
      except:
        logClient.debug("hostInfo update error")
        logClient.debug(str(sys.exc_info()))
        sys.exit(1)



      try:
        logClient.debug("trying to insert hostResource")
        dbconn.execute("INSERT INTO hostResource (hostName,ip,freeCpus) VALUES ('" \
                      + hostname +"','" \
                      + ipAddr +"'," \
                      + str(totalCpus) +") \
                        ON DUPLICATE KEY UPDATE \
                        freeCpus="+ str(totalCpus) +", \
                        ip=\'"+ str(ipAddr) +"\'")
      except:
        logClient.debug("hostResource update error")
        logClient.debug(str(sys.exc_info()))
        sys.exit(1)



      try:
        logClient.debug(" : Trying to insert hostAlive")
        dbconn.execute("INSERT INTO hostAlive (hostName,ip) VALUES ('" \
                        + str(hostname) +"','" \
                        + str(ipAddr) +"') \
                          ON DUPLICATE KEY UPDATE \
                          ip='"+ str(ipAddr) +"'")
      except:
        logClient.debug("hostAlive update error")
        logClient.debug(str(sys.exc_info()))
        sys.exit(1)


      try:
        dbconn.execute("INSERT INTO hostEffectiveResource (hostName,ip) VALUES ('" \
                        + str(hostname) +"','" \
                        + str(ipAddr) +"') \
                          ON DUPLICATE KEY UPDATE \
                          ip='"+ str(ipAddr) +"'")
      except:
        logClient.debug("hostEffectiveResource update error")
        logClient.debug(str(sys.exc_info()))
        sys.exit(1)
      try:
        dbconn.execute("insert into hostStates (ip) values ('"+ str(ipAddr) +"')")
      except:
        logClient.debug("hostStates insert error")
        logClient.debug(str(sys.exc_info()))
      try:
        dbconn.execute("insert into hostSystem (ip,hostName) values ('"+ str(ipAddr) +"','"+ str(hostname) +"')")
      except:
        logClient.debug("hostStates insert error")
        logClient.debug(str(sys.exc_info()))
      break
    except:
      logClient.debug(str(sys.exc_info()))
      pass


def setHostResMem(dbconn,freeRam='0',freeSwap='0', load1='0', load5='0', load10='0'):
  hostname,ipAddr = getHostNameIP()
  if(ipAddr == "127.0.0.1"):
    return(0)
  try:
    dbconn.execute("UPDATE hostResource SET freeRam=" + str(freeRam) +" \
          , freeSwap="+ str(freeSwap) +" \
          , load1="+ str(load1) +" \
          , load5="+ str(load5) +" \
          , load10="+ str(load10) +" \
          WHERE ip='"+ str(ipAddr) +"'")
  except:
    logClient.debug(str(sys.exc_info()))
    return(0)
  return(1)

def setFreeCpus(frameInfo, dbconn):
  hostname,ipAddr = getHostNameIP()
  if(ipAddr == "127.0.0.1"):
    return(0)
  try:
    dbconn.execute("UPDATE hostResource SET freeCpus=IF((freeCpus+"+ str(frameInfo['fThreads']) +")>="+ str(multiprocessing.cpu_count()) +","+ str(multiprocessing.cpu_count()) +",freeCpus+"+ str(frameInfo['fThreads']) +") WHERE ip='"+ str(ipAddr) +"'")
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

  #if(os.path.exists(mainPidFile)):
    #logClient.debug("rbhusDrone allready running . please check the do a proper cleanup before restarting")
    #sys.exit(1)

  #singularity()
  time.sleep(60)
  p = []
  init()

  frameFcuk = multiprocessing.Queue()
  frameScrutiny = multiprocessing.Queue()

  hostUpdaterProcess = multiprocessing.Process(target=hostUpdater)
  p.append(hostUpdaterProcess)
  hostUpdaterProcess.start()

  hostUpdaterSysProcess = multiprocessing.Process(target=hostUpdaterSys)
  p.append(hostUpdaterSysProcess)
  hostUpdaterSysProcess.start()

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

  mainOnlyD = open(pidOnlyFile,"w",0)
  try:
    mainOnlyD.write(str(myPid) +"\n")
  except:
    print("Couldnt write pidOnlyFile : "+ str(sys.exc_info()))
  mainOnlyD.close()


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
  try:
    os.remove(mainPidFile)
  except:
    pass
  try:
    os.remove(pidOnlyFile)
  except:
    pass
  sys.exit(0)


if __name__ == "__main__":
  mainFunc()
