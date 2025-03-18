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
@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_crypto_data(crypto_id, days=90):
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart?vs_currency=usd&days={days}"
    response = requests.get(url)

    if response.status_code == 200:
        try:
            data = response.json()
            if 'prices' not in data or not data['prices']:
                st.error("⚠ API returned an empty price list.")
                return pd.DataFrame(columns=['Timestamp', 'Price'])

            # Convert API response to DataFrame
            prices = data['prices']
            df = pd.DataFrame(prices, columns=['timestamp', 'price'])
            df['Timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.drop(columns=['timestamp'], inplace=True)

            return df
        except Exception as e:
            st.error(f"⚠ Failed to parse API response: {e}")
            return pd.DataFrame(columns=['Timestamp', 'Price'])

    else:
        st.error(f"⚠ API Error: {response.status_code}. Please try again later.")
        return pd.DataFrame(columns=['Timestamp', 'Price'])

# 📊 Fetch and Display Price Chart
crypto_id = COINS[crypto]
data = get_crypto_data(crypto_id, days)

if data.empty:
    st.error(f"⚠ No data available for {crypto}. Try another cryptocurrency.")
else:
    st.write(f"### {crypto} Price Trend - Last {days} Days")
    fig = px.line(data, x='Timestamp', y='Price', title=f"{crypto} Price Trend")
    st.plotly_chart(fig)

    # Show Latest Price
    latest_price = data['Price'].iloc[-1]
    st.metric(label=f"Current {crypto} Price", value=f"${latest_price:.2f}")
