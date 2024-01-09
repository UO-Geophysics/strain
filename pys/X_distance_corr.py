 #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 18 13:48:43 2020

@author: sydneydybing
"""
from obspy.core import read
import numpy as np
import pandas as pd

path_to_files = '/Users/sydneydybing/StrainProject/M6_500km_sel/StrainData_sel/Trimmed/PeakStrains/'
quake_folders = np.genfromtxt('/Users/sydneydybing/StrainProject/M6_500km_sel/StrainData_sel/Trimmed/PeakStrains/grp1_folders.txt', dtype=str)
stas = np.genfromtxt('/Users/sydneydybing/StrainProject/stations.txt', dtype=str)

earthquakes = pd.read_csv(path_to_files + 'grp1_corr.csv')
print(earthquakes)

earthquakes = earthquakes.to_numpy()
print(earthquakes)

xref = 150

for k_eq in range(len(earthquakes)):
    
    print('-------NEW LOOP-------')
    
    dist_m = earthquakes[k_eq, 8]
    sta = earthquakes[k_eq, 5]
    eqnum = int(earthquakes[k_eq, 0])
    year = int(earthquakes[k_eq, 1])
    mag = earthquakes[k_eq, 2]
    
    quake = str(eqnum) + '_' + str(year) + '_' + str(mag)
    print(quake)
    
    print(sta)
    #print(dist_m)
    dist_km = dist_m / 1000
    #print(dist_km)
    
    PST = read(path_to_files + quake + '/' + sta + '_PST.mseed')
    PST_data = PST[0].data
    #print(PST_data)
    
    correction = dist_km/xref
    correction = np.expand_dims(correction, 1)
    correction = np.tile(correction, PST_data.shape[0])
    correction = correction**1 # R vs R^2
    
    #Apply correction
    PST_corr = PST_data * correction
    print(PST_corr)
    
    PSTc = PST.copy()
    PSTc.write('/Users/sydneydybing/StrainProject/M6_500km_sel/StrainData_sel/Trimmed/PeakStrains/Corrected/' + quake + '/' + sta + '_PSTc' + '.mseed', format='MSEED')