#!/usr/bin/python

import os
import sys
import pwd
import time
import socket
import subprocess

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
runScript.split(os.sep)
if(renExtArgs == "None"):
  renExtArgs = ""
RENDERCMD = "/usr/local/bin/blender -noaudio -b \"" + str(fileName) +"\""
RENDER_CMD = ""

outputN = os.sep.join(runScript.split(os.sep)[0:-1]) + os.sep +"outputNodes.py"

layerScF = "/tmp/"+ str(taskId) +"_"+ str(frameId) +".py"
wbd = open(washMyButt,"w")
wbd.writelines(layerScF +"\n\r")
wbd.flush()



fRs = " -f ".join(frames.split(","))
fr = " -f "+ fRs

outFile = "default"
if(outDir.find("default") < 0):
  outFile = outDir.rstrip(os.sep) + os.sep
if(outName.find("default") < 0):
  outFile = outFile.rstrip(os.sep) + os.sep + ".".join(outName.split(".")[0:-1]) + "_" + "".rjust(int(pad),"#") + "." + outName.split(".")[-1]


outputNoutF = "/tmp/"+ str(taskId) +"_"+ str(frameId) +"_outputNodes.py"
wbd.writelines(outputNoutF +"\n\r")
wbd.flush()
wbd.close()








os.system("cp "+ outputN +" "+ outputNoutF +" >& /dev/null")
os.system("sed -i 's/renameOutputDir/"+"\\/".join(outDir.split(os.sep)) +"/' "+ outputNoutF +" >& /dev/null")
if(renderer.find("default") < 0):
  RENDERCMD = RENDERCMD +" -E "+ renderer
RENDERCMD = RENDERCMD +" -t "+ rThreads
if(layer.find("default") < 0):
  layerScript = "import bpy\nfor x in bpy.context.scene.render.layers:\n  bpy.context.scene.render.layers[x.name].use = False\n\nbpy.context.scene.render.layers[\'"+ layer +"\'].use = True"
  f = open(layerScF,"w")
  f.writelines(layerScript)
  f.flush()
  f.close()
  RENDERCMD = RENDERCMD +" --python "+ layerScF
RENDERCMD = RENDERCMD +" --python "+ outputNoutF
if(imType.find("default") < 0):
  RENDERCMD = RENDERCMD +" -F "+ imType
if(outFile.find("default") < 0):
  RENDERCMD = RENDERCMD +" -o "+ outFile
RENDERCMD = RENDERCMD + fr


#if(renderer.find("default") < 0):
  #if(layer.find("default") < 0):
    #if(imType.find("default") < 0):
      #if((outDir.find("default") <  0) and (outName.find("default") <  0)):
        #RENDER_CMD = RENDERCMD +" -b "+ fileName +" -t "+ rThreads +" -E "+ renderer +" --python "+ layerScF +" -F "+ imType +" -o "+ outDir.rstrip(os.sep) + os.sep + layer + os.sep + ".".join(outName.split(".")[0:-1]) + "_" + "".rjust(int(pad),"#") + "." + outName.split(".")[-1] +" -f "+ fRs
      #else:
        #RENDER_CMD = RENDERCMD +" -b "+ fileName +" -t "+ rThreads +" -E "+ renderer +" --python "+ layerScF +" -F "+ imType +" -f "+ fRs
    #else:
      #if((outDir.find("default") <  0) and (outName.find("default") <  0)):
        #RENDER_CMD = RENDERCMD +" -b "+ fileName +" -t "+ rThreads +" -E "+ renderer +" --python "+ layerScF +" -o "+ outDir.rstrip(os.sep) + os.sep + layer + os.sep + ".".join(outName.split(".")[0:-1]) + "_" + "".rjust(int(pad),"#") + "." + outName.split(".")[-1] +" -f "+ fRs
      #else:
        #RENDER_CMD = RENDERCMD +" -b "+ fileName +" -t "+ rThreads +" -E "+ renderer +" --python "+ layerScF +" -f "+ fRs
  #else:
    #if(imType.find("default") < 0):
      #if((outDir.find("default") <  0) and (outName.find("default") <  0)):
        #RENDER_CMD = RENDERCMD +" -b "+ fileName +" -t "+ rThreads +" -E "+ renderer +" -F "+ imType +" -o "+ outDir.rstrip(os.sep) + os.sep + ".".join(outName.split(".")[0:-1]) + "_" + "".rjust(int(pad),"#") + "." + outName.split(".")[-1] +" -f "+ fRs
      #else:
        #RENDER_CMD = RENDERCMD +" -b "+ fileName +" -t "+ rThreads +" -E "+ renderer +" -F "+ imType +" -f "+ fRs
    #else:
      #if((outDir.find("default") <  0) and (outName.find("default") <  0)):
        #RENDER_CMD = RENDERCMD +" -b "+ fileName +" -t "+ rThreads +" -E "+ renderer +" -o "+ outDir.rstrip(os.sep) + os.sep + ".".join(outName.split(".")[0:-1]) + "_" + "".rjust(int(pad),"#") + "." + outName.split(".")[-1] +" -f "+ fRs
      #else:
        #RENDER_CMD = RENDERCMD +" -b "+ fileName +" -t "+ rThreads +" -E "+ renderer +" -f "+ fRs
