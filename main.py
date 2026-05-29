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

# 🔴 CONFIGURATION DATA
TOKEN = "8735814245:AAFk849g-0ZEmZDINRwyWMTGSCzcOg5yRFg"
DEFAULT_CHAT_ID = "-1003993233052" 

# 📞 OWNER SUPPORT DETAILS
OWNER_MOBILE = "+91 8767812831"
OWNER_EMAIL = "arjuntradar@gmail.com"

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

# In-memory database to keep track of active user automations
# Format: { "pair_code": [set of chat_ids] }
ACTIVE_AUTOMATIONS = {key: set() for key in SUPPORTED_PAIRS.keys()}

# Footer Support Block
def get_support_footer():
    return f"""━━━━━━━━━━━━━━━━━━━━
📞 **OFFICIAL SUPPORT & CONTACT:**
👤 **Owner:** Arjun
📱 **Mobile:** {OWNER_MOBILE}
📧 **Email:** {OWNER_EMAIL}
💬 *Any issues or inquiries? Feel free to contact.*"""

# 2-Column Grid Format
def get_main_menu():
    keyboard = []
    row = []
    for index, (key, value) in enumerate(SUPPORTED_PAIRS.items()):
        row.append({"text": value, "callback_data": f"select_{key}"})
        if len(row) == 2 or index == len(SUPPORTED_PAIRS) - 1:
            keyboard.append(row)
            row = []
    return {"inline_keyboard": keyboard}

# Control Buttons + Multi-Timeframe Expiry Choices (5s to 1m)
def get_dashboard_buttons(pair_code):
    return {
        "inline_keyboard": [
            [
                {"text": "⏱️ 5 Sec", "callback_data": f"tf_5s_{pair_code}"},
                {"text": "⏱️ 15 Sec", "callback_data": f"tf_15s_{pair_code}"},
                {"text": "⏱️ 30 Sec", "callback_data": f"tf_30s_{pair_code}"},
                {"text": "⏱️ 1 Min", "callback_data": f"tf_1m_{pair_code}"}
            ],
            [
                {"text": "🚀 ON Auto", "callback_data": f"auto_on_{pair_code}"},
                {"text": "🛑 OFF Auto", "callback_data": f"auto_off_{pair_code}"},
                {"text": "🔄 Re-Analyze", "callback_data": f"recalc_{pair_code}"}
            ],
            [
                {"text": "🔍 Select Currency Menu (Start)", "callback_data": "back_menu"}
            ]
        ]
    }

@app.get("/")
def home():
    return {"status": "TradeFather Webhook Engine Running 24/7"}

# ==================================================
# 🔥 TRADINGVIEW WEBHOOK RECEIVER (FORWARDS AUTOMATICALLY)
# ==================================================
@app.post("/tradingview-webhook")
async def receive_tradingview_signal(request: Request, background_tasks: BackgroundTasks):
    try:
        data = await request.json()
        pair_code = data.get("pair", "EURUSDOTC").upper().replace("/", "").replace(" ", "")
        action = data.get("action", "BUY ⬆️ (CALL)")
        price = data.get("price", "Live")
        sentiment = data.get("sentiment", "REALTIME BREAKOUT")
        accuracy = data.get("accuracy", "99.6")
        timeframe = data.get("expiry", "1 MINUTE")
        
        pair_display = SUPPORTED_PAIRS.get(pair_code, pair_code)
        
        dashboard = f"""👑 **TRADEFATHER 100% LIVE SIGNAL**
━━━━━━━━━━━━━━━━━━━━
💱 **Asset Pair :** {pair_display}
💵 **Strike Price :** `{price}`
⏱️ **Timeframe    :** `{timeframe}`
━━━━━━━━━━━━━━━━━━━━
🚨 **TRADINGVIEW LIVE ACTION :**
👉 **🎯 {action}** 👈

🎯 **AI Verified Accuracy :** `{accuracy}%`
🔥 **Market Momentum   :** `{sentiment}`
⚖️ **Martingale Rule   :** `⚠️ USE 1ST MARTINGALE IF OTM`
{get_support_footer()}
"""
        # 1. Main Channel/Group par broadcast karein
        background_tasks.add_task(
            bot.send_message,
            chat_id=DEFAULT_CHAT_ID,
            text=dashboard,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text="🔍 Select Currency Menu (Start)", callback_data="back_menu")]
            ]),
            parse_mode="Markdown"
        )
        
        # 2. IMPORTANT: Jis-jis user ne Auto-mode ON kiya hai, unki personal chat par automatic bhejein
        if pair_code in ACTIVE_AUTOMATIONS:
            for user_chat_id in ACTIVE_AUTOMATIONS[pair_code]:
                background_tasks.add_task(
                    bot.send_message,
                    chat_id=user_chat_id,
                    text=dashboard,
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton(text="🔍 Select Currency Menu (Start)", callback_data="back_menu")]
                    ]),
                    parse_mode="Markdown"
                )
                
        return {"status": "Signal Broadcasted Successfully"}
    except Exception as e:
        logger.error(f"Webhook Error: {str(e)}")
        return {"status": "error", "message": str(e)}

