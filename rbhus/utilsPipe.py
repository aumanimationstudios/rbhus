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
import debug

progPath =  sys.argv[0].split(os.sep)
if(len(progPath) > 1):
  pwd = os.sep.join(progPath[0:-1])
  cwd = os.path.abspath(pwd)
  debug.info("utilsPipe 1: "+ str(cwd))
else:
  cwd = os.path.abspath(os.getcwd())


etcpathtmp = cwd.split(os.sep)[0:-2]
etcpathtmp.append("rbhus")
etcpathtmp.append("etc")
etcpath = os.sep.join(etcpathtmp)
debug.info("utilsPipe 1: "+ str(etcpath))


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


# LOG_FILENAME = logging.FileHandler(tempDir + os.sep +"rbhusPipe_utilsPipe_module_"+ username +"_"+ str(hostname) +".log")
#   #LOG_FILENAME = logging.FileHandler('z:/pythonTestWindoze.DONOTDELETE/clientLogs/rbhusDb_'+ hostname +'.log')
#
# #LOG_FILENAME = logging.FileHandler('/var/log/rbhusDb_module.log')
# debug = logging.getLogger("debug")
# debug.setLevel(logging.DEBUG)
#
#
# #ROTATE_FILENAME = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=104857600, backupCount=3)
# BASIC_FORMAT = logging.Formatter("%(asctime)s - %(funcName)s - %(levelname)s - %(message)s")
# LOG_FILENAME.setFormatter(BASIC_FORMAT)
# debug.addHandler(LOG_FILENAME)




def getDirMaps():
  dbconn = dbPipe.dbPipe()
  try:
    rows = dbconn.execute("SELECT * FROM dirMaps", dictionary=True)
    return(rows)
  except:
    debug.debug(str(sys.exc_info()))
    return(0)


def getTags(projName="",assPath="",assId=""):
  dbconn = dbPipe.dbPipe()
  if(projName):
    try:
      rows = dbconn.execute("SELECT tags FROM assets", dictionary=True)
      if(rows):
        #debug.info(rows)
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
      debug.debug(str(sys.exc_info()))
      return(0)
  return(0)




def getDirMapsDetails(directory):
  dbconn = dbPipe.dbPipe()
  try:
    rows = dbconn.execute("SELECT * FROM dirMaps where directory='"+ str(directory) +"'", dictionary=True)
  except:
    debug.debug(str(sys.exc_info()))
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
      rows = dbconn.execute("SELECT * FROM projTypes where type='"+ str(ptype) +"'", dictionary=True)
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
    debug.debug(str(sys.exc_info()))
    return(0)


def getStageTypes(stype=None):
  dbconn = dbPipe.dbPipe()
  try:
    if(stype):
      rows = dbconn.execute("SELECT * FROM stageTypes where type='"+ str(stype) +"'", dictionary=True)
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
    debug.debug(str(sys.exc_info()))
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
    debug.debug(str(sys.exc_info()))
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
    debug.debug(str(sys.exc_info()))
    return(0)


def getAssTypes(atype=None, status=constantsPipe.typesActive):
  dbconn = dbPipe.dbPipe()
  try:
    if(atype):
      rows = dbconn.execute("SELECT * FROM assetTypes where type=\"" + str(atype)+ "\"", dictionary=True)
      if(rows):
        return(rows[0])
      else:
        return(0)
    else:
      if(status != constantsPipe.typesAll):
        rows = dbconn.execute("SELECT * FROM assetTypes where status=\""+ str(status) +"\" order by type", dictionary=True)
      else:
        rows = dbconn.execute("SELECT * FROM assetTypes order by type", dictionary=True)
      if(rows):
        return(rows)
      else:
        return(0)
  except:
    debug.debug(str(sys.exc_info()))
    return(0)


def importAssets(toProject, assetPath, toAssetPath='default', getVersions=True,force=False):
  assDets = getAssDetails(assPath=assetPath)
  origAssPath = getAbsPath(assetPath)
  toAsset = None
  if(toAssetPath != 'default'):
    toAsset = getAssDetails(assPath=toAssetPath)
    if(getVersions):
      toAsset['versioning'] = assDets['versioning']

  else:
    newAsset = copy.copy(assDets)
    newAsset['projName'] = toProject
    newAsset['assignedWorker'] = os.environ['rbhusPipe_acl_user']
    newAsset['reviewUser'] = os.environ['rbhusPipe_acl_user']
    newAsset['importedFrom'] = assDets['projName']

    newAssId = assRegister(newAsset,copyFromTemplate=False)
    if(newAssId):
      toAsset = getAssDetails(assId=newAssId)
    else:
      if(force):
        newAssPath = getAssPath(newAsset)
        toAsset = getAssDetails(assPath=newAssPath)
      else:
        return(4)


  if(toAsset):
    if (not isAssAssigned(toAsset)):
      return (3)
    newAssPath = getAbsPath(toAsset['path'])
    if((toAsset['sequenceName'] != "default" or toAsset['sceneName'] != "default") and toAssetPath == 'default'):
      seqScnDict = {}
      seqScnDict['sequenceName'] = newAsset['sequenceName']
      seqScnDict['projName'] = toProject
      seqScnDict['sceneName'] = newAsset['sceneName']
      seqScnDict['createdUser'] = os.environ['rbhusPipe_acl_user']
      setupSequenceScene(seqScnDict)

    debug.info(newAssPath)
    debug.info(origAssPath)
    if(sys.platform.lower().find("linux") >= 0):
      if(getVersions):
        os.system("rsync -av "+ origAssPath +"/ "+ newAssPath +"/")
      else:
        os.system("rsync -av " + origAssPath + "/ " + newAssPath + "/ --exclude=.hg")
    return(1)
  else:
    return(0)




