# Version Control System for Deep Learning

**Professor: Yug Yung Lee**

## Project Increment 2:

## Team Details:

**Team ID:** 6

**Name:** Dinesh Kumar, Kusam   
**Class ID:** 14

**Name:** Pradeepika, Kolluru   
**Class ID:** 12

**Name:** Sindhusha, Tiyyagura   
**Class ID:** 24

**Name:** Sravan Kumar, Pagadala   
**Class ID:** 21

## Project Goal and Objectives:
The main aim of the project is to develop a version control system for deep learning models( source code, input and output data files, metrics about the experiment)similar to GIT.

## Project Increment -1
1) Getting familiar with GIT open source code.
2) Understanding the requirements and coming up with the design for the functionality of dlv commands. 
3) Implementing dlv init, add and commit commands.

## Project Increment - 2:
1) Creating Basic User Interface for version control system similar to GIT desktop.
2) Modifying Increment 1 commands to clear all the bugs.
3) Implemented commands {status, history, push, diff of files}
4) Implementing commands {list, desc, diff between models}

### Technologies used:
1) Angular, MongoDB 
2) Python 

### Task -1: Modifying Increment 1 commands to be more interactive and make it more bug free.
Steps for making dlv command line python executable binary from anywhere.
1) Created bin and lib directories in the home directory.
2) Implemented all the required dlv_commands in the lib directory.
3) created dlv file( without any '.' extension ) in the bin directory and included the following contents.    
#!/usr/bin/env python2    

import sys    
sys.path.append("/home/user/VCS-Git-for-deep-learning/dlv_commands/lib/")    

import lib_dlv    
lib_dlv.main()    

