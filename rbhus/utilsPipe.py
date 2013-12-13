import sys
import os
import socket
import MySQLdb
import multiprocessing
import pickle
import datetime
import hashlib
import logging
import logging.handlers
import tempfile

progPath =  sys.argv[0].split(os.sep)
if(len(progPath) > 1):
  pwd = os.sep.join(progPath[0:-1])
  cwd = os.path.abspath(pwd)
else:
  cwd = os.path.abspath(os.getcwd())

sys.path.append(cwd.rstrip(os.sep) + os.sep)
import dbPipe
import constantsPipe


hostname = socket.gethostname()
tempDir = os.path.abspath(tempfile.gettempdir())


LOG_FILENAME = logging.FileHandler(tempDir + os.sep +"rbhusDb_module"+ str(hostname) +".log")
  #LOG_FILENAME = logging.FileHandler('z:/pythonTestWindoze.DONOTDELETE/clientLogs/rbhusDb_'+ hostname +'.log')

#LOG_FILENAME = logging.FileHandler('/var/log/rbhusDb_module.log')
utilsPipeLogger = logging.getLogger("utilsPipeLogger")
utilsPipeLogger.setLevel(logging.ERROR)


#ROTATE_FILENAME = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=104857600, backupCount=3)
BASIC_FORMAT = logging.Formatter("%(asctime)s - %(funcName)s - %(levelname)s - %(message)s")
LOG_FILENAME.setFormatter(BASIC_FORMAT)
utilsPipeLogger.addHandler(LOG_FILENAME)




def getDirMaps():
  dbconn = dbPipe.dbPipe()
  try:
    rows = dbconn.execute("SELECT * FROM dirMaps", dictionary=True)
    return(rows)
  except:
    utilsPipeLogger(str(sys.exc_info()))
    return(0)
  
 
def getDirMapsDetails(directory):
  dbconn = dbPipe.dbPipe()
  try:
    rows = dbconn.execute("SELECT * FROM dirMaps where directory='"+ str(directory) +"'", dictionary=True)
  except:
    utilsPipeLogger(str(sys.exc_info()))
    return(0)
  if(rows):
    ret = {}
    fs = rows[0].keys()
    for x in fs:
      ret[x] = rows[0][x]
    return(ret)

 
def getProjTypes():
  dbconn = dbPipe.dbPipe()
  try:
    rows = dbconn.execute("SELECT * FROM projTypes", dictionary=True)
    return(rows)
  except:
    utilsPipeLogger(str(sys.exc_info()))
    return(0)
  
  
def getStageTypes():
  dbconn = dbPipe.dbPipe()
  try:
    rows = dbconn.execute("SELECT * FROM stageTypes", dictionary=True)
    return(rows)
  except:
    utilsPipeLogger(str(sys.exc_info()))
    return(0)


def getDefaults(table):
  dbconn = dbPipe.dbPipe()
  try:
    rows = dbconn.execute("desc "+ str(table),dictionary=True)
    taskFieldss = {}
    for row in rows:
      taskFieldss[row['Field']] = row['Default']
    return(taskFieldss)
  except:
    utilsPipeLogger(str(sys.exc_info()))
    return(0)


def getAdmins():
  dbconn = dbPipe.dbPipe()
  adminUsers = []
  try:
    rows = dbconn.execute("select * from admins", dictionary=True)
    if(rows):
      for x in rows:
        adminUsers.append(x['user'])
    return(adminUsers)
  except:
    utilsPipeLogger(str(sys.exc_info()))
    # easy to search like - if admin in getAdmins():
    return(adminUsers)


