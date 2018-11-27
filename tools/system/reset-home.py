#!/usr/bin/env python2
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys
import os
import uuid

homedir = os.environ['HOME'] + os.sep
backupdir = os.path.join(homedir,"backup."+ str(uuid.uuid4()))
backupConfigTray = os.path.join(backupdir,".config","tray-server")
configTray = os.path.join(homedir,".config/")
backupConfigKrita = os.path.join(backupdir,".config","krita*")
configKrita = os.path.join(homedir,".config/")
backupLocalKrita = os.path.join(backupdir,".local","share","krita*")
localKrita = os.path.join(homedir,".local","share/")
backupConfigBlend = os.path.join(backupdir,".config","blender")
configBlend = os.path.join(homedir,".config/")
os.system("mkdir -p "+ backupdir)
os.system("mv "+ os.path.join(homedir,".*") +" "+ backupdir)
os.system("mkdir -p "+ os.path.join(homedir,".local/share/"))
os.system("rsync -av /etc/skel/ "+ homedir)
os.system("rsync -av "+ backupConfigKrita +" "+ configKrita)
os.system("rsync -av "+ backupConfigTray +" "+ configTray)
os.system("rsync -av "+ backupLocalKrita +" "+ localKrita)
os.system("rsync -av "+ backupConfigBlend +" "+ configBlend)


