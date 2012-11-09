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
if(sys.platform.find("linux") >= 0):
  import pwd

import pickle
import rbhus.dbRbhus as dbRbhus
import rbhus.constants as constants
if(sys.platform.find("linux") >= 0):
  import psi
  import psi.process
import tempfile
import inspect

time.sleep(1)
hostname = socket.gethostname()
tempDir = tempfile.gettempdir()
mainPidFile = tempDir + os.sep +"rbusClient.pids"
db_conn = dbRbhus.dbRbhus()

if(sys.platform.find("linux") >=0):
  LOG_FILENAME = '/var/log/rbhusClient.log'
elif(sys.platform.find("win") >=0):
  LOG_FILENAME = tempDir + os.sep +"rbusClient_"+ str(hostname) +".log"
  #LOG_FILENAME = "z:"+ os.sep +"pythonTestWindoze.DONOTDELETE"+ os.sep +"rbhus"+ os.sep +"rbusClient_"+ str(hostname) +".log"
logging.BASIC_FORMAT = "%(asctime)s - %(lineno)s -  %(message)s"
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
#logLock = multiprocessing.Lock()
#def logging.debug(msg):
  ##if(sys.platform.find("linux")):
    ##try:
      ##logging.debug(msg)
    ##except:
      ##pass
  ##else:
    ###logLock.acquire()
  #print("debug : "+ msg)
    ##logLock.release()

#def logging.error(msg):
  ##if(sys.platform.find("linux")):
    ##try:
      ##logging.error(msg)
    ##except:
      ##pass
  ##else:
    ###logLock.acquire()
  #print("error : "+ msg)
    ##logLock.release()

# The most stupid signal handler :)
def sigHandle(sigNum, frame):
  myPid = os.getpid()
  logging.debug(str(str(inspect.stack()[1][2])) +" : "+ str(inspect.stack()[1][3]) +" : "+"signal handler called with "+ str(sigNum) +" signal")
  logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+"my pid "+ str(myPid))
  # run this only if linux?! .. omfg .. i dont know !!!!
  if(sys.platform.find("linux")):
    killProcessKids(myPid)
  return(1)


def getProcessLastKids(ppid,lastKids):
  try:
    pidDets = psi.process.Process(ppid)
  except:
    pidDets = None
  try:
    pidKids = pidDets.children()
  except:
    pidKids = None
  if(not pidKids):
    lastKids.append(ppid)
    return(0)
  else:
    for pidKid in pidKids:
      getProcessLastKids(pidKid.pid,lastKids)



def getProcessLastKids_win(ppid,lastKids):
  pidKids = getProcessKids_win(ppid)
  if(not pidKids):
    lastKids.append(ppid)
    return(0)
  else:
    for pidKid in pidKids:
      getProcessLastKids_win(pidKid,lastKids)



def getProcessKids_win(ppid):
  result = {}
  pList = "wmic process get handle,parentprocessid"
  response1 = os.popen(pList + ' 2>&1','r').read().strip().split("\r\n")[1:]
  if(response1):
    for x in response1:
      pid,pppid = x.split()
      try:
        result[pppid]
      except:
        result[pppid] = []
      result[pppid].append(pid.rstrip().lstrip())
    kidsFound = 0
    for parentId in result.keys():
      if(int(parentId) == int(ppid)):
        kidsFound = 1
        return(result[parentId])
    if(kidsFound == 0):
      return None
  else:
    return None



def killProcessKids(ppid):
  try:
    pidDets = psi.process.Process(ppid)
  except:
    logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ "No details : "+ str(ppid))
    return(0)
  try:
    pidKids = pidDets.children()
  except:
    logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ "No children")
    return(0)
  if(not pidKids):
    logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ "killing kid "+ str(ppid))
    os.kill(int(ppid),9)
    return(1)
  else:
    for pidKid in pidKids:
      killProcessKids(pidKid.pid)



# Get the host info and update the database.
def init():
  hostname = socket.gethostname()
  totalCpus = multiprocessing.cpu_count()
  totalMem = totalMemInfo()
  ret = setHostInfo(hostname,totalMem['MemTotal'],totalCpus,totalMem['SwapTotal'])
  if(ret == 1):
    return(1)
  return(0)


