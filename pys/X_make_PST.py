#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  8 13:14:58 2020

@author: sydneydybing
"""

from obspy.core import Stream, read
import numpy as np
import matplotlib.pyplot as plt

path_to_files = '/Users/sydneydybing/StrainProject/M6_500km_sel/StrainData_sel/Trimmed/'
quake_folders = np.genfromtxt('/Users/sydneydybing/StrainProject/M6_500km_sel/quake_folders_sel.txt', dtype=str)
stas = np.genfromtxt('/Users/sydneydybing/StrainProject/stations.txt', dtype=str)

quake_folders_test = ['59_2008_6.3']
stas_test = ['B035']

for quake in quake_folders:
    for sta in stas:        
        
        #print(sta)    
        
        try:
        
            # Strain data
        
            tRMS = read(path_to_files + quake + '/' + sta + '_tRMS.mseed')
            
            #print(tRMS[0].stats)
            
            tRMS_data = tRMS[0].data # numpy array of strain values
            
            #tRMS_points = range(tRMS[0].stats.npts) # range of number of points in stream
            #print(np.asarray(tRMS_times)) # prints list of sample numbers
            #tRMS_times = np.asarray(tRMS_points)/(tRMS[0].stats.sampling_rate)
            #print(tRMS_times) # numpy array of time steps
            
            #insitalize the outut stream
            pst = tRMS.copy()
            
            #loop voer samples
            for k in range(1,len(tRMS[0].data)): #avoid starting at zero
                
                #grab progressively longer windows
                strain = tRMS[0].data[0:k]
                
                #what is the peak value in that window?
                max_strain = max(strain)
                
                #put that back into the output stream
                pst[0].data[k] = max_strain
                
            pst[0].stats.channel = 'PST'    
            pst.plot()
            pst.write('/Users/sydneydybing/StrainProject/M6_500km_sel/StrainData_sel/Trimmed/PeakStrains/' + quake + '/' + sta + '_PST' + '.mseed', format='MSEED')
                 
        except:
            
            print(quake + " no station " + sta)
            
            
            