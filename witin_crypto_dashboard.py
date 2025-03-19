import streamlit as st
import pandas as pd
import requests
import plotly.express as px

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

# Function to fetch cryptocurrency news
def get_crypto_news(crypto_symbol):
    url = f"https://cryptonews-api.com/api/v1?tickers={crypto_symbol}&items=5&token=YOUR_API_KEY"
    response = requests.get(url)

    try:
        data = response.json()
        return data.get("data", [])
    except Exception as e:
        st.error(f"Failed to fetch news: {e}")
        return []

# Streamlit UI
st.title("📈 WITIN Crypto Analytics Dashboard")

# 🎨 Display Logo in Sidebar
LOGO_URL = "https://raw.githubusercontent.com/camel-lion-child/witin_crypto_dashboard/refs/heads/main/witin.png"  # Update with your GitHub raw link
st.sidebar.image(LOGO_URL, width=80)

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
st.write(f"### 📰 Latest {crypto} News")
news_articles = get_crypto_news(crypto)

if news_articles:
    for article in news_articles:
        st.markdown(f"#### [{article['title']}]({article['url']})")
        st.write(article["text"])
        st.image(article["image_url"])
        st.write("---")
else:
    st.write("No news found for this cryptocurrency.")