def hostUpdater():
  db_conn = dbRbhus.dbRbhus()
  myPid = os.getpid()
  logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) +" : "+ "hostUpdater : "+ str(myPid))
  while(1):
    time.sleep(5)
    hostname = socket.gethostname()
    try:
      freeMem = freeMeminfo()
      logging.debug("WTF0 : "+ str(freeMem))
      loads = loadAvg()
      logging.debug("WTF1 : "+ str(loads))
      setHostResMem(hostname, db_conn,freeMem['MemFree'],freeMem['SwapFree'], loads[0], loads[1], loads[2])
      #print("foooooooooooooooooooooooooooooook")
      #print(hostname)
      #print(freeMem['MemFree'])
      #print(freeMem['SwapFree'])
      #print(loads[0])
      #print(loads[1])
      #print(loads[2])
      #print("fuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuk")
    except:
      logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ str(sys.exc_info()))
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
      logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ str(sys.exc_info()))
  elif(sys.platform.find("win") >=0):
    try:
      cmd = "wmic cpu get loadpercentage"
      try:
        load = str(os.popen(cmd + ' 2>&1','r').read().strip().split("\r\n")[1])
      except:
        load = 1
        logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ str(sys.exc_info()))
      if(load):
        loads = [str(load), '0', '0']
    except:
      logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ str(sys.exc_info()))
  return(loads)



def upHostAliveStatus(hostName, status, dbconn):
  try:
    dbconn.execute("UPDATE hostAlive SET status = "+ str(status) +" WHERE hostName=\'"+ str(hostName) +"\'")
  except:
    return(0)
  return(1)



def getAssignedFrames(qAssigned):
  db_conn = dbRbhus.dbRbhus()
  logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ str(os.getpid()) + ": getAssignedFrames func")
  while(1):
    hostname = socket.gethostname()
    rows = 0
    try:
      rows = db_conn.execute("SELECT frames.frameId, frames.fThreads, tasks.* FROM frames, tasks \
                      WHERE frames.hostName=\'"+ str(hostname) +"\' \
                      AND tasks.id=frames.id \
                      AND frames.status="+ str(constants.framesAssigned) +" \
                      ORDER BY frames.frameId", dictionary=True)
    except:
      logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ "1 : "+ str(sys.exc_info()[1]))
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
            logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ "2 : "+ str(sys.exc_info()[1]))
          time.sleep(1)
    time.sleep(1)

  sys.exit(0)


def runFrames(qRun,frameScrutiny):
  db_conn = dbRbhus.dbRbhus()
  logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ str(os.getpid()) + ": runFrames func")
  processFrames = []
  while(1):
    time.sleep(0.2)
    hostEff = getEffectiveDetails(db_conn)

    totalPids = multiprocessing.cpu_count()
    if(hostEff):
      eCpus = hostEff['eCpus']
      if(eCpus == 0):
        totalPids = multiprocessing.cpu_count()
      elif(eCpus != 0):
        totalPids = eCpus
      else:
        totalPids = 1
    while(1):
      if(len(processFrames) >= totalPids):
        for i in range(0,len(processFrames)):
          if(processFrames[i].is_alive()):
            pass
          else:
            del(processFrames[i])
            break
        if(len(processFrames) < totalPids):
          break
        if(not processFrames):
          break
      else:
        break
      time.sleep(0.1)


    while(1):
      try:
        frameInfo = qRun.get()
        break
      except:
        time.sleep(0.2)
    logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ "Got frameInfo : "+ str(frameInfo))
    processFrames.append(multiprocessing.Process(target=execFrames,args=(frameInfo,frameScrutiny,)))
    processFrames[-1].start()



