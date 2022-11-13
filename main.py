from pycoingecko import CoinGeckoAPI
import menu3
from datetime import datetime
import plotly.graph_objects as go


def dca_investments(initial, dca, freq):
    bi_week = 14
    month = 30
    day = 1
    owned_amount = [initial / price_data[0]]
    value = [initial]

    for price in price_data:
        if freq == frequency[0]:
            owned_amount.append(owned_amount[-1] + dca / price)
            value.append(owned_amount[-1] * price)
            print(value[-1])

        elif freq == frequency[1]:
            if day != bi_week:
                value.append(owned_amount[-1] * price)
                day += 1
            elif day == bi_week:
                owned_amount.append(owned_amount[-1] + dca / price)
                value.append(owned_amount[-1] * price)
                day = 1
        elif freq == frequency[2]:
            if day != month:
                value.append(owned_amount[-1] * price)
                day += 1
            elif day == month:
                owned_amount.append(owned_amount[-1] + dca / price)
                value.append(owned_amount[-1] * price)
                day = 1

    value.pop(0)
    owned_amount.pop(0)
    #print(value)
    #print(owned_amount)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=date_data, y=value, mode='lines', name='lines'))
    fig.update_yaxes(title_text='Investment Value',title=dict(text= 'Investment'))
    fig.update_xaxes(title_text = 'Date', calendar='gregorian',title=dict(text= 'Date'))
    fig.show()


def price_plot(id, currency):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=date_data, y=price_data,
                             mode='lines',
                             name='lines'))
    fig.show()


menu = menu3.Menu(True)
cg = CoinGeckoAPI()

# Coin IDs
coin_list = [id['id'] for id in cg.get_coins_list()]
# currency list
currency_list = cg.get_supported_vs_currencies()
# Frequency List
frequency = ['D', 'BW', 'M']

# Menu for the coin Ids
start_menu = menu.menu('Please Pick One: ', coin_list, "Please Press 'q' to quit now!")
currency_menu = menu.menu('Please Pick One:', currency_list)
# Data retrieval ----> change the ending of data "'max'" to specified number of days or 'max'
data = cg.get_coin_market_chart_by_id(coin_list[start_menu - 1], currency_list[currency_menu - 1], 'max')
price_data = [line[1] for line in data['prices']]
date_data = [datetime.utcfromtimestamp(line[0] / 1000).strftime('%Y-%m-%d') for line in data['prices']]
# first function
#price_plot(coin_list[start_menu - 1], currency_list[currency_menu - 1])
dca_investments(100,50,'BW')