Implemented lib_dlv command - which parses the command line arguments and calls the appropriate dlv command.    
1) This file specifies the usage of each command and its description.     
Code for the  following file:
![](https://github.com/sindhusha-t/VCS-Git-for-deep-learning/raw/sindhusha/Screenshots/lib_dlv%20code.PNG)
Sample execution of the command:
![](https://github.com/sindhusha-t/VCS-Git-for-deep-learning/raw/sindhusha/Screenshots/lib_dlv%20exec.PNG)

Implemented dlv init command
1) Initiates the repository and creates .dlv directory under the repository for storing the meta data and different versions of the files.
Any command other than init runs only if the following directory is present in the repository.
This command runs locally and nothing is done with the server.    
Code for the following command:
![](https://github.com/sindhusha-t/VCS-Git-for-deep-learning/raw/sindhusha/Screenshots/init%20code.PNG)
Execution and output of the command:
![](https://github.com/sindhusha-t/VCS-Git-for-deep-learning/raw/sindhusha/Screenshots/init%20exec.PNG)

Implemented dlv add command:
1) Adds the following files to the staging area ( step done before the commit command )     
Code for the following command:
![](https://github.com/sindhusha-t/VCS-Git-for-deep-learning/raw/sindhusha/Screenshots/add%20code.PNG)
Execution of the command:
![](https://github.com/sindhusha-t/VCS-Git-for-deep-learning/raw/sindhusha/Screenshots/add%20exec%20-1.PNG)
![](https://github.com/sindhusha-t/VCS-Git-for-deep-learning/raw/sindhusha/Screenshots/add%20exec%20-2.PNG)

Implemented dlv commit command:
1) Creates a snapshot of the files and new version of the file.
2) Takes the list of all files and its versions and saves as one commit command.
3) Command requires commit message and author as arguments    
Code for the following command:
![](https://github.com/sindhusha-t/VCS-Git-for-deep-learning/raw/sindhusha/Screenshots/commit%20code%201.PNG)
![](https://github.com/sindhusha-t/VCS-Git-for-deep-learning/raw/sindhusha/Screenshots/commit%20code%202.PNG)
Execution of the following command:
![](https://github.com/sindhusha-t/VCS-Git-for-deep-learning/raw/sindhusha/Screenshots/commit%20exec.PNG)

Implemented dlv status command:
1) Compares the files in the local repository with the staging area and the remote repository. 
2) Gives the status of the files like staged files, new files, modified files, deleted files.    
Code for the command:
![](https://github.com/sindhusha-t/VCS-Git-for-deep-learning/raw/sindhusha/Screenshots/status%20code.PNG)
Execution of the command:
![](https://github.com/sindhusha-t/VCS-Git-for-deep-learning/raw/sindhusha/Screenshots/status%20exec.PNG)

Implemented dlv history command:
1) Displays all the commits done in the repository.
2) for each commit it shows the commit message, author , time of commit and the files that are changed.   
Code for the command:
![](https://github.com/sindhusha-t/VCS-Git-for-deep-learning/raw/sindhusha/Screenshots/history%20code.PNG)
Execution of the command:
![](https://github.com/sindhusha-t/VCS-Git-for-deep-learning/raw/sindhusha/Screenshots/history%20exec.PNG)

Implemented dlv diff command:
1) Displays the diff between two models if user specifies two models.
2) Displays the diff between the current model and its previous version if only one model is specified by the user.
3) Displays the diff between a file ( for current version and the previous version ) if only one file is specified by the user.
4) Displays the diff between a file ( for local repository and the last snapshot version of the file )     
Code for the command:
![](https://github.com/sindhusha-t/VCS-Git-for-deep-learning/raw/sindhusha/Screenshots/diff%20code.PNG)
Execution of the command:
![](https://github.com/sindhusha-t/VCS-Git-for-deep-learning/raw/sindhusha/Screenshots/diff%20exec.PNG)

Implemented dlv list command:
1) This command interacts with the server to get the list of repositories present in the author account.    

## Task-2: Created Basic User Interface just like GIT desktop.
1) Home page with the guide tour of the project 
![](https://github.com/sindhusha-t/VCS-Git-for-deep-learning/raw/sindhusha/Screenshots/Home%20UI.jpeg)
2) Current repository tab shows the list of repositories uploaded by the user. ( executes dlv list command)
![](https://github.com/sindhusha-t/VCS-Git-for-deep-learning/raw/sindhusha/Screenshots/repositories%20UI.jpeg)
3) Current branch tab shows the list of all branches present in the selected repository ( executed dlv branch command)
![](https://github.com/sindhusha-t/VCS-Git-for-deep-learning/raw/sindhusha/Screenshots/tour%20guide%20%20UI.jpeg)
![](https://github.com/sindhusha-t/VCS-Git-for-deep-learning/raw/sindhusha/Screenshots/tour%20guide%20UI%202.jpeg)
4) On selection of the branch , shows the status and history of previous commits.
![](https://github.com/sindhusha-t/VCS-Git-for-deep-learning/raw/sindhusha/Screenshots/status%20UI.jpeg)
5) Status displays the modified, tracked, untracked, staged files and the diff of the files with the last commit.
6) History shows all the previous commits along with the author, time and commit message.
![](https://github.com/sindhusha-t/VCS-Git-for-deep-learning/raw/sindhusha/Screenshots/history%20UI.jpeg)
7) Based on the selection of the commit version - it shows the list of changed files in that commit version and also the diff of those modified files with the previous commit version.

## Task Responsibilities:   
**1) Dinesh Kumar Reddy Kusam:** Worked on the User Interface part.    
Created components for  home page, repository and branch tabs, status pages.   
**2) Sravan Kumar Pagadala:** Worked on the User Interface part.   
Created components for history and the html diff view of the files on selection of the commit version and the modified file.   
**3) Sindhusha Tiyyagura:** Worked on the backend part ( Command execution )    
Modified the commands ( init, add, commit ) to handle all the cases and to make it bug free    
Implemented the commands diff, list commands.   
**4) Pradeepika Kolluru**: Worked on the backend part ( Command execution )    
Implemented commands like dlv status and dlv history commands.   
Implemented push and desc commands along with the connection to MongoDB.    
