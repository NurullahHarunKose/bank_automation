import json
from datetime import datetime

def musteri_bilgilerini_kaydet(musteri_bilgileri):
    try:
        try:
            with open("musteriler.json", "r", encoding='utf-8') as dosya:
                data = json.load(dosya)
                musteriler = data["musteriler"]
        except FileNotFoundError:
            data = {"musteriler": []}
            musteriler = data["musteriler"]
            
        musteriler.append(musteri_bilgileri)
        
        with open("musteriler.json", "w", encoding='utf-8') as dosya:
            json.dump(data, dosya, indent=4, ensure_ascii=False)
            
    except Exception as e:
        print(f"\n❌ Müşteri kaydedilirken hata oluştu: {str(e)}")

def musteri_bilgilerini_dogrula(hesap_no, sifre):
    try:
        with open("musteriler.json", "r", encoding='utf-8') as dosya:
            data = json.load(dosya)
            musteriler = data["musteriler"]
            
            # Hesap no ve şifre kontrolü
            for musteri in musteriler:
                if str(musteri["hesap_no"]) == str(hesap_no) and str(musteri["sifre"]) == str(sifre):
                    return True
                    
        return False
        
    except FileNotFoundError:
        print("\n❌ Müşteri dosyası bulunamadı!")
        return False
    except json.JSONDecodeError:
        print("\n❌ Müşteri dosyası okuma hatası!")
        return False
    except Exception as e:
        print(f"\n❌ Beklenmeyen bir hata oluştu: {str(e)}")
        return False

def musteri_bilgilerini_goruntule(hesap_no):
    try:
        with open("musteriler.json", "r", encoding="utf-8") as dosya:
            data = json.load(dosya)
            musteriler = data["musteriler"]
            
            musteri = next((m for m in musteriler if str(m["hesap_no"]) == str(hesap_no)), None)
            
            if musteri:
                print("\n" + "=" * 40)
                print("👤 MÜŞTERİ BİLGİLERİ")
                print("=" * 40)
                print(f"Ad               : {musteri['ad'].title()}")
                print(f"Soyad            : {musteri['soyad'].title()}")
                print(f"Doğum Tarihi     : {musteri['dogum_tarihi']}")
                print(f"TC Kimlik No     : {musteri['tc_kimlik_no']}")
                print(f"Telefon          : {musteri['telefon']}")
                print(f"Email            : {musteri['email']}")
                print(f"Adres            : {musteri['adres']}")
                print("=" * 40)
                return
                
            print("\n❌ Müşteri bulunamadı!")
            
    except FileNotFoundError:
        print("\n❌ Müşteri dosyası bulunamadı!")
    except Exception as e:
        print(f"\n❌ Bir hata oluştu: {str(e)}")

def musteri_ad_soyad(hesap_no):
    try:
        with open("musteriler.json", "r", encoding='utf-8') as dosya:
            data = json.load(dosya)
            musteriler = data["musteriler"]
            
            for musteri in musteriler:
                if str(musteri["hesap_no"]) == str(hesap_no):
                    return f"{musteri['ad']} {musteri['soyad']}"
    except Exception as e:
        print(f"\n❌ Bir hata oluştu: {str(e)}")
        return "Bilinmiyor"
    
    return "Bilinmiyor"

def hesap_bilgilerini_goruntule(hesap_no):
    try:
        with open("hesaplar.json", "r", encoding='utf-8') as dosya:
            data = json.load(dosya)
            hesaplar = data["hesaplar"]
            
            hesap = next((h for h in hesaplar if str(h["hesap_no"]) == str(hesap_no)), None)
            
            if hesap:
                print("\n========================================")
                print("💰 HESAP BİLGİLERİ")
                print("========================================")
                print(f"💵 Türk Lirası : {hesap['bakiye_tl']:,.2f} TL")
                print(f"💵 Dolar      : {hesap['bakiye_usd']:,.2f} USD")
                print(f"💵 Euro       : {hesap['bakiye_eur']:,.2f} EUR")
                print(f"🏆 Altın      : {hesap['bakiye_altin']:,.2f} gram")
                print(f"🥈 Gümüş      : {hesap['bakiye_gumus']:,.2f} gram")
                print("========================================")
                return
                
        print("\n❌ Hesap bulunamadı!")
        
    except FileNotFoundError:
        print("\n❌ Hesap bilgileri dosyası bulunamadı!")
    except Exception as e:
        print(f"\n❌ Bir hata oluştu: {str(e)}")