def execFrames(frameInfo,frameScrutiny):
  db_conn = dbRbhus.dbRbhus()
  logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ str(os.getpid()) + ": execFrames func : "+ str(frameInfo['fileName']))
  hostEff = getEffectiveDetails(db_conn)
  if(hostEff != 0):
    while(1):
      if(setFramesStatus(frameInfo['id'],frameInfo['frameId'],constants.framesRunning) == 1):
        break
      time.sleep(0.1)

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
    os.environ['rbhus_layer']      = str(frameInfo['layer'])
    os.environ['rbhus_imageType']   = str(frameInfo['imageType']).lstrip().rstrip()
    if((frameInfo['logBase'] == "default") and (frameInfo['outDir'] != "default")):
      lb = frameInfo['outDir'].rstrip(os.sep) + os.sep + "logs"
      frameInfo['logBase'] = lb
    else:
      frameInfo['logBase'] = tempDir
    os.environ['rbhus_logBase']   = str(frameInfo['logBase']).lstrip().rstrip()



    logFile = str(frameInfo['logBase']).rstrip(os.sep) + os.sep + str(frameInfo['id']).lstrip().rstrip() +"_"+ str(frameInfo['frameId']).rjust(4,"0") +".log"
    os.environ['rbhus_logFile'] = str(logFile).lstrip().rstrip()
    if(sys.platform.find("linux") >=0):
      ruid = pwd.getpwnam(str(frameInfo['user']).lstrip().rstrip())[2]
      rgid = pwd.getpwnam(str(frameInfo['user']).lstrip().rstrip())[3]
    #envFile = "/tmp/"+ str(myPid) +".rbhus"
    #logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ envFile)
    #envFileDesc = open(envFile,"w")
    #pickle.dump(envPickled,envFileDesc)
    #envFileDesc.close()
    try:
      os.makedirs(str(frameInfo['outDir']),0777)
    except:
      logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ "MKDIR : "+ str(sys.exc_info()[1]))
    if(sys.platform.find("linux") >= 0):
      try:
        os.chmod(str(frameInfo['outDir']),0777)
        os.chown(str(frameInfo['outDir']),ruid,rgid)
      except:
        logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ "MKDIR : "+ str(sys.exc_info()[1]))


    try:
      os.makedirs(str(frameInfo['logBase']),0777)
    except:
      logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ "MKDIR : "+ str(sys.exc_info()[1]))
    try:
      os.chmod(str(frameInfo['logBase']),0777)
      os.chown(str(frameInfo['logBase']),ruid,rgid)
    except:
      logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ "MKDIR : "+ str(sys.exc_info()[1]))


    #Run the beforeFrame shits
    if(str(frameInfo['beforeFrameCmd']) != 'default'):
      logging.debug("running beforeFrameCmd :"+ str(frameInfo['beforeFrameCmd']))
      runCommand(str(frameInfo['beforeFrameCmd']))



    runScript = getDefaultScript(frameInfo['fileType'])
    logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ "runScript : "+ str(runScript))
    try:
      if(sys.platform.find("win") >= 0):
        runCmd = os.popen('python.exe '+ runScript +' 2>&1','r').read().strip().split("\r\n")[0]
      elif(sys.platform.find("linux") >= 0):
        runCmd = os.popen('python '+ runScript +' 2>&1','r').read().strip().split("\r\n")[0]
    except:
      os.environ['rbhus_exit']   = "1"
      logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ "runCmd  : "+ str(sys.exc_info()))
      while(1):
        if(setFramesStatus(frameInfo['id'],frameInfo['frameId'],constants.framesFailed) == 1):
          logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ "run cmd failed !! ")
          break
        time.sleep(0.5)

      #Run the afterFrame shits
      if(str(frameInfo['afterFrameCmd']) != 'default'):
        logging.debug("running afterFrameCmd :"+ str(frameInfo['afterFrameCmd']))
        runCommand(str(frameInfo['afterFrameCmd']))

      while(1):
        if(setFreeCpus(frameInfo, db_conn) ==  1):
          break
        time.sleep(0.5)
      sys.exit(0)


    logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ "RUN CMD :"+ runCmd)


    logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ "logFile : "+ str(logFile))
    try:
      logD = open(logFile,"a+",0)
      logD.write("START \n"+ socket.gethostname() +" : "+ time.asctime() +"\n")
    except:
      pass

    while(1):
      if(setFramesStime(frameInfo) == 1):
        break
      time.sleep(0.5)


    retryThres = 5
    retryCount = 0
    if(sys.platform.find("linux") >=0):
      while(1):
        try:
          logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ "/bin/su "+ frameInfo['user'] +" -c \'"+ runCmd +"\' "+ str(logD))
          fProcess = subprocess.Popen("/bin/su "+ frameInfo['user'] +" -c \'"+ runCmd +"\'",shell=True,stdout=logD,stderr=logD)
          break
        except:
          os.environ['rbhus_exit']   = "2"
          logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ str(sys.exc_info()))
          retryCount = retryCount + 1
          if(retryCount >= retryThres):
            while(1):
              if(setFramesEtime(frameInfo) == 1):
                break
              time.sleep(0.2)
            logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ "retryCount : "+ str(retryCount))

            while(1):
              if(setFramesStatus(frameInfo['id'],frameInfo['frameId'],constants.framesFailed) == 1):
                break
              time.sleep(0.2)

            #Run the afterFrame shits
            if(str(frameInfo['afterFrameCmd']) != 'default'):
              logging.debug("running afterFrameCmd :"+ str(frameInfo['afterFrameCmd']))
              runCommand(str(frameInfo['afterFrameCmd']))

            while(1):
              if(setFreeCpus(frameInfo, db_conn) ==  1):
                break
              time.sleep(0.2)
            logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ "setFreeCpus  ")

            sys.exit(0)
        time.sleep(1)

    elif(sys.platform.find("win") >=0):
      logging.warning("PLATFORM : windoze!")

      logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ str(runCmd.split()))
      while(1):
        try:
          logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ str(runCmd.split())+" : "+str(logD))
          fProcess = subprocess.Popen(runCmd.split(),stdout=logD,stderr=logD)
          break
        except:
          os.environ['rbhus_exit']   = "2"
          logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ str(sys.exc_info()))
          retryCount = retryCount + 1
          if(retryCount >= retryThres):
            while(1):
              if(setFramesEtime(frameInfo) == 1):
                break
              time.sleep(0.2)

            while(1):
              if(setFramesStatus(frameInfo['id'],frameInfo['frameId'],constants.framesFailed) == 1):
                logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ "Break point ZERO")
                break
              time.sleep(0.2)

            #Run the afterFrame shits
            if(str(frameInfo['afterFrameCmd']) != 'default'):
              logging.debug("running afterFrameCmd :"+ str(frameInfo['afterFrameCmd']))
              runCommand(str(frameInfo['afterFrameCmd']))

            while(1):
              if(setFreeCpus(frameInfo, db_conn) ==  1):
                break
              time.sleep(0.2)

            sys.exit(0)
        time.sleep(1)

    #time.sleep(0.5)
    fProcessPid = [fProcess.pid]

    fProcessPid.insert(0,frameInfo) #send the frameInfo in the first
    logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ "Frame pid : "+ str(fProcessPid))
    forScrutiny = fProcessPid
    frameScrutiny.put(forScrutiny)


    kidsForStatus = []
    pidfileLock = multiprocessing.Lock()
    while(1):
      kidsForStatus = []
      if(sys.platform.find("linux") >= 0):
        if(getProcessLastKids(fProcess.pid,kidsForStatus) == 0):
          break
      elif(sys.platform.find("win") >= 0):
        if(getProcessLastKids_win(fProcess.pid,kidsForStatus) == 0):
          break
      if(len(kidsForStatus) > 0):
        logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ "kidsForStatus : "+ str(kidsForStatus))
        while(1):
          if(writeFramePidFile(pidfileLock,frameInfo['id'],frameInfo['frameId'],kidsForStatus) == 1):
            break
          time.sleep(1)
      time.sleep(2)

    logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ "-------------------------------")
    logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ "kidsForStatus : "+ str(kidsForStatus))

    try:
      fProcess.wait()
    except:
      logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " PROCESS wait!! : "+ str(sys.exc_info()))
    status = fProcess.returncode
    logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ "frame status of pid :"+ str(fProcess.pid) +": "+ str(status))

    fStatus = getFrameStatus(frameInfo['id'],frameInfo['frameId'])
    logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ "Frame status afterdone 1: "+ str(fStatus[0]['status']))

    if((status == 0) and (fStatus[0]['status'] != constants.framesKilled)):
      os.environ['rbhus_exit']   = "0"
      while(1):
        if(setFramesStatus(frameInfo['id'],frameInfo['frameId'],constants.framesDone) == 1):
          logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ "Break point ONE")
          break
        time.sleep(0.2)
    elif(fStatus[0]['status'] != constants.framesKilled):
      os.environ['rbhus_exit']   = str(constants.framesKilled)
      while(1):
        if(setFramesStatus(frameInfo['id'],frameInfo['frameId'],constants.framesFailed) == 1):
          logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ "Break point TWO")
          break
        time.sleep(0.2)

    while(1):
      if(setFramesEtime(frameInfo) == 1):
        logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ "Break point THREE")
        break
      time.sleep(0.2)



    #DOING THIS FOR WINDOWS.. fucking 3dsmax-server doesnt close after rendering!!!! dont know y 3dsmax is still making bussiness!
    #time.sleep(0.5)
    if(sys.platform.find("win") >= 0):
      killFrame(frameInfo['id'],frameInfo['frameId'],pidfileLock,-1)
    delFramePidFile(pidfileLock,frameInfo['id'],frameInfo['frameId'])


    #Run the afterFrame shits
    if(str(frameInfo['afterFrameCmd']) != 'default'):
      logging.debug("running afterFrameCmd :"+ str(frameInfo['afterFrameCmd']))
      runCommand(str(frameInfo['afterFrameCmd']))


    try:
      logD.write(socket.gethostname() +" : "+ time.asctime() +"\nEND\n\n")
      logD.close()
    except:
      pass
    while(1):
      if(setFreeCpus(frameInfo, db_conn) ==  1):
        logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ "Break point FOUR")
        break
      time.sleep(0.2)
    sys.exit(0)


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
    logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ "runCmd  : "+ rcmd +" : "+ str(sys.exc_info()))

