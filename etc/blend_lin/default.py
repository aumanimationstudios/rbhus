#!/usr/bin/python

import os
import sys
import pwd
import time
import socket
import subprocess

taskId = os.environ['rbhus_taskId']
frameId = os.environ['rbhus_frameId']
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

if(renExtArgs == "None"):
  renExtArgs = ""
RENDERCMD = "/usr/local/blender_svn/blender -noaudio"
RENDER_CMD = ""
layerScF = "/tmp/"+ str(taskId) +"_"+ str(frameId) +".py"

if(layer.find("default") < 0):
  layerScript = "import bpy\nfor x in bpy.context.scene.render.layers:\n  bpy.context.scene.render.layers[x.name].use = False\n\nbpy.context.scene.render.layers[\'"+ layer +"\'].use = True"
  f = open(layerScF,"w")
  f.writelines(layerScript)
  f.flush()
  f.close()

if(renderer.find("default") < 0):
  if(layer.find("default") < 0):
    if(imType.find("default") < 0):
      RENDER_CMD = RENDERCMD +" -b "+ fileName +" -E "+ renderer +" --python "+ layerScF +" -F "+ imType +" -o "+ outDir.rstrip(os.sep) + os.sep + layer + os.sep + ".".join(outName.split(".")[0:-1]) + "_" + "".rjust(int(pad),"#") + "." + outName.split(".")[-1] +" -s "+ frameId +" -e "+ frameId +" -a -t "+ rThreads
    else:
      RENDER_CMD = RENDERCMD +" -b "+ fileName +" -E "+ renderer +" --python "+ layerScF +" -o "+ outDir.rstrip(os.sep) + os.sep + layer + os.sep + ".".join(outName.split(".")[0:-1]) + "_" + "".rjust(int(pad),"#") + "." + outName.split(".")[-1] +" -s "+ frameId +" -e "+ frameId +" -a -t "+ rThreads
  else:
    if(imType.find("default") < 0):
      RENDER_CMD = RENDERCMD +" -b "+ fileName +" -E "+ renderer +" -F "+ imType +" -o "+ outDir.rstrip(os.sep) + os.sep + ".".join(outName.split(".")[0:-1]) + "_" + "".rjust(int(pad),"#") + "." + outName.split(".")[-1] +" -s "+ frameId +" -e "+ frameId +" -a -t "+ rThreads
    else:
      RENDER_CMD = RENDERCMD +" -b "+ fileName +" -E "+ renderer +" -o "+ outDir.rstrip(os.sep) + os.sep + ".".join(outName.split(".")[0:-1]) + "_" + "".rjust(int(pad),"#") + "." + outName.split(".")[-1] +" -s "+ frameId +" -e "+ frameId +" -a -t "+ rThreads
else:
  if(layer.find("default") < 0):
    if(imType.find("default") < 0):
      RENDER_CMD = RENDERCMD +" -b "+ fileName +" --python "+ layerScF +" -F "+ imType +" -o "+ outDir.rstrip(os.sep) + os.sep + layer + os.sep + ".".join(outName.split(".")[0:-1]) + "_" + "".rjust(int(pad),"#") + "." + outName.split(".")[-1] +" -s "+ frameId +" -e "+ frameId +" -a -t "+ rThreads
    else:
      RENDER_CMD = RENDERCMD +" -b "+ fileName +" --python "+ layerScF +" -o "+ outDir.rstrip(os.sep) + os.sep + layer + os.sep + ".".join(outName.split(".")[0:-1]) + "_" + "".rjust(int(pad),"#") + "." + outName.split(".")[-1] +" -s "+ frameId +" -e "+ frameId +" -a -t "+ rThreads
  else:
    if(imType.find("default") < 0):
      RENDER_CMD = RENDERCMD +" -b "+ fileName +" -F "+ imType +" -o "+ outDir.rstrip(os.sep) + os.sep + ".".join(outName.split(".")[0:-1]) + "_" + "".rjust(int(pad),"#") + "." + outName.split(".")[-1] +" -s "+ frameId +" -e "+ frameId +" -a -t "+ rThreads
    else:
      RENDER_CMD = RENDERCMD +" -b "+ fileName +" -o "+ outDir.rstrip(os.sep) + os.sep + ".".join(outName.split(".")[0:-1]) + "_" + "".rjust(int(pad),"#") + "." + outName.split(".")[-1] +" -s "+ frameId +" -e "+ frameId +" -a -t "+ rThreads

print(RENDER_CMD)


sys.exit(0)




