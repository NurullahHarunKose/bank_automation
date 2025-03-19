# BANKA OTOMASYONU PROJESİ

## 1. KULLANILAN KÜTÜPHANELER VE TEKNOLOJİLER

### 1.1 Python Kütüphaneleri
- **Flask**: Web framework (v2.0+)
  - flask: Ana framework
  - flask_session: Oturum yönetimi
  - jsonify: JSON yanıtları için
  - render_template: HTML şablon işleme
  - redirect, url_for: Yönlendirmeler için

- **Requests**: API istekleri (v2.28+)
  - Döviz kuru verilerini çekmek için
  - ExchangeRate API entegrasyonu

- **JSON**: Veri depolama
  - json.loads(): JSON string'i parse etme
  - json.dumps(): JSON string'e çevirme

- **Datetime**: Tarih/saat işlemleri
  - datetime.now(): Anlık zaman
  - strftime(): Tarih formatlama

### 1.2 Frontend Teknolojileri
- **HTML5**
  - Semantik elementler
  - Form validasyonu
  - Responsive tasarım

- **CSS3**
  - Flexbox/Grid layout
  - Animations/Transitions
  - Media queries
  - Custom properties

- **JavaScript**
  - Fetch API
  - DOM Manipülasyonu
  - Event handling
  - AJAX istekleri

- **Font Awesome 6.5.1**
  - İkonlar ve simgeler
  - Animasyonlu ikonlar

### 1.3 Veritabanı
- **JSON Dosya Sistemi**
  - musteriler.json: Müşteri bilgileri
  - hesaplar.json: Hesap bakiyeleri
  - islem_gecmisi.json: İşlem kayıtları

### 1.4 API Entegrasyonları
- **ExchangeRate API**
  - Güncel döviz kurları
  - Altın/Gümüş fiyatları
  - 5 dakikada bir güncelleme

### 1.5 Güvenlik
- **Session Yönetimi**
  - Flask-Session
  - Oturum zaman aşımı
  - Şifreli cookie'ler

- **Veri Doğrulama**
  - Form validasyonu
  - TC Kimlik kontrolü
  - Bakiye kontrolleri

### 1.6 Geliştirme Araçları
- **Git**: Versiyon kontrolü
- **VS Code**: Kod editörü
- **Postman**: API testi
- **Chrome DevTools**: Frontend debug

## 2. PROJENİN AMACI
Modern bankacılık işlemlerini gerçekleştirebilen, hem web arayüzü hem de konsol uygulaması olarak çalışabilen çok yönlü bir banka otomasyonu sistemi.

## 3. TEKNOLOJİK ALTYAPI
Backend: Python 3.8+
Web Framework: Flask
Frontend: HTML5, CSS3, JavaScript
Veritabanı: JSON tabanlı dosya sistemi
API: ExchangeRate-API (Döviz kurları için)
UI Framework: Font Awesome ikonları

## 4. PROJE YAPISI
banka/
├── templates/              # HTML şablonları
├── static/                # Statik dosyalar (CSS, JS)
├── app.py                # Flask web sunucusu
├── main.py               # Konsol uygulaması
├── kur_bilgileri.py      # Döviz işlemleri
├── musteri_islemleri.py  # Müşteri yönetimi
├── admin_panel.py        # Yönetici paneli
├── musteriler.json       # Müşteri veritabanı
├── hesaplar.json        # Hesap veritabanı
└── islem_gecmisi.json   # İşlem kayıtları

## 5. TEMEL ÖZELLİKLER
    5.1 Para İşlemleri
    Para transferi (TL/USD/EUR/Altın/Gümüş)
    Döviz alım/satım
    Kıymetli maden işlemleri
    Bakiye sorgulama
    Detaylı işlem geçmişi

    5.2 Hesap Yönetimi
    Yeni müşteri kaydı
    Müşteri profil yönetimi
    TC Kimlik doğrulama
    Şifre yönetimi

    5.3 Döviz İşlemleri
    Güncel kur takibi
    Alış/Satış işlemleri
    Çoklu döviz desteği
    Anlık kur hesaplama

    5.4 Yönetici Paneli
    Müşteri yönetimi
    İşlem takibi
    Sistem ayarları
    Raporlama araçları

## 6. GÜVENLİK ÖZELLİKLERİ
Session tabanlı kimlik doğrulama
Şifreli veri iletişimi
İşlem onay sistemi
Otomatik oturum sonlandırma
TC Kimlik doğrulama

## 7. VERİ YAPISI
7.1 Müşteri Bilgileri (musteriler.json)
    {
        "hesap_no": "1111",        // Otomatik oluşturulan hesap numarası
        "ad": "Ad",
        "soyad": "Soyad",
        "tc_no": "11111111111",
        "dogum_tarihi": "01/01/1990"
    }

7.1.1 Hesap Numarası Ataması
    - Her yeni müşteri kaydında 4 haneli benzersiz hesap numarası otomatik oluşturulur
    - Hesap numarası formatı: XXXX (1000-9999 arası)
    - Sistem mevcut hesap numaralarını kontrol ederek kullanılmayan ilk numarayı atar
    - Hesap numarası bir kez atandıktan sonra değiştirilemez
    - Silinen hesapların numaraları yeni müşterilere tekrar atanmaz

7.1.2 Hesap Numarası Kontrol Mekanizması
    - Yeni kayıt sırasında otomatik kontrol
    - Benzersizlik doğrulaması
    - Ardışık numara sistemi
    - Güvenlik doğrulaması

7.2 Hesap Bilgileri (hesaplar.json)
    {
        "hesap_no": "1111",
        "bakiye_tl": "1000.00",
        "bakiye_usd": "100.00",
        "bakiye_eur": "50.00"
    }

## 8. MODÜLLER ARASI İLETİŞİM
    8.1 Web Arayüzü -> Backend
    Flask route'ları
    AJAX istekleri
    Session yönetimi

    8.2 Backend -> Veritabanı
    JSON dosya işlemleri
    CRUD operasyonları
    Veri tutarlılığı kontrolleri

    8.3 Döviz API -> Sistem
    Real-time kur güncellemesi
    Hata yönetimi
    Önbellekleme sistemi

## 9. KULLANIM SENARYOLARI
    9.1 Müşteri İşlemleri
        Hesap açma
        Para transferi
        Döviz alım/satım
        Bakiye sorgulama
        İşlem geçmişi görüntüleme

    9.2 Yönetici İşlemleri  
        Müşteri yönetimi
        İşlem takibi
        Sistem raporları
        Hesap yönetimi

## 10. KURULUM VE ÇALIŞTIRMA
    # Web arayüzü için:
    python app.py

    # Konsol uygulaması için:
    python main.py

## 11. DEMO HESAPLAR

    11.1 Müşteri Girişi
        Hesap No: 1000
        Şifre: 1234

    11.2 Yönetici Girişi
        ID: 0616