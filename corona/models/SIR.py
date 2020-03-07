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


class SIR(object):

    #_______________________________________________________________________________
    def __init__(self, initialValues, params):

        ## values at t=0
        self.S0 = initialValues[0]
        self.I0 = initialValues[1]
        self.R0 = initialValues[2]
        self.N0 = self.S0 + self.I0 + self.R0

        # removal rate = number of death + recover per unit time (time in days)
        self.tau_i = params[0]
        self.tau_r = params[1]
        self.d = params[2]

        self.cX = 1/self.tau_i
        self.gamma = 1/self.tau_r
        self.cXmG = self.cX - self.gamma
        self.tau_ieff = 1./self.cXmG
        self.dgamma = self.d * self.gamma

        ### lambda0 = C Chi / N
        self.lambda0 = self.cX / self.N0

        ### basic reproductive number
        self.r0 = self.cX / self.gamma

        ### time at maximum
        self.tstar = -1
        self.Istar = -1
        self.Dstar = -1

        self.N = OrderedDict()
        self.S = OrderedDict()
        self.I = OrderedDict()
        self.Ias = OrderedDict()
        self.R = OrderedDict()
        self.D = OrderedDict()
        self.Das = OrderedDict()
        self.F = OrderedDict()
        self.lmbd = OrderedDict()

        self.I[0]=self.I0
        self.Ias[0]=self.I0
        self.S[0]=self.S0
        self.R[0]=0
        self.N[0]=self.N0
        self.D[0] = 0.
        self.Das[0] = 0.
        self.F[0] = 0.
        self.lmbd[0] = self.lambda0

    #_______________________________________________________________________________
    def print_params(self):
        print '-----------------------'
        print ''
        print 'Simulation parameters:'
        print '-----------------------'
        print 'I0        = {:.2f}'.format(self.I0)
        print 'tau_i     = {:.2f}'.format(self.tau_i)
        print 'cX        = {:.2f}'.format(self.cX)
        print 'd         = {:.2f}'.format(self.d)
        print 'tau_r     = {:.2f}'.format(self.tau_r)
        print 'gamma     = {:.2f}'.format(self.gamma)
        print 'cX -gamma = {:.2f}'.format(self.cXmG)
        print 'tau_ieff  = {:.2f}'.format(1./self.cXmG)
        print '-----------------------'
        print 'S0        = {:.2f}'.format(self.S0)
        print 'I0        = {:.2f}'.format(self.I0)
        print 'R0        = {:.2f}'.format(self.R0)
        print '-----------------------'
        print 'r0        = {:.2f}'.format(self.r0)
        print '-----------------------'
        print ''

    #____7___________________________________________________________________________
    def simulate(self, nsteps=1000, ndays=1000):

        ## peak epidemics time
        Istar = -999

        ## number of steps per day for differentiation
        dt = float(1./nsteps)

        II = self.I0
        NN = self.N0
        SS = self.S0
        RR = 0.

        for n in range(1, ndays*nsteps):

            l = self.cX*II/NN
            SS = SS*(1. - l*dt)
            II = II*(1. - self.gamma*dt) + SS*l*dt
            #Ias[t] = Ias[t-1] + (cX - gamma) * Ias[t-1]

            RR = RR + self.gamma * dt * II
            NN = SS + II + RR
            DD = self.d*RR

            t=n*dt

            if n%nsteps == 0:

                self.Ias[t] = self.I0 * math.exp((self.cXmG)*t)
                self.Das[t] = self.dgamma*self.I0/self.cXmG * (np.exp(self.cXmG*t) - 1.)
                #Das[t] = death(t, d*gamma)

                self.I[t] = II
                self.S[t] = SS
                self.R[t] = RR
                self.D[t] = DD
                self.lmbd[t] = l

                # fatality rate
                self.F[t] = self.D[t]/(self.I[t]+self.R[t])

                ## compute chi2
                    ## compute time when max infected
                if self.I[t] > Istar:
                    Istar = self.I[t]
                    self.tstar = t

                if self.I[t] < 1: break
                #print t, S[t], I[t], R[t], N[t]

    #___________________________________________________________________________
    def print_simulation(self):

        print "{0:>7s} {1:>10s} {2:>10s} {3:>10s}  {4:>10s} {5:>10s} {6:>13s} {7:>10s} {8:>13s}".format("time (days)", "S(t)", "I(t)", "Ias(t)", "R(t)", "D(t)", "Das(t)", "F(t)", "lambda(t)")
        print "------------------------------------------------------------------------------------------------------------------------------------------"
        for t in range(len(self.I)):
            print "{0:5.0f} {1:17.2e} {2:10.2e} {3:10.2e} {4:10.2e} {5:11.2e} {6:11.2e} {7:11.2e} {8:11.2e} ".format(t, self.S[t], self.I[t], self.Ias[t], self.R[t], self.D[t], self.Das[t], self.F[t], self.lmbd[t])
        print ""
        print "FIXME: print interesting results"


    #___________________________________________________________________________
    def plot_yields(self, I_data, D_data, tp=0, tmin=0, tmax=1.e10, ymin=0, ymax=1.e10, log=True, plotData=False, tag='v0'):

        fig, ax = plt.subplots(figsize=(7, 5))

        nd = self.S.keys()

        ax.plot(nd, self.S.values(), label='S(t)', linewidth=2, color='blue')
        ax.plot(nd, self.I.values(), label='I(t)', linewidth=2, color='orange')
        ax.plot(nd, self.R.values(), label='R(t)', linewidth=2, color='green')
        #ax.plot(nd, RR.values(), label='R(t)', linewidth=2, color='green')
        #ax.plot(nd, T.values(), label='I(t) + R(t)', linewidth=2, color='purple')
        #ax.plot(nd, F.values(), label='F(t)', linewidth=2, color='red')
        ax.plot(nd, self.D.values(), label='D(t)', linewidth=2, color='red')

        if plotData:
            ax.scatter(I_data.keys(), I_data.values(), label='I(data)',  color='orange')
            ax.scatter(D_data.keys(), D_data.values(), label='D(data)', color='red')

        ax.axvline(x=self.tstar, color='black', linestyle='--')
        ax.axvline(x=tp, color='black', linestyle='-')

        ax.set_title(r'$\tau_i = {:.1f},  \tau_r = {:.1f},  R_0 = c \chi/\gamma = \tau_r/\tau_i = {:.2f}, t_* = {} \mathrm{{\,days}}$'.
            format(self.tau_i,self.tau_r,self.tau_r/self.tau_i,self.tstar))
        ax.legend(loc='lower center')
        ax.set_ylabel('N')
        ax.set_xlabel('t (days)')

        if tmax > nd[-1]: tmax=nd[-1]
        ax.set_xlim(xmin=tmin, xmax=tmax)
        if ymax > 10*self.S0: ymax=10*self.S0
        ax.set_ylim(ymin=1, ymax=ymax)
        if log:
            ax.set_yscale('log')

        ax.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)
        ax.grid(True, 'major', 'x', ls='--', lw=.5, c='k', alpha=.3)
        ax.legend(loc='best')
        #ax.text(0.6, 0.2, r'$t_* = {}$'.format(tstar) + ' days', horizontal alignment='center',verticalalignment='center', transform=ax.transAxes)

        fig.tight_layout()

        filename = 'corona_ti{:.2e}_tr{:.2e}_r0{:.2e}_{}_yields.png'.format(self.tau_i,self.tau_r,self.tau_r/self.tau_i,tag)

        fig.savefig('plots/{}'.format(filename))
        print ''
        print 'created plots/{}'.format(filename)


    #_______________________________________________________________________________
    def plot_rates(self, tp=0, tmin=0, tmax=1.e10, ymin=0, ymax=1.e10, log=True, tag='v0'):

        nd = S.keys()

        ## second plot
        fig2, ax2 = plt.subplots(figsize=(7, 5))
        ax2.plot(nd, F.values(), label='F(t)', linewidth=2, color='red')
        ax2.plot(nd, lmbd.values(), label='$\lambda(t)$', linewidth=2, color='orange')

        ax2.set_title(r'$\tau_i = {:.1f},  \tau_r = {:.1f},  R_0 = c \chi/\gamma = \tau_r/\tau_i = {:.2f}, t_* = {} \mathrm{{\,days}}$'.format(tau_i,tau_r,tau_r/tau_i,tstar))
        ax2.legend(loc='lower center')
        ax2.set_ylabel('rate (/day)')
        ax2.set_xlabel('t (days)')

        if tmax > nd[-1]: tmax=nd[-1]
        ax2.set_xlim(xmin=tmin, xmax=tmax)

        if ymax < 1.e10:
            ax2.set_ylim(ymin=0, ymax=ymax)
        if log:
            ax2.set_yscale('log')

        ax2.axvline(x=tstar, color='black', linestyle='--')
        ax2.axvline(x=tp, color='black', linestyle='-')

        ax2.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)
        ax2.grid(True, 'major', 'x', ls='--', lw=.5, c='k', alpha=.3)
        ax2.legend(loc='best')

        fig2.tight_layout()
        #fig.show()

        #title_str = '{}_c{}_chi{}_R0{},
        filename2 = 'corona_ti{:.2e}_tr{:.2e}_r0{:.2e}_rate.png'.format(tau_i,tau_r,tau_r/tau_i)
        fig2.savefig('plots/{}'.format(filename2))
        print ''
        print 'created plots/{}'.format(filename2)
