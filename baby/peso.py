import pandas as pd
import numpy as np
#Data viz
import plotly.graph_objs as go
from plotly.subplots import make_subplots

extras=dict()


extras['X']=0.0

## couches
extras['c0']=0.015
extras['c1']=0.018

## bodies
extras['b_orsetto']=0.037
extras['b_stella']=0.042
extras['b_colletto']=0.059

## ghettine
extras['g_strisce']=0.038
extras['g_cuori']=0.038
extras['g_spugna']=0.056
extras['g_rosa']=0.044

## pigiama
extras['p_nuvola']=0.097
extras['p_gatto']=0.106
extras['p_rosa']=0.107
extras['p_stricerosa']=0.100 ## TBC
extras['p_snoopy']=0.097 ## TBC

## maglioni
extras['m_rosa']= 0.063


## read data
df = pd.read_csv('peso.csv', keep_default_na=0)
df_model = pd.read_csv('weights_z0.csv', keep_default_na=0)
print(df_model.head(40))

#df_model['date'] = pd.to_datetime(df_model['days'], unit='day',
              # origin=pd.Timestamp('2021-01-16'))
print(df_model.head(40))


df['ew1'] = df['extra1'].map(extras)
df['ew2'] = df['extra2'].map(extras)
df['ew3'] = df['extra3'].map(extras)
df['ew4'] = df['extra4'].map(extras)

df['peso'] = df['weight']-df['ew1']-df['ew2']-df['ew3']-df['ew4']

## convert absolute time to ndays
df['t0'] = pd.Timestamp(2021, 1, 16, 13)
df['datetime'] = pd.to_datetime(df['date']).dt.tz_localize(None)
df['day'] = (df['datetime'] - df['t0']).apply(lambda x: x/np.timedelta64(1,'D'))

print(df.head(40))
'''
for index, row in df.iterrows():

    percs=[]
    rois=[]

    if index%3!=0: continue
    strike_price=row['Strike']
    option_price=row['Price']
'''

#slope = pd.Series(np.gradient(.values), .index, name='slope')
df_model['slope'] = pd.Series(np.gradient(df_model['weight_kg'], df_model['days']))
#print(df_model.head(40))

#fig = make_subplots()
fig = make_subplots(specs=[[{"secondary_y": True}]])


#fig.add_trace(go.Scatter(x=df.time_min, y=df['deltas'],line=dict(color='blue', width=1.5), name = 'time interval'))
#line=dict(color='blue', width=1.5)

error_y=dict(
            type='percent', # value of error bar given in data coordinates
            value=2.5,
            thickness=1.5,
            color='blue',
            width=3,
            visible=True)


fig.add_trace(go.Scatter(x=df['day'], y=df['peso'], mode='markers',error_y=error_y, name = 'peso'))
fig.add_trace(go.Scatter(x=df_model['days'], y=df_model['weight_kg'], mode='lines', name = 'peso_model'))
fig.add_trace(go.Scatter(x=df_model['days'], y=df_model['slope'], mode='lines', name = 'slope'), secondary_y=True)

# Add titles
fig.update_layout(
    title='',
    yaxis_title='peso (kg)',
    xaxis_title='date (days)',
    xaxis_range=[0,30],
    yaxis_range=[2.5,4]
    )
fig.update_yaxes(title_text="weight (kg)", secondary_y=False)
fig.update_yaxes(title_text="slope (kg/day)", secondary_y=True)


#Show
fig.show()
# See content in 'star_name'
#print(df.star_name)
