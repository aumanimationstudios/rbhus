#!/usr/bin/python

import xlsxwriter
import os
import sys

dirSelf = os.path.dirname(os.path.realpath(__file__))
print(dirSelf)
sys.path.append(dirSelf.rstrip(os.sep).rstrip("tests").rstrip(os.sep) + os.sep + "lib")

import dbPipe


project = sys.argv[1]
dbconn = dbPipe.dbPipe()

try:
  rows = dbconn.execute("select * from assets where projName = '"+ str(project) +"'")
except:
  print(str(sys.exc_info()))
  return(0)




workbook  = xlsxwriter.Workbook('/tmp/filename.xlsx')
worksheet = workbook.add_worksheet("assets")

green_bg = workbook.add_format()
green_bg.set_pattern(1)  # This is optional when using a solid fill.
green_bg.set_bg_color('green')

red_bg = workbook.add_format()
red_bg.set_pattern(1)  # This is optional when using a solid fill.
red_bg.set_bg_color('red')





worksheet.write(0,0, 'Hello Excel',green_bg)
worksheet.write(0,1, 'Hello Excel',red_bg)

workbook.close()