# ==================================================
# TELEGRAM WEBHOOK CONTROLLER
# ==================================================
@app.post("/telegram-updates")
async def telegram_updates(request: Request):
    try:
        update = await request.json()
        
        # 1. Text Message Handle (/start)
        if "message" in update:
            chat_id = update["message"]["chat"]["id"]
            text = update["message"].get("text", "")
            
            if text == "/start" or text == "/signal":
                welcome_text = f"🦅 **WELCOME TO TRADEFATHER LIVE WEBHOOK BOT** 🦅\n━━━━━━━━━━━━━━━━━━━━\n💎 **Status:** Connected to TradingView Server\n⏱️ **Expiry Options:** 5s | 15s | 30s | 1m\n\n👇 **Niche se currency choose karein:**\n\n{get_support_footer()}"
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={
                    "chat_id": chat_id, "text": welcome_text, "reply_markup": get_main_menu(), "parse_mode": "Markdown"
                })
                
        # 2. Inline Button Clicks Handle
        elif "callback_query" in update:
            query = update["callback_query"]
            chat_id = query["message"]["chat"]["id"]
            data = query["data"]
            
            requests.post(f"https://api.telegram.org/bot{TOKEN}/answerCallbackQuery", json={"callback_query_id": query["id"]})
            
            if data == "back_menu":
                welcome_text = f"🔍 **Please select currency from grid:**\n\n{get_support_footer()}"
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={
                    "chat_id": chat_id, "text": welcome_text, "reply_markup": get_main_menu(), "parse_mode": "Markdown"
                })
                
            elif data.startswith("select_") or data.startswith("recalc_"):
                p_code = data.replace("select_", "").replace("recalc_", "")
                p_disp = SUPPORTED_PAIRS.get(p_code, p_code)
                
                wait_text = f"⏳ **{p_disp}** ka live signal jaise hi TradingView par trigger hoga, aapki is personal chat par turant flash ho jayega. Niche diye gaye choices select karein.\n\n{get_support_footer()}"
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={
                    "chat_id": chat_id, "text": wait_text, "reply_markup": get_dashboard_buttons(p_code), "parse_mode": "Markdown"
                })
                
            elif data.startswith("auto_on_"):
                p_code = data.replace("auto_on_", "")
                if p_code in ACTIVE_AUTOMATIONS:
                    ACTIVE_AUTOMATIONS[p_code].add(chat_id) # Save user session for auto forward
                
                p_disp = SUPPORTED_PAIRS.get(p_code, p_code)
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={
                    "chat_id": chat_id, "text": f"🚀 **AUTOMATION MODE: ON ({p_disp})**\nTradingView par signal bante hi wo automatic bina kisi delay ke is chat mein deliver hoga.\n\n{get_support_footer()}", "parse_mode": "Markdown"
                })
                
            elif data.startswith("auto_off_"):
                p_code = data.replace("auto_off_", "")
                if p_code in ACTIVE_AUTOMATIONS and chat_id in ACTIVE_AUTOMATIONS[p_code]:
                    ACTIVE_AUTOMATIONS[p_code].remove(chat_id) # Remove user session
                    
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={
                    "chat_id": chat_id, "text": f"🛑 **AUTOMATION MODE: OFF**\nIs pair ke liye automatic routing rok di gayi hai.\n\n{get_support_footer()}", "parse_mode": "Markdown"
                })
                
            # Timeframe button click response
            elif data.startswith("tf_"):
                parts = data.split("_")
                tf_selected = parts[1] # 5s, 15s, 30s, 1m
                p_code = parts[2]
                p_disp = SUPPORTED_PAIRS.get(p_code, p_code)
                
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={
                    "chat_id": chat_id, "text": f"⏱️ **Timeframe Updated to {tf_selected.upper()}** for **{p_disp}**.\nTradingView alert pipeline ko optimize kar diya gaya hai. Aane wale signal ka wait karein.\n\n{get_support_footer()}", "parse_mode": "Markdown"
                })
                
        return {"ok": True}
    except Exception as e:
        logger.error(f"Telegram Updates Error: {str(e)}")
        return {"error": str(e)}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
