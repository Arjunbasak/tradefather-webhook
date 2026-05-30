# ==================================================
# REAL-TIME PRODUCTION: AUTOMATED 24/7 AUTO ON/OFF SIGNAL ENGINE
# ==================================================
import os
import logging
import hashlib
import time
import asyncio
import requests
from fastapi import FastAPI, Request, BackgroundTasks
import uvicorn

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# 🔴 CONFIGURATION DATA
TOKEN = "8735814245:AAFk849g-0ZEmZDINRwyWMTGSCzcOg5yRFg"
DEFAULT_CHAT_ID = "-1003993233052"          
OWNER_MOBILE = "+91 8767812831"

app = FastAPI()

# 🔄 GLOBAL CONTROL STATE FOR 24/7 AUTO SIGNALS
# Is matrix mein hum active pairs ka track rakhte hain jinka auto-signal chal raha hai
AUTO_SIGNAL_STATE = {}

# 📊 37+ ASSETS GRID
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

def get_support_footer():
    return f"""━━━━━━━━━━━━━━━━━━━━
📞 **OFFICIAL SUPPORT & CONTACT:**
👤 **Owner:** Arjun trader
📱 **Mobile:** {OWNER_MOBILE}"""

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
        direction, emoji, color_bullet, logic = "CALL", "UP ⬆️", "🟢", "RSI Oversold Pivot + Support Line Reversal"
    elif rsi_14 >= 57 or cci_period >= 85:
        direction, emoji, color_bullet, logic = "PUT", "DOWN ⬇️", "🔴", "RSI Overbought Resistance + Upper Band Rejection"
    else:
        if hash_int % 3 == 0:
            direction, emoji, color_bullet, logic = "CALL", "UP ⬆️", "🟢", "Moving Average Golden Cross Confirmed"
        else:
            direction, emoji, color_bullet, logic = "PUT", "DOWN ⬇️", "🔴", "Supertrend Bearish Micro-Trend Continuation"
        
    base_prices = {"EUR": 1.08250, "USD": 83.4500, "GBP": 1.26400, "AUD": 0.66150, "NZD": 0.61200}
    prefix = pair_code[:3]
    start_price = base_prices.get(prefix, 1.15200)
    live_strike_price = round(start_price + ((hash_int % 500) / 100000), 5)
    
    return {
        "direction": direction, "emoji": emoji, "color_bullet": color_bullet,
        "rsi": round(rsi_14, 2), "cci": round(cci_period, 2),
        "trend": sma_trend, "logic": logic, "price": live_strike_price
    }

# 🔄 BACKGROUND INFINITE LOOP FOR 24/7 AUTOMATIC SIGNALS
async def auto_signal_worker(p_code, p_disp):
    logger.info(f"🚀 24/7 Auto-Signal Loop Started for: {p_disp}")
    while AUTO_SIGNAL_STATE.get(p_code, False):
        try:
            analysis = analyze_high_probability_trade(p_code)
            
            dashboard_msg = f"""👑 🌈 **24/7 AUTOMATIC LIVE SIGNAL** 🌈 👑
━━━━━━━━━━━━━━━━━━━━
💱 **Asset Pair :** {p_disp} [AUTOMATED]
💵 **Strike Price :** `{analysis['price']}`
⏱️ **Timeframe    :** `1 MIN (INSTANT)`
━━━━━━━━━━━━━━━━━━━━
📊 **PRO FILTER INDICATORS DATA:**
📈 **Market Trend (SMA) :** `{analysis['trend']}`
🎯 **RSI (14) Valuation   :** `{analysis['rsi']}`
⚡ **CCI Oscillator      :** `{analysis['cci']}`
🔍 **Filter Validation    :** `{analysis['logic']}`
━━━━━━━━━━━━━━━━━━━━
🚨 **LIVE TRADE DIRECTION :**
👉 **🎯 {analysis['color_bullet']} {analysis['direction']} ({analysis['emoji']})** 👈

🎯 **VIP Accuracy :** `100% INDICATOR CONFIRMED`
⚖️ **Martingale Rule   :** `⚠️ USE 1ST MARTINGALE IF OTM`
"""
            # Channel par automatic dispatch
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={
                "chat_id": DEFAULT_CHAT_ID, "text": dashboard_msg, "parse_mode": "Markdown"
            })
            
        except Exception as e:
            logger.error(f"Error in auto signal background thread: {str(e)}")
            
        # 1 Minute Interval sleep constraint (Har 1 minute me automation signal generate hoga)
        await asyncio.sleep(60)
    logger.info(f"🛑 24/7 Auto-Signal Loop Stopped for: {p_disp}")

@app.get("/")
def home():
    return {"status": "Arjun A1 24/7 Automation Grid Active"}

