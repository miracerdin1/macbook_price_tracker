import time
import schedule
import random
from config import TARGET_URLS, CHECK_INTERVAL_MINUTES
from database import init_db, update_price
from scraper import scrape_product
from notifier import send_telegram_alert, format_price_alert

# Configure logging
import logging
import os

# Create a logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# File handler
file_handler = logging.FileHandler("bot.log", encoding="utf-8")
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

# Console handler (optional, but good for debugging)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
logger.addHandler(console_handler)

def check_prices():
    logger.info("--- Kontrol Başlıyor ---")
    
    # Doğrudan hedef linkleri tara
    logger.info(f"Takip listesindeki {len(TARGET_URLS)} ürün taranıyor...")
    
    for i, url in enumerate(TARGET_URLS):
        try:
            logger.info(f"Ürün kontrol ediliyor ({i+1}/{len(TARGET_URLS)}): {url}")
            price, name = scrape_product(url)
            
            if price and price > 0:
                old_price = update_price(url, name, price)
                
                if old_price is None:
                    logger.info(f"✅ Yeni ürün eklendi: {name} ({price} TL)")
                elif price < old_price:
                    logger.info(f"🔻 FİYAT DÜŞTÜ! {old_price} -> {price}")
                    msg = format_price_alert(name, old_price, price, url)
                    send_telegram_alert(msg)
                elif price > old_price:
                    logger.info(f"🔺 Fiyat arttı: {old_price} -> {price}")
                else:
                    logger.info(f"➖ Fiyat değişmedi: {price} TL")
            else:
                logger.warning(f"❌ Fiyat çekilemedi: {url}")
                
        except Exception as e:
            logger.error(f"URL işlenirken hata: {url} - {e}")
        
        # Siteyi boğmamak için ürünler arası bekleme
        time.sleep(random.uniform(5, 10))

def main():
    # Write PID to file for easy stopping
    pid = os.getpid()
    with open("bot.pid", "w") as f:
        f.write(str(pid))
    
    logger.info(f"MacBook Fiyat Takip Botu Başlatılıyor (PID: {pid})...")
    init_db()
    
    # Check for Single Run Mode (GitHub Actions)
    import sys
    if "--once" in sys.argv or os.getenv("GITHUB_ACTIONS") == "true":
        logger.info("Mod: Tek Seferlik Çalıştırma (CI/CD)")
        check_prices()
        logger.info("İşlem tamamlandı, çıkılıyor.")
        return

    # Loop Mode (Local)
    # İlk çalışma
    check_prices()
    
    # Zamanlayıcı
    logger.info(f"{CHECK_INTERVAL_MINUTES} dakikada bir kontrol edilecek...")
    schedule.every(CHECK_INTERVAL_MINUTES).minutes.do(check_prices)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
