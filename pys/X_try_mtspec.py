#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 12:34:47 2020

@author: sydneydybing
"""
from obspy.core import read, Stream
import numpy as np
import matplotlib.pyplot as plt
from mtspec import mtspec

path_to_files = '/Users/sydneydybing/IRIS_pbo_data/Data_noise/'
quake_folders = np.genfromtxt(path_to_files + 'quake_folders_sel4.txt', dtype=str)
stas = np.genfromtxt(path_to_files + 'stations_sel4.txt', dtype=str)

quake1 = ['152_2012_6.0']
sta1 = ['B022']

for quake in quake1:   
    for sta in stas:
        
        try:
        
            path_to_files = '/Users/sydneydybing/IRIS_pbo_data/Data_noise/Processed/RMS/'
                
            RMS_strain = Stream()
            RMS_strain = read(path_to_files + quake + '/' + sta + '_' + 'RMS.mseed')
            
            sampling_rate = RMS_strain[0].stats.sampling_rate
            RMS_data = RMS_strain[0].data
            
            delta = 1/sampling_rate
            time_bandwidth = 5
            nfft = len(RMS_data)
            number_of_tapers = 6
            
            spec, freq = mtspec(data=RMS_data, delta=delta, time_bandwidth=time_bandwidth, nfft=nfft, number_of_tapers=number_of_tapers)
            
            period=1/freq
            
            plt.semilogx(period, spec)
            plt.xlim(0.5, 50)
            #plt.ylim(-0.05, 0.4)
            plt.xlabel('Period (s)')
            plt.ylabel('Power Spectral Density')
            plt.title('Noise before event ' + quake + ', station ' + sta)
            
            plt.savefig('/Users/sydneydybing/IRIS_pbo_data/Data_noise/mtspec_plots/' + quake + '/' + sta + '.jpg', format="JPEG", dpi=400)
            
            plt.close()
        
        except:
            
            print(quake + " no station " + sta)
       