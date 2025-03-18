import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import yfinance as yf

# Function to fetch the top 100 crypto coins from CoinGecko API
def get_top_coins(limit=100):
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": limit,
        "page": 1,
        "sparkline": False
    }
    
    response = requests.get(url)
    
    # Kiểm tra nếu API request thất bại
    if response.status_code != 200:
        st.error(f"⚠ Failed to fetch top coins. API Error: {response.status_code}")
        return {}

    try:
        data = response.json()
        if not isinstance(data, list):
            st.error("⚠ Invalid API response format. Expected a list.")
            return {}

        # Kiểm tra nếu danh sách coins rỗng
        if len(data) == 0:
            st.error("⚠ No coins found. Try again later.")
            return {}

        # Lấy 100 đồng coin đầu tiên
        coin_dict = {coin.get('name', 'Unknown'): coin.get('id', 'Unknown') for coin in data[:100]}
        return coin_dict
    
    except Exception as e:
        st.error(f"⚠ Error parsing API response: {e}")
        return {}

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

# Fetch top 100 coins
coin_dict = get_top_coins(100)

# Nếu API lỗi, hiển thị cảnh báo và dừng ứng dụng
if not coin_dict:
    st.error("⚠ Could not fetch top cryptocurrencies. Please try again later.")
    st.stop()

coin_names = list(coin_dict.keys())

# Sidebar: User input
crypto = st.sidebar.selectbox("Select Cryptocurrency", coin_names)
days = st.sidebar.slider("Select Days of Data", min_value=1, max_value=90, value=7)

# Fetch and display data
crypto_id = coin_dict[crypto]  # Get CoinGecko ID
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
