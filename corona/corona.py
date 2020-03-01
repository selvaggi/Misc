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

from collections import OrderedDict

#_______________________________________________________________________________
def epidemics_simulation(r, gamma, S0, I0):

    N0 = S0 + I0

    ### lambda0 = C Chi / N
    lambda0 = r / N0

    ### basic reproductive number
    R0 = r / gamma

    print 'Simulation parameters:'
    print '-----------------------'
    print 'gamma:', gamma
    print 'r:', r
    print 'R0:', R0
    print '-----------------------'
    print ''
    print ''


    ## number of days to run sim on

    N = OrderedDict()
    S = OrderedDict()
    I = OrderedDict()
    R = OrderedDict()
    lmbd = OrderedDict()

    I[0]=I0
    S[0]=S0
    R[0]=R0
    N[0]=N0
    lmbd[0] = lambda0

    print "{0:>7s} {1:>10s} {2:>10s} {3:>10s} {4:>13s}".format("time (days)", "S(t)", "I(t)", "R(t)", "lambda(t)")
    print"--------------------------------------------------------------------------------------------------------------"


    ndays_tot = 999999999

    for t in range(1, ndays_tot):

        lmbd[t] = r*I[t-1]/N[t-1]
        S[t] = S[t-1] - lmbd[t] * S[t-1]
        I[t] = I[t-1] + lmbd[t] * S[t-1] - gamma * I[t-1]
        R[t] = R[t-1] + gamma * I[t-1]
        N[t] = S[t] + I[t] + R[t]

        if I[t] < 1: break
        #print t, S[t], I[t], R[t], N[t]
        print "{0:5.0f} {1:17.2e} {2:10.2e} {3:10.2e} {4:11.2e}  ".format(t, S[t], I[t], R[t], lmbd[t])

    fig, ax = plt.subplots(figsize=(7, 5))

    nd = S.keys()

    ax.plot(nd, S.values(), label='S', linewidth=2)
    ax.plot(nd, I.values(), label='I', linewidth=2)
    ax.plot(nd, R.values(), label='R', linewidth=2)

    ax.set_title(r'$\gamma = {:.2f},    r = c \chi = {:.2f},     R_0 = r/\gamma = {:.2f} $'.format(gamma,r,R0))
    ax.legend(loc='upper left')
    ax.set_ylabel('N')
    ax.set_xlabel('t (days)')
    ax.set_xlim(xmin=nd[0], xmax=nd[-1])
    ax.set_yscale('log')

    ax.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)
    ax.grid(True, 'major', 'x', ls='--', lw=.5, c='k', alpha=.3)

    fig.tight_layout()
    #fig.show()

    #title_str = '{}_c{}_chi{}_R0{},
    filename = 'corona_gamma{:.2e}_r{:.2e}_R0{:.2e}.png'.format(gamma,r,R0)

    fig.savefig('plots/{}'.format(filename))
    print 'created plots/{}'.format(filename)

#_______________________________________________________________________________

# average time spent as infected (in days)
tau = 30.

# removal rate = number of death + recover per unit time (time in days)
gamma = 1/tau

## c = number of contacts per unit time (time in days)
c = 20

### chi = effectiveness of contact
chi = 0.01

# rate of infections per unit time
r = c* chi

r = 1/15.

### initial conditions

S0 = 6.e7 -1
I0 = 1 ## initial infected

epidemics_simulation(r, gamma, S0, I0)
