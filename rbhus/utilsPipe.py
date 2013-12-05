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


def getProjDefaults():
  dbconn = dbPipe.dbPipe()
  try:
    rows = dbconn.execute("desc proj",dictionary=True)
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
def createProj(projType,projName,directory,admins,rbhusRenderIntergration,rbhusRenderServer,aclUser,aclGroup,dueDate,description):
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
  projDets['rbhusRenderIntergration'] = rbhusRenderIntergration if(rbhusRenderIntergration) else pDefs['rbhusRenderIntergration']
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
def setupProj(projType,projName,directory,admins,rbhusRenderIntergration,rbhusRenderServer,aclUser,aclGroup,createdUser,dueDate,description):
  dbconn = dbPipe.dbPipe()
  pTypes = getProjTypes()
  cScript = ""
  for pT in pTypes:
    if(pT['type'] == projType):
      cScript = pT['scriptDir']
      
  os.environ['rp_projName_c'] = str(projName)
  os.environ['rp_projType_c'] = str(projType)
  os.environ['rp_projDirectory_c'] = str(directory)
  os.environ['rp_projAdmin_c'] = str(admins)
  os.environ['rp_projRender_c'] = str(rbhusRenderIntergration)
  os.environ['rp_projRenderS_c'] = str(rbhusRenderServer)
  os.environ['rp_projDesc_c'] = str(description)
  os.environ['rp_projAclUser_c'] = str(aclUser)
  os.environ['rp_projAclGroup_c'] = str(aclGroup)
  os.environ['rp_projDueDate_c'] = str(dueDate)
  os.environ['rp_projCreatedUser_c'] = str(createdUser)

  exportDirMaps(directory)
  exportProjTypes(projType)
  utilsPipeLogger(description)
  utilsPipeLogger(projName)
  try:
    dbconn.execute("insert into proj (projName,directory,admins,projType,rbhusRenderIntergration,rbhusRenderServer,aclUser,aclGroup,createdUser,dueDate,createDate,description) \
                    values ('"+ str(projName) +"', \
                    '"+ str(directory) +"', \
                    '"+ str(admins) +"', \
                    '"+ str(projType) +"', \
                    '"+ str(rbhusRenderIntergration) +"', \
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
      status = os.system("python -d '"+ str(cScript) +"'")
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


def getProjDetails(projName):
  if(projName):
    dbconn = dbPipe.dbPipe()
    try:
      rows = dbconn.execute("select * from proj where projName='"+ str(projId) +"'", dictionary=True)
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
  
  
def setupSequence(seqDict):
  projName = str(seqDict['projName'])
  seqName = str(seqDict['sequenceName'])
  seqId = hashlib.sha256(projName +":"+ seqName)
  
  projDets = getProjDetails(str(seqDict['projName']))
  dirMapsDets = getDirMapsDetails(str(projDets['directory']))
  
  dbconn = dbPipe.dbPipe()
  try:
    dbconn.execute("insert into sequence (sequenceId,projName,sequenceName,admins,sFrame,eFrame,createDate,dueDate,createdUser,description) \
                    values('" \
                    + str(seqId) +"','" \
                    + str(seqDict['projName']) +"','" \
                    + str(seqDict['sequenceName']) +"','" \
                    + str(seqDict['admins']) +"','" \
                    + str(seqDict['sFrame']) +"','" \
                    + str(seqDict['eFrame']) +"','" \
                    + str(MySQLdb.Timestamp.now()) +"','" \
                    + str(seqDict['dueDate']) +"','" \
                    + str(seqDict['createdUser']) +"','" \
                    + str(seqDict['description']) +"')")
  except:
    utilsPipeLogger(str(sys.exc_info()))
    return(0)
  
  if(sys.platform.find("linux") >= 0):
    try:
      os.makedirs(dirMapsDets['linuxMapping'].rstrip("/") +"/"+ seqDict['projName'] +"/"+ seqDict['sequenceName'])
    except:
      utilsPipeLogger(str(sys.exc_info()))
    
  if(sys.platform.find("win") >= 0):
    try:
      os.makedirs(dirMapsDets['windowsMapping'].rstrip("/") +"/"+ seqDict['projName'] +"/"+ seqDict['sequenceName'])
    except:
      utilsPipeLogger(str(sys.exc_info()))
  return(1)    
      
    
  
  
def setupScene(sceDict):
  sceneId = hashlib.sha256(str(sceDict['projName']) +":"+ str(sceDict['sequenceId']) +":"+ str(sceDict['sceneName']))
  dbconn = dbPipe.dbPipe()
  try:
    dbconn.execute("insert into scene (sceneId,projName,sequenceId,sceneName,admins,sFrame,eFrame,createDate,dueDate,createdUser,description) \
                    values('" \
                    + str(sceneId) +"','" \
                    + str(sceDict['projName']) +"','" \
                    + str(sceDict['sequenceId']) +"','" \
                    + str(sceDict['sceneName']) +"','" \
                    + str(sceDict['admins']) +"','" \
                    + str(sceDict['sFrame']) +"','" \
                    + str(sceDict['eFrame']) +"','" \
                    + str(MySQLdb.Timestamp.now()) +"','" \
                    + str(sceDict['dueDate']) +"','" \
                    + str(sceDict['createdUser']) +"','" \
                    + str(sceDict['description']) +"')")
  except:
    utilsPipeLogger(str(sys.exc_info()))
    return(0)
  
  if(sys.platform.find("linux") >= 0):
    try:
      os.makedirs(dirMapsDets['linuxMapping'].rstrip("/") +"/"+ sceDict['projName'] +"/"+ sceDict['sequenceName'])
    except:
      utilsPipeLogger(str(sys.exc_info()))
    
  if(sys.platform.find("win") >= 0):
    try:
      os.makedirs(dirMapsDets['windowsMapping'].rstrip("/") +"/"+ sceDict['projName'] +"/"+ sceDict['sequenceName'])
    except:
      utilsPipeLogger(str(sys.exc_info()))
  return(1)    
  

  
  
class assets(object):
  def register(self,assDetDict):
    projId = str(assDetDict['projName'])
    seqId = str(assDetDict['sequenceName'])
    sceneId = str(assDetDict['sceneName'])
    stageType = str(assDetDict['stageType'])
    assName = str(assDetDict['assName'])
    nodeType = str(assDetDict['nodeType'])
    fileType = str(assDetDict['fileType'])
    aId = hashlib.sha256(projId +":"+ seqId +":"+ sceneId +":"+ stageType +":"+ assName +":"+ nodeType +":"+ fileType)
    assId = aId.hexdigest()
    
  
  def details(self,assDetDict={},assId=0):
    pass
  
  def openAsset(self,assId):
    pass
  
  def links(self,assId):
    pass
  
  def linkedTo(self,assId):
    pass
  
  
  
  
    