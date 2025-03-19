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

# Set up Streamlit interface
st.set_page_config(layout="wide")

# 🎨 Display Logo in Sidebar
LOGO_URL = "https://raw.githubusercontent.com/camel-lion-child/witin_crypto_dashboard/refs/heads/main/witin.png"  # Update with your GitHub raw link
st.sidebar.image(LOGO_URL, width=100)

# Sidebar with logo and title
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/6/6f/Bitcoin_Logo.png", width=100)
st.sidebar.title("Crypto Dashboard")
st.sidebar.write("Displaying prices of the top 50 cryptocurrencies")

# Fetch data
st.title("Top 50 Cryptocurrency Prices")
data = get_crypto_data()

# If data is valid, display chart and table
if data:
    df = pd.DataFrame(data)[["name", "symbol", "current_price", "market_cap", "total_volume"]]
    df.columns = ["Name", "Symbol", "Price (USD)", "Market Cap", "24h Volume"]
    
    # Plot Market Cap chart
    fig, ax = plt.subplots(figsize=(10, 4))
    top10 = df.head(10)  # Select top 10 coins
    ax.barh(top10["Name"], top10["Market Cap"], color="blue")
    ax.set_xlabel("Market Cap (USD)")
    ax.set_ylabel("Cryptocurrency")
    ax.set_title("Top 10 Cryptocurrencies by Market Cap")
    st.pyplot(fig)
    
    # Display data table
    st.dataframe(df)
else:
    st.error("Unable to fetch data from CoinGecko. Please try again later!")
