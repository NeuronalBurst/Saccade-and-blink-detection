# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 12:06:29 2021

@author: Nikhil
"""

import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt

# calculation of distances from calibration
average_hor = 47.72225 # mean distance in pixels from l1 to r1
average_ver = 32.3 # mean distance in pixels from fixation to top

l1_to_r1 = 19.5 # distance in cm from l1 to r1
f1_to_f2 = 10 # distance in cm from f1 to f2

cm_per_pixel_x =   l1_to_r1/average_hor
cm_per_pixel_y =  f1_to_f2/average_ver

cm_per_pixel_x, cm_per_pixel_y

# load coordinate files

#change this to the folder which you want to select

videofiles = '.'


from os import listdir

from os.path import isfile, join
os.chdir('F:/sacc_analysis/Full_Data_and_Saccades/Subject1Stim')
onlyfiles = [f for f in listdir(videofiles) if isfile(join(videofiles, f))]

# only process the data which has been averaged
csvs = []
for file in onlyfiles:
    if file[0:8] == 'averaged' and file[-5]=='d':
        csvs.append(file)
csvs


# gets distance in pixels and converts it into degrees
def pixels_to_degrees(distance, x=True):
    if (x):
        to_cm = distance * cm_per_pixel_x # = cm per pixels
    else:
        to_cm = distance * cm_per_pixel_y
    to_degree = np.degrees(np.arctan(to_cm / 65)) # distance to the screen
    return to_degree
    
    

def detect_saccade(filename):

    
    # create new directory for each file
    if not os.path.exists('figures_' + str(filename[:-60])):
        os.makedirs('figures_' + str(filename[:-60]))

    
    
   # max_amplitudes = []
    
    eye_traces = pd.read_csv(filename)
    x = np.array(eye_traces[['xaverage']]) 
    y = np.array(eye_traces[['yaverage']])
    
    index=0
    x_dist=[]
    y_dist=[]
    x_deg=[]
    y_deg=[]
    
    while (index < len(x)):
        
        x_dist.append(abs(x[index] - x[index+1]))
        y_dist.append(abs(y[index] - y[index+1]))
        
        x_deg.append(pixels_to_degrees(x_dist[index],True))
        y_deg.append(pixels_to_degrees(y_dist[index],False))
        
        x_vel_per_sec=(x_deg[index]*1000)/33.33
        y_vel_per_sec=(y_deg[index]*1000)/33.33
        
        sacc_vel_thresh = 30
        
        if x_vel_per_sec>sacc_vel_thresh:
            
            plt.xlabel("time in ms")
            plt.ylabel("deflection in degrees")
            plt.xlim(-60,120)
            plt.ylim(-15,15)
            plt.plot([x_deg[index-2],x_deg[index+6]],[1,9]) #assuming saccade duration of 120ms
            fig, ax = plt.subplots()
            fig.savefig("figures_" + filename[:-60] + "/" + "x_" + str(index) + ".png")
            plt.close();
            
        if y_vel_per_sec>sacc_vel_thresh:

            plt.xlabel("time in ms")
            plt.ylabel("deflection in degrees")
            plt.xlim(-60,120)
            plt.ylim(-15,15)
            plt.plot([y_deg[index-2],y_deg[index+6]],[1,9]) #assuming saccade duration of 120ms
            fig, ax = plt.subplots()
            fig.savefig("figures_" + filename[:-60] + "/" + "y_" + str(index) + ".png")
            plt.close();   

        if (x_vel_per_sec>sacc_vel_thresh) and (y_vel_per_sec>sacc_vel_thresh):
            file = open("XY_index_file.txt","a+")
            file.write(index)
            file.close
        
    index += 1
        

# detect saccades for all files
for csv in csvs:
    detect_saccade(csv)        
        
        
        