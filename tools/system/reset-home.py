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

print("mv "+ os.path.join(homedir,".*") +" "+ backupdir)
print("mkdir -p .local/share/")
print("rsync -av /etc/skel/ "+ homedir)
print("rsync -av "+ backupConfigKrita +" "+ configKrita)
print("rsync -av "+ backupConfigTray +" "+ configTray)
print("rsync -av "+ backupLocalKrita +" "+ localKrita)
print("rsync -av "+ backupConfigBlend +" "+ configBlend)


