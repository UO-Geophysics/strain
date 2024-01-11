#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 22 01:09:23 2020

@author: sydneydybing
"""
from obspy.core import read
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

apref = -6.407
bpref = 0.385

##### Ridgecrest #####

Rcrest = pd.read_csv('/Users/sydneydybing/StrainProject/Ridgecrest/rcrest_quakes_Mo.csv')

Rcrest_Mo = Rcrest.Mo.values
print(Rcrest_Mo)

Rcrest_S_list = []
Rcrest_S_mags_list = [6.4, 5.36, 7.1, 5.5, 5.44, 5.53]

for Mo in Rcrest_Mo:
    
    logS = apref + bpref * np.log10(Mo)
    #print(logS)
    
    S = 10**logS
    Rcrest_S = S
    
    print(Rcrest_S)
    
    Rcrest_S_list.append(Rcrest_S)

print(Rcrest_S_list)
print('-------------')

##### Barbour #####

Barbour = pd.read_csv('/Users/sydneydybing/StrainProject/Barbour_quakes_Mo.csv')

Barbour_Mo = Barbour.Mo.values
print(Barbour_Mo)

Barbour_S_list = []
Barbour_S_mags_list = [6.3, 6.5, 7.2, 6.4, 6.0, 6.1, 6.8]

for Mo in Barbour_Mo:
    
    logS = apref + bpref * np.log10(Mo)
    #print(logS)
    
    S = 10**logS
    Barbour_S = S
    
    print(Barbour_S)
    
    Barbour_S_list.append(Barbour_S)

print(Barbour_S_list)
    
print('-------------')

##### Taiwan #####

Taiwan_Mo = 2.195*10**18
Taiwan_S_list = []
Taiwan_S_mags_list = [6.2]

Taiwan_logS = apref + bpref * np.log10(Taiwan_Mo)
#print(logS)

Taiwan_S = 10**Taiwan_logS

print(Taiwan_S)
Taiwan_S_list.append(Taiwan_S)

print(Taiwan_S_list)

print('-------------')

Rcrest_S_array = np.asarray(Rcrest_S_list)
Rcrest_S_mags_array = np.asarray(Rcrest_S_mags_list)

Barbour_S_array = np.asarray(Barbour_S_list)
Barbour_S_mags_array = np.asarray(Barbour_S_mags_list)

Taiwan_S_array = np.asarray(Taiwan_S_list)
Taiwan_S_mags_array = np.asarray(Taiwan_S_mags_list)

plt.scatter(Rcrest_S_mags_array, Rcrest_S_array)
plt.scatter(Barbour_S_mags_array, Barbour_S_array)
plt.scatter(Taiwan_S_mags_array, Taiwan_S_array)
    