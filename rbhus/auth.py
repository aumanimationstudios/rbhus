import ldap
import sys
import dbRbhus
import os



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
  
  
  def ldapLogin(self,user, passwd):
    print("connecting ldap server : "+ str(self.ldaphost) +" : at port : "+ str(self.ldapport))
    try:
      conn = ldap.initialize(self.ldaphost +":"+ self.ldapport)
      conn.simple_bind_s('uid='+ user +',ou=people,dc=bluepixels,dc=in',passwd)
      conn.unbind()
      self.status = True
      self.username = user
      self._setEnvs()
      return(1)
    except:
      print(str(sys.exc_info()))
      self.status = False
      self._unsetEnvs()
      return(0)
  
  def useEnvUser(self):
    if(sys.platform.find("win") >= 0):
      try:
        self.username = os.environ['USERNAME']
        self.status = True
        self._setEnvs()
        return(1)
      except:
        self.username = None
        self.status = False
        self._unsetEnvs()
        return(0)
    elif(sys.platform.find("linux") >= 0):
      try:
        self.username = os.environ['USER']
        self.status = True
        self._setEnvs()
        return(1)
      except:
        self.status = False
        self._unsetEnvs()
        self.username = None
        return(0)
        
    
  
  def _setEnvs(self):
    self.__getUserDets()
    print("\nexporting environment variables...\n")
    os.environ['rbhus_acl_user'] = self.username
    os.environ['rbhus_acl_projIds'] = ""
    os.environ['rbhus_acl_admin'] = ""
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
        rows = db_conn.execute("select * from proj", dictionary=True)
        adminRows = db_conn.execute("select * from admins", dictionary=True)
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
      
    