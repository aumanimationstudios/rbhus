#!/usr/bin/python

import os
import sys
import pwd
import time
import socket
import subprocess
rbhus_main_path = os.sep.join(os.path.abspath(__file__).split(os.sep)[0:-3])
sys.path.append(rbhus_main_path)
import rbhus.renderPlugin

taskId = os.environ['rbhus_taskId']
frameId = os.environ['rbhus_frameId']
frames = os.environ['rbhus_frames']
user = os.environ['rbhus_user']
fileName = os.environ['rbhus_fileName']
btCmd = os.environ['rbhus_btCmd']    #Should be run by the server .. WTF!!!!!!!!!
fileType = os.environ['rbhus_fileType']
renderer = os.environ['rbhus_renderer']
minRam = os.environ['rbhus_minRam']
maxRam = os.environ['rbhus_maxRam']
outDir = os.environ['rbhus_outDir']
outName = os.environ['rbhus_outName']
logBase = os.environ['rbhus_logBase']
framePad = os.environ['rbhus_pad']
atCmd = os.environ['rbhus_atCmd']    #Should be run by the server .. WTF!!!!!!!!!
bfCmd = os.environ['rbhus_bfCmd']
afCmd = os.environ['rbhus_afCmd']
rThreads = os.environ['rbhus_threads']
renExtArgs = os.environ['rbhus_renExtArgs']
layer = os.environ['rbhus_layer']
pad = os.environ['rbhus_pad']
imType = os.environ['rbhus_imageType']
washMyButt = os.environ['rbhus_washmybutt']
runScript = os.environ['rbhus_runScript']
camera = os.environ['rbhus_camera']
res = os.environ['rbhus_resolution']

if(fileType == "convert_png_mp4"):
  script = "/projdump/pythonTestWindoze.DONOTDELETE/rbhus/tools/rbhus/convert_png_mp4.py"
else:
  script = "/projdump/pythonTestWindoze.DONOTDELETE/rbhus/tools/rbhus/convert_png_flv.py"
cmd = script +" "+ outDir
print (cmd)
rbhus.renderPlugin.sendCmd(cmd)