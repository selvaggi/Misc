from models.SIR import *
from bin.fit import *
from bin.data_parsers import *
from collections import OrderedDict

#_______________________________________________________________________________
def main():


    datasets = DataSets('data/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv',
                      'data/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv',
                      'data/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv')


    ## death fraction (take from WHO)
    d = 0.001
    N0 = 6.e9

    tmin=30
    tp = 44-tmin

    dataset = datasets.countryDict['NotChina']
    dataset.resize(tmin, 99999)
    dataset.rescaleI(10.)

    I_data = dataset.getI()
    D_data = dataset.getD()

    ## fit asymptotics
    I0, cXmG = fit_I_asympt(I_data)
    dgamma   = fit_D_asympt(D_data, I0, cXmG)
    #I0, cXmG = fit_I_asympt(I_data, show=True)
    #dgamma   = fit_D_asympt(D_data, I0, cXmG, show=True)

    gamma = dgamma/d
    ## characteristic time for recovery
    tau_r = 1./gamma

    cX = cXmG + gamma

    ## characteristic time for infection
    tau_i = 1./cX

    ### initial conditions
    R0 = 0 ## initial recovered
    S0 = N0 - I0 - R0

    ## days from beginning

    initialValues = []
    params = []

    initialValues.append(S0)
    initialValues.append(I0)
    initialValues.append(R0)

    params.append(tau_i)
    params.append(tau_r)
    params.append(d)

    corona = SIR(initialValues, params)

    corona.print_params()
    corona.simulate()
    corona.print_simulation()

    corona.plot_yields(I_data, D_data, tp, plotData=True, tag='norm')
    corona.plot_yields(I_data, D_data, tp, tmin=0., tmax=50., ymin=0. , ymax=40000., log=False,  plotData=True, tag='zoom')

#_______________________________________________________________________________
if __name__ == "__main__":
    main()
