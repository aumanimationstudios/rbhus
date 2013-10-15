import sys
import os
import socket
import MySQLdb
progPath =  sys.argv[0].split(os.sep)
if(len(progPath) > 1):
  pwd = os.sep.join(progPath[0:-1])
  cwd = os.path.abspath(pwd)
else:
  cwd = os.path.abspath(os.getcwd())

sys.path.append(cwd.rstrip(os.sep) + os.sep)
import dbRbhus
import constants



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
      
    aGroups = getHostGroupsActive()
    aGroups.sort(reverse=True)
    for x in aGroups:
      try:
        retRows.remove(x)
      except:
        pass
      retRows.insert(0,x)
    return(retRows)
  else:
    return(0)
    

def getHostGroupsActive():
  dbconn = dbRbhus.dbRbhus()
  retGroups = []
  try:
    rows = dbconn.execute("select gName from hostGroupsActive group by gName", dictionary=True)
    if(rows):
      for x in rows:
        retGroups.append(x['gName'])
      return(retGroups)
    return(0)
  except:
    print("Error connecting to db 1")
    return(0)
  

def getDefaults(table="tasks"):
  dbconn = dbRbhus.dbRbhus()
  defs = {}
  try:
    rows = dbconn.execute("desc "+ table, dictionary=True)
  except:
    print(str(sys.exc_info()))
    return(0)
  for x in rows:
    
    if(x['Default']):
      defs[x['Field']] = x['Default']
    else:
      defs[x['Field']] = ""
  return(defs)
  

def getResTemplates():
  dbconn = dbRbhus.dbRbhus()
  try:
    rows = dbconn.execute("SELECT * FROM resTemplates", dictionary=True)
  except:
    print(str(sys.exc_info()))
    return(0)
  return(rows)
    
def getProjects():
  dbconn = dbRbhus.dbRbhus()
  try:
    rows = dbconn.execute("select * from proj", dictionary=True)
  except:
    print("Error connecting to db 2")
    return(0)
  retRows = []  
  if(rows):
    for row in rows:
      retRows.append(row['projName'])
    return(retRows)
  else:
    return(0)

def getFileTypes():
  dbconn = dbRbhus.dbRbhus()
  try:
    rows = dbconn.execute("select * from fileType", dictionary=True)
  except:
    print("Error connecting to db 3")
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
    
def getLocalNameIP():
  while(1):
    try:
      hostname = socket.gethostname()
      ipAddr = socket.gethostbyname(socket.gethostname()).strip()
      return(hostname,ipAddr)
    except:
      print(str(sys.exc_info()))
      time.sleep(1)




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





