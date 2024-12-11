from enum import Enum
from typing import Dict, Optional, List
from pydantic import BaseModel, Field

from crypto_api2.model.FiltersDataBinance import LotSizeFilter, PriceFilter


class OrderSide(str, Enum):
    BUY = "BUY"
    SELL = "SELL"

class OrderType(str, Enum):
    LIMIT = "LIMIT"
    MARKET = "MARKET"
    STOP = "STOP"
    TAKE_PROFIT = "TAKE_PROFIT"
    STOP_MARKET = "STOP_MARKET"
    TAKE_PROFIT_MARKET = "TAKE_PROFIT_MARKET"

class TimeInForce(str, Enum):
    GTC = "GTC"  # Good Till Cancel
    IOC = "IOC"  # Immediate or Cancel
    FOK = "FOK"  # Fill or Kill
    GTX = "GTX"  # Good Till Crossing

class OrderRequest(BaseModel):
    symbol: str
    side: OrderSide
    type: OrderType
    quantity: float
    price: Optional[float] = None
    timeInForce: Optional[TimeInForce] = None
    stopPrice: Optional[float] = None
    activationPrice: Optional[float] = None
    callbackRate: Optional[float] = None
    reduceOnly: Optional[bool] = False
    closePosition: Optional[bool] = False
    workingType: str = "CONTRACT_PRICE"
    priceProtect: Optional[bool] = False
    newClientOrderId: Optional[str] = None
    positionSide: Optional[str] = "BOTH"

class AccountBalance(BaseModel):
    asset: str
    balance: str
    crossWalletBalance: str
    crossUnPnl: str
    availableBalance: str
    maxWithdrawAmount: str

class PositionRisk(BaseModel):
    symbol: str
    positionAmt: str
    entryPrice: str
    markPrice: str
    unRealizedProfit: str
    liquidationPrice: str
    leverage: str
    maxNotionalValue: str
    marginType: str
    isolatedMargin: str
    isAutoAddMargin: str
    positionSide: str
    notional: str
    isolatedWallet: str
    updateTime: int

class TicketRow(BaseModel):
    ds: int
    prices: Dict[str, float]


class MarketDataItem(BaseModel):
    pricePrecision: int
    quantityPrecision: int
    priceFilter: PriceFilter
    lotSizeFilter: LotSizeFilter
    minNotational: float