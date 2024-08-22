from pydantic import BaseModel
from datetime import datetime
from typing import List
from enum import Enum
from abc import ABC, abstractmethod


class OrderAction(str, Enum):
    BUY = 'BUY'
    SELL = 'SELL'
    HOLD = 'HOLD'


class Stock(BaseModel):
    ticker: str
    open: float
    high: float
    low: float
    close: float


class TradeBotInput(BaseModel):
    stocks: List[Stock]
    timestamp: datetime | str
    platform_id: str


class Order(BaseModel):
    ticker: str
    price: float
    timestamp: datetime | str
    platform_id: str
    action: OrderAction


class TradeBotOutput(BaseModel):
    orders: List[Order]
    timestamp: datetime
    platform_id: str


class TradeBot(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def reset(self):
        '''
        description: reset tradebot to initial state
        '''
        pass

    @abstractmethod
    def act(self, input: TradeBotInput) -> TradeBotOutput:
        '''
        args:
            input: TradeBotInput - input data for tradebot
        returns:
            TradeBotOutput - output data for tradebot
        description: base class for tradebots
        '''
        pass


class DullBot(TradeBot):
    '''
    DullBot - tradebot that buys and sells all stocks in the same timestamp.
    Only for demonstration purposes.
    '''
    def __init__(self):
        super(TradeBot).__init__()
        self.current_order = OrderAction.BUY

    def reset(self):
        self.current_order = OrderAction.BUY

    def act(self, input: TradeBotInput) -> TradeBotOutput:
        orders = []

        if isinstance(input.timestamp, datetime):
            input.timestamp = input.timestamp.isoformat()

        for stock in input.stocks:
            orders.append(Order(ticker=stock.ticker,
                                price=stock.close,
                                timestamp=input.timestamp,
                                platform_id=input.platform_id,
                                action=self.current_order))
        if self.current_order == OrderAction.BUY:
            self.current_order = OrderAction.SELL
        else:
            self.current_order = OrderAction.BUY
        return TradeBotOutput(orders, input.timestamp, input.platform_id)
