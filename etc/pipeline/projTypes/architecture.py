#!/usr/bin/python
import glob, os, posix, pwd, time, fcntl, shutil, sys

progPath =  sys.argv[0].split(os.sep)
if(len(progPath) > 1):
  pwd = os.sep.join(progPath[0:-1])
  cwd = os.path.abspath(pwd)
else:
  cwd = os.path.abspath(os.getcwd())






projName = os.environ['rp_projName_c']
projType = os.environ['rp_projType_c']
directory = os..environ['rp_projDirectory_c']
admins = os.environ['rp_projAdmin_c']
rbhusRender =  os.environ['rp_projRender_c']
rbhusRenderServer = os.environ['rp_projRenderS_c']
projOs = os.environ['rp_projOs_c']
desc = os.environ['rp_projDesc_c']
diskServer = os.environ['rp_dirMaps_server']
diskNfsExport = os.environ['rp_dirMaps_nfsServDir']
diskNfsMount = os.environ['rp_dirMaps_nfsMountDir']

level1 = ['share','library','output','dump']
level2 = {'share':['bin','stageTemplates/stageType'],
          'library':['assets'],
          'output':['forClient']}


os.system("mount "+ diskServer +":"+ diskNfsExport.rstrip(os.sep) + os.sep +" "+ diskNfsMount)
for x in level1:
  os.makedirs(diskNfsMount.rstrip(os.sep) + os.sep + x)
  
  