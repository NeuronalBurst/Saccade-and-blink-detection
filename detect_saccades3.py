# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 13:16:10 2021

@author: Nikhil
"""
import numpy as np
import pandas as pd
import os
from os import listdir
import matplotlib.pyplot as plt
import glob


def detect_saccade(filename):
    
    x_deg=[]
    y_deg=[]
    eye_param_file = pd.read_csv(filename)
    x_deg = np.array(eye_param_file[['x_deg']]) 
    y_deg = np.array(eye_param_file[['y_deg']])
    
    
    sacc_vel_thresh = 30
    
    x_vel_per_sec=(x_deg*1000)/33.33
    y_vel_per_sec=(y_deg*1000)/33.33
    
    count_x=0
    count_y=0
    
    for index in range(0, len(x_deg)):
    
        
        if x_vel_per_sec[index]>sacc_vel_thresh and np.any(x_deg[index-2:index+6]>=2) :
            
            plt.xlabel("time in ms")
            plt.ylabel("saccades in degrees")
            # plt.xlim(0,8)
            ticks=np.arange(0,8)
            labels=np.arange(-40, 120, step=20)
            plt.xticks(ticks,labels)
            plt.ylim(-5,5)
            plt.plot(x_deg[index-2:index+6]) #assuming max saccade duration of 100ms
            plt.savefig("x_" + str(index) + ".png")
            plt.close();
            count_x += 1
            
        if y_vel_per_sec[index]>sacc_vel_thresh and np.any(y_deg[index-2:index+6]>=2):
    
            plt.xlabel("time in ms")
            plt.ylabel("saccades in degrees")
            ticks=np.arange(0,8)
            labels=np.arange(-40, 120, step=20)
            plt.xticks(ticks,labels)
            plt.ylim(-5,5)
            plt.plot(y_deg[index-2:index+6]) #assuming max saccade duration of 100ms
            plt.savefig("y_" + str(index) + ".png")
            plt.close();  
            count_y += 1
    
        if (x_vel_per_sec[index]>sacc_vel_thresh) and (y_vel_per_sec[index]>sacc_vel_thresh) and np.any(x_deg[index-2:index+6]>=2) and np.any(y_deg[index-2:index+6]>=2)  :
            file = open("XY_index_file.txt","w")
            file.write(str(index))
            file.close
            
    count_file = open("saccade_count.txt","w")
    # data=['x_saccades=','y_saccades=']
    # with open('saccade_count.txt', 'w') as count_file:
    #     for d in range(0,len(data)-1):
    count_file.write('%s %d\n' %('x_saccades=', count_x))
    count_file.write('%s %d\n' %('y_saccades=', count_y))
            
            # count_file.write(str("x_saccades" + "=" + count_x + "\n"))
            # count_file.write(str("y_saccades" + "=" + count_y + "\n"))
            # count_file.close();
    
        
    # index += 1
    # index
    
    
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