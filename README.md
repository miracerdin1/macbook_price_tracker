# MacBook Price Tracker Kurulum Rehberi

Botunuz kullanıma hazır dosyalar halindedir. Çalıştırmak için aşağıdaki adımları izleyin.

## 1. Hazırlık

Proje klasörüne gidin:

```bash
cd "C:\Users\mirac.erdin\.gemini\antigravity\scratch\macbook_price_tracker"
```

## 2. Kurulum

Gerekli kütüphaneleri yükleyin:

```bash
pip install -r requirements.txt
playwright install
```

## 3. Yapılandırma

`config.py` dosyasını açın ve aşağıdaki alanları doldurun:

- `TELEGRAM_BOT_TOKEN`: @BotFather'dan aldığınız token.
- `TELEGRAM_CHAT_ID`: Mesajın geleceği chat ID (örn: @userinfobot ile öğrenebilirsiniz).
- `TARGET_URLS`: Takip etmek istediğiniz ürün linklerini listeye ekleyin.

## 4. Çalıştırma

Botu başlatın:

```bash
python main.py
```

Bot ilk çalıştığında bir veritabanı oluşturacak ve ekli ürünlerin güncel fiyatlarını kaydedecektir. Daha sonra 30 dakikada bir (veya config'de ne ayarladıysanız) kontrol etmeye devam edecektir.
