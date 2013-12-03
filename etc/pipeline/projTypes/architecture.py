#!/usr/bin/python
import glob
import os
import posix
import pwd
import time
import fcntl
import shutil
import sys
import re
import grp

progPath =  sys.argv[0].split(os.sep)
if(len(progPath) > 1):
  pwd = os.sep.join(progPath[0:-1])
  cwd = os.path.abspath(pwd)
else:
  cwd = os.path.abspath(os.getcwd())






projName = os.environ['rp_projName_c']
projType = os.environ['rp_projType_c']
directory = os.environ['rp_projDirectory_c']
admins = os.environ['rp_projAdmin_c']
rbhusRender =  os.environ['rp_projRender_c']
rbhusRenderServer = os.environ['rp_projRenderS_c']
aclUser = os.environ['rp_projAclUser_c']
aclGroup = os.environ['rp_projAclGroup_c']
desc = os.environ['rp_projDesc_c']
diskServer = os.environ['rp_dirMaps_server'] 
diskNfsExport = os.environ['rp_dirMaps_nfsServDir']
diskNfsMount = os.environ['rp_dirMaps_nfsMountDir']
projTypeLibrary = os.environ['rp_projTypes_libDir']
projTypeShare = os.environ['rp_projTypes_shareDir']
projTypeOutput = os.environ['rp_projTypes_outDir']

try:
  os.makedirs(diskNfsMount)
except:
  pass

try:
  os.system("mount "+ diskServer +":"+ os.sep + diskNfsExport.rstrip(os.sep).lstrip(os.sep) + os.sep +" "+ os.sep + diskNfsMount.lstrip(os.sep))
except:
  print(str(sys.exc_info()))
  sys.exit(1)


lib = projTypeLibrary.split(":")
libdir = ""
for x in lib:
  if(re.search("^\$directory",x)):
    libdir = libdir.rstrip(os.sep) + os.sep + diskNfsMount.lstrip(os.sep).rstrip(os.sep) 
  elif(re.search("^\$projName",x)):
    libdir = libdir.rstrip(os.sep) + os.sep + projName.lstrip(os.sep)
  else:
    libdir = libdir.rstrip(os.sep) + os.sep + x.lstrip(os.sep)
if(libdir):
  try:
    os.makedirs(libdir)
  except:
    pass
  

share = projTypeShare.split(":")
sharedir = ""
for x in share:
  if(re.search("^\$directory",x)):
    sharedir = sharedir.rstrip(os.sep) + os.sep + diskNfsMount.lstrip(os.sep).rstrip(os.sep) 
  elif(re.search("^\$projName",x)):
    sharedir = sharedir.rstrip(os.sep) + os.sep + projName.lstrip(os.sep)
  else:
    sharedir = sharedir.rstrip(os.sep) + os.sep + x.lstrip(os.sep)
if(sharedir):
  try:
    os.makedirs(sharedir)
  except:
    pass


output = projTypeOutput.split(":")
outputdir = ""
for x in output:
  if(re.search("^\$directory",x)):
    outputdir = outputdir.rstrip(os.sep) + os.sep + diskNfsMount.lstrip(os.sep).rstrip(os.sep) 
  elif(re.search("^\$projName",x)):
    outputdir = outputdir.rstrip(os.sep) + os.sep + projName.lstrip(os.sep)
  else:
    outputdir = outputdir.rstrip(os.sep) + os.sep + x.lstrip(os.sep)
if(outputdir):
  try:
    os.makedirs(outputdir)
  except:
    pass
  
    
try:
  os.system("chown -R "+ aclUser +":"+ aclGroup +" "+ diskNfsMount.rstrip(os.sep) + os.sep + projName)
except:
  print(str(sys.exc_info()))
  
  
os.system("umount -f "+ str(diskNfsMount))
sys.exit(0)
      
  