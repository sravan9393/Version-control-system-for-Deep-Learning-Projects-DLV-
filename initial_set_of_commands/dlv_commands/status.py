import os
import sys
import json
import global_config
import hashlib

def handle_options_status(cmd_parser):

    cmd_parser.add_argument('-v', '--version',
                          help="version",
                          action="store_true")

    cmd_parser.set_defaults(func=status)

def write_status_to_file(status_file, current_status):
    with open(status_file, 'w') as f:
        f.write(json.dumps(current_status))

def has_diff(file1, file2):
    hash_value1 = hashlib.md5(open(file1).read()).hexdigest()
    hash_value2 = hashlib.md5(open(file2).read()).hexdigest()

    return hash_value1 != hash_value2

def get_status(orig_file):

    current_branch = global_config.get_current_branch()
    branch_path = os.path.join(global_config.root_dir, global_config.DLV_DIR, current_branch)

    index_file = os.path.join(branch_path, global_config.STAGE_DIR, orig_file)

    file_version = str(global_config.get_last_file_version(branch_path, orig_file))
    last_commit_file = os.path.join(branch_path, global_config.CACHE_DIR, orig_file + "." + file_version)

    if os.path.exists(orig_file):
        if os.path.exists(index_file):
            if has_diff(orig_file, index_file):
                return "Modified Files"
            else:
                return "Staged Files"
        elif os.path.exists(last_commit_file):
            if has_diff(orig_file, last_commit_file):
                return "Modified Files"
            else:
                return "Tracked Files"
        else:
            return "Untracked Files"
    else:
        return "Deleted Files" # this case never happens - check from commit history log      

def print_status(file_status):
    for status in file_status.keys():
        print(status)
        for f in file_status[status]:
            print("\t" + f)
        print("\n")

def status(args = {}):

    if not global_config.check_dlv_exists():
        print("No dlv repository exists")
        sys.exit()

    current_branch = global_config.get_current_branch()
    branch_path = os.path.join(global_config.root_dir, global_config.DLV_DIR, current_branch)

    status_log = os.path.join(branch_path, global_config.STATUS_FILE)

    file_status = {}
    file_status["Untracked Files"] = []
    file_status["Modified Files"] = []
    file_status["Deleted Files"] = []
    file_status["Staged Files"] = []
    file_status["Tracked Files"] = []

    for folder, subfolders, files in os.walk( os.curdir ):

        if global_config.DLV_DIR in folder:
            continue

        for f in files:
            orig_file = os.path.join(folder, f)
            file_status[get_status(orig_file)].append(orig_file)

    write_status_to_file(status_log, file_status)
    print_status(file_status)
    
