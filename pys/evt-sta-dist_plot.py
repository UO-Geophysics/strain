#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 18:19:51 2020

@author: sydneydybing
"""

import pandas as pd
import matplotlib.pyplot as plt

good_eq_sta_distances = pd.read_csv('/Users/sydneydybing/IRIS_pbo_data/evt-sta_distances_clean_pythag.csv')
bad_eq_sta_distances = pd.read_csv('/Users/sydneydybing/IRIS_pbo_data/ID_useful_eq-sta_pairs.csv')
#print(eq_sta_distances)

good_dist = good_eq_sta_distances.r_hyp.values
good_mag = good_eq_sta_distances.mag.values
bad_dist = bad_eq_sta_distances.distaz_m.values
bad_mag = bad_eq_sta_distances.mag.values

plt.scatter(good_dist/1000, good_mag, s = 6, alpha = 0.9, color = 'C0', label = 'Cleaned')
plt.scatter(bad_dist/1000, bad_mag, s = 6, alpha = 0.1, color = 'C1', label = 'Uncleaned')
plt.legend(loc = 1)
plt.xlabel('Event-Station Distance (km)')
plt.ylabel('Earthquake Magnitude')
plt.title('Event-Station Distances for Strain Dataset (uncleaned vs. cleaned with depth)')

plt.savefig('/Users/sydneydybing/IRIS_pbo_data/Event-Station Distances for Strain Dataset (uncleaned vs. cleaned).jpg', format="JPEG", dpi=400)