import os
import sys
import json
import hashlib
import global_config
import datetime
import string
import shutil
import status
import errno
import difflib
import re
import status

show_only_changes = False
show_only_file = None

def handle_options_diff(cmd_parser):

    cmd_parser.add_argument('-f', '--file',
                          dest='file',
                          nargs=1,
                          help="File name to compare")

    cmd_parser.add_argument('-c', '--changes',
                          dest='changes',
                          action="store_true",
                          help="show only the changes")

    cmd_parser.add_argument('-v', '--version',
                          dest='versions',
                          nargs='+',
                          help="Compare with the versions specified ")

    cmd_parser.add_argument('-d', '--dir',
                          action="store",
                          dest="root_dir",
                          help="Staus of the repository")

    cmd_parser.set_defaults(func=diff)

def print_file(file, start_line, end_line):

    for i in range(start_line, end_line):
        print(" " + file[i]),

def diff_files(file1, file2):

    text1 = open(file1).readlines()
    text2 = open(file2).readlines()

    matches = difflib.SequenceMatcher(
                  None, text1, text2).get_matching_blocks()

    diff = difflib.unified_diff(text1, text2)

    start_line = 0
    end_line = 0
    for line in diff:

        m0 = re.match(r'^@@ -(\d+),(\d+) +', line)
        if m0 and not show_only_changes:
            end_line = int(m0.group(1)) - 1
            print_file(text1, start_line, end_line)
            start_line = end_line + int(m0.group(2))
        else:
            print(line),

    if not show_only_changes:
        end_line = len(text1)
        print_file(text1, start_line, end_line)

    print("\n")

def compare_files(branch_path, commit_version_1, commit_version_2):
    global show_only_file

    files_dict_1 = {}
    with open(commit_version_1, 'r') as f:
        try:
            files_dict_1 = json.load(f)
        except: pass

    if commit_version_2 == "":
        for key, value in files_dict_1.items():

            if show_only_file and not key.endswith(show_only_file):
                continue

            file1 = os.path.join(branch_path, global_config.CACHE_DIR, key + "." + str(value))
            orig_file = os.path.join(global_config.root_dir, key)
            if not status.has_diff(orig_file, file1):
                text1 = open(orig_file).readlines()
                for line in text1:
                    print(line)
                continue

            print("Comparing File " + key + " local file and version" + str(value))
            diff_files(orig_file, file1)
        return

    files_dict_2 = {}
    with open(commit_version_2, 'r') as f:
        try:
            files_dict_2 = json.load(f)
        except: pass

    for key, value in files_dict_1.items():

        if show_only_file and not key == show_only_file:
            continue

        file1 = os.path.join(branch_path, global_config.CACHE_DIR, key + "." + str(value))
        file2 = os.path.join(branch_path, global_config.CACHE_DIR, key + "." + str(files_dict_2[key]))

        if not status.has_diff(file1, file2):
            text1 = open(file1).readlines()
            for line in text1:
                    print(line)
            continue
        print("Comparing file " + key + " with versions " + str(value) + " and " + str(files_dict_2[key]))
        diff_files(file1, file2)

def diff(args):
    global show_only_changes, show_only_file

    if args.root_dir != None:
        global_config.root_dir = args.root_dir

    if not global_config.check_dlv_exists():
        print("No dlv repository exists")
        sys.exit()

    current_branch = global_config.get_current_branch()
    branch_path = os.path.join(global_config.root_dir, global_config.DLV_DIR, current_branch)


    show_only_changes = args.changes
    if args.file:
        show_only_file = args.file[0]
        show_only_file = show_only_file.replace("\\\\", "\\")

    commit_version_1 = "" 
    commit_version_2 = ""
    if args.versions:
        if len(args.versions) > 2:
            print("You can compare only 2 versions")
            sys.exit(0)
        elif len(args.versions) == 2:
            if( args.versions[0] > args.versions[1] ):
                temp = args.versions[0]
                args.versions[0] = args.versions[1]
                args.versions[1] = temp
            commit_version_1 = os.path.join( branch_path, global_config.COMMIT_DIR, "commit." + str(args.versions[0]) ) 
            commit_version_2 = os.path.join( branch_path, global_config.COMMIT_DIR, "commit." + str(args.versions[1]) )
        elif len(args.versions) == 1:
            commit_version_1 = os.path.join( branch_path, global_config.COMMIT_DIR, "commit." + str(args.versions[0]) )
        else:
            commit_version_1 = global_config.get_last_commit_version_file(branch_path)

    else:
        commit_version_1 = global_config.get_last_commit_version_file(branch_path)

    compare_files(branch_path, commit_version_1, commit_version_2)

    
    
