import logging
import random
import json
from datetime import datetime
from dosya_islemleri_modul import musteri_bilgilerini_kaydet, musteri_bilgilerini_dogrula, musteri_bilgilerini_goruntule, musteri_ad_soyad, hesap_bilgilerini_goruntule, para_transferi_yap, islem_kaydet
from kur_bilgileri import KurBilgileri

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a file handler
file_handler = logging.FileHandler('banking_system.log')
file_handler.setLevel(logging.INFO)

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create a formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def musteri_giris():
    hesap_no = input("Hesap Numaranız: ")
    sifre = input("Şifreniz: ")
    
    if musteri_bilgilerini_dogrula(hesap_no, sifre):
        ad_soyad = musteri_ad_soyad(hesap_no)
        logger.info(f"User {ad_soyad} logged in successfully.")
        print(f"\nGiriş başarılı, hoşgeldiniz {ad_soyad}!\n")
        musteri_menu(hesap_no)
    else:
        logger.warning(f"Invalid login attempt for account {hesap_no}.")
        print("\nHatalı hesap numarası veya şifre. Lütfen tekrar deneyin.\n")
        from main import ana_menu
        ana_menu()

def musteri_menu(hesap_no):
    ad_soyad = musteri_ad_soyad(hesap_no)
    print(f"\n---{ad_soyad}---")
    print("1. Kullanıcı Bilgileri Görüntüle")
    print("2. Hesap Bilgileri Görüntüle")
    print("3. Para Transferi")
    print("4. Güncel Döviz ve Emtia Bilgileri Gör")
    print("5. Döviz/Kıymetli Maden Alış Satış")
    print("6. İşlem Geçmişi")
    print("7. Çıkış\n")

    secim = input("Seçiminiz: ")

    if secim == '1':
        print("\n---Kullanıcı Bilgileri---")
        musteri_bilgilerini_goruntule(hesap_no)
        musteri_menu(hesap_no)
    elif secim == '2':
        hesap_bilgileri(hesap_no)
        musteri_menu(hesap_no)
    elif secim == '3':
        para_transferi(hesap_no)
        print()
        musteri_menu(hesap_no)
    elif secim == '4':
        doviz_bilgileri()
        print()
        musteri_menu(hesap_no)
    elif secim == '5':
        doviz_kiymetli_maden(hesap_no)
        print()
        musteri_menu(hesap_no)
    elif secim == '6':
        islem_gecmisi(hesap_no)
        print()
        musteri_menu(hesap_no)
    elif secim == '7':
        return
    else:
        print("\nGeçersiz seçim, lütfen tekrar deneyin.\n")
        musteri_menu(hesap_no)

