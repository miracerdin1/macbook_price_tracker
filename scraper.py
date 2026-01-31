from playwright.sync_api import sync_playwright
import time
import random
import re

def get_product_links(category_url):
    """
    Crawls a category page and returns a set of product URLs.
    Handles infinite scrolling or pagination if necessary.
    """
    product_links = set()
    print(f"Kategori taranıyor: {category_url}")
    
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
                viewport={'width': 1920, 'height': 1080}
            )
            page = context.new_page()
            
            page.goto(category_url, timeout=60000)
            page.wait_for_load_state("domcontentloaded")
            time.sleep(5)
            
            # --- DEBUGGING START ---
            # Hata ayıklama için ekran görüntüsü ve HTML kaydet
            domain = "vatan" if "vatanbilgisayar" in category_url else "mediamarkt" if "mediamarkt" in category_url else "other"
            
            # 1. Ekran Görüntüsü
            screenshot_name = f"debug_category_{domain}.png"
            page.screenshot(path=screenshot_name)
            print(f"DEBUG: Kategori ekran görüntüsü kaydedildi: {screenshot_name}")
            
            # 2. HTML Kaydı
            html_name = f"debug_category_{domain}.html"
            with open(html_name, "w", encoding="utf-8") as f:
                f.write(page.content())
            print(f"DEBUG: Kategori HTML kaynağı kaydedildi: {html_name}")
            # --- DEBUGGING END ---

            # Scroll down to trigger lazy loading
            for _ in range(5):
                page.mouse.wheel(0, 1000)
                time.sleep(1)
            
            # Link Analizi
            all_links = page.locator("a").all()
            print(f"DEBUG: Sayfada toplam {len(all_links)} link bulundu.")

            # Vatan Selectors
            if "vatanbilgisayar.com" in category_url:
                # Vatan ürün kartları genellikle .product-list__link classına sahip
                # veya .product-list__content -> a
                elements = page.locator("a.product-list__link").all()
                if len(elements) == 0:
                     print("DEBUG: a.product-list__link ile ürün bulunamadı. Alternatif aranıyor...")
                     elements = page.locator(".product-list a").all()
                
                for el in elements:
                    href = el.get_attribute("href")
                    if href:
                        if not href.startswith("http"):
                            href = "https://www.vatanbilgisayar.com" + href
                        product_links.add(href)
                        
            # MediaMarkt Selectors
            elif "mediamarkt.com.tr" in category_url:
                # MediaMarkt genellikle card yapısı kullanır
                # Linkler genellikle data-test='product-title' olan elementin annesi veya kendisi
                # Basitçe tüm geçerli ürün linklerini filtreleyelim
                links = page.locator("a").all()
                for link in links:
                    href = link.get_attribute("href")
                    if href and "/product/" in href and ".html" in href:
                         if not href.startswith("http"):
                            href = "https://www.mediamarkt.com.tr" + href
                         product_links.add(href)

            print(f"Bulunan ürün sayısı: {len(product_links)}")
            browser.close()
        except Exception as e:
            print(f"Kategori taranırken hata: {e}")
            
    return list(product_links)

def clean_price(price_text):
    """
    "58.999,00 TL" -> 58999.00
    "100 TL" -> 100.0
    """
    if not price_text:
        return 0.0
    # Remove text like 'TL', whitespace
    price_text = price_text.upper().replace('TL', '').replace(' ', '').strip()
    # European format: 58.999,00 -> remove dot, replace comma with dot
    # But sometimes it's plain english. Let's assume Turkish format for these sites.
    price_text = price_text.replace('.', '').replace(',', '.')
    
    # Extract only numbers and dot
    price_text = re.sub(r'[^\d.]', '', price_text)
    
    try:
        return float(price_text)
    except ValueError:
        return 0.0

