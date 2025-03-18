import streamlit as st
import pandas as pd
import requests
import plotly.express as px

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
    data = response.json()
    
    # Extract coin names & IDs
    coin_dict = {coin['name']: coin['id'] for coin in data}
    return coin_dict

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

# Streamlit UI
st.title("📈 WITIN Crypto Analytics Dashboard")

# Fetch top 100 coins
coin_dict = get_top_coins(100)
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

    # Show data preview
    st.write("### Data Preview")
    st.dataframe(data.head())
