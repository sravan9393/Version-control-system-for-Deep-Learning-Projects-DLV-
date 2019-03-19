import os
import sys
import errno
import json
import hashlib
import global_config
import shutil
import datetime
import status

def handle_options_commit(cmd_parser):

    cmd_parser.add_argument('-v', '--version',
                          help="version",
                          action="store_true")

    cmd_parser.add_argument('-a','--author',
                          nargs=1,
                          dest='author',
                          help='Enter the author address')    

    cmd_parser.add_argument('-m','--message',
                          nargs=1,
                          dest='message',
                          help='Enter commit description')

    cmd_parser.set_defaults(func=commit)

def copy_to_cached_dir(orig_file, cache_file, branch_path):

    if orig_file.startswith(".\\"): # only modify the text if it starts with the prefix
        orig_file = orig_file.replace(".\\", "", 1) # remove one instance of prefix
        
    commit_file = os.path.join(branch_path, global_config.CACHE_DIR, cache_file)

    try:
        shutil.copy2(orig_file, commit_file)

    except IOError as e:
        if e.errno != errno.ENOENT:
            raise

        try:   
            os.makedirs(os.path.dirname(commit_file))
        except: pass

        shutil.copy2(orig_file, commit_file)

def clear_staged_file(branch_path):

    stage_dir = os.path.join(branch_path, global_config.STAGE_DIR, ".")

    for root, dirs, files in os.walk(stage_dir):
        for f in files:
            os.remove(os.path.join(root, f))
    

def create_commit_file(branch_path, commit_version, commit_files_versions):

    commit_file = os.path.join(branch_path, global_config.COMMIT_DIR, "commit." + str(commit_version))

    with open(commit_file, 'w') as f:
        f.write(json.dumps(commit_files_versions, indent=4))


def load_commit_file(branch_path):

    last_commit = global_config.get_last_commit_version_file(branch_path)

    if not os.path.exists(last_commit):
        return {}
        
    with open(last_commit, 'r') as f:
        return json.load(f)
        

def update_commit_log(branch_path, commit_file, commit_log_dict):

    currentDT = datetime.datetime.now()
    commit_log_dict['date'] = str(currentDT)
    
    commit_log_file = os.path.join(branch_path, global_config.COMMIT_LOG_FILE)

    commit_files = {}
    if os.path.exists(commit_log_file):
        with open(commit_log_file, 'r') as f:
            try:
                commit_files = json.load(f)
            except: pass

    commit_files[commit_file] = commit_log_dict

    with open(commit_log_file, 'w') as f:
        f.write(json.dumps(commit_files, indent=4))
        

def commit(args):
     
    if not global_config.check_dlv_exists():
        print("No dlv repository exists")
        sys.exit()

    if( args.message == None or args.author == None ):
        print("Please specify commit message and author name")
        sys.exit(0)

    current_branch = global_config.get_current_branch()
    branch_path = os.path.join(global_config.root_dir, global_config.DLV_DIR, current_branch)

    commit_files_versions = {}
    commit_files_versions = load_commit_file(branch_path)

    stage_dir = os.path.join(branch_path, global_config.STAGE_DIR)

    changed_files = []
    for folder, subfolders, files in os.walk( os.curdir ):

        if global_config.DLV_DIR in folder:
            continue

        for f in files:
            orig_file = os.path.join(folder, f)
            file_version = global_config.get_last_file_version(branch_path, orig_file)

            if file_version == 0:
                file_version += 1
                copy_to_cached_dir(orig_file, orig_file + "." + str(file_version), branch_path)
                changed_files.append(orig_file)
            else:    
                last_commit_file = os.path.join(branch_path, global_config.CACHE_DIR, orig_file + "." + str(file_version))

                if os.path.exists(last_commit_file) and status.has_diff(orig_file, last_commit_file):
                    file_version += 1
                    copy_to_cached_dir(orig_file, orig_file + "." + str(file_version), branch_path)
                    changed_files.append(orig_file)

            commit_files_versions[orig_file] = file_version

    # Write the commit file
    commit_version = global_config.commit_counter(branch_path)

    if len(changed_files) != 0:
        # Write Commit log file
	commit_log_dict = { 'message': args.message[0], 'author': args.author[0], 'changed_files': changed_files }
        update_commit_log(branch_path, "commit." + str(commit_version), commit_log_dict)

        create_commit_file(branch_path, commit_version, commit_files_versions)
	print("Committed to branch name: " + current_branch + " with version: " + str(commit_version))
    else:
        print("All staged files already tracked")

    clear_staged_file(branch_path)