def musteri_ol():
    try:
        print("Test - Fonksiyon başladı")  # Test için eklendi
        print("\n" + "=" * 40)
        print("📝 YENİ MÜŞTERİ KAYDI")
        print("=" * 40)
        
        # Tüm bilgileri aynı formatta iste
        print("Test - Bilgi isteme başlıyor")  # Test için eklendi
        ad = input("Adı: ").strip().lower()
        soyad = input("Soyadı: ").strip().lower()
        dogum_tarihi = input("Doğum Tarihi: ").strip()
        tc_no = input("TC Kimlik Numarası: ").strip()
        telefon = input("Telefon Numarası: ").strip()
        email = input("Email Adresi: ").strip()
        adres = input("Adresi: ").strip()
        sifre = input("Şifre: ").strip()
        
        # Validasyonlar
        if not (ad and soyad and tc_no and dogum_tarihi and telefon and email and adres and sifre):
            print("\n❌ Tüm alanlar zorunludur!")
            return
            
        # TC Kimlik No kontrolü
        if not tc_no.isdigit() or len(tc_no) != 11:
            print("\n❌ TC Kimlik No 11 haneli olmalıdır!")
            return
            
        # Telefon kontrolü
        if not telefon.replace(" ", "").isdigit() or len(telefon.replace(" ", "")) != 11:
            print("\n❌ Geçersiz telefon numarası!")
            return
            
        # Email kontrolü
        if "@" not in email or "." not in email:
            print("\n❌ Geçersiz e-posta adresi!")
            return
            
        # Yaş kontrolü
        try:
            gun, ay, yil = map(int, dogum_tarihi.split("/"))
            dogum = datetime(yil, ay, gun)
            yas = (datetime.now() - dogum).days / 365
            if yas < 18:
                print("\n❌ 18 yaşından küçük olan kişilerin müşteri olma izni yoktur!")
                return
        except:
            print("\n❌ Geçersiz doğum tarihi!")
            return
            
        # Hesap numarası oluştur
        try:
            with open("musteriler.json", "r", encoding="utf-8") as dosya:
                musteriler = json.load(dosya)
                son_hesap_no = max(int(m["hesap_no"]) for m in musteriler)
                yeni_hesap_no = str(son_hesap_no + 1)
        except:
            yeni_hesap_no = "1111"
            musteriler = []
            
        # Yeni müşteri
        yeni_musteri = {
            "hesap_no": yeni_hesap_no,
            "ad": ad,
            "soyad": soyad,
            "dogum_tarihi": dogum_tarihi,
            "tc_kimlik_no": tc_no,
            "telefon": telefon,
            "email": email,
            "adres": adres,
            "sifre": sifre
        }
        
        # Müşteriyi kaydet
        musteriler.append(yeni_musteri)
        with open("musteriler.json", "w", encoding="utf-8") as dosya:
            json.dump(musteriler, dosya, indent=4, ensure_ascii=False)
            
        # Hesap bakiyelerini oluştur
        try:
            with open("hesaplar.json", "r", encoding="utf-8") as dosya:
                hesaplar = json.load(dosya)
        except:
            hesaplar = []
            
        yeni_hesap = {
            "hesap_no": yeni_hesap_no,
            "bakiye": {
                "TL": 0.0,
                "USD": 0.0,
                "EUR": 0.0,
                "ALTIN": 0.0,
                "GUMUS": 0.0
            }
        }
        
        hesaplar.append(yeni_hesap)
        with open("hesaplar.json", "w", encoding="utf-8") as dosya:
            json.dump(hesaplar, dosya, indent=4)
            
        print("\n✅ Müşteri kaydı başarıyla oluşturuldu!")
        print(f"👤 Hesap Numaranız: {yeni_hesap_no}")
        print("🔑 Giriş yapmak için bu bilgileri kullanabilirsiniz.")
        
    except Exception as e:
        print(f"\n❌ Bir hata oluştu: {str(e)}")
        
    input("\nDevam etmek için Enter'a basın...")

def para_transferi(gonderen_hesap_no):
    try:
        while True:
            print("\n" + "=" * 40)
            print("💸 PARA TRANSFERİ")
            print("=" * 40)
            print("1️⃣  TL")
            print("2️⃣  USD")
            print("3️⃣  EUR")
            print("4️⃣  ALTIN")
            print("5️⃣  GÜMÜŞ")
            print("0️⃣  Çıkış")
            print("=" * 40)

            tur_secim = input("Seçiminiz: ").strip()

            if tur_secim == "0":
                print("Çıkış yapılıyor...")
                break

            birim_map = {
                "1": "TL",
                "2": "USD",
                "3": "EUR",
                "4": "ALTIN",
                "5": "GÜMÜŞ"
            }

            if tur_secim not in birim_map:
                print("\n❌ Geçersiz seçim! Lütfen tekrar deneyin.")
                continue

            birim = birim_map[tur_secim]

            # Alıcı bilgilerini al
            alici_hesap_no = input("\nAlıcı Hesap No: ").strip()

            # Alıcı bilgilerini kontrol et
            with open("musteriler.json", "r", encoding="utf-8") as dosya:
                musteriler = json.load(dosya)["musteriler"]  # "musteriler" listesine eriş
                alici = next((m for m in musteriler if str(m["hesap_no"]) == str(alici_hesap_no)), None)
                gonderen = next((m for m in musteriler if str(m["hesap_no"]) == str(gonderen_hesap_no)), None)

            if not alici:
                print("\n❌ Alıcı hesap bulunamadı!")
                continue

            if str(alici_hesap_no) == str(gonderen_hesap_no):
                print("\n❌ Kendinize transfer yapamazsınız!")
                continue

            print(f"\n👥 Alıcı: {alici['ad'].title()} {alici['soyad'].title()}")

            # Transfer bilgilerini al
            try:
                miktar = float(input(f"Transfer Miktarı ({birim}): "))
                if miktar <= 0:
                    print("\n❌ Transfer miktarı 0'dan büyük olmalıdır!")
                    continue
            except ValueError:
                print("\n❌ Geçersiz miktar!")
                continue

            aciklama = input("Transfer Açıklaması: ").strip()
            if not aciklama:
                print("\n❌ Transfer açıklaması boş olamaz!")
                continue

            # Onay al
            onay = input("Transfer işlemini onaylıyor musunuz? (1/0): ").strip().lower()
            if onay != "1":
                print("\n❌ İşlem iptal edildi!")
                continue

            # Transferi gerçekleştir
            if para_transferi_yap(gonderen_hesap_no, alici_hesap_no, miktar, birim):
                print(f"\n✅ {miktar} {birim} transfer başarıyla gerçekleştirildi!")

                # İşlem kaydı
                islem_kaydet(
                    hesap_no=gonderen_hesap_no,
                    islem_tipi="Para Transferi",
                    miktar=miktar,
                    birim=birim,
                    aciklama=f"Transfer: {aciklama}",
                    karsi_hesap=alici_hesap_no
                )
            else:
                print(f"\n❌ Transfer gerçekleştirilemedi! {birim} bakiyenizi kontrol edin.")

    except Exception as e:
        print(f"\n❌ Bir hata oluştu: {str(e)}")

    input("\nDevam etmek için Enter'a basın...")

