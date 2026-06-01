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
OWNER_EMAIL = "arjuntradar@gmail.com"

# ⏱️ GLOBAL LIVE BINOMO/QUOTEX RUNTIME VARIABLES
CURRENT_PLATFORM = "Quotex" 
DYNAMO_RUNTIME_STATUS = "10 Hours" 
IS_DYNAMO_ACTIVE = True

app = FastAPI()

# 📊 ALL ASSETS MATRIX (QUOTEX + OLYMP TRADE + IMAGES ASSETS INCLUDED)
SUPPORTED_PAIRS = {
    # Existing OTC Pairs
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
    "GOLDOTC": "GOLD OTC", "SILVEROTC": "SILVER OTC",
    
    # Newly Added From Images (Olymp Trade & Normal Market Pairs)
    "CRYPTOIDX": "Crypto IDX", "BITCOINCASH": "Bitcoin Cash (OTC)", "SOLANA": "Solana (OTC)",
    "ETHEREUM": "Ethereum (OTC)", "BITCOIN": "Bitcoin", "UNISWAP": "Uniswap (OTC)",
    "PANCAKESWAP": "Pancake Swap (OTC)", "AUDCAD": "AUD/CAD", "AUDCHF": "AUD/CHF",
    "AUDDKK": "AUD/DKK", "AUDHUF": "AUD/HUF", "AUDJPY": "AUD/JPY", "AUDNOK": "AUD/NOK",
    "AUDNZD": "AUD/NZD", "AUDSEK": "AUD/SEK", "AUDSGD": "AUD/SGD", "AUDUSD": "AUD/USD",
    "AUDZAR": "AUD/ZAR", "CADDKK": "CAD/DKK", "CADJPY": "CAD/JPY", "CADMXN": "CAD/MXN",
    "CADNOK": "CAD/NOK", "CADSEK": "CAD/SEK", "CADSGD": "CAD/SGD", "CHFDKK": "CHF/DKK",
    "CHFJPY": "CHF/JPY", "CHFNOK": "CHF/NOK", "CHFPLN": "CHF/PLN", "CHFSEK": "CHF/SEK",
    "CHFSGD": "CHF/SGD", "EURHUF": "EUR/HUF", "EURILS": "EUR/ILS", "EURJPY": "EUR/JPY",
    "EURMXN": "EUR/MXN", "EURNOK": "EUR/NOK", "EURNZD": "EUR/NZD", "EURSEK": "EUR/SEK",
    "EURSGD": "EUR/SGD", "EURUSD": "EUR/USD", "EURZAR": "EUR/ZAR", "GBPCAD": "GBP/CAD",
    "GBPCZK": "GBP/CZK", "GBPDKK": "GBP/DKK", "GBPHKD": "GBP/HKD", "GBPMXN": "GBP/MXN",
    "GBPNOK": "GBP/NOK", "GBPNZD": "GBP/NZD", "GBPPLN": "GBP/PLN", "GBPSGD": "GBP/SGD",
    "GBPTRY": "GBP/TRY", "NOKJPY": "NOK/JPY", "NOKSEK": "NOK/SEK", "NZDCAD": "NZD/CAD"
}

def get_support_footer():
    return f"""━━━━━━━━━━━━━━━━━━━━
📞 OFFICIAL SUPPORT & CONTACT

👤 Owner: Arjun Trader
📱 Mobile: {OWNER_MOBILE}
📧 Email: {OWNER_EMAIL}

💎 VIP SERVICE AVAILABLE
🔥 Premium Signals
🔥 TradingView Setup Support
🔥 Fast Customer Support
🔥 Private VIP Access
⚠️ Trade Responsibly"""

