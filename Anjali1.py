# ==================================================
# REAL-TIME PRODUCTION: AUTOMATED 24/7 ENGINE (ALL 37+ ASSETS FIXED)
# ==================================================
import os
import logging
import requests
from fastapi import FastAPI, Request
import uvicorn

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# 🔴 CONFIGURATION DATA
TOKEN = "8735814245:AAFk849g-0ZEmZDINRwyWMTGSCzcOg5yRFg"
DEFAULT_CHAT_ID = "-1003993233052"          
OWNER_MOBILE = "+91 8767812831"

app = FastAPI()

# 📊 ALL HIGHLIGHTED 37+ ASSETS MATRIX (ADDED & VERIFIED)
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
    return f"━━━━━━━━━━━━━━━━━━━━\n📞 **OFFICIAL SUPPORT & CONTACT:**\n👤 **Owner:** Arjun trader\n📱 **Mobile:** {OWNER_MOBILE}"

def get_main_menu():
    keyboard = []
    row = []
    for index, (key, value) in enumerate(SUPPORTED_PAIRS.items()):
        row.append({"text": value, "callback_data": f"tv_info_{key}"})
        if len(row) == 2 or index == len(SUPPORTED_PAIRS) - 1:
            keyboard.append(row)
            row = []
    return {"inline_keyboard": keyboard}

@app.get("/")
def home():
    return {"status": "Arjun A1 REAL Webhook Engine Running Seamlessly"}

# 🎯 TRADINGVIEW SE REAL AUTOMATED SIGNALS RECEIVE KARNE KA ENDPOINT
@app.post("/tradingview-webhook")
async def tradingview_webhook(request: Request):
    try:
        data = await request.json()
        logger.info(f"📥 Real Signal Received: {data}")
        
        # TradingView se pairs match karne ka logic
        pair_raw = data.get("pair", "AUDUSDOTC")
        clean_key = pair_raw.replace("/", "").replace(" ", "").upper()
        pair_display = SUPPORTED_PAIRS.get(clean_key, pair_raw)
        
        direction = data.get("direction", "CALL").upper()
        price = data.get("price", "LIVE")
        timeframe = data.get("timeframe", "1 MIN")
        trend = data.get("trend", "ANALYZING 📈")
        rsi = data.get("rsi", "NEUTRAL")
        cci = data.get("cci", "STABLE")
        logic = data.get("logic", "Premium Indicator Breakout")
        
        emoji = "UP ⬆️" if direction == "CALL" else "DOWN ⬇️"
        color_bullet = "🟢" if direction == "CALL" else "🔴"

        dashboard_msg = f"""👑 🌈 **ARJUN A1 PREMIUM LIVE SIGNAL** 🌈 👑
━━━━━━━━━━━━━━━━━━━━
💱 **Asset Pair :** {pair_display} [100% REAL LIVE]
💵 **Strike Price :** `{price}`
⏱️ **Timeframe    :** `{timeframe}`
━━━━━━━━━━━━━━━━━━━━
📊 **PRO FILTER INDICATORS DATA:**
📈 **Market Trend :** `{trend}`
🎯 **RSI Valuation :** `{rsi}`
⚡ **CCI Oscillator :** `{cci}`
🔍 **Filter Validation :** `{logic}`
━━━━━━━━━━━━━━━━━━━━
🚨 **LIVE TRADE DIRECTION :**
👉 **🎯 {color_bullet} {direction} ({emoji})** 👈

🎯 **VIP Accuracy :** `100% REAL INDICATOR CONFIRMED`
⚖️ **Martingale Rule   :** `⚠️ USE 1ST MARTINGALE IF OTM`
"""
        # Telegram Channel Dispatch
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, json={
            "chat_id": DEFAULT_CHAT_ID, "text": dashboard_msg, "parse_mode": "Markdown"
        })
        
        return {"status": "success", "message": "Real Signal Posted To Telegram"}
        
    except Exception as e:
        logger.error(f"Webhook Processing Error: {str(e)}")
        return {"status": "error", "message": str(e)}

# 🔄 TELEGRAM BOT COMMANDS AND MENU HANDLING
@app.post("/telegram-updates")
async def telegram_updates(request: Request):
    try:
        update = await request.json()
        if "message" in update:
            chat_id = update["message"]["chat"]["id"]
            text = update["message"].get("text", "")
            
            if text.startswith("/start"):
                welcome_text = f"🦅 🌈 **WELCOME TO ARJUN A1 REAL WEBHOOK BOT** 🌈 🦅\n━━━━━━━━━━━━━━━━━━━━\n💎 **Engine Status:** 37+ ASSETS READY FOR REAL TRADINGVIEW WEBHOOKS\n\n👇 **Niche pure assets ki grid check karein:**\n\n{get_support_footer()}"
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={
                    "chat_id": chat_id, "text": welcome_text, "reply_markup": get_main_menu(), "parse_mode": "Markdown"
                })
                
        elif "callback_query" in update:
            query = update["callback_query"]
            chat_id = query["message"]["chat"]["id"]
            data = query["data"]
            message_id = query["message"]["message_id"]
            
            requests.post(f"https://api.telegram.org/bot{TOKEN}/answerCallbackQuery", json={"callback_query_id": query["id"]})
            
            if data.startswith("tv_info_"):
                p_code = data.replace("tv_info_", "")
                p_disp = SUPPORTED_PAIRS.get(p_code, p_code)
                
                info_msg = f"⚙️ **{p_disp} Automation Connected**\n\nTradingView Alert settings mein is pair ka naam `{p_disp}` likhein aur message box mein standard JSON data pass karein. Live automatic alerts seedhe channel par chalenge."
                
                requests.post(f"https://api.telegram.org/bot{TOKEN}/editMessageText", json={
                    "chat_id": chat_id, "message_id": message_id, "text": info_msg,
                    "reply_markup": {"inline_keyboard": [[{"text": "🔍 Main Menu", "callback_data": "back_menu"}]]}, "parse_mode": "Markdown"
                })
                
            elif data == "back_menu":
                requests.post(f"https://api.telegram.org/bot{TOKEN}/editMessageText", json={
                    "chat_id": chat_id, "message_id": message_id, "text": "👇 **Niche grid se apna asset ya currency pair choose karein:**",
                    "reply_markup": get_main_menu(), "parse_mode": "Markdown"
                })

        return {"ok": True}
    except Exception as e:
        logger.error(f"Telegram Interface Error: {str(e)}")
        return {"error": str(e)}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
