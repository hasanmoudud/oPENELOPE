import os 
from numpy import genfromtxt
import pandas as pd 
from tkinter import Tk
from tkinter import filedialog

# Change to working directory to current file location 
working_directory = filedialog.askdirectory(title='Please select working directory')
os.chdir(working_directory)

dose_all ={}
for i in range (1,11):
    if i > 9:
        filename_out =working_directory+"/dose-charge-%i.dat" %i
    else:
        filename_out =working_directory+"/dose-charge-0%i.dat" %i
    out_data = genfromtxt(filename_out)
    dose_all[i]=out_data
dose_data= pd.DataFrame.from_dict(dose_all, orient='index')
writer = pd.ExcelWriter(working_directory+"/Dose_Br3_D55.xlsx")
dose_data.to_excel(writer,'Dose')
writer.save()
print (dose_all)


