# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 16:37:49 2018

@author: mhasan
"""

import os 
from tkinter import Tk
from tkinter import filedialog
import fileinput
import sys
import subprocess
import shutil

working_directory = filedialog.askdirectory(title='Please select working directory')
os.chdir(working_directory)

def replaceAll(file,searchExp,replaceExp):
    for line in fileinput.input(file, inplace=1):
        if line.strip().startswith(searchExp):
            line = str(replaceExp + "\n")
        sys.stdout.write(line)

position = {5.9550:7.5000, 14.705:10.0000, 24.705:10.0000, 34.705:10.0000,
            44.705:10.0000, 54.705:10.0000,
            64.705:10.0000, 74.705:10.0000, 84.705:10.0000,  94.705:10.0000} 
    
for pos in position:
    sthick1 = "STHICK   %4.4f" %position[pos]
    spost1 = "SPOSIT   0    0    %4.4f" %pos
    replaceAll("k.inp",
               "STHICK",
               sthick1)
    replaceAll("k.inp",
               "SPOSIT",
               spost1)
    
    p = subprocess.Popen(str(working_directory+'/k.bat'), 
                         cwd=str(working_directory), 
                         shell=True, 
                         stdout = subprocess.PIPE)
    stdout, stderr = p.communicate()
    print (p.returncode) # is 0 if success
    dir_name = str(working_directory+"/Simulation/layer_%s" %str(int(pos)))
    if not os.path.exists(dir_name):
            os.makedirs(dir_name)
    shutil.copy(str(working_directory+'/k.inp'),str(dir_name+'/k.inp'))
    shutil.copy(str(working_directory+'/KP_Ra_3_3.txt'),str(dir_name+'/KP_Ra_3_3.txt'))
    shutil.copy(str(working_directory+'/KP_Ra_4_3.txt'),str(dir_name+'/KP_Ra_4_3.txt'))
