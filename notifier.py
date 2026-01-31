import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def send_telegram_alert(message):
    """
    Sends a message to the configured Telegram chat.
    """
    if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN":
        print("Telegram Token ayarlanmamış, mesaj gönderilmedi.")
        print(f"Mesaj: {message}")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            print(f"Telegram hatası: {response.text}")
        else:
            print("Telegram mesajı gönderildi.")
    except Exception as e:
        print(f"Telegram bağlantı hatası: {e}")

def format_price_alert(product_name, old_price, new_price, url):
    """
    Formats the alert message.
    """
    drop_amount = old_price - new_price
    drop_percent = (drop_amount / old_price) * 100
    
    msg = (
        f"🚨 <b>FİYAT DÜŞTÜ!</b>\n\n"
        f"📦 <b>Ürün:</b> {product_name}\n"
        f"📉 <b>İndirim:</b> {drop_amount:,.2f} TL (%{drop_percent:.1f})\n"
        f"💰 <b>Eski Fiyat:</b> {old_price:,.2f} TL\n"
        f"🏷️ <b>Yeni Fiyat:</b> {new_price:,.2f} TL\n\n"
        f"🔗 <a href='{url}'>Ürüne Git</a>"
    )
    return msg
