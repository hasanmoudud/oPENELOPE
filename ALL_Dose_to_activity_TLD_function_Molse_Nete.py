# 0     -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 16:05:22 2018

@author: mhasan
"""
import os 
import matplotlib.pyplot as plt
from numpy import genfromtxt
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
from tkinter import Tk
from tkinter import filedialog
import scipy.linalg as sp
from scipy.optimize import lsq_linear

# Change to working directory to current file location 
working_directory = filedialog.askdirectory(title='Please select working directory')
os.chdir(working_directory)

file_name = filedialog.askopenfilename(title='Please select excel file with all data')
Measured_data = pd.read_excel(file_name, sheetname="Measured")

Activity_all1 = {}
Activity_all1["Depth"] = Measured_data["Depth"].values
nuclides = ["Cs", "Am", "K"]

for nuclide in nuclides:
    Effi_dose_microSv_s = pd.read_excel(file_name, sheetname="Effi_dose_microSv_s_%s" %nuclide, header=None)
    Effi_dose_microSv_s_mat = Effi_dose_microSv_s.values
    
    Eimission_probability = pd.read_excel(file_name, sheetname="Eimission_probability")
    Total_probalility = Eimission_probability["Total"][nuclide]
    #Conversion_factor = Eimission_probability["Conversion_factor"][nuclide]
    
    Effi_dose_microSv_s_mat = Effi_dose_microSv_s_mat * Total_probalility
    print(nuclide, np.linalg.cond(Effi_dose_microSv_s_mat))
    
    Measured_dose = Measured_data["Dose_%s" %nuclide].values 
       
    Dose_activity_optimized1 = lsq_linear(Effi_dose_microSv_s_mat, Measured_dose, method='trf', bounds=(0, 5000), lsq_solver='lsmr', lsmr_tol = 'auto', verbose=0)
    Activity_all1[str("Activity_BqpKg"+ nuclide)] = Dose_activity_optimized1["x"]
    
    Measured_activity = Measured_data["Activity_%s" %nuclide].values 
    
    Dose_activity_optimized = np.matmul(Effi_dose_microSv_s_mat, Measured_activity)
    Activity_all1[str("Dose_MicropDay"+ nuclide)] = Dose_activity_optimized * 24*60*60
    
    if nuclide =="Cs":
        Measured_activity = Measured_data["Activity_insitu_%s" %nuclide].values 
        Dose_activity_optimized = np.matmul(Effi_dose_microSv_s_mat, Measured_activity)
        Activity_all1[str("Dose_MicropDay_insitu_"+ nuclide)] = Dose_activity_optimized * 24*60*60
    

Activity_all_data1= pd.DataFrame.from_dict(Activity_all1)
writer = pd.ExcelWriter(working_directory+"/Dose_all_data_optimized_Mol_activity_all.xlsx")
Activity_all_data1.to_excel(writer,'Dose_all_data')
writer.save()

# =============================================================================
# plt.plot(Dose_activity_optimized, label="Dose")
# plt.legend()
# plt.show()
# 
# print ("Dose:", Dose_activity_optimized)
# =============================================================================

