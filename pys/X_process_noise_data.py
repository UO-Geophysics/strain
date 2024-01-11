#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 11:28:40 2020

@author: sydneydybing
"""

from obspy.core import Stream, read
from scipy.interpolate import interp1d
import numpy as np
import matplotlib.pyplot as plt

path_to_files = '/Users/sydneydybing/IRIS_pbo_data/Data_noise/'
quake_folders = np.genfromtxt(path_to_files + 'quake_folders_sel4.txt', dtype=str)
stas = np.genfromtxt(path_to_files + 'stations_sel4.txt', dtype=str)
chans = ['BS1', 'BS2', 'BS3', 'BS4']

quake_folders_test = ['172_2012_6.2']
stas_test = ['B007']

bad_stachan = []

for quake in quake_folders_test:
    for sta in stas_test:
        for chan in chans:          
            
            g = Stream()
            
            try:
            
                g = read(path_to_files + quake + '/' + sta + '_' + chan + '.mseed')
                
                #g.plot()
                
                # Equations from Barbour and Crowell to convert to strain
                # R = ratio of the gap between the fixed-capacitance plates and instrument diameter (0.087 m)
                # Going to use 100 microns for gap for now (10**(-4) m)
                
                if (sta == 'B001') or (sta == 'B003') or (sta == 'B004') or (sta == 'B005') \
                    or (sta ==  'B006') or (sta == 'B007') or (sta == 'B009') or (sta == 'B010') \
                    or (sta == 'B011') or (sta == 'B012') or (sta == 'B018') or (sta == 'B022') \
                    or (sta == 'B024') or (sta == 'B035') or (sta == 'B081') or (sta == 'B082') \
                    or (sta == 'B086') or (sta == 'B087'):
                    
                    R = 2*10**(-4) / 0.087
                                    
                else:
                    
                    R = 10**(-4) / 0.087
                                
                C = 10**8
                
                # Calculating new linear extensional strains (turns from a Stream into a numpy array)
                
                e = R * (((g[0].data)/C)/(1 - (g[0].data)/C))
                
                times = range(g[0].stats.npts)
                times = np.asarray(times)/(g[0].stats.sampling_rate)
                                                     
                ## Fixing the data ##
                
                # Identifying stations with issues using derivatives
                
                # Taking the derivative of the timeseries
                
                deriv_e = np.diff(np.hstack((e[0],e)))
             
                deriv_e_min = np.min(deriv_e)
                deriv_e_max = np.max(deriv_e)
                deriv_e_avg = np.average(deriv_e)
                
                if deriv_e_min <= -0.00025 or deriv_e_max >= 0.00025: # better to do this with averages or #s?
                    
                    bad_label = quake + '_' + sta + '_' + chan 
                    bad_stachan.append(bad_label)
                    
                else:
                    pass
                
                if quake + '_' + sta + '_' + chan in bad_stachan:
                    
                    # Finding the value of the messed up samples
                    
                    data_min = np.amin(e)
                    
                    # Finding the indices of the messed up samples
                    
                    i = np.where(e <= data_min)[0]
                    
                    num_bad = i.shape[0]
                    
                    print("Bad station & channel - event " + quake + ': ' + sta + '_' + chan + '. ' + str(num_bad) + ' bad samples')
                    
                    # Deleting the bad samples from the data and the times arrays
                    
                    e_clean = np.delete(e, i)
                    times_clean = np.delete(times, i)
                                    
                    # Now fill in the gaps with the linear interpolation
                    
                    f = interp1d(times_clean, e_clean)
                    e_fill = f(times)
                    e = e_fill
                    
                else: 
                    print("Good station & channel - event " + quake + ': ' + sta + '_' + chan)
                    
                # Normalizing unfiltered data
                
                norm_value = e[0]
                data_length = e.shape
                normalize = np.full(data_length, norm_value)
                
                e_norm = np.subtract(e, normalize)
                
                # Plotting normalized fixed data
                
                plt.plot(times, e_norm*10**6)
                plt.xlim(0.,60.)
                plt.ylim()
                plt.xlabel('Time (s) from Earthquake Origin')
                plt.ylabel('Microstrain ($10^{-6}$ m/m)')
                plt.title(quake + ' Earthquake at PBO Station ' + sta + '_' + chan)

                e_fixed = g.copy()
                #g.plot()
                e_fixed[0].data = e_norm
                #e_fixed.plot()
                #e_fixed.write(path_to_files + 'Processed/' + quake + '/' + sta + '_' + chan + '.mseed', format='MSEED')
    
            except: 
            
                print(quake + " no station " + sta)                        

print(bad_stachan)