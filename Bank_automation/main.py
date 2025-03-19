from musteri_islemleri import giris_yap, kullanici_bilgileri, hesap_bilgileri, para_transferi, doviz_bilgileri, doviz_islemleri, islem_gecmisi
from admin_panel import AdminPanel  # AdminPanel sınıfını import et
import json
from datetime import datetime

def giris_menusu():
    while True:
        print("\n" + "=" * 40)
        print("🏦 BANKA SİSTEMİNE HOŞGELDİNİZ")
        print("========================================")
        print("1️⃣  Müşteri Girişi")
        print("2️⃣  Yeni Müşteri Ol")
        print("3️⃣  Yönetici Girişi")
        print("0️⃣  Çıkış")
        print("========================================")

        secim = input("\nSeçiminiz: ")
        return secim

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
            print("7️⃣  Çıkış")
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
            elif secim == "7":
                print("\n" + "=" * 40)
                print("👋 İyi günler dileriz!")
                print("=" * 40 + "\n")
                break
            else:
                print("\n❌ Geçersiz seçim! Lütfen tekrar deneyin.")
                
    except Exception as e:
        print(f"\n❌ Bir hata oluştu: {str(e)}")

def yeni_musteri_kaydi():
    print("\n========================================")
    print("📝 YENİ MÜŞTERİ KAYDI")
    print("========================================")
    
    try:
        # Mevcut müşterileri oku
        with open('musteriler.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            musteriler = data["musteriler"]
        
        # Yeni hesap numarası oluştur
        son_hesap_no = max([int(m['hesap_no']) for m in musteriler]) if musteriler else 1110
        yeni_hesap_no = str(son_hesap_no + 1)
        
        # Yeni müşteri bilgilerini al
        ad = input("Adı: ")
        soyad = input("Soyadı: ")
        dogum_tarihi = input("Doğum Tarihi (GG/AA/YYYY): ")
        
        # Yaş kontrolü
        gun, ay, yil = map(int, dogum_tarihi.split('/'))
        dogum = datetime(yil, ay, gun)
        yas = (datetime.now() - dogum).days / 365
        if yas < 18:
            print("❌ 18 yaşından küçük kişiler müşteri olamaz!")
            return
            
        while True:
            tc_kimlik = input("TC Kimlik Numarası: ")
            if len(tc_kimlik) != 11 or not tc_kimlik.isdigit():
                print("❌ TC Kimlik Numarası 11 haneli olmalıdır!")
                continue
            break
            
        telefon = input("Telefon Numarası: ")
        email = input("Email Adresi: ")
        adres = input("Adresi: ")
        sifre = input("Şifre: ")
        
        # Yeni müşteri objesi
        yeni_musteri = {
            "hesap_no": yeni_hesap_no,
            "ad": ad,
            "soyad": soyad,
            "dogum_tarihi": dogum_tarihi,
            "tc_kimlik_no": tc_kimlik,
            "telefon": telefon,
            "email": email,
            "adres": adres,
            "sifre": sifre,
            "islem_gecmisi": []
        }
        
        # Müşteri listesine ekle
        musteriler.append(yeni_musteri)
        
        # Müşteri dosyasını güncelle
        with open('musteriler.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
            
        # Hesap bilgilerini oku
        with open('hesaplar.json', 'r', encoding='utf-8') as file:
            hesap_data = json.load(file)
            
        # Yeni hesap objesi
        yeni_hesap = {
            "hesap_no": yeni_hesap_no,
            "bakiye_tl": 0.0,
            "bakiye_usd": 0.0,
            "bakiye_eur": 0.0,
            "bakiye_altin": 0.0,
            "bakiye_gumus": 0.0
        }
        
        # Hesap listesine ekle
        hesap_data["hesaplar"].append(yeni_hesap)
        
        # Hesap dosyasını güncelle
        with open('hesaplar.json', 'w', encoding='utf-8') as file:
            json.dump(hesap_data, file, indent=4, ensure_ascii=False)
            
        print("\n✅ Müşteri kaydı başarıyla oluşturuldu!")
        print(f"👤 Hesap Numaranız: {yeni_hesap_no}")
        print("🔑 Giriş yapmak için bu bilgileri kullanabilirsiniz.")
        
    except ValueError as e:
        print("❌ Geçersiz tarih formatı!")
    except FileNotFoundError:
        print("❌ Sistem dosyaları bulunamadı!")
    except Exception as e:
        print(f"❌ Bir hata oluştu: {str(e)}")
    
    input("\nDevam etmek için Enter'a basın...")

# Ana program
if __name__ == "__main__":
    admin_panel = AdminPanel()  # AdminPanel örneği oluştur
    
    while True:
        secim = giris_menusu()
        if secim == "1":
            print("\n" + "=" * 40)
            print("🔐 MÜŞTERİ GİRİŞİ")
            print("=" * 40)
            hesap_no = input("Hesap No: ")
            sifre = input("Şifre: ")
            
            basarili, hesap_no = giris_yap(hesap_no, sifre)  # hesap_no olarak değiştirildi
            if basarili:
                kullanici_menusu(hesap_no)  # Direkt hesap_no gönderiliyor
            
        elif secim == "2":
            yeni_musteri_kaydi()
            
        elif secim == "3":
            admin_panel.admin_login()  # Yönetici girişini çağır
                
        elif secim == "0":
            print("\n" + "=" * 40)
            print("👋 İyi günler dileriz!")
            print("=" * 40 + "\n")
            break
        else:
            print("\n❌ Geçersiz seçim! Lütfen tekrar deneyin.")