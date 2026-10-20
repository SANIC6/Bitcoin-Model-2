import pandas as pd
import numpy as np
import logging
import requests
import torch
from torch.utils.data import DataLoader, TensorDataset
from coingecko_sdk import Coingecko
from datetime import datetime, timedelta, timezone
from scipy import stats

from dotenv import load_dotenv
import os

load_dotenv()

#--- Logger set up -------------------------
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
#--------------------------------

class DataExtractor:
    """
        Extracts and processes Bitcoin price data.
        
        Attributes:
            None
    """
    def __init__(self) -> None:
        self.API_KEY  = os.getenv("COINGECKO_API_KEY")
        self.BASE_URL = "https://api.coingecko.com/api/v3"
        self.client = Coingecko(demo_api_key=self.API_KEY, environment="demo")
     
    def _fetch_data(self):
        now = datetime.now(timezone.utc)
        start = now - timedelta(days=364)

        response = self.client.coins.market_chart.get_range(
            "bitcoin",
            vs_currency="usd",
            from_=str(int(start.timestamp())),
            to=str(int(now.timestamp())),
        )

        data = response.model_dump() if hasattr(response, "model_dump") else response

        df = pd.DataFrame(data["prices"], columns=["timestamp", "price"])
        df["market_cap"] = [x[1] for x in data["market_caps"]]
        df["total_volume"] = [x[1] for x in data["total_volumes"]]
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df = df.set_index("timestamp")
        return df
    
    def _preprocess_data(self, df):
        """
        Preprocess the data by adding log price, price difference, price change, and volatility.
        
        Args:
            df (pd.DataFrame): The input DataFrame containing price data.
            
        Returns:
            pd.DataFrame: The DataFrame with added features.
        """
        
        df["log_price"] = np.log(df["price"])
        df['price_diff'] = df['price'].diff()
        df["price_change"] = df["price"].pct_change()
        df["volatility"] = df["price_change"].rolling(window=30).std()
    
        return df
    def _clean_data(self, df):
        pass
    def _get_loaders(self,df):
        pass

