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

# SERVER!!!!!!!!
import sys
import os
import logging
import time
import signal
import setproctitle
import tempfile
import uuid
import rbhus.dbRbhus as dbRbhus
import rbhus.constants as constants

LOG_FILENAME = '/var/log/rbhusQueen_scheduler.log'
logging.BASIC_FORMAT = "%(asctime)s - %(funcName)s - %(levelname)s - %(message)s"
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

db_conn = dbRbhus.dbRbhus()
tempDir = tempfile.gettempdir()
mainPidFile = tempDir + os.sep +"rbusServer.pids"





setproctitle.setproctitle("rQ_scheduler")

def getFreeHosts():
  freeHosts = []
  potentHosts = db_conn.getPotentHosts()
  #logging.debug("potentHosts : "+ str(potentHosts))
  if(potentHosts):
    for hostDetails in potentHosts:
      if(hostDetails["eCpus"] == 0):
        hostDetails["eCpus"] = hostDetails["totalCpus"]
        if((hostDetails["freeCpus"] <= hostDetails["totalCpus"]) and (hostDetails["freeCpus"] > 0)):
          freeHosts.append(hostDetails)
      elif(hostDetails['eCpus'] != 0):
        if((hostDetails["totalCpus"] - hostDetails["freeCpus"]) < hostDetails["eCpus"]):
          freeHosts.append(hostDetails)
  return(freeHosts)

def getBestHost(activeTask):
  freeHosts = getFreeHosts()
  #logging.debug("free host : "+ str(freeHosts))
  #Try to giv to the last host that the task ran
  for freeHost in freeHosts:
    if(not activeTask['lastHost']):
      activeTask['lastHost'] = ""
    if(freeHost['hostName'].find(activeTask['lastHost']) >= 0):
      hostGroups = freeHost["groups"].split(",")
      taskGroups = activeTask["hostGroups"].split(",")
      hostOss = freeHost["os"].split(",")
      taskOss = activeTask["os"].split(",")
      inOSflag = 1
      for tOs in taskOss:
        if(tOs not in hostOss):
          inOSflag = 0

      inGroupFlag = 1
      for taskGroup in taskGroups:
        if(taskGroup not in hostGroups):
          inGroupFlag = 0

      if(inGroupFlag and inOSflag):
        if(freeHost['freeRam'] >= activeTask['minRam']):
          if(activeTask['threads'] == 0):
            if(freeHost['totalCpus'] - freeHost['freeCpus'] == 0):
              #logging.debug("free host : "+ str(freeHost))
              return(freeHost)
          else:
            if((freeHost['freeCpus'] - activeTask['threads']) >= (freeHost['totalCpus'] - freeHost['eCpus'])):
              #logging.debug("free host : "+ str(freeHost))
              return(freeHost)

  #If no last host then find a new one :)
  for freeHost in freeHosts:
    hostGroups = freeHost["groups"].split(",")
    taskGroups = activeTask["hostGroups"].split(",")
    hostOss = freeHost["os"].split(",")
    taskOss = activeTask["os"].split(",")
    inOSflag = 1
    for tOs in taskOss:
      if(tOs not in hostOss):
        inOSflag = 0

    inGroupFlag = 1
    for taskGroup in taskGroups:
      if(taskGroup not in hostGroups):
        inGroupFlag = 0
    if(inGroupFlag and inOSflag):
      if(freeHost['freeRam'] >= activeTask['minRam']):
        if(activeTask['threads'] == 0):
          if(freeHost['totalCpus'] - freeHost['freeCpus'] == 0):
            #logging.debug("free host : "+ str(freeHost))
            return(freeHost)
        else:
          if((freeHost['freeCpus'] - activeTask['threads']) >= (freeHost['totalCpus'] - freeHost['eCpus'])):
            #logging.debug("free host : "+ str(freeHost))
            return(freeHost)
  return(0)

