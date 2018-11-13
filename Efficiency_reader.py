import os
from numpy import genfromtxt
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk
from tkinter import filedialog
import os
# Change to working directory to current file location 
#abspath = os.path.abspath(__file__)
#dname = os.path.dirname(abspath)
#os.chdir(dname)

working_directory = filedialog.askdirectory(title='Please select working directory')
os.chdir(working_directory)

 #------------- Input ----------
 
source_thickness = 10.0 # cm 
Srad_inner = 2.0 #cm
Srad_outter = 52.0 #cm 
soil_density = 1.4 #g/cm3 
No_of_layer= 60   # layer no * 3

#-------------------------------

density_out = {}
uncertainty_out = {}
total_counts = {}

layer_no = 3
while layer_no < No_of_layer:
    filename_out =working_directory+"/KP_Ra_%i_6.txt" %(layer_no)
    out_data = genfromtxt(filename_out)
    x = out_data[ : , 0]
    y = out_data[ : , 1]
    plt.plot(x, y, "-")
    plt.show()
    interval_enr = out_data[1,0] - out_data[0,0]
    density_out [layer_no]= out_data [-1, 1] * interval_enr  # Location  of energy line
    uncertainty_out [layer_no]= out_data [-1, 2] * interval_enr
    total_counts[layer_no] = sum(out_data [ : , 1]*interval_enr)
    layer_no +=5

volume_in = 3.1416*source_thickness* Srad_inner**2
volume_out = 3.1416*source_thickness* Srad_outter**2
volume = volume_out - volume_in
mass= (volume*soil_density)/1000.0

density_data = pd.DataFrame.from_dict(density_out, orient='index')
density_data.index = density_data.index.astype(int)
density_data = density_data.sort_index()

uncertainty_data= pd.DataFrame.from_dict(uncertainty_out, orient='index')
uncertainty_data.index = uncertainty_data.index.astype(int)
uncertainty_data = uncertainty_data.sort_index()

total_counts_data = pd.DataFrame.from_dict(total_counts, orient='index')
total_counts_data.index = total_counts_data.index.astype(int)
total_counts_data = total_counts_data.sort_index()

uncertainty_per= uncertainty_data.div(density_data)
uncertainty_per = uncertainty_per.multiply(100)

density_M = density_data * mass
uncertainty_M = uncertainty_data * mass
total_counts_data_M = total_counts_data * mass

writer = pd.ExcelWriter(working_directory+"/Simulation_Kp_Ra226_352_1.xlsx")
density_data.to_excel(writer,'Efficiency')
density_M.to_excel(writer,'Density_mass')
uncertainty_data.to_excel(writer,'Uncertainty')
uncertainty_M.to_excel(writer,'Uncertainty_mass')
uncertainty_per.to_excel(writer,'Uncertainty_per')
total_counts_data.to_excel(writer,'total_counts')
total_counts_data_M.to_excel(writer,'total_counts_mass')
writer.save()