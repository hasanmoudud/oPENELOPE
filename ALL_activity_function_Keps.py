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
from tkinter import filedialog

# Change to working directory to current file location 
working_directory = filedialog.askdirectory(title='Please select working directory')
os.chdir(working_directory)



parameter = { "Effi_total_counts_Ra":["Total_Ra", "Total_counts_cps"],
              "Effi_dose_microSv_s_Ra":["Total_Ra", "Dose_microSv_sec"],
              "Effi_E352":["E_352", "Net_Peak_counts_E352"],
              "Effi_E352s":["E_352", "Net_Peak_counts_E352"],
              "Effi_E352s1m":["E_352", "Net_Peak_counts_E352"],
              "Effi_E609":["E_609", "Net_Peak_counts_E609"],
              "Effi_E609s1m":["E_609", "Net_Peak_counts_E609"]
            }

Uncertainty_parameter = { "Uncertainty_E352":["E_352", "Effi_E352s1m"],
              "Uncertainty_E609":["E_609", "Effi_E609s1m"]
            }

file_name = filedialog.askopenfilename(title='Please select excel file with all data')
Measured_data = pd.read_excel(file_name, sheet_name="Measured")
Eimission_probability = pd.read_excel(file_name, sheet_name="Eimission_probability")


def activity_calculation(file_name_s, sheetname_s, Em_probalility, cps):
    efficency_mass = pd.read_excel(file_name, sheet_name= sheetname_s, header=None)
    efficency_mass_mat = efficency_mass.values
    efficency_mass_mat_em = efficency_mass_mat * Em_probalility
    init_len = len(cps)
    cps = cps[np.nonzero(cps)]
    mat_len = len(cps)
    zero_values = np.zeros(init_len - mat_len)
    Activity_optimized = np.linalg.lstsq(efficency_mass_mat_em [0:mat_len, 0:mat_len], cps)[0] 
    Activity_optimized = np.append(Activity_optimized, zero_values)
    return Activity_optimized

def Uncertainty_calculation(file_name_s, sheetname_s, Em_probalility, count_un_s):
    efficency_mass = pd.read_excel(file_name, sheet_name= sheetname_s, header=None)
    efficency_mass_mat = efficency_mass.values
    efficency_mass_mat_em = efficency_mass_mat * Em_probalility
    init_len = len(count_un_s)
    count_un_s = count_un_s[np.nonzero(count_un_s)]
    mat_len = len(count_un_s)
    zero_values = np.zeros(init_len - mat_len)
    count_un_s_sq = count_un_s**2
    count_un_s_sq_ivrs = count_un_s_sq**-1
    count_un_s_mat = np.diag(count_un_s_sq_ivrs)
    uncertainty_m = np.matmul(efficency_mass_mat_em [0:mat_len, 0:mat_len], count_un_s_mat)
    uncertainty1_m = np.matmul(uncertainty_m, efficency_mass_mat_em[0:mat_len, 0:mat_len])
    uncertainty1_dia = uncertainty1_m.diagonal()
    uncertainty1_dia_r = np.sqrt((uncertainty1_dia)**-1)
    uncertainty1_dia_r = np.append(uncertainty1_dia_r, zero_values)
    return uncertainty1_dia_r



Activity_all = {}
Activity_all["Depth"] = Measured_data["Depth"].values

for key in parameter:
    Activity_all[key] = activity_calculation(file_name_s = file_name, 
                                            sheetname_s = key, 
                                            Em_probalility = Eimission_probability[parameter[key][0]].values, 
                                            cps = Measured_data[parameter[key][1]].values)


### Peak counts uncertainty matrix making 
for key in Uncertainty_parameter:
    Activity_all[key] = Uncertainty_calculation(file_name_s = file_name, sheetname_s = Uncertainty_parameter[key][1] , Em_probalility = Eimission_probability[Uncertainty_parameter[key][0]].values, 
    count_un_s = Measured_data[key].values)

Activity_all_data= pd.DataFrame.from_dict(Activity_all)
writer = pd.ExcelWriter(working_directory+"/Activity_all_data_optimized_extra.xlsx")
Activity_all_data.to_excel(writer,'Activity_all_data')
writer.save()

#Activity_all_data.plot(x= Measured_data["Depth"],figsize=(8,6))
    
    
    