def para_transferi_yap(gonderen_hesap_no, alici_hesap_no, miktar, birim):
    try:
        birim = birim.lower()  # Birim ismini küçük harfe çevir
        
        with open("hesaplar.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            hesaplar = data["hesaplar"]
            
            # Gönderen ve alıcı hesapları bul
            gonderen = None
            alici = None
            for hesap in hesaplar:
                if str(hesap["hesap_no"]) == str(gonderen_hesap_no):
                    gonderen = hesap
                if str(hesap["hesap_no"]) == str(alici_hesap_no):
                    alici = hesap
                    
            if not gonderen or not alici:
                return False

            # Bakiye anahtarını belirle (TL için özel durum)
            bakiye_key = "bakiye_tl" if birim == "tl" else f"bakiye_{birim}"

            # String bakiyeleri float'a çevir
            gonderen_bakiye = float(gonderen[bakiye_key])
            alici_bakiye = float(alici[bakiye_key])

            if gonderen_bakiye >= float(miktar):
                # Bakiyeleri güncelle
                gonderen[bakiye_key] = str(gonderen_bakiye - float(miktar))
                alici[bakiye_key] = str(alici_bakiye + float(miktar))
                
                # Değişiklikleri kaydet
                with open("hesaplar.json", "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
                return True
                
            return False
            
    except Exception as e:
        print(f"Para transferi hatası: {str(e)}")
        return False

def islem_kaydet(hesap_no, islem_tipi, miktar, birim, aciklama, kur=None, karsi_hesap=None):
    try:
        # Mevcut işlemleri oku veya yeni dosya oluştur
        try:
            with open("islem_gecmisi.json", "r", encoding="utf-8") as dosya:
                data = json.load(dosya)
        except FileNotFoundError:
            # Dosya yoksa yeni bir veri yapısı oluştur
            data = {"islemler": []}
            
        # Yeni işlem kaydı oluştur
        yeni_islem = {
            "hesap_no": str(hesap_no),
            "tarih": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "islem_tipi": islem_tipi,
            "miktar": float(miktar),
            "birim": birim,
            "aciklama": aciklama
        }
        
        # Opsiyonel alanları ekle
        if kur:
            yeni_islem["kur"] = float(kur)
        if karsi_hesap:
            yeni_islem["karsi_hesap"] = str(karsi_hesap)
        
        # İşlemi listeye ekle
        data["islemler"].append(yeni_islem)
        
        # Dosyaya kaydet
        with open("islem_gecmisi.json", "w", encoding="utf-8") as dosya:
            json.dump(data, dosya, indent=4, ensure_ascii=False)
            
        return True
            
    except Exception as e:
        print(f"\n❌ İşlem kaydedilirken hata oluştu: {str(e)}")
        return False

def islem_gecmisi(hesap_no):
    try:
        # İşlem geçmişi dosyasını kontrol et, yoksa oluştur
        try:
            with open("islem_gecmisi.json", "r", encoding="utf-8") as dosya:
                data = json.load(dosya)
        except FileNotFoundError:
            # Dosya yoksa yeni bir dosya oluştur
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
            
        print("\n" + "=" * 40)
        print("📋 İŞLEM GEÇMİŞİ")
        print("=" * 40)
        
        for islem in reversed(musteri_islemleri):  # En son işlemden başlayarak göster
            print(f"Tarih      : {islem['tarih']}")
            print(f"İşlem Tipi : {islem['islem_tipi']}")
            print(f"Miktar     : {islem['miktar']} {islem['birim']}")
            if "kur" in islem:
                print(f"Kur        : {islem['kur']:.4f}")
            if "karsi_hesap" in islem:
                print(f"Karşı Hesap: {islem['karsi_hesap']}")
            print(f"Açıklama   : {islem['aciklama']}")
            print("-" * 40)
            
    except Exception as e:
        print(f"\n❌ İşlem geçmişi görüntülenirken hata oluştu: {str(e)}")
    
    input("\nDevam etmek için Enter'a basın...")

def para_transferi(hesap_no):
    try:
        with open("hesaplar.json", "r", encoding="utf-8") as dosya:
            data = json.load(dosya)
            hesaplar = data["hesaplar"]
            
            gonderen = next((h for h in hesaplar if str(h["hesap_no"]) == str(hesap_no)), None)
            
            if not gonderen:
                print("\n❌ Hesap bulunamadı!")
                return
                
            print("\n" + "=" * 40)
            print("💸 PARA TRANSFERİ")
            print("=" * 40)
            print(f"Mevcut Bakiye: {gonderen['bakiye_tl']:,.2f} TL")
            
            alici_hesap_no = input("\nAlıcı Hesap No: ")
            miktar = float(input("Transfer Miktarı (TL): "))
            
            if miktar <= 0:
                print("\n❌ Geçersiz miktar!")
                return
                
            if miktar > gonderen["bakiye_tl"]:
                print("\n❌ Yetersiz bakiye!")
                return
                
            if para_transferi_yap(hesap_no, alici_hesap_no, miktar, "tl"):
                islem_kaydet(
                    hesap_no=hesap_no,
                    islem_tipi="Para Transferi",
                    miktar=miktar,
                    birim="TL",
                    aciklama=f"Hesap No: {alici_hesap_no}'ya transfer",
                    karsi_hesap=alici_hesap_no
                )
                print("\n✅ Transfer başarıyla gerçekleşti!")
            else:
                print("\n❌ Transfer başarısız!")
                
    except ValueError:
        print("\n❌ Geçersiz miktar!")
    except Exception as e:
        print(f"\n❌ Bir hata oluştu: {str(e)}")