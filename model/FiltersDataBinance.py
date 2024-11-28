import json
from pydantic import BaseModel, Field
from typing import List, Union,Dict

# Define a model for each filter type
class PriceFilter(BaseModel):
    filterType: str = Field("PRICE_FILTER")
    maxPrice: float
    minPrice: float
    tickSize: float

class LotSizeFilter(BaseModel):
    filterType: str = Field("LOT_SIZE")
    maxQty: float
    minQty: float
    stepSize: float

class MarketLotSizeFilter(BaseModel):
    filterType: str = Field("MARKET_LOT_SIZE")
    maxQty: float
    minQty: float
    stepSize: float

class MaxNumOrdersFilter(BaseModel):
    filterType: str = Field("MAX_NUM_ORDERS")
    limit: int

class MaxNumAlgoOrdersFilter(BaseModel):
    filterType: str = Field("MAX_NUM_ALGO_ORDERS")
    limit: int

class MinNotionalFilter(BaseModel):
    filterType: str = Field("MIN_NOTIONAL")
    notional: float

class PercentPriceFilter(BaseModel):
    filterType: str = Field("PERCENT_PRICE")
    multiplierUp: float
    multiplierDown: float
    multiplierDecimal: int

# Define a union type for all filter types
FilterUnion = Union[PriceFilter, LotSizeFilter, MarketLotSizeFilter,
                    MaxNumOrdersFilter, MaxNumAlgoOrdersFilter,
                    MinNotionalFilter, PercentPriceFilter]

class FiltersData(BaseModel):
    filters: Dict[str, FilterUnion]