def getFrameStatus(taskId,frameId):
  try:
    rows = db_conn.execute("SELECT frames.status FROM frames \
                    WHERE frames.id = "+ str(taskId) +" \
                    AND frames.frameId = "+ str(frameId), dictionary=True)
    return(rows)
  except:
    logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ str(sys.exc_info()))
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
    logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ str(sys.exc_info()))
    return(0)
  return(1)

def delFramePidFile(pidLock,taskId,frameId):
  taskPidF = tempDir + os.sep + "rbhus_"+ str(taskId).rstrip().lstrip() +"_"+ str(frameId).rstrip().lstrip()
  try:
    if(isinstance(pidLock, int)):
      pidLock.acquire()
    os.remove(taskPidF)
    if(isinstance(pidLock, int)):
      pidLock.release()
    return(1)
  except:
    logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ str(sys.exc_info()))
    return(0)


def getFrameInfo(taskid, frameid, dbconn):
  try:
    rows = dbconn.execute("SELECT * FROM frames \
                    WHERE frames.id="+ str(taskid) +" \
                    AND frames.frameId="+ str(frameid), dictionary=True)
  except:
    logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ "1 : "+ str(sys.exc_info()[1]))
    rows = 0
  return(rows)

#error = 1 ; success = 0
def killFrame(taskId,frameId,pidLock = 0,statusAfterKill = -1):
  taskPidF = tempDir + os.sep + "rbhus_"+ str(taskId).rstrip().lstrip() +"_"+ str(frameId).rstrip().lstrip()
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
  logging.debug("MAIN PIDS : "+ str(mainPids))

  if(pidLock != 0):
    pidLock.release()
  numPids = len(kpids)
  killFail = 0
  fCount = 0
  for kpid in kpids:
    try:
      kpid.rstrip().lstrip()
      #Check if the pid belongs to any mother process . (i think i need to check this only when running on windows .. damn Y WINDOZE)
      if(kpid in mainPids):
        print("Opps .. killing mother process is not allowed .its against humanity!!!")
        continue
      if(sys.platform.find("linux") >= 0):
        if(kpid):
          try:
            os.kill(int(kpid),signal.SIGTERM)
          except:
            fCount = fCount + 1
            logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ "killing problem .. please help me murder this")
      elif(sys.platform.find("win") >= 0):
        if(kpid):
          try:
            os.system("taskkill /t /f /pid "+ str(kpid))
          except:
            fCount = fCount + 1
            logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ "killing problem .. please help me murder this")
    except:
      e = sys.exc_info()[1]
      logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ str(e))
      killFail += 1
  if((killFail < numPids) and (statusAfterKill != -1)):
    while(1):
      if(setFramesStatus(taskId,frameId,statusAfterKill) == 1):
        break
      time.sleep(0.5)
  return(0)

