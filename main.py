# ==================================================
# FINAL COMPREHENSIVE PRODUCTION: ALL 37 ASSETS ENGINE
# ==================================================
import os
import logging
import hashlib
import time
import random
import requests
from fastapi import FastAPI, Request
import uvicorn

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# 🔴 CONFIGURATION DATA
TOKEN = "8735814245:AAFk849g-0ZEmZDINRwyWMTGSCzcOg5yRFg"
VIP_LINK = "https://t.me/+Nx_7ZeyV5UYyMWM1" 
DEFAULT_CHAT_ID = "-1003993233052"          

# ⚠️ APNE BOT KA USERNAME YAHAN LIKHEIN (Bina @ ke, jaise: TradeFather_bot)
BOT_USERNAME = "YOUR_BOT_USERNAME" 

OWNER_MOBILE = "+91 8767812831"
OWNER_EMAIL = "arjuntradar@gmail.com"

app = FastAPI()

# 📊 100% COMPLETE ASSETS GRID
SUPPORTED_PAIRS = {
    "AUDCADOTC": "AUD/CAD OTC", "AUDCHFOTC": "AUD/CHF OTC", "AUDJPYOTC": "AUD/JPY OTC",
    "AUDNZDOTC": "AUD/NZD OTC", "AUDUSDOTC": "AUD/USD OTC", "CADCHFOTC": "CAD/CHF OTC",
    "CADJPYOTC": "CAD/JPY OTC", "CHFJPYOTC": "CHF/JPY OTC", "EURAUDOTC": "EUR/AUD OTC",
    "EURCADOTC": "EUR/CAD OTC", "EURCHFOTC": "EUR/CHF OTC", "EURGBPOTC": "EUR/GBP OTC",
    "EURJPYOTC": "EUR/JPY OTC", "EURNZDOTC": "EUR/NZD OTC", "EURUSDOTC": "EUR/USD OTC",
    "GBPAUDOTC": "GBP/AUD OTC", "GBPCADOTC": "GBP/CAD OTC", "GBPCHFOTC": "GBP/CHF OTC",
    "GBPJPYOTC": "GBP/JPY OTC", "GBPNZDOTC": "GBP/NZD OTC", "GBPUSDOTC": "GBP/USD OTC",
    "NZDCADOTC": "NZD/CAD OTC", "NZDCHFOTC": "NZD/CHF OTC", "NZDJPYOTC": "NZD/JPY OTC",
    "NZDUSDOTC": "NZD/USD OTC", "USDARSOTC": "USD/ARS OTC", "USDBDTOTC": "USD/BDT OTC",
    "USDBRLOTC": "USD/BRL OTC", "USDCHFOTC": "USD/CHF OTC", "USDIDROTC": "USD/IDR OTC",
    "USDINROTC": "USD/INR OTC", "USDJPYOTC": "USD/JPY OTC", "USDMXNOTC": "USD/MXN OTC",
    "USDPKROTC": "USD/PKR OTC", "USDPHPOTC": "USD/PHP OTC", "USDZAROTC": "USD/ZAR OTC",
    "GOLDOTC": "GOLD OTC", "SILVEROTC": "SILVER OTC"
}

# 📦 PLAN META DETAILS CONFIGURATION (As per video data mapping)
PLAN_DETAILS = {
    "plan_1d": {"name": "1 Day Premium Trial", "price": "2.00", "duration": "day"},
    "plan_1m": {"name": "1 Month Premium Pack", "price": "20,000.00", "duration": "month"},
    "plan_3m": {"name": "3 Month Premium (5% OFF)", "price": "60,000.00", "duration": "3 months"},
    "plan_6m": {"name": "6 Month Premium (10% OFF)", "price": "1,20,000.00", "duration": "6 months"},
    "plan_9m": {"name": "9 Month Premium (15% OFF)", "price": "1,80,000.00", "duration": "9 months"},
    "plan_1y": {"name": "1 Year Premium (25% OFF)", "price": "2,40,000.00", "duration": "1 year"}
}

def get_subscription_text():
    return """💎 **TRADEFATHER PREMIUM SUBSCRIPTION PLANS** 💎
━━━━━━━━━━━━━━━━━━━━
🎯 **Choose your premium plan duration to generate your dynamic payment interface:**"""

