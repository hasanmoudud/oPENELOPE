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

# Change to working directory to current file location 
working_directory = filedialog.askdirectory(title='Please select working directory')
os.chdir(working_directory)

file_name = filedialog.askopenfilename(title='Please select excel file with all data')
Measured_data = pd.read_excel(file_name, sheetname="Measured")
Activity_all = {}
Activity_all["Depth"] = Measured_data["Depth"].values
nuclides = ["Co","Ba", "Eu152", "Eu155"]

for nuclide in nuclides:
    Effi_dose_microSv_s = pd.read_excel(file_name, sheetname="Effi_dose_microSv_s_%s" %nuclide, header=None)
    Effi_dose_microSv_s_mat = Effi_dose_microSv_s.values
    
    Eimission_probability = pd.read_excel(file_name, sheetname="Eimission_probability")
    Total_probalility = Eimission_probability["Total"][nuclide]
    Conversion_factor = Eimission_probability["Conversion_factor"][nuclide]
    time_total = Eimission_probability["Time"][nuclide]
    
    Effi_dose_microSv_s_mat = Effi_dose_microSv_s_mat * Total_probalility
    #Effi_dose_microSv_s_mat = Effi_dose_microSv_s_mat / Conversion_factor
    Effi_dose_microSv_s_mat = Effi_dose_microSv_s_mat * time_total
    
    Measured_activity = Measured_data["Activity_%s" %nuclide].values 
    
    Dose_activity_optimized = np.matmul(Effi_dose_microSv_s_mat, Measured_activity)
    Activity_all[nuclide] = Dose_activity_optimized


Activity_all_data= pd.DataFrame.from_dict(Activity_all)
writer = pd.ExcelWriter(working_directory+"/Dose_From_activity_all_data_ratio_activity.xlsx")
Activity_all_data.to_excel(writer,'Dose_all_data')
writer.save()


plt.plot(Dose_activity_optimized, label="Dose")
plt.legend()
plt.show()

print ("Dose:", Dose_activity_optimized)
