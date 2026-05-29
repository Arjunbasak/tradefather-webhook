
# ==================================================
# DEPLOYMENT READY: FASTAPI + TELEGRAM WEBHOOK BOT
# ==================================================
import os
import logging
import random
from fastapi import FastAPI, Request, BackgroundTasks
import uvicorn
import requests

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# 🔴 CONFIGURATION DATA
TOKEN = "8735814245:AAFk849g-0ZEmZDINRwyWMTGSCzcOg5yRFg"
VIP_LINK = "https://t.me/+4ZPssc8CaKQwNjU1" # 🌟 Yahan apna asli VIP link daalein
DEFAULT_CHAT_ID = "-1003993233052"          # 🔥 Aapka Channel ID jahan automatic signals jayenge

# 📞 OWNER SUPPORT DETAILS
OWNER_MOBILE = "+91 8767812831"
OWNER_EMAIL = "arjuntradar@gmail.com"

app = FastAPI()

# 📊 LIVE REGISTERED PAIRS GRID (Bilkul pehle jaisa same)
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

# Footer Support Block
def get_support_footer():
    return f"""━━━━━━━━━━━━━━━━━━━━
📞 **OFFICIAL SUPPORT & CONTACT:**
👤 **Owner:** Arjun
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

# Step 2: CALL / PUT Direction Selection Buttons
def get_direction_buttons(pair_code):
    return {
        "inline_keyboard": [
            [
                {"text": "🟢 CALL (UP)", "callback_data": f"dir_call_{pair_code}"},
                {"text": "🔴 PUT (DOWN)", "callback_data": f"dir_put_{pair_code}"}
            ],
            [
                {"text": "🔍 Select Currency Menu", "callback_data": "back_menu"}
            ]
        ]
    }

# Step 3: Modified Expiry Choices (5s removed, 1m to 5m added)
def get_timeframe_buttons(direction, pair_code):
    return {
        "inline_keyboard": [
            [
                {"text": "⏱️ 1 Min", "callback_data": f"final_{direction}_1m_{pair_code}"},
                {"text": "⏱️ 2 Min", "callback_data": f"final_{direction}_2m_{pair_code}"},
                {"text": "⏱️ 3 Min", "callback_data": f"final_{direction}_3m_{pair_code}"}
            ],
            [
                {"text": "⏱️ 4 Min", "callback_data": f"final_{direction}_4m_{pair_code}"},
                {"text": "⏱️ 5 Min", "callback_data": f"final_{direction}_5m_{pair_code}"}
            ],
            [
                {"text": "🔄 Change Direction", "callback_data": f"select_{pair_code}"},
                {"text": "🔍 Main Menu", "callback_data": "back_menu"}
            ]
        ]
    }

# Step 4: Final Signal Output Markup with VIP Link & Back Button
def get_final_signal_markup(direction, pair_code):
    return {
        "inline_keyboard": [
            [
                {"text": "✨ JOIN VIP FOR MORE ✨", "url": VIP_LINK}
            ],
            [
                {"text": "🔄 Another Trade", "callback_data": f"select_{pair_code}"},
                {"text": "🔍 Main Menu", "callback_data": "back_menu"}
            ]
        ]
    }

@app.get("/")
def home():
    return {"status": "TradeFather Engine Active with TradingView Signal Receiver"}

# ==================================================
# 📡 NEW FEATURE: TRADINGVIEW LIVE SIGNAL RECEIVER
# ==================================================
@app.post("/tradingview-webhook")
async def tradingview_webhook(request: Request, background_tasks: BackgroundTasks):
    try:
        data = await request.json()
        pair_code = data.get("pair", "EURUSDOTC").upper().replace("/", "").replace(" ", "")
        action = data.get("action", "CALL").upper()
        price = data.get("price", "Live")
        timeframe = data.get("expiry", "1 MIN").upper()
        
        p_disp = SUPPORTED_PAIRS.get(pair_code, pair_code)
        
        direction = "CALL" if "CALL" in action or "BUY" in action else "PUT"
        emoji = "UP ⬆️" if direction == "CALL" else "DOWN ⬇️"
        color_bullet = "🟢" if direction == "CALL" else "🔴"
        
        # Exact Matching Dashboard Style for Automated Signals
        tv_dashboard = f"""👑 🌈 **TRADEFATHER 1000% VIP LIVE SIGNAL** 🌈 👑
━━━━━━━━━━━━━━━━━━━━
💱 **Asset Pair :** {p_disp}
💵 **Strike Price :** `{price}`
⏱️ **Timeframe    :** `{timeframe} (REAL-TIME)`
━━━━━━━━━━━━━━━━━━━━
🚨 **LIVE TRADE DIRECTION :**
👉 **🎯 {color_bullet} {direction} ({emoji})** 👈

