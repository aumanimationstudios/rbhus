#!/usr/bin/python

###
# Copyright (C) 2012  Shrinidhi Rao shrinidhi@clickbeetle.in
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
###

# place this file in /prodloops/lib/python2/

# DEPRECATED #


import MySQLdb
import MySQLdb.cursors


class dict(MySQLdb.cursors.DictCursor):
  pass

#def dictCursor():
#  dictCursor = MySQLdb.cursors.DictCursor
#  return(dictCursor)

def connHosts():
  try:
    conn = MySQLdb.connect(host = "bluepixelsanimation.dyndns-office.com",port=6000,db = "hosts")
    conn.autocommit(1)
  except:
    raise
  return(conn)
  
  
def connRbhus():
  try:
    conn = MySQLdb.connect(host = "bluepixelsanimation.dyndns-office.com",port=6000,db = "rbhus")
    conn.autocommit(1)
  except:
    raise
  return(conn)
  
