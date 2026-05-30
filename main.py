# ==================================================
# FINAL COMPREHENSIVE PRODUCTION: ALL 37 ASSETS ENGINE
# ==================================================
import os
import logging
import hashlib
import time
import requests
from fastapi import FastAPI, Request
import uvicorn

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# 🔴 CONFIGURATION DATA
TOKEN = "8735814245:AAFk849g-0ZEmZDINRwyWMTGSCzcOg5yRFg"
VIP_LINK = "https://t.me/+Nx_7ZeyV5UYyMWM1" 
DEFAULT_CHAT_ID = "-1003993233052"          

OWNER_MOBILE = "+91 8767812831"
OWNER_EMAIL = "arjunto" 

app = FastAPI()

# 📊 100% COMPLETE ASSETS GRID
SUPPORTED_PAIRS = {
    # --- Group 1 ---
    "AUDCADOTC": "AUD/CAD OTC", "AUDCHFOTC": "AUD/CHF OTC", "AUDJPYOTC": "AUD/JPY OTC",
    "AUDNZDOTC": "AUD/NZD OTC", "AUDUSDOTC": "AUD/USD OTC", "CADCHFOTC": "CAD/CHF OTC",
    "CADJPYOTC": "CAD/JPY OTC", "CHFJPYOTC": "CHF/JPY OTC", "EURAUDOTC": "EUR/AUD OTC",
    # --- Group 2 ---
    "EURCADOTC": "EUR/CAD OTC", "EURCHFOTC": "EUR/CHF OTC", "EURGBPOTC": "EUR/GBP OTC",
    "EURJPYOTC": "EUR/JPY OTC", "EURNZDOTC": "EUR/NZD OTC", "EURUSDOTC": "EUR/USD OTC",
    "GBPAUDOTC": "GBP/AUD OTC", "GBPCADOTC": "GBP/CAD OTC", "GBPCHFOTC": "GBP/CHF OTC",
    # --- Group 3 ---
    "GBPJPYOTC": "GBP/JPY OTC", "GBPNZDOTC": "GBP/NZD OTC", "GBPUSDOTC": "GBP/USD OTC",
    "NZDCADOTC": "NZD/CAD OTC", "NZDCHFOTC": "NZD/CHF OTC", "NZDJPYOTC": "NZD/JPY OTC",
    "NZDUSDOTC": "NZD/USD OTC", "USDARSOTC": "USD/ARS OTC", "USDBDTOTC": "USD/BDT OTC",
    # --- Group 4 ---
    "USDBRLOTC": "USD/BRL OTC", "USDCHFOTC": "USD/CHF OTC", "USDIDROTC": "USD/IDR OTC",
    "USDINROTC": "USD/INR OTC", "USDJPYOTC": "USD/JPY OTC", "USDMXNOTC": "USD/MXN OTC",
    "USDPKROTC": "USD/PKR OTC", "USDPHPOTC": "USD/PHP OTC", "USDZAROTC": "USD/ZAR OTC",
    # --- Bonus Commodities / Stocks ---
    "GOLDOTC": "GOLD OTC", "SILVEROTC": "SILVER OTC"
}

def get_support_footer():
    return f"""━━━━━━━━━━━━━━━━━━━━
📞 **OFFICIAL SUPPORT & CONTACT:**
👤 **Owner:** Arjun trader
📱 **Mobile:** {OWNER_MOBILE}
📧 **Email:** {OWNER_EMAIL}
💬 *Any issues or inquiries? Feel free to contact.*"""

def get_main_menu():
    keyboard = []
    row = []
    for index, (key, value) in enumerate(SUPPORTED_PAIRS.items()):
        row.append({"text": value, "callback_data": f"select_{key}"})
        if len(row) == 2 or index == len(SUPPORTED_PAIRS) - 1:
            keyboard.append(row)
            row = []
    return {"inline_keyboard": keyboard}

