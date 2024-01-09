#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 22 14:42:32 2020

@author: sydneydybing
"""

from obspy.core import read
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd

path_to_files = '/Users/sydneydybing/StrainProject/M6_500km_sel/StrainData_sel/Trimmed/PeakStrains/'
quake_folders = np.genfromtxt('/Users/sydneydybing/StrainProject/M6_500km_sel/quake_folders_sel.txt', dtype=str)
stas = np.genfromtxt('/Users/sydneydybing/StrainProject/stations.txt', dtype=str)

quake_folders_test = ['145_2011_6.4']
stas_test = ['B933', 'B934']

font = {'family' : 'sans-serif',
        'weight' : 'regular',
        'size'   : 16}

mpl.rc('font', **font)

# Load my uncorrected peak strain data

fig = plt.figure(figsize = (8,8))

for quake in quake_folders:
    for sta in stas:        
            
        try:
        
            # Strain data
        
            PST = read(path_to_files + quake + '/' + sta + '_PST.mseed')
            
            #tRMS.plot()
            PST_data = PST[0].data
            
            PST_times = range(PST[0].stats.npts)
            PST_times = np.asarray(PST_times)/(PST[0].stats.sampling_rate)
            
            #print(PST_data)
            peak_strain = np.amax(PST_data)
            #print(peak_strain)
            print(str(peak_strain) + ' at station ' + str(sta) + ' for earthquake ' + str(quake))
            peak_strain_index = np.where(PST_data == peak_strain)
            index = peak_strain_index[0][0]
            #print(index)
            
            #print(len(PST_data))
            #print(len(PST_times))
            
            peak_strain_time = PST_times[index]
            #print(peak_strain_time)
            
            mag = quake[-3:]
            
            #plt.xlim(0,20)
            #plt.ylim(0,1.2)
            plt.xlabel('Magnitude (Mw)')
            plt.ylabel('Peak RMS Microstrain ($10^{-6}$ m/m)')
            
            
            ax = plt.gca()
#            mine = ax.scatter(mag, peak_strain*10**6, color = 'gray', label = sta, alpha = 0.5)
            mine = ax.scatter(mag, peak_strain, color = 'gray', label = sta, alpha = 0.5)
            ax.set_yscale('log')
            
            #plt.title(quake + ' Earthquake at PBO Station ' + sta)
            #plt.xlim(0,25)
            #plt.legend()
            
            #plt.show()
            
           
            #plt.close()
        
        except:
            pass
            #print(quake + " no station " + sta)

# Load Andy's peak strain data

AB_data = pd.read_csv('/Users/sydneydybing/StrainProject/Andy_peak_strains_sel.csv', dtype = str)
#print(AB_data)

AB_peak_strain_logs = AB_data.logE.values
AB_stas = AB_data.Station.values
AB_quakes = AB_data.Earthquake.values
AB_mags = AB_data.Mw.values

for idx in range(len(AB_data)):
    
    AB_quake = AB_quakes[idx]
    #print(AB_quake)
    AB_sta = AB_stas[idx]
    #print(AB_sta)

    AB_peak_strain_log = float(AB_peak_strain_logs[idx])
    #print(AB_peak_strain_log)
    
    AB_peak_strain = 10**AB_peak_strain_log
    print(str(AB_peak_strain) + ' at station ' + str(AB_sta) + ' for earthquake ' + str(AB_quake))
    
#    AB_peak_strain = np.exp(AB_peak_strain_log)

    AB_mag = AB_mags[idx]
    #print(AB_mag)
    
#    andys = ax.scatter(AB_mag, AB_peak_strain*10**6, marker = 'x', color = 'black')
    andys = ax.scatter(AB_mag, AB_peak_strain, marker = 'x', color = 'black')

plt.legend((mine, andys), ('Dybing', 'Barbour'), loc = 4)
plt.ylim(10**(-10),10**(-4))
plt.show()

#plt.savefig('/Users/sydneydybing/StrainProject/M6_500km_sel/StrainData_sel/Trimmed/PeakStrains/Compare_peak_strains.jpg', format="JPEG", dpi=400)