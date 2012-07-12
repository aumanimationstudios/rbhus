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
import db




def getHostGroups():
    try:
      conn = db.connRbhus()
      cursor = conn.cursor(db.dict)
      cursor.execute("select groups from hostInfo group by groups")
      rows = cursor.fetchall()
      cursor.close()
      conn.close()
    except:
      print("Error connecting to db")
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