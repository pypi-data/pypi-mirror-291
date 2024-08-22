from fastapi import FastAPI
from fastapi.responses import JSONResponse
from tradebots.tradebot import TradeBotInput, TradeBotOutput, TradeBot


class TradeBotServer():
    '''
    Wrapper for TradeBot to expose it as a REST API
    '''
    def __init__(self, bot: TradeBot):
        '''
        Args:
        - bot (TradeBot): TradeBot instance
        '''
        self.bot = bot
        self.app = FastAPI()

        # Route for the reset method
        @self.app.post("/reset")
        def reset():
            self.bot.reset()
            return JSONResponse(content={"status": "success", "message": "Bot reset successfully"})

        # Route for the act method
        @self.app.post("/act", response_model=TradeBotOutput)
        def act(input: TradeBotInput):
            output = self.bot.act(input)
            return output

    def listen(self, host: str = "0.0.0.0", port: int = 8000):
        import uvicorn
        uvicorn.run(self.app, host=host, port=port)
