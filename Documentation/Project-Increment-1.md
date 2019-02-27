# Version Control System for Deep Learning

**Professor: Yug Yung Lee**

## Project Pre-proposal:

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
The main aim of the project is to develop a version control system for deep learning models( source code, input and output data files, metrics about the experiment).

## Project Increment -1
1) Getting familiar with GIT open source code.
2) Understanding the requirements and coming up with the design for the functionality of dlv commands. 
3) Implementing dlv init, add and commit commands.

### Technologies used:
1) Downloaded git, python.
2) Used gdb command

### Task -1: Getting familiar with GIT source code.
1) We have downloaded the git source code from the github repository.
2) We have modified few files to understand git init, add and commit functions internal working.
3) We compiled and installed source code files and generated git binary file.
4) We have used gdb command to debug few variables in the C code.


### Reasons why GIT is not best for deep learning experiments.
1) There is no functionality in GIT to track group of files as a version ( Deep learning is more dependent on the tracking of each experiment as a version )
2) Git is not flexible is handling huge data files more than a GB.
3) There is no tool to track or compare different experiments of the deep learning project.

### Existing GIT functionality
1) Git tracks each file history independently.      
Most of the git commands are used to change the git meta data files on the local machine.       
Only 2 commands( git pull and push commands) are connected to the GIT server for downloading and uploading files respectively using File transfer protocol.             
2) GIT init command: Creates .git directory( contains meta data about the files to be tracked) on the project directory.          
Example:
        .git/      
           ----HEAD        
           ----objects/    
           ----refs/     
               ----====heads/     
               ----====tags/     
           ----config     
       .gitignore     

HEAD specifies to which branch GIT to commit         
config contains the settings like repository name, user profiles.          
objects directory contains 3 different objects like commit, tree and blob objects. All these files will be stores in the form of hash file_name       

3) GIT add command: It creates cache of all the files specified and creates BLOB objects for all the files.        
BLOB objects are nothing but the physical files which contains the file content.            
The BLOB object is not stored with the file name. It will be stored with the md5_hash value as the file name and with the first two chars as the directory name.             
MD5 hash value will be same for same file content files. ( different if there is any change in the file contents )     
The functionality of MD5 checksum filename is to track different versions of the same file. ( in which same file_name cannot be used for tracking different versions ).           
Example:            
git add file1.py             
.git/                    
-------objects/              
--------------info/         
-------------------92/              
----------------------f65tbjh784hj345j34hmw4    --> BLOB object contains file1.py contents        

It also adds the files to the staging directory which will be later used by commit to commit the files          
4) GIT commit command: It creates DAG ( Directed acyclic graph ) for the list of files commited in the project repository.
In commit command, it starts tracking the files(BLOB objects) stored in the cache.        
It creates commit and tree objects.              
TREE object basically represents a directory. It references to TREE and BLOB objects.( basically sub directories and files inside the directory )            
COMMIT object points out to the TREE object(latest commited version) and the parent COMMIT object( previous COMMIT object).               

-----> TREE object <-------                
Author: Name            
commit time: time                    
              
TREE 5437hg4t7854th45y45y9y568                     
BLOB dg67w45g4ry754hg587th458t               
BLOB fg478yt57th58th58t5t8945fb                 

-----> COMMIT Object <--------                
Author: Name                                  
commit Time: time                          

TREE fgdsyu74htfw38eduhw8e3wd8                       
PARENT g47uygr4ewiuh4yturhutre74e                           

### Proposed functionality for Deep learning experiments                            
In GIT it is hard to maintain huge amount of data files. So Database like S3, Azure or GS are used for storing the huge data sets like ( source code, input and output files, metrics of the experiment).                      
In Increment 1 will go over the internal working of the 3 commands ( dlv init, add and commit ).                 

1) DLV init command:                 
This command is similar to the git init command.                       
It creates .dlv directory which specifies the metadata for the project repository.                     
.dlv/                  
--------config                
--------cache/              
--------HEAD                  
---------stage                  

2) DLV add command:                     
This command is also similar to the git add command which creates BLOB objects for the files to be tracked using DLV.           
Example:            
dlv add file1.py               
.git/                   
-------cache/                
-------------------92/                    
----------------------f65tbjh784hj345j34hmw4    --> BLOB object contains file1.py contents               

3) DLV commit command:               
This command is little different compared to the git commit command.               
In this it creates TREE and COMMIT objects similar to the git functionality but the structure of the COMMIT object is different compared to the git functionality.                

-----> TREE object <-------                 
Author: Name                    
commit time: time                    

TREE 5437hg4t7854th45y45y9y568        # represents SUB_DIRECTORY                 
BLOB dg67w45g4ry754hg587th458t        # represents a file                  
BLOB fg478yt57th58th58t5t8945fb                     

-----> COMMIT Object <--------                    
Author: Name                    
commit Time: time                           

code: file1.py                 
md5: fgf785tg578hg54t8h43wefre34                         
input: data1.json                           
md5: df46rgf64h4e8ty58t43efedw43t                  
output: output_data.json                      
md5: gf54gt754ht7854h58t54tr5ty5r                  
metrics: metrics.json                        
md5: gf487tg78e5tgf74yty85t5t8y54                       

commit object contains full details of the experiment run and its versions used in it.          

### Basic Implementation of the commands:
1) dlv init command:
![](https://github.com/sindhusha-t/VCS-Git-for-deep-learning/raw/master/Screenshots/Increment-1_files/dlv%20init.png)
2) dlv add command:
![](https://github.com/sindhusha-t/VCS-Git-for-deep-learning/raw/master/Screenshots/Increment-1_files/dlv%20add.png)
3) dlv commit commad:
![](https://github.com/sindhusha-t/VCS-Git-for-deep-learning/raw/master/Screenshots/Increment-1_files/dlv%20commit.png)

### UML Data Flow Diagram:
![](https://github.com/sindhusha-t/VCS-Git-for-deep-learning/raw/pradeepika/VCS%20for%20Deep%20learning.png)
![](https://github.com/sindhusha-t/VCS-Git-for-deep-learning/raw/pradeepika/VCS%20for%20Deep%20learning%20(1).png)

Tasks done by each Team member:
1) Getting familiar with GIT source code and internal functionality 
------ Explored and discussed by all team members
2) Understanding the requirements and faults in the existing project(GIT) and coming up with the design for the proposed project.
------ Sindhusha Tiyyagura and discussed with all team members for the final conclusion.
3) Implementing dlv init command:
------ Sravan Pagadala
4) Implementing dlv add command:
------ Pradeepika kolluru
5) Implementing dlv commit command:
------ Dinesh Kumar Reddy Kusam
6) UML diagrams:
------ Pradeepika kolluru
7) Increment 1 Documentation and video:
------ Sindhusha Tiyyagura