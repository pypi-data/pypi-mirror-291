import httpx
from typing import Dict
from tradebots.tradebot import TradeBotInput, TradeBotOutput
from datetime import datetime

class TradeBotInterface:
    '''
    Interface to interact with TradeBotServer via HTTP API
    '''
    def __init__(self, host: str = "0.0.0.0", port: int = 8000):
        '''
        Args:
        - host (str): Host where the TradeBotServer is running
        - port (int): Port where the TradeBotServer is listening
        '''
        self.base_url = f"http://{host}:{port}"

    def reset(self) -> Dict[str, str]:
        '''
        Sends a reset request to the TradeBotServer

        Returns:
        - Dict[str, str]: Response from the server
        '''
        response = httpx.post(f"{self.base_url}/reset")
        response.raise_for_status()  # Raises an exception if the request was unsuccessful
        return response.json()

    def act(self, input: TradeBotInput) -> TradeBotOutput:
        '''
        Sends a request to act on the input data

        Args:
        - input (TradeBotInput): The input data for the TradeBot

        Returns:
        - TradeBotOutput: The output data from the TradeBot
        '''
        if isinstance(input.timestamp, datetime):
            input.timestamp = input.timestamp.isoformat()
        response = httpx.post(f"{self.base_url}/act", json=input.dict())
        response.raise_for_status()  # Raises an exception if the request was unsuccessful
        return TradeBotOutput(**response.json())