from typing import Final

BINANCE_URLS: Final = {
    "production": "https://fapi.binance.com",
    "testnet": "https://testnet.binancefuture.com"
}

BINANCE_WS_URLS: Final = {
    "production": "wss://fstream.binance.com",
    "testnet": "wss://stream.binancefuture.com"
}


def get_binance_base_url(is_paper_trading:bool):
        base_url = (
            BINANCE_URLS["testnet"]
            if is_paper_trading
            else BINANCE_URLS["production"]
        )
        
