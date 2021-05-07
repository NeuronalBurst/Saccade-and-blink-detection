# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 11:42:43 2021

@author: Nikhil
"""

import numpy as np
import os
import pandas as pd
import csv


# load coordinate files

#change this to the folder which you want to select

videofiles = '.'


from os import listdir

from os.path import isfile, join
os.chdir('F:/sacc_analysis/Full_Data_and_Saccades/Subject1Stim')
onlyfiles = [f for f in listdir(videofiles) if isfile(join(videofiles, f))]

# only process the data which has been averaged
xy_avg_files = []
for file in onlyfiles:
    if file[0:8] == 'averaged' and file[-5]=='d':
        xy_avg_files.append(file)


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
   
    
    while (index < len(x)-1):
        
        x_dist.append(abs(x[index] - x[index+1]))
        y_dist.append(abs(y[index] - y[index+1]))

        index += 1
    
    x_dist=np.array(x_dist)
    y_dist=np.array(y_dist)
    
    
    # for n in x_dist:
    #     data1=[x_dist[n],y_dist[n]]
    data1=np.concatenate((x_dist, y_dist), axis=1)
    
    
    file = open("figures_" + filename[:-60] + "/" + filename[:-60] + 'eye_trace_params.csv',"w", newline='')
    data2=['x_dist','y_dist']
    writer=csv.writer(file)
    writer.writerow(data2)
    
    for m in data1:
        writer.writerow(m)

    
         
    
    
    # with file:
    #     writer=csv.writer(file)
    #     writer.writerows(data)
        #writer.writerow(data2)
        
    file.close
    
# detect saccades for all files
for file in xy_avg_files:
    detect_saccade(file) 