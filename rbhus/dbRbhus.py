import MySQLdb
import MySQLdb.cursors
import time
import sys
import constants

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
        print("Db connected" +"\n")
        return(con)
      except:
        print("Db not connected : "+ str(sys.exc_info()) +"\n")
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
            print("fetching failed : "+ str(sys.exc_info()) +"\n")
          
          cur.close()
          if(rows):
            return(rows)
          else:
            return(0)
        else:
          cur.close()
          return(1)
      except:
        print("Failed query : "+ str(query) +" : "+ str(sys.exc_info()) +"\n")
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
          print("faaaaaaaaack ..getActiveTasks missed!!!! ")
          return(0)
    except:
      logging.error(str(sys.exc_info()))
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
          print("faaaaaaaaack ..getPotentHosts missed!!!!")
          return(0)
    except:
      logging.error(str(sys.exc_info()))    
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
      logging.error(str(sys.exc_info()))
      return(0)
    return(rows)
  
  def resetFailedFrames(self,taskId):
    try:  
      self.execute("UPDATE frames SET status="+ str(constants.framesUnassigned) +" WHERE id="+ str(taskId) +" \
                      AND (status="+ str(constants.framesFailed) +" \
                      OR status="+ str(constants.framesKilled) +")")
      return(1)
    except:
      logging.error(str(sys.exc_info()))
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
      logging.error(str(sys.exc_info()))
      return(0)
    return(rows)
    
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
  
  
  