# createdUser should come from an env variable set by the authPipe module
def createProj(projType,projName,directory,admins,rbhusRenderIntegration,rbhusRenderServer,aclUser,aclGroup,dueDate,description):
  if(os.environ['rbhusPipe_acl_user'] not in getAdmins()):
    utilsPipeLogger("User not allowed to create projects")
    return(0)
  pDefs = getProjDefaults()
  now = datetime.datetime.now()
  projDets = {}
  projDets['projType'] = projType if(projType) else pDefs['projType']
  projDets['projName'] = projName if(projName) else pDefs['projName']
  projDets['directory'] = directory if(directory) else pDefs['directory']
  projDets['admins'] = admins if(admins) else pDefs['admins']
  projDets['rbhusRenderIntegration'] = rbhusRenderIntegration if(rbhusRenderIntegration) else pDefs['rbhusRenderIntegration']
  projDets['rbhusRenderServer'] = rbhusRenderServer if(rbhusRenderServer) else pDefs['rbhusRenderServer']
  projDets['aclUser'] = aclUser if(aclUser) else pDefs['aclUser']
  projDets['aclGroup'] = aclGroup if(aclGroup) else pDefs['aclGroup']
  projDets['createdUser'] = os.environ['rbhusPipe_acl_user']
  projDets['dueDate'] = dueDate if(dueDate) else str(now.year + 1) +"-"+ str(now.month) +"-"+ str(now.day) +" "+ str(now.hour) +"-"+ str(now.minute) +"-"+ str(now.second)
  projDets['description'] = description if(description) else pDefs['description']
  
  servSoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:
    servSoc.settimeout(15)
    servSoc.connect((constantsPipe.projInitServer,constantsPipe.projInitPort))
  except:
    utilsPipeLogger("utilsPipe createProj : "+ str(sys.exc_info()))
    return(0)
    
  servSoc.send(pickle.dumps(projDets))
  servSoc.close()
  return(1)


#always called by the server
def setupProj(projType,projName,directory,admins,rbhusRenderIntegration,rbhusRenderServer,aclUser,aclGroup,createdUser,dueDate,description):
  dbconn = dbPipe.dbPipe()
  pTypes = getProjTypes()
  cScript = ""
  for pT in pTypes:
    if(pT['type'] == projType):
      cScript = pT['scriptDir']
      
  os.environ['rp_proj_projName'] = str(projName)
  os.environ['rp_proj_projType'] = str(projType)
  os.environ['rp_proj_directory'] = str(directory)
  os.environ['rp_proj_admins'] = str(admins)
  os.environ['rp_proj_rbhusRenderIntegration'] = str(rbhusRenderIntegration)
  os.environ['rp_proj_rbhusRenderServer'] = str(rbhusRenderServer)
  os.environ['rp_proj_description'] = str(description)
  os.environ['rp_proj_aclUser'] = str(aclUser)
  os.environ['rp_proj_aclGroup'] = str(aclGroup)
  os.environ['rp_proj_dueDate'] = str(dueDate)
  os.environ['rp_proj_createdUser'] = str(createdUser)

  exportDirMaps(directory)
  exportProjTypes(projType)
  utilsPipeLogger(description)
  utilsPipeLogger(projName)
  try:
    dbconn.execute("insert into proj (projName,directory,admins,projType,rbhusRenderIntegration,rbhusRenderServer,aclUser,aclGroup,createdUser,dueDate,createDate,description) \
                    values ('"+ str(projName) +"', \
                    '"+ str(directory) +"', \
                    '"+ str(admins) +"', \
                    '"+ str(projType) +"', \
                    '"+ str(rbhusRenderIntegration) +"', \
                    '"+ str(rbhusRenderServer) +"', \
                    '"+ str(aclUser) +"', \
                    '"+ str(aclGroup) +"', \
                    '"+ str(createdUser) +"', \
                    '"+ str(dueDate) +"', \
                    '"+ str(MySQLdb.Timestamp.now()) +"', \
                    '"+ str(description) +"')")
  except:
    utilsPipeLogger(str(sys.exc_info()))
    return(0)
    
  try:
    if(cScript):
      status = os.system("python -d '"+ str(cScript).rstrip("/") +"/"+ projType +".py'")
      return(1)
  except:
    utilsPipeLogger(str(sys.exc_info()))
    return(0)
    

def exportDirMaps(directory):
  dirms = getDirMaps()
  if(dirms):
    for x in dirms:
      if(x['directory'] == directory):
        flds = x.keys()
        for f in flds:
          os.environ['rp_dirMaps_'+ str(f).rstrip().lstrip()] = str(x[f])
        return(1)
  return(0)


def exportProjTypes(projType):
  ptypes = getProjTypes()
  if(ptypes):
    for x in ptypes:
      if(x['type'] == projType):
        flds = x.keys()
        for f in flds:
          os.environ['rp_projTypes_'+ str(f).rstrip().lstrip()] = str(x[f])
        return(1)
  return(0)



