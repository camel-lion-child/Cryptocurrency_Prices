import streamlit as st
import requests
import pandas as pd

# Lấy dữ liệu từ CoinGecko API
def get_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 50,
        "page": 1,
        "sparkline": False
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return []

# Chạy ứng dụng Streamlit
st.title("Top 50 Cryptocurrency Prices")

# Lấy dữ liệu
data = get_crypto_data()

# Nếu dữ liệu hợp lệ, hiển thị trong bảng
if data:
    df = pd.DataFrame(data)[["name", "symbol", "current_price", "market_cap", "total_volume"]]
    df.columns = ["Name", "Symbol", "Price (USD)", "Market Cap", "24h Volume"]
    st.dataframe(df)
else:
    st.error("Không thể lấy dữ liệu từ CoinGecko. Hãy thử lại sau!")
