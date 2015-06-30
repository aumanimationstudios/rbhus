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
import subprocess
import re
import shutil
import copy


progPath =  sys.argv[0].split(os.sep)
if(len(progPath) > 1):
  pwd = os.sep.join(progPath[0:-1])
  cwd = os.path.abspath(pwd)
  print("utilsPipe 1: "+ str(cwd))
else:
  cwd = os.path.abspath(os.getcwd())


etcpathtmp = cwd.split(os.sep)[0:-2]
etcpathtmp.append("rbhus")
etcpathtmp.append("etc")
etcpath = os.sep.join(etcpathtmp)
print("utilsPipe 1: "+ str(etcpath))


sys.path.append(cwd.rstrip(os.sep) + os.sep)
import dbPipe
import constantsPipe


if(sys.platform.find("win") >= 0):
  try:
    username = os.environ['USERNAME']
  except:
    username = "nobody"
if(sys.platform.find("linux") >= 0):
  try:
    username = os.environ['USER']
  except:
    username = "nobody"







hostname = socket.gethostname()
tempDir = os.path.abspath(tempfile.gettempdir())


LOG_FILENAME = logging.FileHandler(tempDir + os.sep +"rbhusPipe_utilsPipe_module_"+ username +"_"+ str(hostname) +".log")
  #LOG_FILENAME = logging.FileHandler('z:/pythonTestWindoze.DONOTDELETE/clientLogs/rbhusDb_'+ hostname +'.log')

#LOG_FILENAME = logging.FileHandler('/var/log/rbhusDb_module.log')
utilsPipeLogger = logging.getLogger("utilsPipeLogger")
utilsPipeLogger.setLevel(logging.DEBUG)


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
    utilsPipeLogger.debug(str(sys.exc_info()))
    return(0)
  

def getTags(projName="",assPath="",assId=""):
  dbconn = dbPipe.dbPipe()
  if(projName):
    try:
      rows = dbconn.execute("SELECT tags FROM assets WHERE projName='"+ projName +"' order by tags", dictionary=True)
      if(rows):
        #print(rows)
        tags = {}
        for x in rows:
          t = x['tags'].split(",")
          for b in t:
            tags[b] = 1
        retags = []
        for y in tags.keys():
          retags.append(y)
        return(retags)
    except:
      utilsPipeLogger.debug(str(sys.exc_info()))
      return(0)
  return(0)
  



def getDirMapsDetails(directory):
  dbconn = dbPipe.dbPipe()
  try:
    rows = dbconn.execute("SELECT * FROM dirMaps where directory='"+ str(directory) +"' order by directory", dictionary=True)
  except:
    utilsPipeLogger.debug(str(sys.exc_info()))
    return(0)
  if(rows):
    ret = {}
    fs = rows[0].keys()
    for x in fs:
      ret[x] = rows[0][x]
    return(ret)

 
def getProjTypes(ptype=None):
  dbconn = dbPipe.dbPipe()
  try:
    if(ptype):
      rows = dbconn.execute("SELECT * FROM projTypes where type='"+ str(ptype) +"' order by type", dictionary=True)
      if(rows):
        return(rows[0])
      else:
        return(0)
    else:
      rows = dbconn.execute("SELECT * FROM projTypes order by type", dictionary=True)
      if(rows):
        return(rows)
      else:
        return(0)
  except:
    utilsPipeLogger.debug(str(sys.exc_info()))
    return(0)
  
  
def getStageTypes(stype=None):
  dbconn = dbPipe.dbPipe()
  try:
    if(stype):
      rows = dbconn.execute("SELECT * FROM stageTypes where type='"+ str(stype) +"' order by type", dictionary=True)
      if(rows):
        return(rows[0])
      else:
        return(0)
    else:
      rows = dbconn.execute("SELECT * FROM stageTypes order by type", dictionary=True)
      if(rows):
        return(rows)
      else:
        return(0)
  except:
    utilsPipeLogger.debug(str(sys.exc_info()))
    return(0)


def getValidNodes(stype):
  pass
  
  
  
  

def getNodeTypes(ntype=None):
  dbconn = dbPipe.dbPipe()
  try:
    if(ntype):
      rows = dbconn.execute("SELECT * FROM nodeTypes where type='"+ str(ntype) +"' order by type", dictionary=True)
      if(rows):
        return(rows[0])
      else:
        return(0)
    else:
      rows = dbconn.execute("SELECT * FROM nodeTypes order by type", dictionary=True)
      if(rows):
        return(rows)
      else:
        return(0)
  except:
    utilsPipeLogger.debug(str(sys.exc_info()))
    return(0)


def getFileTypes(ftype=None):
  dbconn = dbPipe.dbPipe()
  try:
    if(ftype):
      rows = dbconn.execute("SELECT * FROM fileTypes where type='"+ str(ftype) +"' order by type", dictionary=True)
      if(rows):
        return(rows[0])
      else:
        return(0)
    else:
      rows = dbconn.execute("SELECT * FROM fileTypes order by type", dictionary=True)
      if(rows):
        return(rows)
      else:
        return(0)
  except:
    utilsPipeLogger.debug(str(sys.exc_info()))
    return(0)


