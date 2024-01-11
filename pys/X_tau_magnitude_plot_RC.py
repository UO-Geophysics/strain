#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 00:06:26 2020

@author: sydneydybing
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

path_to_files = '/Users/sydneydybing/StrainProject/Ridgecrest/StrainData/Processed/RMS/Trimmed/PST/'
quake_folders = ['1', '2', '3', '4', '5', '6']
stas = ['B916', 'B917', 'B921']
dist = pd.read_csv('/Users/sydneydybing/StrainProject/Ridgecrest/evt-sta_dist.csv')

dist = dist.to_numpy()

# file = path_to_files + '1/MCMC_xinter/B916_xinter2.npz'
# xinter_1_916 = np.load(file) 

# print(xinter_1_916['xinter'])

tau_list = []

for quake in quake_folders:
    
    for sta in stas:
        
        file = path_to_files + quake + '/MCMC_xinter/' + sta + '_xinter.npz'
        xinter = np.load(file)
        xinter_array = xinter['xinter']
        
        print('Quake: ' + quake)
        print('Station: ' + sta)
        print(xinter_array)
        
        if (quake == '1') or (quake == '2') or (quake == '5') or (quake == '6'):
            start = 10
        elif quake == '3':
            start = 10.2
        else:
            start = 10.1
        
        mean_xinter = np.mean(xinter_array)
        
        print('xinter mean: ' + str(mean_xinter))
        
        tau = mean_xinter - start
        
        print('tau: ' + str(tau))
        
        tau_list.append(tau)
        
        print(tau_list)
        
        if (quake == '1'):
            mag = 6.4
        elif (quake == '2'):
            mag = 5.36
        elif (quake == '3'):
            mag = 7.1
        elif (quake == '4'):
            mag = 5.5
        elif quake == '5':
            mag = 5.44
        else:
            mag = 5.53
        
        print('mag: ' + str(mag))
        
        print('-------')

tau_plot = pd.read_csv('/Users/sydneydybing/StrainProject/Ridgecrest/tau_plot.csv', encoding="utf-8-sig")

tau_array = np.asarray(tau_list)
dist = tau_plot.dist.values

print(tau_array.shape)
print(dist.shape)

plt.scatter(dist[6:8],tau_array[6:8],label='M7.1',color='maroon')
plt.scatter(dist[0:2],tau_array[0:2],label='M6.4',color='firebrick')
plt.scatter(dist[15:17],tau_array[15:17],label='M5.5',color='red')
plt.scatter(dist[9:11],tau_array[9:11],label='M5.5',color='coral')
plt.scatter(dist[12:14],tau_array[12:14],label='M5.4',color='lightsalmon')
plt.scatter(dist[3:5],tau_array[3:5],label='M5.4',color='peachpuff')
plt.xlabel('Hypocentral Distance (km)')
plt.ylabel('Tau (s)')
plt.legend(loc=2)
plt.title('Ridgecrest Tau-Distance')

plt.savefig('RC_tauplot.jpg', format='JPEG', dpi=400)




