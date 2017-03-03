#!/usr/bin/env python2
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import os
import subprocess
import sys
import argparse
import tempfile

tempdir = tempfile.gettempdir()
parser = argparse.ArgumentParser()

parser.add_argument("-s","--start",dest='start',help='start frame')
parser.add_argument("-e","--end",dest='end',help='end frame')
parser.add_argument("-b","--batch",dest='batch',help="batch by number of frames")
parser.add_argument("-f","--file",dest='filename',help="filename to render")
parser.add_argument("-o","--output",dest='output',help="output path (abs path)")
args = parser.parse_args()

try:
  outputpath = args.output
except:
  outputpath = tempdir
start_frame = int(args.start)
end_frame = int(args.end)
batch_by = int(args.batch)
filename = args.filename
outfile = (".".join(filename.split(".")[:-1])).split(os.sep)[-1]
print(outfile)
filename_no = 1
filesrendered = []
if(batch_by <= (end_frame-start_frame)+1):
  getlost = False
  while(True):
    s = start_frame
    e = start_frame + batch_by
    if(e > end_frame):
      e = end_frame
      getlost = True
    start_frame = e + 1


    of = outfile + "_" + str(filename_no).rjust(4, "0") + ".mov"
    outfilename = os.path.join(outputpath, of)
    tmp_bpy_file = os.path.join(tempdir, outfile + "_" + str(filename_no).rjust(4, "0") + ".py")
    tmp_bpy_file_fd = open(tmp_bpy_file, "w")
    bpy = "import bpy\nbpy.data.scenes['Scene'].render.filepath = \"" + outfilename +"\""
    tmp_bpy_file_fd.write(bpy)
    tmp_bpy_file_fd.flush()
    tmp_bpy_file_fd.close()

    blender_cmd = "blender_beta -b "+ filename +" --python "+ tmp_bpy_file +" -s "+ str(s) +" -e "+ str(e) +" -a"
    print (blender_cmd)
    p = subprocess.Popen(blender_cmd,shell=True)
    p.wait()
    filename_no = filename_no + 1
    filesrendered.append(outfilename)
    try:
      os.remove(tmp_bpy_file)
    except:
      print (sys.exc_info())
    if(getlost):
      break

concat_list_file = os.path.join(tempdir,"ffmpeg_file_list.txt")
concat_list_file_fd = open(concat_list_file,"w")
if(filesrendered):
  for x in filesrendered:
    concat_list_file_fd.write("file\t\'"+ x +"\'\n")
concat_list_file_fd.flush()
concat_list_file_fd.close()
ffmpegCmd = "ffmpeg -auto_convert 1 -f concat -safe 0 -i "+ concat_list_file + " -c copy "+ os.path.join(outputpath,outfile) +".mov"
print (ffmpegCmd)
f = subprocess.Popen(ffmpegCmd,shell=True)
f.wait()





