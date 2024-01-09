#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 18:19:51 2020

@author: sydneydybing
"""

import pandas as pd
import matplotlib.pyplot as plt

eq_sta_distances = pd.read_csv('/Users/sydneydybing/StrainProject/evt-sta_dist_sel6500.csv')
#bad_eq_sta_distances = pd.read_csv('/Users/sydneydybing/IRIS_pbo_data/ID_useful_eq-sta_pairs.csv')
#print(eq_sta_distances)

dist = eq_sta_distances.r_hyp.values
mag = eq_sta_distances.mag.values
#bad_dist = bad_eq_sta_distances.distaz_m.values
#bad_mag = bad_eq_sta_distances.mag.values

plt.scatter(dist/1000, mag, s = 6, alpha = 0.9, color = 'C0')
#plt.scatter(bad_dist/1000, bad_mag, s = 6, alpha = 0.1, color = 'C1', label = 'Uncleaned')
plt.xlabel('Event-Station Distance (km)')
plt.ylabel('Earthquake Magnitude')
plt.title('Event-Station Distances for Strain Dataset')

#plt.show()
plt.savefig('/Users/sydneydybing/StrainProject/M6_500km_sel/Distance_vs_Mag.jpg', format="JPEG", dpi=400)