def arrangedActiveTasks():
  priorities = {}
  arrangedTasks = []
  activeTasks = db_conn.getActiveTasks()
  afterTasks = {}
  #logging.debug("activeTasks :"+ str(activeTasks))
  if(activeTasks):
    for activeTask in activeTasks:
      try:
        priorities[activeTask["priority"]].append(activeTask)
      except:
        priorities[activeTask["priority"]] = []
        priorities[activeTask["priority"]].append(activeTask)
      #try:
        #afterTasks[activeTask["afterTasks"]].append(activeTask["id"])
      #except:
        #afterTasks[activeTask["afterTasks"]] = []
        #afterTasks[activeTask["afterTasks"]].append(activeTask["id"])
    pKeys = priorities.keys()
    pKeys.sort(reverse=True)
    #logging.debug("Sorted Keys :"+ str(pKeys))

    numPrios = len(pKeys)
    totalPrios = sum(pKeys)

    pcentPkeys = {}
    for pKey in pKeys:
      pcentPkeys[pKey] = (float(pKey) * 100) / float(totalPrios)
    #logging.debug("pcentPkeys :" + str(pcentPkeys))

    pcentPkeysRun = {}
    totalRunFrames = 0
    for pKey in pKeys:
      for activeTask in priorities[pKey]:
        runShit = db_conn.getRunFrames(activeTask["id"])
        if(runShit):
          totalRunFrames = totalRunFrames + len(runShit)

    for pKey in pKeys:
      runFrames = 0
      for activeTask in priorities[pKey]:
        runShit = db_conn.getRunFrames(activeTask["id"])
        if(runShit):
          runFrames = runFrames + len(runShit)
      try:
        pcentPkeysRun[pKey] = (100 * float(runFrames)) / float(totalRunFrames)
      except:
        pcentPkeysRun[pKey] = 0
    #logging.debug("pcentPkeysRun :"+ str(pcentPkeysRun))

    #The logic below SUCKS!!!! :`(
    pKeysTmp = pKeys
    pKeysRevised = []
    while(len(pKeysTmp)):
      doneCrapping = 0
      for pKey in pKeysTmp:
        if(pcentPkeysRun[pKey] <= pcentPkeys[pKey]):
          pKeysRevised.append(pKey)
          pKeysTmp.remove(pKey)
          doneCrapping = 1
          break
      if(doneCrapping == 0):
        for pKey in pKeysTmp:
          pKeysRevised.append(pKey)
        break

    #logging.debug("RevisedPkeys : "+ str(pKeysRevised))

    for pKey in pKeysRevised:
      pcent = {}
      for activeTask in priorities[pKey]:
        completedShit = 0
        completedShit = db_conn.getRunFrames(activeTask["id"])
        allFrames = 0
        allFrames = db_conn.getAllFrames(activeTask["id"])
        if(allFrames):
          numAllFrames = len(allFrames)
        else:
          return(0)

        if(completedShit):
          numCompletedShit = len(completedShit)
        else:
          numCompletedShit = 0
        percent = (100 * numCompletedShit) / numAllFrames
        try:
          pcent[percent].append(activeTask)
        except:
          pcent[percent] = []
          pcent[percent].append(activeTask)
      pcentKeys = pcent.keys()
      pcentKeys.sort()
      for pcentKey in pcentKeys:
        tasks = pcent[pcentKey]
        for task in tasks:
          arrangedTasks.append(task)
    #logging.debug("arrangeTasks :"+ str(arrangedTasks))


    ##get the tasks arranged according to afterTasks shits
    #if(afterTasks):
      #for afterT in afterTasks.keys():
        #afterTid =

    return(arrangedTasks)
  else:
    return(0)

