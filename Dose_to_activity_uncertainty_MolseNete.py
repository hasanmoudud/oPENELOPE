# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 13:26:54 2019
To calculate uncertainty in dose to activity calculation. 
This function will take dose of four different TLDs and their mean 
as input and convert them to activty.
First user have to select a excel file that containts all data (all simulation and measured data).
As a output user will get figure ( excel can be obtained as well).
@author: mhasan
"""
import os 
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 
import random
from tkinter import filedialog
import scipy.linalg as sp
from scipy.linalg import lstsq
from scipy.optimize import lsq_linear
from scipy.sparse.linalg import spsolve
from scipy.sparse import csc_matrix

# Change to working directory to current file location 
working_directory = filedialog.askdirectory(title='Please select working directory')
os.chdir(working_directory)

file_name = filedialog.askopenfilename(title='Please select excel file with all data')
Measured_data = pd.read_excel(file_name, sheetname="Measured")

Msdata = Measured_data[["Right","Up","Left","Down"]].values

nuclides = ["Cs", "Am", "K"]
writer = pd.ExcelWriter(working_directory+"/Dose_all_data_optimized_Molsenete_uncertainty_All_background.xlsx")

for nuclide in nuclides:
    Activity_all1 = {}
    Activity_all1["Depth"] = Measured_data["Depth"].values
    
    Dose_all1 = {}
    Dose_all1["Depth"] = Measured_data["Depth"].values

    Effi_dose_microSv_s = pd.read_excel(file_name, sheetname="Effi_dose_microSv_s_%s" %nuclide, header=None)
    Effi_dose_microSv_s_mat = Effi_dose_microSv_s.values
    
    Eimission_probability = pd.read_excel(file_name, sheetname="Eimission_probability")
    Total_probalility = Eimission_probability["Total"][nuclide]
    
    Effi_dose_microSv_s_mat = Effi_dose_microSv_s_mat * Total_probalility
    print(nuclide, np.linalg.cond(Effi_dose_microSv_s_mat))
    
    Measured_ratio = Measured_data["Ratio_%s" %nuclide].values 
    
    dose_type = ["Dose_total", "Right","Up","Left","Down"]
    for type_D in dose_type:
        Measured_dose = Measured_data[type_D].values * Measured_ratio
        #Dose_activity_optimized2 = sp.cho_solve(sp.cho_factor(Effi_dose_microSv_s_mat), Measured_dose)
        #Activity_all1["%s%s_cho" %(nuclide,type_D)] = Dose_activity_optimized2
        #Dose_activity_optimized0, res, rnk, s = lstsq(Effi_dose_microSv_s_mat, Measured_dose)
        #Activity_all1["%s%s" %(nuclide,type_D)] = Dose_activity_optimized0
        Dose_activity_optimized1 = lsq_linear(Effi_dose_microSv_s_mat,  Measured_dose, method='trf', bounds=(0, 5000), lsq_solver='lsmr', verbose=0)
        Activity_all1["%s%s_s" %(nuclide,type_D)] = Dose_activity_optimized1["x"]
        Dose_all1["%s%s" %(nuclide,type_D)] = Measured_dose
        
    
    for un in range (1, 1001):
        dose = [0]* 20
        for i in range (0, 20):
            dose[i] = random.choice(list(Msdata[i]))
        Measured_dose = dose * Measured_ratio
        #Dose_activity_optimized1 = sp.cho_solve(sp.cho_factor(Effi_dose_microSv_s_mat), Measured_dose)
        #Dose_activity_optimized1, res, rnk, s = lstsq(Effi_dose_microSv_s_mat, Measured_dose)
        Dose_activity_optimized1 = lsq_linear(Effi_dose_microSv_s_mat,  Measured_dose, method='trf', bounds=(0, 5000), lsq_solver='lsmr', verbose=0)
        Activity_all1["%s%i" %(nuclide,un)] = Dose_activity_optimized1["x"]
        Dose_all1["%s%i" %(nuclide,un)] = dose
        
    Activity_all_data1= pd.DataFrame.from_dict(Activity_all1)
    Dose_all_data1= pd.DataFrame.from_dict(Dose_all1)
    
    Activity_all_data1.to_excel(writer,"%s_Activity" %(nuclide))
    Dose_all_data1.to_excel(writer,"%s_Dose" %(nuclide))
    
    # Plot a line between the means of each dataset
    fig = plt.figure(figsize=(10,6))
    #plt.plot(Activity_all_data1["Depth"].values, Activity_all_data1["%sDose_total" %(nuclide)], 'b-', label="Mean (TLD)")
    plt.plot(Activity_all_data1["Depth"].values, Activity_all_data1["%sDose_total_s" %(nuclide)], 'r-', label="Mean (TLD)_sparse")
    #plt.plot(Activity_all_data1["Depth"].values, Activity_all_data1["%sDose_total_cho" %(nuclide)], 'k-', label="Mean (TLD)_cho")
#    plt.plot(Activity_all_data1["Depth"].values, Activity_all_data1["%sRight" %(nuclide)], 'ro', label="Right (TLD)")
#    plt.plot(Activity_all_data1["Depth"].values, Activity_all_data1["%sUp" %(nuclide)], 'ko', label="Up (TLD)")
#    plt.plot(Activity_all_data1["Depth"].values, Activity_all_data1["%sLeft" %(nuclide)], 'bo', label="Left (TLD)")
#    plt.plot(Activity_all_data1["Depth"].values, Activity_all_data1["%sDown" %(nuclide)], 'yo', label="Down (TLD)")
    plt.plot(Activity_all_data1["Depth"].values, Measured_data["Activity_%s" %(nuclide)].values, 'g-', label= "Lab")
    if nuclide == "Cs":
        plt.plot(Activity_all_data1["Depth"].values, Measured_data["Activity_insitu_%s" %(nuclide)].values, 'y-', label= "Insitu(labr3)")

    plt.boxplot(Activity_all_data1.iloc[:, 6:1001], positions=Activity_all_data1["Depth"].values,  whis=[2.5,97.5], showfliers=False)
    
    # Reset the xtick locations.
    plt.xticks(Activity_all_data1["Depth"].values)
    plt.ylabel('Activity Sp. (Bq/kg)',  fontsize =12)
    plt.xlabel('Depth (cm)', fontsize=12)
    plt.legend()
    plt.xlim(0,100)
    plt.title('%s Activity ' %(nuclide))
    plt.savefig("Activity_dia_%s" %(nuclide))
    plt.show()
    
writer.save()