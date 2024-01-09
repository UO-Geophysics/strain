#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  8 12:39:56 2020

@author: sydneydybing
"""

from obspy.core import Stream, read
import numpy as np
import matplotlib.pyplot as plt

path_to_files = '/Users/sydneydybing/StrainProject/M6_500km_sel/StrainData_sel/Trimmed/'
quake_folders = np.genfromtxt('/Users/sydneydybing/StrainProject/M6_500km_sel/quake_folders_sel.txt', dtype=str)
stas = np.genfromtxt('/Users/sydneydybing/StrainProject/stations.txt', dtype=str)

quake_folders_test = ['59_2008_6.3']
stas_test = ['B017']

for quake in quake_folders:
    for sta in stas:        
            
        try:
        
            # Strain data
        
            tRMS = read(path_to_files + quake + '/' + sta + '_tRMS.mseed')
            
            #tRMS.plot()
            tRMS_data = tRMS[0].data
            
            tRMS_times = range(tRMS[0].stats.npts)
            tRMS_times = np.asarray(tRMS_times)/(tRMS[0].stats.sampling_rate)
            
            if quake == '59_2008_6.3':
                plt.plot(tRMS_times, tRMS_data*10**6, color = 'green', label = quake, alpha = 0.3)
            elif quake == '109_2010_6.5':
                plt.plot(tRMS_times, tRMS_data*10**6, color = 'orange', label = quake, alpha = 0.3)
            elif quake == '112_2010_7.2':
                plt.plot(tRMS_times, tRMS_data*10**6, color = 'black', label = quake, alpha = 0.3)
            elif quake == '145_2011_6.4':    
                plt.plot(tRMS_times, tRMS_data*10**6, color = 'yellow', label = quake, alpha = 0.3)
            elif quake == '152_2012_6.0':    
                plt.plot(tRMS_times, tRMS_data*10**6, color = 'purple', label = quake, alpha = 0.3)
            elif quake == '172_2012_6.1':    
                plt.plot(tRMS_times, tRMS_data*10**6, color = 'blue', label = quake, alpha = 0.3)
            else:
                plt.plot(tRMS_times, tRMS_data*10**6, color = 'red', label = quake, alpha = 0.3)
            
            plt.xlim(0,120)
            #plt.ylim(0,2.5)
            plt.xlabel('Time (s)')
            plt.ylabel('RMS Microstrain ($10^{-6}$ m/m)')
            
            plt.title(quake + ' Earthquake at PBO Station ' + sta)
            #plt.xlim(0,25)
            #plt.legend()
            
            #plt.show()
            
           
            #plt.close()
        
        except:
            
            print(quake + " no station " + sta)

plt.savefig('/Users/sydneydybing/StrainProject/M6_500km_sel/StrainData_sel/Trimmed/Trimmed_summary.jpg', format="JPEG", dpi=400)