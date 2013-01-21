import ldap
import sys
import dbRbhus
import os



class login():
  def __init__(self):
    self.status = False
    self.userAcl = None
    self.username = None
    
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
    conn = ldap.initialize(self.ldaphost +":"+ self.ldapport)
    try:
      conn.simple_bind_s('uid='+ user +',ou=people,dc=bluepixels,dc=in',passwd)
      conn.unbind()
      self.status = True
      self.username = user
      self._getUserDets()
      return(1)
    except:
      print(str(sys.exc_info()))
      self.status = False
      self.username = None
      return(0)
    
    
  def _getUserDets(self):
    if(self.username):
      db_conn = dbRbhus.dbRbhus()
      try:
        rows = db_conn.execute("select * from admins where user='"+ str(self.username) +"'", dictionary=True)
        if(not isinstance(rows,int)):
          self.userAcl = rows[0]
      except:
        print(str(sys.exc_info()))
        self.userAcl = None
      
    