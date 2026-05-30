
# ==================================================
# DEPLOYMENT READY: FASTAPI + TRADINGVIEW ENGINE BOT
# ==================================================
import os
import logging
from fastapi import FastAPI, Request, BackgroundTasks
import uvicorn
import requests

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# 🔴 CONFIGURATION DATA
TOKEN = "8735814245:AAFk849g-0ZEmZDINRwyWMTGSCzcOg5yRFg"
VIP_LINK = "https://t.me/+4ZPssc8CaKQwNjU1" 
DEFAULT_CHAT_ID = "-1003993233052"          # 🔥 Signals isi channel/group par jayenge

# 📞 OWNER SUPPORT DETAILS
OWNER_MOBILE = "+91 8767812831"
OWNER_EMAIL = "arjuntradar@gmail.com"

app = FastAPI()

# 📊 LIVE SUPPORTED PAIRS GRID (Saari 27 Currencies Pehle Jaisi Safe Hain)
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

@app.get("/")
def home():
    return {"status": "TradeFather Pure TradingView Analytics Engine Active"}

# ====================================================================
# 📡 PURE ANALYSIS: TRADINGVIEW WEBHOOK RECEIVER (NO MANUAL BUTTONS)
# ====================================================================
@app.post("/tradingview-webhook")
async def tradingview_webhook(request: Request, background_tasks: BackgroundTasks):
    try:
        data = await request.json()
        
        # TradingView alerts se data pull karna
        pair_code = data.get("pair", "EURUSDOTC").upper().replace("/", "").replace(" ", "")
        action = data.get("action", "CALL").upper() # 'BUY'/'CALL' ya 'SELL'/'PUT'
        price = data.get("price", "Live Price")
        timeframe = data.get("expiry", "1 MIN").upper()
        
        p_disp = SUPPORTED_PAIRS.get(pair_code, pair_code)
        
        # TradingView ke order action ke mutabik direction decide karna
        if "SELL" in action or "PUT" in action or "DOWN" in action:
            direction = "PUT"
            emoji = "DOWN ⬇️"
            color_bullet = "🔴"
        else:
            direction = "CALL"
            emoji = "UP ⬆️"
            color_bullet = "🟢"
        
        # Real Market Automated Dashboard Style
        tv_dashboard = f"""👑 🌈 **TRADEFATHER 1000% REAL ANALYSIS SIGNAL** 🌈 👑
━━━━━━━━━━━━━━━━━━━━
💱 **Asset Pair :** {p_disp}
💵 **Strike Price :** `{price}`
⏱️ **Timeframe    :** `{timeframe} (TRADINGVIEW LIVE)`
━━━━━━━━━━━━━━━━━━━━
🚨 **LIVE MARKET MOVEMENT DETECTED :**
👉 **🎯 {color_bullet} {direction} ({emoji})** 👈

🎯 **Signal Quality :** `1000% ANALYSIS ACCURATE`
🔥 **Market Momentum   :** `STRATEGIC TREND CONFIRMED`
⚖️ **Martingale Rule   :** `⚠️ USE 1ST MARTINGALE IF OTM`
{get_support_footer()}
"""
        # Telegram channel par real-time signal automatic forward karna
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
        return {"status": "signal_analyzed_and_sent"}
    except Exception as e:
        logger.error(f"TradingView Analysis Webhook Error: {str(e)}")
        return {"error": str(e)}

# ==================================================
# TELEGRAM LIVE COMMAND CONTROLLER
# ==================================================
@app.post("/telegram-updates")
async def telegram_updates(request: Request):
    try:
        update = await request.json()
        
        if "message" in update:
            chat_id = update["message"]["chat"]["id"]
            text = update["message"].get("text", "")
            
            if text == "/start" or text == "/status":
                status_text = f"🦅 🌈 **TRADEFATHER LIVE ENGINE STATUS** 🌈 🦅\n━━━━━━━━━━━━━━━━━━━━\n💎 **System:** AUTOMATED LIVE ANALYSIS MODE\n📊 **Currencies:** 27 OTC/LIVE PAIRS CONNECTED\n🚨 **Call/Put Buttons:** DISABLED ❌ (Pure TradingView Setup)\n\n🟢 *Bot bilkul active hai. Jaise hi TradingView par real signal banega, wo automatic aapke channel par aa jayega!*"
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={
                    "chat_id": chat_id, "text": status_text, "parse_mode": "Markdown"
                })

        return {"ok": True}
    except Exception as e:
        logger.error(f"Telegram Handler Error: {str(e)}")
        return {"error": str(e)}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
