import MySQLdb
import MySQLdb.cursors
import time
import sys

class dbRbhus:
  """database querying class for rbhus"""
  def __init__(self):
    self.__conn = self._connRbhus()

  def __del__(self):
    self.__conn.close()
    print("Db connection closed")
  
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
        print("Db connected : "+ str(sys.exc_info()))
        return(con)
        break
      except:
        print("Db not connected : "+ str(sys.exc_info()))
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
          rows = cur.fetchall()
          cur.close()
          if(rows):
            return(rows)
          else:
            return(0)
        else:
          cur.close()
          return(1)
      except:
        print("Failed query : "+ str(query) +" : "+ str(sys.exc_info()))
        try:
          cur.close()
        except:
          pass
        if(str(sys.exc_info()).find("OperationalError") >= 0):
          self.__conn = self._connRbhus()
          continue
        else:
          raise
        
    
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
  
  
  