# PATH VARIABLES WERE CONTRADICTORY. PYTHON3 DOES NOT REQUIRIE PATH SPECIFICATION HERE.
"""
This script fits an example data set with an exponential decay function.
"""

#Import libraries
import abbie_csv as ac
import numpy as np      # NEVER IMPORT WITHIN A FUNCTION
import matplotlib.pyplot as plt #for plotting function
from scipy.optimize import curve_fit

#Data import method
def csvimport(filename, headskip):          # ALL THAT OS STUFF NOT NEEDED
    #Then uses that file location to run numpy's "generate from text" method
    newdata = np.genfromtxt(datalocation, delimiter=', ', unpack=True, skip_header=headskip)
    return newdata

#Function that tells you the index in an array closest to a given value.
#This is useful if you want to fit only between two times (and need to know
# where those times show up in the data set.)
def get_index(subset, shift):           # ONLY TAKES ONE TIME? //NEVER CALLED//NO DOCSTRING
    return min(range(len(subset)),  key=lambda i: abs(subset[i]-shift))

def main():     # THERE SHOULD BE NO TOP LEVEL CODE --> KEEP EVERYTHING INSIDE A MAIN() FUNCTION IN CASE OF IMPORT
    #Define the function to which data will be fit
    #Simple exponential function with vertical offset for fitting
    def varexp(x, a, k, c):
        return a*np.exp(k*x)+c

    #Import Data    IDEALLY NOTHING WOULD BE HARD CODED
    data = ac.csvImport('HillPractice.csv')
    data = np.array(data)
    data = data.T

    #Fitting will happen here------------------------------------------------------
    fit, cov = curve_fit(varexp, data[0], data[1], p0=[-3, -0.002, 0], maxfev=100000)       # BOUNDS PREVENTED ACCURATE REGRESSION
                               
    #p0 is data syntax from curve_fit method,  list initial
    #parameters in order listed in def varexp
    #bounds,  square bracket first set is lower,  2nd is upper      WHAT WERE THEY LIMIITING??
    errors = np.sqrt(np.diag(cov))
    print(f'a={fit[0]}\tk={fit[1]}\tc={fit[2]}')        # TERMNAL OUTPUT SHOULD INDICATE WHAT IT IS
    print(f'The error array is {errors}.')
    #cov is covariance is how one variable depends on another
    #------------------------------------------------------------------------------

    plt.rcParams.update({'font.size': 14}) #Up the font size if we're going to plot large
    #Plot the results
    plt.close(1) #Close figure 1 where we'll be plotting (if it's open) so that we don't keep plotting over old results as we
                 # develop the figure through piecewise coding. THIS MAKES NO SENSE      THE BENEFIT OF CODE IS THAT IT CAN BE RUN ONCE. PLUS PYTHON IS SINGLE THREADED SO YOU CAN'T HAVE TWO SCRIPTS INTERACTNG WITH THE SAME OBJECT IN MEMORY
    fig1 = plt.figure(1)
    plt.plot(data[0], data[1], 'ok', data[0], varexp(data[0], fit[0], fit[1], fit[2]), '-r') # "o" means plot dots,  "k" means plot black (key) color
    plt.xlabel("Time (ms)") #Label the axes
    plt.ylabel("Integrated peak area")
    plt.legend(['Rapid-Scan FTIR Bleach Recovery Data', 'Fit Results:\na='+"%10.3E"%(fit[0])+' +/- '+'%10.3E'%(errors[0])+'\nk='+'%10.6E'%(fit[1])+' +/- '+'%10.6E'%(errors[1])+'\nc='+'%10.2E'%(fit[2])+' +/- '+'%10.2E'%(errors[2])])     # USE AN F-STRING. THIS IS PYTHON 3
    fig1.tight_layout() #Makes figure borders go to near window borders--good for figures for publication.

    plt.show()

if __name__ == '__main__':
    main()
