#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 01:52:58 2020

@author: sydneydybing
"""

from obspy.core import read
import matplotlib.pyplot as plt
import numpy as np
from pymc3 import  *
import theano
import pandas as pd
from statsmodels.formula.api import glm as glm_sm
import statsmodels.api as sm
from pandas.plotting import scatter_matrix

path_to_file = '/Users/sydneydybing/StrainProject/M6_500km_sel/StrainData_sel/Trimmed/PeakStrains/Corrected/112_2010_7.2/B086_PSTc.mseed'
st = read(path_to_file)
st.plot()

data = st[0].data
times = st[0].times()
print(times)

plt.semilogy(times, data*10**6)
plt.xlim(0,120)
plt.xlabel('Times (s)')
plt.ylabel('Peak Microstrain')
plt.show()

# First growth section - ~60 samples

plt.semilogy(times, data*10**6)
plt.xlim(10.25,12.2)
plt.ylim(0.0008,0.015)
plt.show()

print(times[205])
print(times[244])

first_times = times[205:245]
print(first_times)
first_data = data[205:245]
print(first_data)

# Second growth section

plt.semilogy(times, data*10**6)
plt.xlim(12.2,64)
#plt.ylim(0.0008,0.015)
plt.show()

print(times[244])
print(times[1280])

second_times = times[244:1281]
print(second_times)
second_data = data[244:1281]
print(second_data)

# ##### Making a model for the first set

# data = {'x' : first_times, 'y' : first_data}

# with Model() as model:
#     GLM.from_formula('y ~ x', data)
#     trace = sample(2000, tune=2000, cores=1)

# #plt.figure(figsize=(5, 5))
# plt.plot(first_times, first_data)
# plot_posterior_predictive_glm(trace)