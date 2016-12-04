#!/usr/bin/env python2
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import subprocess
import os
import sys

mysqldump = "/usr/bin/mysqldump"
mysqldump_nodata = "/usr/bin/mysqldump --no-data"
mysql = "/usr/bin/mysql"
backup_path = "/mnt/swr/BACKUP/mysql_blues2/"
date = "/bin/date +%Y_%m_%d__%H_%M"
try:
  os.makedirs(backup_path)
except:
  print (sys.exc_info())

os.chdir(backup_path)
p = subprocess.Popen("/bin/echo \"show databases\" | "+ mysql +" -h blues2",shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
q = p.communicate()[0]
for x in q.split():
  if(x != "Database" and x != "mysql" and x != "performance_schema" and x != "information_schema" and x != "sys"):
    mysqldump_cmd = mysqldump +" -h blues2 "+ x +" > ./"+ x +"_data____`"+ date +"`.mysql"
    mysqldump_nodata_cmd = mysqldump_nodata +" -h blues2 "+ x +" > ./"+ x +"_nodata____`"+ date +"`.mysql"
    pro = subprocess.Popen(mysqldump_cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    print (pro.communicate())
    pro_nodata = subprocess.Popen(mysqldump_nodata_cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    print (pro_nodata.communicate())

