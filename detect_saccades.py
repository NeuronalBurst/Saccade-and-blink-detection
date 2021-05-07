# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 18:00:31 2021

@author: Nikhil
"""
import numpy as np
import pandas as pd
import csv
import glob
import os
import matplotlib.pyplot as plt

# import pdb

from os import listdir

# input calibration data, convert pixels to cms
average_hor = 47.72225 # mean distance in pixels from l1 to r1
average_ver = 32.3 # mean distance in pixels from fixation to top

l1_to_r1 = 19.5 # distance in cm from l1 to r1
f1_to_f2 = 10 # distance in cm from f1 to f2

cm_per_pixel_x =   l1_to_r1/average_hor
cm_per_pixel_y =  f1_to_f2/average_ver

cm_per_pixel_x, cm_per_pixel_y

# convert cms to degrees
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

    
    
    eye_traces = pd.read_csv(filename)
    x = np.array(eye_traces[['xaverage']]) 
    y = np.array(eye_traces[['yaverage']])
    
    
    # # plot x and y full traces
    # ############
    # plt.xlabel("frame no")
    # plt.ylabel("raw trace")
    # x_ticks=np.arange(1, len(x), step=30)
    # x_labels=np.arange(0, len(x)/30, step=1)
    # # x_ticks=np.arange(index-2,index+8)
    # # x_labels=np.arange(index-2,index+8)
    # y_ticks=np.arange(np.amin(x),np.amax(x), step=50)
    # y_labels=np.arange(np.amin(x),np.amax(x), step=50)
    # plt.xticks(x_ticks,x_labels)
    # plt.yticks(y_ticks,y_labels)
    # # plt.ylim(np.amin(x),np.amax(x))
    # plt.plot(x) 
    # # plt.title('%s %d\n' %('max deflection in deg=', np.amax(x_deg[index-2:index+6])))
    # plt.savefig("figures_" + filename[:-60] + "/" + "x_full_trace" + ".png")
    # plt.close();
    
    
    # plt.xlabel("frame no")
    # plt.ylabel("raw trace")
    # y_ticks=np.arange(1, len(y), step=30)
    # y_labels=np.arange(0, len(y)/30, step=1)
    # # x_ticks=np.arange(index-2,index+8)
    # # x_labels=np.arange(index-2,index+8)
    # y_ticks=np.arange(np.amin(y),np.amax(y), step=50)
    # y_labels=np.arange(np.amin(y),np.amax(y), step=50)
    # plt.xticks(x_ticks,x_labels)
    # plt.yticks(y_ticks,y_labels)
    # # plt.ylim(np.amin(x),np.amax(x))
    # plt.plot(y) 
    # # plt.title('%s %d\n' %('max deflection in deg=', np.amax(x_deg[index-2:index+6])))
    # plt.savefig("figures_" + filename[:-60] + "/" + "y_full_trace" + ".png")
    # plt.close();
    
    ##############
    
    
    index=0
    x_dist=[]
    y_dist=[]
    x_deg=[]
    y_deg=[]
    
    while (index < len(x)-1):
        
        x_dist.append(abs(x[index] - x[index+1]))
        y_dist.append(abs(y[index] - y[index+1]))
        
        x_deg.append(pixels_to_degrees(x_dist[index],True))
        y_deg.append(pixels_to_degrees(y_dist[index],False))

        index += 1
    
    
    
    x_dist=np.array(x_dist)
    y_dist=np.array(y_dist)
    
    x_deg=np.array(x_deg)
    y_deg=np.array(y_deg)
    
    
    
    x=x[:-1]  # equalisation of array lengths with x_dist etc.
    y=y[:-1]
    
    # ind=np.arange(1,len(x)+1).reshape(len(x),1) #index of elements in data1
    
    data1=np.concatenate((x,y,x_dist, y_dist, x_deg, y_deg), axis=1)
    
    
    file = open("figures_" + filename[:-60] + "/" + filename[:-60] + 'eye_trace_params.csv',"w", newline='')
    data2=['index','x_dist','y_dist', 'x_deg','y_deg']
    writer=csv.writer(file)
    writer.writerow(data2)
    
    
    for m in data1:
        writer.writerow(m)
     
    file.close()    
    #plot saccade figures 
    sacc_vel_thresh = 30
    
    x_vel_per_sec=(x_deg*1000)/33.33
    y_vel_per_sec=(y_deg*1000)/33.33
    
    index=0
    count_x=0
    count_y=0
    
    
    # for index in range(0, len(x_deg)):
    while index < len(x)-6: #6 for index+6, index errors
        
        loop_log=None
                    
        if x_vel_per_sec[index]>sacc_vel_thresh and np.any(x_deg[index-2:index+6]>=2) and np.all(x_deg[index-2:index+6]):
        
            plt.xlabel("time in seconds")
            plt.ylabel("raw trace")
            # x_ticks=np.arange(0,10)
            # x_labels=np.arange(-33*2, 33*8, step=33)
            x_ticks=np.round((np.arange(index-2,index+6)/30),2) #convert frames to seconds
            x_labels=np.round((np.arange(index-2,index+6)/30),2)
            # y_ticks=np.arange(np.amin(x_deg),np.amax(x_deg))
            # y_labels=np.arange(np.amin(x_deg),np.amax(x_deg))
            plt.xticks(x_ticks,x_labels)
            # plt.yticks(y_ticks,y_labels)
            # plt.ylim(np.amin(x),np.amax(x))
            plt.plot(x_ticks,x[index-2:index+6]) #assuming max saccade duration of 100ms
            plt.title('%s %d\n' %('max deflection in deg=', np.amax(x_deg[index-2:index+6])))
            plt.savefig("figures_" + filename[:-60] + "/" + "x_" + str(np.round((index/30),2)) + ".png")
            plt.close();
            count_x += 1
            
            loop_log=1
    
        if y_vel_per_sec[index]>sacc_vel_thresh and np.any(y_deg[index-2:index+6]>=2) and np.all(y_deg[index-2:index+6]):
    
            plt.xlabel("time in seconds")
            plt.ylabel("raw trace")
            # x_ticks=np.arange(0,10)
            # x_labels=np.arange(-33*2, 33*8, step=33)
            x_ticks=np.round((np.arange(index-2,index+6)/30),2)
            x_labels=np.round((np.arange(index-2,index+6)/30),2)
            # y_ticks=np.arange(np.amin(y_deg),np.amax(y_deg))
            # y_labels=np.arange(np.amin(y_deg),np.amax(y_deg))
            plt.xticks(x_ticks,x_labels)
            # plt.yticks(y_ticks,y_labels)
            # plt.ylim(np.amin(y),np.amax(y))
            # try:
            plt.plot(x_ticks,y[index-2:index+6]) #assuming max saccade duration of 100ms
            # except:
            #     pdb.set_trace()
                
            plt.title('%s %d\n' %('max deflection in deg=', np.amax(y_deg[index-2:index+6])))
            plt.savefig("figures_" + filename[:-60] + "/" + "y_" + str(np.round((index/30),2)) + ".png")
            plt.close();  
            count_y += 1
            
            loop_log=1

        if x_vel_per_sec[index]>sacc_vel_thresh and y_vel_per_sec[index]>sacc_vel_thresh and np.all(x_deg[index-2:index+6]) and np.all(y_deg[index-2:index+6]) and np.any(x_deg[index-2:index+6]>=2) and np.any(y_deg[index-2:index+6]>=2) :
            file = open("figures_" + filename[:-60] + "/" + "XY_index_file.txt","w")
            file.write(str(np.round((index/30),2)))
            file.close
            
            loop_log=1
                
        if loop_log is not None:
            index += 6
        else:
            index += 1
            
        
        
        
    count_file = open("figures_" + filename[:-60] + "/" + "saccade_count.txt","w")
    # data=['x_saccades=','y_saccades=']
    # with open('saccade_count.txt', 'w') as count_file:
    #     for d in range(0,len(data)-1):
    count_file.write('%s %d\n' %('x_saccades=', count_x))
    count_file.write('%s %d\n' %('y_saccades=', count_y))
    
        
    

# pick subject folders and subdirectories

subj_folders=glob.glob("F:\\sacc_analysis\\*")

# os.chdir('F:\sacc_analysis')
# subj_folders=glob.glob("*")
for sf in range(0,len(subj_folders)):
    files=listdir(subj_folders[sf])
    
    os.chdir(subj_folders[sf])
    # for f in range(0, len(folders)):
    #     files=listdir(folders[f])
        
    
        
    # only pick files with eye parameters
    for file in files:
        if file[0:8] == 'averaged' and file[-5]=='d':
            filename=file
            # path=os.getcwd()
            # os.chdir(path + "\\" +  subj_folders[sf])
            # detect saccades for files
            detect_saccade(filename) 