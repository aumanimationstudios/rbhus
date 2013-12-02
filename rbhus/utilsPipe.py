import sys
import os
import socket
import MySQLdb
import multiprocessing
import pickle
import datetime

progPath =  sys.argv[0].split(os.sep)
if(len(progPath) > 1):
  pwd = os.sep.join(progPath[0:-1])
  cwd = os.path.abspath(pwd)
else:
  cwd = os.path.abspath(os.getcwd())

sys.path.append(cwd.rstrip(os.sep) + os.sep)
import dbPipe
import constantsPipe





def getDirMaps():
  dbconn = dbPipe.dbPipe()
  try:
    rows = dbconn.execute("SELECT * FROM dirMaps", dictionary=True)
    return(rows)
  except:
    print(str(sys.exc_info()))
    return(0)
  
 
 
def getProjTypes():
  dbconn = dbPipe.dbPipe()
  try:
    rows = dbconn.execute("SELECT * FROM projTypes", dictionary=True)
    return(rows)
  except:
    print(str(sys.exc_info()))
    return(0)
  
  
def getStageTypes():
  dbconn = dbPipe.dbPipe()
  try:
    rows = dbconn.execute("SELECT * FROM stageTypes", dictionary=True)
    return(rows)
  except:
    print(str(sys.exc_info()))
    return(0)


def getProjDefaults(self):
  try:
    rows = self.db_conn.execute("desc proj",dictionary=True)
    taskFieldss = {}
    for row in rows:
      taskFieldss[row['Field']] = row['Default']
    return(taskFieldss)
  except:
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
    print(str(sys.exc_info()))
    # easy to search like - if admin in getAdmins():
    return(adminUsers)


# createdUser should come from an env variable set by the authPipe module
def createProj(projType,projName,directory,admins,rbhusRenderIntergration,rbhusRenderServer,aclUser,aclGroup,createdUser,dueDate,description):
  if(createdUser not in getAdmins()):
    print("User not allowed to create projects")
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
  projDets['createdUser'] = createdUser if(createdUser) else pDefs['createdUser']
  projDets['dueDate'] = dueDate if(dueDate) else str(now.year + 1) +"-"+ str(now.month) +"-"+ str(now.day) +" "+ str(now.hour) +"-"+ str(now.minute) +"-"+ str(now.second)
  projDets['description'] = description if(description) else pDefs['description']
  servSoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:
    servSoc.settimeout(15)
    servSoc.connect((ipAddr,constantsPipe.projInitPort))
  except:
    print(str(sys.exc_info()))
    return(0)
    
  servSoc.send("CREATE:"+ str(pickle.dumps(projDets)))
  servSoc.close()
  return(1)


#always called by the server
def setupProj(projType,projName,directory,admins,rbhusRenderIntergration,rbhusRenderServer,aclUser,aclGroup,createdUser,dueDate,description):
  dbconn = dbPipe.dbPipe()
  pTypes = getProjTypes()
  cScript = ""
  projId = 0
  for pT in pTypes:
    if(pT['type'] == projType):
      cScript = pT['scriptDir']
      
  os.environ['rp_projName_c'] = projName
  os.environ['rp_projType_c'] = projType
  os.environ['rp_projDirectory_c'] = directory
  os.environ['rp_projAdmin_c'] = admins
  os.environ['rp_projRender_c'] = rbhusRenderIntergration
  os.environ['rp_projRenderS_c'] = rbhusRenderServer
  os.environ['rp_projDesc_c'] = description
  os.environ['rp_projAclUser_c'] = aclUser
  os.environ['rp_projAclGroup_c'] = aclGroup
  os.environ['rp_projDueDate_c'] = dueDate
  os.environ['rp_projCreatedUser_c'] = createdUser

  exportDirMaps(directory)
  exportProjTypes(projType)
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
                    now(), \
                    '"+ str(description) +"')")
    ids = self.db_conn.execute("select last_insert_id()", dictionary = True)
    projId = ids[0]['last_insert_id()']
  except:
    print(str(sys.exc_info()))
    return(0)
    
  try:
    if(cScript):
      status = os.system("python -d '"+ str(cScript) +"'")
      return(1)
  except:
    print(str(sys.exc_info()))
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