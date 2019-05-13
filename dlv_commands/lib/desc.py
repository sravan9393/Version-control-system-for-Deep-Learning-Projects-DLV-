import os
import sys
import json
import global_config
import pandas as pd

def handle_options_desc(cmd_parser):

    cmd_parser.add_argument('-v', '--version',
                          help="version",
                          action="store_true")

    cmd_parser.add_argument('-u','--username',
                          nargs=1,
                          dest='username',
                          help='Enter the author address')

    cmd_parser.add_argument('-m','--model',
                          nargs=1,
                          dest='model',
                          help='Enter the model to describe')

    cmd_parser.set_defaults(func=desc)


def get_project_description(project_path):
    
    config_file = os.path.join(project_path, global_config.DLV_DIR, global_config.CONFIG_FILE)
    config_dict = {}
    with open(config_file, 'r') as f:
        config_dict = json.load(f)

    return config_dict['description']


def get_history_of_files(project_path):

    files_history = {}
    current_branch = global_config.MASTER_BRANCH
    project_branch_path = os.path.join(project_path, global_config.DLV_DIR, current_branch)

    # open history file and get author message and date for each version
    commit_log_file = os.path.join(project_branch_path, global_config.COMMIT_LOG_FILE) 
    commit_history = {}

    with open(commit_log_file, 'r') as f:
        commit_history = json.load(f)

    # open last commit file and get list of files and versions
    last_commit_file = global_config.get_last_commit_version_file(project_branch_path)
    
    with open(last_commit_file, 'r') as f:
        last_commit_dict = json.load(f)
        for key in last_commit_dict.keys():
            files_history[key] = {}
            files_history[key]['version'] = last_commit_dict[key]
            files_history[key]['author'] = commit_history["commit." + str(last_commit_dict[key])]['author']
            files_history[key]['message'] = commit_history["commit." + str(last_commit_dict[key])]['message']
            files_history[key]['date'] = commit_history["commit." + str(last_commit_dict[key])]['date']

    # return the dictionary
    return files_history

def printTable(list_dict):

    if list_dict == {}:
        print("No model found in the user directory")

    for k,v in list_dict.iteritems():

        print(k + " => " + v['description'])
        print("{:<25} {:<4} {:<15} {:<15} {:<20}".format('file', 'version', 'author', 'message', 'date'))

        for key,val in v['files'].iteritems():
            print("{:<25} {:<4} {:<15} {:<15} {:<20}".format(key, val['version'], val['author'], val['message'], val['date']))
    
        print("\n\n")

def desc(args = {}):

    # Check whether the username is specified or not
    if args.username == None:
        print("FATAL: Please specify the username to list the projects")
        sys.exit(0)

    # Check whether the username is there is on server or not
    user_server_dir = os.path.join(global_config.SERVER_PROJECT_DIR, args.username[0])
    
    if not os.path.isdir(user_server_dir):
        print("Invalid Username")
        sys.exit(0)

    list_dict = {} # containes the list of projects and its lineages

    # Get list of all projects in the user dir
    for folder in os.listdir(user_server_dir):

         if not folder == args.model[0]:
             continue
         list_dict[folder] = {}

         # For each project get the description
         project_path = os.path.join(user_server_dir, folder)
         list_dict[folder]['description'] = get_project_description(project_path)
         
         # For each project get the history ( file, version, author, message, date )
         list_dict[folder]['files'] = get_history_of_files(project_path)

    printTable(list_dict)
