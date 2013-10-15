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
import logging.handlers
import time
import signal
import setproctitle
import tempfile
import rbhus.dbRbhus as dbRbhus
import rbhus.constants as constants
import multiprocessing

LOG_FILENAME = '/var/log/rbhusQueen_frameCheck.log'
logging.BASIC_FORMAT = "%(asctime)s - %(funcName)s - %(levelname)s - %(message)s"
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)


tempDir = tempfile.gettempdir()
mainPidFile = tempDir + os.sep +"rbusServer.pids"

setproctitle.setproctitle("rQ_frameCheck")

def resetHungFrames(taskId,db_conn):
  try:
    db_conn.execute("UPDATE frames SET status="+ str(constants.framesUnassigned) +" WHERE (id="+ str(taskId) +") \
                    AND (status="+ str(constants.framesHung) +")")
  except:
    logging.error(str(sys.exc_info()))
    return(0)
  return(1)


def resetHungFramesProc():
  db_conn = dbRbhus.dbRbhus()
  setproctitle.setproctitle("rQ_resetHungFramesProc")
  while(1):
    tasks = db_conn.getActiveTasks()
    if(tasks):
      for task in tasks:
        resetHungFrames(task['id'],db_conn)
        #hFrames = db_conn.getHungFrames(task['id'])
        #if(hFrames):
          #for hF in hFrames:
            #resetHungFrames(hF['id'], hF['frameId'])
    time.sleep(1800)
    #keep this at 1800
    


    
def autoStopper():
  db_conn = dbRbhus.dbRbhus()
  setproctitle.setproctitle("rQ_autoStopper")
  while(1):
    tasks = db_conn.getActiveTasks()
    if(tasks):
      for task in tasks:
        if(task):
          allFrames = db_conn.getAllFrames(task['id'])
          framesThresh = db_conn.getFramesRerunThresh(task['id'])
          if(allFrames == 0):
            continue
          if(framesThresh == 0):
            continue
          totalFrames = len(allFrames)
          totalThresh = len(framesThresh)
          if(totalFrames == totalThresh):
            logging.debug("Auto stopping task : "+ str(task['id']))
            while(1):
              if(db_conn.setTaskStatus(task['id'],constants.taskAutoStopped)):
                break
              time.sleep(1)
          else:
            for x in framesThresh:
              db_conn.setFramesStatus(x['id'],x['frameId'],constants.framesAutoHold)
              logging.debug("Auto stopping frame  : "+ str(task['id']) +" "+ str(x['frameId']))
    else:
      time.sleep(1)
    time.sleep(0.1)


  
def setCompletedTasks():
  db_conn = dbRbhus.dbRbhus()
  setproctitle.setproctitle("rQ_setCompletedTasks")
  while(1):
    tasks = db_conn.getAllButStoppedTasks()
    
    if(tasks):
      for task in tasks:
        if(task):
          status = db_conn.checkTaskCompleted(task['id'])
          #logging.debug("active tasks wtf5 : "+ str(task['id']) +"\n\n")
        
          if(status >= 0):
            if(status ==  constants.taskDone):
              db_conn.setTaskDoneTime(task['id'])
            while(1):
              if(db_conn.setTaskStatus(task['id'],status)):
                logging.debug("task "+ str(task['id']) +" status changed to : "+ str(status))
                break
              time.sleep(0.1)
    else:
      time.sleep(1)
    time.sleep(0.1)
    
    
if __name__=="__main__":
  p = []
  setCompletedTasks_proc = multiprocessing.Process(target=setCompletedTasks)
  p.append(setCompletedTasks_proc)
  setCompletedTasks_proc.start()
  
  time.sleep(2)
  
  resetHungFramesProc_proc = multiprocessing.Process(target=resetHungFramesProc)
  p.append(resetHungFramesProc_proc)
  resetHungFramesProc_proc.start()
  
  time.sleep(2)
  
  autoStopper_proc = multiprocessing.Process(target=autoStopper)
  p.append(autoStopper_proc)
  autoStopper_proc.start()
  
  
  while(1):
    time.sleep(1)
    if(not p):
      break
    for i in range(0,len(p)):
      if(p[i].is_alive()):
        time.sleep(0.5)
      else: 
        logging.debug("MAIN Process dead : "+ str(p[i].pid))
        try:
          del(p[i])
        except:
          logging.debug("MAIN Process dead . cannot delete index")
        break
  