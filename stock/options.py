import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import pandas as pd



stock_price=370.2
#strike_price=360
#option_price=5.83

position=100000

## compute number of stocks for that given stock price
number_of_stocks=int(position/stock_price)
print(number_of_stocks)

number_of_contracts=int(number_of_stocks/100)+1

number_of_contracts=10


print(number_of_contracts)


datanames = [
'options_feb19.csv',
'options_mar19.csv',
'options_apr19.csv',
'options_jun19.csv',
]

for data in datanames:

    ## read data
    df = pd.read_csv(data,  sep='\s+')
    print(df.head(40))

    fig = go.Figure()


    for index, row in df.iterrows():

        percs=[]
        rois=[]

        if index%3!=0: continue
        strike_price=row['Strike']
        option_price=row['Price']

        print(strike_price, option_price)
        for perc in np.arange(0.0, 1.5, 0.01):
            #print(perc)

            price_at_expiry=stock_price*perc
            position_at_expiry=position*perc

            gain= position_at_expiry - number_of_contracts*100*(option_price) + number_of_contracts*100*(strike_price-price_at_expiry)
            if strike_price-price_at_expiry <0:
                gain= position_at_expiry - number_of_contracts*100*(option_price)

            roi=gain/position-1.0
            #print(position_at_expiry, gain, roi)

            percs.append((perc-1.0)*100)
            rois.append(roi*100)

        fig.add_trace(go.Scatter(x=percs, y=rois,
                        mode='lines',
                        name='{}'.format(strike_price)))


    # Add titles
    fig.update_layout(
        title=data,
        yaxis_title='ROI (%)',
        xaxis_title='variation (%)',
        #yaxis_range=[2.5,4]
        )

    fig.show()
