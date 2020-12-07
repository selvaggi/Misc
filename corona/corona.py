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
def epidemics_simulation(r, gamma, d, S0, I0):

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
    RR = OrderedDict()
    D = OrderedDict()
    T = OrderedDict()
    lmbd = OrderedDict()

    I[0]=I0
    S[0]=S0
    R[0]=0
    RR[0]=0
    N[0]=N0
    D[0] = 0
    T[0] = I[0] + R[0]
    lmbd[0] = lambda0

    print "{0:>7s} {1:>10s} {2:>10s} {3:>10s} {4:>13s}".format("time (days)", "S(t)", "I(t)", "R(t)", "lambda(t)")
    print"--------------------------------------------------------------------------------------------------------------"


    ndays_tot = 9999

    tstar = 0
    Istar = -999

    for t in range(1, ndays_tot):

        lmbd[t] = r*I[t-1]/N[t-1]
        S[t] = S[t-1] - lmbd[t] * S[t-1]
        I[t] = I[t-1] + lmbd[t] * S[t-1] - gamma * I[t-1]
        R[t] = R[t-1] + gamma * I[t-1]
        N[t] = S[t] + I[t] + R[t]
        T[t] = I[t] + R[t]

        D[t] = d*R[t]
        RR[t] = R[t] - D[t]

        ## compute time when max infected
        if I[t] > Istar:
            Istar = I[t]
            tstar = t

        if I[t] < 1: break
        #print t, S[t], I[t], R[t], N[t]
        print "{0:5.0f} {1:17.2e} {2:10.2e} {3:10.2e} {4:11.2e}  ".format(t, S[t], I[t], R[t], lmbd[t])

    fig, ax = plt.subplots(figsize=(7, 5))

    nd = S.keys()

    ax.plot(nd, S.values(), label='S(t)', linewidth=2, color='blue')
    ax.plot(nd, I.values(), label='I(t)', linewidth=2, color='orange')
    ax.plot(nd, RR.values(), label='R(t)', linewidth=2, color='green')
    ax.plot(nd, T.values(), label='I(t) + R(t)', linewidth=2, color='purple')
    ax.plot(nd, D.values(), label='D(t)', linewidth=2, color='red')

    ax.axvline(x=tstar, color='black', linestyle='--')

    ax.set_title(r'$\gamma = {:.2f},    r = c \chi = {:.2f},     R_0 = r/\gamma = {:.2f},  t_* = {} \mathrm{{\,days}}$'.format(gamma,r,R0,tstar))
    ax.legend(loc='lower center')
    ax.set_ylabel('N')
    ax.set_xlabel('t (days)')
    ax.set_xlim(xmin=nd[0], xmax=nd[-1])
    ax.set_ylim(ymin=1, ymax=10*S0)
    ax.set_yscale('log')

    ax.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)
    ax.grid(True, 'major', 'x', ls='--', lw=.5, c='k', alpha=.3)
    ax.legend(loc='best')
    #ax.text(0.6, 0.2, r'$t_* = {}$'.format(tstar) + ' days', horizontalalignment='center',verticalalignment='center', transform=ax.transAxes)

    fig.tight_layout()
    #fig.show()

    #title_str = '{}_c{}_chi{}_R0{},
    filename = 'corona_gamma{:.2e}_r{:.2e}_R0{:.2e}.png'.format(gamma,r,R0)

    fig.savefig('plots/{}'.format(filename))
    print 'created plots/{}'.format(filename)

#_______________________________________________________________________________

# average time spent as infected (in days)
tau = 4.

# removal rate = number of death + recover per unit time (time in days)
gamma = 1/tau

#tau_r
tau_r = 2.

r = 1/tau_r

### initial conditions

S0 = 6.e9 -1
I0 = 10 ## initial infected

## death rate (not an actual parameter for the dynamics)
d = 0.01

epidemics_simulation(r, gamma, d, S0, I0)
