import ldap
import sys
import dbRbhus



class login():
  def __init__(self):
    self.status = False
    self.userAcl = None
    self.username = None
  
  
  def ldapLogin(self,user, passwd, host='ldap://ldaphost', port='389'):
    conn = ldap.initialize(host +":"+ port)
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
      
    