def getSequenceScenes(proj,seq=None,sce=None):
  dbconn = dbPipe.dbPipe()
  try:
    if(proj and seq and (not sce)):
      rows = dbconn.execute("SELECT * FROM sequenceScenes where projName='"+ str(proj) +"' and sequenceName='"+ str(seq) +"' order by sceneName", dictionary=True)
    elif(proj and seq and sce):
      rows = dbconn.execute("SELECT * FROM sequenceScenes where projName='"+ str(proj) +"' and sequenceName='"+ str(seq) +"' and sceneName='"+ str(sce) +"'", dictionary=True)
    else:
      rows = dbconn.execute("SELECT * FROM sequenceScenes where projName='"+ str(proj) +"' order by sequenceName,sceneName", dictionary=True)
    if(rows):
      return(rows)
    else:
      return(0)
  except:
    debug.debug(str(sys.exc_info()))
    return(0)

def updateAssModifies(assId,notes):
  username = os.environ['rbhusPipe_acl_user']
  dbconn = dbPipe.dbPipe()
  try:
    dbconn.execute("insert into assetModifies (assetId,username,notes,datetime) values ('"+ assId +"','"+ username +"','"+ notes +"', now())")
  except:
    debug.error(sys.exc_info())




def getDefaults(table):
  dbconn = dbPipe.dbPipe()
  try:
    rows = dbconn.execute("desc "+ str(table),dictionary=True)
    taskFieldss = {}
    for row in rows:
      taskFieldss[row['Field']] = row['Default']
    return(taskFieldss)
  except:
    debug.debug(str(sys.exc_info()))
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
    debug.debug(str(sys.exc_info()))
    # easy to search like - if admin in getAdmins():
    return(adminUsers)


# createdUser should come from an env variable set by the authPipe module
def createProj(projType,projName,directory,admins,rbhusRenderIntegration,rbhusRenderServer,aclUser,aclGroup,dueDate,description,linkedProjs="default"):
  if(os.environ['rbhusPipe_acl_user'] not in getAdmins()):
    debug.debug("User not allowed to create projects")
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
  projDets['linkedProjects'] = linkedProjs

  servSoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:
    servSoc.settimeout(15)
    servSoc.connect((constantsPipe.projInitServer,constantsPipe.projInitPort))
  except:
    debug.debug("utilsPipe createProj : "+ str(sys.exc_info()))
    return(0)

  servSoc.send(pickle.dumps(projDets))
  servSoc.close()
  return(1)


#always called by the server
def setupProj(projType,projName,directory,admins,rbhusRenderIntegration,rbhusRenderServer,aclUser,aclGroup,createdUser,dueDate,description):
  if (os.environ['rbhusPipe_acl_user'] not in getAdmins()):
    debug.info("User not allowed to create projects. Please ask the pipe admin to create a project for you")
    return (0)
  dbconn = dbPipe.dbPipe()
  pDefs = getDefaults("proj")
  pTypes = getProjTypes()
  cScript = ""
  for pT in pTypes:
    if(pT['type'] == projType):
      cScript = pT['scriptDir']

  os.environ['rp_proj_projName'] = str(projName).rstrip().lstrip()
  os.environ['rp_proj_projType'] = str(projType).rstrip().lstrip()
  os.environ['rp_proj_directory'] = str(directory).rstrip().lstrip()
  os.environ['rp_proj_admins'] = str(admins) if(admins) else pDefs['admins']
  os.environ['rp_proj_rbhusRenderIntegration'] = str(rbhusRenderIntegration).rstrip().lstrip()
  os.environ['rp_proj_rbhusRenderServer'] = str(rbhusRenderServer).rstrip().lstrip()
  os.environ['rp_proj_description'] = str(description).rstrip().lstrip()
  os.environ['rp_proj_aclUser'] = str(aclUser).rstrip().lstrip()
  os.environ['rp_proj_aclGroup'] = str(aclGroup).rstrip().lstrip()
  os.environ['rp_proj_dueDate'] = str(dueDate).rstrip().lstrip()
  os.environ['rp_proj_createdUser'] = str(createdUser).rstrip().lstrip()
  standardAsses = getProjAsses("standard")
  exportDirMaps(directory)
  exportProjTypes(projType)
  debug.debug(description)
  debug.debug(projName)
  debug.debug(cScript)
  try:
    dbconn.execute("insert into proj (projName,directory,admins,projType,rbhusRenderIntegration,rbhusRenderServer,aclUser,aclGroup,createdUser,dueDate,createDate,description) \
                    values ('"+ str(projName).rstrip().lstrip() +"', \
                    '"+ str(directory).rstrip().lstrip() +"', \
                    '"+ str(admins).rstrip().lstrip() +"', \
                    '"+ str(projType).rstrip().lstrip() +"', \
                    '"+ str(rbhusRenderIntegration).rstrip().lstrip() +"', \
                    '"+ str(rbhusRenderServer).rstrip().lstrip() +"', \
                    '"+ str(aclUser).rstrip().lstrip() +"', \
                    '"+ str(aclGroup).rstrip().lstrip() +"', \
                    '"+ str(createdUser).rstrip().lstrip() +"', \
                    '"+ str(dueDate).rstrip().lstrip() +"', \
                    '"+ str(MySQLdb.Timestamp.now()).rstrip().lstrip() +"', \
                    '"+ str(description).rstrip().lstrip() +"')")
  except:
    debug.debug(str(sys.exc_info()))
    return(0)

  seqScnDict = {}
  seqScnDict['sequenceName'] = "default"
  seqScnDict['projName'] = str(projName).rstrip().lstrip()
  seqScnDict['sceneName'] = "default"
  seqScnDict['createdUser'] = str(createdUser).rstrip().lstrip()

  setupSequenceScene(seqScnDict)

  # TODO: remove the below logic . Dont create directories . Project is just an idea in the database without any physical manifestation
  try:
    if(cScript):
      dbconn.execute("update proj set createStatus="+ str(constantsPipe.createStatusRunning).rstrip().lstrip() +" where projName='"+ str(projName).rstrip().lstrip() +"'")
      debug.debug("python -d '"+ str(cScript).rstrip("/") +"/"+ projType +".py'")
      status = os.system("python -d '"+ str(cScript).rstrip("/") +"/"+ projType +".py'")
      if(status != 0):
        dbconn.execute("update proj set createStatus="+ str(constantsPipe.createStatusFailed).rstrip().lstrip() +" where projName='"+ str(projName).rstrip().lstrip() +"'")
      else:
        dbconn.execute("update proj set createStatus="+ str(constantsPipe.createStatusDone).rstrip().lstrip() +" where projName='"+ str(projName).rstrip().lstrip() +"'")
      for standardAss in standardAsses:
        importAssets(str(projName).rstrip().lstrip(),standardAss['path'])
      return(1)
  except:
    debug.debug(str(sys.exc_info()))
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
  exportProj(projName=assDets['projName'])
  exportSeqScn(assDets['projName'], assDets['sequenceName'], assDets['sceneName'])
  return(1)


