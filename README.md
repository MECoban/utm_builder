# UTM Link Builder

Kampanya linklerinizi kolayca oluşturabileceğiniz basit ve kullanışlı bir web uygulaması.

## Özellikler

- ✨ Temiz ve modern arayüz
- 🚀 Hızlı ve kolay UTM link oluşturma
- 📋 Tek tıkla kopyalama
- 💾 Tüm linkleri SQLite veritabanında kaydetme
- 📝 Her link için açıklama ekleme
- 🎯 Lansman/Kampanya grubu sistemi (performans takibi için)
- 📚 Kaydedilen tüm linkleri görüntüleme ve yönetme
- 🔍 Lansmanlara göre filtreleme ve gruplama
- 📊 Her lansman için istatistikler (link sayısı, tarih aralığı)
- 🗑️ İstenmeyen linkleri silme
- 📱 Mobil uyumlu responsive tasarım
- 🔒 Kendi sunucunuzda çalışır

## UTM Parametreleri

- **utm_source** (zorunlu): Trafik kaynağı (örn: google, facebook, newsletter)
- **utm_medium** (zorunlu): Marketing ortamı (örn: cpc, email, social)
- **utm_campaign** (zorunlu): Kampanya adı (örn: summer_sale_2025)
- **utm_term** (opsiyonel): Ücretli anahtar kelimeler
- **utm_content** (opsiyonel): İçerik tipi veya reklam versiyonu

## Kurulum

### 1. Gereksinimler

- Python 3.7 veya üzeri

### 2. Bağımlılıkları Yükleyin

```bash
pip install -r requirements.txt
```

### 3. Uygulamayı Başlatın

```bash
python app.py
```

Uygulama varsayılan olarak `http://0.0.0.0:5000` adresinde çalışacaktır.

## Kullanım

1. Tarayıcınızda `http://localhost:5000` adresine gidin
2. Base URL'nizi girin (örn: https://yourwebsite.com/page)
3. **Lansman/Kampanya Grubu** seçin veya yeni bir tane oluşturun (örn: "Ocak 2025 Lansman")
4. UTM parametrelerini doldurun
5. İsteğe bağlı olarak bir açıklama ekleyin
6. "Link Oluştur" butonuna tıklayın
7. Oluşan link otomatik olarak kaydedilir
8. "Tüm Linkleri Görüntüle" ile kaydedilen linkleri yönetin

### Lansman/Kampanya Grubu Sistemi

Linklerinizi lansmanlar veya kampanya grupları altında organize edin:
- **Örnek kullanım**: "Q1 2025 Lansman", "Yaz İndirimleri 2025", "Black Friday"
- Her lansmanın altında ilgili tüm UTM linkleri otomatik gruplandırılır
- Gelecekte performans analizi için mükemmel bir temel oluşturur

### Kaydedilen Linkler

`/links` sayfasından:
- Lansmanlar bazında gruplandırılmış görünüm
- Her lansman için istatistikler (kaç link, tarih aralığı)
- Lansmanlara göre filtreleme
- Linkleri tek tıkla kopyalayın
- İstenmeyen linkleri silin
- Açıklamaları ve kampanya detaylarını görün

## Production Ortamında Çalıştırma

Production ortamında çalıştırmak için Gunicorn kullanmanız önerilir:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Lisans

Bu proje açık kaynaklıdır ve MIT lisansı altında dağıtılmaktadır.

