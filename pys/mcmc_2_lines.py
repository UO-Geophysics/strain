#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 09:56:17 2020

@author: dmelgarm
"""

from numpy import genfromtxt,where,ones,arange,polyfit,tile,zeros
import pymc3 as pm  
from theano.compile.ops import as_op
import theano.tensor as tt
from theano import shared
import matplotlib.pyplot as plt


#get the data
pwaves = genfromtxt('/Users/sydneydybing/Downloads/DT2019_Cascadia_Amplitudes.txt')
# What exactly are the colunns here? Amplitude of waves at a specific time?
# My equivalent = peak strain at a specific time

#split into x and y vectors
xobserved = pwaves[:,0] # all rows, first column
print(xobserved.shape)
yobserved = pwaves[:,6] # all rows, seventh column (20s)
print(yobserved.shape)

# in order to pass the x variable into the target function it needs to be 
# converted to a Theano "shared" variable
xobserved = shared(xobserved)

# MCMC run parameters, these are good numbers for a "production" run. If you are
# fooling arund these can be lower to iterate faster
Nburn = 500
Nmcmc = 2000
Nchains = 1

#build the target function, misfit to this is what is being minimized
@as_op(itypes=[tt.dvector, tt.dscalar, tt.dscalar,tt.dscalar,tt.dscalar], otypes=[tt.dvector])
def two_straight_lines(x,m1,b1,m2,xinter):
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
def non_theano_two_straight_lines(x,m1,b1,m2,xinter):
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
    
    #build first straight line segment
    yout = m1*x + b1
    
    #find points that are after the intersection and make the second segment
    i=where(x>xinter)[0]
    
    #define second y intercept
    b2 = m1*xinter + b1 - m2*xinter
    
    #make second straight line
    yout[i] = m2*x[i] + b2

    return yout



    
    
#bounds for the prior distributions
m1_low = 0 ; m1_high =5 # lowest slope 0, highest 5
m2_low = 0 ; m2_high =5
b1_low = -20 ; b1_high = 0 # lowest y-intercept -20, highest 0
xinter_low = 5 ; xinter_high = 9 # location of the line slope change

#define the Bayesian model
with pm.Model()as model:
    
    #Use normal distributions as priors
    m1 = pm.Normal('m1', mu=0.5, sigma=1)
    m2 = pm.Normal('m2', mu=0,sigma=1)
    b1 = pm.Normal('b1', mu=-5, sigma=5)
    xinter = pm.Uniform('xinter', lower=xinter_low, upper=xinter_high)
    sigma = pm.HalfCauchy('sigma', beta=10, testval=1.)

    #this is the model
    likelihood = pm.Normal('y', mu=two_straight_lines(xobserved,m1,b1,m2,xinter),
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
b1 = mcmc['b1'].mean()
m2 = mcmc['m2'].mean()
xinter = mcmc['xinter'].mean()
b2 = m1*xinter + b1 - m2*xinter

#make plot to check stuff
xpredicted = arange(pwaves[:,0].min(),pwaves[:,0].max()+0.1,0.1)
ypredicted=ones(len(xpredicted))
ypredicted = m1*xpredicted +b1
i=where(xpredicted>xinter)[0]
ypredicted[i]=m2*xpredicted[i]+b2

#get one-sigma region (need to obtain a ton of forward models and get stats)
N=len(mcmc.get_values('m1'))

m1_array=mcmc.get_values('m1')
m2_array=mcmc.get_values('m2')
b1_array=mcmc.get_values('b1')
xinter_array=mcmc.get_values('xinter')

yfit = zeros((len(xpredicted),N))
for k in range(N):
    yfit[:,k] = non_theano_two_straight_lines(xpredicted,m1_array[k],b1_array[k],m2_array[k],xinter_array[k])

mu = yfit.mean(1)
sig = yfit.std(1)*1.95 #for 95% confidence
mu_plus=mu+sig
mu_minus=mu-sig



#least squares
mls,bls = polyfit(pwaves[:,0],yobserved,1)

plt.figure()
plt.scatter(pwaves[:,0],yobserved,s=2,label='observed')
#plt.plot(xpredicted,ypredicted,c='r',label='predicted')
plt.plot(xpredicted,mu,c='r',label='predicted')
plt.plot(xpredicted,xpredicted*mls+bls,c='k',label='lstsq')
plt.legend()
plt.fill_between(xpredicted,mu_plus,mu_minus,color='r',alpha=0.2)
plt.xlabel('Mw')
plt.ylabel('log(Pd)')


