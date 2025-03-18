 
import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import yfinance as yf

# Function to fetch crypto price data from CoinGecko API
def get_crypto_data(crypto='bitcoin', days=7):
    url = f"https://api.coingecko.com/api/v3/coins/{crypto}/market_chart?vs_currency=usd&days={days}"
    response = requests.get(url)
    data = response.json()
    prices = data['prices']
    df = pd.DataFrame(prices, columns=['timestamp', 'price'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

# Function to fetch stock-like crypto data from Yahoo Finance
def get_crypto_stock_data(symbol='BTC-USD'):
    df = yf.download(symbol, period='1mo', interval='1d')
    return df

# Streamlit UI
st.title("📈 WITIN Crypto Analytics Dashboard")

# Sidebar: User input
crypto_options = ['Bitcoin', 'Ethereum', 'Binancecoin', 'Solana', 'Cardano']
crypto = st.sidebar.selectbox("Select Cryptocurrency", crypto_options)
days = st.sidebar.slider("Select Days of Data", min_value=1, max_value=90, value=7)

# Fetch and display data
data = get_crypto_data(crypto, days)
st.write(f"### {crypto.capitalize()} Price Trend - Last {days} Days")
fig = px.line(data, x='timestamp', y='price', title=f"{crypto.capitalize()} Price Trend")
st.plotly_chart(fig)

# Show latest price
latest_price = data['price'].iloc[-1]
st.metric(label=f"Current {crypto.capitalize()} Price", value=f"${latest_price:.2f}")

# Yahoo Finance Data for Comparison
st.write("### Stock-Like Crypto Data from Yahoo Finance")
yf_data = get_crypto_stock_data(symbol=f"{crypto.upper()}-USD")
st.dataframe(yf_data.tail())

# Show data preview
st.write("### Data Preview")
st.dataframe(data.head())