def doviz_bilgileri():
    kur_servisi = KurBilgileri()
    kur_servisi.guncel_kurlari_goster()
    input("\nDevam etmek için Enter'a basın...")

def doviz_kiymetli_maden(hesap_no):
    print(f"\nDöviz/Kıymetli Maden Alış Satış - Hesap No: {hesap_no}")
    doviz_kiymetli_maden_alim_satim(hesap_no)

def islem_gecmisi(hesap_no):
    try:
        # İşlem geçmişi dosyasını kontrol et, yoksa oluştur
        try:
            with open("islem_gecmisi.json", "r", encoding="utf-8") as dosya:
                data = json.load(dosya)
        except FileNotFoundError:
            data = {"islemler": []}
            with open("islem_gecmisi.json", "w", encoding="utf-8") as dosya:
                json.dump(data, dosya, indent=4, ensure_ascii=False)
            print("\n❌ Henüz işlem geçmişi bulunmuyor.")
            return
            
        # Hesaba ait işlemleri filtrele
        musteri_islemleri = [i for i in data.get("islemler", []) if str(i["hesap_no"]) == str(hesap_no)]
        
        if not musteri_islemleri:
            print("\n❌ İşlem geçmişi bulunamadı!")
            return
            
        print("\n" + "=" * 50)
        print("📋 İŞLEM GEÇMİŞİ")
        print("=" * 50)
        
        # Döviz/Emtia işlemlerini filtrele
        print("\n💱 Döviz/Emtia Alış/Satış Geçmişi")
        print("-" * 50)
        doviz_islemler = [i for i in musteri_islemleri if any(tip in i['islem_tipi'] for tip in ['USD', 'EUR', 'ALTIN', 'GUMUS'])]
        
        if doviz_islemler:
            for islem in reversed(doviz_islemler):
                print(f"📅 Tarih      : {islem['tarih']}")
                print(f"🔄 İşlem Tipi : {islem['islem_tipi']}")
                print(f"💰 Miktar     : {islem['miktar']} {islem['birim']}")
                if "kur" in islem:
                    print(f"💵 Kur        : {islem['kur']:.4f} TL")
                print(f"📝 Açıklama   : {islem['aciklama']}")
                print("-" * 50)
        else:
            print("❌ Döviz/Emtia işlemi bulunmamaktadır.")
            print("-" * 50)
        
        # Para transferi işlemlerini filtrele
        print("\n💸 Para Transferi Geçmişi")
        print("-" * 50)
        transfer_islemler = [i for i in musteri_islemleri if 'Transfer' in i['islem_tipi']]
        
        if transfer_islemler:
            for islem in reversed(transfer_islemler):
                print(f"📅 Tarih      : {islem['tarih']}")
                print(f"🔄 İşlem Tipi : {islem['islem_tipi']}")
                print(f"💰 Miktar     : {islem['miktar']} {islem['birim']}")
                if "karsi_hesap" in islem:
                    print(f"👤 Karşı Hesap: {islem['karsi_hesap']}")
                print(f"📝 Açıklama   : {islem['aciklama']}")
                print("-" * 50)
        else:
            print("❌ Transfer işlemi bulunmamaktadır.")
            print("-" * 50)
            
    except Exception as e:
        print(f"\n❌ İşlem geçmişi görüntülenirken hata oluştu: {str(e)}")
    
    input("\nDevam etmek için Enter'a basın...")

