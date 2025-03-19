import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Fetch data from CoinGecko API
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

# Set up Streamlit page
st.set_page_config(layout="wide")
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/6/6f/Bitcoin_Logo.png", width=100)
st.sidebar.title("Crypto Dashboard")
st.sidebar.write("Visualizing cryptocurrency market data.")

# Fetch data
data = get_crypto_data()

# If data is valid, display UI
if data:
    df = pd.DataFrame(data)[["name", "symbol", "current_price", "market_cap", "total_volume"]]
    df.columns = ["Name", "Symbol", "Price (USD)", "Market Cap", "24h Volume"]
    
    # Market Cap Bar Chart
    st.subheader("Market Capitalization of Top 10 Cryptocurrencies")
    top10 = df.head(10)
    fig, ax = plt.subplots()
    ax.barh(top10["Name"], top10["Market Cap"], color="blue")
    ax.set_xlabel("Market Cap (USD)")
    ax.set_ylabel("Cryptocurrency")
    ax.set_title("Top 10 Cryptocurrencies by Market Cap")
    st.pyplot(fig)
    
    # 24h Trading Volume Pie Chart
    st.subheader("24h Trading Volume Distribution")
    fig, ax = plt.subplots()
    ax.pie(top10["24h Volume"], labels=top10["Name"], autopct='%1.1f%%', startangle=90)
    ax.set_title("Top 10 Cryptocurrencies by 24h Volume")
    st.pyplot(fig)
    
else:
    st.error("Unable to fetch data from CoinGecko. Please try again later!")
