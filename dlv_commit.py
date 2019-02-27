import os
import sys
import hashlib

DLV_DIR = ".dlv"
CACHE_DIR = "cache"
STAGE_FILE = "stage"

# Default CONFIG Variables
#Should change in future to get the exact repository directory
root_dir = os.path.abspath(os.curdir)
dlv_dir = os.path.join(root_dir, DLV_DIR)
dlv_cache_dir = os.path.join(dlv_dir, CACHE_DIR)
dlv_stage_file = os.path.join(dlv_dir, STAGE_FILE)

def compute_md5_hash(file_name):
  md5_sum = hashlib.md5(open(file_name).read()).hexdigest()
  return md5_sum


stage_files = []
commit_temp_file = os.path.join(dlv_cache_dir, "commit_file.txt")

# ??? Recursively search for the directories ( create mutiple tree objects not just one )
#Open Stage file
#Create Tree object and add the BLOB contents to the tree object
#Add contents to the Commit object
#Remove the files from the stage file
with open(dlv_stage_file, 'r') as stage_file:
  for line in stage_file:
    line = line[:-1]
    md5_hash_value = compute_md5_hash(line)

    temp_f_path = os.path.join(dlv_cache_dir, "temp.txt")
    with open(temp_f_path, 'a') as temp_f:
      temp_f.write("file: " + line + "\n")
      temp_f.write("md5: " + md5_hash_value + "\n")
      temp_f.write("\n")

    # Rename temp file ( tree object ) to the actual hash value
    md5_hash_value = compute_md5_hash(temp_f_path)
    dlv_hash_dir = md5_hash_value[2:]
    dlv_hash_file = os.path.join(dlv_hash_dir, md5_hash_value[2:])
    os.rename(temp_f_path, dlv_hash_file)

    # create the commit object temporary file
    with open(commit_temp_file, 'a') as commit_file:
      commit_file.write("tree: ", md5_hash_value)

    # Rename temporary commit
    md5_hash_value = compute_md5_hash(commit_temp_file)
    dlv_hash_dir = md5_hash_value[2:]
    dlv_hash_file = os.path.join(dlv_hash_dir, md5_hash_value[2:])
    os.rename(commit_temp_file, dlv_hash_file)

    #Remove the commited files from the staging directory 
    stage_files.append(stage_file)

with open(dlv_stage_file, 'rw') as f:
  for line in f:
    if line not in stage_files:
      f.write(line)