def getAssTypes(atype=None):
  dbconn = dbPipe.dbPipe()
  try:
    if(atype):
      rows = dbconn.execute("SELECT * FROM assetTypes where type='"+ str(atype) +"' order by type", dictionary=True)
      if(rows):
        return(rows[0])
      else:
        return(0)
    else:
      rows = dbconn.execute("SELECT * FROM assetTypes order by type", dictionary=True)
      if(rows):
        return(rows)
      else:
        return(0)
  except:
    utilsPipeLogger.debug(str(sys.exc_info()))
    return(0)


def getSequenceScenes(proj,seq=None,sce=None):
  dbconn = dbPipe.dbPipe()
  try:
    if(proj and seq and (not sce)):
      rows = dbconn.execute("SELECT * FROM sequenceScenes where projName='"+ str(proj) +"' and sequenceName='"+ str(seq) +"' order by sequenceName,sceneName", dictionary=True)
    elif(proj and seq and sce):
      rows = dbconn.execute("SELECT * FROM sequenceScenes where projName='"+ str(proj) +"' and sequenceName='"+ str(seq) +"' and sceneName='"+ str(sce) +"' order by sequenceName,sceneName", dictionary=True)
    else:
      rows = dbconn.execute("SELECT * FROM sequenceScenes where projName='"+ str(proj) +"' order by sequenceName,sceneName", dictionary=True)
    if(rows):
      return(rows)
    else:
      return(0)
  except:
    utilsPipeLogger.debug(str(sys.exc_info()))
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
    utilsPipeLogger.debug(str(sys.exc_info()))
    return(0)


def getAdmins():
  dbconn = dbPipe.dbPipe()
  adminUsers = []
  try:
    rows = dbconn.execute("select * from admins  order by user", dictionary=True)
    if(rows):
      for x in rows:
        adminUsers.append(x['user'])
    return(adminUsers)
  except:
    utilsPipeLogger.debug(str(sys.exc_info()))
    # easy to search like - if admin in getAdmins():
    return(adminUsers)


# createdUser should come from an env variable set by the authPipe module
def createProj(projType,projName,directory,admins,rbhusRenderIntegration,rbhusRenderServer,aclUser,aclGroup,dueDate,description):
  if(os.environ['rbhusPipe_acl_user'] not in getAdmins()):
    utilsPipeLogger.debug("User not allowed to create projects")
    return(0)
  pDefs = getDefaults("proj")
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
    utilsPipeLogger.debug("utilsPipe createProj : "+ str(sys.exc_info()))
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
  utilsPipeLogger.debug(description)
  utilsPipeLogger.debug(projName)
  utilsPipeLogger.debug(cScript)
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
    utilsPipeLogger.debug(str(sys.exc_info()))
    return(0)
  
  seqScnDict = {}
  seqScnDict['sequenceName'] = "default"
  seqScnDict['projName'] = str(projName)
  seqScnDict['sceneName'] = "default"
  seqScnDict['createdUser'] = str(createdUser)
  
  setupSequenceScene(seqScnDict)
  
    
  try:
    if(cScript):
      dbconn.execute("update proj set createStatus="+ str(constantsPipe.createStatusRunning) +" where projName='"+ str(projName) +"'")
      utilsPipeLogger.debug("python -d '"+ str(cScript).rstrip("/") +"/"+ projType +".py'")
      status = os.system("python -d '"+ str(cScript).rstrip("/") +"/"+ projType +".py'")
      if(status != 0):
        dbconn.execute("update proj set createStatus="+ str(constantsPipe.createStatusFailed) +" where projName='"+ str(projName) +"'")
      else:
        dbconn.execute("update proj set createStatus="+ str(constantsPipe.createStatusDone) +" where projName='"+ str(projName) +"'")
      return(1)
  except:
    utilsPipeLogger.debug(str(sys.exc_info()))
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


def exportAsset(assDets):
  for x in assDets:
    os.environ['rp_assets_'+ str(x).rstrip().lstrip()] = str(assDets[x])
  return(1)
  


#when you give the projName it returns a single dict else it returns an array of dict
def getProjDetails(projName=None,status=None):
  if(projName):
    dbconn = dbPipe.dbPipe()
    try:
      rows = dbconn.execute("select * from proj where projName='"+ str(projName) +"' order by projName", dictionary=True)
    except:
      utilsPipeLogger.debug(str(sys.exc_info()))
      return(0)
    if(rows):
      ret = {}
      fs = rows[0].keys()
      for x in fs:
        ret[x] = rows[0][x]
      return(ret)
  elif(status):
    if(status != "all"):
      dbconn = dbPipe.dbPipe()
      try:
        rows = dbconn.execute("select * from proj where status="+ str(status) +" order by projName", dictionary=True)
      except:
        utilsPipeLogger.debug(str(sys.exc_info()))
        return(0)
      return(rows)
    else:
      dbconn = dbPipe.dbPipe()
      try:
        rows = dbconn.execute("select * from proj", dictionary=True)
      except:
        utilsPipeLogger.debug(str(sys.exc_info()))
        return(0)
      return(rows)
  return(0)
    