def getMainPids():
  mainPidD = open(mainPidFile,"r")
  mainPids = []
  for x in mainPidD.readlines():
    mainPids.append(x.rstrip().lstrip())
    logging.debug("MAIN PIDS : "+ str(mainPids))
  if(mainPids):
    return(mainPids)
  else:
    return(0)

#For future ref for loading custom envs from files in diff paths
#DOES NOT WORK ON WINDOZE!
#def setSysEnviron(envPath):
  #import glob
  #evnFilesSh = glob.glob(envPath.rstrip("/") +"/*")
  #for envFile in evnFilesSh:
    #envF = open(envFile,"r")
    #for envLine in envF.readlines():
      #if(not envLine.startswith("#")):
        #if(envLine.startswith("export")):
          #os.environ[envLine.split()[-1].split("=")[0]] = envLine.split()[-1].split("=")[1]
  #return(1)


def frameScrutinizer(frameScrutiny):
  db_conn = dbRbhus.dbRbhus()
  logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ str(os.getpid()) + ": frameScrutinizer func")
  snoopFramesProcess = []
  while(1):
    while(1):
      time.sleep(0.2)
      try:
        frameDets = frameScrutiny.get()
        break
      except:
        pass
      if(len(snoopFramesProcess) > 0):
        for i in range(0,len(snoopFramesProcess)):
          if(snoopFramesProcess[i].is_alive()):
            continue
          else:
            logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ "snoopFrameProcess dead : "+ str(snoopFramesProcess[i].pid))
            del(snoopFramesProcess[i])
            break


    snoopFramesProcess.append(multiprocessing.Process(target=snoopFrames,args=(frameDets,)))
    snoopFramesProcess[-1].start()


