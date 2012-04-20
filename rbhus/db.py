#!/usr/bin/python

# place this file in /prodloops/lib/python2/

import MySQLdb
import MySQLdb.cursors


class dict(MySQLdb.cursors.DictCursor):
  pass

#def dictCursor():
#  dictCursor = MySQLdb.cursors.DictCursor
#  return(dictCursor)

def connHosts():
  try:
    conn = MySQLdb.connect(host = "dbHosts",
			   db = "hosts")
    conn.autocommit(1)
  except:
    raise
  return(conn)
  
  
def connRbhus():
  try:
    conn = MySQLdb.connect(host = "dbRbhus",
			   db = "rbhus")
    conn.autocommit(1)
  except:
    raise
  return(conn)
  