class hosts(object):
  def __init__(self,hostIp = 0):
    self.db_conn = dbRbhus.dbRbhus()
    
    self.MyHost = socket.gethostname()
    self.MyIp = socket.gethostbyname(socket.gethostname()).strip()

    self.username = None
    self.userProjIds = []
    try:
      self.username = os.environ['rbhus_acl_user'].rstrip().lstrip()
    except:
      pass
    try:
      self.userProjIds = os.environ['rbhus_acl_projIds'].split()
    except:
      pass
    try:
      self.userAdmin = int(os.environ['rbhus_acl_admin'])
    except:
      pass
    if(hostIp):
      self.ip = hostIp
    else:
      self.ip = self.MyIp
    self.hostDetails = self._getHostDetails()
    
  
  
  def _getHostDetails(self):
    try:
      rows = self.db_conn.execute("select * from hostInfo, hostEffectiveResource, hostResource, hostAlive where (hostInfo.ip COLLATE utf8_unicode_ci = hostResource.ip) and (hostInfo.ip COLLATE utf8_unicode_ci =hostEffectiveResource.ip) and (hostInfo.ip COLLATE utf8_unicode_ci = hostAlive.ip) and (hostInfo.ip = '"+ str(self.ip) +"')",dictionary=True)
      if(rows):
        return(rows[-1])
      else:
        return(0)
    except:
      return(0)
      
  def hStop(self):
    if(self.userAdmin or (str(self.hostDetails['ip']) == MyIp)):
      try:
        rFrames = self.db_conn.execute("select * from frames where status = "+ str(constants.framesRunning) +" and hostName = \'"+ str(self.hostDetails['hostName']) +"\'", dictionary=True)
      except:
        print(str(sys.exc_info()))
        return(0)
      if(rFrames):
        for rF in rFrames:
          self.db_conn.stopFrames(self.hostDetails['hostName'],rF['id'],rF['frameId'])
          print(str(self.hostDetails['hostName']) +" : "+ str(rF['id']) +" : "+ str(rF['frameId']))
      return(1)
    else:
      print("Only local hosts can be stopped without admin rights!")
      return(0)
      
  def hEnable(self):
    if(self.userAdmin or (str(self.hostDetails['ip']) == MyIp)):
      try:
        self.db_conn.execute("update hostInfo set status = "+ str(constants.hostInfoEnable) +" where ip=\'"+ str(self.hostDetails['ip']) +"\'")
      except:
        print(str(sys.exc_info()))
        return(0)
      self.hostDetails = self._getHostDetails()
      return(1)
    else:
      print("Only local hosts can be enabled without admin rights!")
      return(0)
      
  def hDisable(self):
    if(self.userAdmin or (str(self.hostDetails['ip']) == MyIp)):
      try:
        self.db_conn.execute("update hostInfo set status = "+ str(constants.hostInfoDisable) +" where ip=\'"+ str(self.hostDetails['ip']) +"\'")
      except:
        print(str(sys.exc_info()))
        return(0)
      self.hostDetails = self._getHostDetails()
      return(1)
    else:
      print("Only local hosts can be enabled without admin rights!")
      return(0)
  
  
  def setGroups(self,nGroups):
    tmpRow = nGroups.split(",")
    try:
      tmpRow.remove("default")
    except:
      pass
    try:
      tmpRow.remove(self.hostDetails['hostName'])
    except:
      pass
    aGroups = getHostGroupsActive()
    newGroups = ["default"]
    newGroups.append(self.hostDetails['hostName'])
    for tr in tmpRow:
      if(tr not in aGroups):
        print("hostGroup "+ str(tr) +" not a valid group")
      else:
        try:
          newGroups.remove(tr)
        except:
          pass
        newGroups.append(tr)
    uGroups = {}
    for x in newGroups:
      uGroups[x] = 1
    fGroups = uGroups.keys()
    self.setHostData("hostInfo","groups","'"+ ",".join(fGroups) +"'")
      
      
  def updateGroups(self,nGroups):
    tmpRow = nGroups.split(",")
    try:
      tmpRow.remove("default")
    except:
      pass
    try:
      tmpRow.remove(self.hostDetails['hostName'])
    except:
      pass
    aGroups = getHostGroupsActive()
    newGroups = ["default"]
    newGroups.append(self.hostDetails['hostName'])
    
    for tr in tmpRow:
      if(tr not in aGroups):
        print("hostGroup "+ str(tr) +" not a valid group")
      else:
        try:
          newGroups.remove(tr)
        except:
          pass
        newGroups.append(tr)
        
    oldGroups = self.hostDetails['groups'].split(",")
    revampedGroups = []
    for x in newGroups:
      if(x in oldGroups):
        print("hostGroup "+ str(tr) +" duplicate group")
      else:
        oldGroups.append(x)
        
    uGroups = {}
    for x in oldGroups:
      uGroups[x] = 1
    fGroups = uGroups.keys()
    self.setHostData("hostInfo","groups","'"+ ",".join(fGroups) +"'")
    
          
  
  def killClient(self):
    if(self.userAdmin):
      clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      try:
        clientSocket.settimeout(15)
        clientSocket.connect((self.hostDetails['ip'],6661))
      except:
        print("cannot connect : "+ self.hostDetails['hostName'] +" : "+ str(sys.exc_info()))
        try:
          clientSocket.close()
        except:
          pass
      clientSocket.send("CLIENTKILL")
      clientSocket.close()
  
  
  def startClient(self):
    if(self.userAdmin):
      clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      try:
        clientSocket.settimeout(15)
        clientSocket.connect((self.hostDetails['ip'],6661))
      except:
        print("cannot connect : "+ self.hostDetails['hostName'] +" : "+ str(sys.exc_info()))
        try:
          clientSocket.close()
        except:
          pass
      clientSocket.send("CLIENTSTART")
      clientSocket.close()
  
  
  def setHostData(self,table,field,value):
    if(self.userAdmin):
      try:
        self.db_conn.execute("update "+ str(table) +" set "+ str(field) +"="+ str(value) +" where ip='"+ str(self.hostDetails['ip']) +"'")
      except:
        print(str(sys.exc_info()))
        return(0)
      self.hostDetails = self._getHostDetails()
      return(1)
    else:
      print("Only local hosts or a human with  admin rights can edit hosts data!")
      return(0)





