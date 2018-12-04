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

source_thickness = 10.0 # cm 
Srad_inner = 2.5 #cm
Srad_outter = 62.5 #cm 
soil_density = 1.4 #g/cm3 


volume_in = 3.1416*source_thickness* Srad_inner**2
volume_out = 3.1416*source_thickness* Srad_outter**2
volume = volume_out - volume_in
mass= (volume*soil_density)/1000.0

dose_all ={}
for i in range (1,11):
    if i > 9:
        filename_out =working_directory+"/dose-charge-%i.dat" %i
    else:
        filename_out =working_directory+"/dose-charge-0%i.dat" %i
    out_data = genfromtxt(filename_out)
    dose_all[i]=out_data[2] * (1.6E-19*1000/0.000001) * mass  # microSV
dose_data= pd.DataFrame.from_dict(dose_all, orient='index')
writer = pd.ExcelWriter(working_directory+"/Dose_KP_Ra226D_mass.xlsx")
dose_data.to_excel(writer,'Dose')
writer.save()
print (dose_all)


