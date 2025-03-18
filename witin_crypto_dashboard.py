import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import yfinance as yf

# Danh sách 50 đồng coin quan trọng
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

# Function to fetch crypto price data from CoinGecko API
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

# Function to fetch stock-like crypto data from Yahoo Finance
def get_crypto_stock_data(symbol='BTC-USD'):
    try:
        df = yf.download(symbol, period='1mo', interval='1d')
        if df.empty:
            st.warning(f"⚠ No stock data found for {symbol}. Yahoo Finance may not support this symbol.")
        return df
    except Exception as e:
        st.error(f"⚠ Error fetching Yahoo Finance data: {e}")
        return pd.DataFrame()

# Streamlit UI
st.title("📈 WITIN Crypto Analytics Dashboard")

# Sidebar: User input
crypto = st.sidebar.selectbox("Select Cryptocurrency", list(COINS.keys()))
days = st.sidebar.slider("Select Days of Data", min_value=1, max_value=90, value=7)

# Fetch and display data
crypto_id = COINS[crypto]  # Get CoinGecko ID
data = get_crypto_data(crypto_id, days)

# Kiểm tra nếu DataFrame rỗng trước khi hiển thị biểu đồ
if data.empty:
    st.error(f"⚠ No data available for {crypto}. Try another cryptocurrency.")
else:
    st.write(f"### {crypto} Price Trend - Last {days} Days")
    fig = px.line(data, x='Timestamp', y='Price', title=f"{crypto} Price Trend")
    st.plotly_chart(fig)

    # Show latest price
    latest_price = data['Price'].iloc[-1]
    st.metric(label=f"Current {crypto} Price", value=f"${latest_price:.2f}")

    # Yahoo Finance Data for Comparison
    st.write("### Stock-Like Crypto Data from Yahoo Finance")
    yf_data = get_crypto_stock_data(symbol=f"{crypto.upper()}-USD")
    if not yf_data.empty:
        st.dataframe(yf_data.tail())
    
    # Show data preview
    st.write("### Data Preview")
    st.dataframe(data.head())