def exportProj(projName):
  if(projName):
    dets = getProjDetails(projName=projName)
    for x in dets.keys():
      os.environ['rp_proj_'+ str(x)] = str(dets[x])
    exportProjTypes(dets['projType'])
    exportDirMaps(dets['directory'])
  
  
  

    
  
  
def setupSequenceScene(seqSceDict):
  dbconn = dbPipe.dbPipe()
  projDets = getProjDetails(str(seqSceDict['projName']))
  dirMapsDets = getDirMapsDetails(str(projDets['directory']))
  defaultSeq = {}
  defaultSeq['projName'] = str(seqSceDict['projName'])
  defaultSeq['sequenceName'] = str(seqSceDict['sequenceName'])
  defaultSeq['sceneName'] = "default"
  
  defKeys = defaultSeq.keys()
  defValues = ["'"+ defaultSeq[x] +"'" for x in defKeys]
  
  seqKeys = seqSceDict.keys()
  seqValues = ["'"+ seqSceDict[x] +"'" for x in seqKeys]
  seqKeys.append("createDate")
  seqValues.append("'"+ str(MySQLdb.Timestamp.now()) +"'")
  
  
  if(not seqSceDict.has_key("createdUser")):
    try:
      seqValues.append("'"+ os.environ['rbhusPipe_acl_user'] +"'")
      seqKeys.append("createdUser")
    except:
      print("createdUser not given for seq scn")
      return(0)
  
    
  try:
    dbconn.execute("insert into sequenceScenes ("+ ",".join(defKeys) +") \
                    values("+ ",".join(defValues) +")")
  except:
    utilsPipeLogger.debug(str(sys.exc_info()))
    
    
  try:
    dbconn.execute("insert into sequenceScenes ("+ ",".join(seqKeys) +") \
                    values("+ ",".join(seqValues) +")")
  except:
    utilsPipeLogger.debug(str(sys.exc_info()))
    return(0)
  

def getFieldValue(table,field,fkey,fvalue):
  dbconn = dbPipe.dbPipe()
  try:
    rows = dbconn.execute("select "+ str(field) +" from "+ str(table) +" where "+ str(fkey) +"='"+ str(fvalue) +"'",dictionary=True)
    return(rows)
  except:
    utilsPipeLogger.debug(str(sys.exc_info()))
    return(0)
  
# take in a pipe type path eg :  $table_field:test: 
# first and second should be $proj_directory:$proj_projName
def getAbsPath(pipePath):
  absPath = []
  absPathArray = pipePath.split(":")
  for x in absPathArray:
    if(re.search("^\$",str(x))):
      absPath.append(os.environ["rp_"+ str(x).lstrip("$")])
    else:
      absPath.append(str(x))
  
  projName = absPath[0]
  #print("getAbsPath 1: "+ str(projName))
  
  
  #print("getAbsPath 2: "+ str(projDets))
  
  assDets = getAssDetails(assPath=pipePath)
  #print("getAbsPath 3: "+ str(projDets))
  if(assDets):
    projDirMapsDets = getDirMapsDetails(assDets['directory'])
  else:
    projDets = getProjDetails(projName)
    projDirMapsDets = getDirMapsDetails(projDets['directory'])
    
  #print("getAbsPath 4: "+ str(projDirMapsDets))
  absPathRet = ""
  if(sys.platform.find("linux") >= 0):
    absPathRet = os.path.abspath(projDirMapsDets['linuxMapping'].rstrip("/") +"/"+ ":".join(absPath).replace(":","/").lstrip("/"))
  elif(sys.platform.find("win") >= 0):
    absPathRet = os.path.abspath(projDirMapsDets['windowsMapping'].rstrip("/") +"/"+ ":".join(absPath).replace(":","/").lstrip("/"))
  return(absPathRet)
  
  


def getAssDetails(assId="",assPath=""):
  if(assId):
    dbconn = dbPipe.dbPipe()
    try:
      rows = dbconn.execute("select * from assets where assetId='"+ str(assId) +"'", dictionary=True)
    except:
      utilsPipeLogger.debug(str(sys.exc_info()))
      return(0)
    if(rows):
      ret = {}
      fs = rows[0].keys()
      for x in fs:
        ret[x] = rows[0][x]
      return(ret)
    return(0)
  if(assPath):
    dbconn = dbPipe.dbPipe()
    try:
      rows = dbconn.execute("select * from assets where path='"+ str(assPath) +"'", dictionary=True)
    except:
      utilsPipeLogger.debug(str(sys.exc_info()))
      return(0)
    if(rows):
      ret = {}
      fs = rows[0].keys()
      for x in fs:
        ret[x] = rows[0][x]
      return(ret)
    return(0)
  