#else:
  #if(layer.find("default") < 0):
    #if(imType.find("default") < 0):
      #if((outDir.find("default") <  0) and (outName.find("default") <  0)):
        #RENDER_CMD = RENDERCMD +" -b "+ fileName +" -t "+ rThreads +" --python "+ layerScF +" -F "+ imType +" -o "+ outDir.rstrip(os.sep) + os.sep + layer + os.sep + ".".join(outName.split(".")[0:-1]) + "_" + "".rjust(int(pad),"#") + "." + outName.split(".")[-1] +" -f "+ fRs
      #else:
        #RENDER_CMD = RENDERCMD +" -b "+ fileName +" -t "+ rThreads +" --python "+ layerScF +" -F "+ imType +" -f "+ fRs
    #else:
      #if((outDir.find("default") <  0) and (outName.find("default") <  0)):
        #RENDER_CMD = RENDERCMD +" -b "+ fileName +" -t "+ rThreads +" --python "+ layerScF +" -o "+ outDir.rstrip(os.sep) + os.sep + layer + os.sep + ".".join(outName.split(".")[0:-1]) + "_" + "".rjust(int(pad),"#") + "." + outName.split(".")[-1] +" -f "+ fRs
      #else:
        #RENDER_CMD = RENDERCMD +" -b "+ fileName +" -t "+ rThreads +" --python "+ layerScF +" -f "+ fRs
  #else:
    #if(imType.find("default") < 0):
      #if((outDir.find("default") <  0) and (outName.find("default") <  0)):
        #RENDER_CMD = RENDERCMD +" -b "+ fileName +" -t "+ rThreads +" -F "+ imType +" -o "+ outDir.rstrip(os.sep) + os.sep + ".".join(outName.split(".")[0:-1]) + "_" + "".rjust(int(pad),"#") + "." + outName.split(".")[-1] +" -f "+ fRs
      #else:
        #RENDER_CMD = RENDERCMD +" -b "+ fileName +" -t "+ rThreads +" -F "+ imType +" -f "+ fRs
    #else:
      #if((outDir.find("default") <  0) and (outName.find("default") <  0)):
        #RENDER_CMD = RENDERCMD +" -b "+ fileName +" -t "+ rThreads +" -o "+ outDir.rstrip(os.sep) + os.sep + ".".join(outName.split(".")[0:-1]) + "_" + "".rjust(int(pad),"#") + "." + outName.split(".")[-1] +" -f "+ fRs
      #else:
        #RENDER_CMD = RENDERCMD +" -b "+ fileName +" -t "+ rThreads +" -f "+ fRs

print(RENDERCMD)


sys.exit(0)