#this should inteligently snoop on any more pids that are spawned by the given pids
#
#welll... yes !!! . INTELIGENTLY!!!! :|
#
def snoopFrames(fDets):
  db_conn = dbRbhus.dbRbhus()
  logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ str(os.getpid()) + ": snoopFrames func")
  frameInfo = fDets.pop(0)
  ProcessPid = fDets.pop(0)
  forMean = []

  logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ str(os.getpid()) + ": snoopFrames func : "+ str(ProcessPid) +" : "+ str(frameInfo))
  lastKids = []
  while(1):
    lastKids = []
    vmSize = 0
    if(sys.platform.find("win") >= 0):
      lKids = getProcessLastKids_win(ProcessPid,lastKids)
      if(lKids == 0):
        break
    elif(sys.platform.find("linux") >= 0):
      lKids = getProcessLastKids(ProcessPid,lastKids)
      if(lKids == 0):
        break
    if(len(lastKids) != 0):
      for framePid in lastKids:
        vmSize = vmSize + int(getProcessVmSize(framePid))
      forMean.append(vmSize)
      forMean.sort()
      vmSizeAvg = forMean[(len(forMean)-1)/2]
      setFramesVmSize(frameInfo,vmSizeAvg)
      time.sleep(0.2)
      fInfo = getFrameInfo(frameInfo['id'],frameInfo['frameId'], db_conn)
      if(fInfo[0]['status'] == constants.framesHung):
        while(1):
          if(setFramesStatus(frameInfo['id'],frameInfo['frameId'],constants.framesRunning) == 1):
            logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ "Break point SNOOOOOOOOOP")
            break
          time.sleep(1)
      time.sleep(2)
    else:
      continue
  if(len(forMean) > 0):
    forMean.sort()
    vmSizeAvg = forMean[len(forMean)/2]
    while(1):
      if(setFramesVmSize(frameInfo,vmSizeAvg) == 1):
        break
      time.sleep(1)
  sys.exit(0)


def getProcessVmSize(pid):
  vmSizeRet = 0
  if(sys.platform.find("win") >= 0):
    try:
      cmd = "wmic process "+ str(pid) +" get workingsetsize"
      vmSizeRet = os.popen(cmd + ' 2>&1','r').read().strip().split("\r\n")[1]
    except:
      return(0)
  elif(sys.platform.find("linux") >= 0):
    try:
      pidFile = open("/proc/"+ str(pid) +"/status","r")
      for line in pidFile.readlines():
        if(line.find('VmPeak') == 0):
          pidFile.close()
          vmSizeRet = line.lstrip().rstrip().split()[1]
    except:
      return(0)
  return(vmSizeRet)


def setFramesVmSize(frameInfo,vmSize):
  try:
    db_conn.execute("UPDATE frames SET ram="+ str(vmSize) +" \
                    WHERE frameId="+ str(frameInfo['frameId']) +" \
                    AND id="+ str(frameInfo['id']))
  except:
    return(0)
  return(1)


def setFramesStime(frameInfo):
  try:
    db_conn.execute("UPDATE frames SET sTime=NOW() \
                    WHERE frameId="+ str(frameInfo['frameId']) +" \
                    AND id="+ str(frameInfo['id']))
  except:
    return(0)
  return(1)


def setFramesEtime(frameInfo):
  try:
    db_conn.execute("UPDATE frames SET eTime=NOW() \
                    WHERE frameId="+ str(frameInfo['frameId']) +" \
                    AND id="+ str(frameInfo['id']))
  except:
    logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ str(sys.exc_info()))
    return(0)
  return(1)


