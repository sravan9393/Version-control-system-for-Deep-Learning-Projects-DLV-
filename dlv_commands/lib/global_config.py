import os
import json
import re
import zipfile

DLV_DIR = ".dlv"

CONFIG_FILE = "config.txt"  # to store the file storage details
HEAD_FILE = "HEAD.txt"   # to point to the current branch address

MASTER_BRANCH = "master"   # default branch ( main branch )

CACHE_DIR = "cache"    # Stores different versions of files
STATUS_FILE = "status.txt"   # Stores the status of the file
STAGE_DIR = "stage"   # Stores the files added to the staging area

COMMIT_DIR = "commits"   # Stores different commits made by the user
COMMIT_LOG_FILE = "commit_log.txt"   # Stores the commit message for each commit

root_dir = os.path.abspath(os.curdir)
 

def create_directory(dir_path):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    elif os.path.isfile(dir_path):
        print("Can't create directory, file exists with the same name")
        return False

    return True

def create_empty_file(file_name):
    if not os.path.exists(file_name):
        open(file_name, 'a').close()
    elif os.path.isdir(file_name):
        print("Can't create a file, directory exists with the same name")
        return False
    
    return True
    

def create_repository(dir_name):
    global root_dir
    
    root_dir = os.path.abspath(dir_name)
    create_directory(root_dir)


def create_dlv_dir():

    dlv_dir_path = os.path.join(root_dir, DLV_DIR)

    dlv_config_file = os.path.join(dlv_dir_path, CONFIG_FILE)
    dlv_head_file = os.path.join(dlv_dir_path, HEAD_FILE)

    create_directory(dlv_dir_path)

    create_empty_file(dlv_config_file)
    create_empty_file(dlv_head_file)

def check_dlv_exists():

    if os.path.isdir(os.path.join(root_dir, DLV_DIR)):
        return True
    
    return False

def set_branch(branch_name):

    dlv_head_file = os.path.join(root_dir, DLV_DIR, HEAD_FILE)
    
    with open(dlv_head_file, 'w') as f:
        f.write(branch_name)

def get_current_branch():

    dlv_head_file = os.path.join(root_dir, DLV_DIR, HEAD_FILE)

    with open(dlv_head_file, 'r') as f:
        lines = f.readlines()

    return lines[0]

def create_branch(branch_name):

    dlv_master_path = os.path.join(root_dir, DLV_DIR, MASTER_BRANCH)

    dlv_cache_dir = os.path.join(dlv_master_path, CACHE_DIR)
    dlv_status_file = os.path.join(dlv_master_path, STATUS_FILE)
    dlv_stage_dir = os.path.join(dlv_master_path, STAGE_DIR)

    dlv_commit_dir = os.path.join(dlv_master_path, COMMIT_DIR)
    dlv_commit_log_file = os.path.join(dlv_master_path, COMMIT_LOG_FILE)

    create_directory(dlv_master_path)
    create_directory(dlv_cache_dir)
    create_directory(dlv_stage_dir)
    create_directory(dlv_commit_dir)

    create_empty_file(dlv_status_file)
    create_empty_file(dlv_commit_log_file)

def commit_counter(branch_path):
    commit_count = 0
    commit_dir = os.path.join( branch_path, COMMIT_DIR)
    for folder, subfolders, files in os.walk(commit_dir):
        for f in files:
            result = re.match(".*\.(\d+)", f)
            if result:
                current_commit = int(result.group(1))
                if current_commit > commit_count:
                    commit_count = current_commit


    commit_count += 1
    return commit_count

def get_last_commit_version_file(branch_path):
    
    last_commit_number = commit_counter(branch_path) - 1
    last_commit_file = os.path.join( branch_path, COMMIT_DIR, "commit." + str(last_commit_number) )

    return last_commit_file

def get_last_file_version(branch_path, file_name):

    last_commit_file = get_last_commit_version_file(branch_path)

    version = 0
    tracked_files = {}
    if not os.path.exists(last_commit_file):
        return version

    with open(last_commit_file, 'r') as f:
        tracked_files = json.load(f)

    if file_name in tracked_files.keys():
        version = tracked_files[file_name]

    return version

def compress_file(file_name, dest_file_path):
    fantasy_zip = zipfile.ZipFile(dest_file_path, 'w')
        
    for folder, subfolders, files in os.walk(file_name):
             
        for file in files:
            fantasy_zip.write(os.path.join(folder, file),
                                  os.path.relpath(os.path.join(folder,file), file_name),
                                  compress_type = zipfile.ZIP_DEFLATED)
    
    fantasy_zip.close() 