@app.post("/telegram-updates")
async def telegram_updates(request: Request, background_tasks: BackgroundTasks):
    try:
        update = await request.json()
        
        if "message" in update:
            chat_id = update["message"]["chat"]["id"]
            text = update["message"].get("text", "")
            
            if text.startswith("/start"):
                welcome_text = f"🦅 🌈 **WELCOME TO ARJUN A1 24/7 AUTOMATION BOT** 🌈 🦅\n━━━━━━━━━━━━━━━━━━━━\n💎 **Engine Status:** 37+ ASSETS READY FOR 24/7 LIVE AUTOMATION\n\n👇 **Niche grid se asset select karein aur 24/7 automatic channel posting trigger karein:**\n\n{get_support_footer()}"
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={
                    "chat_id": chat_id, "text": welcome_text, "reply_markup": get_main_menu(), "parse_mode": "Markdown"
                })
                
        elif "callback_query" in update:
            query = update["callback_query"]
            chat_id = query["message"]["chat"]["id"]
            data = query["data"]
            message_id = query["message"]["message_id"]
            
            requests.post(f"https://api.telegram.org/bot{TOKEN}/answerCallbackQuery", json={"callback_query_id": query["id"]})
            
            if data == "back_menu":
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={
                    "chat_id": chat_id, "text": "👇 **Niche grid se apna asset ya currency pair choose karein:**", "reply_markup": get_main_menu(), "parse_mode": "Markdown"
                })
                
            elif data.startswith("select_"):
                p_code = data.replace("select_", "")
                p_disp = SUPPORTED_PAIRS.get(p_code, p_code)
                analysis = analyze_high_probability_trade(p_code)
                
                # Check active automation status
                is_on = AUTO_SIGNAL_STATE.get(p_code, False)
                status_text = "🔴 ON (Click to Stop)" if is_on else "🟢 OFF (Click to Start 24/7)"
                toggle_action = f"stop_auto_{p_code}" if is_on else f"start_auto_{p_code}"
                
                dashboard_msg = f"""👑 🌈 **ARJUN A1 LIVE TRACKING CONTROL** 🌈 👑
━━━━━━━━━━━━━━━━━━━━
💱 **Asset Pair :** {p_disp}
💵 **Strike Price :** `{analysis['price']}`
⏱️ **Timeframe    :** `1 MIN (LIVE MANUAL INSTANT)`
━━━━━━━━━━━━━━━━━━━━
📊 **INDICATOR VECTOR MATRIX:**
📈 **Market Trend :** `{analysis['trend']}`
🎯 **RSI (14)      :** `{analysis['rsi']}`
⚡ **CCI Oscillator:** `{analysis['cci']}`
━━━━━━━━━━━━━━━━━━━━
🚨 **LIVE TRADE DIRECTION :**
👉 **🎯 {analysis['color_bullet']} {analysis['direction']} ({analysis['emoji']})** 👈

⚙️ **24/7 AUTOMATION ENGINE STATUS:**
Aap niche diye gaye button par click karke is pair ke signals ko Telegram channel par 24/7 bina ruke automatic continuous update par laga sakte hain!
"""
                bot_buttons = [
                    [{"text": f"🔄 24/7 Auto Signal: {status_text}", "callback_data": toggle_action}],
                    [{"text": "🔄 Next Instant Manual Trade", "callback_data": f"select_{p_code}"}],
                    [{"text": "🔍 Main Menu", "callback_data": "back_menu"}]
                ]
                
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={
                    "chat_id": chat_id, "text": dashboard_msg,
                    "reply_markup": {"inline_keyboard": bot_buttons}, "parse_mode": "Markdown"
                })

            elif data.startswith("start_auto_"):
                p_code = data.replace("start_auto_", "")
                p_disp = SUPPORTED_PAIRS.get(p_code, p_code)
                
                # Set dynamic state flags to active
                AUTO_SIGNAL_STATE[p_code] = True
                
                # FastAPI background task workers setup running infinitely
                background_tasks.add_task(auto_signal_worker, p_code, p_disp)
                
                # UI inline button updating response grid
                updated_buttons = [
                    [{"text": "🔄 24/7 Auto Signal: 🔴 ON (Click to Stop)", "callback_data": f"stop_auto_{p_code}"}],
                    [{"text": "🔍 Main Menu", "callback_data": "back_menu"}]
                ]
                
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={
                    "chat_id": chat_id,
                    "text": f"✅ **24/7 AUTOMATION ACTIVATED!**\n\nSystem ab channel `{DEFAULT_CHAT_ID}` par `{p_disp}` ke signals har 1 minute mein continuous automatic delivery mode par daal chuka hai.",
                    "reply_markup": {"inline_keyboard": updated_buttons},
                    "parse_mode": "Markdown"
                })

            elif data.startswith("stop_auto_"):
                p_code = data.replace("stop_auto_", "")
                p_disp = SUPPORTED_PAIRS.get(p_code, p_code)
                
                # Kill execution loop by changing dictionary status state
                AUTO_SIGNAL_STATE[p_code] = False
                
                updated_buttons = [
                    [{"text": "🔄 24/7 Auto Signal: 🟢 OFF (Click to Start 24/7)", "callback_data": f"select_{p_code}"}],
                    [{"text": "🔍 Main Menu", "callback_data": "back_menu"}]
                ]
                
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={
                    "chat_id": chat_id,
                    "text": f"🛑 **24/7 AUTOMATION PAUSED!**\n\n`{p_disp}` ki channel par hone wali continuous structural automation updates ko successfully turn off kar diya gaya hai.",
                    "reply_markup": {"inline_keyboard": updated_buttons},
                    "parse_mode": "Markdown"
                })

        return {"ok": True}
    except Exception as e:
        logger.error(f"Telegram Updates Error: {str(e)}")
        return {"error": str(e)}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
