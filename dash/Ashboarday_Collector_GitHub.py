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
  files = [ file.path for file in os.scandir(folder) ]
  for f in files:
    if file.is_dir():
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
	
	
def getFolderData(folder, parent, order, level);

  if folder.is_dir():
		
    # Get the folder data:
    result = getLatestDate(folder)
		
    # We must create this folder as a node on the dashboard before continuing, so we know the parent node ID for any children:
    nID = urllib.request.urlopen(dashapi+"?p=" + parent + "&n=" + urllib.parse.quote_plus(folder) +"&f=" + str(result[1]) + "&l=" + str(level) + "&o=" + order + "&k=" + result[3] + "&s=GitHub&d=" + urllib.parse.quote_plus(result[0]) + "&z=" + str(result[2]) + "&i=" + urllib.parse.quote_plus(folder)).read()
		
    # If we are not at depth and up to our width, process the child folders of this folder:
    subfolders = [ f.path for f in os.scandir(folder) if f.is_dir() ]
    iOrder = 0
    level += 1
    if level < depth:
      for f in subfolders:
        if f.is_dir():
          iOrder += 1
          if iOrder <= width:
            getFolderData(folder."/".f, nID, $iOrder, level)
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
  root = jsondata['Start']
  width = jsondata['Width']
  depth = jsondata['Depth']

  f.close

  # Position ourselves at the start folder. We do not collect this folder, just its children.
  if root.is_dir():
	
    # Get all subdirectories in the current directory:
    subfolders = [ f.path for f in os.scandir(root) if f.is_dir() ]
    iOrder = 0
	
    for f in subfolders:
      if f.is_dir():
        iOrder += 1
        getFolderData(root."/".f, 0, $iOrder, 1)
        print("SUCCESS: processing complete.")
	
  else:
    print("ERROR: specified root is not a directory.")
else:
  print("ERROR: json guidance file is not found. Please place in the same folder as this script.")

#-------------------------------------------------------
