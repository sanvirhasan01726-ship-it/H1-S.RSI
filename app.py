import streamlit as st
import pandas as pd
import numpy as np
import requests
import time
from datetime import datetime

# ১. পেজ কনফিগারেশন এবং লেআউট সেটআপ (Wide Mode)
st.set_page_config(page_title="Crypto Luxury Scanner", layout="wide")

# ২. প্রিমিয়াম কাস্টম সিএসএস (Luxury UI)
st.markdown("""
    <style>
    /* Main Theme - ডার্ক লাক্সারি ব্যাকগ্রাউন্ড */
    .stApp {
        background: linear-gradient(135deg, #090d16 0%, #111827 100%);
        color: #f8fafc;
    }
    
    /* Glowing Title */
    h1 {
        color: #00d2ff !important;
        background: linear-gradient(to right, #00ffff, #0088ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Inter', sans-serif;
        font-weight: 900 !important;
        text-shadow: 0px 0px 20px rgba(0, 255, 255, 0.3);
        text-align: center;
    }
    
    /* Live Scanning Card Styling */
    .scanning-box {
        background: rgba(17, 24, 39, 0.85);
        border: 2px solid #38bdf8;
        box-shadow: 0px 0px 25px rgba(56, 189, 248, 0.4);
        padding: 20px;
        border-radius: 16px;
        text-align: center;
        margin: 15px 0;
    }
    
    /* Glowing Scanning Coin */
    .scanning-coin {
        font-size: 2.5rem !important;
        font-weight: 800;
        color: #ff007f !important;
        text-shadow: 0 0 15px rgba(255, 0, 127, 0.6);
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    
    /* Signal Cards - ছোট সাইজের কমপ্যাক্ট ডিজাইন */
    .signal-card {
        padding: 10px 15px;
        border-radius: 10px;
        margin-bottom: 8px;
        font-family: 'Inter', sans-serif;
    }
    .buy-card {
        background: rgba(16, 185, 129, 0.1);
        border-left: 5px solid #10b981;
        border-right: 1px solid rgba(16, 185, 129, 0.2);
        border-top: 1px solid rgba(16, 185, 129, 0.2);
        border-bottom: 1px solid rgba(16, 185, 129, 0.2);
        box-shadow: 0 0 15px rgba(16, 185, 129, 0.15);
    }
    .sell-card {
        background: rgba(239, 68, 68, 0.1);
        border-left: 5px solid #ef4444;
        border-right: 1px solid rgba(239, 68, 68, 0.2);
        border-top: 1px solid rgba(239, 68, 68, 0.2);
        border-bottom: 1px solid rgba(239, 68, 68, 0.2);
        box-shadow: 0 0 15px rgba(239, 68, 68, 0.15);
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>Crypto Luxury Automative Scanner</h1>", unsafe_allow_html=True)

# ৩. টেলিগ্রাম ক্রেডেনশিয়ালস
TELEGRAM_BOT_TOKEN = "8957518460:AAE_9HaugsNNYfjOzCpbHi2nJAEKf4GSiKs"
TELEGRAM_CHAT_ID = "6166836299"

# ৪. CoinGecko Coin IDs লিস্ট
coingecko_coin_ids = [
    "bitcoin", "ethereum", "binancecoin", "solana", "ripple", 
    "cardano", "polkadot", "avalanche-2", "chainlink", "litecoin", 
    "dogecoin", "shiba-inu", "cosmos", "bitcoin-cash", "ethereum-classic", 
    "stellar", "near", "tron", "uniswap", "sui", "aptos", "toncoin", 
    "injective-protocol", "sei-network", "fantom", "algorand", "elrond-erd-2", 
    "celestia", "mina-protocol", "flow", "internet-computer", "eos", "kava", 
    "astar", "harmony", "hedera-hashgraph", "iota", "neo", "qtum", "vechain", 
    "zilliqa", "waves", "theta-token", "arbitrum", "optimism", "starknet", 
    "metis-token", "manta-network", "skale", "celo", "loopring", "immutable-x", 
    "pepe", "dogwifhat", "bonk", "floki", "book-of-meme", "memecoin", "myro", 
    "turbo", "notcoin", "popcat", "brett", "mog-coin", "moodeng", "aave", 
    "pendle", "maker", "curve-dao-token", "lido-dao", "jupiter-exchange-solana", 
    "thorchain", "dydx-chain", "ethereum-name-service", "pancakeswap-token", 
    "raydium", "1inch", "ethena", "pyth-network", "ondo-finance", "gala", 
    "axie-infinity", "the-sandbox", "decentraland", "pixel", "beam", 
    "yield-guide-games", "chiliz", "superfarm", "bigtime", "token-fi", 
    "zcash", "monero", "dash", "horizen", "iotex", "ravencoin", 
    "basic-attention-token", "woo-network", "stepn", "space-id"
]

# ৫. টেলিগ্রাম মেসেজ সেন্ডিং ফাংশন
def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=5)
    except:
        pass

# ৬. CoinGecko API থেকে ওএইচএলসি (OHLC) ডেটা আনার ফাংশন
def get_ohlc_data(coin_id):
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/ohlc?vs_currency=usd&days=30"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            return df
        elif response.status_code == 429:
            time.sleep(10)
        return None
    except:
        return None

# 💡 বিশুদ্ধ পান্ডাস ব্যবহার করে Stochastic RSI ক্যালকুলেশন (No pandas-ta)
def calculate_stoch_rsi(close_series, length=20, rsi_length=20, k=3, d=3):
    delta = close_series.diff()
    gain = (delta.where(delta > 0, 0)).ewm(span=rsi_length, adjust=False).mean()
    loss = (-delta.where(delta < 0, 0)).ewm(span=rsi_length, adjust=False).mean()
    
    rs = gain / (loss + 1e-10)
    rsi = 100 - (100 / (1 + rs))
    
    rsi_min = rsi.rolling(window=length).min()
    rsi_max = rsi.rolling(window=length).max()
    
    stoch_rsi = 100 * (rsi - rsi_min) / (rsi_max - rsi_min + 1e-10)
    stoch_k = stoch_rsi.rolling(window=k).mean()
    stoch_d = stoch_k.rolling(window=d).mean()
    return stoch_k, stoch_d

# ৭. টেকনিক্যাল ইন্ডিকেটর এবং সিগন্যাল ক্যালকুলেশন লজিক
def check_signals(df):
    if len(df) < 200:
        return None
    
    # বিশুদ্ধ পান্ডাস দিয়ে ২০০ EMA হিসাব
    df['ema_200'] = df['close'].ewm(span=200, adjust=False).mean()
    
    # Stochastic RSI হিসাব
    df['stoch_k'], df['stoch_d'] = calculate_stoch_rsi(df['close'])
    
    last_idx = len(df) - 1
    current_close = df['close'].iloc[last_idx]
    current_ema = df['ema_200'].iloc[last_idx]
    
    if pd.isna(current_ema) or pd.isna(df['stoch_k'].iloc[last_idx]):
        return None

    # ১. ইএমএ ফিল্টার চেক
    ema_down = current_close < current_ema
    ema_up = current_close > current_ema

    # ২. Equal Low / High লজিক
    lookback = 5
    buffer = 0.0025
    recent_lows = df['low'].iloc[last_idx-lookback:last_idx]
    recent_highs = df['high'].iloc[last_idx-lookback:last_idx]
    
    current_low = df['low'].iloc[last_idx]
    current_high = df['high'].iloc[last_idx]
    
    is_equal_low = any(abs(current_low - prev_low) <= (current_low * buffer) for prev_low in recent_lows)
    is_equal_high = any(abs(current_high - prev_high) <= (current_high * buffer) for prev_high in recent_highs)

    # ৩. Stoch RSI Divergence সিম্পল প্রক্সি
    stoch_k_last = df['stoch_k'].iloc[last_idx]
    stoch_k_prev = df['stoch_k'].iloc[last_idx-1]
    
    stoch_buy_div = (stoch_k_last < 20) and (stoch_k_last > stoch_k_prev)
    stoch_sell_div = (stoch_k_last > 80) and (stoch_k_last < stoch_k_prev)

    if ema_down and is_equal_low and stoch_buy_div:
        return "BUY"
    elif ema_up and is_equal_high and stoch_sell_div:
        return "SELL"
        
    return None

# ----------------- UI Structure -----------------

if 'buy_signals' not in st.session_state: st.session_state.buy_signals = []
if 'sell_signals' not in st.session_state: st.session_state.sell_signals = []
if 'is_scanning' not in st.session_state: st.session_state.is_scanning = False
if 'current_index' not in st.session_state: st.session_state.current_index = 0

st.sidebar.header("⚙️ কন্ট্রোল প্যানেল")
if st.sidebar.button("🚀 স্ক্যান শুরু করুন"):
    st.session_state.buy_signals = []
    st.session_state.sell_signals = []
    st.session_state.current_index = 0
    st.session_state.is_scanning = True
    send_telegram_message("🔄 *কয়েনগিকো (CoinGecko) ১ ঘণ্টার ফ্রেম লাইভ স্ক্যান শুরু হয়েছে...*")

live_status_box = st.empty()
col_buy, col_sell = st.columns(2)

with col_buy:
    st.markdown("<h2 style='color: #10b981; text-align: center;'>🟢 BUY SIGNALS</h2>", unsafe_allow_html=True)
    buy_container = st.container()

with col_sell:
    st.markdown("<h2 style='color: #ef4444; text-align: center;'>🔴 SELL SIGNALS</h2>", unsafe_allow_html=True)
    sell_container = st.container()

# পূর্বের সংরক্ষিত ডেটা স্ক্রিনে রেন্ডার করা
with buy_container:
    for sig in st.session_state.buy_signals:
        st.markdown(f"""
            <div class="signal-card buy-card">
                <strong style="color: #10b981; font-size: 1.1rem;">🪙 {sig['coin']}</strong><br/>
                <span style="color: #f8fafc;">💰 Price: ${sig['price']:.4f}</span><br/>
                <span style="color: #64748b; font-size: 0.8rem;">⏰ Time: {sig['time']} (H1 Frame)</span>
            </div>
        """, unsafe_allow_html=True)

with col_sell:
    for sig in st.session_state.sell_signals:
        st.markdown(f"""
            <div class="signal-card sell-card">
                <strong style="color: #ef4444; font-size: 1.1rem;">🪙 {sig['coin']}</strong><br/>
                <span style="color: #f8fafc;">💰 Price: ${sig['price']:.4f}</span><br/>
                <span style="color: #64748b; font-size: 0.8rem;">⏰ Time: {sig['time']} (H1 Frame)</span>
            </div>
        """, unsafe_allow_html=True)

# মূল এক্সিকিউশন রানার লুপ
if st.session_state.is_scanning:
    idx = st.session_state.current_index
    total_coins = len(coingecko_coin_ids)
    
    if idx < total_coins:
        coin = coingecko_coin_ids[idx]
        progress_perc = int(((idx + 1) / total_coins) * 100)
        
        live_status_box.markdown(f"""
            <div class="scanning-box">
                <p style="color: #38bdf8; font-size: 1.2rem; margin-bottom: 5px; font-weight: 600;">
                    🔍 বর্তমান স্ক্যানিং প্রোগ্রেস: {progress_perc}% ({idx+1}/{total_coins})
                </p>
                <div class="scanning-coin">{coin.replace('-', ' ')}</div>
                <p style="color: #64748b; font-size: 0.9rem; margin-top: 5px;">
                    কয়েনগিকো (CoinGecko) সার্ভার কুলডাউন বিরতি চলমান...
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        df_data = get_ohlc_data(coin)
        
        if df_data is not None:
            signal = check_signals(df_data)
            time_now = datetime.now().strftime("%H:%M:%S")
            current_price = df_data['close'].iloc[-1]
            coin_display = coin.upper().replace('-', ' ')
            coin_url = f"https://www.coingecko.com/en/coins/{coin}"
            
            if signal == "BUY":
                st.session_state.buy_signals.append({"coin": coin_display, "time": time_now, "price": current_price})
                # সাথে সাথে টেলিগ্রামে একটি করে আলাদা মেসেজ পাঠানো হচ্ছে
                tg_msg = f"🟢 *DEX/CEX BUY SIGNAL (H1)* 🟢\n\n*Coin:* [{coin_display}]({coin_url})\n*Price:* ${current_price:,.4f}\n*Indicator:* Price Below 200 EMA + Equal Lows + Stoch RSI Reversal"
                send_telegram_message(tg_msg)
                
            elif signal == "SELL":
                st.session_state.sell_signals.append({"coin": coin_display, "time": time_now, "price": current_price})
                # সাথে সাথে টেলিগ্রামে একটি করে আলাদা মেসেজ পাঠানো হচ্ছে
                tg_msg = f"🔴 *DEX/CEX SELL SIGNAL (H1)* 🔴\n\n*Coin:* [{coin_display}]({coin_url})\n*Price:* ${current_price:,.4f}\n*Indicator:* Price Above 200 EMA + Equal Highs + Stoch RSI Drop"
                send_telegram_message(tg_msg)
        
        st.session_state.current_index += 1
        time.sleep(1.5) # রেট লিমিট এড়ানোর জন্য সেফ ডিলে
        st.rerun()
    else:
        st.session_state.is_scanning = False
        live_status_box.markdown(f"""
            <div class="scanning-box" style="border-color: #7c3aed; box-shadow: 0 0 25px rgba(124, 58, 237, 0.4);">
                <p style="color: #a78bfa; font-size: 1.3rem; font-weight: bold;">😴 স্ক্যান সম্পন্ন! পরবর্তী স্ক্যান ১ ঘণ্টা পর স্বয়ংক্রিয়ভাবে শুরু হবে।</p>
                <p style="color: #64748b; font-size: 0.9rem;">সর্বশেষ চক্র সম্পন্ন হয়েছে: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
        """, unsafe_allow_html=True)
        time.sleep(3600)
        st.session_state.is_scanning = True
        st.session_state.current_index = 0
        st.rerun()
