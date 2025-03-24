import streamlit as st
import requests
import matplotlib.pyplot as plt
import datetime

# --- Configuration ---
THRESHOLD_UP = 0.5
THRESHOLD_DOWN = -0.5

# Store data
timestamps = []
usdt_d_values = []
previous_usdt_d = None

st.set_page_config(page_title="USDT.D Alert", page_icon="🔔")

st.title("🔔 USDT Dominance Alert")

def get_usdt_dominance():
    """Fetch USDT.D data from CoinGecko API"""
    url = "https://api.coingecko.com/api/v3/global"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        usdt_dominance = data.get("data", {}).get("market_cap_percentage", {}).get("tether")
        if usdt_dominance is not None:
            return round(usdt_dominance, 2)
    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {e}")
    return None

def check_alert(usdt_d):
    """Check for strong USDT.D movements and display alerts"""
    global previous_usdt_d
    if previous_usdt_d is not None:
        change = usdt_d - previous_usdt_d
        if change >= THRESHOLD_UP:
            st.warning(f"🚨 WARNING: USDT.D surged by {change:.2f}%. BTC might drop.")
        elif change <= THRESHOLD_DOWN:
            st.success(f"✅ GOOD SIGNAL: USDT.D dropped by {change:.2f}%. BTC might pump.")
    previous_usdt_d = usdt_d

def update_usdt_d():
    """Update USDT.D data"""
    usdt_d = get_usdt_dominance()
    if usdt_d is None:
        st.error("Failed to retrieve USDT Dominance data.")
        return

    timestamps.append(datetime.datetime.now().strftime('%H:%M'))
    usdt_d_values.append(usdt_d)

    # Keep only the last 50 data points
    if len(timestamps) > 50:
        timestamps.pop(0)
        usdt_d_values.pop(0)

    check_alert(usdt_d)

# --- 📢 USDT.D ALERT SECTION ---
st.subheader("📢 USDT.D Alert")
if st.button("Update USDT Dominance"):
    update_usdt_d()
    if usdt_d_values:
        st.success(f"USDT Dominance: {usdt_d_values[-1]}% (Updated!)")
    else:
        st.warning("No data available. Try updating again.")

# --- 📈 USDT.D CHART SECTION ---
st.subheader("📊 USDT Dominance Chart")
if usdt_d_values:
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(timestamps, usdt_d_values, marker='o', linestyle='-', color='b', label="USDT Dominance")
    ax.set_xlabel("Time")
    ax.set_ylabel("USDT Dominance (%)")
    ax.set_title("USDT.D Volatility Over Time")
    ax.legend()
    ax.grid()
    st.pyplot(fig)
else:
    st.warning("No data available yet. Click 'Update USDT Dominance' to fetch data.")