def getProjAssesLinked(projName,limit=None,whereDict={}):
  dbconn = dbPipe.dbPipe()
  linkedProjects = "default"
  projs = []
  whereProj = ""
  try:
    linkedProjects = os.environ["rp_proj_linkedProjects"]
  except:
    utilsPipeLogger.debug(str(sys.exc_info()))
    return(0)
  if(linkedProjects != "default"):
    projs = ["'"+ x +"'" for x in linkedProjects.split(",")]
    print(projs)
    whereProj = " where projName=" + " or projName=".join(projs)
  print("in getProjAssesLinked module 1")
  whereString = []
  try:
    if(not limit):
      if(whereDict):
        
        for x in whereDict:
          whereDicts = []
          y = whereDict[x].split(",")
          for z in y:
            if(x == "assName"):
              if(z):
                whereDicts.append(x +" like '%"+ z +"%'")
            elif(x == "tags"):
              if(z):
                whereDicts.append(x +" like '%"+ z +"%'")
            elif(x == "assignedWorker"):
              if(z):
                whereDicts.append(x +" like '%"+ z +"%'")
            else:
              if(z):
                whereDicts.append(x +"='"+ z +"'")
          whereString.append("("+ " or ".join(whereDicts) +")")
          
        rows = dbconn.execute("select * from assets "+ whereProj +" and ("+ " and ".join(whereString) +") order by sequenceName,sceneName,assName,assetType", dictionary=True)
      else:
        rows = dbconn.execute("select * from assets "+ whereProj +" order by sequenceName,sceneName,assName,assetType", dictionary=True)
    else:
      if(whereDict):
        
        for x in whereDict:
          whereDicts = []
          y = whereDict[x].split(",")
          for z in y:
            if(x == "assName"):
              if(z):
                whereDicts.append(x +" like '%"+ z +"%'")
            elif(x == "tags"):
              if(z):
                whereDicts.append(x +" like '%"+ z +"%'")
            elif(x == "assignedWorker"):
              if(z):
                whereDicts.append(x +" like '%"+ z +"%'")
            else:
              if(z):
                whereDicts.append(x +"='"+ z +"'")
          whereString.append("("+ " or ".join(whereDicts) +")")
        rows = dbconn.execute("select * from assets "+ whereProj +" and ("+ " and ".join(whereString) +") order by sequenceName,sceneName,assName,assetType limit "+ str(limit), dictionary=True)
      else:
        rows = dbconn.execute("select * from assets "+ whereProj +" order by sequenceName,sceneName,assName,assetType limit "+ str(limit), dictionary=True)
        
    print("in getProjAssesLinked module 2")
    return(rows)
  
  except:
    utilsPipeLogger.debug(str(sys.exc_info()))
    return(0)
  
  
def getLibAsses(projNames,limit=None,whereDict={}):
  dbconn = dbPipe.dbPipe()
  linkedProjects = "default"
  projs = []
  whereProj = ""
  
    
  try:
    if(projNames == "default"):
      linkedProjects = os.environ["rp_proj_linkedProjects"]
    else:
      linkedProjects = projNames
  except:
    utilsPipeLogger.debug(str(sys.exc_info()))
    return(0)
  if(linkedProjects != "default"):
    projs = ["'"+ x +"'" for x in linkedProjects.split(",")]
    print(projs)
    whereProj = " where projName=" + " or projName=".join(projs)
  print("in getProjAssesLinked module 1")
  whereString = []
  try:
    if(not limit):
      if(whereDict):
        for x in whereDict:
          whereDicts = []
          y = whereDict[x].split(",")
          for z in y:
            if(x == "assName"):
              if(z):
                whereDicts.append(x +" like '%"+ z +"%'")
            elif(x == "tags"):
              if(z):
                whereDicts.append(x +" like '%"+ z +"%'")
            elif(x == "assignedWorker"):
              if(z):
                whereDicts.append(x +" like '%"+ z +"%'")
            else:
              if(z):
                whereDicts.append(x +"='"+ z +"'")
          whereString.append("("+ " or ".join(whereDicts) +")")
          
        rows = dbconn.execute("select * from assets "+ whereProj +" and ("+ " and ".join(whereString) +") order by projName,sequenceName,sceneName,assName,assetType", dictionary=True)
      else:
        rows = dbconn.execute("select * from assets "+ whereProj +" order by projName,sequenceName,sceneName,assName,assetType", dictionary=True)
    else:
      if(whereDict):
        
        for x in whereDict:
          whereDicts = []
          y = whereDict[x].split(",")
          for z in y:
            if(x == "assName"):
              if(z):
                whereDicts.append(x +" like '%"+ z +"%'")
            elif(x == "tags"):
              if(z):
                whereDicts.append(x +" like '%"+ z +"%'")
            elif(x == "assignedWorker"):
              if(z):
                whereDicts.append(x +" like '%"+ z +"%'")
            else:
              if(z):
                whereDicts.append(x +"='"+ z +"'")
          whereString.append("("+ " or ".join(whereDicts) +")")
        rows = dbconn.execute("select * from assets "+ whereProj +" and ("+ " and ".join(whereString) +") order by projName,sequenceName,sceneName,assName,assetType limit "+ str(limit), dictionary=True)
      else:
        rows = dbconn.execute("select * from assets "+ whereProj +" order by projName,sequenceName,sceneName,assName,assetType limit "+ str(limit), dictionary=True)
        
    print("in getProjAssesLinked module 2")
    return(rows)
  
  except:
    utilsPipeLogger.debug(str(sys.exc_info()))
    return(0)
  
  
  
  

  
  
  
