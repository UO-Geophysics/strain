#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 15:14:13 2020

@author: seansantellanes
"""

from pandas import read_csv
from numpy import array,arange
import numpy as np

from matplotlib import pyplot as plt
import scipy.integrate as integrate

import datetime
import pandas as pd
import warnings
warnings.simplefilter('ignore',UserWarning)
from scipy.interpolate import interp1d
from scipy.interpolate import InterpolatedUnivariateSpline
from multitaper import MTSpec
from obspy.signal import PPSD
from obspy import Stream,Trace
from mudpy.forward import highpass
from mudpy.forward import lowpass
import logging
from random import gauss
plt.close("all")
def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)
def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth
#from mudpy.forward import lowpass
#region='South_Am'
station='46407'
depth=3300
#date='2019_2021'
#regionDir=region+'/csv/'
##path1=regionDir+station+'_'+date+'_'
#path2=region+'/'+station+'/'+date+'/biweekly/figures/'
#filename=path1+'biweekly_slope_intercept.csv'
logging.basicConfig(filename=f'LOG/ppsd_{station}.log',encoding='utf-8',level=logging.INFO,filemode='w',force=True)
fcorner=[1./(3600*2),1./(70)]
#x_array=[]
#y_array=[]
#z_array=[]
start_date = datetime.date(2010, 1, 1)
infragravity_wave_list=[]
day_list=[]
end_date = datetime.date(2022, 4, 30)
#tsu_df=pd.read_csv('tsunami_database_pacific.csv')
#tsunami=tsu_df['Tsunamis']
#tsunami=pd.to_datetime(tsunami)
#tsunami=list(tsunami.dt.date)
#date_ls=[]
#date_tsu=[]
counter=0
# if os.path.exists(filename):
#     os.remove(filename)
# else:
#     print('cannot delete file as it does not exist')
# if os.path.exists(path2):
#     shutil.rmtree(path2)
    
# else:
#     print('This directory did not exist!')
# os.makedirs(path2)
# if os.path.exists(regionDir):
#     pass
# else:
#     print('Making directory:',regionDir)
#     os.makedirs(regionDir)
startTime = datetime.datetime.now()
#weekStart=datetime.datetime.strptime(str(sys.argv[1]),'%Y-%m-%d').date()
#weekStart=datetime.datetime.strptime('2009-01-01','%Y-%m-%d').date()
weekStart=start_date
df=read_csv(station+'/pressure_res_long.csv',parse_dates=['Time'],index_col=['Time'])
flag=0
while start_date < end_date:
    dayItr=datetime.timedelta(days=1)
    nextday=start_date+dayItr
    dayStartStr=str(start_date)
    nextDayStr=str(nextday)
    #print(single_date)
    #print((dayStartStr), (nextDayStr))
    
    try:
        
        #df2=df[dayStartStr:nextDayStr]
        df2=df.loc[dayStartStr]
    except AssertionError:
        start_date=start_date+dayItr
        continue
    #print('Made it through slice.')
    time_epi = np.datetime64(weekStart)
    #Check for empty dataframe
    if df2.empty == True:
        #print('This beh emteh!!!')
        start_date=start_date+dayItr
        continue
    #Check for null values in the dataframe
    if df2.isnull().values.any() == False:
        pass
    #Move on to next dataframe if this one has nulls
    else:
        #print('Oh, crap!')
        dt=0 
        start_date=start_date+dayItr
        continue
    #Check for any sets of mismatching dts in the two week period
    try:
        dtls = []
        for j in range(1,df2.index.size):
            dt = df2.index.values[j]-df2.index.values[j-1]
            dtls.append(dt)
        dtset = set(dtls)
        if len(dtset) == 1:
            seconds = dt / np.timedelta64(1, 's')
            #print(seconds)
        elif len(dtset) > 1:
            dt = min(dtset)
            seconds = dt / np.timedelta64(1, 's')
            start_date=start_date+dayItr
            continue
    except IndexError as e:
        print(e)
        print('Ope!')
        dt=0 
        start_date=start_date+dayItr
        continue
    dt=int(seconds) #seconds
    pressure=array(df2['Pressure [dbar]'])
    #Check to see if Hi-Res before proceeding
    # if start_date in tsunami:
    #     #print(f'Tsunami at {start_date}, skipping 14 days')
    #     dayItr=datetime.timedelta(days=13)
    #     start_date=start_date+dayItr
    #     continue
    if dt > 15:
        print('Not Hi-Res')
        start_date=start_date+dayItr
        continue
    else:
        flag+=1
        #print('Hi-Res. Proceeding...')
    #slice out fall season
    
    time=arange(0,len(pressure)*dt,dt)
    t=np.zeros(len(time))
    if len(dtset) > 1:
        #print('Hope this interpolates')
        for k in range(len(time)):
            t[k]=((df2.index.values[k])-time_epi)/np.timedelta64(1, 's')
        #print(t[0], t[-1])
        t_in=arange(t[0],t[-1],15)
        f=interp1d(t,pressure)
        data_in=f(t_in)
        #data_smooth=smooth(data_in,30)
        pressure=data_in-np.mean(data_in)
        dt=t_in[2]-t_in[1]
    else:
        pass
    
    #Apply corection factors, first convert from dBar to Pa
    pressure*=1e4
    
    #nowd ivide by rho*g with rho=1037kg/m^3 and g=9.8m/s/s 
    sea_surface_height = pressure / (1037*9.8)
    
    #demean before spectra
    sea_surface_height -= sea_surface_height.mean()
    psd= MTSpec(
        sea_surface_height,nw=3.5,
        kspec=5, dt=dt)
    f=psd.freq
    k=(2*np.pi*f)/np.sqrt(9.81*depth)
    M=(1037*9.81)/np.cosh(k*depth)
    E=M**2*psd.sk
    
    try:
        x_1=f[144]
        x_2=f[1977]
    except IndexError:
        start_date=start_date+dayItr
        continue
    
    dx=(f[1977]-f[144])/len(f[144:1977])
    #H_integrate=integrate.quad(E,8.3e-4,1.1e-2)
    H_integrate=np.trapz(E[144:1977],dx=dx[0])
    H_ig=4*np.sqrt(H_integrate.sum())
    
    if H_ig > 0.:
        infragravity_wave_list.append(H_ig)
        day_list.append(start_date)
    st=Stream(Trace())
    st[0].data=sea_surface_height
    st[0].stats.delta=15
    st[0].stats.starttime=start_date
    #print(st)
    #st[0].stats.endtime=weekStart+datetime.timedelta(days=14)
    paz = {'gain': 1,'poles': [1],'sensitivity': 1,'zeros': [0j, 0j]}
    if flag==1:
        ppsd=PPSD(st[0].stats,paz,db_bins=(-80,-20,0.5),period_limits=[30,3600*2],ppsd_length=3600*24,overlap=0.5,special_handling='ringlaser')
        
    elif flag >= 1:
        if flag%10==0:
            #series=np.array([gauss(0,0.0001) for i in range(len(sea_surface_height))])
            #st[0].data+=series
            ppsd.add(st)
        else:
            ppsd.add(st)
    if len(ppsd.psd_values) > 0:
        #print("Accessing ppsd values")
        
        min_psd=np.min(ppsd.psd_values[-1])
        if min_psd < -55.:
            logging.info(f'{start_date} idx {len(ppsd.psd_values)-1} at flag={flag} in bottom branch.')

            if str(start_date) == '2021-12-24':
                ssh_fil=lowpass(sea_surface_height,fcorner,1/15,2,zerophase=True)
                print(np.max(ssh_fil))
                plt.plot(ssh_fil,label=f'{start_date} low branch')
                #plt.xlim([2000,2500])
                plt.legend()
                plt.savefig(f'time_series_png/{start_date}_{station}_bottom_branch.pdf')
         
            else:
                pass
        elif min_psd >= -55.:
            logging.info(f'{start_date} idx {len(ppsd.psd_values)-1} at flag={flag} in top branch.')
        #    pass
            if str(start_date) == '2021-12-24':
                print(len(ppsd.psd_values)-1)
                #ssh_fil=lowpass(sea_surface_height,fcorner,1/15,2,zerophase=True)
                ssh_fil=sea_surface_height
                print(np.max(ssh_fil))
                plt.plot(ssh_fil, label=f'{start_date} top branch')
                #plt.xlim([2000,2500])
                plt.legend()
                plt.savefig(f'time_series_png/{start_date}_{station}_top_branch.pdf')
            else:
                pass
    else:
        pass
    start_date=start_date+dayItr
    

# plt.legend() 
# plt.savefig(f'time_series_png/{start_date}.png')   
infragravity_wave_arr=np.array(infragravity_wave_list)
days_ig=pd.to_datetime(day_list)
df_dict={'Time':days_ig,'infragravity heights':infragravity_wave_arr}
df=pd.DataFrame(data=df_dict)
df.to_csv(f'/Users/seansantellanes/Documents/Background_Spectra/infragravity_waves/{station}_ig.csv')
ppsd.save_npz(f'/Users/seansantellanes/Documents/Background_Spectra/PPSD/NPZ/{station}_psd.npz')
#set legend, size,...
print(datetime.datetime.now() - startTime)