def exportSeqScn(projName,scq,scn):
  dbconn = dbPipe.dbPipe()
  rows = 0
  try:
    rows = dbconn.execute("select * from sequenceScenes where projName='"+ str(projName) +"' and sequenceName='"+ str(scq) +"' and sceneName='"+ str(scn) +"'",dictionary=True)
  except:
    debug.debug(str(sys.exc_info()))
  if(not isinstance(rows, int)):
    row = rows[0]
    for x in row.keys():
      os.environ['rp_sequenceScenes_'+ str(x).rstrip().lstrip()] = str(row[x])




def exportProj(projName):
  if(projName):
    dets = getProjDetails(projName=projName)
    for x in dets.keys():
      os.environ['rp_proj_'+ str(x)] = str(dets[x])
    exportProjTypes(dets['projType'])
    exportDirMaps(dets['directory'])


#when you give the projName it returns a single dict else it returns an array of dict
def getProjDetails(projName=None,status=None):
  if(projName):
    dbconn = dbPipe.dbPipe()
    try:
      rows = dbconn.execute("select * from proj where projName='"+ str(projName) +"'", dictionary=True)
    except:
      debug.debug(str(sys.exc_info()))
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
        debug.debug(str(sys.exc_info()))
        return(0)
      return(rows)
    else:
      dbconn = dbPipe.dbPipe()
      try:
        rows = dbconn.execute("select * from proj order by projName", dictionary=True)
      except:
        debug.debug(str(sys.exc_info()))
        return(0)
      return(rows)
  return(0)









def setupSequenceScene(seqSceDict):

  projDets = getProjDetails(str(seqSceDict['projName']))
  dirMapsDets = getDirMapsDetails(str(projDets['directory']))
  defaultSeq = {}
  defaultSeq['projName'] = str(seqSceDict['projName']).rstrip().lstrip()
  defaultSeq['sequenceName'] = str(seqSceDict['sequenceName']).rstrip().lstrip()
  defaultSeq['sceneName'] = "default"

  defKeys = defaultSeq.keys()
  defValues = ["'"+ str(defaultSeq[x]).rstrip().lstrip() +"'" for x in defKeys]

  seqKeys = seqSceDict.keys()
  seqValues = ["'"+ str(seqSceDict[x]).rstrip().lstrip() +"'" for x in seqKeys]
  seqKeys.append("createDate")
  seqValues.append("'"+ str(MySQLdb.Timestamp.now()) +"'")


  if(not seqSceDict.has_key("createdUser")):
    try:
      seqValues.append("'"+ os.environ['rbhusPipe_acl_user'] +"'")
      seqKeys.append("createdUser")
    except:
      debug.info("createdUser not given for seq scn")
      return(0)


  try:
    dbconn = dbPipe.dbPipe()
    dbconn.execute("insert into sequenceScenes ("+ ",".join(defKeys) +") \
                    values("+ ",".join(defValues) +")")
  except:
    debug.debug(str(sys.exc_info()))


  try:
    dbconn = dbPipe.dbPipe()
    dbconn.execute("insert into sequenceScenes ("+ ",".join(seqKeys) +") \
                    values("+ ",".join(seqValues) +")")
  except:
    debug.debug(str(sys.exc_info()))
    return(0)




def editSequenceScene(seqSceDict):
  seqSceDictTem = copy.copy(seqSceDict)
  del seqSceDictTem['projName']
  del seqSceDictTem['sequenceName']
  del seqSceDictTem['sceneName']
  dbvalues = []
  if(seqSceDictTem):
    for k in seqSceDictTem:
      dbvalues.append(str(k) +"=\""+ str(seqSceDictTem[k]).rstrip().lstrip() +"\"")
  if(dbvalues):
    dbconn = dbPipe.dbPipe()
    try:
      dbconn.execute("update sequenceScenes set "+ ",".join(dbvalues) +" where sequenceName=\""+ str(seqSceDict['sequenceName']) +"\" and sceneName=\""+ str(seqSceDict['sceneName']) +"\" and projName=\""+ str(seqSceDict['projName']) +"\"")
    except:
      debug.debug(str(sys.exc_info()))
    debug.info(dbvalues)
    return(1)
  else:
    return(0)



