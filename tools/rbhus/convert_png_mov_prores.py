#!/usr/bin/env python2
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys
import os

sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-3]))



import multiprocessing
import glob
import subprocess
import uuid
import shutil


path = os.path.abspath(sys.argv[1])

cpus = multiprocessing.cpu_count()
pngs = glob.glob(path.rstrip(os.sep) + os.sep + "*.png")
pngs.sort()
mov = "_".join(pngs[-1].split(".")[0].split("_")[:-1]) + ".mov"
png = "_".join(pngs[-1].split(".")[0].split("_")[:-1]) + "_%04d.png"
startFrame = pngs[0].split("_")[-1].rstrip(".png")
# print(startFrame)

endFrame = pngs[-1].split("_")[-1].rstrip(".png")
# print(endFrame)
inputFileFmt = "_".join(pngs[-1].split(".")[0].split("_")[:-1]) + "_"+ startFrame +"-"+ endFrame +".png"

ffmpeg = None
if(os.path.exists("/opt/lib/ffmpeg/bin/ffmpeg")):
  ffmpeg = "/opt/lib/ffmpeg/bin/ffmpeg"
else:
  print("Not found : /opt/lib/ffmpeg/bin/ffmpeg")
  ffmpeg = "ffmpeg"
# cmd = "ffmpeg -probesize 5000000 -gamma 2.2 -r 24 -i "+ png +" -c:v prores_ks -profile:v 3 -vendor ap10 -pix_fmt yuv422p10le -qscale:v 5 -y "+ mov
cmd = ffmpeg +" -probesize 50000000 -r 24 -start_number "+ str(startFrame) +" -i "+ png +" -c:v prores_ks -profile:v 3 -vendor ap10 -pix_fmt yuv422p10le -qscale:v 5 -y "+ mov
# print (cmd)
# os.system(cmd)
p = subprocess.Popen(cmd,shell=True)
p.wait()
# os.remove(unatron)
