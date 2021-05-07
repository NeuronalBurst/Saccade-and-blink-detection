# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 11:52:30 2021

@author: Nikhil
"""

import numpy as np
import pandas as pd
import glob
import os
from os import listdir


# calculation of distances from calibration
average_hor = 47.72225 # mean distance in pixels from l1 to r1
average_ver = 32.3 # mean distance in pixels from fixation to top

l1_to_r1 = 19.5 # distance in cm from l1 to r1
f1_to_f2 = 10 # distance in cm from f1 to f2

cm_per_pixel_x =   l1_to_r1/average_hor
cm_per_pixel_y =  f1_to_f2/average_ver

cm_per_pixel_x, cm_per_pixel_y

# gets distance in pixels and converts it into degrees
def pixels_to_degrees(distance, x=True):
    if (x):
        to_cm = distance * cm_per_pixel_x # = cm per pixels
    else:
        to_cm = distance * cm_per_pixel_y
    to_degree = np.degrees(np.arctan(to_cm / 65)) # distance to the screen
    return to_degree
    
 

def detect_saccade(filename):
    
    x_dist=[]
    y_dist=[]    
    eye_param_file = pd.read_csv(filename)
    x_dist = np.array(eye_param_file[['x_dist']]) 
    y_dist = np.array(eye_param_file[['y_dist']])
    
    index=0    
    x_deg=[]
    y_deg=[]
    
    while (index < len(x_dist)):
    
        x_deg.append(pixels_to_degrees(x_dist[index],True))
        y_deg.append(pixels_to_degrees(y_dist[index],False))
        
        index += 1
        
    x_deg=np.array(x_deg)
    y_deg=np.array(y_deg)
        
    
    csv_file = pd.read_csv(filename)
    csv_file["x_deg"] = x_deg
    csv_file["y_deg"] = y_deg
    
    csv_file.to_csv(filename, index=True)
    
    # data2=['x_deg','y_deg']
    # writer=csv.writer(file)
    # writer.writerow(data2)
    
    # for m in data1:
    #     writer.writerow(m)

    # file.close
    


# pick all folders in the directory

folders=glob.glob("F:\\sacc_analysis\\Full_Data_and_Saccades\\Subject1Stim\\figures_*")

for f in range(0, len(folders)):
    files=listdir(folders[f])
    os.chdir(folders[f])
    
    filename=[]
    # only pick files with eye parameters
    for file in files:
        if file[24:40] == 'eye_trace_params':
            filename=file
    # detect saccades for files
    detect_saccade(filename) 

