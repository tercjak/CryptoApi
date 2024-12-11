import numpy as np

from crypto_api2.binance_client.BinanceAuth import BinanceAuth
from crypto_api2.binance_client.BinanceFuturesClient import BinanceFuturesClient
from crypto_api2.binance_client.BinanceTrader import BinanceTrader
from crypto_api2.model.models import OrderSide,OrderType, TicketRow
import asyncio
import sys
import os


api_key=os.environ['BINANCE_API_KEY']
api_secret=os.environ['BINANCE_API_SECRET']

#     auth_data=BinanceAuth(api_key,api_secret)

#     client :BinanceFuturesClient = BinanceFuturesClient(
#             auth_data,
#             is_paper_trading=True
#      )
        

#     response= client.place_order( 
#             symbol="BTCUSDT",
#             side=OrderSide.BUY,
#             order_type=OrderType.LIMIT,
#             quantity=0.001,
#             price=45000.0
#     )
#     print(response)
               

def run_test_cases(trader: BinanceTrader):
    # 1. Get the current price for BTCUSDT and ADAUSDT
    print(f"Current prices: {trader.row}")

    def log_hedge(row:TicketRow):
        print(row)
        prices_dict=row.prices
        keys=trader.symbols
        betas=[1,-1]


        order_dict=row.prices.copy()

        sum=0.0

        for i in range(0,len(keys) -1) :
            key=keys[i]
            price=np.log(prices_dict[key])* abs(betas[i])
            order_dict[key]=price
            sum+=price

        
        for i in range(0,len(keys) -1) :
            v=order_dict[key]
            v/=sum
            v= v if betas[i]>1 else -v
            order_dict[key]=v


        print("order_dict")
        print(order_dict)
        return trader.modify_order(order_dict)
    
    def getBetas()->tuple[float,float]:{
         1,-1 
    }
    
    trader.setSingleOnNextUpdate(log_hedge)

    trader.run()
    

auth_data=BinanceAuth(api_key,api_secret)

symbols = ["BTCUSDT", "ADAUSDT"]

trader=BinanceTrader(auth_data,symbols,is_paper_trading=True)

run_test_cases(trader)