#when you give the projName it returns a single dict else it returns an array of dict
def getProjDetails(projName=None,status=None):
  if(projName):
    dbconn = dbPipe.dbPipe()
    try:
      rows = dbconn.execute("select * from proj where projName='"+ str(projName) +"'", dictionary=True)
    except:
      utilsPipeLogger(str(sys.exc_info()))
      return(0)
    if(rows):
      ret = {}
      fs = rows[0].keys()
      for x in fs:
        ret[x] = rows[0][x]
      return(ret)
  if(status):
    if(status != "all")
      dbconn = dbPipe.dbPipe()
      try:
        rows = dbconn.execute("select * from proj where status="+ str(status), dictionary=True)
      except:
        utilsPipeLogger(str(sys.exc_info()))
        return(0)
      return(rows)
    else:
      dbconn = dbPipe.dbPipe()
      try:
        rows = dbconn.execute("select * from proj", dictionary=True)
      except:
        utilsPipeLogger(str(sys.exc_info()))
        return(0)
      return(rows)
  return(0)
    
    

    
    
def getSequenceSceneDetails(projName,sequence,scene):
  if(seqId):
    dbconn = dbPipe.dbPipe()
    try:
      rows = dbconn.execute("select * from sequenceScene where \
                             projName='"+ str(projName) +"' \
                             and sequenceName='"+ str(sequence) +"' \
                             and sceneName='"+ str(scene) +"'", dictionary=True)
    except:
      utilsPipeLogger(str(sys.exc_info()))
      return(0)
    if(rows):
      ret = {}
      fs = rows[0].keys()
      for x in fs:
        ret[x] = rows[0][x]
      return(ret)


def exportProj(projName):
  if(projName):
    dets = getProjDetails(projName=projName)
    for x in dets.keys():
      os.environ['rp_proj_'+ str(x)] = dets[x]
      return(1)
  
  

    
  
  
def setupSequenceScene(seqSceDict):
  dbconn = dbPipe.dbPipe()
  projDets = getProjDetails(str(seqSceDict['projName']))
  dirMapsDets = getDirMapsDetails(str(projDets['directory']))
  try:
    dbconn.execute("insert into sequenceScene (projName,sequenceName,sceneName,admins,sFrame,eFrame,createDate,dueDate,createdUser,description) \
                    values('" \
                    + str(seqSceDict['projName']) +"','" \
                    + str(seqSceDict['sequenceName']) +"','" \
                    + str(seqSceDict['sceneName']) +"','" \
                    + str(seqSceDict['admins']) +"','" \
                    + str(seqSceDict['sFrame']) +"','" \
                    + str(seqSceDict['eFrame']) +"','" \
                    + str(MySQLdb.Timestamp.now()) +"','" \
                    + str(seqSceDict['dueDate']) +"','" \
                    + str(os.environ['rbhusPipe_acl_user']) +"','" \
                    + str(seqSceDict['description']) +"')")
  except:
    utilsPipeLogger(str(sys.exc_info()))
    return(0)
  
  if(sys.platform.find("linux") >= 0):
    try:
      os.makedirs(dirMapsDets['linuxMapping'].rstrip("/") +"/"+ seqSceDict['projName'] +"/"+ seqSceDict['sequenceName'] +"/"+ seqSceDict['sceneName'])
    except:
      utilsPipeLogger(str(sys.exc_info()))
    
  if(sys.platform.find("win") >= 0):
    try:
      os.makedirs(dirMapsDets['windowsMapping'].rstrip("/") +"/"+ seqSceDict['projName'] +"/"+ seqSceDict['sequenceName'] +"/"+ seqSceDict['sceneName'])
    except:
      utilsPipeLogger(str(sys.exc_info()))
  return(1)    
  

def getFieldValue(table,field,fkey,fvalue):
  dbconn = dbPipe.dbPipe()
  try:
    rows = dbconn.execute("select "+ str(field) +" from "+ str(table) +" where "+ str(fkey) +"='"+ str(fvalue) +"'",dictionary=True)
    return(rows)
  except:
    utilsPipeLogger(str(sys.exc_info()))
    return(0)
  
# take in a pipe type path eg :  $table_field:test: 
# first and second should be $proj_directory:$proj_projName
def getAbsPath(pipePath):
  pPaths = pipePath.split(":")
  projName = pPaths[0]
  assDets = getAssDetails(assPath=pipePath)
  projDets = getProjDetails(projName)
  projDirMapsDets = getDirMapsDetails(assDets['directory'])
  absPath = ""
  
  if(sys.platform.find("linux") >= 0):
    absPath = os.path.abspath(projDirMapsDets['linuxMapping'].rstrip("/") +"/"+ pipePath.lstrip("/"))
  elif(sys.platform.find("win") >= 0):
    absPath = os.path.abspath(projDirMapsDets['linuxMapping'].rstrip("/") +"/"+ pipePath.lstrip("/"))
  return(absPath)
  

