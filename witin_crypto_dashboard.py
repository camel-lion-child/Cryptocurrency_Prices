import streamlit as st
import pandas as pd
from binance.client import Client
import plotly.express as px

# 🚀 Binance API Client (No API Key Required for Price Data)
client = Client()

# 🚀 Page Configuration
st.set_page_config(page_title="WITIN Crypto Dashboard", page_icon="💎", layout="wide")

# 🎨 Display Logo in Sidebar
LOGO_URL = "https://raw.githubusercontent.com/camel-lion-child/witin_crypto_dashboard/refs/heads/main/witin.png"  # Update with your GitHub raw link
st.sidebar.image(LOGO_URL, width=150)

# 📊 Title
st.title("📊 Crypto Price Dashboard (Binance API)")

# 🔥 List of Top Cryptocurrencies Supported by Binance
COINS = {
    "Bitcoin": "BTCUSDT",
    "Ethereum": "ETHUSDT",
    "Binance Coin": "BNBUSDT",
    "Solana": "SOLUSDT",
    "Cardano": "ADAUSDT",
    "XRP": "XRPUSDT",
    "Polkadot": "DOTUSDT",
    "Dogecoin": "DOGEUSDT",
    "Avalanche": "AVAXUSDT",
    "Polygon": "MATICUSDT",
    "Litecoin": "LTCUSDT",
    "Chainlink": "LINKUSDT",
    "Stellar": "XLMUSDT",
    "Cosmos": "ATOMUSDT",
    "Uniswap": "UNIUSDT",
    "VeChain": "VETUSDT",
    "Tron": "TRXUSDT",
    "Filecoin": "FILUSDT",
    "Monero": "XMRUSDT",
    "EOS": "EOSUSDT"
}

# 🎯 Sidebar Selection
crypto = st.sidebar.selectbox("Select Cryptocurrency", list(COINS.keys()))
symbol = COINS[crypto]

# 📡 Fetch Historical Data from Binance API
@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_crypto_data(symbol, interval='1d', limit=30):
    klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)

    df = pd.DataFrame(klines, columns=[
        "Timestamp", "Open", "High", "Low", "Close", "Volume", 
        "Close_time", "Quote_asset_volume", "Trades", 
        "Taker_buy_base_vol", "Taker_buy_quote_vol", "Ignore"
    ])
    
    # Convert timestamp to readable date
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='ms')
    df['Close'] = pd.to_numeric(df['Close'])
    
    return df[['Timestamp', 'Close']]

# 📊 Fetch and Display Price Chart
data = get_crypto_data(symbol)

if data.empty:
    st.error(f"⚠ No valid data available for {crypto}. API may have failed.")
else:
    st.write(f"### {crypto} Price Trend - Last 30 Days")
    fig = px.line(data, x="Timestamp", y="Close", title=f"{crypto} Price Trend")
    st.plotly_chart(fig)

    # Show Latest Price
    latest_price = data['Close'].iloc[-1]
    st.metric(label=f"Current {crypto} Price", value=f"${latest_price:.2f}")
