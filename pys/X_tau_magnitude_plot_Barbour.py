#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 03:36:03 2020

@author: sydneydybing
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

B_path_to_files = '/Users/sydneydybing/StrainProject/M6_500km_sel/StrainData_sel/Trimmed/PeakStrains/'
B_quake_folders = np.genfromtxt('/Users/sydneydybing/StrainProject/M6_500km_sel/quake_folders_sel.txt', dtype=str)
B_stas = np.genfromtxt('/Users/sydneydybing/StrainProject/stations.txt', dtype=str)
B_dist = pd.read_csv('/Users/sydneydybing/StrainProject/Barbour_sel_dists.csv')

B_dist = B_dist.to_numpy()

# file = path_to_files + '1/MCMC_xinter/B916_xinter2.npz'
# xinter_1_916 = np.load(file) 

# print(xinter_1_916['xinter'])

B_tau_list = []

for B_quake in B_quake_folders:
    
    for B_sta in B_stas:
        
        try:
        
            B_file = B_path_to_files + B_quake + '/MCMC_xinter/' + B_sta + '_xinter.npz'
            B_xinter = np.load(B_file)
            B_xinter_array = B_xinter['xinter']
            
            print('-------')
            print('Quake: ' + B_quake)
            print('Station: ' + B_sta)
            # print(B_xinter_array)
            
            if (B_quake == '59_2008_6.3'):
                start = 0
                
            elif (B_quake == '109_2010_6.5'):
                if (B_sta == 'B933') or (B_sta == 'B934') or (B_sta == 'B935') or (B_sta == 'B035') or (B_sta == 'B036'):
                    start = 10.1
                else:
                    start = 10
                
            elif (B_quake == '112_2010_7.2'):
                if (B_sta == 'B916') or (B_sta == 'B917') or (B_sta == 'B918') or (B_sta == 'B921'):
                    start = 9.8
                else:
                    start = 10.1
                    
            else:
                start = 10
            
            B_mean_xinter = np.mean(B_xinter_array)
            
            # print('xinter mean: ' + str(B_mean_xinter))
            
            B_tau = B_mean_xinter - start
            
            print('tau: ' + str(B_tau))
            
            B_tau_list.append(B_tau)
            
            # print(B_tau_list)
            
            if (B_quake == '59_2008_6.3'):
                mag = 6.3
                
            elif (B_quake == '109_2010_6.5'):
                mag = 6.5
                
            elif (B_quake == '112_2010_7.2'):
                mag = 7.2
                
            elif (B_quake == '152_2012_6.0'):
                mag = 6.0
                
            elif (B_quake == '172_2012_6.1'):
                mag = 6.1
                
            elif (B_quake == '185_2014_6.8'):
                mag = 6.8
            
            # print('mag: ' + str(mag))
            
            print('-------')

        except:
            pass

B_dist = pd.read_csv('/Users/sydneydybing/StrainProject/Barbour_sel_dists.csv')

B_tau_array = np.asarray(B_tau_list)
B_dist = B_dist.dist_km.values

print(B_tau_array.shape)
print(B_dist.shape)

plt.scatter(B_dist[18:28],B_tau_array[18:28],label='M7.2',color='maroon')
plt.scatter(B_dist[68:83],B_tau_array[68:83],label='M6.8',color='firebrick')
plt.scatter(B_dist[5:17],B_tau_array[5:17],label='M6.5',color='red')
plt.scatter(B_dist[0:4],B_tau_array[0:4],label='M6.3',color='coral')
plt.scatter(B_dist[48:67],B_tau_array[48:67],label='M6.1',color='lightsalmon')
plt.scatter(B_dist[29:47],B_tau_array[29:47],label='M6.0',color='peachpuff')

plt.xlabel('Hypocentral Distance (km)')
plt.ylabel('Tau (s)')
plt.legend()
plt.title('Barbour Tau-Distance')

plt.savefig('Barbour_tauplot_nooutlier.jpg', format='JPEG', dpi=400)



