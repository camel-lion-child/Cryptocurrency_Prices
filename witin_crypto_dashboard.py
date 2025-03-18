import subprocess
subprocess.run(["pip", "install", "matplotlib seaborn plotly pandas requests"], shell=True)

import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# 🚀 Page Configuration
st.set_page_config(page_title="WITIN Crypto Dashboard", page_icon="💎", layout="wide")

# 🎨 Display Logo in Sidebar
LOGO_URL = "https://raw.githubusercontent.com/your-username/your-repo/main/witin.png"  # Update with your correct GitHub raw link
st.sidebar.image(LOGO_URL, width=150)

# 📊 Title
st.title("📊 Crypto Analytics Dashboard")

# 🔥 List of 50 important cryptocurrencies
COINS = {
    "Bitcoin": "bitcoin",
    "Ethereum": "ethereum",
    "Binance Coin": "binancecoin",
    "Solana": "solana",
    "Cardano": "cardano",
    "XRP": "ripple",
    "Polkadot": "polkadot",
    "Dogecoin": "dogecoin",
    "Avalanche": "avalanche-2",
    "Polygon": "matic-network",
    "Litecoin": "litecoin",
    "Chainlink": "chainlink",
    "Stellar": "stellar",
    "Cosmos": "cosmos",
    "Uniswap": "uniswap",
    "VeChain": "vechain",
    "Tron": "tron",
    "Filecoin": "filecoin",
    "Monero": "monero",
    "EOS": "eos",
    "Aave": "aave",
    "Tezos": "tezos",
    "The Graph": "the-graph",
    "Fantom": "fantom",
    "Maker": "maker",
    "NEO": "neo",
    "Kusama": "kusama",
    "Dash": "dash",
    "Zcash": "zcash",
    "SushiSwap": "sushi",
    "Curve DAO Token": "curve-dao-token",
    "Compound": "compound",
    "Waves": "waves",
    "Chiliz": "chiliz",
    "Hedera": "hedera-hashgraph",
    "Enjin Coin": "enjincoin",
    "Theta Network": "theta-token",
    "Bitcoin Cash": "bitcoin-cash",
    "Algorand": "algorand",
    "Decentraland": "decentraland",
    "Axie Infinity": "axie-infinity",
    "Gala": "gala",
    "Quant": "quant-network",
    "Celo": "celo",
    "Thorchain": "thorchain",
    "Harmony": "harmony",
    "Stacks": "blockstack",
    "Flow": "flow",
    "Kava": "kava",
    "Helium": "helium"
}

# 🎯 Sidebar Selection
crypto = st.sidebar.selectbox("Select Cryptocurrency", list(COINS.keys()), key="crypto_select")
days = st.sidebar.slider("Select Days of Data", min_value=1, max_value=90, value=7, key="days_slider")

# 📡 Function to Fetch Cryptocurrency Data
@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_crypto_data(crypto_id, days=7):
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart?vs_currency=usd&days={days}"
    response = requests.get(url)
    
    try:
        data = response.json()
    except Exception as e:
        st.error(f"Failed to parse API response: {e}")
        return pd.DataFrame(columns=['Timestamp', 'Price'])

    if 'prices' not in data:
        st.error("⚠ No price data found. API response may be invalid.")
        return pd.DataFrame(columns=['Timestamp', 'Price'])

    prices = data['prices']
    df = pd.DataFrame(prices, columns=['timestamp', 'price'])
    df['Timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.drop(columns=['timestamp'], inplace=True)

    return df

# 📊 Fetch and Display Crypto Price Trend
crypto_id = COINS[crypto]
data = get_crypto_data(crypto_id, days)

if data.empty:
    st.error(f"⚠ No data available for {crypto}. Try another cryptocurrency.")
else:
    st.write(f"### {crypto} Price Trend - Last {days} Days")
    fig = px.line(data, x='Timestamp', y='Price', title=f"{crypto} Price Trend")
    st.plotly_chart(fig)

    # Show latest price
    latest_price = data['Price'].iloc[-1]
    st.metric(label=f"Current {crypto} Price", value=f"${latest_price:.2f}")

# 🚀 Fetch Bitcoin Price Data for Heatmap
@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_bitcoin_price_history():
    API_URL = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    params = {"vs_currency": "usd", "days": "30", "interval": "daily"}
    response = requests.get(API_URL)

    if response.status_code == 200:
        return response.json()
    else:
        st.warning("⚠ Unable to fetch Bitcoin price data. Please try again later!")
        return None

# 🔥 Fetch Bitcoin Data
btc_data = get_bitcoin_price_history()

if btc_data:
    prices = btc_data["prices"]
    df = pd.DataFrame(prices, columns=["timestamp", "price"])
    df["date"] = pd.to_datetime(df["timestamp"], unit="ms").dt.date  # Convert timestamp to date

    # Convert to pivot table format for heatmap
    df["hour"] = [datetime.now().hour] * len(df)  # Create a dummy hour column
    heatmap_data = df.pivot("hour", "date", "price")

    # 🎨 Plot Heatmap
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.heatmap(heatmap_data, cmap="coolwarm", annot=True, fmt=".0f", linewidths=0.5, ax=ax)
    plt.title("Bitcoin Price Heatmap (USD) - Last 30 Days", fontsize=14)

    # Display heatmap
    st.pyplot(fig)
