import pandas as pd
import numpy as np
#Data viz
import plotly.graph_objs as go
from plotly.subplots import make_subplots


#df = pd.read_csv('data.csv', skipinitialspace=True, usecols=fields)
df = pd.read_csv('data.csv')
# See the keys
#print(df.keys())

#print(df['time'])

df['time'] = pd.to_datetime(df['time'])

print(df.head(40))

#print(df.dtypes)
print(pd.Timestamp('today'))
begin=pd.Timestamp(2020, 1, 16, 3)
df['delta'] = df['time']-begin

print(df.dtypes)


df['time_min'] = df['delta'].apply(lambda x: x/np.timedelta64(1,'m')-527040)
df['deltas'] = df['time_min'].diff()
df['deltas'] = df['time_min'].diff()
df['errx'] = df['time_min'].diff()/2

df['MA'] = df.rolling(window=).mean()

print(df.head(40))


fig = make_subplots()
#fig.add_trace(go.Scatter(x=df.time_min, y=df['deltas'],line=dict(color='blue', width=1.5), name = 'time interval'))
#line=dict(color='blue', width=1.5)

error_x=dict(
            type='data', # value of error bar given in data coordinates
            array=df['errx'],
            thickness=1.5,
            color='blue',
            width=3,
            visible=True)
error_y=dict(
            type='constant', # value of error bar given in data coordinates
            value=0.5,
            thickness=1.5,
            color='blue',
            width=3,
            visible=True)

fig.add_trace(go.Scatter(x=df.time_min, y=df['deltas'],mode='markers',error_x=error_x, error_y=error_y, name = 'time interval'))


# Add titles
fig.update_layout(
    title='',
    yaxis_title='delta t (min)',
    xaxis_title='time (min)',
    yaxis_range=[0,10]
    )

fig.add_shape(type='line',
                x0=0,
                y0=5,
                x1=200,
                y1=5,
                line={'dash': 'dash', 'color': 'green'},
                xref='x',
                yref='y'
)


#Show
fig.show()
# See content in 'star_name'
#print(df.star_name)
