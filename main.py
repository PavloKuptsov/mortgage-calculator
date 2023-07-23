def format_sum(amount, is_perc=False, is_int=False):
    suffix = '%' if is_perc else ''
    res = f'{amount}' if is_int else f'{amount:,.2f}'
    res = f'{res}{suffix}'
    tab = ' ' * (20 - len(res))
    return f'{res}{tab}'


def apply_fee(amount, fee):
    return amount * fee / 100


def calc_monthly(sum_credit, credit_term, rate):
    rate_m = rate / 100 / 12 * 365 / 360
    response = (sum_credit * rate_m * ((1 + rate_m) ** credit_term)) / ((1 + rate_m) ** credit_term - 1)
    return response


def calc_credit_total(price, initial_payment, credit_term, monthly):
    commission = 1.0
    sum_credit = price - initial_payment
    total = monthly * credit_term + \
        sum_credit * (commission / 100)
    return total


def calc_insurance(price, initial_payment, credit_term):
    real_estate_insurance_rate = 0.5
    life_insurance_rate = 0.5
    sum_credit = price - initial_payment
    real_estate_ensurance_sum = price * (real_estate_insurance_rate / 100) * (credit_term / 12)
    life_insurance_sum = sum_credit * (life_insurance_rate / 100) * (credit_term / 12)
    return real_estate_ensurance_sum + life_insurance_sum


def calc_taxes(price):
    pension_fund_rate = 1.0
    state_fee_rate = 1.0
    war_fee_rate = 1.5
    return apply_fee(price, pension_fund_rate) + apply_fee(price, state_fee_rate) + apply_fee(price, war_fee_rate)


def calc_misc_fees(initial_payment):
    notarial = 12000
    appraiser = 3500
    bank_commissions = 0.2
    return appraiser + notarial + apply_fee(initial_payment, bank_commissions)


def calc_rate(credit_term, first_year_rate, later_rate):
    years = credit_term / 12
    return (first_year_rate + later_rate * (years - 1)) / years


def calculate(exchange_rate, price_usd, initial_payment_usd, first_year_rate, later_rate, rent_usd, credit_terms):
    price = int(price_usd * exchange_rate)
    initial_payment = int(initial_payment_usd * exchange_rate)
    rent = int(rent_usd * exchange_rate)
    sum_credit = price - initial_payment

    str_credit_terms = ''
    str_rates = ''
    str_monthlies = ''
    str_credit_totals = ''
    str_insurance = ''
    str_taxes = ''
    str_misc_fees = ''
    str_rent_savings = ''
    str_credit_overpays = ''
    str_overpay_vs_rents = ''
    str_real_overpay_rates = ''
    str_totals = ''

    for months in credit_terms:
        rate = calc_rate(months, first_year_rate, later_rate)
        monthly = calc_monthly(sum_credit, months, rate)
        credit_total = calc_credit_total(price, initial_payment, months, monthly)
        insurance = calc_insurance(price, initial_payment, months)
        taxes = calc_taxes(price)
        misc_fees = calc_misc_fees(initial_payment)

        rent_saving = rent * months
        credit_overpay = credit_total - sum_credit + insurance
        overpay_vs_rent = credit_overpay - rent_saving
        real_overpay_rate = (((initial_payment + credit_total) / price) - 1) * 100
        total = initial_payment + credit_total + taxes + misc_fees

        str_credit_terms += format_sum(months, is_int=True)
        str_rates += format_sum(rate, is_perc=True)
        str_monthlies += format_sum(monthly)
        str_credit_totals += format_sum(credit_total)
        str_insurance += format_sum(insurance)
        str_taxes += format_sum(taxes)
        str_misc_fees += format_sum(misc_fees)
        str_rent_savings += format_sum(rent_saving)
        str_credit_overpays += format_sum(credit_overpay)
        str_overpay_vs_rents += format_sum(overpay_vs_rent)
        str_real_overpay_rates += format_sum(real_overpay_rate, is_perc=True)
        str_totals += format_sum(total)

    print('Initial data')
    print('  Exchange rate:       ', format_sum(exchange_rate))
    print('  Price, USD:          ', format_sum(price_usd))
    print('  Price, UAH:          ', format_sum(price))
    print('  Initial payment, USD:', format_sum(initial_payment_usd))
    print('  Initial payment, UAH:', format_sum(initial_payment))
    print('  First year rate:     ', format_sum(first_year_rate))
    print('  Later rate:          ', format_sum(later_rate))
    print('  Months:              ', str_credit_terms)
    print('\nResults')
    print('  Monthly:             ', str_monthlies)
    print('  Total credit cost:   ', str_credit_totals)
    print('  Insurance:           ', str_insurance)
    print('  Credit overpay:      ', str_credit_overpays)
    print('  Rent saving:         ', str_rent_savings)
    print('  Overpay vs rent:     ', str_overpay_vs_rents)
    print('  Avg yearly rate:     ', str_rates)
    print('  Overpay percent:     ', str_real_overpay_rates)
    print('  Taxes:               ', str_taxes)
    print('  Misc fees            ', str_misc_fees)
    print('  Total cost:          ', str_totals)


if __name__ == '__main__':
    exchange_rate = 37.25
    price_usd = 150000
    initial_payment_usd = 110000
    first_year_rate = 12
    later_rate = 19.29
    rent_usd = 600
    credit_terms = [12, 24, 36, 48, 60]

    calculate(exchange_rate, price_usd, initial_payment_usd, first_year_rate, later_rate, rent_usd, credit_terms)
