## renting
cost_rent = 1100.
rental_inflation = 0.03
annual_return_investment = 0.05

### FIXME includere tasse compravendita

house_prize = 280000.
## transaction cost if sell (percentage)
#buy_transaction_rate = 0.15
buy_transaction_rate = 0.10
sell_transaction_rate = 0.05

purchase_prize = house_prize*(1. + buy_transaction_rate)

#down_payment_frac = 0.10
down_payment_frac = 0.10
down_payment = purchase_prize * down_payment_frac

## interest rate
# BNP20
r = 0.01 ## 20 anni
time = 25



#BNP25
#r = 0.022
#time = 25

#BNPCHF20
#r =
#time =

#BNPCHF25
#r =
#time =

total_debt = purchase_prize - down_payment

## monthly morgage payment  P*(1-r/12)/(1-r/12)
monthly_mortgage = (total_debt)*(1.-1./(1.+r/12.))/(1.-1./(1+r/12.)**(time*12.+1.))

c = r/12.
n = time*12
#monthly_mortgage =  total_debt*(c* (1 + c)**n) / ((1+c)**n - 1)

## POUR les variables v_ (donner min e max)
taux_abattement = 0.12
#property_tax = cost_rent*12*taux_abattement

## riparazioni
annual_maintenance = 2000

## assicurazione
annual_insurance = 100

## condominio
annual_dues = 1500

## annual appreciation
annual_appreciation = 0.03

## marginal tax income rate (fraction of income)
marginal_tax_income_rate = 0.

## inflation
inflation_rate = 0.02

print 'Simulation parameters:'
print '---------------------------------------------------'
print 'Home prize:', house_prize
print 'Purchase prize:', purchase_prize
print 'Down payment:', down_payment
print 'Loan:', total_debt
print 'Interest rate:', r
print 'Mortgage time (yrs):', time
print 'Monthly mortgage: {:.0f}'.format(monthly_mortgage)
print 'Property tax rate:', taux_abattement
print 'Annual maintenance (/yr):', annual_maintenance
print 'Annual dues (/yr):', annual_dues
print 'Annual appreciation (frac.):', annual_appreciation
print 'Inflation rate:',inflation_rate
print 'Inflation rate (rents):',rental_inflation
print 'Buy transaction rate (frac):',buy_transaction_rate
print 'Sell transaction rate (frac):',sell_transaction_rate
print '---------------------------------------------------'
print 'Rent (/month):', cost_rent
print 'Rental Inflation (frac.):',rental_inflation
print 'Annual private investment rate:', annual_return_investment
print ''
print ''
print ''
print ''

print "{0:>7s} {1:>10s} {2:>10s} {3:>10s} {4:>10s} {5:>25s} {6:>25s} {7:>25s}".format("year", "value", "debt", "equity", "saving", "PV (own vs. rent)", "equiv. ROI (savings)", "equiv. ROI (equity)")
print"--------------------------------------------------------------------------------------------------------------"

home_values                = []
debts                      = []
home_equities              = []
interests_on_debt          = []
mortgages_payment          = []
paid_principals            = []
insurance_payments         = []
housing_dues               = []
maintenance_dues           = []
property_taxes             = []
income_tax_savings         = []
total_cash_outs            = []
net_cashes                 = []
savings                    = []
presentvalues_own_vs_rent  = []
net_monthly_deltas         = []

months = 12*time

home_value = house_prize
debt = total_debt
insurance_payment = annual_insurance/12.
housing_due = annual_dues/12.
maintenance = annual_maintenance/12.
saving = down_payment
#property_tax = property_tax_rate/12.
rent = cost_rent

saving0 = down_payment

for m in range(1,months+1):

    home_value *= (1+annual_appreciation/12.)
    interest_on_debt = (debt*r/12.)
    paid_principal = monthly_mortgage - interest_on_debt
    debt = debt - paid_principal
    home_equity = home_value - debt
    #property_tax = home_value*property_tax_rate/12.
    property_tax = cost_rent*taux_abattement

    ## FIXME (does this apply ?)
    income_tax_saving = (interest_on_debt + property_tax)*marginal_tax_income_rate

    if m > 1:
        insurance_payment *= (1.+ inflation_rate/12.)
        housing_due *= (1.+ inflation_rate/12.)
        maintenance *= (1.+ inflation_rate/12.)

    total_cash_out = monthly_mortgage + insurance_payment + housing_due + maintenance + property_tax - income_tax_saving

    rent *= (1.+rental_inflation/12.)

    ## if sell here transaction cost
    sell_transaction_cost = home_value*sell_transaction_rate
    net_cash = home_equity - sell_transaction_cost

    #print saving, total_cash_out, rent

    ### if had not bought house and invested all down payment money
    saving = saving*(1. + annual_return_investment/12.) + total_cash_out - rent

    net_delta = rent - total_cash_out

    ##
    #monthly_roi = (net_delta + home_value *annual_appreciation/12.)
    #print monthly_roi


    ## present value of owning vs renting
    pv_own_vs_rent = (net_cash - saving)/(1+inflation_rate/12.)**m
    #pv_own_vs_rent = (net_cash - saving)

    ## equivalent ROI
    roi_savings = -999
    if saving>0:
        roi_savings = ((saving/saving0)**(1./m) - 1.)*12

    net_investment = (net_cash-total_cash_out+rent)
    roi_equity = -999
    if net_investment > 0:
        roi_equity = ((net_investment/saving0)**(1./m) - 1.)*12



    #print m, home_value, debt, home_equity, insurance_payment, housing_due, maintenance, property_tax, total_cash_out, rent, saving, pv_own_vs_rent


    if m%12 == 0:
        #print float(m)/12, home_value, debt, home_equity, insurance_payment, housing_due, maintenance, property_tax, total_cash_out, rent, saving, pv_own_vs_rent
        print "{0:5.0f} {1:12.0f} {2:11.0f} {3:8.0f} {4:11.0f} {5:20.0f} {6:20.3f} {7:20.3f} ".format(
              float(m)/12, home_value, debt, home_equity, saving, pv_own_vs_rent,roi_savings,roi_equity
            )


    '''
    print "{0:5.0f} {1:12.0f} {2:11.0f} {3:8.0f} {4:11.0f} {5:12.0f} ".format(
          float(m), home_value, debt, home_equity, saving, pv_own_vs_rent
        )
    '''
    home_values               .append(home_value)
    debts                     .append(debt)
    home_equities             .append(home_equity)
    interests_on_debt         .append(interest_on_debt)
    paid_principals           .append(paid_principal)
    insurance_payments        .append(insurance_payment)
    housing_dues              .append(housing_due)
    maintenance_dues          .append(maintenance)
    property_taxes            .append(property_tax)
    income_tax_savings        .append(income_tax_saving)
    total_cash_outs           .append(total_cash_out)
    net_cashes                .append(net_cash)
    savings                   .append(saving)
    presentvalues_own_vs_rent .append(pv_own_vs_rent)
    net_monthly_deltas        .append(net_delta)



import matplotlib.pyplot as plt
plt.plot(presentvalues_own_vs_rent)
plt.ylabel('some numbers')

plt.plot()
plt.savefig('plots/delta.png')
