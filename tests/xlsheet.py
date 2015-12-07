#!/usr/bin/python

import xlsxwriter
import os
import sys

dirSelf = os.path.dirname(os.path.realpath(__file__))
print(dirSelf)
sys.path.append(dirSelf.rstrip(os.sep).rstrip("tests").rstrip(os.sep) + os.sep + "rbhus")

import dbPipe
import constantsPipe


project = sys.argv[1].rstrip().lstrip()
print(project)
dbconn = dbPipe.dbPipe()

# get list of all the assets with a name and stage model
try:
  assetsLib = dbconn.execute("select * from assets where projName = '"+ str(project) +"' and assetType = 'library' and assName != 'default' and stageType = 'model'",dictionary=True)
except:
  print(str(sys.exc_info()))


# get a list of all the seq/scns
try:
  assetsSeqScns = dbconn.execute("select * from assets where projName = '"+ str(project) +"' and sequenceName != 'default' and sceneName != 'default'",dictionary=True)
except:
  print(str(sys.exc_info()))


assnames = {}
stagesNodesLibrary = {}
stagesNodesLibrary['model'] = ['assetDesign','geom','lookdev','rig']

seqScnNodesLibrary= {}
seqScnNodesLibrary['anim'] = ['previz','secondary','primary']
seqScnNodesLibrary['fx'] = ['secondary','primary']
seqScnNodesLibrary['model'] = ['layout']






if(not isinstance(assetsLib, int)):
  for x in assetsLib:
    try:
      assnames[x['assName']].append(x)
    except:
      assnames[x['assName']] = []
      assnames[x['assName']].append(x)
else:
  sys.exit(1)





workbook  = xlsxwriter.Workbook('/tmp/filename.xlsx')
worksheet = workbook.add_worksheet("assets")
workseqscn = workbook.add_worksheet("seq_scn")

green_bg = workbook.add_format()
green_bg.set_pattern(1)  # This is optional when using a solid fill.
green_bg.set_bg_color('green')
green_bg.set_border()
green_bg.set_border_color('black')

red_bg = workbook.add_format()
red_bg.set_pattern(1)  # This is optional when using a solid fill.
red_bg.set_bg_color('red')
red_bg.set_border()
red_bg.set_border_color('black')


orange_bg = workbook.add_format()
orange_bg.set_pattern(1)  # This is optional when using a solid fill.
orange_bg.set_bg_color('orange')
orange_bg.set_border()
orange_bg.set_border_color('black')

worksheet.write(0,0, 'Asset')
j = 1
lensn = []
for x in stagesNodesLibrary['model']:
  pstr = "model."+ str(x)
  worksheet.write(0,j,pstr)
  worksheet.set_column(j,j,len(pstr))
  # lensn.append(len(pstr))
  j = j + 1


def getStatus(asslist,stagetype,nodetype):
  for x in asslist:
    if(x['stageType'] == str(stagetype) and x['nodeType'] == str(nodetype)):
      return (x['progressStatus'],x['assignedWorker'],x['createDate'],x['dueDate'])
  return(None,None,None,None)

i = 1
lens = []
for x in assnames:
  lens.append(len(x))
  worksheet.write(i,0,x,orange_bg)
  j = 1
  for y in stagesNodesLibrary['model']:
    progress,user,cd,dd = getStatus(assnames[x],'model',y)
    if(progress != None):
      if(progress == constantsPipe.assetProgressInProgress):
        worksheet.write(i,j,user,red_bg)
      else:
        worksheet.write(i,j,user,green_bg)
      worksheet.write_comment(i,j,"Created Date : "+ str(cd).split()[0] +"\nDue Date : "+ str(dd).split()[0] +"")
    j += 1
  i = i+1
worksheet.freeze_panes(1, 1)
worksheet.set_column(0,0, max(lens))



for x in



workbook.close()