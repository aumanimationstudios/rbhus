#!/usr/bin/python

import os
import sys
import pwd
import time
import socket
import subprocess


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
pad = os.environ['rbhus_pad']
if(renExtArgs == "None"):
  renExtArgs = ""
RENDERCMD = "/usr/local/bin/Render"
RENDER_CMD = ""


if(renderer == "vray"):
  RENDER_CMD = RENDERCMD +" -renderer vray -s "+ frameId +" -e "+ frameId +" -rd \""+ outDir +"\" -im "+ outName +" -threads "+ rThreads +" "+ renExtArgs +" \""+ fileName +"\""
  

print(RENDER_CMD)


sys.exit(0)
  



