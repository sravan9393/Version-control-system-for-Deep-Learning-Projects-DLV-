import os
import sys
import hashlib

DLV_DIR = ".dlv"
CACHE_DIR = "cache"
STAGE_FILE = "stage"

#Should change in future to get the exact repository directory
root_dir = os.path.abspath(os.curdir)
dlv_dir = os.path.join(root_dir, DLV_DIR) 
dlv_cache_dir = os.path.join(dlv_dir, CACHE_DIR)
dlv_stage_file = os.path.join(dlv_dir, STAGE_FILE)

file_name = sys.argv[1];

def is_already_staged(file_to_check):
  with open(dlv_stage_file) as f:
    for line in f:
      if file_to_check == line:
        return True

  return False

files_to_add = []
if os.path.isdir(file_name):
  for root, dirs, files in os.walk(str(file_name)):
    for f in files:
      #Ignore if file is already staged
      if is_already_staged(f):
        continue
      #Ignore if the file is in dlv_ignore_file
      #Ignore if the file is already tracked and not modified
      files_to_add.append(os.path.join(root_dir, root + f))
else:
  files_to_add.append(os.path.join(root_dir, file_name))

# Adding the BLOB object to the dlv directory
# ????? What in case of Large files ( deep learning data sets )
for f in files_to_add:
  md5_value = hashlib.md5(open(f).read()).hexdigest()
  hash_dir = md5_value[:2];
  hash_file = md5_value[2:]

  # Creating the hash directory and hash file
  dlv_hash_dir = os.path.join(dlv_cache_dir, hash_dir)
  dlv_hash_file = os.path.join(dlv_hash_dir, hash_file)
  os.mkdir(dlv_hash_dir)
  open(dlv_hash_file, 'a').close()
  
  #Copying the contents from the actual file to the dlv_hash file
  with open(f) as read_file:
    with open(dlv_hash_file, 'w') as write_file:
      for line in read_file:
        write_file.write(line)

  #Adding the files to the staging directory
  with open(dlv_stage_file, 'a') as stage_file:
    stage_file.write(f + "\n")