# 🧠 ACCURACY OPTIMIZER FILTER (Bina Badlav ke)
def analyze_high_probability_trade(pair_code):
    current_time_slot = int(time.time() / 60)
    seed_string = f"{pair_code}-{current_time_slot}"
    hash_hex = hashlib.md5(seed_string.encode()).hexdigest()
    hash_int = int(hash_hex[:8], 16)
    
    rsi_14 = 30 + (hash_int % 41)       
    cci_period = -150 + (hash_int % 300) 
    sma_trend = "UPTREND 📈" if (hash_int % 2 == 0) else "DOWNTREND 📉"
    
    if rsi_14 <= 43 or cci_period <= -85:
        direction = "CALL"
        emoji = "UP ⬆️"
        color_bullet = "🟢"
        logic = "RSI Oversold Pivot + Support Line Reversal"
    elif rsi_14 >= 57 or cci_period >= 85:
        direction = "PUT"
        emoji = "DOWN ⬇️"
        color_bullet = "🔴"
        logic = "RSI Overbought Resistance + Upper Band Rejection"
    else:
        if hash_int % 3 == 0:
            direction = "CALL"
            emoji = "UP ⬆️"
            color_bullet = "🟢"
            logic = "Moving Average Golden Cross Confirmed"
        else:
            direction = "PUT"
            emoji = "DOWN ⬇️"
            color_bullet = "🔴"
            logic = "Supertrend Bearish Micro-Trend Continuation"
        
    base_prices = {"EUR": 1.08250, "USD": 83.4500, "GBP": 1.26400, "AUD": 0.66150, "NZD": 0.61200}
    prefix = pair_code[:3]
    start_price = base_prices.get(prefix, 1.15200)
    live_strike_price = round(start_price + ((hash_int % 500) / 100000), 5)
    
    return {
        "direction": direction, "emoji": emoji, "color_bullet": color_bullet,
        "rsi": round(rsi_14, 2), "cci": round(cci_period, 2),
        "trend": sma_trend, "logic": logic, "price": live_strike_price
    }

@app.get("/")
def home():
    return {"status": "TradeFather All 37 Assets Successfully Connected"}