def assignFramesToHost(hostDetail,taskDets, taskFrames, batchId):
  eThreads = 0
  if(taskDets['threads'] == 0):
    if(hostDetail['eCpus'] == 0):
      eThreads = hostDetail['freeCpus']
    else:
      eThreads = hostDetail['freeCpus'] - (hostDetail['totalCpus'] - hostDetail['eCpus'])
  else:
    eThreads = taskDets['threads']

  framesStr = " or frames.frameId=".join(str(x) for x in taskFrames)
  db_conn.execute("UPDATE hostResource \
                  SET freeCpus=freeCpus-"+ str(eThreads) +" \
                  WHERE hostName=\""+ hostDetail['hostName'] +"\"")
  db_conn.execute("UPDATE frames \
                  SET hostName=\""+ hostDetail['hostName'] +"\" , \
                  status=if(frameId="+ str(min(taskFrames)) +","+ str(constants.framesAssigned) +","+ str(constants.framesBatched) +"), \
                  runCount=runCount+1 , \
                  batchId=\""+ str(batchId) +"\", \
                  fThreads="+ str(eThreads) +" \
                  WHERE (frames.frameId="+ framesStr +") \
                  AND frames.id="+ str(taskDets["id"]))
  #db_conn.execute("UPDATE hostResource \
                  #SET freeCpus=freeCpus+"+ str(eThreads) +" \
                  #WHERE hostName=\""+ hostDetail['hostName'] +"\"")
  db_conn.execute("UPDATE tasksLog SET lastHost=\""+ hostDetail['hostName'] +"\" WHERE tasksLog.id="+ str(taskDets['id']))


def initBatchId():
  try:
    bUid = str(uuid.uuid4())
    db_conn.execute("insert into batch (id) value ('"+ str(bUid) +"')")
  except:
    logging.error("batchId failed : "+ str(sys.exc_info()))
    raise
  return(str(bUid))


def insertToBatchId(batchId,frameNo):
  try:
    db_conn.execute("update batch set frange=CONCAT(frange,\" "+ str(frameNo) +" \") where id=\""+ str(batchId) +"\"")
    logging.debug("adding frame : "+ str(frameNo) +" to batchId : "+ str(batchId))
  except:
    logging.error("adding frame to batchId failed : "+ str(sys.exc_info()))
    return(0)
  return(1)




def scheduler():
  while(1):
    freeHosts = getFreeHosts()
    if(freeHosts):
      activeTasks = arrangedActiveTasks()
      if(activeTasks):
        afterTasks = {}
        for activeTask in activeTasks:
          if(activeTask["afterTasks"]):
            ats = activeTask["afterTasks"].split(",")
            for at in ats:
              if(int(at) != 0):
                for actsk in activeTasks:
                  if(int(at) == int(actsk['id'])):
                    try:
                      afterTasks[at.lstrip().rstrip()].append(activeTask)
                    except:
                      afterTasks[at.lstrip().rstrip()] = []
                      afterTasks[at.lstrip().rstrip()].append(activeTask)
                    break
        if(afterTasks):
          for ats in afterTasks.keys():
            for ts in afterTasks[ats]:
              if(ts == 0):
                continue
              try:
                activeTasks.remove(ts)
              except:
                pass

        for activeTask in activeTasks:
          taskFrames = db_conn.getUnassignedFrames(activeTask["id"])
          batchFlag = activeTask["batch"]
          minBatch = activeTask["minBatch"]
          maxBatch = activeTask["maxBatch"]

          if(taskFrames):
            totalFreeHosts = len(freeHosts)
            totalTaskFrames = len(taskFrames)
            assignedHost = getBestHost(activeTask)
            if(assignedHost):
              #Initialize batch id for the frame
              while(1):
                try:
                  batchId = initBatchId()
                  break
                except:
                  time.sleep(1)

              bestBatch = 1
              if(batchFlag == constants.batchActive):
                bestBatch = int(totalTaskFrames)/int(totalFreeHosts)
                
                if(bestBatch <= totalTaskFrames):
                  if(bestBatch < minBatch):
                    bestBatch = minBatch
                  elif(bestBatch > maxBatch):
                    bestBatch = maxBatch
                else:
                  bestBatch = totalTaskFrames
                
              taskFramesToAssign = []
              for bB in range(0,bestBatch):
                insertToBatchId(batchId,taskFrames[bB]['frameId'])
                taskFramesToAssign.append(taskFrames[bB]['frameId'])
                
                
              assignFramesToHost(assignedHost, activeTask, taskFramesToAssign, batchId)
              logging.debug("batchID : "+ str(batchId) +" : ASSIGNED to "+ assignedHost["hostName"] +" : "+ str(activeTask["id"]) +" : "+ str(taskFramesToAssign))
              break
          else:
            while(1):
              if(db_conn.resetFailedFrames(activeTask["id"])):
                break
              time.sleep(1)
    time.sleep(0.01)






if __name__=="__main__":
  scheduler()