def kullanici_bilgileri(hesap_no):
    try:
        with open("musteriler.json", "r", encoding="utf-8") as dosya:
            musteriler = json.load(dosya)
            
        musteri = next((m for m in musteriler["musteriler"] if str(m["hesap_no"]) == str(hesap_no)), None)
        
        if musteri:
            print("\n" + "=" * 40)
            print("📋 KULLANICI BİLGİLERİ")
            print("=" * 40)
            print("\n👤 Kişisel Bilgiler:")
            print("-" * 20)
            print(f"Ad            : {musteri['ad'].title()}")
            print(f"Soyad         : {musteri['soyad'].title()}")
            print(f"TC Kimlik No  : {musteri['tc_kimlik_no']}")
            print(f"Hesap No      : {musteri['hesap_no']}")
            print(f"Doğum Tarihi  : {musteri['dogum_tarihi']}")
            
            print("\n📞 İletişim Bilgileri:")
            print("-" * 20)
            print(f"Telefon       : {musteri.get('telefon', 'Bilgi Yok')}")
            print(f"E-posta       : {musteri.get('email', 'Bilgi Yok')}")
            
            print("\n📍 Adres Bilgileri:")
            print("-" * 20)
            print(f"Adres         : {musteri.get('adres', 'Bilgi Yok')}")
            print("=" * 40)
        else:
            print("Müşteri bulunamadı!")
            
    except FileNotFoundError:
        print("Müşteri dosyası bulunamadı.")
    except json.JSONDecodeError:
        print("Müşteri dosyası bozuk.")
    except Exception as e:
        print(f"Bir hata oluştu: {str(e)}")
        
    input("\nDevam etmek için Enter'a basın...")

def hesap_bilgileri(hesap_no):
    try:
        with open("hesaplar.json", "r", encoding="utf-8") as dosya:
            data = json.load(dosya)
            hesap = next((h for h in data["hesaplar"] if str(h["hesap_no"]) == str(hesap_no)), None)
            
        if not hesap:
            print("\n❌ Hesap bulunamadı!")
            return
            
        print("\n========================================")
        print("💰 HESAP BİLGİLERİ")
        print("========================================")
        print(f"💵 Türk Lirası : {hesap['bakiye_tl']:,.2f} TL")
        print(f"💵 Dolar      : {hesap['bakiye_usd']:,.2f} USD")
        print(f"💵 Euro       : {hesap['bakiye_eur']:,.2f} EUR")
        print(f"🏆 Altın      : {hesap['bakiye_altin']:,.2f} gram")
        print(f"🥈 Gümüş      : {hesap['bakiye_gumus']:,.2f} gram")
        print("========================================")
        
    except FileNotFoundError:
        print("\n❌ Hesap bilgileri dosyası bulunamadı!")
    except Exception as e:
        print(f"\n❌ Bir hata oluştu: {str(e)}")
        
    input("\nDevam etmek için Enter'a basın...")

def giris_yap(hesap_no, sifre):
    try:
        if musteri_bilgilerini_dogrula(hesap_no, sifre):
            print(f"\n✅ Giriş başarılı! Hoşgeldiniz {musteri_ad_soyad(hesap_no)}")
            return True, hesap_no
        else:
            print("\n❌ Hatalı hesap no veya şifre!")
            return False, None
    except Exception as e:
        print(f"\n❌ Giriş yapılırken bir hata oluştu: {str(e)}")
        return False, None

