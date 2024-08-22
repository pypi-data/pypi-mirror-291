from tradebots.tradebot import TradeBotInput, TradeBotOutput, TradeBot
from tradebots.tradebot import DullBot
from tradebots.server import TradeBotServer


app = TradeBotServer(DullBot())
app.listen()