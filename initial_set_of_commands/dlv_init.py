import global_c
import os
import sys
import json
import shutil

def handle_options_init(cmd_parser):
  
  cmd_parser.add_argument('-v', '--version',
                          help="version",
                          action="store_true")

  cmd_parser.add_argument('-f', '--force',
                          dest="force",
                          help="to force remove and create new one",
                          action="store_true")

  cmd_parser.add_argument('-r', '--repo',
                          action="store",
                          dest="repo_dir",
                          help="create repository and initialize")  

  cmd_parser.set_defaults(func=dlv_init)

def dlv_init(args):
  
  if args.repo_dir == None:
    global_c.set_defaults()
  else:
    global_c.set_defaults(args.repo_dir)
  
  if os.path.isdir(global_c.dlv_dir):
    if args.force:
      shutil.rmtree(global_c.dlv_dir)
    else:
      print("{repo} exists. Use '-f' to force create or remove " + global_c.dlv_dir + " directory")
      sys.exit()

  # Create dirs -
  #       .dlv  - Creating .dlv directory for tracking the meta data of the files,
  #       cache - Creating cache dir for storing the BLOB hash files( physical files ) in this directory,
  #       refs  - Gives information about the last commit ( for each branch )
  
  dirs = [global_c.dlv_dir, global_c.dlv_cache_dir,
          global_c.dlv_refs_dir]
  for dir in dirs:
    os.mkdir(dir)
  
  # Create files -
  #        config - Creating config dir for storing the information of the repository and storage details like ( database location ),
  #        head - Creating HEAD directory for pointing to the current branch,
  #        stage - Creating staging file to store the files added to the staging directory,
  #        refs/master - points to the latest commit in the branch
  
  files = [global_c.dlv_config_file, global_c.dlv_head_file,
           global_c.dlv_stage_file, global_c.dlv_master_file]
  for file in files:
    open(file, 'a').close()

  # Pointing HEAD to the master branch address
  with open(global_c.dlv_head_file, 'w') as f:
    f.write(global_c.dlv_master_file)

  # Setting config with the dictionary key value pair
  config = { 'url': '',
             'repository': '',
             'author': 'Sindhusha',
             'branch': { 'master': { 'path': global_c.dlv_master_file
                                     }
                         }
             }
  
  with open(global_c.dlv_config_file, 'w') as f:
    f.write(json.dumps(config, indent=4))

  # creating stage file
  stage = {}
  with open(global_c.dlv_stage_file, 'w') as f:
    f.write(json.dumps(stage, indent=4))

  master = {'tree': '',
            'commit': ''}
  with open(global_c.dlv_master_file, 'w') as f:
    f.write(json.dumps(master, indent=4))
