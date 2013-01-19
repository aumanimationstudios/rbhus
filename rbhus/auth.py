import ldap
import sys


def ldapLogin(user, passwd, host='ldap://bluepixelsanimation.dyndns-office.com', port='500'):
  conn = ldap.initialize(host +":"+ port)
  try:
    conn.simple_bind_s('uid='+ user +',ou=people,dc=bluepixels,dc=in',passwd)
    conn.unbind()
    return(1)
  except:
    return(0)
    
    
