import json
from typing import Callable, List,Dict

import websocket

from crypto_api2.model.models import TicketRow




class BinanceWSClient:
    last_prices :Dict[str,float]

    def __init__(self, symbols: List[str], on_price_update: Callable[[TicketRow], None]):
        self.symbols = symbols
        self.on_price_update = on_price_update
        self.last_prices = {symbol: 0 for symbol in symbols}
        self.base_url = "wss://fstream.binance.com/ws"
        self.base_url_one = "wss://fstream.binance.com/ws"

    def on_message(self, ws, message):
        data = json.loads(message)
        # print("data")
        # print(data)

        if data["e"] == "markPriceUpdate":
            symbol = data["s"]
            price = float(data["p"])
            timestamp = data["E"]
            self.last_prices[symbol] = price
            self.on_price_update(TicketRow(ds=timestamp, prices=self.last_prices))

    def on_error(self, ws, error):
        print(f"WebSocket error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        print(f"WebSocket connection closed: {close_msg}")

    def run(self):
        streams = [f"{symbol.lower()}@markPrice@1s" for symbol in self.symbols]
        ws_url = f"{self.base_url}/{'/'.join(streams)}"
        ws = websocket.WebSocketApp(
            ws_url,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
        )
        ws.run_forever()