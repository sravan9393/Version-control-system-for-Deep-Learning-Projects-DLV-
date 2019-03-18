import os
import json
import hashlib
import global_c
import dlv_add

def handle_options_commit(cmd_parser):
  
  cmd_parser.add_argument('-v', '--version',
                          help="version",
                          action="store_true")

  cmd_parser.add_argument('-m','--model',
                          nargs='?',
                          dest='model_file',
                          help='Select model file( .h5 extension)')

  cmd_parser.add_argument('-M','--metadata',
                          nargs='?',
                          dest='metadata_file',
                          help='Select metadata file( .txt extension)')

  cmd_parser.add_argument('-i','--images',
                          nargs='*',
                          dest='image_files',
                          help='Select images')
  
  cmd_parser.set_defaults(func=dlv_commit)

def compute_md5_hash(file_name):
  hash_value = hashlib.md5(open(file_name).read()).hexdigest()
  return hash_value


#Open Stage file
#Create Commit object ( also reference previous commit file in refs/branch
#Add contents to the Commit object
#Remove the files from the stage file
def dlv_commit(args):

  global_c.set_defaults()

  #Get the current branch
  current_branch = ''
  with open(global_c.dlv_head_file, 'r') as f:
    for line in f:
      current_branch = line

  # Get the root tree object hash value
  tree_hash_value = ''
  previous_commit_version = ''
  with open(global_c.dlv_master_file) as f:
    dict_v = json.load(f)

  tree_hash_value = dict_v['tree']
  previous_commit_version = dict_v['commit']

  # Create temp file and add the contents
  temp_file_name = os.path.join(global_c.dlv_cache_dir + "temp.txt")
  dlv_add.add_sub_objects_addr(temp_file_name, tree_hash_value, 'tree')
  dlv_add.add_sub_objects_addr(temp_file_name, previous_commit_version, 'parent')

  # Reference all files by opening stage file

  # Rename the temp file to hash object
  #get hash value
  hash_value = hashlib.md5(open(temp_file_name).read()).hexdigest()
  hash_dir = hash_value[:2]
  hash_file = hash_value[2:]
  
  dlv_hash_dir = os.path.join(global_c.dlv_cache_dir, hash_dir)
  dlv_hash_file = os.path.join(dlv_hash_dir, hash_file)

  if not os.path.isdir(dlv_hash_dir):
    os.mkdir(dlv_hash_dir)

  if not os.path.exists(dlv_hash_file) or os.path.isfile(dlv_hash_file):
    os.rename(temp_file_name, dlv_hash_file)

  # Adding header
  dlv_add.add_header_to_object('commit object', dlv_hash_file)
    
  #Remove stage file

  # Add the recent commit object to the main head file
  dlv_branch_file = os.path.join(global_c.dlv_dir, current_branch)
  with open(dlv_branch_file, 'w') as f:
    f.write(hash_value)