def kullanici_menusu(hesap_no):
    try:
        with open("musteriler.json", "r", encoding="utf-8") as dosya:
            data = json.load(dosya)
            musteriler = data["musteriler"]
        
        musteri = next((m for m in musteriler if str(m["hesap_no"]) == str(hesap_no)), None)
        
        if not musteri:
            print("\n❌ Müşteri bulunamadı!")
            return
            
        ad = musteri["ad"].title()
        soyad = musteri["soyad"].title()
        
        while True:
            print("\n" + "=" * 40)
            print(f"👋 HOŞGELDİNİZ {ad} {soyad}")
            print("=" * 40)
            print("1️⃣  Kullanıcı Bilgileri Görüntüle")
            print("2️⃣  Hesap Bilgileri Görüntüle")
            print("3️⃣  Para Transferi")
            print("4️⃣  Güncel Döviz ve Emtia Bilgileri")
            print("5️⃣  Döviz/Kıymetli Maden Alış Satış")
            print("6️⃣  İşlem Geçmişi")
            print("0️⃣  Çıkış")
            print("=" * 40)
            
            secim = input("\nSeçiminiz: ")
            
            if secim == "1":
                kullanici_bilgileri(hesap_no)
            elif secim == "2":
                hesap_bilgileri(hesap_no)
            elif secim == "3":
                para_transferi(hesap_no)
            elif secim == "4":
                doviz_bilgileri()
            elif secim == "5":
                doviz_islemleri(hesap_no)
            elif secim == "6":
                islem_gecmisi(hesap_no)
            elif secim == "0":
                print("\n✅ Çıkış yapıldı. İyi günler!")
                break
            else:
                print("\n❌ Geçersiz seçim!")
                
    except Exception as e:
        print(f"\n❌ Bir hata oluştu: {str(e)}")

