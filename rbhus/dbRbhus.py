import MySQLdb
import MySQLdb.cursors
import time
import sys
import constants
import logging
import logging.handlers
import socket
import os
import tempfile


hostname = socket.gethostname()
tempDir = os.path.abspath(tempfile.gettempdir())

dbHostname = "blues2"
dbPort = "3306"
dbDatabase = "rbhus"
dbLogDatabase = "rbhusLog"

try:
  dbHostname = os.environ['rbhus_dbHostname']
except:
  pass
try:
  dbPort = os.environ['rbhus_dbPort']
except:
  pass
try:
  dbDatabase = os.environ['rbhus_dbDatabase']
except:
  pass
try:
  dbLogDatabase = os.environ['rbhus_dbLogDatabase']
except:
  pass

LOG_FILENAME = logging.FileHandler(tempDir + os.sep +"rbhusDb_module"+ str(hostname) +".log")
  #LOG_FILENAME = logging.FileHandler('z:/pythonTestWindoze.DONOTDELETE/clientLogs/rbhusDb_'+ hostname +'.log')

#LOG_FILENAME = logging.FileHandler('/var/log/rbhusDb_module.log')
modLogger = logging.getLogger("modLogger")
modLogger.setLevel(logging.ERROR)


#ROTATE_FILENAME = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=104857600, backupCount=3)
BASIC_FORMAT = logging.Formatter("%(asctime)s - %(funcName)s - %(levelname)s - %(message)s")
LOG_FILENAME.setFormatter(BASIC_FORMAT)
modLogger.addHandler(LOG_FILENAME)
#modLogger.addHandler(ROTATE_FILENAME)