def getFieldValue(table,field,fkey,fvalue):
  dbconn = dbPipe.dbPipe()
  try:
    rows = dbconn.execute("select "+ str(field) +" from "+ str(table) +" where "+ str(fkey) +"='"+ str(fvalue) +"'",dictionary=True)
    return(rows)
  except:
    debug.debug(str(sys.exc_info()))
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
  #debug.info("getAbsPath 1: "+ str(projName))


  #debug.info("getAbsPath 2: "+ str(projDets))

  assDets = getAssDetails(assPath=pipePath)
  #debug.info("getAbsPath 3: "+ str(projDets))
  if(assDets):
    projDirMapsDets = getDirMapsDetails(assDets['directory'])
  else:
    projDets = getProjDetails(projName)
    projDirMapsDets = getDirMapsDetails(projDets['directory'])

  #debug.info("getAbsPath 4: "+ str(projDirMapsDets))
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
      debug.debug(str(sys.exc_info()))
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
      debug.debug(str(sys.exc_info()))
      return(0)
    if(rows):
      ret = {}
      fs = rows[0].keys()
      for x in fs:
        ret[x] = rows[0][x]
      return(ret)
    return(0)




def getLibAsses(projNames,limit=None,whereDict={}):
  dbconn = dbPipe.dbPipe()
  linkedProjects = "default"
  projs = []
  whereProj = ""
  whereDictTemp = copy.copy(whereDict)
  whereDictTemp['assetType'] = "library"
  whereDictTemp['status'] = str(constantsPipe.assetStatusActive)
  rows = 0
  try:
    if(projNames == "default"):
      linkedProjects = os.environ["rp_proj_linkedProjects"]
    else:
      linkedProjects = projNames
  except:
    debug.debug(str(sys.exc_info()))
    return(0)
  if(linkedProjects != "default"):
    projs = ["'"+ x +"'" for x in linkedProjects.split(",")]
    debug.info(projs)
    whereProj = " where (projName=" + " or projName=".join(projs) +")"
  debug.info("in getProjAssesLinked module 1 : "+ str(whereProj) )
  whereString = []
  try:
    if(not limit):
      for x in whereDictTemp:
        whereDicts = []
        y = whereDictTemp[x].split(",")
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
      for x in whereDictTemp:
        whereDicts = []
        y = whereDictTemp[x].split(",")
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
    if(rows):
      return(rows)
    else:
      return(0)
  except:
    debug.debug(str(sys.exc_info()))
    return(0)





def getProjAssesForDelete(projName,limit=None,whereDict={}):
  dbconn = dbPipe.dbPipe()
  whereString = []
  whereDictTemp = copy.copy(whereDict)
  whereDictTemp['status'] = str(constantsPipe.assetStatusDelete)
  rows = 0
  try:
    if(not limit):
      for x in whereDictTemp:
        whereDicts = []
        y = whereDictTemp[x].split(",")
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
      for x in whereDictTemp:
        whereDicts = []
        y = whereDictTemp[x].split(",")
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
    if(rows):
      return(rows)
    else:
      return(0)
  except:
    debug.debug(str(sys.exc_info()))
    return(0)



def getProjAsses(projName,limit=None,whereDict={}):
  dbconn = dbPipe.dbPipe()
  whereString = []
  whereDictTemp = copy.copy(whereDict)
  whereDictTemp['status'] = str(constantsPipe.assetStatusActive)
  rows = 0
  try:
    if(not limit):
      for x in whereDictTemp:
        whereDicts = []
        y = whereDictTemp[x].split(",")
        for z in y:
          if(x == "assName" or x == "tags" or x == "assignedWorker" or x == "path"):
            if(z):
              whereDicts.append("LOWER("+ x +") like '%"+ str(z).lower() +"%'")
          else:
            if(z):
              whereDicts.append(x +"='"+ z +"'")
        whereString.append("("+ " or ".join(whereDicts) +")")
      debug.debug(whereString)
      rows = dbconn.execute("select * from assets where projName='"+ str(projName) +"' and ("+ " and ".join(whereString) +") order by sequenceName,sceneName,assName,assetType", dictionary=True)
    else:
      for x in whereDictTemp:
        whereDicts = []
        y = whereDictTemp[x].split(",")
        for z in y:
          if (x == "assName" or x == "tags" or x == "assignedWorker" or x == "path"):
            if (z):
              whereDicts.append("LOWER(" + x + ") like '%" + str(z).lower() + "%'")
          else:
            if(z):
              whereDicts.append(x +"='"+ z +"'")
        whereString.append("("+ " or ".join(whereDicts) +")")
      debug.debug(whereString)
      rows = dbconn.execute("select * from assets where projName='"+ str(projName) +"' and ("+ " and ".join(whereString) +") order by sequenceName,sceneName,assName,assetType limit "+ str(limit), dictionary=True)
    if(rows):
      return(rows)
    else:
      return(0)
  except:
    debug.debug(str(sys.exc_info()))
    return(0)


def getUsers():
  dbconn = dbPipe.dbPipe()
  try:
    rows = dbconn.execute("select * from users order by id", dictionary=True)
    #debug.info([row['id'] for row in rows])
    return([str(row['id']).rstrip().lstrip() for row in rows])
  except:
    debug.debug(str(sys.exc_info()))
    return(0)

def getStageAdmins(stageType):
  dbconn = dbPipe.dbPipe()
  try:
    rows = dbconn.execute("select admins from stageTypes where type = '"+ str(stageType) +"'", dictionary=True)
    return([x.rstrip().lstrip() for x in rows[-1]['admins'].split(",")])
  except:
    debug.debug(str(sys.exc_info()))
    return(0)



def assPathColorCoded(assDetDict):
  assPath = str(assDetDict['projName']) +"#"+ "indigo"
  if(not re.search("^default",str(assDetDict['assetType']))):
    assPath = assPath +":"+ str(assDetDict['assetType']) +"#"+ "saddlebrown"
  if(not re.search("^default",str(assDetDict['sequenceName']))):
    assPath = assPath +":"+ str(assDetDict['sequenceName']) +"#"+ "navy"
  if(not re.search("^default",str(assDetDict['sceneName']))):
    assPath = assPath +":"+ str(assDetDict['sceneName']) +"#"+ "Indigo"
  if(not re.search("^default",str(assDetDict['assName']))):
    assPath = assPath +":"+ str(assDetDict['assName']) +"#"+ "crimson"
  if(not re.search("^default",str(assDetDict['stageType']))):
    assPath = assPath +":"+ str(assDetDict['stageType']) +"#"+ "Teal"
  if(not re.search("^default",str(assDetDict['nodeType']))):
    assPath = assPath +":"+ str(assDetDict['nodeType']) +"#"+ "Olive"
  if(not re.search("^default",str(assDetDict['fileType']))):
    assPath = assPath +":"+ str(assDetDict['fileType']) +"#"+ "darkviolet"
  return(assPath)




