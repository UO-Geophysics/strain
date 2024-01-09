#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 17:36:49 2020

@author: sydneydybing
"""

from obspy.core import Stream, read
import numpy as np
import matplotlib.pyplot as plt

path_to_files = '/Users/sydneydybing/StrainProject/SeismicData/'
quake_folders = np.genfromtxt('/Users/sydneydybing/StrainProject/quake_folders.txt', dtype=str)
stas = np.genfromtxt('/Users/sydneydybing/StrainProject/stations.txt', dtype=str)
chans = ['EHZ']

#quake_folders_test = ['112_2010_7.2', '145_2011_6.4', '185_2014_6.8']
#stas_test = ['B007']

#quake_folders_test = ['125_2010_5.4']
#stas_test = ['B941']

quake_folders_test = ['150_2012_5.8']
stas_test = ['B006']



for quake in quake_folders_test:
    for sta in stas_test:
        for chan in chans:          
            
            data = Stream()
            
            try:
                
                data = read(path_to_files + quake + '/' + sta + '_' + chan + '.mseed')
                
                #data.plot()
                data_array = data[0].data
                
                times = range(data[0].stats.npts)
                times = np.asarray(times)/(data[0].stats.sampling_rate)
                                                     
                # Normalizing unfiltered data
                
                norm_value = data_array[0]
                data_length = data_array[0].shape
                normalize = np.full(data_length, norm_value)
                
                data_norm = np.subtract(data_array, normalize)
                
                # Plotting normalized fixed data
                
    #            plt.plot(times, data_norm)
    #            plt.xlim(0.,300.)
    #            plt.ylim()
    #            plt.xlabel('Time (s) from Earthquake Origin')
    #            plt.ylabel('Normalized Counts')
    #            plt.title(quake + ' Earthquake at PBO Station ' + sta + '_' + chan)
    
                st_norm = data.copy()
                st_norm[0].data = data_norm
                st_norm.plot()
                #st_norm.write(path_to_files + 'Normalized/' + quake + '/' + sta + '_' + chan + '.mseed', format='MSEED')
    
            except: 
            
                print(quake + " no station " + sta)                        