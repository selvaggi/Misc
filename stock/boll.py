# Raw Package
import numpy as np
import pandas as pd

#Data Source
import yfinance as yf

#Data viz
import plotly.graph_objs as go
from plotly.subplots import make_subplots

#-------------------------------------------------------------------------------
'''
def compute_sma(data, ndays):
    for i in range(0,data.shape[0]-ndays):
        #print(i, data.iloc[i,3]) ## this is the 4th column, corresponds to the close

        #data.loc[data.index[i+2],'SMA_3'] = np.round(((data.iloc[i,3]+ data.iloc[i+1,3] +data.iloc[i+2,3])/3),1)
        sma=0.
        for j in range(0,ndays):
            sma+=data.iloc[i+j,3]
        sma=np.round(float(sma)/ndays)
        data.loc[data.index[i+ndays-1],'SMA_{}'.format(ndays)]=sma
        #print(i, sma)
'''
'''
def sma(mylist, N):

    cumsum, moving_aves = [0], []

    for i, x in enumerate(mylist, 1):
        cumsum.append(cumsum[i-1] + x)
        if i>=N:
            moving_ave = (cumsum[i] - cumsum[i-N])/N
            #can do stuff with moving_ave here
            moving_aves.append(moving_ave)
    return moving_aves
'''

def compute_sma(data, ndays):
    for i in range(0,data.shape[0]-ndays):
        #print(i, data.iloc[i,3]) ## this is the 4th column, corresponds to the close

        #data.loc[data.index[i+2],'SMA_3'] = np.round(((data.iloc[i,3]+ data.iloc[i+1,3] +data.iloc[i+2,3])/3),1)
        sma=0.
        for j in range(0,ndays):
            sma+=data.iloc[i+j,3]
        sma=np.round(float(sma)/ndays)
        data.loc[data.index[i+ndays-1],'SMA_{}'.format(ndays)]=sma
        #print(i, sma)



#-------------------------------------------------------------------------------

def compute_risk(data, ndays):
    max_risk = -1.
    for i in range(0,data.shape[0]-ndays):
        #print(i, data.iloc[i,3]) ## this is the 4th column, corresponds to the close

        #data.loc[data.index[i+2],'SMA_3'] = np.round(((data.iloc[i,3]+ data.iloc[i+1,3] +data.iloc[i+2,3])/3),1)
        print(data.iloc[i+ndays-1,6],data.iloc[i+ndays-1,7])
        risk = data.iloc[i+ndays-1,6]/data.iloc[i+ndays-1,7]
        if risk>max_risk:
            max_risk=risk
        data.loc[data.index[i+ndays-1],'risk']=risk


    print(max_risk)
    for i in range(0,data.shape[0]-ndays):
        #print(i, data.iloc[i,3]) ## this is the 4th column, corresponds to the close

        #data.loc[data.index[i+2],'SMA_3'] = np.round(((data.iloc[i,3]+ data.iloc[i+1,3] +data.iloc[i+2,3])/3),1)
        risk = data.iloc[i+ndays-1,8]/max_risk
        data.loc[data.index[i+ndays-1],'risk']=risk



#-------------------------------------------------------------------------------

