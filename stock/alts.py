# Raw Package
import numpy as np
import pandas as pd

## (initial price, number of coins)
coins = dict()

coins['UMX']={
    'ncoins':1355.622,
    'value':3800,
    'marketcap':20e6,
    'nepochs':10,
}

coins['STMX']={
    'ncoins':52466.838,
    'value':3033.31,
    'marketcap':475e6,
    'nepochs':5,
}

coins['SPI']={
    'ncoins':19.511,
    'value':3386.88,
    'marketcap':166e6,
    'nepochs':10,
}

coins['CFI']={
    'ncoins':92.779,
    'value':3837,
    'marketcap':40e6,
    'nepochs':10,
}
coins['CHAIN']={
    'ncoins':6830,
    'value':3800,
    'marketcap':100e6,
    'nepochs':10,
}

coins['ORAI']={
    'ncoins':71.5,
    'value':3445,
    'marketcap':40e6,
    'nepochs':10,
}






for key, val in coins.items():

    if key != 'CFI': continue

    print('---- {} coin ----'.format(key))


    amount_of_coins = val['ncoins']
    price_per_coin = val['value']/val['ncoins']
    portfolio = amount_of_coins*price_per_coin
    print('price/coin: {:.2f} , {:.2f}  coins, {:.0f} $ '.format(price_per_coin, amount_of_coins, portfolio))
    print('')

    #rate = 2  ## double every epoch
    n_epochs = val['nepochs']
    stop_epoch = n_epochs

    marketcap = val['marketcap']
    total_removed_coins = 0
    total_withdrawn = 0
    total_fraction = 0
    sum_of_epochs = float(n_epochs*(n_epochs+1)/2)

    for i in range(1,n_epochs+2):


        if i-1>stop_epoch: break

        multiplier = float(i)
        withdraw_fraction = float(i-1)/sum_of_epochs

        # fraction to withdraw at this stage

        print('    ---------{}-------- epoch '.format(i))
        print('')

        if i>1:
            rate = multiplier/(multiplier-1)
        else:
            rate = 1

        price_per_coin *= rate
        marketcap*= rate
        portfolio = amount_of_coins*price_per_coin

        #print(multiplier, '{:.2f}'.format(rate), '{:.2f}'.format(amount_of_coins), '{:.2f}'.format(portfolio))

        if i>1:
            total_fraction += withdraw_fraction
            removed_coins = withdraw_fraction*amount_of_coins
            total_removed_coins += removed_coins
            amount_of_coins -= removed_coins

            withdrawal = removed_coins*price_per_coin
            total_withdrawn += withdrawal
            portfolio = portfolio - total_withdrawn
            #print('{:.2f}'.format(withdraw_fraction),'{:.2f}'.format(total_fraction),'{:.2f}'.format(withdrawal),'{:.2f}'.format(total_withdrawn), '{:.2f}'.format(portfolio), '{:.2f}'.format(removed_coins))
            print('    price is {:.2f}, now has {}x'.format(price_per_coin,multiplier))
            print('    have to withdraw {:.2f} coins, corresponding to {:.0f} $'.format(removed_coins,withdrawal))
            print('    up to this point, you have removed {:.2f} coins, corresponding to {:.0f} $'.format(total_removed_coins,total_withdrawn))
            print('    you have now {:.2f} coins left, corresponding to {:.0f} $'.format(amount_of_coins,portfolio))
            print('')


    print('    -------------------------------------')
    print ('    market cap      : ', '{:+.2e}'.format(marketcap))
    print ('    total_withdrawn : ', '{:+.2e}'.format(total_withdrawn))
    print ('    total_fraction  : ', '{:+.2e}'.format(total_fraction))
