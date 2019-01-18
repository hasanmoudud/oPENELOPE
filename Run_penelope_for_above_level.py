# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 17:45:07 2018

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
        if searchExp in line:
            line = line.replace(searchExp,replaceExp)
        sys.stdout.write(line)

position = {8.7600:7.5000, 17.5100:10.0000, 27.5100:10.0000, 37.5100:10.0000,
            47.5100:10.0000, 57.5100:10.0000,
            67.5100:10.0000, 77.5100:10.0000, 87.5100:10.0000,  97.5100:10.0000} 
sthick = "STHICK   7.5000" 
spost = "SPOSIT   0    0    8.7600"
    
for pos in position:
    sthick1 = "STHICK   %4.4f" %position[pos]
    spost1 = "SPOSIT   0    0    %4.4f" %pos
    replaceAll("k.inp",
               sthick,
               sthick1)
    replaceAll("k.inp",
               spost,
               spost1)
    sthick = sthick1
    spost = spost1
    
    p = subprocess.Popen(str(working_directory+'/k.bat'), 
                         cwd=str(working_directory), 
                         hell=True, 
                         stdout = subprocess.PIPE)
    stdout, stderr = p.communicate()
    print (p.returncode) # is 0 if success
    dir_name = os.path.dirname(str(working_directory+"/Simulation_data/layer_%i" %pos))
    if not os.path.exists(dir_name):
            os.makedirs(dir_name)
    shutil.copy(str(working_directory+'/k.inp'),str(dir_name+'/k.inp'))
    shutil.copy(str(working_directory+'/KP_Ra_3_3.txt'),str(dir_name+'/KP_Ra_3_3.txt'))