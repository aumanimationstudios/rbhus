#!/usr/bin/python
import MySQLdb
import MySQLdb.cursors
import time
import sys
import socket
import os
import tempfile


hostname = socket.gethostname()
tempDir = tempfile.gettempdir()

dbHostname = "blues2"
dbPort = "3306"
dbDatabase = "hosts"

try:
  dbHostname = os.environ['hosts_dbHostname']
except:
  pass
try:
  dbPort = os.environ['hosts_dbPort']
except:
  pass
try:
  dbDatabase = os.environ['hosts_dbDatabase']
except:
  pass



class dbHosts:
  """database querying class for rbhus"""
  def __init__(self):
    self.__myip = socket.gethostbyname(socket.gethostname())
    
    self.__conn = self._connHosts()

  def __del__(self):
    self.__conn.close()
  
  def _connDb(self,hostname,port,dbname):
    try:
      conn = MySQLdb.connect(host = hostname,port=port,db = dbname)
      conn.autocommit(1)
    except:
      raise
    return(conn)
    
  def _connHosts(self):
    while(1):
      try:
        con = self._connDb(hostname=dbHostname,port=int(dbPort),dbname=dbDatabase)
        return(con)
      except:
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
            pass
          cur.close()
          if(rows):
            return(rows)
          else:
            return(0)
        else:
          cur.close()
          return(1)
      except:
        if(str(sys.exc_info()).find("OperationalError") >= 0):
          try:
            cur.close()
          except:
            pass
          try:
            self._conn.close()
          except:
            pass
          self.__conn = self._connHosts()
          continue
        else:
          try:
            cur.close()
          except:
            pass
          raise
        
  def getCloneInfo(self):
    try:
      rows = self.execute("select * from clonedb where ip=\'"+ str(self.__myip) +"\' order by ip", dictionary=True)
    except:
      print("no clone info to get! : "+ str(sys.exc_info()))
      return(0)
    if(rows):
      return(rows[0])
    else:
      return(0)
  # returns an array of all the frames in the given batchId   
def test():
  dbR = dbHosts()
  diskin = dbR.getCloneInfo()
  if(diskin):
    print(diskin)
  else:
    print("fuck off")
  #if(diskin):
    #for disk in diskin:
      #print(disk)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
  
  
if __name__ == "__main__":
  test()
  
  
  
