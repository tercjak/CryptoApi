import time
from typing import Annotated, Final, Optional, List, Dict, Any

import requests

from crypto_api2.binance_client import BinanceAuth
from crypto_api2.model.models import OrderSide, OrderType, TimeInForce


BINANCE_URLS: Final = {
    "production": "https://fapi.binance.com",
    "testnet": "https://testnet.binancefuture.com",
}

BINANCE_WS_URLS: Final = {
    "production": "wss://fstream.binance.com",
    "testnet": "wss://stream.binancefuture.com",
}


class BinanceFuturesClient:
    def __init__(
        self,
        auth_data:BinanceAuth,
        is_paper_trading: bool = True,
    ):
        self.auth = auth_data
        self.is_paper_trading = is_paper_trading
        self.base_url = (
            BINANCE_URLS["testnet"] if is_paper_trading else BINANCE_URLS["production"]
        )
        self.api_key = auth_data.api_key

    def place_order(
        self,
        symbol: str,
        side: OrderSide,
        order_type: OrderType,
        quantity: float,
        price: Optional[float] = None,
        timeInForce: TimeInForce = TimeInForce.GTC,
    ) -> Dict:
        
        params = self.get_params(symbol,
                                    side.value,
                                    order_type.value,
                                    quantity,
                                    price,
                                    timeInForce) 
        auth = self.auth

        payload = auth.prepare_params(params)

        params["signature"] = auth.generate_signature(payload)
        print(params)

        headers = {"X-MBX-APIKEY": self.api_key}

        response = requests.post(
            f"{self.base_url}/fapi/v1/order", headers=headers, params=params
        )
        print(response)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Order placement failed: {response.text}")
        
    def exchangeInfo(self):
        url = f"{self.base_url}/fapi/v1/exchangeInfo"
        payload = {}

        exchange_info = requests.get(url, payload)
        return exchange_info
    
    def get_account_balance(self) -> float:
        params = {
            "timestamp": int(time.time() * 1000),
        }
        auth = self.auth
        payload = auth.prepare_params(params)

        params["signature"] = auth.generate_signature(payload)
        headers = {"X-MBX-APIKEY": self.api_key}

        response = requests.get(
            f"{self.base_url}/fapi/v2/balance", headers=headers, params=params
        )
        # url_path = "/dapi/v1/balance"
        if response.status_code == 200:
            balances = response.json()
            return sum(float(balance["balance"]) for balance in balances)
        else:
            print(params)
            print("headers")
            print(headers)

            raise Exception(f"Failed to get account balance: {response.text}")
        

    def get_params(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: Optional[float] = None,
        timeInForce: TimeInForce = TimeInForce.GTC,
    ) -> str:
        params = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
            "timestamp": int(time.time() * 1000),
        }
        print("params")
        print(f"{params}")

        if price!=None:
            params["price"] = price

        if order_type == OrderType.LIMIT:
            if price is None:
                raise ValueError("Price is required for LIMIT orders")
            params["price"] = price

            # Add Time in Force for LIMIT orders
            params["timeInForce"] = timeInForce.value
            return params