def getBestDir(assDetDict):
  pass



def assRegister(assDetDict,copyFromTemplate=True):
  assPath = getAssPath(assDetDict)
  #assPath = str(assDetDict['projName'])
  assId = ""
  dirMapsDets = getDirMapsDetails(str(assDetDict['directory']))
  assDetDict['createDate'] = str(MySQLdb.Timestamp.now())
  assDetDict['createdUser']  = os.environ['rbhusPipe_acl_user'].rstrip().lstrip()
  fileName = getAssFileName(assDetDict)
  assId = hashlib.sha256(assPath).hexdigest()
  assDetDict['assetId'] = assId
  assDetDict['path'] = assPath
  fieldsA = []
  valuesA = []
  for x in assDetDict.keys():
    fieldsA.append(str(x))
    valuesA.append("'"+ str(assDetDict[x]).rstrip().lstrip() +"'")
  fs = "("+ ",".join(fieldsA) +")"
  vs = "("+ ",".join(valuesA) +")"
  debug.debug(assDetDict)
  dbconn = dbPipe.dbPipe()
  try:
    rows = dbconn.execute("insert into assets "+ fs +" values "+ vs)
  except:
    debug.debug(str(sys.exc_info()))
    return(0)
  try:

    if(sys.platform.find("win") >= 0):
      corePath = dirMapsDets['windowsMapping'] + assPath.replace(":","/")
    else:
      corePath = dirMapsDets['linuxMapping'] + assPath.replace(":","/")
    debug.debug(corePath)
    try:
      os.makedirs(corePath,0775)
    except:
      debug.debug(str(sys.exc_info()))
    if(copyFromTemplate):
      if(assDetDict['assetType'].rstrip().lstrip() != "output" and assDetDict['assetType'].rstrip().lstrip() != "share" and assDetDict['assetType'].rstrip().lstrip() != "template"):
        setAssTemplate(assDetDict)
  except:
    debug.debug(str(sys.exc_info()))
    return(0)
  return(assDetDict['assetId'])
  #else:
    #return(0)

def getStageDefaultDirectories(assDetDict):
  pass

def getNodeDefaultDirectories(assDetDict):
  pass

def getFileTypeDefaultDirectories(assDetDict):
  pass


def getDistinctAssNames(projName):
  dbconn = dbPipe.dbPipe()
  assnames = []
  try:
    rows = dbconn.execute("select distinct(assName) from assets where projName=\"{0}\"".format(projName),dictionary=True)
  except:
    debug.warn(sys.exc_info())
  debug.info(rows)
  if (isinstance(rows, int)):
    return (0)
  else:
    for x in rows:
      assnames.append(x['assName'])
    return(assnames)



def setAssTemplate(assDetDict,hard=False):
  templateFile = getTemplatePath(assDetDict)
  assPath = getAssPath(assDetDict)
  dirMapsDets = getDirMapsDetails(str(assDetDict['directory']))
  fileName = getAssFileName(assDetDict)
  if(sys.platform.find("win") >= 0):
    corePath = dirMapsDets['windowsMapping'] + assPath.replace(":","/")
  else:
    corePath = dirMapsDets['linuxMapping'] + assPath.replace(":","/")

  if(templateFile):
    if(hard):
      debug.debug("recopied template file")
      shutil.copyfile(templateFile, corePath.rstrip("/") + "/" + fileName + "." + templateFile.split(".")[-1])
    else:
      if(not os.path.exists(corePath.rstrip("/") +"/"+ fileName +"."+ templateFile.split(".")[-1])):
        debug.debug("recopied template file")
        shutil.copyfile(templateFile,corePath.rstrip("/") +"/"+ fileName +"."+ templateFile.split(".")[-1])
      else:
        debug.debug("file already exits. not copying template")


def setTemplateAss(assDetDict):
  templateFile = getTemplatePath(assDetDict)
  assPath = getAssPath(assDetDict)
  dirMapsDets = getDirMapsDetails(str(assDetDict['directory']))
  fileName = getAssFileName(assDetDict)

  if(sys.platform.find("win") >= 0):
    corePath = dirMapsDets['windowsMapping'] + assPath.replace(":","/")
  else:
    corePath = dirMapsDets['linuxMapping'] + assPath.replace(":","/")

  fullFileName = corePath.rstrip("/") + "/" + fileName + "." + templateFile.split(".")[-1]
  debug.info(fullFileName)
  debug.info(templateFile)
  if(os.path.exists(fullFileName)):
    try:
      shutil.copyfile(fullFileName,templateFile)
    except:
      debug.error(sys.exc_info())




def getAssFileName(assDetDict):
  fileName = ""
  if(assDetDict.has_key('assName')):
    if(str(assDetDict['assName']) != "default"):
      fileName = str(assDetDict['assName'])
  if(not re.search("^default$",str(assDetDict['sequenceName']))):
    if(not re.search("^default$",str(assDetDict['sceneName']))):
      if(fileName):
        fileName = fileName +"_"+ str(assDetDict['sequenceName']) +"_" + str(assDetDict['sceneName'])
      else:
        fileName = str(assDetDict['sequenceName']) +"_" + str(assDetDict['sceneName'])
    else:
      if(fileName):
        fileName = fileName +"_"+ str(assDetDict['sequenceName'])
      else:
        fileName = str(assDetDict['sequenceName'])
  if(not re.search("^default$",str(assDetDict['stageType']))):
    if(fileName):
      fileName = fileName +"_"+ str(assDetDict['stageType'])
    else:
      fileName = str(assDetDict['stageType'])
  if(not re.search("^default$",str(assDetDict['nodeType']))):
    if(fileName):
      fileName = fileName +"_"+ str(assDetDict['nodeType'])
    else:
      fileName = str(assDetDict['nodeType'])
  return(fileName)