def getProjAsses(projName,limit=None,whereDict={}):
  dbconn = dbPipe.dbPipe()
  whereString = []
  try:
    if(not limit):
      if(whereDict):
        
        for x in whereDict:
          whereDicts = []
          y = whereDict[x].split(",")
          for z in y:
            if(x == "assName"):
              if(z):
                whereDicts.append(x +" like '%"+ z +"%'")
            elif(x == "tags"):
              if(z):
                whereDicts.append(x +" like '%"+ z +"%'")
            elif(x == "assignedWorker"):
              if(z):
                whereDicts.append(x +" like '%"+ z +"%'")
            else:
              if(z):
                whereDicts.append(x +"='"+ z +"'")
          whereString.append("("+ " or ".join(whereDicts) +")")
          
        rows = dbconn.execute("select * from assets where projName='"+ str(projName) +"' and ("+ " and ".join(whereString) +") order by sequenceName,sceneName,assName,assetType", dictionary=True)
      else:
        rows = dbconn.execute("select * from assets where projName='"+ str(projName) +"' order by sequenceName,sceneName,assName,assetType", dictionary=True)
    else:
      if(whereDict):
        
        for x in whereDict:
          whereDicts = []
          y = whereDict[x].split(",")
          for z in y:
            if(x == "assName"):
              if(z):
                whereDicts.append(x +" like '%"+ z +"%'")
            elif(x == "tags"):
              if(z):
                whereDicts.append(x +" like '%"+ z +"%'")
            elif(x == "assignedWorker"):
              if(z):
                whereDicts.append(x +" like '%"+ z +"%'")
            else:
              if(z):
                whereDicts.append(x +"='"+ z +"'")
          whereString.append("("+ " or ".join(whereDicts) +")")
        rows = dbconn.execute("select * from assets where projName='"+ str(projName) +"' and ("+ " and ".join(whereString) +") order by sequenceName,sceneName,assName,assetType limit "+ str(limit), dictionary=True)
      else:
        rows = dbconn.execute("select * from assets where projName='"+ str(projName) +"' order by sequenceName,sceneName,assName,assetType limit "+ str(limit), dictionary=True)
    return(rows)
  except:
    utilsPipeLogger.debug(str(sys.exc_info()))
    return(0)
  

def getUsers():
  dbconn = dbPipe.dbPipe()
  try:
    rows = dbconn.execute("select * from users order by id", dictionary=True)
    #print([row['id'] for row in rows])
    return([row['id'] for row in rows])
  except:
    utilsPipeLogger.debug(str(sys.exc_info()))
    return(0)
  
def assPathColorCoded(assDetDict):
  assPath = str(assDetDict['projName']) +"#"+ "indigo"
  if(not re.search("^default",str(assDetDict['assetType']))):
    assPath = assPath +":"+ str(assDetDict['assetType']) +"#"+ "saddlebrown"
  if(not re.search("^default",str(assDetDict['sequenceName']))):
    assPath = assPath +":"+ str(assDetDict['sequenceName']) +"#"+ "green"
  if(not re.search("^default",str(assDetDict['sceneName']))):
    assPath = assPath +":"+ str(assDetDict['sceneName']) +"#"+ "olive"
  if(not re.search("^default",str(assDetDict['assName']))):
    assPath = assPath +":"+ str(assDetDict['assName']) +"#"+ "maroon"
  if(not re.search("^default",str(assDetDict['stageType']))):
    assPath = assPath +":"+ str(assDetDict['stageType']) +"#"+ "dimgray"
  if(not re.search("^default",str(assDetDict['nodeType']))):
    assPath = assPath +":"+ str(assDetDict['nodeType']) +"#"+ "blue"
  if(not re.search("^default",str(assDetDict['fileType']))):
    assPath = assPath +":"+ str(assDetDict['fileType']) +"#"+ "darkviolet"
  return(assPath)

