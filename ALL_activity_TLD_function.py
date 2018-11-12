# -*- coding: utf-8 -*-
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

Effi_dose_microSv_s = pd.read_excel(file_name, sheetname="Effi_dose_microSv_s", header=None)
Effi_dose_microSv_s_mat = Effi_dose_microSv_s.values

Eimission_probability = pd.read_excel(file_name, sheetname="Eimission_probability")
Total_probalility = Eimission_probability["Total"].values
Conversion_factor = Eimission_probability["Conversion_factor"].values

Effi_dose_microSv_s_mat = Effi_dose_microSv_s_mat * Total_probalility
Measured_dose = Measured_data["Dose_microSv_sec"].values * Conversion_factor


Dose_activity_optimized = np.linalg.lstsq(Effi_dose_microSv_s_mat, Measured_dose)[0]


Activity_all = {}
Activity_all["Depth"] = Measured_data["Depth"].values
Activity_all["Dose_activity_Bq_kg"] = Dose_activity_optimized


Activity_all_data= pd.DataFrame.from_dict(Activity_all)
writer = pd.ExcelWriter(working_directory+"/Activity_all_data_optimized.xlsx")
Activity_all_data.to_excel(writer,'Activity_all_data')
writer.save()

plt.plot(Dose_activity_optimized, label="Dose")
plt.legend()
plt.show()

print ("Dose:", Dose_activity_optimized)
