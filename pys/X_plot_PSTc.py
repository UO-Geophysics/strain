#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 18 14:53:46 2020

@author: sydneydybing
"""

from obspy.core import read
import numpy as np
import matplotlib.pyplot as plt

path_to_files = '/Users/sydneydybing/StrainProject/M6_500km_sel/StrainData_sel/Trimmed/PeakStrains/Corrected/'
quake_folders = np.genfromtxt('/Users/sydneydybing/StrainProject/M6_500km_sel/StrainData_sel/Trimmed/PeakStrains/grp1_folders.txt', dtype=str)
stas = np.genfromtxt('/Users/sydneydybing/StrainProject/stations.txt', dtype=str)

quake_folders_test = ['145_2011_6.4']
stas_test = ['B928']

for quake in quake_folders:
    for sta in stas:        
            
        try:
        
            # Strain data
        
            PSTc = read(path_to_files + quake + '/' + sta + '_PSTc.mseed')
            
            #tRMS.plot()
            PSTc_data = PSTc[0].data
            
            PSTc_times = range(PSTc[0].stats.npts)
            PSTc_times = np.asarray(PSTc_times)/(PSTc[0].stats.sampling_rate)
            
            if quake == '109_2010_6.5':
                plt.semilogy(PSTc_times, PSTc_data*10**6, color = 'green', label = quake)
            elif quake == '112_2010_7.2':
                plt.semilogy(PSTc_times, PSTc_data*10**6, color = 'red', label = quake)
            elif quake == '145_2011_6.4':    
                plt.semilogy(PSTc_times, PSTc_data*10**6, color = 'blue', label = quake)
            else:
                plt.semilogy(PSTc_times, PSTc_data*10**6, color = 'orange', label = quake)
    #            
               
#            plt.plot(PSTc_times, PSTc_data*10**6, label = sta)
            
#            if quake == '145_2011_6.4':    
#                plt.plot(PSTc_times, PSTc_data*10**6, label = sta)
#            else:
#                pass
            
            plt.xlim(0,120)
            plt.ylim(0,25)
            plt.xlabel('Time (s) (p-wave arrivals at 10s)')
            plt.ylabel('Peak RMS Microstrain ($10^{-6}$ m/m)')
            
            plt.title('Peak Strain over Time (Selected Barbour Data)')
            #plt.xlim(0,25)
            #plt.legend()
            
            #plt.show()
            
           
                #plt.close()
        
        except:
            
            print(quake + " no station " + sta)

plt.show()

#plt.savefig('/Users/sydneydybing/StrainProject/M6_500km_sel/StrainData_sel/Trimmed/PeakStrains/PeakStrains_semilog.jpg', format="JPEG", dpi=400)