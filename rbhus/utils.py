import sys
import os

progPath =  sys.argv[0].split(os.sep)
print progPath
if(len(progPath) > 1):
  pwd = os.sep.join(progPath[0:-1])
  cwd = os.path.abspath(pwd)
else:
  cwd = os.path.abspath(os.getcwd())

sys.path.append(cwd.rstrip(os.sep) + os.sep)
import dbRbhus


dbconn = dbRbhus.dbRbhus()

def getHostGroups():
  try:
    rows = dbconn.execute("select groups from hostInfo group by groups", dictionary=True)
  except:
    print("Error connecting to db 1")
    return(0)
  gtr = {}
  retRows = []
  if(rows):
    for row in rows:
      tmpRow = row['groups'].split(",")
      for tr in tmpRow:
        gtr[tr.rstrip().lstrip()] = 1
    for gt in gtr.keys():
      retRows.append(gt)
    return(retRows)
  else:
    return(0)
      
def getFileTypes():
  try:
    rows = dbconn.execute("select * from fileType", dictionary=True)
  except:
    print("Error connecting to db 2")
    return(0)
  retRows = []  
  if(rows):
    for row in rows:
      retRows.append(row['fileType'])
    return(retRows)
  else:
    return(0)
    
def getRenderers():
  try:
    rows = dbconn.execute("select * from renderer", dictionary=True)
  except:
    print("Error connecting to db 2")
    return(0)
  retRows = {}  
  if(rows):
    for row in rows:
      try:
        retRows[row['fileType']].append(row['renderer'])
      except:
        retRows[row['fileType']] = []
        retRows[row['fileType']].append(row['renderer'])
    return(retRows)
  else:
    return(0)
    
def getOsTypes():
  try:
    rows = dbconn.execute("select os from hostInfo group by os", dictionary=True)
  except:
    print("Error connecting to db 1")
    return(0)
  otr = {}
  retRows = []
  if(rows):
    for row in rows:
      tmpRow = row['os'].split(",")
      for tr in tmpRow:
        otr[tr.rstrip().lstrip()] = 1
    for gt in otr.keys():
      retRows.append(gt)
    return(retRows)
  else:
    return(0)
      