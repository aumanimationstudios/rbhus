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
RENDERCMD = "\"c:\\Program Files\\Autodesk\\3ds Max 2011\\3dsmaxcmd.exe\""
RENDER_CMD = ""

if(outDir != "default"):
  imageName = outDir.rstrip(os.sep) + os.sep + outFile

totalCpus = multiprocessing.cpu_count()
b = ""
for x in range(0,int(rThreads)):
  b = b + "1"
hexAffinity = hex(int(b.rjust(totalCpus,"0"),2))

f = open(tempfile.gettempdir() + os.sep + taskId +"_"+ frameId +".bat","w")

logFile = str(logBase).rstrip(os.sep) + os.sep + ".".join(str(fileName).lstrip(os.sep).rsplit(os.sep)[-1].rsplit(".")[0:-1]) +"_"+ str(frameId).rjust(int(pad),"0") +".log"
#f.write("echo %pid%\n\r")

if(outDir != "default"):
  RENDER_CMD = RENDERCMD +" \""+ fileName +"\" -start:"+ frameId +" -end:"+ frameId +" -showRFW:0 -o:"+ imageName +" 2>&1"
else:
  RENDER_CMD = RENDERCMD +" \""+ fileName +"\" -start:"+ frameId +" -end:"+ frameId +" -showRFW:0 2>&1"
  

f.write(RENDER_CMD +"\n\r")
f.flush()
#f.write("taskkill /f /t /fi \""+ fileName +"\"\n\r")
#f.write("del %0\n\r")
f.write("SLEEP 20\n\r")
f.flush()

f.write("EXIT %errorlevel%\n\r")
f.close()

print("C:\Windows\System32\cmd.exe /C start /affinity "+ str(hexAffinity) +" "+ tempfile.gettempdir() + os.sep + taskId +"_"+ frameId +".bat 2>&1" )


sys.exit(0)
  
