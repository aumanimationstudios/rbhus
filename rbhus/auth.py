import ldap
import sys
import dbRbhus
import os
import tempfile
import time
import constants

class login():
  def __init__(self):
    self.status = False
    self.userAclProjIds = []
    self.username = None
    self.rbhusAdminFlag = 0
    try:
      self.ldaphost = os.environ['rbhus_ldapHost']
    except:
      self.ldaphost = 'ldap://ldaphost'
    
    try:
      self.ldapport = os.environ['rbhus_ldapPort']
    except:
      self.ldapport = '389'
  
  def tryRememberMe(self):
    passwdF = tempfile.gettempdir() + os.sep +"sys_init.dnd"
    pFs = 0
    try:
      createT = os.stat(passwdF)
      pFs = 1
    except:
      print(str(sys.exc_info()))
    if(pFs):
      if((time.time() - createT.st_ctime)/60 >= 500):
        try:
          os.remove(passwdF)
        except:
          print(str(sys.exc_info()))
        return(0)
      else:
        pf = open(passwdF,"r")
        x = pf.readlines()
        user = x[0].rstrip().lstrip()
        os.environ['rbhus_acl_rememberMe'] = user
        self.useEnvUser()
        return(1)
        
    
  def rememberMeStore(self):
    passwdF = tempfile.gettempdir() + os.sep +"sys_init.dnd"
    try:
      os.remove(passwdF)
    except:
      print(str(sys.exc_info()))
    pf = open(passwdF,"w")
    pf.writelines(self.username)
    
  def logout(self):
    passwdF = tempfile.gettempdir() + os.sep +"sys_init.dnd"
    try:
      os.remove(passwdF)
    except:
      pass
  
  def ldapLogin(self,user, passwd, rMs = False):
    print("connecting ldap server : "+ str(self.ldaphost) +" : at port : "+ str(self.ldapport))
    try:
      conn = ldap.initialize(self.ldaphost +":"+ self.ldapport)
      conn.simple_bind_s('uid='+ user +',ou=people,dc=bluepixels,dc=in',passwd)
      conn.unbind()
      self._unsetEnvs()
      self.status = True
      self.username = user
      self._setEnvs()
      if(rMs):
        self.rememberMeStore()
      return(1)
    except:
      print(str(sys.exc_info()))
      self.status = False
      self._unsetEnvs()
      return(0)
  
  def useEnvUser(self):
    try:
      self.username = os.environ['rbhus_acl_rememberMe']
      self.status = True
      self._setEnvs()
      return(1)
    except:
      if(sys.platform.find("win") >= 0):
        try:
          self.username = os.environ['USERNAME']
          self.status = True
          self._setEnvs()
          return(1)
        except:
          self._unsetEnvs()
          return(0)
      elif(sys.platform.find("linux") >= 0):
        try:
          self.username = os.environ['USER']
          self.status = True
          self._setEnvs()
          return(1)
        except:
          self._unsetEnvs()
          return(0)
        
    
  
  def _setEnvs(self):
    self.__getUserDets()
    print("\nexporting environment variables...\n")
    os.environ['rbhus_acl_user'] = self.username
    os.environ['rbhus_acl_projIds'] = ""
    os.environ['rbhus_acl_admin'] = "0"
    if(self.userAclProjIds):
      os.environ['rbhus_acl_projIds'] = os.environ['rbhus_acl_projIds'] + " ".join(self.userAclProjIds)
    if(self.rbhusAdminFlag):
      os.environ['rbhus_acl_admin'] = "1"
  
  def _unsetEnvs(self):
    self.status = False
    self.username = None
    self.userAclProjIds = []
    self.rbhusAdminFlag = 0
    os.environ['rbhus_acl_user'] = ""
    os.environ['rbhus_acl_projIds'] = ""
    os.environ['rbhus_acl_admin'] = ""
  
  def __getUserDets(self):
    if(self.username):
      db_conn = dbRbhus.dbRbhus()
      try:
        rows = db_conn.execute("select * from proj where status="+ str(constants.projActive), dictionary=True)
        adminRows = db_conn.execute("select * from admins where user like '%"+ str(self.username) +"%'", dictionary=True)
        if(not isinstance(rows,int)):
          for x in rows:
            users = x['admins'].split()
            if(self.username in users):
              print("appending project id : "+ str(x['id']))
              self.userAclProjIds.append(str(x['id']))
        if(not isinstance(adminRows,int)):
          for x in adminRows:
            if(self.username == x['user']):
              self.rbhusAdminFlag = 1
              break
      except:
        print(str(sys.exc_info()))
      
    