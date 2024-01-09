#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 18:48:42 2020

@author: sydneydybing
"""

from obspy.core import Stream, read
import numpy as np
import matplotlib.pyplot as plt

path_to_files = '/Users/sydneydybing/StrainProject/StrainData/Processed/'
quake_folders = np.genfromtxt('/Users/sydneydybing/StrainProject/quake_folders.txt', dtype=str)
small_quake_folders = np.genfromtxt('/Users/sydneydybing/StrainProject/M6_500km_sel/StrainData_sel/Trimmed/PeakStrains/grp1_folders_2.txt', dtype=str)
stas = np.genfromtxt('/Users/sydneydybing/StrainProject/stations.txt', dtype=str)
chans = ['BS1', 'BS2', 'BS3', 'BS4']

quake_folders_test = ['112_2010_7.2', '145_2011_6.4', '185_2014_6.8']
stas_test = ['B028']



for quake in quake_folders:   
    for sta in stas:
                    
        try:
            
            BS1 = Stream()
            BS2 = Stream()
            BS3 = Stream()
            BS4 = Stream()
            
            BS1 = read(path_to_files + quake + '/' + sta + '_' + 'BS1.mseed')
            BS2 = read(path_to_files + quake + '/' + sta + '_' + 'BS2.mseed')
            BS3 = read(path_to_files + quake + '/' + sta + '_' + 'BS3.mseed')
            BS4 = read(path_to_files + quake + '/' + sta + '_' + 'BS4.mseed')
            
#            BS1.plot()
#            BS2.plot()
#            BS3.plot()
#            BS4.plot()
            
            RMS_strain = np.sqrt(((BS1[0].data)**2 + (BS2[0].data)**2 + (BS3[0].data)**2 + (BS4[0].data)**2)/4)         
            
            times = range(BS1[0].stats.npts)
            times = np.asarray(times)/(BS1[0].stats.sampling_rate) 
            
            #plt.plot(times, RMS_strain*10**6, label = quake)
            
            timeseries = [0.,300.]
            #plt.xlim(timeseries)
            timeseries = str(timeseries)
            
#            plt.xlabel('Time (s)')
#            plt.ylabel('RMS Microstrain ($10^{-6}$ m/m)')
#            plt.title(quake + ' Earthquake at PBO Station ' + sta)
#            plt.legend(loc = 1)
            
            RMS_st = BS1.copy()
            RMS_st[0].stats.channel = 'BSR'
            RMS_st[0].data = RMS_strain
            
            RMS_st.plot()
            #print(RMS_st[0].stats)
            
            RMS_st.write('/Users/sydneydybing/StrainProject/StrainData/Processed/RMS/' + quake + '/' + sta + '_RMS' + '.mseed', format='MSEED')
                
        except:
            
            print(quake + " no station " + sta)