def assRegister(assDetDict):
  assPath = str(assDetDict['projName'])
  assId = ""
  dirMapsDets = getDirMapsDetails(str(assDetDict['directory']))
  assDetDict['createDate'] = str(MySQLdb.Timestamp.now())
  assDetDict['createdUser']  = os.environ['rbhusPipe_acl_user'].rstrip().lstrip()
  utilsPipeLogger.debug("WTF : "+ str(assDetDict))
  fileName = ""
  if(assDetDict.has_key('assName')):
    if(str(assDetDict['assName']) != "default"):
      fileName = str(assDetDict['assName'])
  if(re.search("^default$",str(assDetDict['assetType']))):
    pass 
  else:
    assTypeDets = getAssTypes(str(assDetDict['assetType']))
    if(assTypeDets):
      for p in assTypeDets['path'].split(":"):
        if(re.search("^\$",str(p))):
          assPath = assPath +":"+ os.environ["rp_"+ str(p).lstrip("$")]
        else:
          assPath = assPath +":"+ p
  if(assPath):
    if(not re.search("^default$",str(assDetDict['sequenceName']))):
      if(not re.search("^default$",str(assDetDict['sceneName']))):
        assPath = assPath +":"+ str(assDetDict['sequenceName']) +":" + str(assDetDict['sceneName'])
        if(fileName):
          fileName = fileName +"_"+ str(assDetDict['sequenceName']) +"_" + str(assDetDict['sceneName'])
        else:
          fileName = str(assDetDict['sequenceName']) +"_" + str(assDetDict['sceneName'])
      else:
        assPath = assPath +":"+ str(assDetDict['sequenceName'])
        if(fileName):
          fileName = fileName +"_"+ str(assDetDict['sequenceName'])
        else:
          fileName = str(assDetDict['sequenceName'])
    #utilsPipeLogger.debug("WTF 001 : "+ str(assPath))
    if(assDetDict.has_key('assName')):
      if(not re.search("^default$",str(assDetDict['assName']))):
        assPath = assPath +":" + str(assDetDict['assName'])
    
    #utilsPipeLogger.debug("WTF 002 : "+ str(assPath))
    if(not re.search("^default$",str(assDetDict['stageType']))):
      assPath = assPath +":" + str(assDetDict['stageType'])
      if(fileName):
        fileName = fileName +"_"+ str(assDetDict['stageType'])
      else:
        fileName = str(assDetDict['stageType'])
    #utilsPipeLogger.debug("WTF 003 : "+ str(assPath))
    if(not re.search("^default$",str(assDetDict['nodeType']))):
      assPath = assPath +":" + str(assDetDict['nodeType'])
      if(fileName):
        fileName = fileName +"_"+ str(assDetDict['nodeType'])
      else:
        fileName = str(assDetDict['nodeType'])
    #utilsPipeLogger.debug("WTF 004 : "+ str(assPath))
    
    
      
    if(not re.search("^default$",str(assDetDict['fileType']))): 
      assPath = assPath +":" + str(assDetDict['fileType'])
    #utilsPipeLogger.debug("WTF 005 : "+ str(assPath))
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
    utilsPipeLogger.debug(assDetDict)
    dbconn = dbPipe.dbPipe()
    try:
      rows = dbconn.execute("insert into assets "+ fs +" values "+ vs)
    except:
      utilsPipeLogger.debug(str(sys.exc_info()))
      return(0)
    try:
      if(sys.platform.find("win") >= 0):
        corePath = dirMapsDets['windowsMapping'] + assPath.replace(":","/")
      else:
        corePath = dirMapsDets['linuxMapping'] + assPath.replace(":","/")
      utilsPipeLogger.debug(corePath)
      try:
        os.makedirs(corePath,0775)
      except:
        utilsPipeLogger.debug(str(sys.exc_info()))
      templateFile = getTemplatePath(assDetDict)
      if(templateFile):
        if(not os.path.exists(corePath.rstrip("/") +"/"+ fileName +"."+ templateFile.split(".")[-1])):
          shutil.copyfile(templateFile,corePath.rstrip("/") +"/"+ fileName +"."+ templateFile.split(".")[-1])
          utilsPipeLogger.debug(templateFile +" : "+ corePath.rstrip("/") +"/"+ fileName +"."+ templateFile.split(".")[-1])
    except:
      utilsPipeLogger.debug(str(sys.exc_info()))
      return(0)
    return(assDetDict['assetId'])
  else:
    return(0)
    
    
