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

#position = {3.7500:7.5000, 12.5000:10.0000, 22.5000:10.0000, 32.5000:10.0000,
#            42.5000:10.0000, 52.5000:10.0000,62.5000:10.0000, 72.5000:10.0000,
#            82.5000:10.0000,  93.7500:12.5000} 

position = {3.7500:7.5000, 12.5000:10.0000, 22.5000:10.0000, 32.5000:10.0000,
            52.5000:10.0000, 93.7500:12.5000} 
    
for pos in position:
    sthick1 = "STHICK   %4.4f" %position[pos]
    spost1 = "SPOSIT   0    0    %4.4f" %pos
    replaceAll("k.inp",
               "STHICK",
               sthick1)
    replaceAll("k.inp",
               "SPOSIT",
               spost1)
    
#    p = subprocess.Popen(str(working_directory+'/k.bat'), 
#                         cwd=str(working_directory), 
#                         shell=True, 
#                         stdout = subprocess.PIPE)
#    stdout, stderr = p.communicate()
#    print (p.returncode) # is 0 if success
    dir_name = str(working_directory+"/Simulation/layer_%s" %str(int(pos)))
    if not os.path.exists(dir_name):
            os.makedirs(dir_name)
    shutil.copy(str(working_directory+'/k.inp'),str(dir_name+'/k.inp'))
    layer=4
    i=1
    while i <= len(position):
        shutil.copy(str(working_directory+'/KP_Ra_%i_3.txt' %layer),str(dir_name+'/KP_Ra_%i_3.txt' %layer))
        shutil.copy(str(working_directory+'/dose-charge-%02d.dat' %i),str(dir_name+'/dose-charge-%02d.dat' %i))
        layer +=7
        i += 1
        
