#!/usr/bin/python

import argparse
import os
import sys

dirSelf = os.path.dirname(os.path.realpath(__file__))
rbhusLib = dirSelf.rstrip(os.sep).rstrip("system").rstrip(os.sep).rstrip("tools").rstrip(os.sep) + os.sep + "rbhus"

sys.path.append(dirSelf.rstrip(os.sep).rstrip("system").rstrip(os.sep).rstrip("tools").rstrip(os.sep) + os.sep + "rbhus")

print(dirSelf)
print(rbhusLib)


import dbRbhus
import constants




dbconn = dbRbhus.dbRbhus()
dbconnhost = dbRbhus.dbRbhusHost()

parser = argparse.ArgumentParser()

parser.add_argument("-m","--mac",dest='mac',help='macc address of the host')
parser.add_argument("-i","--ip",dest='ip',help='ip address of the host')
parser.add_argument("-n","--hostname",dest='hostname',help="hostname of the host")
parser.add_argument("-a","--alias",dest='alias',help="comma seperated alias of the host")
parser.add_argument("-d","--domain",dest='domain',help="domain of the host")
args = parser.parse_args()


try:
  dbconnhost.execute("insert into main (macc, ip,name,alias,domain) values ( \
                    '"+ str(args.mac)  +"', \
                    '"+ str(args.ip)+"', \
                    '"+ str(args.hostname) +"', \
                    '"+ str(args.alias) +"', \
                    '"+ str(args.domain) +"')")
except:
  print(sys.exc_info())
  sys.exit(1)


try:
  dbconnhost.execute("insert into clonedb (ip,cloneType,cloneStatus,clone) values ( \
                    '"+ str(args.ip) +"', \
                    '"+ str(constants.cloneTypeLinuxWin) +"', \
                    '"+ str(constants.cloneStatusInitiate) +"', \
                    '"+ str(constants.cloneClone) +"')")
except:
  print(sys.exc_info())
  sys.exit(1)

sys.exit(0)









