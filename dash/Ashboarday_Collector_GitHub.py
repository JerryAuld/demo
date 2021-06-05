#-------------------------------------------------------
#
# Ashboarday GitHub Collector
# 
# Place in repository and run directly or set Action to run periodically.
# Takes direction from local json file "ashboaday.c.json" to read each listed folder
# and send the latest date to the dashboard's API to update its data.
#
# Jerry Auld, Otago Computing, 2021-06-05
#
#-------------------------------------------------------

import pathlib
import os
from datetime import datetime
import json
import urllib.request
import urllib.parse

#---------------  FUNCTIONS  ---------------------------

def getLatestDate(folder):
  # returns the latest date found in the folder's files as an ISO date string.
  latedate = datetime.now()
  fcount = 0
  fsize = 0
  kids = 0
  for f in os.scandir(folder):
    if f.is_dir():
      kids += 1
    else:
      fcount += 1
      (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(f)
      thisdate = datetime.fromtimestamp(mtime)
      fsize += size
      if thisdate < latedate:
        latedate = thisdate
      
  if fcount == 0:
    return "2009-01-01", fcount, fsize, kids
  else:
    return latedate.strftime("%Y-%m-%d"), fcount, fsize, kids
	
	
def getFolderData(folder, parent, order, level):
		
  # Get the folder data:
  result = getLatestDate(folder)
		
  # We must create this folder as a node on the dashboard before continuing, so we know the parent node ID for any children:
  sFolderPath = urllib.parse.quote_plus(folder.path)
  sFolderName = urllib.parse.quote_plus(folder.name)
  print("Sending "+folder.name+" ("+folder.path+")")
  nID = urllib.request.urlopen(dashapi+"&p=" + str(parent) + "&n=" + sFolderPath +"&f=" + str(result[1]) + "&l=" + str(level) + "&o=" + str(order) + "&k=" + str(result[3]) + "&s=GitHub&d=" + urllib.parse.quote_plus(result[0]) + "&z=" + str(result[2]) + "&i=" + sFolderName).read()
		
  # If we are not at depth and up to our width, process the child folders of this folder:
  order = 0
  level += 1
  if level < depth:
    for f in os.scandir(folder):
      if f.is_dir():
        order += 1
        if order <= width:
          if nID.isnumeric():
	          getFolderData(f, nID, order, level)
	        else:
            print("API Error: "+nID)
          return true
        else:
          return false

#-----------------  MAIN   -----------------------------

print("Python :: Running the Ashboarday Collector.")

# Get our guidance file:
if os.path.exists('dash/ashboarday.c.json'):
  
  with open('dash/ashboarday.c.json') as f:
    jsondata = json.load(f)

  dashapi = jsondata['Target']  # License is defined within this URL.
  root = "./"  # jsondata['Start']
  width = 99 #jsondata['Width']
  depth = 4 #jsondata['Depth']

  f.close
	
  # Get all subdirectories in the current directory:
  iOrder = 0
  for f in os.scandir(root):
    if f.is_dir():
      iOrder += 1
      getFolderData(f, 0, iOrder, 1)
      
  print("SUCCESS: processing complete.")

else:
  print("ERROR: json guidance file is not found. Please place in the same folder as this script.")

#-------------------------------------------------------
