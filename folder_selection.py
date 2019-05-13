import tkinter as tk
from tkinter import filedialog

import shutil
import os
 
def copyDirectory(src, dest):
    try:
        shutil.copytree(src, dest)
    # Directories are the same
    except shutil.Error as e:
        print('Directory not copied. Error: %s' % e)
    # Any error saying that the directory doesn't exist
    except OSError as e:
        print('Directory not copied. Error: %s' % e)

root = tk.Tk()
root.withdraw()

#file_path = filedialog.askopenfilename()
#print(file_path)


dirname = filedialog.askdirectory(parent=root,initialdir="/",title='Please select a directory')

project_path = "E:\ASE_database"
dest_path = os.path.join(project_path, os.path.basename(dirname))
print(dest_path)
copyDirectory(dirname, dest_path)
