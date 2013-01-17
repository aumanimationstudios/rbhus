#!/usr/bin/python


###
# Copyright (C) 2012  Shrinidhi Rao shrinidhi@clickbeetle.in
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
###


import os
import sys
import time
import socket
import subprocess
import multiprocessing
import tempfile

taskId = os.environ['rbhus_taskId']
frameId = os.environ['rbhus_frameId']
user = os.environ['rbhus_user']     
fileName = os.environ['rbhus_fileName'] 
minRam = os.environ['rbhus_minRam']   
maxRam = os.environ['rbhus_maxRam']   
logBase = os.environ['rbhus_logBase']  
framePad = os.environ['rbhus_pad']      
rThreads = os.environ['rbhus_threads']  
pad = os.environ['rbhus_pad']
outDir = os.environ['rbhus_outDir']
outFile = os.environ['rbhus_outName']
logFile = os.environ['rbhus_logFile']
washMyButt = os.environ['rbhus_washmybutt']
runScript = os.environ['rbhus_runScript']
frames = os.environ['rbhus_frames']
cam = os.environ['rbhus_camera']
res = os.environ['rbhus_resolution']
wbd = open(washMyButt,"w")

RENDERCMD = "\"c:/Program Files/Autodesk/3ds Max 2013/3dsmaxcmd.exe\""
RENDER_CMD = ""

if(outDir != "default"):
  if(outFile != "default"):
    imageName = outDir.rstrip("/") + "/" + outFile
  else:
    imageName = outDir.rstrip("/") + "/" + "image_"+ str(frameId).rjust(int(pad),"0") +".png"

totalCpus = multiprocessing.cpu_count()
b = ""
for x in range(0,int(rThreads)):
  b = b + "1"
hexAffinity = hex(int(b.rjust(totalCpus,"0"),2))

ffile = tempfile.gettempdir() + os.sep + taskId +"_"+ frameId +".bat"

wbd.writelines(ffile +"\n\r")
wbd.flush()
wbd.close()
f = open(ffile,"w")

renderCmd = RENDERCMD +" \""+ fileName +"\" -frames:"+ frames

#logFile = str(logBase).rstrip(os.sep) + os.sep + ".".join(str(fileName).lstrip(os.sep).rsplit(os.sep)[-1].rsplit(".")[0:-1]) +"_"+ str(frameId).rjust(int(pad),"0") +".log"
#f.write("echo %pid%\n\r")
if(cam != "default"):
  renderCmd = renderCmd +" -camera:"+ cam 
if(res != "default"):
  renderCmd = renderCmd +" -width:"+ res.split("x")[0] +" -height:"+ res.split("x")[1]
  
renderCmd = renderCmd + " -showRFW:0 -gammaCorrection:1 -gammaValueIn:2.2 -gammaValueOut:1 -continueOnError"

  

if(outDir != "default"):
  renderCmd = renderCmd +" -o:"+ imageName 

  

f.write("@ECHO ON\n\r")
f.flush()
f.write(renderCmd +"\n\r")
f.flush()
#f.write("taskkill /f /t /fi \""+ fileName +"\"\n\r")
#f.write("del %0\n\r")
f.write("SLEEP 1\n\r")
f.flush()

f.write("EXIT %errorlevel%\n\r")
f.close()

print("C:\Windows\System32\cmd.exe /C start /wait /affinity "+ str(hexAffinity) +" "+ tempfile.gettempdir() + os.sep + taskId +"_"+ frameId +".bat ")


sys.exit(0)
  