def getAssPath(assDetDictTemp = {}):
  assDetDict = copy.copy(assDetDictTemp)
  if(not assDetDict):
    return(0)
  assPath = str(assDetDict['projName'])
  debug.debug(assDetDict['assetType'])
  if(re.search("^default$",str(assDetDict['assetType']))):
    debug.info("passing : "+ assDetDict['assetType'])
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
      else:
        assPath = assPath +":"+ str(assDetDict['sequenceName'])
    if(assDetDict.has_key('assName')):
      if(not re.search("^default$",str(assDetDict['assName']))):
        assPath = assPath +":" + str(assDetDict['assName'])

    if(not re.search("^default$",str(assDetDict['stageType']))):
      assPath = assPath +":" + str(assDetDict['stageType'])
    if(not re.search("^default$",str(assDetDict['nodeType']))):
      assPath = assPath +":" + str(assDetDict['nodeType'])
    if(not re.search("^default$",str(assDetDict['fileType']))):
      assPath = assPath +":" + str(assDetDict['fileType'])
    return(assPath)
  return(0)


def assEdit(asspath="",assid="",assdict={}):
  debug.debug("editing ass : "+ str(assdict))
  dbvalues = []
  if(assdict):
    for k in assdict:
      dbvalues.append(str(k) +"=\""+ str(assdict[k]).rstrip().lstrip() +"\"")
  debug.info(dbvalues)
  if(dbvalues):
    dbconn = dbPipe.dbPipe()
    if(assid):
      try:
        dbconn.execute("update assets set "+ ",".join(dbvalues) +" where assetId=\""+ str(assid) +"\"")
        debug.debug("update assets set "+ ",".join(dbvalues) +" where assetId=\""+ str(assid) +"\"")
      except:
        debug.debug(str(sys.exc_info()))
        return(0)
    elif(asspath):
      try:
        dbconn.execute("update assets set "+ ",".join(dbvalues) +" where path=\""+ str(asspath) +"\"")
        debug.debug("update assets set "+ ",".join(dbvalues) +" where path=\""+ str(asspath) +"\"")
      except:
        debug.debug(str(sys.exc_info()))
        return(0)
    return(1)
  return(0)


def reviewAdd(assdict={}):
  if(not assdict.has_key("referenceFolder")):
    assdict["referenceFolder"] = ""
  dbconn = dbPipe.dbPipe()
  try:
    dbconn.execute("insert into assetReviews (assetId,reviewVersion,message,username,referenceFolder,datetime) value (\""\
      + str(assdict['assetId']).rstrip().lstrip() +"\",\""\
      + str(assdict['reviewVersion']).rstrip().lstrip() +"\",\""\
      + str(assdict['message']).rstrip().lstrip() +"\",\""\
      + str(assdict['username']).rstrip().lstrip() +"\",\""\
      + str(assdict['referenceFolder']).rstrip().lstrip() +"\",\""\
      + str(MySQLdb.Timestamp.now()).rstrip().lstrip() +"\")")
  except:
    debug.debug(str(sys.exc_info()))

def notesAdd(assdict={}):
  dbconn = dbPipe.dbPipe()
  try:
    dbconn.execute("insert into assetNotes (assetId,notes,username,datetime) value (\""\
      + str(assdict['assetId']).rstrip().lstrip() +"\",\""\
      + str(assdict['notes']).rstrip().lstrip() +"\",\""\
      + str(assdict['username']).rstrip().lstrip() +"\",\""\
      + str(MySQLdb.Timestamp.now()).rstrip().lstrip() +"\")")
  except:
    debug.debug(str(sys.exc_info()))


def reviewVersion(asspath,version):
  dbconn = dbPipe.dbPipe()
  try:
    dbconn.execute("update assets set reviewVersion = \""+ str(version) +"\",reviewStatus=\""+ str(constantsPipe.reviewStatusInProgress) +"\" where path = \""+ str(asspath) +"\"")
  except:
    debug.debug(str(sys.exc_info()))



def reviewEdit(assdict={}):
  assDets = copy.copy(assdict)
  debug.debug("editing ass review : "+ str(assdict))
  dbvalues = []
  assid = ""
  if(assdict):
    assid = assDets['assetId']
    del(assDets['assetId'])
    for k in assDets:
      dbvalues.append(str(k) +"=\""+ str(assDets[k]).rstrip().lstrip() +"\"")
  debug.info(dbvalues)
  if(dbvalues):
    dbconn = dbPipe.dbPipe()
    if(assid):
      try:
        dbconn.execute("update assetReviews set "+ ",".join(dbvalues) +" where assetId=\""+ str(assid) +"\"")
        debug.debug("update assetReviews set "+ ",".join(dbvalues) +" where assetId=\""+ str(assid) +"\"")
      except:
        debug.debug(str(sys.exc_info()))
        return(0)
    return(1)
  return(0)

