import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px

# 🚀 Page Configuration
st.set_page_config(page_title="WITIN Crypto Dashboard", page_icon="💎", layout="wide")

# 🎨 Display Logo in Sidebar
LOGO_URL = "https://raw.githubusercontent.com/camel-lion-child/witin_crypto_dashboard/refs/heads/main/witin.png"  # Replace with your GitHub raw link
st.sidebar.image(LOGO_URL, width=150)

# 📊 Title
st.title("📊 Crypto Price Dashboard (Yahoo Finance API)")

# 🔥 Yahoo Finance Cryptocurrency Symbols
COINS = {
    "Bitcoin": "BTC-USD",
    "Ethereum": "ETH-USD",
    "Binance Coin": "BNB-USD",
    "Solana": "SOL-USD",
    "Cardano": "ADA-USD",
    "XRP": "XRP-USD",
    "Polkadot": "DOT-USD",
    "Dogecoin": "DOGE-USD",
    "Avalanche": "AVAX-USD",
    "Polygon": "MATIC-USD",
    "Litecoin": "LTC-USD",
    "Chainlink": "LINK-USD",
    "Stellar": "XLM-USD",
    "Cosmos": "ATOM-USD",
    "Uniswap": "UNI-USD",
    "VeChain": "VET-USD",
    "Tron": "TRX-USD",
    "Filecoin": "FIL-USD",
    "Monero": "XMR-USD",
    "EOS": "EOS-USD",
    "Aave": "AAVE-USD",
    "Tezos": "XTZ-USD",
    "The Graph": "GRT-USD",
    "Fantom": "FTM-USD",
    "Maker": "MKR-USD",
    "NEO": "NEO-USD",
    "Kusama": "KSM-USD",
    "Dash": "DASH-USD",
    "Zcash": "ZEC-USD",
    "SushiSwap": "SUSHI-USD",
    "Curve DAO Token": "CRV-USD",
    "Compound": "COMP-USD",
    "Waves": "WAVES-USD",
    "Chiliz": "CHZ-USD",
    "Hedera": "HBAR-USD",
    "Enjin Coin": "ENJ-USD",
    "Theta Network": "THETA-USD",
    "Bitcoin Cash": "BCH-USD",
    "Algorand": "ALGO-USD",
    "Decentraland": "MANA-USD",
    "Axie Infinity": "AXS-USD",
    "Gala": "GALA-USD",
    "Quant": "QNT-USD",
    "Celo": "CELO-USD",
    "Thorchain": "RUNE-USD",
    "Harmony": "ONE-USD",
    "Stacks": "STX-USD",
    "Flow": "FLOW-USD",
    "Kava": "KAVA-USD",
    "Helium": "HNT-USD"
}

# 🎯 Sidebar Selection
crypto = st.sidebar.selectbox("Select Cryptocurrency", list(COINS.keys()))
symbol = COINS[crypto]

# 📡 Fetch Crypto Data from Yahoo Finance
@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_crypto_data(symbol):
    try:
        df = yf.download(symbol, period="30d", interval="1d")  # Get last 30 days of data
        df.reset_index(inplace=True)
        df.rename(columns={"Date": "Timestamp", "Close": "Price"}, inplace=True)
        return df[["Timestamp", "Price"]]
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