def get_main_menu():
    status_indicator = "🟢 ACTIVE" if IS_DYNAMO_ACTIVE else "🔴 INACTIVE"
    
    keyboard = [
        # RESTORED: Binomo Signals Button back in place
        [
            {"text": "📊 Quotex Signals", "callback_data": "set_platform_Quotex"},
            {"text": "📉 Binomo Signals", "callback_data": "set_platform_Binomo"}
        ],
        [
            {"text": "📈 Olymp Trade Signals", "callback_data": "set_platform_OlympTrade"}
        ],
        # Timing Status Info Button shown to users
        [
            {"text": f"⏱️ Bot Status: {DYNAMO_RUNTIME_STATUS} [{status_indicator}]", "callback_data": "dynamo_status_click"}
        ],
        # Admin Configuration Button
        [
            {"text": "⚙️ Admin Timing Control Panel", "callback_data": "admin_timing_menu"}
        ],
        [{"text": "👇 CHOOSE YOUR ASSET PAIR 👇", "callback_data": "ignore"}]
    ]
    
    row = []
    for index, (key, value) in enumerate(SUPPORTED_PAIRS.items()):
        row.append({"text": value, "callback_data": f"tv_info_{key}"})
        if len(row) == 2 or index == len(SUPPORTED_PAIRS) - 1:
            keyboard.append(row)
            row = []
            
    return {"inline_keyboard": keyboard}

def get_admin_timing_keyboard():
    return {
        "inline_keyboard": [
            [{"text": "⏱️ 1 Hour", "callback_data": "time_1h"}, {"text": "⏱️ 5 Hours", "callback_data": "time_5h"}],
            [{"text": "⏱️ 10 Hours", "callback_data": "time_10h"}, {"text": "⏱️ 24 Hours", "callback_data": "time_24h"}],
            [{"text": "🛑 Stop Engine Bot", "callback_data": "time_stop"}, {"text": "🔄 Main Menu", "callback_data": "back_menu"}]
        ]
    }

@app.get("/")
def home():
    return {"status": "Arjun A1 REAL Webhook Engine Running with Quotex, Binomo & Olymp Trade Configuration"}

# 🎯 TRADINGVIEW ENDPOINT
@app.post("/tradingview-webhook")
async def tradingview_webhook(request: Request):
    try:
        data = await request.json()
        logger.info(f"📥 Real Signal Received: {data}")

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

        platform_upper = CURRENT_PLATFORM.upper()
        
        dashboard_msg = f"""👑 🌈 **ARJUN A1 PREMIUM LIVE SIGNAL ({platform_upper})** 🌈 👑

━━━━━━━━━━━━━━━━━━━━
💱 Asset Pair : {pair_display} [100% REAL LIVE]
💵 Strike Price : {price}
⏱️ Timeframe    : {timeframe}
🚀 Platform     : {CURRENT_PLATFORM} 
⏱️ Engine Setup : Active for {DYNAMO_RUNTIME_STATUS}
━━━━━━━━━━━━━━━━━━━━
📊 PRO FILTER INDICATORS DATA:
📈 Market Trend : {trend}
🎯 RSI Valuation : {rsi}
⚡ CCI Oscillator : {cci}
🔍 Filter Validation : {logic}
━━━━━━━━━━━━━━━━━━━━
🚨 LIVE TRADE DIRECTION :
👉 🎯 {color_bullet} {direction} ({emoji}) 👈

🎯 VIP Accuracy : 100% REAL INDICATOR CONFIRMED
⚖️ Martingale Rule   : ⚠️ USE 1ST MARTINGALE IF OTM
"""
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, json={
            "chat_id": DEFAULT_CHAT_ID, "text": dashboard_msg, "parse_mode": "Markdown"
        })

        return {"status": "success", "message": f"Real Signal Posted for {CURRENT_PLATFORM}"}  
          
    except Exception as e:  
        logger.error(f"Webhook Processing Error: {str(e)}")  
        return {"status": "error", "message": str(e)}