def reviewDetails(assId = 0,revCount=0):
  if(assId):
    dbconn = dbPipe.dbPipe()
    if(revCount == 0):
      try:
        rows = dbconn.execute("select * from assetReviews where assetId='"+ str(assId) +"' order by reviewCount", dictionary=True)
      except:
        debug.debug(str(sys.exc_info()))
        return(0)
      if(isinstance(rows, int)):
        return(0)
      else:
        return(rows)
    else:
      try:
        rows = dbconn.execute("select * from assetReviews where assetId='"+ str(assId) +"' and reviewCount='"+ str(revCount) +"'", dictionary=True)
      except:
        debug.debug(str(sys.exc_info()))
        return(0)
      if(isinstance(rows, int)):
        return(0)
      else:
        return(rows[0])
  else:
    return(0)


def notesDetails(assId = 0):
  if(assId):
    dbconn = dbPipe.dbPipe()
    try:
      rows = dbconn.execute("select * from assetNotes where assetId='"+ str(assId) +"' order by notesCount", dictionary=True)
    except:
      debug.debug(str(sys.exc_info()))
      return(0)
    if(isinstance(rows, int)):
      return(0)
    else:
      return(rows)
  else:
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
  debug.info("in getTemplatePath")
  assdets = copy.copy(assdetsTemp)
  filetypedets = {}
  tempMain = ""
  dirs = getDirMaps()

  assdets['assName'] = "default"
  assdets['assetType'] = "template"
  assPathTemp = getAssPath(assdets)
  assdetails = getAssDetails(assPath = assPathTemp)
  debug.info(assdetails)
  debug.info(assPathTemp)

  if(not assdetails):
    assdets['sceneName'] = "default"
  assPathTemp = getAssPath(assdets)
  assdetails = getAssDetails(assPath = assPathTemp)
  debug.info(assdetails)
  debug.info(assPathTemp)

  if(not assdetails):
    assdets['sequenceName'] = "default"
  assPathTemp = getAssPath(assdets)
  assdetails = getAssDetails(assPath = assPathTemp)
  debug.info(assdetails)
  debug.info(assPathTemp)

  if(not assdetails):
    assdets['nodeType'] = "default"
  assPathTemp = getAssPath(assdets)
  assdetails = getAssDetails(assPath = assPathTemp)
  debug.info(assdetails)
  debug.info(assPathTemp)

  if(not assdetails):
    assdets['stageType'] = "default"
  assPathTemp = getAssPath(assdets)
  assdetails = getAssDetails(assPath = assPathTemp)
  debug.info(assdetails)
  debug.info(assPathTemp)



  if(assdetails):
    assPathTemp = assdetails['path']
    assPathAbs = getAbsPath(assPathTemp)
    debug.info(assPathAbs)
    if(os.path.exists(assPathAbs)):
      filetypedets = getFileTypes(assdets['fileType'])
      filename = assPathAbs+ "/template." + filetypedets['extension'].split(",")[0]
      debug.info(filename)
      return(filename)
  return(0)


def getBinPath(assdetsTemp = {}):
  assdets = copy.copy(assdetsTemp)
  debug.info(assdets)
  filetypedets = getFileTypes(assdets["fileType"])

  if(sys.platform.find("win") >= 0):
    exeAss = "windowsCmd"
    pathAss = "windowsPath"
  elif(sys.platform.find("linux") >= 0):
    exeAss = "linuxCmd"
    pathAss = "linuxPath"

  # assdets['assName'] = "default"
  assdets['assetType'] = "bin"
  assPathTemp = getAssPath(assdets)
  assdetails = getAssDetails(assPath = assPathTemp)
  debug.info(assdetails)
  debug.info(assPathTemp)

  if(not assdetails):
    assdets['sceneName'] = "default"
  assPathTemp = getAssPath(assdets)
  assdetails = getAssDetails(assPath = assPathTemp)
  debug.info(assdetails)
  debug.info(assPathTemp)

  if(not assdetails):
    assdets['sequenceName'] = "default"
  assPathTemp = getAssPath(assdets)
  assdetails = getAssDetails(assPath = assPathTemp)
  debug.info(assdetails)
  debug.info(assPathTemp)

  if(not assdetails):
    assdets['nodeType'] = "default"
  assPathTemp = getAssPath(assdets)
  assdetails = getAssDetails(assPath = assPathTemp)
  debug.info(assdetails)
  debug.info(assPathTemp)

  if(not assdetails):
    assdets['stageType'] = "default"
  assPathTemp = getAssPath(assdets)
  assdetails = getAssDetails(assPath = assPathTemp)
  debug.info(assdetails)
  debug.info(assPathTemp)


  # If there is no asset , then try the above logic with assName as 'default'
  if (not assdetails):
    assdets = copy.copy(assdetsTemp)
    assdets['assetType'] = "bin"
    assdets['assName'] = "default"
  assPathTemp = getAssPath(assdets)
  assdetails = getAssDetails(assPath=assPathTemp)
  debug.info(assdetails)
  debug.info(assPathTemp)

  if (not assdetails):
    assdets['sceneName'] = "default"
  assPathTemp = getAssPath(assdets)
  assdetails = getAssDetails(assPath=assPathTemp)
  debug.info(assdetails)
  debug.info(assPathTemp)

  if (not assdetails):
    assdets['sequenceName'] = "default"
  assPathTemp = getAssPath(assdets)
  assdetails = getAssDetails(assPath=assPathTemp)
  debug.info(assdetails)
  debug.info(assPathTemp)

  if (not assdetails):
    assdets['nodeType'] = "default"
  assPathTemp = getAssPath(assdets)
  assdetails = getAssDetails(assPath=assPathTemp)
  debug.info(assdetails)
  debug.info(assPathTemp)

  if (not assdetails):
    assdets['stageType'] = "default"
  assPathTemp = getAssPath(assdets)
  assdetails = getAssDetails(assPath=assPathTemp)
  debug.info(assdetails)
  debug.info(assPathTemp)



  if(assdetails):
    assPathTemp = assdetails['path']
    assPathAbs = getAbsPath(assPathTemp)
    debug.info(assPathAbs)
    if(os.path.exists(assPathAbs)):
      filename = os.path.join(assPathAbs,filetypedets[exeAss].split(os.sep)[-1])
      debug.info(filename)
      if(os.path.exists(filename)):
        return(filename)

  return (filetypedets[exeAss])