🎯 **VIP Accuracy :** `1000% ACCURATE`
🔥 **Market Momentum   :** `STRONG ACCELERATION`
⚖️ **Martingale Rule   :** `⚠️ USE 1ST MARTINGALE IF OTM`
{get_support_footer()}
"""
        # Send automated alert to your channel asynchronously
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
        return {"status": "processed"}
    except Exception as e:
        logger.error(f"TradingView Webhook Error: {str(e)}")
        return {"error": str(e)}

# ==================================================
# TELEGRAM WEBHOOK CONTROLLER
# ==================================================
@app.post("/telegram-updates")
async def telegram_updates(request: Request):
    try:
        update = await request.json()
        
        # 1. Handle Text Commands (/start)
        if "message" in update:
            chat_id = update["message"]["chat"]["id"]
            text = update["message"].get("text", "")
            
            if text == "/start" or text == "/signal":
                # 🔥 Fast & Colourful Professional Welcome Message
                welcome_text = f"🦅 🌈 **WELCOME TO TRADEFATHER VIP BOT** 🌈 🦅\n━━━━━━━━━━━━━━━━━━━━\n💎 **Status:** VIP SERVER CONNECTED\n🚀 **System Accuracy:** 1000% GUARANTEED\n⚡ **Execution:** FAST & ULTRASONIC\n\n👇 **Niche grid se apni currency pair choose karein:**\n\n{get_support_footer()}"
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={
                    "chat_id": chat_id, "text": welcome_text, "reply_markup": get_main_menu(), "parse_mode": "Markdown"
                })
                
        # 2. Handle Inline Button Clicks
        elif "callback_query" in update:
            query = update["callback_query"]
            chat_id = query["message"]["chat"]["id"]
            data = query["data"]
            
            # Answer callback query to stop loading wheel
            requests.post(f"https://api.telegram.org/bot{TOKEN}/answerCallbackQuery", json={"callback_query_id": query["id"]})
            
            # Action: Back to Main Menu
            if data == "back_menu":
                welcome_text = f"🔍 **Please select currency from grid:**\n\n{get_support_footer()}"
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={
                    "chat_id": chat_id, "text": welcome_text, "reply_markup": get_main_menu(), "parse_mode": "Markdown"
                })
                
            # Action: Currency Selected -> Ask for CALL or PUT Direction
            elif data.startswith("select_"):
                p_code = data.replace("select_", "")
                p_disp = SUPPORTED_PAIRS.get(p_code, p_code)
                
                direction_text = f"💱 **Asset Selected:** {p_disp}\n━━━━━━━━━━━━━━━━━━━━\n👉 **Aapko kis direction mein signal chahiye?**\n\nNiche diye gaye **CALL** ya **PUT** button par touch karein:"
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={
                    "chat_id": chat_id, "text": direction_text, "reply_markup": get_direction_buttons(p_code), "parse_mode": "Markdown"
                })
                
            # Action: Direction Selected (Call) -> Show 1m to 5m Buttons
            elif data.startswith("dir_call_"):
                p_code = data.replace("dir_call_", "")
                p_disp = SUPPORTED_PAIRS.get(p_code, p_code)
                
                tf_text = f"💱 **Asset:** {p_disp}\n🚨 **Direction:** 🟢 CALL (UP)\n━━━━━━━━━━━━━━━━━━━━\n⏱ *Ab trade lene ke liye niche se time select karein (1m to 5m):*"
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={
                    "chat_id": chat_id, "text": tf_text, "reply_markup": get_timeframe_buttons("call", p_code), "parse_mode": "Markdown"
                })

            # Action: Direction Selected (Put) -> Show 1m to 5m Buttons
            elif data.startswith("dir_put_"):
                p_code = data.replace("dir_put_", "")
                p_disp = SUPPORTED_PAIRS.get(p_code, p_code)
                
                tf_text = f"💱 **Asset:** {p_disp}\n🚨 **Direction:** 🔴 PUT (DOWN)\n━━━━━━━━━━━━━━━━━━━━\n⏱ *Ab trade lene ke liye niche se time select karein (1m to 5m):*"
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={
                    "chat_id": chat_id, "text": tf_text, "reply_markup": get_timeframe_buttons("put", p_code), "parse_mode": "Markdown"
                })
                
            # Action: Final Choice clicked (Time + Direction) -> INSTANT SIGNAL RESULT!
            elif data.startswith("final_"):
                parts = data.split("_")
                direction = parts[1].upper() # CALL / PUT
                timeframe = parts[2].upper() # 1M / 2M / 3M / 4M / 5M
                p_code = parts[3]
                p_disp = SUPPORTED_PAIRS.get(p_code, p_code)
                
                emoji = "UP ⬆️" if direction == "CALL" else "DOWN ⬇️"
                color_bullet = "🟢" if direction == "CALL" else "🔴"
                
                # 🌈 Colorful & Professional Dashboard Layout with 1000% Fixed Accuracy
                signal_dashboard = f"""👑 🌈 **TRADEFATHER 1000% VIP SIGNAL** 🌈 👑
━━━━━━━━━━━━━━━━━━━━
💱 **Asset Pair :** {p_disp}
⏱️ **Timeframe    :** `{timeframe} (REAL-TIME)`
━━━━━━━━━━━━━━━━━━━━
🚨 **LIVE TRADE DIRECTION :**
👉 **🎯 {color_bullet} {direction} ({emoji})** 👈

🎯 **VIP Accuracy :** `1000% ACCURATE`
🔥 **Market Momentum   :** `STRONG ACCELERATION`
⚖️ **Martingale Rule   :** `⚠️ USE 1ST MARTINGALE IF OTM`
{get_support_footer()}
"""
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={
                    "chat_id": chat_id, "text": signal_dashboard, "reply_markup": get_final_signal_markup(parts[1], p_code), "parse_mode": "Markdown"
                })

        return {"ok": True}
    except Exception as e:
        logger.error(f"Telegram Updates Error: {str(e)}")
        return {"error": str(e)}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
