import streamlit as st
import requests
import matplotlib.pyplot as plt
import datetime

# --- Cấu hình ---
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
    """Kiểm tra biến động mạnh (chỉ hiển thị trên giao diện Streamlit)"""
    global previous_usdt_d
    if previous_usdt_d is not None:
        change = usdt_d - previous_usdt_d
        if change >= THRESHOLD_UP:
            st.warning(f"🚨 WARNING: USDT.D tăng mạnh ({change:.2f}%)! BTC có thể giảm.")
        elif change <= THRESHOLD_DOWN:
            st.success(f"✅ GOOD SIGNAL: USDT.D giảm ({change:.2f}%)! BTC có thể tăng.")
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
if st.button("Cập nhật USDT Dominance"):
    update_usdt_d()
    st.success(f"USDT Dominance: {usdt_d_values[-1]}% (Đã cập nhật!)")

# --- 📈 BIỂU ĐỒ USDT.D ---
st.subheader("📊 USDT Dominance Chart")
if usdt_d_values:
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(timestamps, usdt_d_values, marker='o', linestyle='-', color='b', label="USDT Dominance")
    ax.set_xlabel("Thời gian")
    ax.set_ylabel("USDT Dominance (%)")
    ax.set_title("Biến động USDT.D theo thời gian")
    ax.legend()
    ax.grid()
    st.pyplot(fig)
else:
    st.warning("Chưa có dữ liệu. Nhấn 'Cập nhật USDT Dominance' để lấy dữ liệu.")
