import MySQLdb
import MySQLdb.cursors
import time
import sys
import constants
import logging

LOG_FILENAME = logging.FileHandler('/var/log/rbhusDb_module.log')
modLogger = logging.getLogger("modLogger")
modLogger.setLevel(logging.ERROR)

BASIC_FORMAT = logging.Formatter("%(asctime)s - %(funcName)s - %(levelname)s - %(message)s")
modLogger.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
LOG_FILENAME.setFormatter(BASIC_FORMAT)
modLogger.addHandler(LOG_FILENAME)

class dbRbhus:
  """database querying class for rbhus"""
  def __init__(self):
    self.__conn = self._connRbhus()

  #def __del__(self):
    #self.__conn.close()
    #print("Db connection closed" +"\n")
  
  def _connDb(self,hostname,dbname):
    try:
      conn = MySQLdb.connect(host = hostname,db = dbname)
      conn.autocommit(1)
    except:
      raise
    return(conn)
    
  def _connRbhus(self):
    while(1):
      try:
        con = self._connDb("dbRbhus","rbhus")
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
          modLogger.error("faaaaaaaaack ..getActiveTasks missed!!!! ")
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
  
  def resetFailedFrames(self,taskId):
    try:  
      self.execute("UPDATE frames SET status="+ str(constants.framesUnassigned) +" WHERE id="+ str(taskId) +" \
                      AND (status="+ str(constants.framesFailed) +" \
                      OR status="+ str(constants.framesKilled) +")")
      return(1)
    except:
      modLogger.error(str(sys.exc_info()))
      return(0)
      
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
      return(1)
    except:
      return(0)
      
  def resetAssignedFrame(self,hostName,statusReset=0):
    try:
      self.execute("UPDATE frames SET status="+ str(statusReset) +" \
                      WHERE hostName=\""+ hostName +"\" AND ((status = "+ str(constants.framesPending) +") \
                      OR (status = "+ str(constants.framesAssigned) +") \
                      OR (status = "+ str(constants.framesRunning) +"))") 
      modLogger.debug("I CANT BELIVE I AM HERE for host : "+ str(hostName) +" : Resetting frame status to "+ constants.framesStatus[statusReset])
      return(1)
    except:
      modLogger.error(str(sys.exc_info()))
      return(0)
    
def test():
  dbR = dbRbhus()
  y = 0
  while(1):
    row = dbR.execute("select id,fileName,status from tasks where status=3", dictionary=True)
    if(row == 1):
      print "done"
      break
      
    if(not row):
      print "quit"
      print row
      break
    for x in row:
      print str(y)+ ":"+ str(x)
      y = y+1
    #time.sleep(1)
  
  
if __name__ == "__main__":
  test()
  
  
  