import MyFunctions as MyFy
import alpaca_trade_api as tradeapi
from config import *

#######################################################################
# My Python Code for DayTrading Using Alpaca
#
# Last Update: 11/11/2021
#######################################################################

# parameters -----------------------------------------------------
symbol = 'TSLA'
Trading = True
#---------------------------------------------------------------------------

# Initiation functions -----------------------------------------------------
api = MyFy.API_connect()
MyFy.Account_Info(api)
MyFy.Portfoli_Info(api)
MyFy.ClearOutput()
#MyFy.order(api,symbol,1,'sell','limit',1099,'day')
#orders = MyFy.list_open_orders(api,symbol)
#MyFy.cancel_orders(api,orders)
#MyFy.SellAll(api,symbol)
#---------------------------------------------------------------------------

# Conneting to socket and start trading ------------------------------------  
if Trading & MyFy.market_is_open(api): 
    conn = tradeapi.stream2.StreamConn(API_KEY, SECRET_KEY, base_url=BASE_URL, 
                                        data_url=WS_URL, data_stream='alpacadatav')

    @conn.on(r'^account_updates$')
    async def on_account_updates(conn, channel, account):
        print('account', account)

    @conn.on(r'^T.{}$'.format(symbol))
    async def trade_info(conn, channel, bar):
        print('-----------------------------------')
        print(f"price: {bar.price} ({bar.size})")  
        MyFy.save_T('trades.txt',bar)   

    @conn.on(r'^Q.{}$'.format(symbol))
    async def trade_info(conn, channel, bar):
        print('-----------------------------------')
        print(f"Ask: {bar.askprice} ({bar.asksize}) | Bid: {bar.bidprice} ({bar.bidsize})")  
        MyFy.save_Q('quotes.txt',bar)


    @conn.on(r'^trade_updates$')
    async def on_trade_updates(conn, channel, trade):
        #print(trade)
        print(f"Trade Event:{trade.event}")         

    @conn.on(r'^AM.{}$'.format(symbol))
    async def on_minute_bars(conn, channel, bar):
        print('-----------------------------------')
        if MyFy.buySignal(bar):
            price = (bar.high + bar.low)/2
            MyFy.BracketOrder(api,symbol,1,'buy','limit',price,'day')    
        
        print(f"High: {bar.high} | Low: {bar.low}")
        MyFy.Cancel_Old_Orders(api,symbol,bar)
        MyFy.save_AM('1min_data.txt',bar)
        MyFy.Portfoli_Info(api)


    #conn.run(['trade_updates','AM.{}'.format(symbol)])
    conn.run(['T.{}'.format(symbol), 'Q.{}'.format(symbol)])

else:
    print("Market is Closed Or Trading Mode is OFF  !")    
# --------------------------------------------------------------------

  

 