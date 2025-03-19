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
        "sparkline": True  # Enable price trend data
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return []

# 🎨 Display Logo in Sidebar
LOGO_URL = "https://raw.githubusercontent.com/camel-lion-child/witin_crypto_dashboard/refs/heads/main/witin.png"  # Update with your GitHub raw link
st.sidebar.image(LOGO_URL, width=80)

# Set up Streamlit page
st.set_page_config(layout="wide")
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/6/6f/Bitcoin_Logo.png", width=100)
st.sidebar.title("Crypto Dashboard")
st.sidebar.write("Select a cryptocurrency to view its price trend.")

# Fetch data
data = get_crypto_data()

# If data is valid, display UI
if data:
    df = pd.DataFrame(data)[["name", "symbol", "current_price", "market_cap", "total_volume", "sparkline_in_7d"]]
    df.columns = ["Name", "Symbol", "Price (USD)", "Market Cap", "24h Volume", "Price Trend"]
    
    # Sidebar selection for a specific cryptocurrency
    selected_coin = st.sidebar.selectbox("Select a cryptocurrency", df["Name"])
    selected_data = df[df["Name"] == selected_coin].iloc[0]
    
    # Display line chart for selected cryptocurrency
    st.subheader(f"7-Day Price Trend for {selected_coin}")
    fig, ax = plt.subplots()
    ax.plot(selected_data["Price Trend"], marker="o", linestyle="-", color="blue")
    ax.set_xlabel("Days")
    ax.set_ylabel("Price (USD)")
    ax.set_title(f"Price Trend of {selected_coin}")
    st.pyplot(fig)
    
    # Display data table
    st.subheader("Top 50 Cryptocurrency Prices")
    st.dataframe(df.drop(columns=["Price Trend"]))
else:
    st.error("Unable to fetch data from CoinGecko. Please try again later!")
