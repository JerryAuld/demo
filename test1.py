from pathlib import Path

print("Running the Ashboarday Updater in python.")

p = Path('./')

# All subdirectories in the current directory, not recursive.
# [f for f in p.iterdir() if f.is_dir()]

subfolders = [ f.path for f in os.scandir('./') if f.is_dir() ]
print(subfolders)
