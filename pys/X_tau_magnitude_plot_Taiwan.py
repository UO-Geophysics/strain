#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 03:03:35 2020

@author: sydneydybing
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

path_to_files = '/Users/sydneydybing/StrainProject/Taiwan/Trimmed/Aligned/PST/MCMC_xinter/'
dist = pd.read_csv('/Users/sydneydybing/StrainProject/Taiwan/evt-sta_dist.csv')

dist = dist.to_numpy()

# file = path_to_files + '1/MCMC_xinter/B916_xinter2.npz'
# xinter_1_916 = np.load(file) 

# print(xinter_1_916['xinter'])

tau_list = []

stas_chans = ['CHMB.EV', 'DONB.EV', 'FBRB.EV', 'HGSB.EV', 'SJNB.EV', 'SSTB.EV', 'ZANB.EV', 'SSNB.EV', 'SSNB.G1', 'SSNB.G2', 'TRKB.EV', 'TRKB.G1', 'TRKB.G2']
    
for sta_chan in stas_chans:
    
    file = path_to_files + sta_chan+ '_xinter.npz'
    xinter = np.load(file)
    xinter_array = xinter['xinter']
    
    print('Station: ' + sta_chan)
    print(xinter_array)
    
    start = 9.9
    
    mean_xinter = np.mean(xinter_array)
    
    print('xinter mean: ' + str(mean_xinter))
    
    tau = mean_xinter - start
    
    print('tau: ' + str(tau))
    
    tau_list.append(tau)
    
    print(tau_list)
    
    mag = 6.3
      
    print('-------')

distances = pd.read_csv('/Users/sydneydybing/StrainProject/Taiwan/evt-sta_dist.csv')

tau_array = np.asarray(tau_list)
dist = distances.dist_km.values

print(tau_array.shape)
print(dist.shape)

plt.scatter(dist,tau_array,label='M6.3')
plt.xlabel('Hypocentral Distance (km)')
plt.ylabel('Tau (s)')
plt.legend()
plt.title('Taiwan Tau-Distance')

plt.savefig('Taiwan_tauplot.jpg', format='JPEG', dpi=400)