def getDefaultScript(fileType):
  rows = 0
  try:
    rows = db_conn.execute("SELECT defScript FROM fileType WHERE fileType.fileType=\'"+ str(fileType) +"\'", dictionary=True)
  except:
    return(0)
  if(rows):
    print("DEF script : "+ str(rows[0]['defScript']))
    return(rows[0]['defScript'].rstrip().lstrip())
  else:
    logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ "NO SCRIPT")
    return(0)

def setFramesStatus(taskId, frameId, status):
  try:
    db_conn.execute("UPDATE frames SET status="+ str(status) +" \
                    WHERE frameId="+ str(frameId) +" \
                    AND id="+ str(taskId))
  except:
    return(0)
  return(1)


def getEffectiveDetails(db_conn):
  hostname = socket.gethostname()
  try:
    rows = db_conn.execute("SELECT * FROM hostEffectiveResource WHERE hostName=\'"+ hostname +"\'", dictionary=True)
  except:
    return(0)
  return(rows[0])



#If not used remove

def atUrService():
  db_conn = dbRbhus.dbRbhus()
  logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ str(os.getpid()) + ": atUrService func")
  while(1):
    try:
      hostName = socket.gethostname()
      serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      serverSocket.bind(("", 6660))
      serverSocket.listen(5)
      break
    except:
      pass
    time.sleep(1)

  while(1):
    clientSocket, address = serverSocket.accept()
    logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ "I got a connection from "+ str(address))
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
      killFrame(taskId,frameId,0,constants.framesKilled)
      delFramePidFile(0,taskId,frameId)
      #while(1):
        #if(setFreeCpus(frameInfos) == 1):
          #break
        #time.sleep(0.2)
    elif(msg == "RESTART"):
      if(sys.platform.find("linux") >= 0):
        try:
          os.system("reboot >& /dev/null &")
        except:
          logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ msg)
      elif(sys.platform.find("win") >= 0):
        try:
          os.system("shutdown /r /t 1")
        except:
          logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ msg)
    elif(msg == "DELETE"):
      if(os.path.isfile(value)):
        try:
          os.remove(value)
        except:
          logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ msg)
      else:
          logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ msg)
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
    totalSwapCmd = "wmic os get sizestoredinpagingfiles"
    totalMemCmd = "wmic os get totalvisiblememorysize"
    try:
      memDetails["MemTotal"] = os.popen(totalMemCmd + ' 2>&1','r').read().strip().split("\r\n")[1]
    except:
      memDetails["MemTotal"] ='0'
    try:
      memDetails["SwapTotal"] = os.popen(totalSwapCmd + ' 2>&1','r').read().strip().split("\r\n")[1]
    except:
      memDetails["SwapTotal"] = '0'
  logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ str(memDetails))
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
    freeRamCmd = "wmic os get freephysicalmemory"
    freeSwapCmd = "wmic os get freespaceinpagingfiles"
    try:
      memDetails["MemFree"] = os.popen(freeRamCmd + ' 2>&1','r').read().strip().split("\r\n")[1]
    except:
      memDetails["MemFree"] = '0'
    try:
      memDetails["SwapFree"] = os.popen(freeSwapCmd + ' 2>&1','r').read().strip().split("\r\n")[1]
    except:
      memDetails["SwapFree"] = '0'


  return(memDetails)


def getHostGroups(hostName):
    try:
      rows = db_conn.execute("select groups from hostInfo where hostName=\""+ str(hostName) +"\" group by groups", dictionary=True)
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

