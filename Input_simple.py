# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 13:06:04 2018

@author: mhasan
"""
import os
import subprocess
import collections
import pandas as pd


# Change to working directory to current file location 
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

energy = 0.662
particle= "5e8"
iner_radius = 2.0  # cm
detector_ht = 3.81 # cm
detector_rad = 3.81/2.0 #cm  
#depth_borehole = 100.0 #cm
out_radius = 50.0 + iner_radius  # cm 
layer_width = [13, 23, 33, 43, 53, 63, 73, 83, 93, 103, 113, 123]
No_of_layer= len(layer_width) * 3

for layer_b in range(0 , len(layer_width)):
    filename_s= dname+"/k_s%i.inp" %(layer_width[layer_b])
    if layer_b == 0:
        layer_thickness = layer_width[0]
    else:
        layer_thickness = layer_width[layer_b] - layer_width[layer_b-1]
    source_pos = layer_width[layer_b] - (layer_thickness/2.0)
    layer_ind_thick = 0.0
    layer_no = 1
    layer_no_d = 1
    layer_no_s = 1
    with open(filename_s, "w") as myfile:
        myfile.write ("TITLE  In situ\n")
        myfile.write ("       .\n")
        myfile.write ("GSTART\n")
        for layer_c in range(0 , len(layer_width)):
            if layer_c == 0:
                layer_thickness_c = layer_width[0]
            else:
                layer_thickness_c = layer_width[layer_c] - layer_width[layer_c-1]
            myfile.write ("LAYER              %2.2f          %2.2f   %i\n" %(layer_ind_thick, (layer_ind_thick+((layer_thickness_c/2.0) -(detector_ht/2.0))),layer_no))
            myfile.write ("CYLIND   1         %2.1f           %2.1f\n"% (iner_radius, out_radius))
            layer_ind_thick = layer_ind_thick+((layer_thickness_c/2.0) -(detector_ht/2.0))
            layer_no +=1

            myfile.write ("LAYER              %2.2f          %2.2f   %i\n" %(layer_ind_thick,(layer_ind_thick+detector_ht), layer_no))
            myfile.write ("CYLIND   2         0.0           %2.2f\n" %detector_rad)
            myfile.write ("CYLIND   1         %2.1f           %2.1f\n"% (iner_radius, out_radius))
            layer_ind_thick =(layer_ind_thick+detector_ht)
            layer_no +=1 

            myfile.write ("LAYER              %2.2f          %2.2f   %i\n" %(layer_ind_thick,(layer_ind_thick+(layer_thickness_c/2.0)-(detector_ht/2.0)),layer_no))
            myfile.write ("CYLIND   1         %2.1f           %2.1f\n" % (iner_radius, out_radius))
            layer_ind_thick = (layer_ind_thick+(layer_thickness_c/2.0)-(detector_ht/2.0))
            layer_no +=1
        
        myfile.write ("GEND\n")
        myfile.write ("       .\n")
        myfile.write ("SKPAR  2\n")
        myfile.write ("SENERG    %2.4fe6\n" %energy)
        myfile.write ("STHICK   %2.1f\n" %layer_thickness)
        myfile.write ("SRADII   %2.1f        %2.1f\n" %(iner_radius, out_radius))
        myfile.write ("SPOSIT   0    0    %3.4F\n" %source_pos)
        myfile.write ("SCONE    0.0   0.0    180.0\n")
        myfile.write ("       .\n")
        myfile.write ("MFNAME soil.mat\n")
        myfile.write ("MSIMPA 3.0e5 1.0e4 3.0e5 0.2 0.2 1.0e6 1.0e6\n")
        myfile.write ("MFNAME LaBr3.mat\n")
        myfile.write ("MSIMPA 3.0e5 1.0e4 3.0e5 0.2 0.2 1.0e6 1.0e6\n")
        myfile.write ("       .\n")
        while layer_no_s <= No_of_layer:
            layer_no_s +=1
            myfile.write ("ENDETC  0.0000 %2.4fe6 512\n" %energy)
            myfile.write ("EDSPC  KP_Ra_%i_%i.txt\n" %(layer_no_s,source_pos))
            myfile.write ("EDBODY    %i    1\n" %layer_no_s)
            layer_no_s +=2
        myfile.write ("       .\n")
        while layer_no_d <= No_of_layer:
            layer_no_d +=1
            myfile.write ("DOSE2D    %i    1    1    1\n" %layer_no_d)
            layer_no_d +=2 
        myfile.write ("       .\n")
        myfile.write ("NSIMSH %s\n"%particle)
        myfile.write ("       .\n")
        myfile.write ("END\n")
        myfile.close()