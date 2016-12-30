#!/usr/bin/env python2
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"


import os
import sys
import pwd
import time
import socket
import subprocess
import simplejson

rbhus_main_path = os.sep.join(os.path.abspath(__file__).split(os.sep)[0:-3])
sys.path.append(rbhus_main_path)
import rbhus.utilsPipe
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

RENDERCMD = "/usr/local/bin/blender -noaudio -b \"" + str(fileName) +"\""

if("rbhus_renExtEnv" in rbhus.renderPlugin.env):
  extEnv = rbhus.renderPlugin.env['rbhus_renExtEnv']
  if(extEnv != "default"):
    extEnvDict = simplejson.loads(extEnv)
    if("exe" in extEnvDict):
      RENDERCMD = extEnvDict['exe'] +" -noaudio -b \"" + str(fileName) + "\""







if(renExtArgs == "None"):
  renExtArgs = ""

RENDER_CMD = ""

outputN = "/"+ "/".join(runScript.split("/")[0:-1]) + "/" +"outputNodes.py"

layerScF = "/tmp/"+ str(taskId) +"_"+ str(frameId) +"_layer.py"
cameraF = "/tmp/"+ str(taskId) +"_"+ str(frameId) +"_camera.py"
resF = "/tmp/"+ str(taskId) +"_"+ str(frameId) +"_res.py"
defaultF = "/tmp/"+ str(taskId) +"_"+ str(frameId) +"_defF.py"
wbd = open(washMyButt,"w")
wbd.writelines(layerScF +"\n\r")
wbd.writelines(cameraF +"\n\r")
wbd.writelines(resF +"\n\r")
wbd.writelines(defaultF +"\n\r")
wbd.flush()



fRs = " -f ".join(frames.split(","))
fr = " -f "+ fRs

outFile = "default"
if(outDir != "default"):
  outFile = outDir.rstrip("/") + "/"
if(outName != "default"):
  outFile = outFile.rstrip("/") + "/" + ".".join(outName.split(".")[0:-1]) + "_" + "".rjust(int(pad),"#") + "." + outName.split(".")[-1]


outputNoutF = "/tmp/"+ str(taskId) +"_"+ str(frameId) +"_outputNodes.py"
wbd.writelines(outputNoutF +"\n\r")
wbd.flush()
wbd.close()


try:
  os.system("cp -a "+ outputN +" "+ outputNoutF +" >& /dev/null")
except:
  pass
try:
  os.system("sed -i 's/renameOutputDir/"+"\\/".join(outDir.split("/")) +"/' "+ outputNoutF +" >& /dev/null")
except:
  pass
if(layer != "default"):
  try:
    os.system("sed -i 's/renameRenderLayer/"+ layer +"/' "+ outputNoutF +" >& /dev/null")
  except:
    pass


if(renderer != "default"):
  RENDERCMD = RENDERCMD +" -E "+ renderer
RENDERCMD = RENDERCMD +" -t "+ rThreads
defaultScripts = "import bpy\nbpy.context.scene.render.use_save_buffers = False\nbpy.context.scene.render.use_overwrite = True\nbpy.context.scene.render.use_simplify = False\nbpy.context.scene.render.fps = 24\nbpy.context.scene.render.fps_base = 1\nbpy.context.scene.render.use_single_layer = False\nbpy.context.scene.render.use_stamp = False"
if(imType.find("PNG") >=0):
  defaultScripts = defaultScripts +"\nbpy.context.scene.color_depth = '16'"
if(imType == "PNG-RGB"):
  defaultScripts = defaultScripts +"\nbpy.context.scene.color_mode = 'RGB'"
  imType = "PNG"
elif(imType == "PNG-RGBA"):
  defaultScripts = defaultScripts + "\nbpy.context.scene.color_mode = 'RGBA'"
  imType = "PNG"

if(renderer == "CYCLES"):
  defaultScripts = defaultScripts + "\nbpy.context.scene.cycles.device = 'CPU'"

dF = open(defaultF,"w")
dF.writelines(defaultScripts)
dF.flush()
dF.close()
RENDERCMD = RENDERCMD +" --python "+ defaultF

if(layer != "default"):

  layerScript = "import bpy\nfor x in bpy.context.scene.render.layers:\n  bpy.context.scene.render.layers[x.name].use = False\n\n"
  lay = layer.split(",")
  for l in lay:
    if(l):
      layerScript = layerScript + "\nbpy.context.scene.render.layers[\'"+ l +"\'].use = True\n"
  f = open(layerScF,"w")
  f.writelines(layerScript)
  f.flush()
  f.close()
  RENDERCMD = RENDERCMD +" --python "+ layerScF
if(camera != "default"):
  cameraScript = "import bpy\nbpy.context.scene.camera = bpy.data.objects[\""+ camera + "\"]"
  c = open(cameraF,"w")
  c.writelines(cameraScript)
  c.flush()
  c.close()
  RENDERCMD = RENDERCMD +" --python "+ cameraF
if(res != "default"):
  resScript = "import bpy\nbpy.context.scene.render.resolution_x = "+ res.split("x")[0] +"\nbpy.context.scene.render.resolution_y = "+ res.split("x")[1] +"\nbpy.context.scene.render.resolution_percentage = 100"
  r = open(resF,"w")
  r.writelines(resScript)
  r.flush()
  r.close()
  RENDERCMD = RENDERCMD +" --python "+ resF
RENDERCMD = RENDERCMD +" --python "+ outputNoutF
if(imType.find("default") < 0):
  RENDERCMD = RENDERCMD +" -F "+ imType
if(outFile.find("default") < 0):
  RENDERCMD = RENDERCMD +" -o "+ outFile
RENDERCMD = RENDERCMD + fr

os.system("chmod 777 {0} {1} {2} {3} {4} >& /dev/null".format(layerScF,cameraF,resF,defaultF,outputNoutF))

print(RENDERCMD)
rbhus.renderPlugin.sendCmd(RENDERCMD)

sys.exit(0)
