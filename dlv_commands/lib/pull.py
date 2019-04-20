import os
import sys
import json
import global_config

def handle_options_pull(cmd_parser):

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
                          help='Enter the project model name')

    cmd_parser.set_defaults(func=pull)

def pull(args = {}):

    if not global_config.check_dlv_exists():
        print("No dlv repository exists")
        sys.exit()

    dlv_dir = os.path.join(global_config.root_dir, global_config.DLV_DIR)

    current_branch = global_config.get_current_branch()
    branch_path = os.path.join(dlv_dir, current_branch)

    if get_push_status(current_branch) == "Updated":
       print("All files are up-to-date in the current branch: " + current_branch)
       sys.exit(0) 

    # Check for project name and the username
    # If no project name get the basename 
    # If no username request for the username
    dlv_config_file = os.path.join(dlv_dir, global_config.CONFIG_FILE)

    config_dict = {}
    with open(dlv_config_file, 'r') as f: 
        try: config_dict = json.load(f)
        except: pass

    if 'project_name' not in config_dict:
        config_dict['project_name'] = os.path.basename(global_config.root_dir)

    if 'username' not in config_dict and args.username == None:
        print("FATAL: Please enter the username");
        sys.exit(0)
    elif 'username' not in config_dict:
        config_dict['username'] = args.username[0]

    if 'description' not in config_dict and args.description == None:
        print("FATAL: Please enter the description of project");
        sys.exit(0)
    elif 'description' not in config_dict:
        config_dict['description'] = args.description[0]

    with open(dlv_config_file, 'w') as f:
        f.write(json.dumps(config_dict, indent=4))

    # Push the files to the specified user project directory locally
    # Check if the server directory exists and if not create it
    server_dir = global_config.SERVER_PROJECT_DIR
    if not global_config.create_directory(server_dir):
        print("Problem with the main server directory")
        sys.exit(0)    

    # Check if the user directory exists and if not create it
    user_dir = os.path.join(server_dir, config_dict['username'])
    if not global_config.create_directory(user_dir):
        print("Problem with the user directory in the server")
        sys.exit(0)

    # Check if the users project exists and if not upload whole files ( check which branch ) 
    project_dir = os.path.join(user_dir, config_dict['project_name'])
    
    if not global_config.create_directory(project_dir):
        print("Problem with the users project directory in the server")
        sys.exit(0)

    for root, dirs, files in os.walk(dlv_dir):
        
        # If folder is DLV_DIR then create dir within server and push all files
        if os.path.basename(root) == global_config.DLV_DIR:
            project_dlv_dir = os.path.join(project_dir, global_config.DLV_DIR)
            global_config.create_directory(project_dlv_dir)
            for f in files:
                shutil.copy(os.path.join(root, f), os.path.join(project_dlv_dir, f))

        # If folder is branch then create dir and push all files within it
        if os.path.basename(root) == current_branch:
            project_branch_dir = os.path.join(project_dir, global_config.DLV_DIR, current_branch)
            copy_tree(root, project_branch_dir)
