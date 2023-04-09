from config import *
import websocket, json, requests, os
import numpy as np
import alpaca_trade_api as tradeapi

#######################################################################
# My General python function for DayTrading using Alpaca
#
# Last Update: 11/11/2021
#######################################################################

# globla variables--------------------
Nmin = 4
gain = 0.001
price_stream = np.full(Nmin,10000)

#--------------------------------------


def API_connect():
    api = tradeapi.REST(
        API_KEY,
        SECRET_KEY,
        BASE_URL,
        api_version='v2'
    )
    return api

def Account_Info(api):
    os.system('clear')
    account = api.get_account()
    print(f'Account Status: {account.status}' )
    print(f'Today\'s portfolio balance change: ${float(account.equity) - float(account.last_equity)}')
    print(f'Cash on my account is: ${account.cash}' )
    print(f'My portfolio_value is: ${account.portfolio_value}' )
    clock = api.get_clock()
    print('The market is {}'.format('open!' if clock.is_open else 'closed.'))

def market_is_open(api):    
    clock = api.get_clock()
    return clock.is_open


def Portfoli_Info(api):
    portfolio = api.list_positions()
    if len(portfolio)==0:
        print("No share on your portfolio :(")
    else:    
        print('your porfolio: ')
        for position in portfolio:
            print("{} shares of {}".format(position.qty, position.symbol))
           

def order(api,symbol,qty,side,type,limit_price,time_in_force):   
    api.submit_order(
       symbol=symbol,
       qty=qty,
       side=side,
       type=type,
       limit_price= limit_price,
       time_in_force=time_in_force
    )
    print(f"{qty} share of {symbol} submitted for {side} at ${limit_price} !")
  
def BracketOrder(api,symbol,qty,side,type,limit_price,time_in_force):
    print(f"submiting Bracket Order {symbol} at price: {limit_price}")
    api.submit_order(
        symbol=symbol,
        qty=qty,
        side=side,
        type=type,
        limit_price= limit_price,
        time_in_force= time_in_force,
        order_class='bracket',
        stop_loss={'stop_price': limit_price * (0.95),
                'limit_price':  limit_price * (0.94)},
        take_profit={'limit_price': limit_price * (1+ gain)}
    )
    

def SellAll(api,symbol):
    portfolio = api.list_positions()
    positions = [o for o in portfolio if o.symbol == symbol]
    for pos in positions:
        print(pos)
        api.submit_order(
            symbol=pos.symbol,
            qty=pos.qty,
            side='sell',
            type='market',
            time_in_force='day'
        )
        print(f"{pos.qty} shares of {pos.symbol} submitted for sell")
     
def list_open_orders(api,symbol):
    orders = api.list_orders(
        status='open',
        limit=100,
        nested=True  # show nested multi-leg orders
    )
    open_order = [o for o in orders if o.symbol == symbol]
    print('List of open order IDs: ')
    for o in orders:
        print(o.id)
    return open_order
    
def cancel_orders(api,orders):
    print('List of canceled orders:')
    for o in orders:
        api.cancel_order(o.id)
        print(o.id)
  

def save_AM(name,bar):
    print('save AM to the file!')
    file = open(f"./market_data/{name}",'a')
    file.write(f"\n{bar.timestamp}, {bar.high}, {bar.low}, {bar.open}, {bar.close}")

def save_T(name,bar):
    print('save trades to the file!')
    file = open(f"./market_data/{name}",'a')
    file.write(f"\n{bar.timestamp}, {bar.price}, {bar.size} ")

def save_Q(name,bar):
    print('save quotes to the file!')
    file = open(f"./market_data/{name}",'a')
    file.write(f"\n{bar.timestamp}, {bar.askprice}, {bar.asksize}, {bar.bidprice}, {bar.bidsize}")

def ClearOutput():
    os.system('rm -rf ./market_data/*')



def buySignal(bar):
    global price_stream
    price = (bar.high + bar.low)/2
    price_stream = np.roll(price_stream,-1)
    price_stream[-1] = price
    print('price histoy: ', price_stream)
    buy = True if (price_stream[-1]-price_stream[-2]) > price*gain else False
    return buy

def Cancel_Old_Orders(api,symbol,bar):
    print('Canceling old orders if needed: ')
    price = (bar.high + bar.low)/2
    orders = api.list_orders(
        status='open',
        limit=100,
        nested=True  # show nested multi-leg orders
    )
    open_order = [o for o in orders if o.symbol == symbol]
    for o in open_order:
        if ( (price - float(o.limit_price) ) > price * (4*gain))  and (o.side =='buy'):
             api.cancel_order(o.id)
             print(f"oder ID {o.id} with side:{o.side} at price: {o.limit_price} is canceled" )


   


