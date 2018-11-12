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

Effi_total_counts = pd.read_excel(file_name, sheetname="Effi_total_counts", header=None)
Effi_total_counts_mat = Effi_total_counts.values

Effi_dose_microSv_s = pd.read_excel(file_name, sheetname="Effi_dose_microSv_s", header=None)
Effi_dose_microSv_s_mat = Effi_dose_microSv_s.values

Effi_E356 = pd.read_excel(file_name, sheetname="Effi_E356", header=None)
Effi_E356_mat = Effi_E356.values

Eimission_probability = pd.read_excel(file_name, sheetname="Eimission_probability")
Total_probalility = Eimission_probability["Total"].values
E356_probalility = Eimission_probability["E_356"].values

Effi_total_counts_mat = Effi_total_counts_mat * Total_probalility
Effi_dose_microSv_s_mat = Effi_dose_microSv_s_mat * Total_probalility
Effi_E356_mat = Effi_E356_mat * E356_probalility

Total_activity_optimized = np.linalg.lstsq(Effi_total_counts_mat, Measured_data.Total_counts_cps.values)[0] 

Dose_activity_optimized = np.linalg.lstsq(Effi_dose_microSv_s_mat, Measured_data.Dose_microSv_sec.values)[0]

E356_activity_optimized = np.linalg.lstsq(Effi_E356_mat, Measured_data.Net_Peak_counts_E356.values)[0]

count_un_s = Measured_data.Uncertainty_356.values
count_un_s_sq = count_un_s**2
count_un_s_sq_ivrs = count_un_s_sq**-1
count_un_s_mat = np.diag(count_un_s_sq_ivrs)
uncertainty_m = np.matmul(Effi_E356_mat, count_un_s_mat)
uncertainty1_m = np.matmul(uncertainty_m, Effi_E356_mat)
uncertainty1_dia = uncertainty1_m.diagonal()
uncertainty1_dia_r = np.sqrt((uncertainty1_dia)**-1)


Activity_all = {}
Activity_all["Total_activity_Bqg"] = Total_activity_optimized/1000
Activity_all["Dose_activity_Bqg"] = Dose_activity_optimized/1000
Activity_all["E356_activity_Bqg"] = E356_activity_optimized/1000
Activity_all["E356_Uncertain_Bqg"] = uncertainty1_dia_r/1000

Activity_all_data= pd.DataFrame.from_dict(Activity_all)
writer = pd.ExcelWriter(working_directory+"/Activity_all_data_optimized.xlsx")
Activity_all_data.to_excel(writer,'Activity_all_data')
writer.save()

plt.plot(Total_activity_optimized, label="Total")
plt.plot(Dose_activity_optimized, label="Dose")
plt.plot(E356_activity_optimized, label="Peak")
plt.legend()
plt.show()

print ("Total:", Total_activity_optimized/1000)
print ("Dose:", Dose_activity_optimized/1000)
print ("Peak", E356_activity_optimized/1000)