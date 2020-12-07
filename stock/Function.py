import matplotlib._color_data as mcd
from scipy import interpolate
import numpy as np
import csv
import os.path
from os import path

class Function(object):

    #_______________________________________________________________________________
    def __init__(self, name='func', file='data/br_B0p_eXN.csv'):

        self.x = []
        self.y = []

        if path.exists(file):
            with open(file) as csvfile:
                ## skip header
                #next(csvfile)
                reader = csv.reader(csvfile, delimiter='\t', quotechar='"')
                id = 0
                for data in reader:
                    #print (data)
                    self.x.append(float(data[0]))
                    self.y.append(float(data[1]))


    #_______________________________________________________________________________
    def eval(self, x):

        val=0
        if x <= max(self.x) and x >= min(self.x):
            f = interpolate.interp1d(self.x, self.y, kind='cubic')
            val = f(x)

        return val

    #_______________________________________________________________________________
    def clear_data(self):
        self.x = []
        self.y = []

    #_______________________________________________________________________________
    def scale_data(self, scale=1.0):

        xr = []
        yr = []

        for x, y in zip(self.x,self.y):
            xr.append(x)
            yr.append(y*scale)

        self.x = xr
        self.y = yr

#_______________________________________________________________________________
    def pow_data(self, power=1.0):

        xr = []
        yr = []

        for x, y in zip(self.x,self.y):
            xr.append(x)
            yr.append(y**power)

        self.x = xr
        self.y = yr
