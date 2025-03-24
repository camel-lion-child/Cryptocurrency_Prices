import streamlit as st
import requests
import matplotlib.pyplot as plt
import datetime
import asyncio
import telegram


# Ngưỡng cảnh báo
THRESHOLD_UP = 0.5
THRESHOLD_DOWN = -0.5

# Lưu dữ liệu
timestamps = []
usdt_d_values = []
previous_usdt_d = None

st.set_page_config(page_title="USDT.D Alert", page_icon="🔔")

st.title("🔔 USDT Dominance Alert")

def get_usdt_dominance():
    """Lấy dữ liệu USDT.D từ CoinGecko API"""
    url = "https://api.coingecko.com/api/v3/global"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        usdt_dominance = data["data"]["market_cap_percentage"]["tether"]
        return round(usdt_dominance, 2)
    return None


def check_alert(usdt_d):
    """Kiểm tra biến động mạnh và gửi cảnh báo"""
    global previous_usdt_d
    if previous_usdt_d is not None:
        change = usdt_d - previous_usdt_d
        if change >= THRESHOLD_UP:
            message = f"🚨 WARNING: USDT.D SURGES STRONGLY ({change:.2f}%)! BTC might drop."
            asyncio.run(send_telegram_alert(message))
        elif change <= THRESHOLD_DOWN:
            message = f"✅ GOOD SIGNAL: USDT.D DECREASES ({change:.2f}%)! BTC might pump."
            asyncio.run(send_telegram_alert(message))
    previous_usdt_d = usdt_d

def update_usdt_d():
    """Cập nhật dữ liệu USDT.D"""
    usdt_d = get_usdt_dominance()
    if usdt_d is None:
        return

    timestamps.append(datetime.datetime.now().strftime('%H:%M'))
    usdt_d_values.append(usdt_d)

    if len(timestamps) > 50:
        timestamps.pop(0)
        usdt_d_values.pop(0)

    check_alert(usdt_d)

# --- 📢 CẢNH BÁO USDT.D ---
st.subheader("📢 USDT.D Alert")
if st.button("USDT Dominance Update"):
    update_usdt_d()
    st.success(f"USDT Dominance: {usdt_d_values[-1]}% (Updated!)")

# --- 📈 BIỂU ĐỒ USDT.D ---
st.subheader("📊 USDT Dominance Chart")
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(timestamps, usdt_d_values, marker='o', linestyle='-', color='b', label="USDT Dominance")
ax.set_xlabel("Time")
ax.set_ylabel("USDT Dominance (%)")
ax.set_title("USDT.D Volatility Over Time")
ax.legend()
ax.grid()
st.pyplot(fig)