def getAssDetails(assId="",assPath=""):
  if(assId):
    dbconn = dbPipe.dbPipe()
    try:
      rows = dbconn.execute("select * from assets where assetId='"+ str(assId) +"'", dictionary=True)
    except:
      utilsPipeLogger(str(sys.exc_info()))
      return(0)
    if(rows):
      ret = {}
      fs = rows[0].keys()
      for x in fs:
        ret[x] = rows[0][x]
      return(ret)
  if(assPath):
    dbconn = dbPipe.dbPipe()
    try:
      rows = dbconn.execute("select * from assets where path='"+ str(assPath) +"'", dictionary=True)
    except:
      utilsPipeLogger(str(sys.exc_info()))
      return(0)
    if(rows):
      ret = {}
      fs = rows[0].keys()
      for x in fs:
        ret[x] = rows[0][x]
      return(ret)
  
def getAssTypes():
  dbconn = dbPipe.dbPipe()
  try:
    rows = dbconn.execute("SELECT * FROM assetTypes", dictionary=True)
    return(rows)
  except:
    utilsPipeLogger(str(sys.exc_info()))
    return(0)

def getAssTypesDetails(assType):
  dbconn = dbPipe.dbPipe()
  try:
    rows = dbconn.execute("SELECT * FROM assetTypes where type='"+ str(assType) +"'", dictionary=True)
    if(rows):
      return(rows[0])
    else:
      return(0)
  except:
    utilsPipeLogger(str(sys.exc_info()))
    return(0)


def assRegister(self,assDetDict):
  assPath = ""
  assId = ""
  
  if(re.search("^default",str(assDetDict['assetType']))):
    assPath = str(assDetDict['projName']) 
  elif(re.search("^path",str(assDetDict['assetType']))):
    assPath = str(assDetDict['projName']) +":"+ str(assDetDict['path'])
  else:
    assTypeDets = getAssTypesDetails(str(assDetDict['assetType']))
    if(assTypeDets):
      if(re.search("^default",str(assTypeDets['path']))):
        assPath = str(assDetDict['projName'])
      else:
        assPath = str(assDetDict['projName']) +":"+ str(assTypeDets['path'])
  if(assPath):
    if(not re.search("^default",str(assDetDict['sequenceName']))):
      if(not re.search("^default",str(assDetDict['sceneName']))):
        assPath = assPath +":"+ str(assDetDict['sequenceName']) +":" + str(assDetDict['sceneName'])
      else:
        utilsPipeLogger.debug("if sequenceName is given sceneName cannot be a default")
        return(0)
    if(not re.search("^default",str(assDetDict['stageType']))):
      assPath = assPath +":" + str(assDetDict['stageType'])
      if(not re.search("^default",str(assDetDict['nodeType']))):
        assPath = assPath +":" + str(assDetDict['nodeType'])
        
    assPath = assPath +":" + str(assDetDict['assName'])
    if(not re.search("^default",str(assDetDict['fileType']))): 
      assPath = assPath +":" + str(assDetDict['fileType'])
    assId = hashlib.sha256(assPath).hexdigest()
    assDetDict['assetId'] = assId
    assDetDict['path'] = assPath
    fieldsA = []
    valuesA = []
    for x in assDetDict.keys():
      fieldsA.append(str(x))
      valuesA.append("'"+ str(assDetDict[x]) +"'")
    fs = "("+ ",".join(fieldsA) +")"
    vs = "("+ ",".join(valuesA) +")"
    dbconn = dbPipe.dbPipe()
    try:
      rows = dbconn.execute("insert into assets "+ fs +" values "+ vs)
    except:
      utilsPipeLogger(str(sys.exc_info()))
      return(0)
    try:
      os.makedirs(getAbsPath(assPath))
    except:
      utilsPipeLogger(str(sys.exc_info()))
      return(0)
    return(1)
  else:
    return(0)
    
    
          
            
    
    
  
  def details(self,assDetDict={},assId=0):
    pass
  
  def openAsset(self,assId):
    pass
  
  def links(self,assId):
    pass
  
  def linkedTo(self,assId):
    pass
  
  
  
  
    