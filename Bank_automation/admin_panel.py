import json
from datetime import datetime

class AdminPanel:
    def __init__(self):
        self.admin_id = "0616"  # Yönetici ID'si kurallara göre güncellendi
        self.customers = []  # Müşteri listesi

    def admin_login(self):
        print("\n========================================")
        print("🔐 YÖNETİCİ GİRİŞİ")
        print("========================================")
        
        admin_input = input("Yönetici ID: ")
        
        if admin_input == self.admin_id:
            print("\n✅ Giriş başarılı!")
            self.show_admin_menu()
            return True
        else:
            print("\n❌ Hatalı Yönetici ID!")
            return False

    def show_admin_menu(self):
        while True:
            print("\n========================================")
            print("🔧 YÖNETİCİ PANELİ")
            print("========================================")
            print("1️⃣  Tüm Müşterileri Listele")
            print("0️⃣  Çıkış")
            print("========================================")
            
            secim = input("Seçiminiz: ")
            
            if secim == "1":
                self.tum_musterileri_listele()
            elif secim == "0":
                print("✅ Yönetici panelinden çıkış yapıldı.")
                break
            else:
                print("❌ Geçersiz seçim!")

    def tum_musterileri_listele(self):
        try:
            with open('musteriler.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
                musteriler = data["musteriler"]
            
            if not musteriler:
                print("❌ Kayıtlı müşteri bulunmamaktadır.")
                return
            
            while True:
                print("\n📋 MÜŞTERİ LİSTESİ")
                print("=" * 50)
                
                # Süslü numaralar listesi
                sayilar = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
                
                # Müşteri listesini oluştur
                musteri_listesi = {}  # Seçim numarası -> müşteri eşleşmesi için sözlük
                for i, musteri in enumerate(musteriler, 1):
                    musteri_listesi[str(i)] = musteri
                    sayi = sayilar[i-1] if i <= len(sayilar) else f"{i}."
                    print(f"{sayi} 👤 {musteri['ad']} {musteri['soyad']} (Hesap No: {musteri['hesap_no']})")
                
                print("0️⃣ Çıkış")
                print("\nDetaylı bilgi görüntülemek için müşteri numarasını girin")
                secim = input("Seçiminiz: ")
                
                if secim == "0":
                    break
                    
                if secim in musteri_listesi:
                    self.musteri_detay_goster(musteri_listesi[secim])
        except Exception as e:
            print(f"❌ Hata oluştu: {str(e)}")

    def musteri_detay_goster(self, musteri):
        while True:
            print("\n" + "=" * 50)
            print("🔍 MÜŞTERİ DETAY MENÜSÜ")
            print("=" * 50)
            print(f"👤 {musteri['ad'].upper()} {musteri['soyad'].upper()}")
            print("-" * 50)
            print("1️⃣  Kişisel Bilgileri Görüntüle")
            print("2️⃣  İşlem Geçmişini Görüntüle")
            print("0️⃣  Geri Dön")
            print("-" * 50)
            
            secim = input("\nSeçiminiz: ")
            
            if secim == "1":
                self.musteri_bilgileri_goster(musteri)
            elif secim == "2":
                self.musteri_gecmis_goster(musteri)
            elif secim == "0":
                break
            else:
                print("\n❌ Geçersiz seçim!")

    def musteri_bilgileri_goster(self, musteri):
        try:
            print("\n" + "=" * 50)
            print("🔍 MÜŞTERİ BİLGİLERİ")
            print("=" * 50)
            
            # Kişisel Bilgiler Bölümü
            print("\n👤 KİŞİSEL BİLGİLER")
            print("-" * 50)
            print(f"📋 Ad Soyad        : {musteri['ad'].title()} {musteri['soyad'].title()}")
            print(f"🆔 Hesap No        : {musteri['hesap_no']}")
            print(f"🪪 TC Kimlik No    : {musteri.get('tc_kimlik_no', musteri.get('tc_no', 'Bilgi yok'))}")
            print(f"📅 Doğum Tarihi    : {musteri['dogum_tarihi']}")
            
            # İletişim Bilgileri Bölümü
            print("\n📞 İLETİŞİM BİLGİLERİ")
            print("-" * 50)
            print(f"📱 Telefon         : {musteri['telefon']}")
            print(f"📧 Email           : {musteri['email']}")
            print(f"📍 Adres          : {musteri['adres']}")
            
            # Bakiye Bilgileri Bölümü
            print("\n💰 BAKİYE BİLGİLERİ")
            print("-" * 50)
            with open("hesaplar.json", "r", encoding="utf-8") as dosya:
                data = json.load(dosya)
                hesap = next((h for h in data["hesaplar"] if str(h["hesap_no"]) == str(musteri["hesap_no"])), None)
                
            if hesap:
                print(f"💵 Türk Lirası     : {float(hesap['bakiye_tl']):,.2f} TL")
                print(f"💵 Dolar           : {float(hesap['bakiye_usd']):,.2f} USD")
                print(f"💶 Euro            : {float(hesap['bakiye_eur']):,.2f} EUR")
                print(f"🏆 Altın           : {float(hesap['bakiye_altin']):,.2f} gr")
                print(f"🥈 Gümüş           : {float(hesap['bakiye_gumus']):,.2f} gr")
            else:
                print("\n❌ Bakiye bilgisi bulunamadı!")
            
            print("\n" + "=" * 50)
            edit_choice = input("\n📝 Bilgileri düzenlemek ister misiniz? (1: Evet / 0: Hayır): ")
            if edit_choice == "1":
                self.edit_customer_details(musteri)

        except Exception as e:
            print(f"\n❌ Bir hata oluştu: {str(e)}")

    def edit_customer_details(self, musteri):
        print("\n📝 MÜŞTERİ BİLGİLERİNİ DÜZENLE")
        print("=" * 50)
        
        # Kişisel Bilgiler
        print("👤 KİŞİSEL BİLGİLER")
        print("-" * 50)
        print("1. Ad")
        print("2. Soyad")
        print("3. TC Kimlik No")
        print("4. Hesap No")
        print("5. Doğum Tarihi")
        
        # İletişim Bilgileri
        print("\n📞 İLETİŞİM BİLGİLERİ")
        print("-" * 50)
        print("6. Telefon Numarası")
        print("7. Email Adresi")
        print("8. Adres")
        
        print("\n0. Geri Dön")
        
        while True:
            secim = input("\nDüzenlemek istediğiniz bilgiyi seçin: ")
            
            if secim == "0":
                break
            elif secim == "1":
                yeni_ad = input("Yeni Ad: ")
                if yeni_ad:
                    musteri['ad'] = yeni_ad
            elif secim == "2":
                yeni_soyad = input("Yeni Soyad: ")
                if yeni_soyad:
                    musteri['soyad'] = yeni_soyad
            elif secim == "3":
                yeni_tc = input("Yeni TC Kimlik No: ")
                if yeni_tc and len(yeni_tc) == 11 and yeni_tc.isdigit():
                    musteri['tc_kimlik_no'] = yeni_tc
                else:
                    print("❌ Geçersiz TC Kimlik No! 11 haneli rakam olmalıdır.")
                    continue
            elif secim == "4":
                yeni_hesap_no = input("Yeni Hesap No: ")
                if yeni_hesap_no:
                    musteri['hesap_no'] = yeni_hesap_no
            elif secim == "5":
                yeni_dogum_tarihi = input("Yeni Doğum Tarihi (GG/AA/YYYY): ")
                if yeni_dogum_tarihi:
                    musteri['dogum_tarihi'] = yeni_dogum_tarihi
            elif secim == "6":
                yeni_telefon = input("Yeni Telefon Numarası: ")
                if yeni_telefon:
                    musteri['telefon'] = yeni_telefon
            elif secim == "7":
                yeni_email = input("Yeni Email Adresi: ")
                if yeni_email:
                    musteri['email'] = yeni_email
            elif secim == "8":
                yeni_adres = input("Yeni Adres: ")
                if yeni_adres:
                    musteri['adres'] = yeni_adres
            else:
                print("❌ Geçersiz seçim!")
                continue
                
            # Değişiklikleri kaydet
            try:
                with open('musteriler.json', 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    
                # Müşteriyi güncelle
                for i, m in enumerate(data['musteriler']):
                    if m['hesap_no'] == musteri['hesap_no']:
                        data['musteriler'][i] = musteri
                        break
                        
                with open('musteriler.json', 'w', encoding='utf-8') as file:
                    json.dump(data, file, indent=4, ensure_ascii=False)
                    
                print("\n✅ Bilgiler başarıyla güncellendi!")
                
            except Exception as e:
                print(f"\n❌ Güncelleme sırasında hata oluştu: {str(e)}")
            
            devam = input("\nBaşka bir bilgi düzenlemek ister misiniz? (1: Evet / 0: Hayır): ")
            if devam != "1":
                break

    def musteri_gecmis_goster(self, musteri):
        try:
            # İşlem geçmişi dosyasını kontrol et
            try:
                with open("islem_gecmisi.json", "r", encoding="utf-8") as dosya:
                    data = json.load(dosya)
            except FileNotFoundError:
                print("\n❌ Henüz işlem geçmişi bulunmuyor.")
                return
                
            # Müşteriye ait işlemleri filtrele
            musteri_islemleri = [i for i in data.get("islemler", []) if str(i["hesap_no"]) == str(musteri["hesap_no"])]
            
            if not musteri_islemleri:
                print("\n❌ İşlem geçmişi bulunamadı!")
                return
                
            print("\n" + "=" * 50)
            print(f"📋 {musteri['ad'].upper()} {musteri['soyad'].upper()} İŞLEM GEÇMİŞİ")
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
        
        input("\nAna menüye dönmek için Enter'a basın...")

    def list_all_customers(self):
        if not self.customers:
            print("\n❌ Kayıtlı müşteri bulunmamaktadır.")
            return

        print("\n=== MÜŞTERİ LİSTESİ ===")
        for i, customer in enumerate(self.customers, 1):
            print(f"{i}. 👤 {customer.name} {customer.surname} (Hesap No: {customer.account_number})")
        
        while True:
            customer_choice = input("\nDetaylı bilgi görüntülemek için müşteri numarasını girin (Çıkış için 0): ")
            
            if customer_choice == "0":
                break
                
            try:
                customer_index = int(customer_choice) - 1
                if 0 <= customer_index < len(self.customers):
                    self.show_customer_details_menu(self.customers[customer_index])
                else:
                    print("\n❌ Geçersiz müşteri numarası!")
            except ValueError:
                print("\n❌ Geçersiz giriş!")

    def show_customer_details_menu(self, customer):
        while True:
            print("\n1. Müşteri Bilgileri Görüntüle")
            print("2. Müşteri Geçmişi Görüntüle")
            print("3. Geri Dön")
            
            choice = input("\nSeçiminiz: ")
            
            if choice == "1":
                self.display_customer_details(customer)
            elif choice == "2":
                self.display_customer_history(customer)
            elif choice == "3":
                break
            else:
                print("\n❌ Geçersiz seçim!")

    def display_customer_details(self, customer):
        print("\n=== MÜŞTERİ DETAY BİLGİLERİ ===")
        print(f"👤 Müşteri Adı Soyadı: {customer.name} {customer.surname}")
        print(f"👤 TC Kimlik Numarası: {customer.tc_no}")
        print(f"👤 Doğum Tarihi: {customer.birth_date}")
        print(f"👤 Hesap Numarası: {customer.account_number}")
        print(f"👤 Telefon Numarası: {customer.phone}")
        print(f"👤 Email Adresi: {customer.email}")
        print(f"👤 Adresi: {customer.address}")
        
        print("\n=== BAKİYE BİLGİLERİ ===")
        print(f"💰 Türk Lirası Bakiyesi: {customer.balance_tl} TL")
        print(f"💰 Dolar Bakiyesi: {customer.balance_usd} USD")
        print(f"💰 Euro Bakiyesi: {customer.balance_eur} EUR")
        print(f"💰 Altın Bakiyesi: {customer.balance_gold} gr")
        print(f"💰 Gümüş Bakiyesi: {customer.balance_silver} gr")
        
        edit_choice = input("\nBilgileri düzenlemek ister misiniz? (1/0): ")
        if edit_choice == "1":
            self.edit_customer_details(customer)

    def display_customer_history(self, customer):
        print("\n=== MÜŞTERİ İŞLEM GEÇMİŞİ ===")
        if not customer.transaction_history:
            print("❌ İşlem geçmişi bulunmamaktadır.")
            return
            
        for transaction in customer.transaction_history:
            print(f"\nTarih: {transaction.date}")
            print(f"İşlem Tipi: {transaction.type}")
            print(f"İşlem Miktarı: {transaction.amount}")
            print(f"Hesap: {transaction.account}")
            print(f"İşlem Açıklaması: {transaction.description}")
            print("-" * 40)