import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# 🚀 Page Configuration
st.set_page_config(page_title="WITIN Crypto Dashboard", page_icon="💎", layout="wide")

# 🎨 Display Logo in Sidebar
LOGO_URL = "https://raw.githubusercontent.com/camel-lion-child/witin_crypto_dashboard/refs/heads/main/witin.png"  # Replace with your GitHub raw link
st.sidebar.image(LOGO_URL, width=150)

# 📊 Title
st.title("📊 Crypto Price Dashboard")

# 🔥 List of 50 Important Cryptocurrencies
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
crypto = st.sidebar.selectbox("Select Cryptocurrency", list(COINS.keys()))
days = st.sidebar.slider("Select Days of Data", min_value=1, max_value=90, value=7)

# 📡 Fetch Crypto Price Data from CoinGecko API
# Define the Streamlit script as a multi-line string
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



# Fetch and display data
data = get_crypto_data(crypto, days)
st.write(f"### {crypto.capitalize()} Price Trend - Last {days} Days")
fig = px.line(data, x='timestamp', y='price', title=f"{crypto.capitalize()} Price Trend")
st.plotly_chart(fig)

# Show latest price
latest_price = data['price'].iloc[-1]
st.metric(label=f"Current {crypto.capitalize()} Price", value=f"${latest_price:.2f}")
