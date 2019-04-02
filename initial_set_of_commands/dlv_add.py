import os
import json
import hashlib
import global_c
import datetime
import string
#import inquirer

def handle_options_add(cmd_parser):
  
  cmd_parser.add_argument('-v', '--version',
                          help="version",
                          action="store_true")

  cmd_parser.add_argument('-d', '--dir_path',
                          dest='dir_path',
                          nargs='?',
                          help="directories or files for adding to staging area")

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
  
  cmd_parser.set_defaults(func=dlv_add)
  

def is_already_staged(file_to_check):
  with open(global_c.dlv_stage_file) as f:
    for line in f:
      if file_to_check == line:
        return True

  return False

"""
def take_inputs(dir_path):

  questions = [
                inquirer.Checkbox('model_file',
                    message="Select model(h5) file",
                    choices=[f for f in listdir(dir_path) if isfile(join(dir_path, f))],
                    ),
                inquirer.Checkbox('metadata_file',
                    message="Select metadata file",
                    choices=[f for f in listdir(dir_path) if isfile(join(dir_path, f))],
                    ),
                inquirer.Checkbox('image_files',
                    message="Select Images",
                    choices=[f for f in listdir(dir_path) if isfile(join(dir_path, f))],
                    ),
              ]
  answers = inquirer.prompt(questions)
  return answers
"""

def walk_dir_and_append_files(dir_path, files_to_add, dirs_dict):

  if dir_path == None:
    return

  if not os.path.isdir(dir_path):
    files_to_add.append(os.path.join(global_c.root_dir, dir_path))
    return

  for root, dirs, files in os.walk(str(dir_path)):
    for f in files:

      #Ignore if file is already staged
      if is_already_staged(f):
        continue

      files_to_add.append(os.path.join(global_c.root_dir, root, f))

    dirs_dict.update({ root : [dirs, files]})
        

def create_blob_object(file_name):

  #get hash value
  hash_value = hashlib.md5(open(file_name).read()).hexdigest()
  hash_dir = hash_value[:2]
  hash_file = hash_value[2:]

  #create the hash files
  dlv_hash_dir = os.path.join(global_c.dlv_cache_dir, hash_dir)
  dlv_hash_file = os.path.join(dlv_hash_dir, hash_file)

  if not os.path.isdir(dlv_hash_dir):
    os.mkdir(dlv_hash_dir)

  if not os.path.exists(dlv_hash_file) or os.path.isfile(dlv_hash_file):
    open(dlv_hash_file, 'a').close()

    #copy the contents to the file
    with open(file_name, 'r') as read_file:
      with open(dlv_hash_file, 'w') as write_file:
        for line in read_file:
          write_file.write(line)

  add_header_to_object(file_name, dlv_hash_file)

  return hash_value

def add_header_to_object(original_file_name, file_name):

  now = datetime.datetime.now()
  with open(file_name, 'r+') as fp:
    lines = fp.readlines()
    
    lines.insert(0, '#DLV_HEADER_START#' + '\n')
    lines.insert(1, 'Author:Sindhusha' + '\n')
    lines.insert(2, 'Time:' + str(now) + '\n')
    lines.insert(3, 'File Name:' + original_file_name + '\n')
    lines.insert(4, '#DLV_HEADER_END#' + '\n')

    fp.seek(0)
    fp.writelines(lines)

def add_sub_objects_addr(file_name, hash_value, type_of_object):
  if hash_value == '':
    return
  
  with open(file_name, 'a') as f:
    f.write(type_of_object + ": " + hash_value + '\n')

def create_tree_object(root, dirs_dict, file_hash_dict):
  dirs = dirs_dict[root][0]
  files = dirs_dict[root][1]

  # Create a temp file name
  temp_file = string.replace(root, '\\', '_')
  file_name = os.path.join(global_c.dlv_cache_dir, "temp_" + temp_file)

  # Creating tree object for sub directories
  if len(dirs) != 0:
    for dir_v in dirs:
      tree_hash_value = create_tree_object(os.path.join(root, dir_v), dirs_dict, file_hash_dict)
      add_sub_objects_addr(file_name, tree_hash_value, "tree")

  # Referencing files(blob objects) to the parent directory(tree object)
  for file_v in files:
    file_v = os.path.join(global_c.root_dir, root, file_v)
    add_sub_objects_addr(file_name, file_hash_dict[file_v], "blob")

  # Computing hash value and renaming the file
  #get hash value
  hash_value = hashlib.md5(open(file_name).read()).hexdigest()
  hash_dir = hash_value[:2]
  hash_file = hash_value[2:]

  #create the hash files
  dlv_hash_dir = os.path.join(global_c.dlv_cache_dir, hash_dir)
  dlv_hash_file = os.path.join(dlv_hash_dir, hash_file)

  if not os.path.isdir(dlv_hash_dir):
    os.mkdir(dlv_hash_dir)

  if not os.path.exists(dlv_hash_file) and not os.path.isfile(dlv_hash_file):
    os.rename(file_name, dlv_hash_file)

  root = os.path.join(global_c.root_dir, root)
  file_hash_dict.update({ root : hash_value })
  add_header_to_object(root, dlv_hash_file)

  return hash_value


def dlv_add(args):

  #Initialize global configs
  global_c.set_defaults()

  dir_path = args.dir_path
  model_file = args.model_file
  metadata_file = args.metadata_file
  image_files = args.image_files
  
  files_to_add = []
  dirs_dict = {}

  # Get list of files to added to the cache/staging area
  walk_dir_and_append_files(dir_path, files_to_add, dirs_dict)
  walk_dir_and_append_files(model_file, files_to_add, dirs_dict)
  walk_dir_and_append_files(metadata_file, files_to_add, dirs_dict)
  walk_dir_and_append_files(image_files, files_to_add, dirs_dict)
  

  file_hash_dict = {}
  
  # Adding the BLOB object to the dlv directory
  for f in files_to_add:
    
    hash_value = create_blob_object(f)
    file_hash_dict.update({ f : hash_value})

  # Adding TREE object to the dlv directory
  tree_hash_value = create_tree_object(dir_path, dirs_dict, file_hash_dict)

  saved_dict = {}
  #Adding the files to the staging directory
  with open(global_c.dlv_stage_file, 'r') as stage_file:
    saved_dict = json.load(stage_file)
    file_hash_dict.update(saved_dict)
    
  with open(global_c.dlv_stage_file, 'w') as stage_file:
    stage_file.write(json.dumps(file_hash_dict, indent=4))

  # Write the top most tree object reference( root directory ) to refs/master
  master = { 'tree': tree_hash_value}
  with open(global_c.dlv_master_file, 'r') as f:
    saved_dict = json.load(f)
    saved_dict.update(master)

  with open(global_c.dlv_master_file, 'w') as f:
    f.write(json.dumps(saved_dict, indent=4))
    