def scrape_product(url):
    """
    Scrapes a single product URL and returns (price, name).
    Returns (None, None) on failure.
    """
    found_price = 0
    product_name = "Bilinmeyen Ürün"
    
    # Random sleep before starting to feel human
    time.sleep(random.uniform(1, 4))
    
    import os
    is_ci = os.getenv("GITHUB_ACTIONS") == "true"
    
    with sync_playwright() as p:
        # Anti-detection args
        browser = p.chromium.launch(
            headless=is_ci,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-setuid-sandbox"
            ]
        )
        
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            viewport={'width': 1920, 'height': 1080},
            locale="tr-TR",
            timezone_id="Europe/Istanbul",
            extra_http_headers={
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
                "Sec-Ch-Ua": '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
                "Sec-Ch-Ua-Mobile": "?0",
                "Sec-Ch-Ua-Platform": '"Windows"',
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "Upgrade-Insecure-Requests": "1"
            }
        )
        
        # Stealth scripts to mask Linux environment
        page = context.new_page()
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            Object.defineProperty(navigator, 'platform', {
                get: () => 'Win32'
            });
            Object.defineProperty(navigator, 'languages', {
                get: () => ['tr-TR', 'tr', 'en-US', 'en']
            });
        """)
        
        try:
            print(f"Gidiliyor: {url}")
            page.goto(url, timeout=60000)
            page.wait_for_load_state("domcontentloaded")
            time.sleep(5) # Allow JS to execute completely

            # WAF / Cloudflare Check
            # "Bir dakika lütfen..." veya "Just a moment..." uyarısı varsa bekle
            try:
                title = page.title()
                if "Bir dakika" in title or "Just a moment" in title:
                    print(f"DEBUG: WAF Takildi ({title}), 30 saniye bekleniyor...")
                    time.sleep(30)
            except:
                pass
            
            # Save HTML immediately for debugging
            domain = "vatan" if "vatanbilgisayar" in url else "mediamarkt" if "mediamarkt" in url else "other"
            debug_filename = f"debug_{domain}_latest.html"
            with open(debug_filename, "w", encoding="utf-8") as f:
                f.write(page.content())
            print(f"DEBUG: Sayfa kaynağı '{debug_filename}' olarak kaydedildi.")

            # 1. METHOD: JSON-LD (Most Reliable)
            try:
                import json
                json_ld_scripts = page.locator('script[type="application/ld+json"]').all_inner_texts()
                print(f"DEBUG: {len(json_ld_scripts)} adet JSON-LD script bulundu.")
                
                for i, script in enumerate(json_ld_scripts):
                    try:
                        data = json.loads(script)
                        # MediaMarkt structure: BuyAction -> object(Product) -> offers -> price
                        if data.get("@type") == "BuyAction" and "object" in data:
                            product_data = data["object"]
                            if "offers" in product_data:
                                price_raw = product_data["offers"].get("price")
                                if price_raw:
                                    found_price = float(price_raw)
                                    print(f"DEBUG: JSON-LD found price (MediaMarkt): {found_price}")
                                    
                            if "name" in product_data:
                                product_name = product_data["name"]

                        # Standard Product structure (Vatan etc.)
                        elif data.get("@type") == "Product":
                            if "offers" in data:
                                offers = data["offers"]
                                # Single offer content
                                if isinstance(offers, dict):
                                    price_raw = offers.get("price")
                                    if price_raw:
                                        found_price = float(price_raw)
                                        print(f"DEBUG: JSON-LD found price (Standard): {found_price}")
                                # List of offers
                                elif isinstance(offers, list) and len(offers) > 0:
                                    price_raw = offers[0].get("price")
                                    if price_raw:
                                        found_price = float(price_raw)
                                        print(f"DEBUG: JSON-LD found price (List): {found_price}")
                            
                            if "name" in data:
                                product_name = data["name"]
                                
                        if found_price > 0:
                            break
                    except json.JSONDecodeError:
                        continue
            except Exception as e:
                print(f"DEBUG: JSON-LD error: {e}")

            # 2. METHOD: CSS Selectors (Fallback)
            if found_price == 0:
                print("DEBUG: JSON-LD failed, trying CSS selectors...")
                
                # Get Product Name if not found
                if product_name == "Bilinmeyen Ürün":
                    name_selectors = ["h1.product-detail__title", "h1.product-list__product-name", "h1[data-test='product-title']", "h1"]
                    for sel in name_selectors:
                        if page.locator(sel).first.is_visible():
                            product_name = page.locator(sel).first.inner_text().strip()
                            break

                # Get Price
                if "vatanbilgisayar.com" in url:
                    # Alternatif Vatan Seçicileri
                    price_selectors = [
                        ".product-list__price", 
                        ".product-detail__price",
                        "span.price",
                        "div.price-text",
                        "#product-price", # Tahmini ID
                        ".price-container"
                    ]
                    # Sayfadaki tüm görünür fiyatları tara (Son çare)
                    all_prices = page.locator("div, span, p").filter(has_text=re.compile(r'\d{2,}\.\d{3}')).all()
                    print(f"DEBUG: Vatan sayfasında {len(all_prices)} olası fiyat elementi bulundu.")
                    
                    for sel in price_selectors:
                        elem = page.locator(sel).first
                        if elem.is_visible():
                            found_price = clean_price(elem.inner_text())
                            if found_price > 0:
                                print(f"DEBUG: CSS found price (Vatan): {found_price}")
                                break
                    
                    if found_price == 0:
                         # Script içinden fiyat avla (Google Tracking vb.)
                        try:
                            content = page.content()
                            # value=89999 gibi desenleri ara
                            match = re.search(r'value\s*[:=]\s*["\']?(\d+(\.\d+)?)["\']?', content)
                            if match:
                                val = float(match.group(1))
                                if val > 10000: # MacBook fiyatı mantıklı bir aralıkta olmalı
                                    found_price = val
                                    print(f"DEBUG: Script regex ile fiyat bulundu: {found_price}")
                        except Exception as e:
                            print(f"DEBUG: Regex hatası: {e}")

                elif "mediamarkt.com.tr" in url:
                    # Meta tag check
                    meta_price = page.locator("meta[itemprop='price']").first
                    if meta_price.count() > 0:
                        content = meta_price.get_attribute("content")
                        if content:
                            found_price = float(content)
                            print(f"DEBUG: Meta tag found price: {found_price}")

                    # Visual elements check
                    if found_price == 0:
                        mm_selectors = [
                            "span[data-test='product-price']",
                            "div[data-test='product-price']",
                            "span[font-family='MMPrice']", 
                            ".price"
                        ]
                        for sel in mm_selectors:
                            elem = page.locator(sel).first
                            if elem.is_visible():
                                txt = elem.inner_text()
                                # Clean garbage Chars
                                p = clean_price(txt) 
                                if p > 0:
                                    found_price = p
                                    print(f"DEBUG: CSS found price (MediaMarkt): {found_price}")
                                    break

            if found_price > 0:
                print(f"Success: {product_name} - {found_price} TL")
                browser.close()
                return found_price, product_name
            else:
                print(f"Price NOT FOUND: {url}")
                # Hata durumunda sayfa başlığı ve içeriğinden ipucu al
                title = page.title()
                print(f"DEBUG: Sayfa Başlığı: {title}")
                
                content_text = page.locator("body").inner_text()[:500].replace("\n", " ")
                print(f"DEBUG: Sayfa İçeriği (İlk 500): {content_text}")
                
                browser.close()
                return None, product_name

        except Exception as e:
            print(f"Error occurred: {e}")
            browser.close()
            return None, None

if __name__ == "__main__":
    # Test run
    test_url = "https://www.vatanbilgisayar.com/macbook-pro-m3-cip-16gb-512gb-ssd-14-2inc-space-grey.html"
    print(scrape_product(test_url))
