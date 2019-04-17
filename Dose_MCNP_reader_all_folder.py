# -*- coding: utf-8 -*-
"""
Created on Fri Jan 25 13:35:37 2019

@author: mhasan
"""
import pandas as pd
import os
from tkinter import filedialog
import numpy as np



# Change to working directory to current file location 
working_directory = filedialog.askdirectory(title='Please select working directory')
os.chdir(working_directory)

directory_list = list()
for root, dirs, files in os.walk(working_directory, topdown=False):
    for name in dirs:
        directory_list.append(os.path.join(root, name))

source_thickness = 5.0 # cm 
Srad_inner = 2.5 #cm
Srad_outter = 102.5 #cm 
soil_density = 1.8 #g/cm3 
mev_to_SV = 1.602E-10
SV_to_micro = 1000000
volume_in = 3.1416*source_thickness* Srad_inner**2
volume_out = 3.1416*source_thickness* Srad_outter**2
volume = volume_out - volume_in
mass= (volume*soil_density)/1000.0


df_dose = pd.DataFrame()
df_uncrt = pd.DataFrame()
df_dose_ms = pd.DataFrame()
df_uncrp = pd.DataFrame()
for folder in directory_list:
    file_name = str(folder+'/outp')
    data_line = []
    with open(file_name) as input_data:
        # Skips text before the beginning of the interesting block:
        for line in input_data:
            if len(line.strip().split()) >= 2:
                if line.strip().split()[1] == 'SI1': 
                    energy = float(line.strip().split()[3])*1000
            if line.strip() == 'masses':  # Or whatever test is needed
                break
        # Reads text until the end of the block:
        for line in input_data:  # This keeps reading the file
            if line.strip() == '===================================================================================================================================':
                break
            if line.strip() == "there are no nonzero tallies in the tally fluctuation chart bin for tally        6":
                break 
            if line.strip() != '' and len(line.strip().split())==2 and line.strip().split()[0] != "cell" and line.strip().split()[0] != "cell:":
                data_line.append(line.strip().split())  # Line is extracted (or block_of_lines.append(line), etc.)
                print (line.strip().split()[0])
    
    labels =["Dose", "Uncertainty"]
    dff = pd.DataFrame.from_records(data_line, columns=labels)
    df = dff.astype(float)
    df_dose["Energy_%i_KeV" %energy] = df.Dose
    df_uncrt["Energy_%i_KeV" %energy] = df["Uncertainty"]
    df_dose_ms["Energy_%i_KeV" %energy] = df.Dose * mass * mev_to_SV * SV_to_micro
    df_uncrp["Energy_%i_KeV" %energy] = df["Uncertainty"]*100
    
    
    Matsize = 20
    effi_mat = np.zeros((Matsize,Matsize))
    for i in range (0,20):
        d= [df_dose_ms["Energy_%i_KeV" %energy].values[i]]
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
        np.savetxt(str(folder +"/Mat_%i_CN%i.csv" %(i, Cdn)), effi_mat, delimiter=",")
        #np.savetxt("Mat_%i.csv" %(i), effi_mat, delimiter=",")

writer = pd.ExcelWriter(working_directory +"/Dose_MCNP_Simulation.xlsx")
df_dose.to_excel(writer,'Dose_eVg')
df_uncrt.to_excel(writer,"Uncertainty")
df_dose_ms.to_excel(writer,"Dose_mSvBqKg")
df_uncrp.to_excel(writer,"Uncertainty_P")
writer.save()
