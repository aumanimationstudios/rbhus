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
  
try:
  rbhusLibPath = os.environ['rbhusLibPath']
  sys.path.append(rbhusLibPath)
  import utilsPipe
except:
  pass
try:
  rbhusUILibPath = os.environ['rbhusUILibPath']
  sys.path.append(rbhusUILibPath)
except:
  pass
print(cwd)
sys.exit()




projName = os.environ['rp_proj_projName']
projType = os.environ['rp_proj_projType']
directory = os.environ['rp_proj_directory']
admins = os.environ['rp_proj_admins']
rbhusRender =  os.environ['rp_proj_rbhusRenderIntegration']
rbhusRenderServer = os.environ['rp_proj_rbhusRenderServer']
aclUser = os.environ['rp_proj_aclUser']
aclGroup = os.environ['rp_proj_aclGroup']
desc = os.environ['rp_proj_description']
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
  if(re.search("^\$",str(x))):
    libdir = libdir.rstrip(os.sep) + os.sep + os.environ["rp_"+ str(x).lstrip("$")]
if(libdir):
  try:
    os.makedirs(libdir)
  except:
    pass
  

share = projTypeShare.split(":")
sharedir = ""
for x in share:
  if(re.search("^\$",str(x))):
    sharedir = sharedir.rstrip(os.sep) + os.sep + os.environ["rp_"+ str(x).lstrip("$")]
if(sharedir):
  try:
    os.makedirs(sharedir)
  except:
    pass


output = projTypeOutput.split(":")
outputdir = ""
for x in output:
  if(re.search("^\$",str(x))):
    outputdir = outputdir.rstrip(os.sep) + os.sep + os.environ["rp_"+ str(x).lstrip("$")]
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
      
  