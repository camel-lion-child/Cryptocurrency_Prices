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
def get_crypto_news():
    url = "https://api.coingecko.com/api/v3/status_updates"
    response = requests.get(url)

    if response.status_code != 200:
        st.error(f"⚠ Failed to fetch news. API returned {response.status_code}")
        return []

    try:
        data = response.json()
        return data.get("status_updates", [])
    except Exception as e:
        st.error(f"⚠ Error fetching news: {e}")
        return []

# Hiển thị logo trong sidebar
st.sidebar.image("https://raw.githubusercontent.com/camel-lion-child/witin_crypto_dashboard/refs/heads/main/witin.png", width=150)

# Streamlit UI
st.title("📈 WITIN Crypto Analytics Dashboard")

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
st.write("### 📰 Latest Crypto Market News")
news_articles = get_crypto_news()

if news_articles:
    for article in news_articles[:5]:  # Show top 5 articles
        st.markdown(f"#### {article['project']['name'] if 'project' in article else 'General News'}")
        st.write(article["description"])
        st.write("---")
else:
    st.write("⚠ No news available at the moment.")