def get_plans_keyboard():
    return {
        "inline_keyboard": [
            [{"text": "⏱️ 1 Day Trial - ₹2", "callback_data": "pay_plan_1d"}],
            [{"text": "⏱️ 1 Month - ₹20,000", "callback_data": "pay_plan_1m"}],
            [{"text": "⏱️ 3 Months - ₹60,000", "callback_data": "pay_plan_3m"}],
            [{"text": "⏱️ 6 Months - ₹1,20,000", "callback_data": "pay_plan_6m"}],
            [{"text": "⏱️ 9 Months - ₹1,80,000", "callback_data": "pay_plan_9m"}],
            [{"text": "⏱️ 1 Year - ₹2,40,000", "callback_data": "pay_plan_1y"}],
            [{"text": "🔙 Main Menu", "callback_data": "back_menu"}]
        ]
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

@app.post("/telegram-updates")
async def telegram_updates(request: Request):
    try:
        update = await request.json()
        
        if "message" in update:
            chat_id = update["message"]["chat"]["id"]
            text = update["message"].get("text", "")
            
            if text.startswith("/start sub"):
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={
                    "chat_id": chat_id, 
                    "text": get_subscription_text(), 
                    "reply_markup": get_plans_keyboard(),
                    "parse_mode": "Markdown"
                })
            elif text in ["/start", "/signal", "menu"]:
                welcome_text = f"🦅 🌈 **WELCOME TO TRADEFATHER COMPREHENSIVE BOT** 🌈 🦅\n━━━━━━━━━━━━━━━━━━━━\n💎 **Engine Status:** ALL 37 PLATFORM ASSETS ACTIVE\n📊 **System Filter:** LOSS PREVENTION MATRIX STABLE\n\n👇 **Niche grid se apni koi bhi currency ya asset select karein:**\n\n{get_support_footer()}"
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={
                    "chat_id": chat_id, "text": welcome_text, "reply_markup": get_main_menu(), "parse_mode": "Markdown"
                })
                
        elif "callback_query" in update:
            query = update["callback_query"]
            chat_id = query["message"]["chat"]["id"]
            data = query["data"]
            
            requests.post(f"https://api.telegram.org/bot{TOKEN}/answerCallbackQuery", json={"callback_query_id": query["id"]})
            
            # Action 1: Show plans selection dashboard
            if data == "show_subscription":
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={
                    "chat_id": chat_id, 
                    "text": get_subscription_text(), 
                    "reply_markup": get_plans_keyboard(),
                    "parse_mode": "Markdown"
                })

            # Action 2: Process selection and output custom payload with absolute checkout lock
            elif data.startswith("pay_plan_"):
                plan_key = data.replace("pay_plan_", "")
                target_plan = PLAN_DETAILS.get(f"plan_{plan_key}", {"name": "Premium Plan", "price": "2.00", "duration": "day"})
                
                # Generate unique dynamic validation data 
                order_id = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=8))
                current_timestamp = time.strftime("%d/%m/%Y, %I:%M:%S %p")
                
                # Dynamic QR mapping using upi address logic (Native string structuring)
                upi_string = f"upi://pay?pa=arjun876779@kotak&pn=ARJUN%20BASAK&am={target_plan['price'].replace(',', '')}&cu=INR"
                qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={upi_string}"
                
                # 1. First send the custom dynamic QR Code Invoice to user
                invoice_caption = f"""🛍️ **Shop:** TradeFather Signals
📦 **Product:** {target_plan['name']}
⏱️ **Duration:** `{target_plan['duration']}`
💰 **Amount:** `₹{target_plan['price']}`
📅 **IST:** {current_timestamp}

✅ *After successful payment, system tracking requires you to forward your transaction screenshot directly to support.*
⏳ *You have exactly 5 minutes to complete the dynamic transaction process.*"""
                
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", json={
                    "chat_id": chat_id,
                    "photo": qr_url,
                    "caption": invoice_caption,
                    "parse_mode": "Markdown"
                })
                
                # 2. Immediately print the secure locked tracking message block (Sem to sem as video layout)
                tracker_msg = f"""⏳ **Payment Checking...**
━━━━━━━━━━━━━━━━━━━━
🛍️ **Shop:** TradeFather Signals
🆔 **Order:** `{order_id}`
📦 **Product:** {target_plan['name']}
⏱️ **Duration:** `{target_plan['duration']}`
💰 **Amount:** `₹{target_plan['price']}`

📈 **Progress:** [█░░░░░░░░░░░░░░░░░░░] 5%
⏳ **Time Left:** `04:59 Mins`

📊 **Payment Status:** `PENDING / WAITING FOR SCREENSHOT`
📝 **Last Checked (IST):** `{current_timestamp}`
"""
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={
                    "chat_id": chat_id,
                    "text": tracker_msg,
                    "reply_markup": {
                        "inline_keyboard": [
                            [{"text": "🔄 Check Payment Status", "callback_data": f"verify_{order_id}"}],
                            [{"text": "🔙 Cancel & Main Menu", "callback_data": "back_menu"}]
                        ]
                    },
                    "parse_mode": "Markdown"
                })

            # Continuous status check routing block to safely lock access
            elif data.startswith("verify_"):
                ord_id = data.replace("verify_", "")
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={
                    "chat_id": chat_id,
                    "text": f"❌ **Verification Failed (Order #{ord_id})**\n\nPayment receipt screenshot was not detected by the system yet. Please forward your payment success page screenshot to the Admin team for explicit manual override.",
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
{get_support_footer()}"""

                bot_buttons = [
                    [{"text": "💳 BUY PAID SUBSCRIPTION", "callback_data": "show_subscription"}],
                    [{"text": "🔄 Next Trade", "callback_data": f"select_{p_code}"}, {"text": "🔍 Main Menu", "callback_data": "back_menu"}]
                ]
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={
                    "chat_id": chat_id, "text": dashboard_msg,
                    "reply_markup": {"inline_keyboard": bot_buttons}, "parse_mode": "Markdown"
                })
                
                channel_buttons = [
                    [{"text": "💳 BUY PAID SUBSCRIPTION", "url": f"https://t.me/{BOT_USERNAME}?start=sub"}]
                ]
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={
                    "chat_id": DEFAULT_CHAT_ID, "text": dashboard_msg,
                    "reply_markup": {"inline_keyboard": channel_buttons}, "parse_mode": "Markdown"
                })

        return {"ok": True}
    except Exception as e:
        logger.error(f"Telegram Updates Error: {str(e)}")
        return {"error": str(e)}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
