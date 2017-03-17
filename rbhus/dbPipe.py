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
os.environ["QT_GRAPHICSSYSTEM"] = "native"

hostname = socket.gethostname()
tempDir = tempfile.gettempdir()

dbHostname = "blues2"
dbPort = "3306"
dbDatabase = "rbhusPipe"
dbLogDatabase = "rbhusPipeLog"

try:
  dbHostname = os.environ['rbhusPipe_dbHostname']
except:
  pass
try:
  dbPort = os.environ['rbhusPipe_dbPort']
except:
  pass
try:
  dbDatabase = os.environ['rbhusPipe_dbDatabase']
except:
  pass
try:
  dbLogDatabase = os.environ['rbhusPipe_dbLogDatabase']
except:
  pass
username = "nobody"
try:
  if(sys.platform.find("win") >= 0):
    username = os.environ['USERNAME']
  if(sys.platform.find("linux") >= 0):
    username = os.environ['USER']
except:
  pass

LOG_FILENAME = logging.FileHandler(tempDir + os.sep +"rbhusPipe_dbPipe_module_"+ username +"_"+ str(hostname) +".log")

#LOG_FILENAME = logging.FileHandler('/var/log/rbhusDb_module.log')
modPipeLogger = logging.getLogger("modPipeLogger")
modPipeLogger.setLevel(logging.ERROR)


#ROTATE_FILENAME = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=104857600, backupCount=3)
BASIC_FORMAT = logging.Formatter("%(asctime)s - %(funcName)s - %(levelname)s - %(message)s")
LOG_FILENAME.setFormatter(BASIC_FORMAT)
modPipeLogger.addHandler(LOG_FILENAME)
#modPipeLogger.addHandler(ROTATE_FILENAME)

class dbPipe:
  """database querying class for rbhus"""
  # def __init__(self):
  #   self.__conn = self._connRbhus()

  def __del__(self):
    try:
      self.__conn.close()
    except:
      modPipeLogger.error(str(sys.exc_info()))
    modPipeLogger.debug("Db connection closed" +"\n")
  
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
        modPipeLogger.debug("Db connected")
        return(con)
      except:
        modPipeLogger.error("Db not connected : "+ str(sys.exc_info()))
      time.sleep(1)
      
       
  def execute(self,query,dictionary=False):
    while(1):
      try:
        self.__conn = self._connRbhus()
        if(dictionary):
          cur = self.__conn.cursor(MySQLdb.cursors.DictCursor)
        else:
          cur = self.__conn.cursor()
        cur.execute(query)
        modPipeLogger.debug(query)
        if(dictionary):
          try:
            rows = cur.fetchall()
          except:
            modPipeLogger.error("fetching failed : "+ str(sys.exc_info()))
          
          cur.close()
          try:
            self._conn.close()
          except:
            pass
          if(rows):
            return(rows)
          else:
            return(0)
        else:
          cur.close()
          try:
            self._conn.close()
          except:
            pass
          return(1)
      except:
        modPipeLogger.error("Failed query : "+ str(query) +" : "+ str(sys.exc_info()))
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
          # self.__conn = self._connRbhus()
          continue
        else:
          try:
            cur.close()
          except:
            pass
          try:
            self._conn.close()
          except:
            pass
          raise