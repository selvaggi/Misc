# Raw Package
import numpy as np
import pandas as pd

## (initial price, number of coins)
coin_price = dict()
coin_price['STMX']=(3033.31,52466.838)
coin_price['SPI']=(3386.88,19.511)
coin_price['CFi']=(3837.53,92.779)
coin_price['UMX']=(3800,1355.622)
coin_price['CHAIN']=(3800,6829.825)

for key, val in coin_price.items():

    if key != 'UMX': continue

    print('---- {} coin ----'.format(key))


    amount_of_coins = val[1]
    price_per_coin = val[0]/val[1]
    portfolio = amount_of_coins*price_per_coin
    print('price/coin: {:.2f} , {:.2f}  coins, {:.0f} $ '.format(price_per_coin, amount_of_coins, portfolio))
    print('')

    #rate = 2  ## double every epoch
    n_epochs = 10
    stop_epoch = n_epochs

    marketcap = 20e6
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
