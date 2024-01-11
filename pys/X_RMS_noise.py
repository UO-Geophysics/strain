#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 18:48:42 2020

@author: sydneydybing
"""

from obspy.core import Stream, read
import numpy as np
import matplotlib.pyplot as plt

path_to_files = '/Users/sydneydybing/IRIS_pbo_data/Data_noise/'
quake_folders = np.genfromtxt(path_to_files + 'quake_folders_sel4.txt', dtype=str)
stas = np.genfromtxt(path_to_files + 'stations_sel4.txt', dtype=str)
chans = ['BS1', 'BS2', 'BS3', 'BS4']

quake_folders_test = ['172_2012_6.2']
stas_test = ['B007']

for quake in quake_folders_test:   
    for sta in stas_test:
                    
        try:
            
            BS1 = Stream()
            BS2 = Stream()
            BS3 = Stream()
            BS4 = Stream()
            
            BS1 = read(path_to_files + 'Processed/' + quake + '/' + sta + '_' + 'BS1.mseed')
            BS2 = read(path_to_files + 'Processed/' + quake + '/' + sta + '_' + 'BS2.mseed')
            BS3 = read(path_to_files + 'Processed/' + quake + '/' + sta + '_' + 'BS3.mseed')
            BS4 = read(path_to_files + 'Processed/' + quake + '/' + sta + '_' + 'BS4.mseed')
            
            BS1.plot()
            #BS2.plot()
            #BS3.plot()
            #BS4.plot()
            
            RMS_strain = np.sqrt(((BS1[0].data)**2 + (BS2[0].data)**2 + (BS3[0].data)**2 + (BS4[0].data)**2)/4)         
            
            times = range(BS1[0].stats.npts)
            times = np.asarray(times)/(BS1[0].stats.sampling_rate) 
            
            plt.plot(times, RMS_strain*10**6, label = quake)
            
            timeseries = [0.,60.]
            plt.xlim(timeseries)
            timeseries = str(timeseries)
            
            plt.xlabel('Time (s)')
            plt.ylabel('RMS Microstrain ($10^{-6}$ m/m)')
            plt.title(quake + ' Earthquake at PBO Station ' + sta)
            #plt.legend(loc = 1)
            
            #plt.show()
            #plt.close()
            #plt.savefig('/Users/sydneydybing/IRIS_pbo_data/Data_noise/compare_for_meeting/' + quake + '/' + sta + '.jpg', format="JPEG", dpi=400)
            
            RMS_st = BS1.copy()
            RMS_st[0].stats.channel = 'BSR'
            RMS_st[0].data = RMS_strain
            
            #RMS_st.plot()
            #print(RMS_st[0].stats)
            
            #RMS_st.write(path_to_files + 'Processed/RMS/' + quake + '/' + sta + '_RMS' + '.mseed', format='MSEED')
                
        except:
            
            print(quake + " no station " + sta)