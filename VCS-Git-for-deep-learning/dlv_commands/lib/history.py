import global_config
import os
import sys
import json
import shutil
import status

def handle_options_history(cmd_parser):

    cmd_parser.add_argument('-v', '--version',
                          help="version",
                          action="store_true")

    cmd_parser.add_argument('-d', '--dir',
                          action="store",
                          dest="root_dir",
                          help="Staus of the repository")

    cmd_parser.set_defaults(func=history)

def print_commit_log_file(branch_path):
    commit_log_file = os.path.join(branch_path, global_config.COMMIT_LOG_FILE)

    commit_files = {}
    if os.path.exists(commit_log_file):
        with open(commit_log_file, 'r') as f:   
            try:
                commit_files = json.load(f)
            except: pass

    print(json.dumps(commit_files, indent=4))

def history(args):

    if args.root_dir != None:
        global_config.root_dir = args.root_dir
    
    if not global_config.check_dlv_exists():
        print("No dlv repository exists")
        sys.exit()

    current_branch = global_config.get_current_branch()
    branch_path = os.path.join(global_config.root_dir, global_config.DLV_DIR, current_branch)

    print_commit_log_file(branch_path)    
