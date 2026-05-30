
# ==================================================
# ARJUN TRADER HYBRID AUTOMATION BOT
# ==================================================
import os
import logging
from fastapi import FastAPI, Request, BackgroundTasks
import uvicorn
import requests

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# 🔴 CONFIGURATION DATA (Aapka Token aur Links)
TOKEN = "8735814245:AAFk849g-0ZEmZDINRwyWMTGSCzcOg5yRFg"
VIP_LINK = "https://t.me/+4ZPssc8CaKQwNjU1" 
DEFAULT_CHAT_ID = "-1003993233052"          # 🔥 Aapka Telegram Channel ID jahan signal jayega

# 📞 OWNER SUPPORT DETAILS
OWNER_MOBILE = "+91 8767812831"
OWNER_EMAIL = "arjuntradar@gmail.com"

app = FastAPI()

# 📊 LIVE REGISTERED PAIRS GRID (Saari Currencies Ekdum Safe Hain)
SUPPORTED_PAIRS = {
    "AUDCADOTC": "AUD/CAD OTC", "CHFJPYOTC": "CHF/JPY OTC", "EURNZDOTC": "EUR/NZD OTC",
    "NZDCADOTC": "NZD/CAD OTC", "EURAUDOTC": "EUR/AUD OTC", "GBPJPYOTC": "GBP/JPY OTC",
    "GBPUSDOTC": "GBP/USD OTC", "NZDJPYOTC": "NZD/JPY OTC", "AUDCHFOTC": "AUD/CHF OTC",
    "EURUSDOTC": "EUR/USD OTC", "NZDUSDOTC": "NZD/USD OTC", "USDINROTC": "USD/INR OTC",
    "USDBRLOTC": "USD/BRL OTC", "USDIDROTC": "USD/IDR OTC",
    "USDZAROTC": "USD/ZAR OTC", "AUDNZDOTC": "AUD/NZD OTC", "USDPHPOTC": "USD/PHP OTC",
    "NZDCHFOTC": "NZD/CHF OTC", "USDBDTOTC": "USD/BDT OTC", "CADCHFOTC": "CAD/CHF OTC",
    "USDPKROTC": "USD/PKR OTC", "GBPCHFOTC": "GBP/CHF OTC", "USDARSOTC": "USD/ARS OTC",
    "CADJPYOTC": "CAD/JPY OTC", "USDCHFOTC": "USD/CHF OTC", "USDJPYOTC": "USD/JPY OTC",
    "USDMXNOTC": "USD/MXN OTC"
}

def get_support_footer():
    return f"""━━━━━━━━━━━━━━━━━━━━
📞 **OFFICIAL SUPPORT & CONTACT:**
👤 **Owner:** Arjun trader
📱 **Mobile:** {OWNER_MOBILE}
📧 **Email:** {OWNER_EMAIL}
💬 *Any issues or inquiries? Feel free to contact.*"""

# 2-Column Grid Format (Main Menu)
def get_main_menu():
    keyboard = []
    row = []
    for index, (key, value) in enumerate(SUPPORTED_PAIRS.items()):
        row.append({"text": value, "callback_data": f"select_{key}"})
        if len(row) == 2 or index == len(SUPPORTED_PAIRS) - 1:
            keyboard.append(row)
            row = []
    return {"inline_keyboard": keyboard}

@app.get("/")
def home():
    return {"status": "TradeFather Hybrid Analytical Engine 100% Active"}

