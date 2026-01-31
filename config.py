import os

# Telegram Configuration
# Buraya kendi değerlerinizi gireceksiniz.
TELEGRAM_BOT_TOKEN = "8505233798:AAEMfuJXSTLV70fHEXzG0CxAWGH24beLOis"
TELEGRAM_CHAT_ID = "5859636523"

# Database Configuration
DB_NAME = "prices.db"

# Check Interval (in minutes)
# Kaç dakikada bir kontrol edileceği
CHECK_INTERVAL_MINUTES = 15

# User Agent (Playwright handles this mostly, but good to have constants)
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Category URLs for Crawler
# Bot bu sayfalardaki tüm ürünleri tarayacaktır.
# Takip edilecek ürünlerin tam adresleri
TARGET_URLS = [
    "https://www.vatanbilgisayar.com/macbook-pro-m5.html",
    "https://www.mediamarkt.com.tr/tr/product/_apple-macbook-pro-apple-m5-islemci-10-cekirdekcpu-10-cekirdek-gpu-24gb-ram-1tb-ssd-142-silver-mde64tua-1250349.html"
]
