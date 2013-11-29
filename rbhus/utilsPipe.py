import sys
import os
import socket
import MySQLdb
import multiprocessing
import pickle

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
def createProj(projType,projName,os,directory,admins,rbhusRenderIntergration,rbhusRenderServer,aclUser,aclGroup,createdUser,dueDate,description):
  if(createdUser not in getAdmins()):
    print("User not allowed to create projects")
    return(0)
  projDets = {}
  projDets['projType'] = projType
  projDets['projName'] = projName
  projDets['os'] = os
  projDets['directory'] = directory
  projDets['admins'] = admins
  projDets['rbhusRenderIntergration'] = rbhusRenderIntergration
  projDets['rbhusRenderServer'] = rbhusRenderServer
  projDets['aclUser'] = aclUser
  projDets['aclGroup'] = aclGroup
  projDets['createdUser'] = createdUser
  projDets['dueDate'] = dueDate
  projDets['description'] = description
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
def setupProj(projType,projName,os,directory,admins,rbhusRenderIntergration,rbhusRenderServer,aclUser,aclGroup,createdUser,dueDate,description):
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
  os.environ['rp_os_c'] = os
  os.environ['rp_projDesc_c'] = description
  os.environ['rp_projAclUser_c'] = aclUser
  os.environ['rp_projAclGroup_c'] = aclGroup
  os.environ['rp_projDueDate_c'] = dueDate
  os.environ['rp_projCreatedUser_c'] = createdUser

  exportDirMaps(directory)
  try:
    dbconn.execute("insert into proj (projName,directory,admins,os,projType,rbhusRenderIntergration,rbhusRenderServer,aclUser,aclGroup,createdUser,dueDate,createDate,description) \
                    values ('"+ str(projName) +"', \
                    '"+ str(directory) +"', \
                    '"+ str(admins) +"', \
                    '"+ str(os) +"', \
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
  dbconn = dbPipe.dbPipe()
  try:
    rows = dbconn.execute("select * from dirMaps where directory='"+ str(directory) +"'", dictionary=True)
  except:
    print(str(sys.exc_info()))
    return(0)
  if(rows):
    flds = rows[0].keys()
    for f in flds:
      os.environ['rp_dirMaps_'+ str(f).rstrip().lstrip()] = str(rows[0][f])
    return(1)
    