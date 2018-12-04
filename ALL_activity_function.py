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
from tkinter import Tk
from tkinter import filedialog

# Change to working directory to current file location 
working_directory = filedialog.askdirectory(title='Please select working directory')
os.chdir(working_directory)



#parameter = { "Effi_total_counts_AmCs":["Total_AmCS", "Total_counts_cps"],
#              "Effi_dose_microSv_s_AmCs":["Total_AmCS", "Dose_microSv_sec"],
#              "Effi_total_counts_Cs":["Total_CS", "Total_counts_cps"],
#              "Effi_dose_microSv_s_Cs":["Total_CS", "Dose_microSv_sec"],
#              "Effi_E662":["E_662", "Net_Peak_counts_E662"],
#            }
parameter = { "Effi_E662":["E_662", "Net_Peak_counts_E662"],
            }



file_name = filedialog.askopenfilename(title='Please select excel file with all data')
Measured_data = pd.read_excel(file_name, sheetname="Measured")
Eimission_probability = pd.read_excel(file_name, sheetname="Eimission_probability")


def activity_calculation(file_name_s, sheetname_s, Em_probalility, cps):
    efficency_mass = pd.read_excel(file_name, sheetname= sheetname_s, header=None)
    efficency_mass_mat = efficency_mass.values
    efficency_mass_mat_em = efficency_mass_mat * Em_probalility
    Activity_optimized = np.linalg.lstsq(efficency_mass_mat_em, cps)[0] 
    return Activity_optimized

def Uncertainty_calculation(file_name_s, sheetname_s, Em_probalility, count_un_s):
    efficency_mass = pd.read_excel(file_name, sheetname= sheetname_s, header=None)
    efficency_mass_mat = efficency_mass.values
    efficency_mass_mat_em = efficency_mass_mat * Em_probalility
    count_un_s_sq = count_un_s**2
    count_un_s_sq_ivrs = count_un_s_sq**-1
    count_un_s_mat = np.diag(count_un_s_sq_ivrs)
    uncertainty_m = np.matmul(efficency_mass_mat_em, count_un_s_mat)
    uncertainty1_m = np.matmul(uncertainty_m, efficency_mass_mat_em)
    uncertainty1_dia = uncertainty1_m.diagonal()
    uncertainty1_dia_r = np.sqrt((uncertainty1_dia)**-1)
    return uncertainty1_dia_r



Activity_all = {}
for key in parameter:
    Activity_all[key] = activity_calculation(file_name_s = file_name, 
                                            sheetname_s = key, 
                                            Em_probalility = Eimission_probability[parameter[key][0]].values, 
                                            cps = Measured_data[parameter[key][1]].values)


### Peak counts uncertainty matrix making 
Activity_all["Uncertainty_662"] = Uncertainty_calculation(file_name_s = file_name, sheetname_s = "Effi_E662", Em_probalility = Eimission_probability["E_662"].values, 
count_un_s = Measured_data["Uncertainty_662"].values)

Activity_all_data= pd.DataFrame.from_dict(Activity_all)
writer = pd.ExcelWriter(working_directory+"/Activity_all_data_optimized_new_density_field.xlsx")
Activity_all_data.to_excel(writer,'Activity_all_data')
writer.save()

#Activity_all_data.plot(x= Measured_data["Depth"],figsize=(8,6))
#plt.plot(Total_activity_optimized, label="Total")
#plt.plot(Dose_activity_optimized, label="Dose")
#plt.plot(E356_activity_optimized, label="Peak")
#plt.legend()
#plt.show()
#
#print ("Total:", Total_activity_optimized/1000)
#print ("Dose:", Dose_activity_optimized/1000)
#print ("Peak", E356_activity_optimized/1000)