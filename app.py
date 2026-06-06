import streamlit as st
import requests
import pandas as pd
import pandas_ta as ta
import time

# Streamlit Page Configuration
st.set_page_config(page_title="Crypto 15m 200 EMA Scanner", page_icon="🔍", layout="wide")

# Advanced CSS for Luxury Look & Dynamic Glow Animations
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
    }
    
    /* Sidebar Border & Dark Theme */
    [data-testid="stSidebar"] {
        background-color: #090d16 !important;
        border-right: 1px solid #1f2937;
    }
    
    /* Live Scanning Card Styling */
    .scanning-box {
        background: rgba(17, 24, 39, 0.85);
        border: 2px solid #38bdf8;
        box-shadow: 0px 0px 25px rgba(56, 189, 248, 0.4);
        padding: 25px;
        border-radius: 16px;
        text-align: center;
        margin: 20px 0;
        animation: pulse 1.5s infinite alternate;
    }
    
    /* Glowing Scanning Coin */
    .scanning-coin {
        font-size: 3rem !important;
        font-weight: 800;
        color: #ff007f !important;
        text-shadow: 0 0 15px rgba(255, 0, 127, 0.6);
        letter-spacing: 2px;
    }
    
    /* Pulse Animation Logic */
    @keyframes pulse {
        0% { transform: scale(0.99); box-shadow: 0 0 15px rgba(56, 189, 248, 0.3); }
        100% { transform: scale(1.01); box-shadow: 0 0 30px rgba(56, 189, 248, 0.6); }
    }
    
    /* Custom Styling for Results */
    .signal-card {
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        font-weight: bold;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .bullish {
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid #10b981;
        color: #10b981;
    }
    .bearish {
        background: rgba(239, 68, 68, 0.15);
        border: 1px solid #ef4444;
        color: #ef4444;
    }
    .coin-link {
        color: #00d2ff;
        text-decoration: none;
    }
    .coin-link:hover {
        text-decoration: underline;
    }
    </style>
""", unsafe_allow_html=True)

# App Title
st.title("🔍 Premium Crypto 15m 200 EMA Live Scanner")
st.write("Binance API ব্যবহার করে প্রতি ১৫ মিনিট পর পর স্বয়ংক্রিয় লাইভ ২০০ EMA ট্র্যাকার।")

# User Credentials
TELEGRAM_BOT_TOKEN = "8957518460:AAE_9HaugsNNYfjOzCpbHi2nJAEKf4GSiKs"
TELEGRAM_CHAT_ID = "6166836299"

# Binance Pairs List (Mapping from CoinGecko IDs to Binance Symbols)
# যেসব কয়েন বাইনান্সে USDT পেয়ারে আছে সেগুলো এখানে দেওয়া হলো
binance_symbols = [
    "BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT", 
    "ADAUSDT", "DOTUSDT", "AVAXUSDT", "LINKUSDT", "LTCUSDT", 
    "DOGEUSDT", "SHIBUSDT", "MATICUSDT", "ATOMUSDT", "BCHUSDT", 
    "ETCUSDT", "XLMUSDT", "NEARUSDT", "TRXUSDT", "UNIUSDT",
    "SUIUSDT", "APTUSDT", "TONUSDT", "INJUSDT", "SEIUSDT", 
    "FTMUSDT", "ALGOUSDT", "EGLDUSDT", "TIAUSDT", "MINAUSDT", 
    "FLOWUSDT", "ICPUSDT", "EOSUSDT", "KAVAUSDT", "ASTRUSDT", 
    "ONEUSDT", "HBARUSDT", "IOTAUSDT", "NEOUSDT", "QTUMUSDT", 
    "VETUSDT", "ZILUSDT", "WAVESUSDT", "THETAUSDT", "STRATISUSDT",
    "ARBUSDT", "OPUSDT", "STRKUSDT", "METISUSDT", "MANTAUSDT", 
    "SKLUSDT", "CELOUSDT", "LRCUSDT", "IMXUSDT", "OMGUSDT", "ROSEUSDT",
    "PEPEUSDT", "WIFUSDT", "BONKUSDT", "FLOKIUSDT", "BOMEUSDT", 
    "MEMEUSDT", "MYROUSDT", "1000SATSUSDT", "TURBOUSDT", "BABYDOGEUSDT", 
    "PEOPLEUSDT", "WENUSDT", "NOTUSDT", "POPCATUSDT", "CATUSDT", 
    "BRETTUSDT", "MOGUSDT", "NEIROUSDT", "MOODENGUSDT", "GOATUSDT", 
    "PNUTUSDT", "ACTUSDT", "SUNDOGUSDT",
    "FETUSDT", "RNDRUSDT", "GRTUSDT", "TAOUSDT", "AKASHTUSDT", 
    "AGIXUSDT", "OCEANUSDT", "PHBUSDT", "ARKMUSDT", "WLDUSDT", 
    "NFPUSDT", "AIUSDT", "LPTUSDT", "FILUSDT", "ARUSDT", 
    "JASMYUSDT", "STORJUSDT", "BLZUSDT", "ANKRUSDT", "IONETUSDT", 
    "GLMUSDT", "ORDIUSDT", "MDTUSDT", "CTXCIUSDT", "GTCUSDT", "CLVUSDT",
    "AAVEUSDT", "PENDLEUSDT", "MKRUSDT", "CRVUSDT", "LDOUSDT", 
    "JUPUSDT", "RUNEUSDT", "DYDXUSDT", "ENSUSDT", "COMPUSDT", 
    "SNXUSDT", "SUSHIUSDT", "YFIUSDT", "CAKEUSDT", "BAKEUSDT", 
    "RAYUSDT", "JOEUSDT", "JTOUSDT", "ORCAUSDT", "COWUSDT", 
    "1INCHUSDT", "BALUSDT", "BADGERUSDT", "ALPHAUSDT",
    "ENAUSDT", "DRIFTUSDT", "SAFEUSDT", "PYTHUSDT", "AXLUSDT", 
    "ONDOUSDT", "TRUUSDT", "ALPACAFUSDT", "BELUSDT", "AUCTIONUSDT", 
    "TROYUSDT", "QUICKUSDT", "FISUSDT", "UNIFIUSDT", "ETHFIUSDT", 
    "REZUSDT", "OMNIUSDT", "TNSRUSDT", "SAGAUSDT", "BBUSDT", 
    "DOCKUSDT", "WRXUSDT", "SCRUSDT", "GALAUSDT", "AXSUSDT", 
    "SANDUSDT", "MANAUSDT", "PIXELUSDT", "BEAMUSDT", "YGGUSDT", 
    "ILVUSDT", "ALICEUSDT", "ENJUSDT", "MAGICUSDT", "PORTALUSDT", 
    "XAIUSDT", "CHZUSDT", "SUPERUSDT", "VOXELUSDT", "DARUSDT", 
    "TLMUSDT", "BIGTIMEUSDT", "TOKENUSDT", "VANRYUSDT", "MBOXUSDT", 
    "HIGHUSDT", "WOMWHOLEUSDT", "STGUSDT", "SYNUSDT", "GLMRUSDT", 
    "MOVRUSDT", "KSMUSDT", "ICXUSDT", "BANDUSDT", "TRBUSDT", 
    "DIAUSDT", "ZECUSDT", "XMRUSDT", "DASHUSDT", "ZENUSDT", 
    "ONTUSDT", "IOTXUSDT", "RVNUSDT", "HOTUSDT", "BATUSDT", 
    "KNCUSDT", "ZRXUSDT", "RENUSDT", "WOOUSDT", "GMTUSDT", 
    "IDUSDT", "EDUUSDT", "HOOKUSDT", "CYBERUSDT", "MAVUSDT", 
    "ARKUSDT", "POLYUSDT", "LOOMUSDT", "BONDUSDT", "VGXUSDT", "RADUSDT"
]

# Function to send Telegram Message
def send_telegram_message(token, chat_id, text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Telegram error: {e}")

# Function to fetch data from Binance and calculate 15m 200 EMA
def get_binance_ema_status(symbol):
    url = "https://api.binance.com/api/v3/klines"
    # Fetch 300 candlesticks of 15-minute intervals to calculate 200 EMA accurately
    params = {"symbol": symbol, "interval": "15m", "limit": "300"}
    
    try:
        response = requests.get(url, params=params)
        if response.status_code != 200:
            return "error", None, None
            
        data = response.json()
        if len(data) < 200:
            return "insufficient_data", None, None
            
        # Extract closing prices
        close_prices = [float(candle[4]) for candle in data]
        
        df = pd.DataFrame(close_prices, columns=["price"])
        df['ema_200'] = ta.ema(df['price'], length=200)
        
        last_row = df.iloc[-1]
        current_price = last_row['price']
        ema_200 = last_row['ema_200']
        
        if pd.isna(ema_200):
            return "insufficient_data", None, None
            
        status = "BULLISH" if current_price > ema_200 else "BEARISH"
        return status, current_price, ema_200
        
    except Exception:
        return "error", None, None

# Main Execution Flow
st.sidebar.header("⚙️ কন্ট্রোল প্যানেল")
st.sidebar.info("এই অ্যাপ্লিকেশনটি চালূ রাখলে প্রতি ১৫ মিনিট পর পর অটোমেটিক লাইভ স্ক্যান হবে এবং রেজাল্ট আপডেট করবে।")

# Containers for results
live_status_box = st.empty()
col1, col2 = st.columns(2)

with col1:
    st.subheader("🟢 15m 200 EMA এর উপরে (Buy Signal)")
    bullish_container = st.container()

with col2:
    st.subheader("🔴 15m 200 EMA এর নিচে (Sell Signal)")
    bearish_container = st.container()

# Auto Refresh & Scan Loop
while True:
    # Clear previous screen results before starting a new cycle
    bullish_container.empty()
    bearish_container.empty()
    
    total_coins = len(binance_symbols)
    
    # Telegram Broadcast for scan start
    send_telegram_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, "🔄 *১৫ মিনিটের ক্যান্ডেল স্ক্যান শুরু হয়েছে...*")
    
    for i, symbol in enumerate(binance_symbols):
        progress_perc = int(((i + 1) / total_coins) * 100)
        
        # Display custom animated scanning card
        live_status_box.markdown(f"""
            <div class="scanning-box">
                <p style="color: #38bdf8; font-size: 1.2rem; margin-bottom: 5px; font-weight: 600;">
                    🔍 লাইভ স্ক্যানিং প্রোগ্রেস (15m Timeframe): {progress_perc}% ({i+1}/{total_coins})
                </p>
                <div class="scanning-coin">{symbol}</div>
                <p style="color: #64748b; font-size: 0.9rem; margin-top: 5px;">
                    বাইনান্স হাই-স্পিড ডাটাবেজ প্রসেসিং চলছে...
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Fetching Status from Binance
        status, price, ema = get_binance_ema_status(symbol)
        
        coin_url = f"https://www.binance.com/en/trade/{symbol.replace('USDT', '_USDT')}"
        
        if status == "BULLISH":
            # Display in UI
            bullish_container.markdown(f"""
                <div class="signal-card bullish">
                    <span>🟢 <a class="coin-link" href="{coin_url}" target="_blank">{symbol}</a></span>
                    <span>Price: ${price:,.4f} | EMA: ${ema:,.4f}</span>
                </div>
            """, unsafe_allow_html=True)
            
            # Send Telegram Message
            msg = f"🟢 *15m BUY SIGNAL* 🟢\n\n*Coin:* [{symbol}]({coin_url})\n*Status:* Above 200 EMA (15m)\n*Price:* ${price:,.4f}\n*200 EMA:* ${ema:,.4f}"
            send_telegram_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, msg)
            
        elif status == "BEARISH":
            # Display in UI
            bearish_container.markdown(f"""
                <div class="signal-card bearish">
                    <span>🔴 <a class="coin-link" href="{coin_url}" target="_blank">{symbol}</a></span>
                    <span>Price: ${price:,.4f} | EMA: ${ema:,.4f}</span>
                </div>
            """, unsafe_allow_html=True)
            
            # Send Telegram Message
            msg = f"🔴 *15m SELL SIGNAL* 🔴\n\n*Coin:* [{symbol}]({coin_url})\n*Status:* Below 200 EMA (15m)\n*Price:* ${price:,.4f}\n*200 EMA:* ${ema:,.4f}"
            send_telegram_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, msg)
            
        # Binance API allows faster requests (0.1 seconds interval is totally fine)
        time.sleep(0.1)
        
    live_status_box.success("🎉 স্ক্যান শেষ! পরবর্তী স্ক্যান ১৫ মিনিট পর স্বয়ংক্রিয়ভাবে শুরু হবে।")
    
    # Wait for 15 minutes (15 minutes = 900 seconds) before starting the next cycle
    time.sleep(900)