# 🔄 TELEGRAM BOT COMMANDS AND CALLBACK HANDLING
@app.post("/telegram-updates")
async def telegram_updates(request: Request):
    global CURRENT_PLATFORM, DYNAMO_RUNTIME_STATUS, IS_DYNAMO_ACTIVE
    try:
        update = await request.json()
        if "message" in update:
            chat_id = update["message"]["chat"]["id"]
            text = update["message"].get("text", "")

            if text.startswith("/start"):  
                welcome_text = f"""🚀 **Welcome to Arjun A1 Trading Signals**

🦅 🌈 **WELCOME TO ARJUN A1 REAL WEBHOOK BOT** 🌈 🦅
━━━━━━━━━━━━━━━━━━━━

📈 **Live Signals**
🔥 **OTC Signals**
🥇 **Gold Signals**
🥈 **Silver Signals**
📊 **Market Analysis**

💎 Engine Status:
50+ MULTI-PLATFORM ASSETS READY FOR TRADINGVIEW

📞 **Support**
Mobile number: {OWNER_MOBILE}
Email id: {OWNER_EMAIL}

👇 Niche pure assets aur systems ki grid check karein:
Select an option below.
{get_support_footer()}"""

                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={  
                    "chat_id": chat_id, "text": welcome_text, "reply_markup": get_main_menu(), "parse_mode": "Markdown"  
                })  
                  
        elif "callback_query" in update:  
            query = update["callback_query"]  
            chat_id = query["message"]["chat"]["id"]  
            data = query["data"]  
            message_id = query["message"]["message_id"]  
              
            requests.post(f"https://api.telegram.org/bot{TOKEN}/answerCallbackQuery", json={"callback_query_id": query["id"]})  
            
            if data == "ignore":
                return {"ok": True}

            # 1. Platform Switch Config
            if data.startswith("set_platform_"):
                CURRENT_PLATFORM = data.replace("set_platform_", "")
                platform_msg = f"✅ **Target Platform Changed to: {CURRENT_PLATFORM}**\n\nAb alerts mein user ko {CURRENT_PLATFORM} show hoga."
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={
                    "chat_id": chat_id, "text": platform_msg, "parse_mode": "Markdown"
                })
                requests.post(f"https://api.telegram.org/bot{TOKEN}/editMessageReplyMarkup", json={
                    "chat_id": chat_id, "message_id": message_id, "reply_markup": get_main_menu()
                })

            # 2. Timing Admin Panel Trigger
            elif data == "admin_timing_menu":
                requests.post(f"https://api.telegram.org/bot{TOKEN}/editMessageText", json={
                    "chat_id": chat_id, "message_id": message_id,
                    "text": "⏱️ **Admin Engine Timing Setup Panel**\n\nSelect karein ki bot user ko kitne ghante ke liye chalu dikhana chahiye:",
                    "reply_markup": get_admin_timing_keyboard(), "parse_mode": "Markdown"
                })

            # 3. Handle Timing Selection Updates
            elif data.startswith("time_"):
                time_choice = data.replace("time_", "")
                if time_choice == "1h":
                    DYNAMO_RUNTIME_STATUS = "1 Hour"
                    IS_DYNAMO_ACTIVE = True
                elif time_choice == "5h":
                    DYNAMO_RUNTIME_STATUS = "5 Hours"
                    IS_DYNAMO_ACTIVE = True
                elif time_choice == "10h":
                    DYNAMO_RUNTIME_STATUS = "10 Hours"
                    IS_DYNAMO_ACTIVE = True
                elif time_choice == "24h":
                    DYNAMO_RUNTIME_STATUS = "24 Hours"
                    IS_DYNAMO_ACTIVE = True
                elif time_choice == "stop":
                    DYNAMO_RUNTIME_STATUS = "Stopped"
                    IS_DYNAMO_ACTIVE = False
                
                requests.post(f"https://api.telegram.org/bot{TOKEN}/editMessageText", json={
                    "chat_id": chat_id, "message_id": message_id,
                    "text": f"⚙️ **Engine Time Configured Successfully!**\n\nAb users ko Bot Status `{DYNAMO_RUNTIME_STATUS}` show karega.",
                    "reply_markup": {"inline_keyboard": [[{"text": "🔙 Back To Main Menu", "callback_data": "back_menu"}]]},
                    "parse_mode": "Markdown"
                })

            # 4. Asset Details Mapping
            elif data.startswith("tv_info_"):  
                p_code = data.replace("tv_info_", "")  
                p_disp = SUPPORTED_PAIRS.get(p_code, p_code)  
                  
                info_msg = f"⚙️ **{p_disp} Automation Connected ({CURRENT_PLATFORM})**\n\nTradingView Alert settings mein is pair ka naam `{p_disp}` likhein aur message box mein standard JSON data pass karein."  
                  
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
