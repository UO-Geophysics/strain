#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 11:26:25 2020

@author: sydneydybing
"""

from obspy.core import Stream, read
import numpy as np
import matplotlib.pyplot as plt

path_to_files = '/Users/sydneydybing/StrainProject/M6_500km_sel/'
quake_folders = np.genfromtxt('/Users/sydneydybing/StrainProject/quake_folders.txt', dtype=str)
stas = np.genfromtxt('/Users/sydneydybing/StrainProject/stations.txt', dtype=str)

quake_folders_test = ['59_2008_6.3']
stas_test = ['B017']


for quake in quake_folders_test:
    for sta in stas_test:        
            
        #try:
        
        # Strain data
    
        strain_data = Stream()
        strain_data = read(path_to_files + 'StrainData_sel/' + quake + '/' + sta + '_RMS.mseed')
        
        #strain_data.plot()
        strain_data_array = strain_data[0].data
        
        strain_times = range(strain_data[0].stats.npts)
        strain_times = np.asarray(strain_times)/(strain_data[0].stats.sampling_rate)
    
        # Seismic data
    
        seismic_data = Stream()
        seismic_data = read(path_to_files + 'SeismicData_sel/' + quake + '/' + sta + '_EHZ.mseed')
                        
        #seismic_data.plot()
        seismic_data_array = seismic_data[0].data
        
        seismic_times = range(seismic_data[0].stats.npts)
        seismic_times = np.asarray(seismic_times)/(seismic_data[0].stats.sampling_rate)
        
        # Plotting strain data
        
        ax1 = plt.subplot(1,1,1)
        
        ax1.set_xlabel('Times (s) from Earthquake Origin')
        ax1.set_ylabel('RMS Microstrain ($10^{-6}$ m/m)')
        ax1.plot(strain_times, strain_data_array*10**6, color = 'C0', label = 'Strain')
        #ax1.set_ylim(0,1)
        
        # Plotting seismic data
        
        ax2 = ax1.twinx()
        ax2.set_ylabel('Normalized Counts', rotation = 270)
        ax2.plot(seismic_times, seismic_data_array, color = 'C1', label = 'Seismic')
        ax2.plot(0,0, color = 'C0', label = 'Strain')
        ax2.set_ylim(-1000000,750000)
        
        plt.title(quake + ' Earthquake at PBO Station ' + sta)
        #plt.xlim(0,25)
        plt.legend()
        
        plt.show()
        #plt.savefig('/Users/sydneydybing/IRIS_pbo_data/Sel4_comp_figs/Limited/' + quake + '/' + sta + '.jpg', format="JPEG", dpi=400)
       
        plt.close()
        
        #except:
            
            #print(quake + " no station " + sta)