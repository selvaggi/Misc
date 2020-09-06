annual_return_investment = 0.10
annual_appreciation = 0.02
inflation_rate = 0.05
cost_rent = 700.

r = 0.0096 ## 20 anni
time = 25

### FIXME includere tasse compravendita

house_prize = 214222.
## transaction cost if sell (percentage)

available_cash = 150000.


### FIXME
buy_transaction_rate = 0.02
buy_transaction_rate = 0.0
sell_transaction_rate = 0.05
purchase_prize = house_prize*(1. + buy_transaction_rate)

#down_payment_fracs = [1.e-10, 0.1, 0.2, 0.3, 0.4, 0.5]
down_payment_fracs = [1.e-10, 0.2, 0.5, 0.99999]

pvs = dict()


for down_payment_frac in down_payment_fracs:

    down_payment = purchase_prize * down_payment_frac

    ## FIXME
    assicurazione_mensile = purchase_prize *(1. - down_payment_frac)/5000.
    assicurazione_mensile = 0.

    ## interest rate
    # BNP20

    total_debt = purchase_prize - down_payment

    ## monthly morgage payment  P*(1-r/12)/(1-r/12)
    monthly_mortgage = (total_debt)*(1.-1./(1.+r/12.))/(1.-1./(1+r/12.)**(time*12.+1.))
    #monthly_mortgage += assicurazione_mensile

    c = r/12.
    n = time*12
    #monthly_mortgage =  total_debt*(c* (1 + c)**n) / ((1+c)**n - 1)

    #taxe fonciere a t=0
    property_tax = 815

    ## riparazioni
    annual_maintenance = 2000

    ## assicurazione 15*12
    annual_insurance = 180

    ## condominio + lavori straordianri comuni
    annual_dues = 2000

    ## marginal tax income rate (fraction of income)
    marginal_tax_income_rate = 0.

    ## inflation

    print 'Simulation parameters:'
    print '---------------------------------------------------'
    print 'Home prize:', house_prize
    print 'Purchase prize:', purchase_prize
    print 'Down payment:', down_payment
    print 'Loan:', total_debt
    print 'Interest rate:', r
    print 'Mortgage time (yrs):', time
    #print 'Monthly mortgage: {:.0f}'.format(monthly_mortgage-assicurazione_mensile)
    print 'Monthly mortgage (with insurance): {:.0f}'.format(monthly_mortgage)
    #print 'Property tax rate:', taux_abattement
    print 'Annual maintenance (/yr):', annual_maintenance
    print 'Annual dues (/yr):', annual_dues
    print 'Annual appreciation (frac.):', annual_appreciation
    print 'Inflation rate:',inflation_rate
    print 'Sell transaction rate (frac):',sell_transaction_rate
    print '---------------------------------------------------'
    print 'Annual private investment rate:', annual_return_investment
    print ''
    print ''
    print ''
    print ''

    print "{0:>7s} {1:>10s} {2:>10s} {3:>10s} {4:>13s} {5:>16s} {6:>20s} {7:>20s}".format("year", "home value", "debt", "equity fraction", "equity", "saving", "investment", "total (PV)")
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
    home_equity = home_value - debt
    insurance_payment = annual_insurance/12.
    housing_due = annual_dues/12.
    maintenance = annual_maintenance/12.
    property_tax = property_tax/12.
    saving = 0.
    saving = down_payment    #property_tax = property_tax_rate/12.
    lost_if_would_invested = 0.
    owned_fraction = home_equity/home_value
    invested = available_cash - down_payment

    sell_transaction_cost = home_value * sell_transaction_rate
    net_cash = home_equity - sell_transaction_cost
    pv_own_vs_rent = net_cash - saving
    net_cash2 = owned_fraction*(home_value-house_prize)
    #pv_own_vs_rent = net_cash2 - saving + (purchase_prize - down_payment)
    pv_own_vs_rent = (invested + down_payment)
    pv_own_vs_rent = (net_cash - saving)

    rent = cost_rent

    print "{0:5.0f} {1:12.0f} {2:11.0f} {3:8.3f} {4:11.0f} {5:20.0f} {6:20.0f} {7:20.0f}".format(
                  0, house_prize, debt, owned_fraction, home_equity, saving, invested, pv_own_vs_rent
                )
    home_values               .append(home_value)
    debts                     .append(debt)
    home_equities             .append(home_equity)
    insurance_payments        .append(insurance_payment)
    housing_dues              .append(housing_due)
    maintenance_dues          .append(maintenance)
    property_taxes            .append(property_tax)
    savings                   .append(saving)
    presentvalues_own_vs_rent .append(pv_own_vs_rent)

    for m in range(1,months+1):

        invested *= (1+annual_return_investment/12.)
        home_value *= (1+annual_appreciation/12.)
        interest_on_debt = (debt*r/12.)
        paid_principal = monthly_mortgage - interest_on_debt
        debt = debt - paid_principal
        home_equity = home_value - debt
        #property_tax = home_value*property_tax_rate/12.
        property_tax *= (1+annual_appreciation/12.)
        rent = cost_rent
        ## FIXME (does this apply ?)
        income_tax_saving = (interest_on_debt + property_tax)*marginal_tax_income_rate

        owned_fraction = home_equity/home_value


        if m > 1:
            insurance_payment *= (1.+ inflation_rate/12.)
            housing_due *= (1.+ inflation_rate/12.)
            maintenance *= (1.+ inflation_rate/12.)
            property_tax *= (1.+ inflation_rate/12.)
            income_tax_saving *= (1.+ inflation_rate/12.)
        rent *= (1.+inflation_rate/12.)
        #total_cash_out = monthly_mortgage + assicurazione_mensile + insurance_payment + housing_due + maintenance + property_tax - income_tax_saving
        total_cash_out = monthly_mortgage + assicurazione_mensile + insurance_payment + housing_due + maintenance + property_tax - income_tax_saving
        #total_cash_out = monthly_mortgage + assicurazione_mensile - rent

        ## if sell here transaction cost
        sell_transaction_cost = home_value*sell_transaction_rate
        net_cash = home_equity - sell_transaction_cost

        net_cash2 = owned_fraction*home_value

        lost_if_would_invested = total_cash_out


        ### if had not bought house and invested all down payment money
        saving = saving*(1. + annual_return_investment/12.) + total_cash_out - rent

        #saving += total_cash_out


        #print monthly_mortgage, insurance_payment , housing_due , maintenance , property_tax , income_tax_saving

        #print total_cash_out, saving, net_cash

        ## present value of owning vs renting
        #pv_own_vs_rent = (net_cash + saving)/(1.+inflation_rate/12.)**m - total_cash_out
        #pv_own_vs_rent = (net_cash + saving)/(1.+inflation_rate/12.)**m
        #pv_own_vs_rent = (net_cash - saving)/(1.+inflation_rate/12.)**m
        #pv_own_vs_rent = (net_cash - saving)
        pv_own_vs_rent = (invested + net_cash2 - saving)/(1.+inflation_rate/12.)**m
        #pv_own_vs_rent = (invested + net_cash2 - saving)
        #print invested, net_cash2, total_cash_out, saving, pv_own_vs_rent
        pv_own_vs_rent = (net_cash - saving)/(1+inflation_rate/12.)**m

        #print m, home_value, debt, home_equity, insurance_payment, housing_due, maintenance, property_tax, total_cash_out, rent, saving, pv_own_vs_rent

        if m%12 == 0:
            #print float(m)/12, home_value, debt, home_equity, insurance_payment, housing_due, maintenance, property_tax, total_cash_out, rent, saving, pv_own_vs_rent
            print "{0:5.0f} {1:12.0f} {2:11.0f} {3:8.3f} {4:11.0f} {5:20.0f} {6:20.0f} {7:20.0f} ".format(
                  float(m)/12, home_value, debt,  owned_fraction, home_equity, saving, invested, pv_own_vs_rent
                )


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

    pvs[down_payment_frac] = presentvalues_own_vs_rent

import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(7, 5))

for down_payment_frac in down_payment_fracs:

    nd = len(pvs[down_payment_frac])
    ax.plot(pvs[down_payment_frac], label='{:.1f}'.format(down_payment_frac), linewidth=2)


ax.legend(loc='best')

fig.tight_layout()
fig.savefig('plots/delta.png')
