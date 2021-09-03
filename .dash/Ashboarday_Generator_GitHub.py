#-------------------------------------------------------
#
# Ashboarday GitHub Generator
# 
# Place in repository and run directly (once) or with a one-off Action.
# Takes direction from local json file "ashboaday.g.json" to create each listed folder
# and a placeholder file (placeholder.txt).
#
# Jerry Auld, Otago Computing, 2021-09-03
#
#-------------------------------------------------------

import pathlib
import os
from datetime import datetime
import json
import urllib.request
import urllib.parse
import subprocess

#---------------  FUNCTIONS  ---------------------------

def createFolder(fID,folder):
  print("Creating "+folder)
  # Create directory if not exists
  if os.path.isdir(folder) == False:
    try:
      os.makedirs(folder)
    except OSError:
      print ("Creation of the directory %s failed" % folder)
    else:
      print ("Successfully created the directory %s" % folder)

  # Create the placeholder file:
  file_text = "This is a placeholder file. Please delete."
  f_w = open(folder+"/placeholder.txt", "w")
  f_w.write(file_text)
  f_w.close()
  
  # Recurse for any child folders:
  for n in nodes:
    if n[1] == fID:
      createFolder(n[0],folder+"/"+n[2])
    
#-----------------  MAIN   -----------------------------

print("Python :: Running the Ashboarday Generator.")

# Get our guidance file:
if os.path.exists('.dash/ashboarday.g.json'):
  
  with open('.dash/ashboarday.g.json') as f:
    jsondata = json.load(f)

  dash = jsondata['Target']  # License is defined within this URL. We don't actually need this when generating.
  nodes = jsondata['Nodes']
  print(nodes)

  f.close
	
  # We create from the root directory.
  # Create all directories that have no parent, and recurse down for each.
  for n in nodes:
    if n[1] == 0:
      createFolder(n[0],n[2])	
  
  print("Set git config...")
  subprocess.Popen(["git", "config", "--global", "user.name", "github-actions[bot]"])
  subprocess.Popen(["git", "config", "--global", "user.email", "41898282+github-actions[bot]@users.noreply.github.com"])
  
  print("Push to remote...")
  subprocess.Popen(["git", "add", "-A"])
  subprocess.Popen(["git", "commit", "-m", "comment message"])
  subprocess.Popen(["git", "push"])
  
  print("SUCCESS: processing complete.")

else:
  print("ERROR: json guidance file is not found. Please place in the same folder as this script.")

#-------------------------------------------------------