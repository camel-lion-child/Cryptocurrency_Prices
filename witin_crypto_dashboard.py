import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from datetime import datetime

# 🚀 Page Configuration
st.set_page_config(page_title="WITIN Crypto Dashboard", page_icon="💎", layout="wide")

# 🎨 Display Logo in Sidebar
LOGO_URL = "https://raw.githubusercontent.com/camel-lion-child/witin_crypto_dashboard/refs/heads/main/witin.png"  # Update with your GitHub raw link
st.sidebar.image(LOGO_URL, width=150)

# 📊 Title
st.title("📊 Crypto Price Dashboard (Binance API)")

# 🔥 Binance Cryptocurrency Symbols
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
    "EOS": "EOSUSDT",
    "Aave": "AAVEUSDT",
    "Tezos": "XTZUSDT",
    "The Graph": "GRTUSDT",
    "Fantom": "FTMUSDT",
    "Maker": "MKRUSDT",
    "NEO": "NEOUSDT",
    "Kusama": "KSMUSDT",
    "Dash": "DASHUSDT",
    "Zcash": "ZECUSDT",
    "SushiSwap": "SUSHIUSDT",
    "Curve DAO Token": "CRVUSDT",
    "Compound": "COMPUSDT",
    "Waves": "WAVESUSDT",
    "Chiliz": "CHZUSDT",
    "Hedera": "HBARUSDT",
    "Enjin Coin": "ENJUSDT",
    "Theta Network": "THETAUSDT",
    "Bitcoin Cash": "BCHUSDT",
    "Algorand": "ALGOUSDT",
    "Decentraland": "MANAUSDT",
    "Axie Infinity": "AXSUSDT",
    "Gala": "GALAUSDT",
    "Quant": "QNTUSDT",
    "Celo": "CELOUSDT",
    "Thorchain": "RUNEUSDT",
    "Harmony": "ONEUSDT",
    "Stacks": "STXUSDT",
    "Flow": "FLOWUSDT",
    "Kava": "KAVAUSDT",
    "Helium": "HNTUSDT"
}

# 🎯 Sidebar Selection
crypto = st.sidebar.selectbox("Select Cryptocurrency", list(COINS.keys()))
symbol = COINS[crypto]

# 📡 Fetch Crypto Price Data from Binance
@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_crypto_data(symbol, interval="1d", limit=30):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    response = requests.get(url)

    try:
        data = response.json()

        # Check if API returned valid data
        if isinstance(data, list):
            df = pd.DataFrame(data, columns=[
                "timestamp", "Open", "High", "Low", "Price", "Volume", "CloseTime",
                "QuoteVolume", "Trades", "TakerBuyBase", "TakerBuyQuote", "Ignore"
            ])
            df["Timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
            df["Price"] = df["Price"].astype(float)  # Convert to float for plotting
            return df[["Timestamp", "Price"]]
        else:
            st.error("⚠ Binance API returned an unexpected response.")
            return pd.DataFrame(columns=["Timestamp", "Price"])

    except Exception as e:
        st.error(f"⚠ API Fetch Error: {e}")
        return pd.DataFrame(columns=["Timestamp", "Price"])

# 📊 Fetch and Display Price Chart
data = get_crypto_data(symbol)

if data.empty:
    st.error(f"⚠ No valid data available for {crypto}. API may have failed.")
else:
    st.write(f"### {crypto} Price Trend - Last 30 Days")
    fig = px.line(data, x="Timestamp", y="Price", title=f"{crypto} Price Trend")
    st.plotly_chart(fig)

    # Show Latest Price
    latest_price = data["Price"].iloc[-1]
    st.metric(label=f"Current {crypto} Price", value=f"${latest_price:.2f}")
