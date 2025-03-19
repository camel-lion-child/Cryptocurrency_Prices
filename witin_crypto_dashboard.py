
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
        "sparkline": True
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
st.sidebar.image(LOGO_URL, width=90)

# Sidebar with logo and title
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/6/6f/Bitcoin_Logo.png", width=100)
st.sidebar.title("Crypto Dashboard")
st.sidebar.write("Displaying prices of the top 50 cryptocurrencies")

# Fetch data
st.title("Top 50 Cryptocurrency Prices")
data = get_crypto_data()

# If data is valid, display chart and table
if data:
    df = pd.DataFrame(data)[["name", "symbol", "current_price", "market_cap", "total_volume", "sparkline"]]
    df.columns = ["Name", "Symbol", "Price (USD)", "Market Cap", "24h Volume", "Price Trend"]
    
    # Sidebar selection for coin
    selected_coin = st.sidebar.selectbox("Select a cryptocurrency", df["Name"])
    selected_data = df[df["Name"] == selected_coin].iloc[0]
    
    # Display line chart for selected coin
    st.subheader(f"Price Trend for {selected_coin}")
    fig, ax = plt.subplots()
    ax.plot(selected_data["Price Trend"], marker="o", linestyle="-", color="blue")
    ax.set_xlabel("Time")
    ax.set_ylabel("Price (USD)")
    ax.set_title(f"Price Trend of {selected_coin}")
    st.pyplot(fig)
    
    # Display data table
    st.dataframe(df.drop(columns=["Price Trend"]))
else:
    st.error("Unable to fetch data from CoinGecko. Please try again later!")