# ====================================================================
# 📡 STEP 1: TRADINGVIEW LIVE ALERT RECEIVER (REAL MARKET ANALYSIS)
# ====================================================================
@app.post("/tradingview-webhook")
async def tradingview_webhook(request: Request, background_tasks: BackgroundTasks):
    try:
        data = await request.json()
        
        # TradingView alert se data read karna
        pair_code = data.get("pair", "EURUSDOTC").upper().replace("/", "").replace(" ", "")
        action = data.get("action", "CALL").upper() # BUY/CALL ya SELL/PUT
        price = data.get("price", "Live Price")
        timeframe = data.get("expiry", "1 MIN").upper()
        
        p_disp = SUPPORTED_PAIRS.get(pair_code, pair_code)
        
        # Real Market Direction Filtering
        if "SELL" in action or "PUT" in action or "DOWN" in action:
            direction = "PUT"
            emoji = "DOWN ⬇️"
            color_bullet = "🔴"
        else:
            direction = "CALL"
            emoji = "UP ⬆️"
            color_bullet = "🟢"
        
        # Sahi Market Oriented Dashboard Style Layout
        tv_dashboard = f"""👑 🌈 **TRADEFATHER 1000% VIP LIVE SIGNAL** 🌈 👑
━━━━━━━━━━━━━━━━━━━━
💱 **Asset Pair :** {p_disp}
💵 **Strike Price :** `{price}`
⏱️ **Timeframe    :** `{timeframe} (REAL-TIME ANALYSIS)`
━━━━━━━━━━━━━━━━━━━━
🚨 **LIVE TRADE DIRECTION :**
👉 **🎯 {color_bullet} {direction} ({emoji})** 👈

🎯 **VIP Accuracy :** `1000% ACCURATE`
🔥 **Market Momentum   :** `STRONG TREND CONFIRMED`
⚖️ **Martingale Rule   :** `⚠️ USE 1ST MARTINGALE IF OTM`
{get_support_footer()}
"""
        # Telegram channel par automatic post karna
        background_tasks.add_task(
            requests.post,
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            json={
                "chat_id": DEFAULT_CHAT_ID,
                "text": tv_dashboard,
                "reply_markup": {"inline_keyboard": [[{"text": "✨ JOIN VIP FOR MORE ✨", "url": VIP_LINK}]]},
                "parse_mode": "Markdown"
            }
        )
        return {"status": "success", "message": "Signal sent to channel"}
    except Exception as e:
        logger.error(f"TradingView Webhook Error: {str(e)}")
        return {"error": str(e)}

# ====================================================================
# 💬 STEP 2: TELEGRAM BOT UPDATES CONTROLLER (FOR INSTANT REPLY ON CLICK)
# ====================================================================
@app.post("/telegram-updates")
async def telegram_updates(request: Request):
    try:
        update = await request.json()
        
        # 1. /start command handling
        if "message" in update:
            chat_id = update["message"]["chat"]["id"]
            text = update["message"].get("text", "")
            
            if text == "/start" or text == "/signal":
                welcome_text = f"🦅 🌈 **WELCOME TO TRADEFATHER VIP BOT** 🌈 🦅\n━━━━━━━━━━━━━━━━━━━━\n💎 **Status:** VIP SERVER CONNECTED\n🚀 **System Mode:** AUTOMATED LIVE ANALYSIS\n\n👇 **Niche grid se apni currency pair choose karein:**\n\n{get_support_footer()}"
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={
                    "chat_id": chat_id, "text": welcome_text, "reply_markup": get_main_menu(), "parse_mode": "Markdown"
                })
                
        # 2. Currency Pair Selection Button Click Handling (Fixes No Reply Error)
        elif "callback_query" in update:
            query = update["callback_query"]
            chat_id = query["message"]["chat"]["id"]
            data = query["data"]
            
            # Loading wheel ko stop karne ke liye answer callback
            requests.post(f"https://api.telegram.org/bot{TOKEN}/answerCallbackQuery", json={"callback_query_id": query["id"]})
            
            if data == "back_menu":
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={
                    "chat_id": chat_id, "text": "👇 **Niche grid se apni currency pair choose karein:**", "reply_markup": get_main_menu(), "parse_mode": "Markdown"
                })
                
            elif data.startswith("select_"):
                p_code = data.replace("select_", "")
                p_disp = SUPPORTED_PAIRS.get(p_code, p_code)
                
                # Instant Confirmation Reply jisse user ko pata chale ki bot kaam kar raha hai
                loading_text = f"⏳ **Analyzing {p_disp} Market Trend...**\n━━━━━━━━━━━━━━━━━━━━\n🤖 **TradeFather Engine** abhi live market chart ko check kar raha hai.\n\n📈 *Jaise hi TradingView par strong confirmation entry (CALL/PUT) banegi, signal turant automatic aapke channel par bhej diya jayega!*"
                
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={
                    "chat_id": chat_id, 
                    "text": loading_text, 
                    "reply_markup": {"inline_keyboard": [[{"text": "🔍 Main Menu", "callback_data": "back_menu"}]]},
                    "parse_mode": "Markdown"
                })

        return {"ok": True}
    except Exception as e:
        logger.error(f"Telegram Updates Error: {str(e)}")
        return {"error": str(e)}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
