#!/usr/bin/env python3

import tkinter as tk
from tkinter import filedialog

import shutil
import os
import subprocess
import json

from flask import Flask, request
from flask_cors import CORS

import sys
sys.path.append("lib")
sys.path.append("bin")



def copyDirectory(src, dest):
    try:
        shutil.copytree(src, dest)
    # Directories are the same
    except shutil.Error as e:
        print('Directory not copied. Error: %s' % e)
    # Any error saying that the directory doesn't exist
    except OSError as e:
        print('Directory not copied. Error: %s' % e)

app = Flask(__name__)

cors = CORS(app)
#app.config['CORS_HEADERS'] = 'application/json'
project_path = "E:\ASE_database"


@app.route("/upload", methods=['POST', 'GET'])
def uploadToServer():

    username = request.args['username']

    root = tk.Tk()
    root.withdraw()

    dirname = filedialog.askdirectory(parent=root,initialdir="/",title='Please select a directory')

    if dirname == None or dirname == "":
        return "No dir selected"

    
    dest_path = os.path.join(project_path, username, os.path.basename(dirname))
    copyDirectory(dirname, dest_path)

    os.system('python dlv init -d \"' + dest_path + '\"')
    os.system('python dlv commit -d \"' + dest_path + '\" -m \"Initial Commit\" -a \"' + username + '\"')
    return "success"

@app.route("/list", methods=['POST', 'GET'])
def vcsList():

    username = request.args['username']

    getOutput =  subprocess.Popen('python dlv list -u \"' + username + '\"', shell=True, stdout=subprocess.PIPE).stdout
    result =  getOutput.read()
    if result.decode().startswith("Invalid Username"):
        return ()

    return result.decode()


def getTree(dict_val, key, paths):
    output = []

    for f_name in dict_val[key]:
        tmp_dict = {}
        tmp_dict['name'] = f_name
        
        if f_name in dict_val:
            tmp_dict['children'] = getTree(dict_val, f_name, paths)
        elif f_name in paths:
            tmp_dict['path'] = paths[f_name]

        output.append(tmp_dict)
    return output

@app.route("/status", methods=['POST', 'GET'])
def vcsStatus():

    username = request.args['username']
    repository = request.args['repository']

    final_path = os.path.join(project_path, username, repository)
    getOutput =  subprocess.Popen('python dlv status --json -d \"' + final_path + '\"', shell=True, stdout=subprocess.PIPE).stdout
    result =  getOutput.read()

    output = json.loads(result.decode())
    modified_files = output["Modified Files"]
    modified_files.extend(output["Untracked Files"])
    final_data = []
    temp_dict = {}
    paths = {}
    for file in modified_files:

        folders = file.split('\\')
        key = 'root'
        index = 0
        while index < len(folders):
            if key not in temp_dict:
                temp_dict[key] = []

            if not folders[index] in temp_dict[key]:
                temp_dict[key].append(folders[index])

            key = folders[index]
            index += 1

        paths[folders[len(folders) - 1]] = file

    if len(modified_files) != 0:
        final_data = getTree(temp_dict, "root", paths)

    return json.dumps(final_data)

@app.route("/listoffiles", methods=['POST', 'GET'])
def vcsGetFiles():

    username = request.args['username']
    repository = request.args['repository']

    final_path = os.path.join(project_path, username, repository)
    getOutput =  subprocess.Popen('python dlv status --json -d \"' + final_path + '\"', shell=True, stdout=subprocess.PIPE).stdout
    result =  getOutput.read()

    output = json.loads(result.decode())
    modified_files = output["Tracked Files"]
    modified_files.extend(output["Modified Files"])
    final_data = []
    temp_dict = {}
    paths = {}
    
    for file in modified_files:

        folders = file.split('\\')
        key = 'root'
        index = 0
        while index < len(folders):
            if key not in temp_dict:
                temp_dict[key] = []

            if not folders[index] in temp_dict[key]:
                temp_dict[key].append(folders[index])

            key = folders[index]
            index += 1

        paths[folders[len(folders) - 1]] = file

    if len(modified_files) != 0:
        final_data = getTree(temp_dict, "root", paths)

    return json.dumps(final_data)

@app.route("/filediff", methods=['POST', 'GET'])
def vcsDiff():
    file_name = request.args['filename']
    username = request.args['username']
    repository = request.args['repository']

    root_dir = os.path.join(project_path, username, repository)

    tmp_file = os.path.join(root_dir, '.dlv', 'tmp.diff')
    foutput = open(tmp_file, 'w')
    getOutput =  subprocess.Popen('python dlv diff -c -d \"' + root_dir + '\" -f \"' + file_name + '\"', shell=True, stdout=foutput)
    ret_code = getOutput.wait()
    foutput.flush()
    foutput.close()
    
    Output =  subprocess.Popen('python diff2html.py -x -i \"' + tmp_file + '\"', shell=True, stdout=subprocess.PIPE).stdout

    result = Output.read()
    
    return result.decode()

@app.route("/historyfilediff", methods=['POST', 'GET'])
def vcsHistoryDiff():
    file_name = request.args['filename']
    username = request.args['username']
    repository = request.args['repository']
    versions = request.args['versions']

    root_dir = os.path.join(project_path, username, repository)

    tmp_file = os.path.join(root_dir, '.dlv', 'tmp.diff')
    foutput = open(tmp_file, 'w')
    command = 'python dlv diff -c -d \"' + root_dir + '\" -f \"' + file_name + '\" -v ' + versions
    print(command)
    getOutput =  subprocess.Popen('python dlv diff -c -d \"' + root_dir + '\" -f \"' + file_name + '\" -v ' + versions, shell=True, stdout=foutput)
    ret_code = getOutput.wait()
    foutput.flush()
    foutput.close()
    
    Output =  subprocess.Popen('python diff2html.py -x -i \"' + tmp_file + '\"', shell=True, stdout=subprocess.PIPE).stdout

    result = Output.read()
    
    return result.decode()

@app.route("/commit", methods=['POST', 'GET'])
def vcsCommit():
    username = request.args['username']
    repository = request.args['repository']
    message = request.args['message']
        
    dest_path = os.path.join(project_path, username, repository)

    os.system('python dlv commit -d \"' + dest_path + '\" -m \"' + message + '\" -a \"' + username + '\"')
    return "success"


@app.route("/history", methods=['POST', 'GET'])
def vcsHistory():
    username = request.args['username']
    repository = request.args['repository']
        
    dest_path = os.path.join(project_path, username, repository)

    Output =  subprocess.Popen('python dlv history -d \"' + dest_path + '\"', shell=True, stdout=subprocess.PIPE).stdout
    result = Output.read()
    commits = json.loads(result.decode())

    for version in commits.keys():
        modified_files = commits[version]['changed_files']
        final_data = []
        temp_dict = {}
        paths = {}
    
        for file in modified_files:

            folders = file.split('\\')
            key = 'root'
            index = 0
            while index < len(folders):
                if key not in temp_dict:
                    temp_dict[key] = []

                if not folders[index] in temp_dict[key]:
                    temp_dict[key].append(folders[index])

                key = folders[index]
                index += 1

            paths[folders[len(folders) - 1]] = file

        if len(modified_files) != 0:
            final_data = getTree(temp_dict, "root", paths)

        commits[version]['changed_files'] = final_data
    
    return json.dumps(commits)

if __name__ == "__main__":
    app.run(debug=True)