def getAssPath(assDetDictTemp = {}):
  assDetDict = copy.copy(assDetDictTemp)
  if(not assDetDict):
    return(0)
  assPath = str(assDetDict['projName'])
  assId = ""
  dirMapsDets = getDirMapsDetails(str(assDetDict['directory']))
  utilsPipeLogger.debug("WTF asspathtemp : "+ str(assDetDict))
  fileName = ""
  if(assDetDict.has_key('assName')):
    if(str(assDetDict['assName']) != "default"):
      fileName = str(assDetDict['assName'])
  if(re.search("^default$",str(assDetDict['assetType']))):
    pass 
  else:
    assTypeDets = getAssTypes(str(assDetDict['assetType']))
    if(assTypeDets):
      for p in assTypeDets['path'].split(":"):
        if(re.search("^\$",str(p))):
          assPath = assPath +":"+ os.environ["rp_"+ str(p).lstrip("$")]
        else:
          assPath = assPath +":"+ p
  if(assPath):
    if(not re.search("^default$",str(assDetDict['sequenceName']))):
      if(not re.search("^default$",str(assDetDict['sceneName']))):
        assPath = assPath +":"+ str(assDetDict['sequenceName']) +":" + str(assDetDict['sceneName'])
        if(fileName):
          fileName = fileName +"_"+ str(assDetDict['sequenceName']) +"_" + str(assDetDict['sceneName'])
        else:
          fileName = str(assDetDict['sequenceName']) +"_" + str(assDetDict['sceneName'])
      else:
        assPath = assPath +":"+ str(assDetDict['sequenceName'])
        if(fileName):
          fileName = fileName +"_"+ str(assDetDict['sequenceName'])
        else:
          fileName = str(assDetDict['sequenceName'])
    #utilsPipeLogger.debug("WTF 001 : "+ str(assPath))
    if(assDetDict.has_key('assName')):
      if(not re.search("^default$",str(assDetDict['assName']))):
        assPath = assPath +":" + str(assDetDict['assName'])
    
    #utilsPipeLogger.debug("WTF 002 : "+ str(assPath))
    if(not re.search("^default$",str(assDetDict['stageType']))):
      assPath = assPath +":" + str(assDetDict['stageType'])
      if(fileName):
        fileName = fileName +"_"+ str(assDetDict['stageType'])
      else:
        fileName = str(assDetDict['stageType'])
    #utilsPipeLogger.debug("WTF 003 : "+ str(assPath))
    if(not re.search("^default$",str(assDetDict['nodeType']))):
      assPath = assPath +":" + str(assDetDict['nodeType'])
      if(fileName):
        fileName = fileName +"_"+ str(assDetDict['nodeType'])
      else:
        fileName = str(assDetDict['nodeType'])
    #utilsPipeLogger.debug("WTF 004 : "+ str(assPath))
    
    
      
    if(not re.search("^default$",str(assDetDict['fileType']))): 
      assPath = assPath +":" + str(assDetDict['fileType'])
    #utilsPipeLogger.debug("WTF 005 : "+ str(assPath))
    return(assPath)
  return(0)


def assEdit(asspath="",assid="",assdict={}):
  utilsPipeLogger.debug("editing ass : "+ str(assdict))
  dbvalues = []
  if(assdict):
    for k in assdict:
      dbvalues.append(str(k) +"=\""+ str(assdict[k]) +"\"")
  print(dbvalues)
  if(dbvalues):
    dbconn = dbPipe.dbPipe()
    if(assid):
      try:
        dbconn.execute("update assets set "+ ",".join(dbvalues) +" where assetId=\""+ str(assid) +"\"")
        utilsPipeLogger.debug("update assets set "+ ",".join(dbvalues) +" where assetId=\""+ str(assid) +"\"")
      except:
        utilsPipeLogger.debug(str(sys.exc_info()))
        return(0)
    elif(asspath):
      try:
        dbconn.execute("update assets set "+ ",".join(dbvalues) +" where path=\""+ str(asspath) +"\"")
        utilsPipeLogger.debug("update assets set "+ ",".join(dbvalues) +" where path=\""+ str(asspath) +"\"")
      except:
        utilsPipeLogger.debug(str(sys.exc_info()))
        return(0)
    return(1)
  return(0)
    
    
            
    
    
  
def assDetails(assDetDict={},assId=0):
  pass

def assOpen(assId):
  pass

def assLinks(assId):
  pass

def assLinkedTo(assId):
  pass

def getTemplatePath(assdetsTemp = {}):
  assdets = copy.copy(assdetsTemp)
  filetypedets = {}
  tempMain = ""
  direcs = {}
  dirs = getDirMaps()
  
  for x in range(0,len(dirs)):
    if(dirs[x]):
      direcs[dirs[x]['directory']] = 1
  for y in direcs:
    print(y)
  assdets['assName'] = "default"
  assdets['assetType'] = "template"
  assPathTemp = getAssPath(assdets)
  assdetails = getAssDetails(assPath = assPathTemp)
  print(assPathTemp)
  
  if(not assdetails):
    assdets['sceneName'] = "default"
  assPathTemp = getAssPath(assdets)
  assdetails = getAssDetails(assPath = assPathTemp)
  print(assPathTemp)
  
  if(not assdetails):
    assdets['sequenceName'] = "default"
  assPathTemp = getAssPath(assdets)
  assdetails = getAssDetails(assPath = assPathTemp)
  print(assPathTemp)
  
  if(not assdetails):
    assdets['stageType'] = "default"
  assPathTemp = getAssPath(assdets)
  assdetails = getAssDetails(assPath = assPathTemp)
  print(assPathTemp)
  
  if(not assdetails):
    assdets['nodeType'] = "default"
  assPathTemp = getAssPath(assdets)
  assdetails = getAssDetails(assPath = assPathTemp)
  print(assPathTemp)
  
  if(assdetails):
    assPathTemp = assdetails['path']
    assPathAbs = getAbsPath(assPathTemp)
    print(assPathAbs)
    if(os.path.exists(assPathAbs)):
      filetypedets = getFileTypes(assdets['fileType'])
      filename = assPathAbs+ "/template." + filetypedets['extension'].split(",")[0]
      print(filename)
      return(filename)
  return(0)
      
        
    
