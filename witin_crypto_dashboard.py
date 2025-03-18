import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

# List of 50 important cryptocurrencies
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

# Function to fetch cryptocurrency price data from CoinGecko API
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
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

    # Rename columns to uppercase
    df.rename(columns={'timestamp': 'Timestamp', 'price': 'Price'}, inplace=True)
    return df

# Page configuration
st.set_page_config(page_title="WITIN Crypto", page_icon="💎", layout="wide")

# Page title
st.title("📊 WITIN Crypto Dashboard")
st.write("Bitcoin price heatmap over time.")

# Fetch Bitcoin price history from CoinGecko API
@st.cache_data(ttl=3600)  # Cache data for 1 hour
def get_bitcoin_price_history():
    API_URL = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    params = {
        "vs_currency": "usd",
        "days": "30",  # Get data for the past 30 days
        "interval": "daily"
    }
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json()
    else:
        st.warning("⚠ Unable to fetch Bitcoin price data. Please try again later!")
        return None

# Call API to get data
data = get_bitcoin_price_history()

if data:
    # Process data
    prices = data["prices"]
    df = pd.DataFrame(prices, columns=["timestamp", "price"])
    df["date"] = pd.to_datetime(df["timestamp"], unit="ms").dt.date  # Convert timestamp to date

    # Convert to pivot table format for heatmap
    df["hour"] = [datetime.now().hour] * len(df)  # Create a dummy hour column
    heatmap_data = df.pivot("hour", "date", "price")

    # Plot Heatmap
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.heatmap(heatmap_data, cmap="coolwarm", annot=True, fmt=".0f", linewidths=0.5, ax=ax)
    plt.title("Bitcoin Price Heatmap (USD) - Last 30 Days", fontsize=14)


# Hiển thị logo trong sidebar
st.sidebar.image("https://raw.githubusercontent.com/camel-lion-child/witin_crypto_dashboard/refs/heads/main/witin.png", width=150)

# Streamlit UI
st.title("Crypto Analytics Dashboard")

# Sidebar: User input
crypto = st.sidebar.selectbox("Select Cryptocurrency", list(COINS.keys()), key="crypto_select")
days = st.sidebar.slider("Select Days of Data", min_value=1, max_value=90, value=7, key="days_slider")

# Fetch and display data
crypto_id = COINS[crypto]  # Get CoinGecko ID
data = get_crypto_data(crypto_id, days)

# Check if DataFrame is empty before displaying the chart
if data.empty:
    st.error(f"⚠ No data available for {crypto}. Try another cryptocurrency.")
else:
    st.write(f"### {crypto} Price Trend - Last {days} Days")
    fig = px.line(data, x='Timestamp', y='Price', title=f"{crypto} Price Trend")
    st.plotly_chart(fig)

    # Show latest price
    latest_price = data['Price'].iloc[-1]
    st.metric(label=f"Current {crypto} Price", value=f"${latest_price:.2f}")

# Display Crypto News
 st.pyplot(fig)

