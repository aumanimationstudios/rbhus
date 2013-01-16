import MySQLdb
import MySQLdb.cursors
import time
import sys
import constants
import logging
import socket
import os
import tempfile


hostname = socket.gethostname()
tempDir = tempfile.gettempdir()

if(sys.platform.find("linux") >=0):
  LOG_FILENAME = logging.FileHandler('/var/log/rbhusDb_module.log')
elif(sys.platform.find("win") >=0):
  LOG_FILENAME = logging.FileHandler(tempDir + os.sep +"rbhusDb_module"+ str(hostname) +".log")


#LOG_FILENAME = logging.FileHandler('/var/log/rbhusDb_module.log')
modLogger = logging.getLogger("modLogger")
modLogger.setLevel(logging.ERROR)

BASIC_FORMAT = logging.Formatter("%(asctime)s - %(funcName)s - %(levelname)s - %(message)s")
LOG_FILENAME.setFormatter(BASIC_FORMAT)
modLogger.addHandler(LOG_FILENAME)

class dbRbhus:
  """database querying class for rbhus"""
  def __init__(self):
    self.__conn = self._connRbhus()

  def __del__(self):
    self.__conn.close()
    modLogger.debug("Db connection closed" +"\n")
  
  def _connDb(self,hostname,port,dbname):
    try:
      conn = MySQLdb.connect(host = hostname,port=port,db = dbname)
      conn.autocommit(1)
    except:
      raise
    return(conn)
    
  def _connRbhus(self):
    while(1):
      try:
        con = self._connDb(hostname="blues2",port=3306,dbname="rbhus")
        modLogger.debug("Db connected")
        return(con)
      except:
        modLogger.error("Db not connected : "+ str(sys.exc_info()))
      time.sleep(1)
      
       
  def execute(self,query,dictionary=False):
    while(1):
      try:
        if(dictionary):
          cur = self.__conn.cursor(MySQLdb.cursors.DictCursor)
        else:
          cur = self.__conn.cursor()
        cur.execute(query)
        
        if(dictionary):
          try:
            rows = cur.fetchall()
          except:
            modLogger.error("fetching failed : "+ str(sys.exc_info()))
          
          cur.close()
          if(rows):
            return(rows)
          else:
            return(0)
        else:
          cur.close()
          return(1)
      except:
        modLogger.error("Failed query : "+ str(query) +" : "+ str(sys.exc_info()))
        if(str(sys.exc_info()).find("OperationalError") >= 0):
          try:
            cur.close()
          except:
            pass
          try:
            self._conn.close()
          except:
            pass
          self.__conn = self._connRbhus()
          continue
        else:
          try:
            cur.close()
          except:
            pass
          raise
        
  # returns an array of all the frames in the given batchId   
  def getBatchedFrames(self,batchId):
    try:
      rows = self.execute("select frange from batch where id=\""+ str(batchId) +"\"",dictionary=True)
      frange = rows[0][rows[0].keys()[-1]].split()
      try:
        frange.remove("default")
      except:
        pass
    except:
      modLogger.error("getting batched frames : "+ str(sys.exc_info()))
      return(None)
    return(frange)
    
  def getBatchId(self, taskId, frameId):
    try:
      rows = self.execute("select batchId from frames where id=\""+ str(taskId) +"\" and frameId=\""+ str(frameId) +"\"",dictionary=True)
      batchId = str(rows[0][rows[0].keys()[-1]])
      try:
        batchId.remove("default")
      except:
        pass
    except:
      modLogger.error("getting batchId : "+ str(sys.exc_info()))
      return(None)
    return(batchId)

  # returns an array of all the frames in the given batchId   
  def delBatchId(self,batchId):
    try:
      self.execute("delete from batch where id=\""+ str(batchId) +"\"")
      return(1)
    except:
      modLogger.error("deleting batchId : "+ str(batchId))
      return(0)

  def getActiveTasks(self):
    try:
      rows = self.execute("SELECT tasks.*, tasksLog.lastHost FROM tasks, tasksLog \
                      WHERE tasks.status=\'"+ str(constants.taskActive) +"\' \
                      AND tasks.id=tasksLog.id \
                      AND tasks.afterTime<=NOW() \
                      ORDER BY tasks.priority DESC", dictionary=True)
    
      #THE BELOW LOGIC IS NONSENSE . this is a temp fix untill i find the right source of the problem
      if(rows):
        if(not 'priority' in rows[0].keys()):
          modLogger.error("faaaaaaaaack ..getActiveTasks missed!!!!  : "+ str(rows))
          return(0)
    except:
      modLogger.error(str(sys.exc_info()))
      return(0)
    return(rows)
    
    
  def getAllTasks(self):
    try:
      rows = self.execute("SELECT tasks.*, tasksLog.lastHost FROM tasks, tasksLog \
                      WHERE tasks.id=tasksLog.id \
                      ORDER BY tasks.priority DESC", dictionary=True)
    
      #THE BELOW LOGIC IS NONSENSE . this is a temp fix untill i find the right source of the problem
      if(rows):
        if(not 'priority' in rows[0].keys()):
          modLogger.error("faaaaaaaaack ..getActiveTasks missed!!!!  : "+ str(rows))
          return(0)
    except:
      modLogger.error(str(sys.exc_info()))
      return(0)
    return(rows)
    
  def getAllButStoppedTasks(self):
    try:
      rows = self.execute("SELECT tasks.*, tasksLog.lastHost FROM tasks, tasksLog \
                      WHERE (tasks.id = tasksLog.id) \
                      AND ((tasks.status != "+ str(constants.taskStopped) +") or (tasks.status != "+ str(constants.taskAutoStopped) +")) \
                      ORDER BY tasks.priority DESC", dictionary=True)
    
      #THE BELOW LOGIC IS NONSENSE . this is a temp fix untill i find the right source of the problem
      if(rows):
        if(not 'priority' in rows[0].keys()):
          modLogger.error("faaaaaaaaack ..getActiveTasks missed!!!!  : "+ str(rows))
          return(0)
    except:
      modLogger.error(str(sys.exc_info()))
      return(0)
    return(rows)
    
  def getPotentHosts(self):
    try:
      rows = self.execute("SELECT hostInfo.hostName, \
                            hostInfo.totalCpus, \
                            hostResource.freeCpus, \
                            hostInfo.totalRam, \
                            hostResource.freeRam, \
                            hostInfo.totalSwap, \
                            hostResource.freeSwap, \
                            hostResource.load1, \
                            hostResource.load5, \
                            hostResource.load10, \
                            hostEffectiveResource.eCpus, \
                            hostInfo.weight, \
                            hostInfo.groups, \
                            hostInfo.os \
                      FROM hostResource, hostInfo, hostAlive, hostEffectiveResource \
                      WHERE hostInfo.status = hostAlive.status \
                      AND hostAlive.status="+ str(constants.hostAliveAlive) +" \
                      AND hostInfo.hostName = hostResource.hostName \
                      AND hostResource.hostName = hostAlive.hostName \
                      AND hostAlive.hostName = hostEffectiveResource.hostName \
                      ORDER BY hostInfo.weight DESC", dictionary=True)
      if(rows):
        if(not 'eCpus' in rows[0].keys()):
          modLogger.error("faaaaaaaaack ..getPotentHosts missed!!!!")
          return(0)
    except:
      modLogger.error(str(sys.exc_info()))    
      return(0)
    return(rows)
    
  def getUnassignedFrames(self,taskId):
    try:
      rows = self.execute("SELECT frames.frameId, tasks.* FROM frames, tasks \
                       WHERE tasks.id="+ str(taskId) +" \
                       AND frames.id= tasks.id \
                       AND frames.status="+ str(constants.framesUnassigned) +" \
                       AND (tasks.rerunThresh>frames.runCount OR tasks.rerunThresh=0) \
                       ORDER BY frames.frameId", dictionary=True)
    except:
      modLogger.error(str(sys.exc_info()))
      return(0)
    return(rows)
    
    
  # Get the total number of unassigned frames  
  def getTotalUnAsFrames(self):
    try:
      rows = self.execute("select count(*) from frames where status=0 and frames.id=tasks.id and tasks.status="+ str(constants.taskActive), dictionary=True)
    except:
      modLogger.error(str(sys.exc_info()))
      return(0)
    return(int(rows[0][rows[0].keys()[-1]]))
    
  
  def resetFailedFrames(self,taskId):
    try:  
      self.execute("UPDATE frames SET status="+ str(constants.framesUnassigned) +" WHERE id="+ str(taskId) +" \
                      AND (status="+ str(constants.framesFailed) +" \
                      OR status="+ str(constants.framesKilled) +")")
    except:
      modLogger.error(str(sys.exc_info()))
      return(0)
    return(1)
      
      
  def getRunFrames(self,taskId):
    try:
      rows = self.execute("SELECT frames.frameId, tasks.* FROM frames, tasks \
                      WHERE tasks.id="+ str(taskId) +" \
                      AND tasks.id=frames.id \
                      AND tasks.status="+ str(constants.taskActive) +" \
                      AND frames.status !="+ str(constants.framesUnassigned) +" \
                      ORDER BY frames.frameId", dictionary=True)
    except:
      modLogger.error(str(sys.exc_info()))
      return(0)
    return(rows)
    
  def getAllFrames(self,taskId):
    try:
      rows = self.execute("SELECT frames.frameId, tasks.* FROM frames, tasks \
                      WHERE tasks.id=\'"+ str(taskId) +"\' \
                      AND tasks.id=frames.id \
                      ORDER BY frames.frameId", dictionary=True)
    except:
      modLogger.error(str(sys.exc_info()))
      return(0)
    return(rows)
    
  def getHostInfo(self,status):
    try:
      if(status == "ALL"):
        rows = self.execute("SELECT * FROM hostInfo", dictionary=True)
      elif(status == "ENABLED"):
        rows = self.execute("SELECT * FROM hostInfo WHERE status="+ str(constants.hostInfoEnable), dictionary=True)
      else:
        rows = self.execute("SELECT * FROM hostInfo WHERE status="+ str(constants.hostInfoDisable), dictionary=True)
    except:
      modLogger.error(str(sys.exc_info()))
      return(0)
    return(rows)
    
    
  def setHostAliveStatus(self,hostName,status):
    try:
      self.execute("UPDATE hostAlive SET status='"+ str(status) +"' WHERE hostName=\""+ hostName +"\"")
    except:
      return(0)
    return(1)
      
      
  def resetAssignedFrame(self,hostName,statusReset=0):
    try:
      self.execute("UPDATE frames SET status="+ str(statusReset) +" \
                      WHERE hostName=\""+ hostName +"\" AND ((status = "+ str(constants.framesPending) +") \
                      OR (status = "+ str(constants.framesAssigned) +") \
                      OR (status = "+ str(constants.framesRunning) +"))") 
      modLogger.debug("I CANT BELIVE I AM HERE for host : "+ str(hostName) +" : Resetting frame status to "+ constants.framesStatus[statusReset])
    except:
      modLogger.error(str(sys.exc_info()))
      return(0)
    return(1)
  
  
  def getHungFrames(self,taskId):
    try:
      rows = self.execute("SELECT frames.frameId, tasks.* FROM frames, tasks \
                      WHERE tasks.id="+ str(taskId) +" \
                      AND frames.id= tasks.id \
                      AND frames.status="+ str(constants.framesHung) +" \
                      AND (tasks.rerunThresh>frames.runCount OR tasks.rerunThresh=0) \
                      ORDER BY frames.frameId", dictionary=True)
    except:
      logging.error(str(sys.exc_info()))
      return(0)
    return(rows)
    
  def getFramesRerunThresh(self,taskId):
    try:
      rows = self.execute("SELECT frames.* FROM frames, tasks \
                      WHERE tasks.id=\'"+ str(taskId) +"\' \
                      AND tasks.id=frames.id \
                      AND frames.runCount>=tasks.rerunThresh \
                      AND frames.status!="+ str(constants.framesDone) +" \
                      AND frames.status!="+ str(constants.framesPending) +" \
                      AND frames.status!="+ str(constants.framesRunning) +" \
                      AND frames.status!="+ str(constants.framesAssigned) +" \
                      ORDER BY frames.frameId", dictionary=True)
    except:
      logging.error(str(sys.exc_info()))
      return(0)
    return(rows)
    
  def setTaskStatus(self,taskId,status):
    try:
      self.execute("UPDATE tasks SET status="+ str(status) +" WHERE id="+ str(taskId))
      logging.debug("Updated task:"+ str(taskId) +" status to "+ str(status))
    except:
      logging.error(str(sys.exc_info()))
      return(0)
    return(1)
    
  def getTaskStatus(self,taskId):
    try:
      status = self.execute("select status from tasks where id="+ str(taskId), dictionary=True)
      return(status[0]['status'])
    except:
      logging.error(str(sys.exc_info()))
      return(-1)
    return(-2)
    
    
  #Return value is the status of the task that needs to be set
  def checkTaskCompleted(self,taskId):
    try:
      f_status = {}
      taskStatus = self.getTaskStatus(taskId)
      for k in constants.framesStatus:
        f_status[constants.framesStatus[k]] = 0
      if((taskStatus == constants.taskWaiting) or (taskStatus == constants.taskPending) or (taskStatus == constants.taskStopped) or (taskStatus == constants.taskAutoStopped)):
        return(-1)
      
      rowss_ = self.execute("SELECT * FROM frames WHERE frames.id="+ str(taskId), dictionary=True)
      if(rowss_):
        for x in rowss_:
          f_status[constants.framesStatus[x['status']]] = f_status[constants.framesStatus[x['status']]] + 1
      if(f_status):
        if((f_status[constants.framesStatus[constants.framesHold]] + f_status[constants.framesStatus[constants.framesAutoHold]]) == len(rowss_)):
          return(constants.taskAutoStopped)
        elif(f_status[constants.framesStatus[constants.framesDone]] == len(rowss_)):
          return(constants.taskDone)
        else:
          return(constants.taskActive)
          
        #for k in f_status:
          #if(f_status[k] == len(rowss_)):
            #if(k == constants.framesStatus[constants.framesDone]):
              #return(constants.taskDone)
            #elif(k == constants.framesStatus[constants.framesHold]):
              #return(constants.taskStopped)
            #elif(k == constants.framesStatus[constants.framesAutoHold]):
              #return(constants.taskAutoStopped)
            #elif(k == constants.framesStatus[constants.framesUnassigned]):
              #return(constants.taskActive)
          #else:
            #return(constants.taskActive)
        
      return(-2)
    except:
      logging.error(str(sys.exc_info()))
      return(-3)

      
  def setFramesStatus(self,taskId, frameId, status):
    try:
      self.execute("UPDATE frames SET status="+ str(status) +" \
                      WHERE frameId="+ str(frameId) +" \
                      AND id="+ str(taskId))
    except:
      return(0)
    return(1)
    
def test():
  dbR = dbRbhus()
  status = dbR.getTaskStatus(sys.argv[1])
  print(str(status))
    #time.sleep(1)
  
  
if __name__ == "__main__":
  test()
  
  
  