class tasks(object):
  def __init__(self, tId = 0):
    self.db_conn = dbRbhus.dbRbhus()
    self.taskFields = self._getTaskFields()
    self.username = None
    self.userProjIds = []
    try:
      self.username = os.environ['rbhus_acl_user'].rstrip().lstrip()
    except:
      pass
    try:
      self.userProjIds = os.environ['rbhus_acl_projIds'].split()
    except:
      pass
    try:
      self.userAdmin = int(os.environ['rbhus_acl_admin'])
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
      self.db_conn.execute("insert into tasksLog (id) values ("+ str(self.taskId) +")")
      return(self.taskId)
    except:
      self.taskId = 0
      raise
  
  
  def fastAssign(self,enable=0):
    if(self.userAdmin == 1):
      try:
        self.db_conn.execute("update tasks set fastAssign='" + str(enable) +"' where id='"+ str(self.taskId) +"'")
        self.taskDetails = self._getTaskDetails(self.taskId)
        return(1)
      except:
        return(0)
    else:
      print("user : "+ str(self.username) +" : NOT allowed to edit")
      return(0)
  
  
  def remove(self):
    if((self.username == self.taskDetails['user']) or (str(self.taskDetails['projId']) in self.userProjIds) or (self.userAdmin == 1)):
      try:
        self.db_conn.execute("delete from tasks where \
                             (id="+ str(taskId) +") and \
                             (status != "+ str(constants.taskWaiting) +") and \
                             (status != "+ str(constants.taskPending) +") and \
                             (status != "+ str(constants.taskActive) +") and \
                             ((select count(*) FROM frames where (id="+ str(self.taskId) +") and ((status="+ str(constants.framesRunning) +") or (status="+ str(constants.framesPending) +")))=0)")
        return(1)
      except:
        return(0)
    else:
      print("user : "+ str(self.username) +" : NOT allowed to edit")
      return(0)
  
  
  def edit(self,fieldDict):
    self.validFields = {}
    self.invalidFields = {}
    print(self.username)
    print(self.userProjIds)
    print(self.taskDetails['projId'])
    if(self.username):
      if((self.username == self.taskDetails['user']) or (str(self.taskDetails['projId']) in self.userProjIds) or (self.userAdmin == 1)):
        print("user : "+ str(self.username) +" : allowed to edit")
      else:
        print("user : "+ str(self.username) +" : NOT allowed to edit")
        return(0)
    else:
      return(0)
    for x in fieldDict.keys():
      if(self.taskFields.has_key(x)):
        self.validFields[x] = fieldDict[x]
      else:
        self.invalidFields[x] = fieldDict[x]
        
    if(self.validFields):
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