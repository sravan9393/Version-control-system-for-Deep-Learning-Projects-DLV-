import global_config
import os
import sys
import json
import shutil
import status

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

  cmd_parser.set_defaults(func=init)


print(1)
print(2)

def init(args):

    if args.repo_dir != None:
        global_config.create_repository(args.repo_dir)

    dlv_dir = os.path.join(global_config.root_dir, global_config.DLV_DIR)

    if os.path.isdir(dlv_dir):
        if args.force:
            for folder, subfolders, files in os.walk(dlv_dir):
                for f in files:
                    os.remove(os.path.join(folder, f))
        else:
            print("{repo} exists. Use '-f' to force create or remove " + dlv_dir + " directory")
            sys.exit()

    global_config.create_dlv_dir()
    global_config.set_branch(global_config.MASTER_BRANCH)
    

    status.status()