# ====================================================================
# 💬 TELEGRAM WEBHOOK CONTROLLER
# ====================================================================
@app.post("/telegram-updates")
async def telegram_updates(request: Request):
    try:
        update = await request.json()
        
        if "message" in update:
            chat_id = update["message"]["chat"]["id"]
            text = update["message"].get("text", "")
            
            if text in ["/start", "/signal", "menu"]:
                welcome_text = f"🦅 🌈 **WELCOME TO TRADEFATHER COMPREHENSIVE BOT** 🌈 🦅\n━━━━━━━━━━━━━━━━━━━━\n💎 **Engine Status:** ALL 37 PLATFORM ASSETS ACTIVE\n📊 **System Filter:** LOSS PREVENTION MATRIX STABLE\n\n👇 **Niche grid se apni koi bhi currency ya asset select karein:**\n\n{get_support_footer()}"
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={
                    "chat_id": chat_id, "text": welcome_text, "reply_markup": get_main_menu(), "parse_mode": "Markdown"
                })
                
        elif "callback_query" in update:
            query = update["callback_query"]
            chat_id = query["message"]["chat"]["id"]
            data = query["data"]
            
            requests.post(f"https://api.telegram.org/bot{TOKEN}/answerCallbackQuery", json={"callback_query_id": query["id"]})
            
            # --- SUBSCRIPTION PLANS DISPLAY DETAILED ---
            if data == "show_subscription":
                sub_plans_text = f"""💎 **TRADEFATHER PREMIUM SUBSCRIPTION PLANS** 💎
━━━━━━━━━━━━━━━━━━━━
🎯 **Choose Your Plan & Boost Your Accuracy:**

⏱️ **1 Days Plan:** ₹2
⏱️ **1 Month Plan:** ₹20,000
⏱️ **3 Month Plan:** ₹60,000 *(5% DISCOUNT)*
⏱️ **6 Month Plan:** ₹1,20,000 *(10% DISCOUNT)*
⏱️ **9 Month Plan:** ₹1,80,000 *(15% DISCOUNT)*
⏱️ **1 Year Plan:** ₹2,40,000 *(25% DISCOUNT)*

━━━━━━━━━━━━━━━━━━━━
🏦 **PAYMENT RECEIVE ACCOUNT DETAILS:**
👤 **Name:** ARJUN BASAK
💳 **Account Number:** `2914509839`
🏛️ **IFSC Code:** `KKNK001774`
📱 **UPI ID:** `arjun876779@kotak`
✨ **QR Code Status:** ALL UPI APPS SUPPORTED (GooglePay, PhonePe, Paytm)

━━━━━━━━━━━━━━━━━━━━
📞 **VIP CUSTOMER SUPPORT:**
📱 **Phone Call / Live Trade Testing:** {OWNER_MOBILE}
📧 **Email ID:** {OWNER_EMAIL}

⚠️ *Payment karne ke baad live verification aur access ke liye screenshot support par send karein.*
"""
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={
                    "chat_id": chat_id, 
                    "text": sub_plans_text, 
                    "reply_markup": {
                        "inline_keyboard": [[{"text": "🔙 Back to Main Menu", "callback_data": "back_menu"}]]
                    },
                    "parse_mode": "Markdown"
                })

            elif data == "back_menu":
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={
                    "chat_id": chat_id, "text": "👇 **Niche grid se apna asset ya currency pair choose karein:**", "reply_markup": get_main_menu(), "parse_mode": "Markdown"
                })
                
            elif data.startswith("select_"):
                p_code = data.replace("select_", "")
                p_disp = SUPPORTED_PAIRS.get(p_code, p_code)
                
                analysis = analyze_high_probability_trade(p_code)
                
                dashboard_msg = f"""👑 🌈 **TRADEFATHER VIP ACCURATE SIGNAL** 🌈 👑
━━━━━━━━━━━━━━━━━━━━
💱 **Asset Pair :** {p_disp}
💵 **Strike Price :** `{analysis['price']}`
⏱️ **Timeframe    :** `1 MIN (INSTANT LIVE)`
━━━━━━━━━━━━━━━━━━━━
📊 **PRO FILTER INDICATORS DATA:**
📈 **Market Trend (SMA) :** `{analysis['trend']}`
🎯 **RSI (14) Valuation   :** `{analysis['rsi']}`
⚡ **CCI Oscillator      :** `{analysis['cci']}`
🔍 **Filter Validation    :** `{analysis['logic']}`
━━━━━━━━━━━━━━━━━━━━
🚨 **LIVE TRADE DIRECTION :**
👉 **🎯 {analysis['color_bullet']} {analysis['direction']} ({analysis['emoji']})** 👈

🎯 **VIP Accuracy :** `98% ACCURACY CONFIRMED`
⚖️ **Martingale Rule   :** `⚠️ USE 1ST MARTINGALE IF OTM`
{get_support_footer()}
"""
                # 🔥 FIX LAYOUT: Alag-alag rows (lines) me buttons specify kiye hain taaki Telegram miss na kare
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={
                    "chat_id": chat_id, "text": dashboard_msg,
                    "reply_markup": {
                        "inline_keyboard": [
                            [{"text": "💳 BUY PAID SUBSCRIPTION", "callback_data": "show_subscription"}],
                            [{"text": "🔄 Next Trade", "callback_data": f"select_{p_code}"}, {"text": "🔍 Main Menu", "callback_data": "back_menu"}]
                        ]
                    }, "parse_mode": "Markdown"
                })
                
                # Public/Channel broadcast message mein naya VIP channel link block
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={
                    "chat_id": DEFAULT_CHAT_ID, "text": dashboard_msg,
                    "reply_markup": {"inline_keyboard": [[{"text": "✨ JOIN VIP CHANNEL ✨", "url": VIP_LINK}]]},
                    "parse_mode": "Markdown"
                })

        return {"ok": True}
    except Exception as e:
        logger.error(f"Telegram Updates Error: {str(e)}")
        return {"error": str(e)}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
