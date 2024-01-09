#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 15:18:04 2020

@author: sydneydybing
"""
from obspy.core import read
import numpy as np
import matplotlib.pyplot as plt

raw_data_files = '/Users/sydneydybing/StrainProject/StrainData/Processed/109_2010_6.5/'
RMS_data_files = '/Users/sydneydybing/StrainProject/M6_500km_sel/StrainData_sel/Trimmed/109_2010_6.5/'
PST_data_files = '/Users/sydneydybing/StrainProject/M6_500km_sel/StrainData_sel/Trimmed/PeakStrains/109_2010_6.5/'

raw_BS1 = read(raw_data_files + 'B033_BS1.mseed')
raw_data_BS1 = raw_BS1[0].data

raw_BS2 = read(raw_data_files + 'B033_BS2.mseed')
raw_data_BS2 = raw_BS2[0].data

raw_BS3 = read(raw_data_files + 'B033_BS3.mseed')
raw_data_BS3 = raw_BS3[0].data

raw_BS4 = read(raw_data_files + 'B033_BS4.mseed')
raw_data_BS4 = raw_BS4[0].data

raw_times = raw_BS1[0].times()

RMS = read(RMS_data_files + 'B033_tRMS.mseed')
RMS_data = RMS[0].data
RMS_times = RMS[0].times()

PST = read(PST_data_files + 'B033_PST.mseed')
PST_data = PST[0].data
PST_times = PST[0].times()

# # BS1

# plt.plot(raw_times,raw_data_BS1*10**6)
# plt.title('M6.5, station B033, channel BS1')
# plt.xlim(0,250)
# plt.ylabel('Microstrain ($10^{-6}$ m/m)')
# plt.xlabel('Time (s)')
# plt.savefig('/Users/sydneydybing/Documents/AGU_Presentation/Figures/rawdata_BS1.jpg', format="JPEG", dpi=400)
# plt.close()

# # BS2

# plt.plot(raw_times,raw_data_BS2*10**6)
# plt.title('M6.5, station B033, channel BS2')
# plt.xlim(0,250)
# plt.ylabel('Microstrain ($10^{-6}$ m/m)')
# plt.xlabel('Time (s)')
# plt.savefig('/Users/sydneydybing/Documents/AGU_Presentation/Figures/rawdata_BS2.jpg', format="JPEG", dpi=400)
# plt.close()

# # BS3

# plt.plot(raw_times,raw_data_BS3*10**6)
# plt.title('M6.5, station B033, channel BS3')
# plt.xlim(0,250)
# plt.ylabel('Microstrain ($10^{-6}$ m/m)')
# plt.xlabel('Time (s)')
# plt.savefig('/Users/sydneydybing/Documents/AGU_Presentation/Figures/rawdata_BS3.jpg', format="JPEG", dpi=400)
# plt.close()

# # BS4

# plt.plot(raw_times,raw_data_BS4*10**6)
# plt.title('M6.5, station B033, channel BS4')
# plt.xlim(0,250)
# plt.ylabel('Microstrain ($10^{-6}$ m/m)')
# plt.xlabel('Time (s)')
# plt.savefig('/Users/sydneydybing/Documents/AGU_Presentation/Figures/rawdata_BS4.jpg', format="JPEG", dpi=400)
# plt.close()

# # RMS

# plt.plot(RMS_times,RMS_data*10**6)
# plt.title('M6.5, station B033, RMS')
# plt.xlim(0,250)
# plt.ylabel('RMS Microstrain ($10^{-6}$ m/m)')
# plt.xlabel('Time (s)')
# plt.savefig('/Users/sydneydybing/Documents/AGU_Presentation/Figures/RMS_data.jpg', format="JPEG", dpi=400)
# plt.close()

# # PST

# plt.plot(PST_times,PST_data*10**6)
# plt.title('M6.5, station B033, RMS')
# plt.xlim(0,250)
# plt.ylabel('Peak RMS Microstrain ($10^{-6}$ m/m)')
# plt.xlabel('Time (s)')
# plt.savefig('/Users/sydneydybing/Documents/AGU_Presentation/Figures/PST_data.jpg', format="JPEG", dpi=400)
# plt.close()

# RMS and PST

fig = plt.figure(1, figsize=(6,4),dpi=300)
plt.plot(RMS_times,RMS_data*10**6, label='RMS strain')
plt.plot(PST_times,PST_data*10**6, label='Peak strain')
plt.title('M6.5, station B033, RMS Strain + Peak Strain')
# plt.xlim(0,250)
plt.xlim(5,35)
plt.ylim(-0.01,0.11)
plt.ylabel('Peak RMS Microstrain ($10^{-6}$ m/m)')
plt.xlabel('Time (s)')
plt.legend(loc = 2, fontsize = 12)

plt.savefig('/Users/sydneydybing/Documents/Comps/Figures/RMS_and_PST_zoom.png', format = 'PNG')
plt.close()