def doviz_islemleri(hesap_no):
    try:
        # Hesap bilgilerini al
        with open("hesaplar.json", "r", encoding="utf-8") as dosya:
            data = json.load(dosya)
            hesap = next((h for h in data["hesaplar"] if str(h["hesap_no"]) == str(hesap_no)), None)
        
        if not hesap:
            print("\n❌ Hesap bulunamadı!")
            return
            
        # Kur servisini başlat
        kur_servisi = KurBilgileri()
        
        while True:
            print("\n" + "=" * 40)
            print("💱 DÖVİZ VE EMTİA İŞLEMLERİ")
            print("=" * 40)
            print("Mevcut Bakiyeleriniz:")
            print(f"💵 Türk Lirası    : {hesap['bakiye_tl']:.2f} TL")
            print(f"💵 Dolar          : {hesap['bakiye_usd']:.2f} USD")
            print(f"💶 Euro           : {hesap['bakiye_eur']:.2f} EUR")
            print(f"🏆 Altın          : {hesap['bakiye_altin']:.2f} GR")
            print(f"🥈 Gümüş          : {hesap['bakiye_gumus']:.2f} GR")
            print("=" * 40)
            print("1️⃣  Döviz/Emtia Al")
            print("2️⃣  Döviz/Emtia Sat")
            print("3️⃣  Ana Menüye Dön")
            print("=" * 40)
            
            secim = input("\nSeçiminiz: ")
            
            if secim == "3":
                break
                
            if secim not in ["1", "2"]:
                print("\n❌ Geçersiz seçim!")
                continue
                
            islem_tipi = "ALIŞ" if secim == "1" else "SATIŞ"
            
            print("\nİşlem yapmak istediğiniz birimi seçin:")
            print("1️⃣  Dolar")
            print("2️⃣  Euro")
            print("3️⃣  Altın")
            print("4️⃣  Gümüş")
            
            birim_secim = input("\nSeçiminiz: ")
            
            birim_map = {
                "1": ("USD", "Dolar", "bakiye_usd"),
                "2": ("EUR", "Euro", "bakiye_eur"),
                "3": ("ALTIN", "Gram Altın", "bakiye_altin"),
                "4": ("GUMUS", "Gümüş", "bakiye_gumus")
            }
            
            if birim_secim not in birim_map:
                print("\n❌ Geçersiz birim seçimi!")
                continue
                
            birim_kod, birim_ad, bakiye_key = birim_map[birim_secim]
            
            # Güncel kur bilgisini al
            alis_kur, satis_kur = kur_servisi.kur_bilgisi_al(birim_kod)
            
            if not alis_kur or not satis_kur:
                print("\n❌ Kur bilgisi alınamadı!")
                continue
                
            # Kur bilgisini göster
            print(f"\n{birim_ad} Güncel Kur Bilgileri:")
            print(f"Alış  : {alis_kur:.4f} TL")
            print(f"Satış : {satis_kur:.4f} TL")
            
            try:
                miktar = float(input(f"\nİşlem miktarını girin ({birim_kod}): "))
                if miktar <= 0:
                    print("\n❌ Miktar 0'dan büyük olmalıdır!")
                    continue
            except ValueError:
                print("\n❌ Geçersiz miktar!")
                continue
                
            if islem_tipi == "ALIŞ":
                # Alış işlemi
                gereken_tl = miktar * satis_kur  # Bankadan alırken satış kurundan
                if gereken_tl > hesap['bakiye_tl']:
                    print("\n❌ Yetersiz TL bakiyesi!")
                    continue
                    
                hesap['bakiye_tl'] -= gereken_tl
                hesap[bakiye_key] += miktar
                
                print(f"\n✅ {miktar:.2f} {birim_kod} alış işlemi başarılı!")
                print(f"💸 Ödenen: {gereken_tl:.2f} TL")
                
                # İşlem kaydet
                islem_kaydet(
                    hesap_no,
                    f"{birim_kod} Alış",
                    miktar,
                    birim_kod,
                    f"{birim_ad} alış işlemi",
                    kur=satis_kur
                )
                
            else:
                # Satış işlemi
                if miktar > hesap[bakiye_key]:
                    print(f"\n❌ Yetersiz {birim_kod} bakiyesi!")
                    continue
                    
                alinacak_tl = miktar * alis_kur  # Bankaya satarken alış kurundan
                hesap[bakiye_key] -= miktar
                hesap['bakiye_tl'] += alinacak_tl
                
                print(f"\n✅ {miktar:.2f} {birim_kod} satış işlemi başarılı!")
                print(f"💰 Alınan: {alinacak_tl:.2f} TL")
                
                # İşlem kaydet
                islem_kaydet(
                    hesap_no,
                    f"{birim_kod} Satış",
                    miktar,
                    birim_kod,
                    f"{birim_ad} satış işlemi",
                    kur=alis_kur
                )
            
            # Hesap dosyasını güncelle
            with open("hesaplar.json", "w", encoding="utf-8") as dosya:
                json.dump(data, dosya, indent=4)
            
            print("\nGüncel Bakiyeleriniz:")
            print(f"💵 Türk Lirası    : {hesap['bakiye_tl']:.2f} TL")
            print(f"💵 {birim_ad:<13}: {hesap[bakiye_key]:.2f} {birim_kod}")
            
    except Exception as e:
        print(f"\n❌ Bir hata oluştu: {str(e)}")
        
    input("\nDevam etmek için Enter'a basın...")

def islem_kaydet(hesap_no, islem_tipi, miktar, birim, aciklama, kur=None, karsi_hesap=None):
    try:
        # Mevcut işlemleri oku veya varsayılan yapıyı oluştur
        try:
            with open('islem_gecmisi.json', 'r', encoding='utf-8') as dosya:
                data = json.load(dosya)
                # Eski format düzeltme (liste ise "islemler" anahtarına al)
                if isinstance(data, list):
                    data = {"islemler": data}
        except FileNotFoundError:
            data = {"islemler": []}  # Varsayılan yapı
        
        # Yeni işlem kaydı
        yeni_islem = {
            "hesap_no": str(hesap_no),
            "tarih": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "islem_tipi": islem_tipi,
            "miktar": float(miktar),
            "birim": birim,
            "aciklama": aciklama
        }
        
        # Opsiyonel alanlar
        if kur:
            yeni_islem["kur"] = float(kur)
        if karsi_hesap:
            yeni_islem["karsi_hesap"] = str(karsi_hesap)
        
        # İşlemi listeye ekle
        data["islemler"].append(yeni_islem)
        
        # Dosyaya yaz
        with open('islem_gecmisi.json', 'w', encoding='utf-8') as dosya:
            json.dump(data, dosya, indent=4, ensure_ascii=False)
            
    except Exception as e:
        print(f"\n❌ İşlem kaydedilirken hata oluştu: {str(e)}")