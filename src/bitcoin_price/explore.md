---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.19.6
  kernelspec:
    display_name: bitcoin-price (3.13.x)
    language: python
    name: python3
---

```python
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import requests
import os
import scipy.stats as stats
from dotenv import load_dotenv
from coingecko_sdk import Coingecko
```

```python
from datetime import datetime, timedelta, timezone
import pandas as pd
import os
import numpy as np
from coingecko_sdk import Coingecko



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
        start = now - timedelta(days=(364))

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
        Preprocesses the data by adding log price, price difference, log price difference, price change, and volatility.
        
        Args:
            df (pd.DataFrame): The input DataFrame containing price data.
            
        Returns:
            pd.DataFrame: The DataFrame with added features.
        """
        df["log_price"] = np.log(df["price"])
        df['price_diff'] = df['price'].diff()
        df['log_price_diff'] = df['log_price'].diff()
        df['box_cox'] = stats.boxcox(df['price'])[0]
        df['box_cox_diff'] = df['box_cox'].diff(periods=12)
        df["price_change"] = df["price"].pct_change()
        df["volatility"] = df["price_change"].rolling(window=30).std()
        df = df.drop(columns =["log_price","market_cap","price_diff","box_cox"])
        return df
    def _get_loader(self,df):
        pass
```

```python
data = DataExtractor()._fetch_data()
```

```python
data_processed = DataExtractor()._preprocess_data(data)
data_processed.head()
```

```python
import matplotlib.pyplot as plt


plt.plot(data['price_diff'])
plt.show()
```

```python
#Inspecting Log_transform_price

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


data_processed["log_price"] = np.log(data_processed["price"])
data_processed["log_price"].plot()
plt.show()

```

```python
#Boxcox Transformation

from scipy import stats

data_processed["log_price"] = np.log(data["price"])
data_processed["boxcox_price"], _ = stats.boxcox(data["price"])
plt.plot(data_processed["boxcox_price"])
plt.show()
```

```python
data_processed['log_price_diff'].plot()
```

```python
import seaborn as sns

correlation_matrix = data_processed.corr()

sns.heatmap(correlation_matrix, 
            annot=True,       # Display correlation values
            cmap='coolwarm',  # Color scheme
            vmin=-1, vmax=1,  # Standardize color scale
            center=0)         # Center white at zero

plt.title('Correlation Matrix Heatmap')
plt.show()
```

```python

```
