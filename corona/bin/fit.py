import os, sys
import math
import random
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from numpy import array
from scipy import stats
from matplotlib.ticker import FuncFormatter, MaxNLocator
from matplotlib.colors import BoundaryNorm
import multiprocessing as mp
import scipy
from collections import OrderedDict

#_______________________________________________________________________________
def fit_I_asympt(data_dict, show=False):

    def exponential(x, a, k):
        return a*np.exp(x*k)

    x_data = np.array(data_dict.keys())
    y_data = np.array(data_dict.values())
    y_err  = np.sqrt(y_data)

    #fitfunc = lambda p, x: p[0]*np.exp(x*p[1])
    #errfunc = lambda p, x, y, err: (y - fitfunc(p, x)) / err

    #params, params_covariance = scipy.optimize.curve_fit(exponential, x_data, y_data, p0=[1,1], sigma=y_err)
    params, params_covariance = scipy.optimize.curve_fit(exponential, x_data, y_data, p0=[1,1])
    #params, params_covariance = scipy.optimize.leastsq(errfunc, [1,1], args=(x_data, y_data, y_err), full_output=1)

    #pinit = [1.0, -1.0]
    #out = scipy.optimize.leastsq(errfunc, pinit,args=(x_data, y_data, y_err), full_output=1)

    #params = out[0]
    #params_covariance = out[1]

    I0 = params[0]
    cXmG = params[1]

    print ""
    print "parameters: I0 = {:.1f}, cX - gamma = {:.1f}, taueff = {:.1f}".format(I0, cXmG,1./cXmG)
    print ""

    I0 = params[0]
    cXmG = params[1]

    fig, ax = plt.subplots(figsize=(7, 5))

        #plt.scatter(x_data, y_data, label='Data')
    ax.errorbar(x_data, y_data, yerr=y_err, fmt="none", linewidth=2, capsize=2, elinewidth=2, markeredgewidth=2)
    ax.plot(x_data, exponential(x_data, params[0], params[1]),
             label='I(t) = {:.1f}exp(t/{:.1f})'.format(I0,1./cXmG), linewidth=2)
    ax.legend(loc='best')
    if show:
        fig.show()

    ax.legend(loc='best')
    fig.tight_layout()
    fig.savefig('plots/fitI.png')

    return I0, cXmG

#_______________________________________________________________________________
def fit_D_asympt(data_dict, I0, cXmG, show=False):

    def death(x, dgamma):
    #def death(x, gamma, d, cX):
        return dgamma*I0/(cXmG)*(np.exp(x*cXmG)-1)

    x_data = np.array(data_dict.keys())
    y_data = np.array(data_dict.values())
    y_err  = np.sqrt(y_data)

    #params, params_covariance = scipy.optimize.curve_fit(death, x_data, y_data, p0=[0.01,1, cX])
    #print "parameters: d = {}, gamma = {}, cX = {}".format(params[0], params[1], params[2])
    #params, params_covariance = scipy.optimize.curve_fit(death, x_data, y_data, p0=[1], maxfev=2000, sigma=y_err)
    params, params_covariance = scipy.optimize.curve_fit(death, x_data, y_data, p0=[1], maxfev=2000)
    dgamma = params[0]
    print ""
    print "parameters: dgamma = {:.3f}".format(dgamma)
    print ""

    dgamma = params[0]

    fig, ax = plt.subplots(figsize=(7, 5))

    ax.errorbar(x_data, y_data, yerr=y_err, fmt="none", linewidth=2, capsize=2, elinewidth=2, markeredgewidth=2)
    ax.plot(x_data, death(x_data, params[0]), label='D(t) fitted', linewidth=2)

    ax.legend(loc='best')
    fig.tight_layout()
    fig.savefig('plots/fitD.png')

    if show:
        fig.show()

    return dgamma