class dbRbhusLog:
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
        con = self._connDb(hostname=dbHostname,port=int(dbPort),dbname=dbLogDatabase)
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
          time.sleep(1)
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
        con = self._connDb(hostname=dbHostname,port=int(dbPort),dbname=dbDatabase)
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
          time.sleep(1)
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
      self.execute("delete from batch where id='"+ str(batchId) +"'")
      modLogger.error("deleted batchId : "+ str(batchId))
      return(1)
    except:
      modLogger.error("deleting failed batchId : "+ str(batchId))
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
    
    
  def setTaskDoneTime(self,taskId):
    try:
      self.execute("UPDATE tasks SET doneTime=IF(doneTime=\'0000-00-00 00:00:00\',NOW(),doneTime) \
                      WHERE id="+ str(taskId))
    except:
      modLogger.debug(str(sys.exc_info()))
      return(0)
    return(1)


  def resetTaskDoneTime(self,taskId):
    try:
      self.execute("UPDATE tasks SET doneTime=\'0000-00-00 00:00:00\' \
                      WHERE id="+ str(taskId))
    except:
      modLogger.debug(str(sys.exc_info()))
      return(0)
    return(1)
  
  
  
  def delTask(self,taskId,auth=False):
    if(auth):
      try:
        username = os.environ['rbhus_acl_user'].rstrip().lstrip()
      except:
        pass
      try:
        userProjIds = os.environ['rbhus_acl_projIds'].split()
      except:
        userProjIds = ['0']
        pass
    rowss_ = self.execute("SELECT * FROM frames WHERE frames.id="+ str(taskId), dictionary=True)
    f_status = {}
    if(rowss_):
      for x in rowss_:
        try:
          f_status[constants.framesStatus[x['status']]] = f_status[constants.framesStatus[x['status']]] + 1
        except:
          f_status[constants.framesStatus[x['status']]] = 1
    if(f_status.has_key(constants.framesStatus[constants.framesRunning])):
      print("cannot delete task : "+ str(taskId) +" : running frames detected!")
      return(0)
    else:
      try:
        if(not auth):
          self.execute("delete from tasks where (id="+ str(taskId) +") and ((status != "+ str(constants.taskWaiting) +") and (status != "+ str(constants.taskPending) +") and (status != "+ str(constants.taskActive) +"))")
        else:
          self.execute("delete from tasks where (id="+ str(taskId) +") and ((status != "+ str(constants.taskWaiting) +") and (status != "+ str(constants.taskPending) +") and (status != "+ str(constants.taskActive) +")) and ((user='"+ str(username) +"') or (projId in ('"+ ",".join(userProjIds) +"')))")
        return(1)
      except:
        print("1 :Error connecting to db :"+ str(sys.exc_info()))
        return(0)    
    
  
  def holdTask(self,taskId,auth=False):
    if(auth):
      try:
        username = os.environ['rbhus_acl_user'].rstrip().lstrip()
      except:
        pass
      try:
        userProjIds = os.environ['rbhus_acl_projIds'].split()
      except:
        userProjIds = ['0']
        pass
    try:
      if(not auth):
        self.execute("update tasks set status = "+ str(constants.taskStopped) +" where (id="+ str(taskId) +") and ((status != "+ str(constants.taskWaiting) +") and (status != "+ str(constants.taskPending) +"))")
      else:
        self.execute("update tasks set status = "+ str(constants.taskStopped) +" where (id="+ str(taskId) +") and ((status != "+ str(constants.taskWaiting) +") and (status != "+ str(constants.taskPending) +")) and ((user='"+ str(username) +"') or (projId in ('"+ ",".join(userProjIds) +"')))")
      return(1)
    except:
      print(str(sys.exc_info()))
      return(0)
      
      
  def rerunTask(self,taskId,auth=False):
    if(auth):
      try:
        username = os.environ['rbhus_acl_user'].rstrip().lstrip()
      except:
        pass
      try:
        userProjIds = os.environ['rbhus_acl_projIds'].split()
      except:
        userProjIds = ['0']
        pass
    try:
      if(not auth):
        self.execute("update tasks set status = "+ str(constants.taskWaiting) +" where (id="+ str(taskId) +")")
      else:
        self.execute("update tasks set status = "+ str(constants.taskWaiting) +" where (id="+ str(taskId) +")  and ((user='"+ str(username) +"') or (projId in ('"+ ",".join(userProjIds) +"')))")
      return(1)
    except:
      print("1 :Error connecting to db :"+ str(sys.exc_info()))
      return(0)
      
  

  def getProjectId(self,projectName):
    try:
      rows = self.execute("SELECT * FROM proj WHERE projName="+ str(projectName))
      if(rows):
        return(rows[0]['id'])
      else:
        return(0)
    except:
      modLogger.error(str(sys.exc_info()))
      return(0)
  
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
    
  def getAllActiveTasks(self):
    try:
      rows = self.execute("SELECT tasks.*, tasksLog.lastHost FROM tasks, tasksLog \
                      WHERE (tasks.id = tasksLog.id) \
                      AND (tasks.status="+ str(constants.taskActive) +") \
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
                            hostInfo.ip, \
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
                       WHERE tasks.id="+ str(int(taskId)) +" \
                       AND frames.id= tasks.id \
                       AND frames.status="+ str(constants.framesUnassigned) +" \
                       AND (tasks.rerunThresh>frames.runCount OR tasks.rerunThresh=0) \
                       ORDER BY frames.frameId", dictionary=True)
    except:
      modLogger.error(str(sys.exc_info()))
      return(0)
    return(rows)
  
  
  def getUnassignedFramesCount(self,taskId):
    try:
      rows = self.execute("SELECT count(*) FROM frames \
                       WHERE frames.id="+ str(int(taskId)) +" \
                       AND frames.status="+ str(constants.framesUnassigned), dictionary=True)
    except:
      modLogger.error(str(sys.exc_info()))
      return(0)
    return(rows)
  
  
  def stopFrames(self,hostIp, tId, fId):
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tryCount = 5 
    while(tryCount):
      time.sleep(1)
      try:
        clientSocket.connect((str(hostIp),6660))
        clientSocket.settimeout(2)
        clientSocket.send("MURDER:"+ str(tId).lstrip("0") +"%"+ str(fId).lstrip("0"))
        clientSocket.close()
        break
      except:
        print(str(sys.exc_info()))
        tryCount = tryCount - 1
        clientSocket.close()
        return(1)
    return(0)  
    
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
                      AND frames.status !="+ str(constants.framesUnassigned) +" \
                      ORDER BY frames.frameId", dictionary=True)
    except:
      modLogger.error(str(sys.exc_info()))
      return(0)
    return(rows)
    
  def getClientPrefs(self):
    try:
      rows = self.execute("SELECT * FROM clientPref", dictionary=True)
      if(not isinstance(rows,int)):
        return(rows[0])
      else:
        return(0)
    except:
      modLogger.error(str(sys.exc_info()))
      return(0)
    
    
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
    
    
  
  
  def getFrameInfo(self,taskid, frameid):
    try:
      rows = self.execute("SELECT * FROM frames \
                      WHERE frames.id="+ str(taskid) +" \
                      AND frames.frameId="+ str(frameid), dictionary=True)
    except:
      modLogger.debug(str(sys.exc_info()))
      rows = 0
    return(rows[0])
  
    
  def getHostInfo(self,status="ALL",hostName=None):
    hostnameSqlWhere = ""
    hostnameSqlAnd = ""
    if(hostName):
      hostnameSqlWhere = " where hostName='"+ str(hostName) +"'"
      hostnameSqlAnd = " and hostName='"+ str(hostName) +"'"
    try:
      if(status == "ALL"):
        rows = self.execute("SELECT * FROM hostInfo"+ str(hostnameSqlWhere), dictionary=True)
      elif(status == "ENABLED"):
        rows = self.execute("SELECT * FROM hostInfo WHERE status="+ str(constants.hostInfoEnable) + str(hostnameSqlAnd), dictionary=True)
      else:
        rows = self.execute("SELECT * FROM hostInfo WHERE status="+ str(constants.hostInfoDisable) + str(hostnameSqlAnd), dictionary=True)
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
    
    
  def getRunningFrames(self):
    try:
      rows = self.execute("select * from frames where status = "+ str(constants.framesRunning), dictionary=True)
    except:
      logging.error(str(sys.exc_info()))
      return(0)
    return(rows)
    
    
  def setTaskDone(self,taskId):
    try:
      self.execute("update tasks set status="+ str(constants.taskDone) +",doneTime=IF(doneTime='0000-00-00 00:00:00',NOW(),doneTime) where \
                    id="+ str(taskId) +" and status!="+ str(constants.taskDone) +" and \
                    (select count(*) from frames where frames.id="+ str(taskId) +" and frames.status="+ str(constants.framesDone) +")=(select count(*) from frames where frames.id="+ str(taskId) +")")
      return(1)
    except:
      logging.error(str(sys.exc_info()))
      return(0)
  
  
  
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
    
  
  def getTaskDetails(self,taskId):
    try:
      rows = self.execute("select * from tasks where id="+ str(taskId), dictionary=True)
    except:
      logging.error(str(sys.exc_info()))
      return(0)
    if(rows):
      return(rows[0])
    else:
      return(0)
    
    
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
      logging.error(str(taskId) +" : "+ str(sys.exc_info()))
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
  dbR.delTask(sys.argv[1])
  
    #time.sleep(1)
  
  
if __name__ == "__main__":
  test()
  
  
  
