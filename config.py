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
    "https://www.mediamarkt.com.tr/tr/product/_apple-macbook-pro-apple-m5-islemci-10-cekirdekcpu-10-cekirdek-gpu-16gb-ram-1tb-ssd-142-space-black-mde14tua-1250346.html",
    "https://www.mediamarkt.com.tr/tr/product/_apple-mw1g3tuamacbook-airapple-m4-islemci10-cekirdek-cpu-10-cekirdek-gpu16gb-ram256gb-ssd153-silver-1245665.html",
    "https://www.mediamarkt.com.tr/tr/product/_apple-mw0w3tuamacbook-airapple-m4-islemci-10-cekirdek-cpu-8-cekirdek-gpu16gb-ram256gb-ssd136silver-1245653.html",
    "https://www.mediamarkt.com.tr/tr/product/_apple-mw0y3tuamacbook-airapple-m4-islemci-10-cekirdek-cpu-8-cekirdek-gpu16gb-ram256gb-ssd136starlight-1245655.html",
    "https://www.mediamarkt.com.tr/tr/product/_apple-mw123tuamacbook-airapple-m4-islemci-10-cekirdek-cpu-8-cekirdek-gpu16gb-ram256gb-ssd136midnight-1245654.html",
    "https://www.pt.com.tr/macbook-air-15-inc-m4-10cpu-10gpu-24gb-512gb-gece-yarisi-mc6l4tu-a"
]
