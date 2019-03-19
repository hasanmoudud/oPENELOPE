# -*- coding: utf-8 -*-
"""
Created on Fri Jan 25 13:35:37 2019

@author: mhasan
"""
import pandas as pd
import os
from tkinter import filedialog
import numpy as np

source_thickness = 5.0 # cm 
Srad_inner = 2.5 #cm
Srad_outter = 102.5 #cm 
soil_density = 1.4 #g/cm3 
mev_to_SV = 1.602E-10
SV_to_micro = 1000000

# Change to working directory to current file location 
working_directory = filedialog.askdirectory(title='Please select working directory')
os.chdir(working_directory)

file_name = filedialog.askopenfilename(title='Please select outp file')

volume_in = 3.1416*source_thickness* Srad_inner**2
volume_out = 3.1416*source_thickness* Srad_outter**2
volume = volume_out - volume_in
mass= (volume*soil_density)/1000.0
print(mass)

data_line = []
with open(file_name) as input_data:
    # Skips text before the beginning of the interesting block:
    for line in input_data:
        if line.strip() == 'masses':  # Or whatever test is needed
            break
    # Reads text until the end of the block:
    for line in input_data:  # This keeps reading the file
        if line.strip() == '===================================================================================================================================':
            break
        if line.strip() == "there are no nonzero tallies in the tally fluctuation chart bin for tally        6":
            break 
        if line.strip() != '' and len(line.strip().split()) <=2 and line.strip().split()[0] != "cell":
            data_line.append(line.strip().split())  # Line is extracted (or block_of_lines.append(line), etc.)
            print (line.strip().split()[0])

labels =["Dose", "Uncertainty"]
dff = pd.DataFrame.from_records(data_line, columns=labels)
df = dff.astype(float)
df["Dose_microSV_mass"] = df.Dose * mass * mev_to_SV * SV_to_micro
df["Uncertainty_%"] = df["Uncertainty"]*100


writer = pd.ExcelWriter(working_directory+"/Dose_MCNP_Simulation.xlsx")
df.to_excel(writer,'Dose_all_data')
writer.save()

Matsize = 20
effi_mat = np.zeros((Matsize,Matsize))
for i in range (0,20):
    d= [df["Dose_microSV_mass"].values[i]]
    dd = d*(Matsize -i) 
    if i == 0:
        wwm= np.diag(dd, i)
        effi_mat = effi_mat + wwm
    else:
        wwu= np.diag(dd, i)
        wwd= np.diag(dd, -i)
        effi_mat = effi_mat + wwu + wwd
    Cdn = np.linalg.cond(effi_mat)
    print(i , Cdn)
    np.savetxt("Mat_%i_CN%i.csv" %(i, Cdn), effi_mat, delimiter=",")
    #np.savetxt("Mat_%i.csv" %(i), effi_mat, delimiter=",")


#import itertools
#a = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]
#xcv = [[1]]
#xcvb = xcv * 16
#bbj = a + xcvb
#len(list(itertools.product(*bbj)))