def setHostInfo(hostName,totalRam=0,totalCpus=0,totalSwap=0):
  while(1):
    time.sleep(0.1)
    if(sys.platform.find("linux") >=0):
      plat = "linux"
    elif(sys.platform.find("win") >= 0):
      plat = "win"

    try:
      ipAddr = socket.gethostbyname(socket.gethostname()).strip()
      logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ "ipaddr : "+ str(ipAddr))

      try:
        rowss = db_conn.execute("SELECT * FROM hostInfo WHERE hostName = \'" + hostName + "\'", dictionary=True)
        logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ "hostInfo : "+ str(rowss))
        if(isinstance(rowss,int)):
          rowss = []
      except:
        logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ str(sys.exc_info()))
        continue
      if(len(rowss) == 0):
        logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ "Hostname is new :)")
        try:
          db_conn.execute("INSERT INTO hostInfo \
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
          logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ str(sys.exc_info()))
      else:
        logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ str(sys.exc_info()))
        grps = 0
        try:
          grps = getHostGroups(hostName)
        except:
          logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ str(sys.exc_info()))

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
          db_conn.execute("UPDATE hostInfo SET \
                          totalRam='"+ str(totalRam) +"', \
                          totalCpus='"+ str(totalCpus) +"', \
                          totalSwap='"+ str(totalSwap) +"' ,\
                          ip='"+ str(ipAddr) +"' ,\
                          os='"+ str("default,"+ plat) +"' ,\
                          groups='"+ ",".join(grps) +"' \
                          WHERE hostName = \'"+ str(hostName) +"\'")
        except:
          logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ str(sys.exc_info()))
          continue


      try:
        rowss = db_conn.execute("SELECT * FROM hostResource WHERE hostName = \'" + str(hostName) + "\'", dictionary=True)
        if(isinstance(rowss,int)):
          rowss = []
      except:
        logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ str(sys.exc_info()))
      if(len(rowss) == 0):
        try:
          logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : Trying to insert hostResource")
          db_conn.execute("INSERT INTO hostResource (hostName, freeCpus) VALUES (\'"
                        + hostName +"\'," \
                        + str(totalCpus) +")")
        except:
          logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ str(sys.exc_info()))
          continue
      else:
        try:
          logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : Trying to update hostResource")
          db_conn.execute("UPDATE hostResource SET freeCpus=\'"+ str(totalCpus) +"\' WHERE hostName=\'"+ str(hostName) +"\'")
        except:
          logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ str(sys.exc_info()))
          continue

      try:
        rowss = db_conn.execute("SELECT * FROM hostAlive WHERE hostName=\'" + hostName + "\'", dictionary=True)
        if(isinstance(rowss,int)):
          rowss = []
      except:
        logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ str(sys.exc_info()))
      if(len(rowss) == 0):
        try:
          logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : Trying to insert hostAlive")
          db_conn.execute("INSERT INTO hostAlive (hostName) VALUES (\'"+ str(hostName) +"\')")
        except:
          logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ str(sys.exc_info()))
          continue


      try:
        rowss = db_conn.execute("SELECT * FROM hostEffectiveResource WHERE hostName=\'" + str(hostName) + "\'", dictionary=True)
        if(isinstance(rowss,int)):
          rowss = []
      except:
        logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ str(sys.exc_info()))
      if(len(rowss) == 0):
        try:
          db_conn.execute("INSERT INTO hostEffectiveResource (hostName) VALUES (\'"+ str(hostName) +"\')")
        except:
          logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ str(sys.exc_info()))
          continue
      #upHostAliveStatus(hostName, 1)
      break
    except:
      logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ str(sys.exc_info()))
      pass


def setHostResMem(hostName, dbconn,freeRam='0',freeSwap='0', load1='0', load5='0', load10='0'):
  try:
    dbconn.execute("UPDATE hostResource SET freeRam=\'" + str(freeRam) +"\' \
          , freeSwap=\'"+ str(freeSwap) +"\' \
          , load1=\'"+ str(load1) +"\' \
          , load5=\'"+ str(load5) +"\' \
          , load10=\'"+ str(load10) +"\' \
          WHERE hostName=\'"+ str(hostName) +"\'")
  except:
    logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ str(sys.exc_info()))
    return(0)
  return(1)

def setFreeCpus(frameInfo, dbconn):
  hostName = socket.gethostname()
  try:
    dbconn.execute("UPDATE hostResource SET freeCpus=freeCpus+"+ str(frameInfo['fThreads']) +" WHERE hostName=\'"+ str(hostName) +"\'")
    logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : freeing CPUs : "+ str(hostName) +":"+ str(frameInfo['fThreads']))
  except:
    logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ str(sys.exc_info()))
    return(0)
  return(1)


def mainFunc():
  logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ str(os.getpid()) + ": main func")
  signal.signal(signal.SIGTERM,sigHandle)
  myPid = os.getpid()
  logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ "Rbhus : "+ str(myPid))
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



  frameFcuk.close()
  frameFcuk.join_thread()
  frameScrutiny.close()
  frameScrutiny.join_thread()

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
        logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ "MAIN Process dead : "+ str(p[i].pid))
        try:
          del(p[i])
        except:
          logging.debug(str(inspect.stack()[1][2]) +" : "+ str(inspect.stack()[1][3]) + " : "+ "MAIN Process dead . cannot delete index")
        break
    if(not p):
      break

  time.sleep(10)


if __name__ == "__main__":
  mainFunc()
