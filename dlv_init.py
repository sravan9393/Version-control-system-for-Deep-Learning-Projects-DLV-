import os
import sys

DLV_DIR = ".dlv"
CONFIG_FILE = "config"
CACHE_DIR = "cache"
HEAD_DIR = "HEAD"
STAGE_FILE = "stage"

root_dir = os.path.abspath(os.curdir)
dlv_dir = os.path.join(root_dir, DLV_DIR)
dlv_config_file = os.path.join(dlv_dir, CONFIG_FILE)
dlv_cache_dir = os.path.join(dlv_dir, CACHE_DIR)
dlv_head_dir = os.path.join(dlv_dir, HEAD_DIR)
dlv_stage_file = os.path.join(dlv_dir, STAGE_FILE)

if os.path.isdir(dlv_dir):
  print("{repo} exists. Use '-f' to force create or remove " + dlv_dir + " directory")
  sys.exit()

#Creating .dlv directory for tracking the meta data of the files
os.mkdir(dlv_dir)

# Creating config dir for storing the information of the repository and storage details like ( database location )
open(dlv_config_file, 'a') 

# Creating cache dir for storing the BLOB hash files( physical files ) in this directory
os.mkdir(dlv_cache_dir)

# Creating HEAD directory for pointing to the latest commit object
os.mkdir(dlv_head_dir)

# Creating staging fiel to store the files added to the staging directory
open(dlv_stage_file, 'a').close()