def openAssetCmd(assdets ={},filename = None):
  dirmapdets = getDirMapsDetails(assdets['directory'])
  filetypedets = None
  runCmd = None
  binPaths = None
  binMain = None
  dirs = []
  exeAss = None
  pathAss = None
  runProc = None
  if(sys.platform.find("win") >= 0):
    binMain = dirmapdets['windowsMapping'] +"/"+ assdets['projName'] +"/share/bin"
    exeAss = "windowsCmd"
    pathAss = "windowsPath"
  elif(sys.platform.find("linux") >= 0):
    binMain = dirmapdets['linuxMapping'] +"/"+ assdets['projName'] +"/share/bin"
    exeAss = "linuxCmd"
    pathAss = "linuxPath"
  dirs.append(binMain)
  
  if(assdets['fileType'] != "default"):
    filetypedets = getFileTypes(assdets['fileType'])
    binDir = binMain +"/"+ assdets['fileType']
    validExtenstions = filetypedets['extension'].split(",")
    fileExt = filename.split(".")[-1]
    if(fileExt not in validExtenstions):
      return(0)
    runCmd = binDir +"/"+ filetypedets[exeAss]
    if(os.path.exists(runCmd)):
      runProc = runCmd +" "+ filename
      print(runProc)
      return(runProc)
    else:
      binPaths = filetypedets[pathAss].split(",")
      for x in reversed(binPaths):
        print(str(x))
        if(str(x) != "default"):
          
          absBinPath = getAbsPath(x)
          if(absBinPath):
            runCmd = absBinPath +"/"+ filetypedets[exeAss]
            if(os.path.exists(runCmd)):
              runProc = runCmd +" "+ filename
              print(runProc)
              return(runProc)
        else:
          return("\""+ filetypedets[exeAss] +"\" "+ filename)
  else:
    return(0)
    
    
  

def assDelete(assId=None,assPath=None):
  
  dbconn = dbPipe.dbPipe()
  if(assId):
    assdets = getAssDetails(assId=str(assId))
    projDets = getProjDetails(os.environ["rp_proj_projName"])
    if(os.environ['rbhusPipe_acl_user'] not in projDets['admins'].split(",") and os.environ['rbhusPipe_acl_user'] not in assdets['createdUser'].split(",")):
      return(0)
    dirMapsDets = getDirMapsDetails(assdets['directory'])
    try:
      if(sys.platform.find("win") >= 0):
        corePath = dirMapsDets['windowsMapping'] + assdets['path'].replace(":","/")
        os.system("rmdir "+ str() +" /s /q")
      else:
        corePath = dirMapsDets['linuxMapping'] + assdets['path'].replace(":","/")
        os.system("rm -frv "+ str(corePath))
      utilsPipeLogger.debug(corePath)
    except:
      utilsPipeLogger.debug(str(sys.exc_info()))
      return(0)
    try:
      dbconn.execute("delete from assets where assetId='"+ str(assId) +"'")
      utilsPipeLogger.debug("deleting asset assetId = "+ str(assId) +" : done")
    except:
      utilsPipeLogger.debug("deleting asset assetId = "+ str(assId) +" : failed")
  elif(assPath):
    assdets = getAssDetails(assPath=str(assPath))
    dirMapsDets = getDirMapsDetails(assdets['directory'])
    try:
      if(sys.platform.find("win") >= 0):
        corePath = dirMapsDets['windowsMapping'] + assdets['path'].replace(":","/")
        #os.system("rmdir "+ str() +" /s /q")
      else:
        corePath = dirMapsDets['linuxMapping'] + assdets['path'].replace(":","/")
        #os.system("rm -frv "+ str(corePath))
      utilsPipeLogger.debug(corePath)
    except:
      utilsPipeLogger.debug(str(sys.exc_info()))
      return(0)
    try:
      dbconn.execute("delete from assets where path='"+ str(assPath) +"'")
      utilsPipeLogger.debug("deleting asset path = "+ str(assPath) +" : done")
    except:
      utilsPipeLogger.debug("deleting asset path = "+ str(assPath) +" : failed")
    
  
  
    
