#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 15:06:13 2020

@author: sydneydybing
"""
from obspy.core import read
import numpy as np
from numpy import genfromtxt,where,ones,arange,polyfit,tile,zeros
import pymc3 as pm  
from theano.compile.ops import as_op
import theano.tensor as tt
from theano import shared
import matplotlib.pyplot as plt


#get the data
#pwaves = genfromtxt('/Users/sydneydybing/Downloads/DT2019_Cascadia_Amplitudes.txt')
# What exactly are the colunns here? Amplitude of waves at a specific time?
# My equivalent = peak strain at a specific time

#build the target function, misfit to this is what is being minimized
@as_op(itypes=[tt.dvector, tt.dscalar, tt.dscalar,tt.dscalar,tt.dscalar,tt.dscalar], otypes=[tt.dvector])
def two_straight_lines(x,m1,m2,xinter,x0,y0):
    '''
    input x coordiantes are in x
    slopes are m1 and m2
    intercept of left hand line is b1 
    intersection of two lines is at xinter
    
    Note that y intercept of second straight line is dependent on b1 and xinter
      and defined entirely by them (so that the lines touch).
    '''
    
    #output vector
    yout = ones(len(x))
    
    #before building the first straight line, calculate the intercept
    b1 = y0 - m1*x0
    
    #build first straight line segment
    yout = m1*x + b1
    
    #find points that are after the intersection and make the second segment
    i=where(x>xinter)[0]
    
    #define second y intercept
    b2 = m1*xinter + b1 - m2*xinter
    
    #make second straight line
    yout[i] = m2*x[i] + b2

    return yout

#build the target function, misfit tot his is what is being minimized
def non_theano_two_straight_lines(x,m1,m2,xinter,x0,y0):
    '''
    input x coordiantes are in x
    slopes are m1 and m2
    intercept of left hand line is b1 
    intersection of two lines is at xinter
    
    Note that y intercept of second straight line is dependent on b1 and xinter
      and defined entirely by them (so that the lines touch).
    '''
    
    #output vector
    yout = ones(len(x))
    
    #before building the first straight line, calculate the intercept
    b1 = y0 - m1*x0
    
    #build first straight line segment
    yout = m1*x + b1
    
    #find points that are after the intersection and make the second segment
    i=where(x>xinter)[0]
    
    #define second y intercept
    b2 = m1*xinter + b1 - m2*xinter
    
    #make second straight line
    yout[i] = m2*x[i] + b2

    return yout

##### Barbour Data Info #####

quake_folders = np.genfromtxt('/Users/sydneydybing/StrainProject/quake_folders.txt', dtype=str)
stas = np.genfromtxt('/Users/sydneydybing/StrainProject/stations.txt', dtype=str)

# stas = ['B081', 'B082', 'B084', 'B086', 'B087', 'B088', 'B093']
# test_stas = ['B081', 'B082', 'B084']

for quake in quake_folders:
    for sta in stas:
        
        try:
            path_to_file = '/Users/sydneydybing/StrainProject/M6_500km_sel/StrainData_sel/Trimmed/PeakStrains/' + quake + '/' + sta + '_PST.mseed'
            st = read(path_to_file)
            # st.plot()
            
            data = st[0].data
            # print(data)
            log10_data = np.log10(data)
            # print(log10_data)
            times = st[0].times()
            print(times)
            
            # x0 = float(10)
            # # find y0 - the strain value at x0
            
            # i = where(times == x0)[0]
            # y0 = float(log10_data[i])
            # print(i)
            # print(y0)
        
            # print(times)
            
            #split into x and y vectors
            xobserved = times[205:1281]
            print(xobserved.shape)
            
            yobserved = log10_data[205:1281]
            print(yobserved.shape)
            
            # xobserved = times[205:1200]
            # print(xobserved.shape)
            
            # yobserved = log10_data[205:1200]
            # print(yobserved.shape)
            
            x0 = xobserved[0]
            y0 = yobserved[0]
            
            # xobserved = times[205:400]
            # # print(xobserved.shape)
            
            # yobserved = log10_data[205:400]
            # # print(yobserved.shape)
            
            # in order to pass the x variable into the target function it needs to be 
            # converted to a Theano "shared" variable
            theano_xobserved = shared(xobserved)
            theano_x0 = shared(x0)
            theano_y0 = shared(y0)
            
            # MCMC run parameters, these are good numbers for a "production" run. If you are
            # fooling arund these can be lower to iterate faster
            Nburn = 1000 # burn in samples that get discarded
            Nmcmc = 2000 # bump to at least 5-10k
            Nchains = 1
            
            #bounds for the prior distributions
            m1_low = 0 ; m1_high = 100 # lowest slope 0, highest 5
            m2_low = 0 ; m2_high = 10
            b1_low = -50 ; b1_high = 0 # lowest y-intercept -20, highest 0
            xinter_low = 11 ; xinter_high = 13 # location of the line slope change
            
            #define the Bayesian model
            with pm.Model()as model:
                
                #Use normal distributions as priors
                m1 = pm.Normal('m1', mu=0.5, sigma=1)
                m2 = pm.Normal('m2', mu=-0.1,sigma=5)
                # b1 = pm.Normal('b1', mu=-5, sigma=5)
                xinter = pm.Uniform('xinter', lower=xinter_low, upper=xinter_high)
                sigma = pm.HalfCauchy('sigma', beta=10, testval=1.)
            
                #this is the model
                likelihood = pm.Normal('y', mu=two_straight_lines(theano_xobserved,m1,m2,xinter,theano_x0,theano_y0),
                                        observed=yobserved,sigma=sigma)
            #    likelihood = pm.Normal('y', mu=one_straight_line(xobserved,m1,b1),observed=yobserved,
            #                           sigma=sigma)
                
                # NUTS sampler (default) is gradient based and won't work, use metropolis
                step = pm.Metropolis()
                
                #This runs the mcmc sampler
                mcmc = pm.sample(Nmcmc, tune = Nburn,cores = Nchains,step=step)
            
            
            # done, now is post-processing to get the data out of the sampler
            
            ##Unwrap coeficients
            m1 = mcmc['m1'].mean() #Youc an also get the uncertainties by getting the std. dev.
            # b1 = mcmc['b1'].mean()
            m2 = mcmc['m2'].mean()
            xinter = mcmc['xinter'].mean()
            b1 = y0 - m1*x0
            b2 = m1*xinter + b1 - m2*xinter
            
            #make plot to check stuff
            xpredicted = arange(xobserved.min(),xobserved.max()+0.1,0.1)
            ypredicted=ones(len(xpredicted))
            ypredicted = m1*xpredicted +b1
            i=where(xpredicted>xinter)[0]
            ypredicted[i]=m2*xpredicted[i]+b2
            
            #get one-sigma region (need to obtain a ton of forward models and get stats)
            N=len(mcmc.get_values('m1'))
            
            m1_array=mcmc.get_values('m1')
            print(m1_array)
            print('m1 Mean: ' + str(np.mean(m1_array)))
            np.savez('/Users/sydneydybing/StrainProject/M6_500km_sel/StrainData_sel/Trimmed/PeakStrains/MCMC_npz/' + quake + '/' + sta + '_m1.npz')
            m2_array=mcmc.get_values('m2')
            print(m2_array)
            print('m2 Mean: ' + str(np.mean(m2_array)))
            np.savez('/Users/sydneydybing/StrainProject/M6_500km_sel/StrainData_sel/Trimmed/PeakStrains/MCMC_npz/' + quake + '/' + sta + '_m2.npz')
            # b1_array=mcmc.get_values('b1')
            xinter_array=mcmc.get_values('xinter')
            
            # plt.hist(m1_array)
            # plt.show()
            
            yfit = zeros((len(xpredicted),N))
            for k in range(N):
                yfit[:,k] = non_theano_two_straight_lines(xpredicted,m1_array[k],m2_array[k],xinter_array[k],x0,y0)
            
            mu = yfit.mean(1)
            sig = yfit.std(1)*1.95 #for 95% confidence
            mu_plus=mu+sig
            mu_minus=mu-sig
            
            
            
            #least squares
            mls,bls = polyfit(xobserved,yobserved,1)
            
            plt.figure()
            plt.plot(xobserved,yobserved,label='observed')
            #plt.plot(xpredicted,ypredicted,c='r',label='predicted')
            plt.plot(xpredicted,mu,c='r',label='predicted')
            plt.plot(xpredicted,xpredicted*mls+bls,c='k',label='lstsq')
            plt.legend()
            plt.fill_between(xpredicted,mu_plus,mu_minus,color='r',alpha=0.2) #95% confidence interval
            plt.xlabel('Time (s) - p-wave at 10s')
            plt.ylabel('log(PST)')
            plt.savefig('/Users/sydneydybing/StrainProject/M6_500km_sel/StrainData_sel/Trimmed/PeakStrains/MCMC_figs/' + quake + '/' + sta + '.jpg', format="JPEG", dpi=400)
            plt.close()
        
        except:
            print(quake + " no station " + sta) 
    
        
        
        