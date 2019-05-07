import os
import sys
import json
import hashlib
import global_config
import datetime
import string
import status
import shutil
import errno

def handle_options_add(cmd_parser):
    cmd_parser.add_argument('-v', '--version',
                          help="version",
                          action="store_true")

    cmd_parser.add_argument('-d', '--dir_path',
                          dest='dir_path',
                          nargs='+',
                          help="directories or files for adding to staging area")

    cmd_parser.set_defaults(func=add)

def copy_to_staged_file(file_path, branch_path):
    
    staged_file = os.path.join(branch_path, global_config.STAGE_DIR, file_path)
    try:
        shutil.copy2(file_path, staged_file)

    except IOError as e:
        if e.errno != errno.ENOENT:
            raise
                    
        os.makedirs(os.path.dirname(staged_file))
        shutil.copy2(file_path, staged_file)

def add(args):

    if not global_config.check_dlv_exists():
        print("No dlv repository exists")
        sys.exit()

    current_branch = global_config.get_current_branch()
    branch_path = os.path.join(global_config.root_dir, global_config.DLV_DIR, current_branch)

    for dir_path in args.dir_path:

        # Check if the dir or file exists or not
        if os.path.isfile(dir_path):
            copy_to_staged_file(dir_path, branch_path)
            
        # walk over each file in the dir
        for folder, subfolders, files in os.walk(str(dir_path)):

            if global_config.DLV_DIR in folder:
                continue
            
            for f in files:
                file_path = os.path.join(folder, f)
                if not status.get_status(file_path) == "Tracked Files":
                    copy_to_staged_file(file_path, branch_path)

    status.status()
    
