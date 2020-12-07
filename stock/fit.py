import numpy as np
import pandas as pd
from datetime import date
import math

today = date.today()
beginning_year = date(today.year, 1, 1)
delta = today - beginning_year
delta_fraction = delta.days/365.25
year_today = today.year+delta_fraction
print(year_today)


# We'll use scipy.optimize.curve_fit to do the nonlinear regression
import scipy.optimize

import matplotlib.pyplot as plt
import seaborn as sns
rc={'lines.linewidth': 2, 'axes.labelsize': 18, 'axes.titlesize': 18}
sns.set(rc=rc)

from Function import *


lower_band = Function('lower', 'data/lower_band.csv')
upper_band = Function('upper', 'data/upper_band.csv')
#lower_band = Function('lower', 'data/lower_band.csv')

#print(lower_band.eval(2014), lower_band.eval(2016), lower_band.eval(2018))

lower_band_today = lower_band.eval(year_today)
upper_band_today = upper_band.eval(year_today)


price_today = 50000

print(price_today,lower_band_today, upper_band_today)


rescaled_price = (price_today - lower_band_today)/(upper_band_today - lower_band_today)

print(rescaled_price)

linear_risk = rescaled_price
exp_risk = math.exp(rescaled_price -1.)
exp10_risk = 10**(rescaled_price -1.)


print(linear_risk, exp_risk, exp10_risk)


# Import data set
#df = pd.read_csv('data/lower_band.csv', delimiter='\t', quotechar='"', comment='#')

# Inspect DataFrame
#print(df)
