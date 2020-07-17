#!/usr/bin/env python3
"""
This script fits an example data set with an exponential decay function.
"""

#Import libraries
import abbie_csv as ac
import numpy as np
import matplotlib.pyplot as plt #for plotting function
plt.rcParams.update({'font.size': 14}) #Up the font size if we're going to plot large
from scipy.optimize import curve_fit

#Data import method
def csvimport(filename, headskip):
    import os #Though I imported a bunch of things at the start because I knew I'd need them,  you can also import elsewhere
    temppath = str(os.path.dirname(os.path.realpath(__file__))) #This asks for the folder where *this* script current is...
    #Then puts that together with the data filename you gave it.
    datalocation = temppath + '/' + filename  #NOTE: '/' is for macOS; change to '\\' for Windows.
    #Then uses that file location to run numpy's "generate from text" method
    newdata = np.genfromtxt(datalocation, delimiter=', ', unpack=True, skip_header=headskip)
    return newdata

#Function that tells you the index in an array closest to a given value.
#This is useful if you want to fit only between two times (and need to know
# where those times show up in the data set.)
def get_index(subset, shift):
    return min(range(len(subset)),  key=lambda i: abs(subset[i]-shift))

#Define the function to which data will be fit
#Simple exponential function with vertical offset for fitting
def varexp(x, a, k, c):
    return a*np.exp(k*x)+c

#Import data
data = ac.csvImport('HillPractice.csv')
data = np.array(data)
data = data.T

#Fitting will happen here------------------------------------------------------
fit, cov = curve_fit(varexp, data[0], data[1], p0=[-3, -0.002, 0], bounds=([-10, -np.inf, -1], [0, 0, 1]), maxfev=100000)
                           
#p0 is data syntax from curve_fit method,  list initial
#parameters in order listed in def varexp
#bounds,  square bracket first set is lower,  2nd is upper
errors = np.sqrt(np.diag(cov))
print(fit)
print(errors)
#cov is covariance is how one variable depends on another
#------------------------------------------------------------------------------

#Plot the results
plt.close(1) #Close figure 1 where we'll be plotting (if it's open) so that we don't keep plotting over old results as we
             # develop the figure through piecewise coding.
fig1 = plt.figure(1)
plt.plot(data[0], data[1], 'ok', data[0], varexp(data[0], fit[0], fit[1], fit[2]), '-r') # "o" means plot dots,  "k" means plot black (key) color
plt.xlabel("Time (ms)") #Label the axes
plt.ylabel("Integrated peak area")
plt.legend(['Rapid-Scan FTIR Bleach Recovery Data', 'Fit Results:\na='+"%10.3E"%(fit[0])+' +/- '+'%10.3E'%(errors[0])+'\nk='+'%10.6E'%(fit[1])+' +/- '+'%10.6E'%(errors[1])+'\nc='+'%10.2E'%(fit[2])+' +/- '+'%10.2E'%(errors[2])])
fig1.tight_layout() #Makes figure borders go to near window borders--good for figures for publication.

plt.show()