def plot_security(ticker, ema1, ema2):

    ema_period1 = ema1          # change it to ema_period = 30 for your case
    ema_period2 = ema2            # change it to ema_period = 30 for your case
    tick=ticker

    data = yf.download(tickers=tick, period='max', interval='1d')


    #Draw the middle band, higher band, lowest band
    #data['Middle Band'] = data['Close'].rolling(window=21).mean()
    #data['Upper Band'] = data['Middle Band'] + 1.96*data['Close'].rolling(window=21).std()
    #data['Lower Band'] = data['Middle Band'] - 1.96*data['Close'].rolling(window=21).std()

    #data['50dayMA'] = data['Middle Band'] - 1.96*data['Close'].rolling(window=21).std()


    df = data

    myalpha1 = 2/(ema_period1+1)
    myalpha2 = 2/(ema_period2+1)

    # concise form : df.expanding(min_periods=12).mean()
    df['Expand_Mean1'] = data['Close'].rolling(window=len(df), min_periods=ema_period1).mean()
    # obtain the very first index after nulls
    idx = df['Expand_Mean1'].first_valid_index()
    # Make all the subsequent values after this index equal to NaN
    df.loc[idx:, 'Expand_Mean1'].iloc[1:] = np.NaN
    # Let these rows now take the corresponding values in the Close column
    df.loc[idx:, 'Expand_Mean1'] = df['Expand_Mean1'].combine_first(df['Close'])
    # Perform EMA by turning off adjustment
    df['EMA1'] = df['Expand_Mean1'].ewm(alpha=myalpha1, adjust=False).mean()

    # concise form : df.expanding(min_periods=12).mean()
    df['Expand_Mean2'] = data['Close'].rolling(window=len(df), min_periods=ema_period2).mean()
    # obtain the very first index after nulls
    idx = df['Expand_Mean2'].first_valid_index()
    # Make all the subsequent values after this index equal to NaN
    df.loc[idx:, 'Expand_Mean2'].iloc[1:] = np.NaN
    # Let these rows now take the corresponding values in the Close column
    df.loc[idx:, 'Expand_Mean2'] = df['Expand_Mean2'].combine_first(df['Close'])
    # Perform EMA by turning off adjustment
    df['EMA2'] = df['Expand_Mean2'].ewm(alpha=myalpha2, adjust=False).mean()


    ##


    df['risk'] = df['EMA1'].div(df['EMA2'])
    df['norm. risk'] = df['risk'].div(df['risk'].max())


    data=df

    #print(sma(mylist, N))
    #compute_sma(data, long_period)
    #compute_risk(data, long_period)

    #print(data.head(40))

    #print(data['Middle Band'])


    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    #declare figure

    #fig.add_trace(go.Scatter(x=data.index, y= data['Middle Band'],line=dict(color='blue', width=.7), name = 'Middle Band'))
    #fig.add_trace(go.Scatter(x=data.index, y= data['Upper Band'],line=dict(color='red', width=1.5), name = 'Upper Band (Sell)'))
    #fig.add_trace(go.Scatter(x=data.index, y= data['Lower Band'],line=dict(color='green', width=1.5), name = 'Lower Band (Buy)'))
    #fig.add_trace(go.Scatter(x=data.index, y= data['SMA_50'],line=dict(color='dark blue', width=1.5), name = 'SMA50'))
    #fig.add_trace(go.Scatter(x=data.index, y= data['SMA_350'],line=dict(color='blue', width=1.5), name = 'SMA350'))

    #Candlestick
    fig.add_trace(go.Candlestick(x=data.index,
                    open=data['Open'],
                    high=data['High'],
                    low=data['Low'],
                    close=data['Close'], name = 'market data'),
                    secondary_y=False,
    )

    fig.add_trace(go.Scatter(x=data.index, y= data['norm. risk'],line=dict(color='blue', width=1.5), name = 'risk'), secondary_y=True)


    # Add titles
    fig.update_layout(
        title='{} live share price evolution'.format(tick),
        yaxis_title='Stock Price (USD per Shares)')



    # Set y-axes titles
    fig.update_yaxes(title_text="price", secondary_y=False, type="log")
    #fig.update_yaxes(title_text="price", secondary_y=False)
    fig.update_yaxes(title_text="risk", secondary_y=True)


    print('--------------- ',tick,' ---------------')
    print('  ')
    print(data.tail(10))


    #Show
    fig.show()

coins0 = [
    'BTC-USD',
]

coins1 = [
    'BTC-USD',
    'ETH-USD',
    'LINK-USD',
    'ADA-USD',
    'DOT-USD',
]

coins2 = [
    'BTC-USD',
    'ETH-USD',
    'LINK-USD',
    'ADA-USD',
    'XMR-USD',
    'LTC-USD',
    'XRP-USD',
    'BCH-USD',
    'EOS-USD',
    'ZEC-USD'
]

stocks = [
    'TSLA',
]


for coin in coins1:
    #plot_security(coin, 20, 350)
    plot_security(coin, 20, 350)
