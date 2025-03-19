import requests
from datetime import datetime
import json
import time

class KurBilgileri:
    def __init__(self):
        self.rates = {
            'USD': {'alis': 0, 'satis': 0},
            'EUR': {'alis': 0, 'satis': 0},
            'ALTIN': {'alis': 0, 'satis': 0},
            'GUMUS': {'alis': 0, 'satis': 0}
        }
        self.last_update = None
        self.update_interval = 300  # 5 dakika

    def fetch_rates(self):
        try:
            api_url = "https://api.exchangerate-api.com/v4/latest/USD"
            response = requests.get(api_url)
            
            if response.status_code != 200:
                raise Exception("API'den veri alınamadı")

            data = response.json()
            usd_try = data['rates']['TRY']
            eur_try = (data['rates']['TRY'] / data['rates']['EUR'])

            # Alış ve satış kurlarını hesapla (spread %1)
            self.rates = {
                'USD': {
                    'alis': round(usd_try * 0.995, 4),
                    'satis': round(usd_try * 1.005, 4)
                },
                'EUR': {
                    'alis': round(eur_try * 0.995, 4),
                    'satis': round(eur_try * 1.005, 4)
                },
                'ALTIN': {
                    'alis': round(usd_try * 1950 / 31.1 * 0.99, 4),
                    'satis': round(usd_try * 1950 / 31.1 * 1.01, 4)
                },
                'GUMUS': {
                    'alis': round(usd_try * 25 / 31.1 * 0.99, 4),
                    'satis': round(usd_try * 25 / 31.1 * 1.01, 4)
                }
            }
            
            self.last_update = datetime.now()
            print(f"✅ Kurlar güncellendi - {self.get_last_update()}")
            return True

        except Exception as e:
            print(f"❌ Kur bilgileri çekilirken hata oluştu: {str(e)}")
            # Hata durumunda örnek değerler
            self.rates = {
                'USD': {'alis': 31.52, 'satis': 31.72},
                'EUR': {'alis': 34.15, 'satis': 34.35},
                'ALTIN': {'alis': 2175.50, 'satis': 2185.50},
                'GUMUS': {'alis': 25.75, 'satis': 26.25}
            }
            return False

    def get_all_rates(self):
        # Eğer hiç veri yoksa veya son güncellemeden 5 dk geçtiyse
        if (not self.last_update or 
            (datetime.now() - self.last_update).seconds > self.update_interval):
            self.fetch_rates()
        return self.rates

    def get_last_update(self):
        if self.last_update:
            return self.last_update.strftime("%H:%M:%S")
        return "Güncelleme bilgisi yok"

    def kur_bilgisi_al(self, birim):
        """Belirli bir birimin alış ve satış kurlarını döndürür"""
        kurlar = self.get_all_rates()
        if birim in kurlar:
            return kurlar[birim]['alis'], kurlar[birim]['satis']
        return None, None

    def guncel_kurlari_goster(self):
        """Güncel kurları ekrana yazdırır"""
        kurlar = self.get_all_rates()
        
        print("\n" + "=" * 40)
        print("💱 GÜNCEL DÖVİZ VE EMTİA KURLARI")
        print("=" * 40)
        
        # USD kurları
        print("\n💵 DOLAR (USD)")
        print("-" * 20)
        print(f"Alış  : {kurlar['USD']['alis']:.4f} TL")
        print(f"Satış : {kurlar['USD']['satis']:.4f} TL")
        
        # EUR kurları
        print("\n💶 EURO (EUR)")
        print("-" * 20)
        print(f"Alış  : {kurlar['EUR']['alis']:.4f} TL")
        print(f"Satış : {kurlar['EUR']['satis']:.4f} TL")
        
        # Altın kurları
        print("\n🏆 ALTIN (GR)")
        print("-" * 20)
        print(f"Alış  : {kurlar['ALTIN']['alis']:.4f} TL")
        print(f"Satış : {kurlar['ALTIN']['satis']:.4f} TL")
        
        # Gümüş kurları
        print("\n🥈 GÜMÜŞ (GR)")
        print("-" * 20)
        print(f"Alış  : {kurlar['GUMUS']['alis']:.4f} TL")
        print(f"Satış : {kurlar['GUMUS']['satis']:.4f} TL")
        
        # Son güncelleme bilgisi
        print("\n🕒 Son Güncelleme:", self.get_last_update())
        print("=" * 40)

# Test
if __name__ == "__main__":
    kurlar = KurBilgileri()
    print("\n💱 Kur Bilgileri Test")
    print("=" * 30)
    
    rates = kurlar.get_all_rates()
    if rates:
        print(f"\n💵 Dolar    : Alış: {rates['USD']['alis']:.4f} TL - Satış: {rates['USD']['satis']:.4f} TL")
        print(f"💶 Euro     : Alış: {rates['EUR']['alis']:.4f} TL - Satış: {rates['EUR']['satis']:.4f} TL")
        print(f"🏆 Altın    : Alış: {rates['ALTIN']['alis']:.4f} TL - Satış: {rates['ALTIN']['satis']:.4f} TL")
        print(f"🥈 Gümüş    : Alış: {rates['GUMUS']['alis']:.4f} TL - Satış: {rates['GUMUS']['satis']:.4f} TL")
        print(f"\n🕒 Son Güncelleme: {kurlar.get_last_update()}")
    else:
        print("\n❌ Kurlar alınamadı!")