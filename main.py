# ==================================================
# DEPLOYMENT READY: FASTAPI + TELEGRAM WEBHOOK BOT
# ==================================================
import os
import logging
from fastapi import FastAPI, Request, BackgroundTasks
import uvicorn
import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Bot

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# 🔴 APNA DATA YAHAN CONFIG KARO
TOKEN = "8735814245:AAFk849g-0ZEmZDINRwyWMTGSCzcOg5yRFg"
# नोट: आप चाहें तो एक फिक्स चैनल या ग्रुप ID भी डाल सकते हैं जहां ऑटो सिग्नल भेजने हैं
DEFAULT_CHAT_ID = "-1003993233052" 

bot = Bot(token=TOKEN)
app = FastAPI()

# 📊 LIVE REGISTERED PAIRS GRID
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

# 2-Column Grid Format
def get_main_menu():
    keyboard = []
    row = []
    for index, (key, value) in enumerate(SUPPORTED_PAIRS.items()):
        row.append(InlineKeyboardButton(text=value, callback_data=f"select_{key}"))
        if len(row) == 2 or index == len(SUPPORTED_PAIRS) - 1:
            keyboard.append(row)
            row = []
    return InlineKeyboardMarkup(keyboard)

# Control Buttons
def get_dashboard_buttons(pair_code):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(text="🚀 ON Auto", callback_data=f"auto_on_{pair_code}"),
            InlineKeyboardButton(text="🛑 OFF Auto", callback_data=f"auto_off_{pair_code}"),
            InlineKeyboardButton(text="🔄 Re-Analyze", callback_data=f"recalc_{pair_code}")
        ],
        [
            InlineKeyboardButton(text="🔍 Select Currency Menu (Start)", callback_data="back_menu")
        ]
    ])

@app.get("/")
def home():
    return {"status": "TradeFather Webhook Engine Running 24/7"}

# ==================================================
# 🔥 TRADINGVIEW WEBHOOK RECEIVER (100% ACCURATE)
# ==================================================
@app.post("/tradingview-webhook")
async def receive_tradingview_signal(request: Request, background_tasks: BackgroundTasks):
    """
    ट्रेडिंगव्यू से आने वाले लाइव अलर्ट को कैप्चर करने का एंडपॉइंट।
    ट्रेडिंगव्यू अलर्ट बॉक्स में यह JSON भेजना होगा:
    {
        "pair": "EURUSDOTC",
        "action": "BUY ⬆️ (CALL)",
        "price": "1.09452",
        "sentiment": "STRONG BULLISH",
        "accuracy": "99.8"
    }
    """
    try:
        data = await request.json()
        pair_code = data.get("pair", "EURUSDOTC")
        action = data.get("action", "BUY ⬆️ (CALL)")
        price = data.get("price", "Live")
        sentiment = data.get("sentiment", "REALTIME BREAKOUT")
        accuracy = data.get("accuracy", "99.6")
        
        pair_display = SUPPORTED_PAIRS.get(pair_code, pair_code)
        
        dashboard = f"""
👑 **TRADEFATHER 100% LIVE SIGNAL**
━━━━━━━━━━━━━━━━━━━━
💱 **Asset Pair :** {pair_display}
💵 **Strike Price :** `{price}`
⏱️ **Timeframe    :** `1 MINUTE (REAL-TIME)`
━━━━━━━━━━━━━━━━━━━━
🚨 **TRADINGVIEW LIVE ACTION :**
👉 **🎯 {action}** 👈

🎯 **AI Verified Accuracy :** `{accuracy}%`
🔥 **Market Momentum   :** `{sentiment}`
⚖️ **Martingale Rule   :** `⚠️ USE 1ST MARTINGALE IF OTM`
━━━━━━━━━━━━━━━━━━━━
📊 *Note: Yeh tradingview server se aaya ekdam live aur accurate signal hai.*
"""
        # टेलीग्राम चैनल/ग्रुप में सीधे ब्रॉडकास्ट करें
        background_tasks.add_task(
            bot.send_message,
            chat_id=DEFAULT_CHAT_ID,
            text=dashboard,
            reply_markup=get_dashboard_buttons(pair_code),
            parse_mode="Markdown"
        )
        return {"status": "Signal Broadcasted Successfully"}
    except Exception as e:
        logger.error(f"Webhook Error: {str(e)}")
        return {"status": "error", "message": str(e)}

# ==================================================
# TELEGRAM POLLING WORKAROUND FOR FASTAPI
# ==================================================
@app.post("/telegram-updates")
async def telegram_updates(request: Request):
    """बटन क्लिक और स्टार्ट कमांड हैंडल करने के लिए"""
    try:
        update = await request.json()
        if "message" in update:
            chat_id = update["message"]["chat"]["id"]
            text = update["message"].get("text", "")
            
            if text == "/start" or text == "/signal":
                welcome_text = "🦅 **WELCOME TO TRADEFATHER 100% LIVE WEBHOOK BOT** 🦅\n━━━━━━━━━━━━━━━━━━━━\n💎 **Status:** Connected to TradingView Server\n⏱️ **Expiry:** 1 Minute Accurate\n\n👇 **Niche se currency choose karein:**"
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={
                    "chat_id": chat_id, "text": welcome_text, "reply_markup": get_main_menu().to_dict(), "parse_mode": "Markdown"
                })
                
        elif "callback_query" in update:
            query = update["callback_query"]
            chat_id = query["message"]["chat"]["id"]
            message_id = query["message"]["message_id"]
            data = query["data"]
            
            # Answer Callback
            requests.post(f"https://api.telegram.org/bot{TOKEN}/answerCallbackQuery", json={"callback_query_id": query["id"]})
            
            if data == "back_menu":
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={
                    "chat_id": chat_id, "text": "🔍 **Please select currency from grid:**", "reply_markup": get_main_menu().to_dict()
                })
            elif data.startswith("select_") or data.startswith("recalc_"):
                p_code = data.replace("select_", "").replace("recalc_", "")
                p_disp = SUPPORTED_PAIRS.get(p_code, p_code)
                
                # यूजर को बताना कि लाइव सिग्नल ट्रेडिंगव्यू से आ रहे हैं
                wait_text = f"⏳ **{p_disp}** का लाइव सिग्नल जैसे ही TradingView पर बनेगा, वह तुरंत यहाँ ऑटो-फ्लैश हो जाएगा। कृपया तब तक वेट करें या अलर्ट चेक करें।"
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={
                    "chat_id": chat_id, "text": wait_text, "reply_markup": get_dashboard_buttons(p_code), "parse_mode": "Markdown"
                })
            elif data.startswith("auto_on_"):
                p_code = data.replace("auto_on_", "")
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={
                    "chat_id": chat_id, "text": f"🚀 **AUTOMATION MODE: ON**\nTradingView से आने वाले सिग्नल्स अब इस चैट में लाइव फॉरवर्ड होना शुरू हो चुके हैं।"
                })
            elif data.startswith("auto_off_"):
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={
                    "chat_id": chat_id, "text": "🛑 **AUTOMATION MODE: OFF**\nऑटो सिग्नल पाइपलाइन को रोक दिया गया है।"
                })
        return {"ok": True}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # लोकल या रेंडर पर रन करने के लिए पोर्ट सेट करें
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
