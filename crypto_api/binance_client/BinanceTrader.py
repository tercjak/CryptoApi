import json
from typing import Callable, Dict, List, Optional

from pydantic import BaseModel
from binance_client import BinanceAuth
from binance_client.BinanceFuturesClient import BinanceFuturesClient

from binance_client.BinanceWSClient import BinanceWSClient
from model.models import MarketDataItem, TicketRow,OrderType,OrderSide


class BinanceTrader() :
    rest_client:BinanceFuturesClient
    ws_client:BinanceWSClient
    markets_limits:Dict[str,MarketDataItem]
    symbols:List[str]
    row: Optional[TicketRow]=None 
    singleOnNextUpdate:Optional[Callable[[TicketRow], None]]=None
    portfolio_value=0.0
    history_portfolio=list()

    def __init__(self, auth_data:BinanceAuth,symbols: List[str],is_paper_trading=True,singleOnNextUpdate=None):
        self.rest_client = BinanceFuturesClient(auth_data,is_paper_trading)
        self.symbols=symbols

        self.singleOnNextUpdate=singleOnNextUpdate
        self.active_orders: Dict[str, float] = {}

        self.ws_client = BinanceWSClient(symbols, self.on_price_update)

    def getMarketInfoDict(self)->Dict[str,any] :
        content=self.rest_client.exchangeInfo().content
        data = json.loads(content)
        _e_info = data["symbols"]
        e_info_dict= {item["symbol"]: item for item in _e_info}
        return e_info_dict
    
    def on_price_update(self, row: TicketRow):

    
        if  self.singleOnNextUpdate is not None:
            self.singleOnNextUpdate(row)
        self.row=row
        # print(f"Price update: {row.model_dump()}")
        self.update_portfolio_value(row.prices)


    def setSingleOnNextUpdate(self,callback:Callable[[TicketRow], None]):
        # print('setSingleOnNextUpdate')
        self.singleOnNextUpdate=callback

    def update_portfolio_value(self, prices: Dict[str, float]):
        # for symbol, quantity in self.active_orders.items():
        #     print(f"## TOTAL ORDER {symbol} {quantity}")

        self.portfolio_value = sum(
            prices[symbol] * abs(quantity) for symbol, quantity in self.active_orders.items()
        )
        self.history_portfolio.append(  self.portfolio_value)

        # print(f"## TOTAL ORDER portfolio_value {self.portfolio_value }")


        # print('self.portfolio_value')
        # print(self.portfolio_value)

    def modify_order(self, target_portfolio_allocation: Dict[str, float]) -> None:

        for symbol, weight in target_portfolio_allocation.items():
            current_weight = self.active_orders.get(symbol, 0)
            weight_change = weight - current_weight
            if weight_change != 0:
                dollar_change = self._calculate_dollar_change(weight_change)
                self._place_order(symbol, dollar_change)
            self.active_orders[symbol] =  weight 

    def _calculate_dollar_change(self, weight_change: float) -> float:
        total_portfolio_value = self.portfolio_value
        return weight_change * total_portfolio_value

    def _place_order(self, symbol: str, dollar_amount: float) -> None:
        side = OrderSide.BUY if dollar_amount > 0 else OrderSide.SELL
        abs_amount = abs(dollar_amount)

        quantity = self._calculate_quantity(symbol, abs_amount)
        # print(f"## PLACED ORDER {side} {symbol} {quantity}")
        try:
            self.rest_client.place_order(
                symbol=symbol,
                side=side,
                order_type=OrderType.MARKET,
                quantity=quantity
            )
        except Exception as e:
            print(f"Error placing order for {symbol}: {e}")

    def _calculate_quantity(self, symbol: str, dollar_amount: float) -> float:
        price = float(self.ws_client.last_prices[symbol])

        quantity= dollar_amount / price
        return quantity
    
    def run(self):
        self.ws_client.run()
