#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 17:22:37 2020

@author: sydneydybing
"""
import numpy as np
from obspy.clients.iris import Client
import os
import pandas as pd

client = Client()

earthquakes = pd.read_csv('/Users/sydneydybing/StrainProject/earthquakes.csv')
sta_loc = pd.read_csv('/Users/sydneydybing/StrainProject/stations_latlong.csv')

earthquakes = earthquakes.to_numpy()
sta_loc = sta_loc.to_numpy()

f = open('/Users/sydneydybing/StrainProject/evt-sta_dist.csv', 'w')
#header = ('eqnum', 'year', 'mag', 'eq_lat', 'eq_lon', 'sta_name', 'sta_lat', 'sta_lon', 'distaz_m')
#f.write('eqnum', 'year', 'mag', 'eq_lat', 'eq_lon', 'sta_name', 'sta_lat', 'sta_lon', 'distaz_m')

for k_eq in range(len(earthquakes)):
    
    eqnum = int(earthquakes[k_eq, 0])
    year = int(earthquakes[k_eq, 1])
    mag = earthquakes[k_eq, 10]
    eq_lat = earthquakes[k_eq, 7]
    eq_lon = earthquakes[k_eq, 8]
    depth = earthquakes[k_eq, 9]
    
    for k_sta in range(len(sta_loc)):
        
        sta_name = sta_loc[k_sta, 0]
        sta_lat = sta_loc[k_sta, 1]
        sta_lon = sta_loc[k_sta, 2]
        
        # Only want to calculate distances for events/stations that actually have data

        data_exists = os.path.isdir('/Users/sydneydybing/StrainProject/StrainData/' + str(eqnum) + '_' + str(year) + '_' + str(mag))
        
        if data_exists:
            
            station_exists = os.path.isfile('/Users/sydneydybing/StrainProject/StrainData/' + str(eqnum) + '_' + str(year) + '_' + str(mag) + '/' + str(sta_name) + '_BS1.mseed')
            
            if station_exists:
                
                distaz = client.distaz(sta_lat, sta_lon, eq_lat, eq_lon)
                r_epi = distaz['distancemeters']
                r_hyp = np.sqrt(r_epi**2 + depth**2)
                
                line = '%d\t%d\t%.1f\t%.2f\t%.2f\t%s\t%.6f\t%.6f\t%.6f\n'%(eqnum,year,mag,eq_lat,eq_lon,sta_name,sta_lat,sta_lon,r_hyp)
                #print(line)
                f.write(line)
                
            else:
                print(str(eqnum) + '_' + str(year) + '_' + str(mag) + ' station ' + str(sta_name) + ' does not exist')
            
        else:
            print(str(eqnum) + '_' + str(year) + '_' + str(mag) + ' data does not exist')
    
f.close()
