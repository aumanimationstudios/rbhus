#!/usr/bin/python

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
  
