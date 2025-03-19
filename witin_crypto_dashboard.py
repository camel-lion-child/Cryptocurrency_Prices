import requests
import pandas as pd

url = "https://api.coingecko.com/api/v3/coins/markets"
params = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": 50,
    "page": 1,
    "sparkline": False
}

response = requests.get(url, params=params)
data = response.json()

# Chuyển dữ liệu thành DataFrame
df = pd.DataFrame(data)[["name", "symbol", "current_price", "market_cap", "total_volume"]]

# Hiển thị dữ liệu
print(df)
