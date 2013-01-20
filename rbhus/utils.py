import sys
import os
import MySQLdb
progPath =  sys.argv[0].split(os.sep)
if(len(progPath) > 1):
  pwd = os.sep.join(progPath[0:-1])
  cwd = os.path.abspath(pwd)
else:
  cwd = os.path.abspath(os.getcwd())

sys.path.append(cwd.rstrip(os.sep) + os.sep)
import dbRbhus



def getHostGroups():
  dbconn = dbRbhus.dbRbhus()
  try:
    rows = dbconn.execute("select groups from hostInfo group by groups", dictionary=True)
  except:
    print("Error connecting to db 1")
    return(0)
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
      
def getFileTypes():
  dbconn = dbRbhus.dbRbhus()
  try:
    rows = dbconn.execute("select * from fileType", dictionary=True)
  except:
    print("Error connecting to db 2")
    return(0)
  retRows = []  
  if(rows):
    for row in rows:
      retRows.append(row['fileType'])
    return(retRows)
  else:
    return(0)
    
def getRenderers():
  dbconn = dbRbhus.dbRbhus()
  try:
    rows = dbconn.execute("select * from renderer", dictionary=True)
  except:
    print("Error connecting to db 2")
    return(0)
  retRows = {}  
  if(rows):
    for row in rows:
      try:
        retRows[row['fileType']].append(row['renderer'])
      except:
        retRows[row['fileType']] = []
        retRows[row['fileType']].append(row['renderer'])
    return(retRows)
  else:
    return(0)
    
def getOsTypes():
  dbconn = dbRbhus.dbRbhus()
  try:
    rows = dbconn.execute("select os from hostInfo group by os", dictionary=True)
  except:
    print("Error connecting to db 1")
    return(0)
  otr = {}
  retRows = []
  if(rows):
    for row in rows:
      tmpRow = row['os'].split(",")
      for tr in tmpRow:
        otr[tr.rstrip().lstrip()] = 1
    for gt in otr.keys():
      retRows.append(gt)
    return(retRows)
  else:
    return(0)

class tasks(object):
  def __init__(self, tId = 0):
    self.db_conn = dbRbhus.dbRbhus()
    self.taskFields = self._getTaskFields()
    self.username = None
    try:
      self.username = os.environ['rbhus_acl_user'].rstrip().lstrip()
    except:
      pass
    
    self.taskId = tId
    if(tId):
      self.taskDetails = self._getTaskDetails(tId)
      
  
  def _getTaskFields(self):
    try:
      rows = self.db_conn.execute("desc tasks",dictionary=True)
      taskFieldss = {}
      for row in rows:
        taskFieldss[row['Field']] = row['Default']
      return(taskFieldss)
    except:
      return(0)
  
  def _getTaskDetails(self,tid):
    try:
      rows = self.db_conn.execute("select * from tasks where id='"+ str(tid) +"'",dictionary=True)
      if(rows):
        return(rows[-1])
      else:
        return(0)
    except:
      return(0)
      
  def submit(self,fieldDict):
    self.validFields = {}
    self.invalidFields = {}
    fieldDict['submitTime'] = str(MySQLdb.Timestamp.now())
    if(self.username):
      fieldDict['user'] = self.username
    else:
      return(0)
    for x in fieldDict.keys():
      if(self.taskFields.has_key(x)):
        self.validFields[x] = fieldDict[x]
      else:
        self.invalidFields[x] = fieldDict[x]
    self.validFields_keys = [x for x in self.validFields.keys()]
    self.validFields_values = ["'"+ str(self.validFields[x]) +"'" for x in self.validFields_keys]
    self.insertStatement = "insert into tasks ("+ ", ".join(self.validFields_keys) +") values ("+ ", ".join(self.validFields_values) +")"
    try:
      self.db_conn.execute(self.insertStatement)
      rows = self.db_conn.execute("select last_insert_id()", dictionary = True)
      self.taskId =  rows[0]['last_insert_id()']
      self.taskDetails = self._getTaskDetails(self.taskId)
      return(self.taskId)
    except:
      self.taskId = 0
      raise
  
  def edit(self,fieldDict):
    self.validFields = {}
    self.invalidFields = {}
    if(self.username):
      fieldDict['user'] = self.username
    else:
      return(0)
    for x in fieldDict.keys():
      if(self.taskFields.has_key(x)):
        self.validFields[x] = fieldDict[x]
      else:
        self.invalidFields[x] = fieldDict[x]
        
    if(self.validFields):
      for validF in  self.validFields.keys():
        try:
          taskAclList = os.environ['rbhus_acl_tasks'].rstrip().lstrip().split()
          try:
            taskAclList.index('all')
            continue
          except:
            pass
          for taskFAcl in taskAclList:
            print("removing "+ str(taskFAcl) +" from editing since you are not qualified to use it :D .. ")
            try:
              del(self.validFields[taskFAcl])
            except:
              print(str(sys.exc_info()))
        except:
          print(str(sys.exc_info()))
      if(self.taskId):
        for x in self.validFields.keys():
          try:
            self.db_conn.execute("update tasks set "+ str(x) +"='"+ str(self.validFields[x]) +"' where id='"+ str(self.taskId) +"'")
          except:
            raise
        self.taskDetails = self._getTaskDetails(self.taskId)
        
        
#if __name__ == "__main__":
  #b = {}
  #b['fileName'] = "/tmp/fff.ff"
  #b['batch'] = "1"
  #b['minBatch'] = "1"
  #b['maxBatch'] = "3"
  #c = 799
  #a = tasks()
  #a.submit(b)
  #print(str(a.taskDetails))