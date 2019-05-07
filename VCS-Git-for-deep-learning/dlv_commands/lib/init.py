import global_config
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

  cmd_parser.add_argument('-d', '--dir',
                          action="store",
                          dest="root_dir",
                          help="Initialize Repository")

  cmd_parser.set_defaults(func=init)


def init(args):

    if args.repo_dir != None:
        global_config.create_repository(args.repo_dir)

    if args.root_dir != None:
        global_config.root_dir = args.root_dir

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
    global_config.create_branch(global_config.MASTER_BRANCH)
    global_config.set_branch(global_config.MASTER_BRANCH)

    # dlv config file
    dlv_config_file = os.path.join(dlv_dir, global_config.CONFIG_FILE)  

    project_model_name = os.path.basename(global_config.root_dir)
    config_dict = { 'project_name': project_model_name }
    with open(dlv_config_file, 'w') as f:
        f.write(json.dumps(config_dict, indent=4))  