def openAssetCmd(assdets ={},filename = None):
  binPathExe = getBinPath(assdets)
  debug.info(filename)
  exportAsset(assdets)
  if(assdets['fileType'] != "default"):
    filetypedets = getFileTypes(assdets['fileType'])
    validExtenstions = filetypedets['extension'].split(",")
    fileExt = filename.split(".")[-1]
    if(fileExt not in validExtenstions):
      return(0)
    runCmd = binPathExe
    if(os.path.exists(runCmd)):
      runProc = runCmd +" "+ filename
      debug.info(runProc)
      debug.info(runProc)
      return(runProc)
  else:
    return(0)





def assMarkForDelete(assId=None,assPath=None):
  dbconn = dbPipe.dbPipe()
  if(assId):
    assdets = getAssDetails(assId=str(assId))
  elif(assPath):
    assdets = getAssDetails(assPath=str(assPath))
  else:
    return(0)

  try:
    dbconn.execute("update assets set status="+ str(constantsPipe.assetStatusDelete) +" where path='"+ str(assdets['path']) +"'")
    debug.debug("marked for deletion asset = "+ str(assdets['path']) +" : done")
  except:
    debug.debug("marked for deletion asset = "+ str(assdets['path']) +" : failed")
    return(0)
  return(1)


def assDelete(assId=None,assPath=None,hard=False):
  dbconn = dbPipe.dbPipe()
  if(assId):
    assdets = getAssDetails(assId=str(assId))
  elif(assPath):
    assdets = getAssDetails(assPath=str(assPath))
  else:
    return(0)




  projDets = getProjDetails(os.environ["rp_proj_projName"])
  if(os.environ['rbhusPipe_acl_user'] in projDets['admins'].split(",") or os.environ['rbhusPipe_acl_user'] in assdets['createdUser'].split(",")):
    dirMapsDets = getDirMapsDetails(assdets['directory'])
    if(hard == True):
      try:
        if(sys.platform.find("win") >= 0):
          corePath = dirMapsDets['windowsMapping'] + assdets['path'].replace(":","/")
          os.system("rmdir "+ str() +" /s /q")
        else:
          corePath = dirMapsDets['linuxMapping'] + assdets['path'].replace(":","/")
          os.system("rm -frv "+ str(corePath))
        debug.debug(corePath)
      except:
        debug.debug(str(sys.exc_info()))
    try:
      dbconn.execute("delete from assets where assetId='"+ str(assdets['assetId']) +"'")
      debug.debug("deleting asset assetId = "+ str(assdets['assetId']) +" : done")
    except:
      debug.debug("deleting asset assetId = "+ str(assdets['assetId']) +" : failed")
  else:
    debug.debug("deleting asset assetId = "+ str(assdets['assetId']) +" : permission denied")



def setWorkInProgress(asspath):
  assdets = getAssDetails(assPath=str(asspath))
  if (isProjAdmin(assdets) or isStageAdmin(assdets) or isAssAssigned(assdets)):
    try:
      dbconn = dbPipe.dbPipe()
      dbconn.execute("update assets set progressStatus="+ str(constantsPipe.assetProgressInProgress) +",doneDate = '0000-00-00 00:00:00' where path='"+ str(asspath) +"'")
    except:
      debug.debug(str(sys.exc_info()))
      return(0)
  else:
    debug.warn("user not permitted to set work in progress")
  return(1)



def setWorkDone(asspath):
  assdets = getAssDetails(assPath=str(asspath))

  if(isProjAdmin(assdets) or isStageAdmin(assdets) or isAssAssigned(assdets)):
    try:
      dbconn = dbPipe.dbPipe()
      dbconn.execute("update assets set progressStatus="+ str(constantsPipe.assetProgressDone) +",doneDate='"+ str(MySQLdb.Timestamp.now()).rstrip().lstrip() +"' where path='"+ str(asspath) +"'")
    except:
      debug.debug(str(sys.exc_info()))
      return(0)
  else:
    debug.warn("user not permitted to set work as done")
  return(1)






def isAssCreated(assdets = {}):
  if(os.environ['rbhusPipe_acl_user'] in assdets['createdUser'].split(",")):
    return(True)
  else:
    return(False)




def isAssAssigned(assdets = {}):
  if(os.environ['rbhusPipe_acl_user'] in assdets['assignedWorker'].split(",")):
    return(True)
  else:
    return(False)



def isStageAdmin(assdets = {}):
  if(assdets['stageType'] != "default"):
    stagedets  = getStageTypes(assdets['stageType'])
    if(os.environ['rbhusPipe_acl_user'] in stagedets['admins'].split(",")):
      return(True)
    else:
      return(False)
  else:
    return(True)

def isProjAdmin(assdets = {}):
  projdets = getProjDetails(projName=assdets['projName'])
  adms = ",".join(projdets['admins'].split())
  projdets['admins'] = adms
  if(os.environ['rbhusPipe_acl_user'] in projdets['admins'].split(",")):
    return(True)
  else:
    return(False)

def isNodeAdmin(assdets = {}):
  if(assdets['nodeType'] != "default"):
    nodedets  = getNodeTypes(assdets['nodeType'])
    if(os.environ['rbhusPipe_acl_user'] in nodedets['admins'].split(",")):
      return(True)
    else:
      return(False)
  else:
    return(True)


def isDbAdmin(assdets = {}):
  if(os.environ['rbhusPipe_acl_admin'] == "1"):
    return(True)
  else:
    return(False)

def isReviewUser(assdets = {}):
  if(os.environ['rbhusPipe_acl_user'] in assdets['reviewUser'].split(",")):
    return(True)
  else:
    return(False)
