from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import json
import os
from kur_bilgileri import KurBilgileri
from dosya_islemleri_modul import para_transferi_yap, islem_kaydet  # Eklenen import
from datetime import datetime  # Ekleyin

app = Flask(__name__, static_folder='static')
app.secret_key = 'gizli_anahtar_123'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        hesap_no = request.form.get('hesap_no')
        sifre = request.form.get('sifre')
        
        print(f"Giriş denemesi - Hesap No: {hesap_no}")
        
        try:
            with open("musteriler.json", "r", encoding="utf-8") as f:
                musteriler = json.load(f)
                for musteri in musteriler["musteriler"]:
                    if str(musteri["hesap_no"]) == str(hesap_no) and str(musteri["sifre"]) == str(sifre):
                        session['hesap_no'] = hesap_no
                        session['ad_soyad'] = f"{musteri['ad']} {musteri['soyad']}"
                        print(f"Giriş başarılı: {musteri['ad']} {musteri['soyad']}")
                        # Transfer mesajını temizle
                        if 'transfer_sonuc' in session:
                            session.pop('transfer_sonuc')
                        return redirect('/kullanici-menu')
                
                flash('Geçersiz hesap numarası veya şifre!', 'error')
                
        except Exception as e:
            print(f"Hata: {str(e)}")
            flash('Giriş yapılırken bir hata oluştu!', 'error')
    
    return render_template('index.html')

@app.route('/kullanici-menu')
def kullanici_menu():
    if 'hesap_no' not in session:
        return redirect(url_for('login'))
    
    try:
        with open("hesaplar.json", "r", encoding="utf-8") as f:
            hesaplar = json.load(f)
            for hesap in hesaplar["hesaplar"]:
                if str(hesap["hesap_no"]) == str(session['hesap_no']):
                    print(f"Kullanıcı menüsü gösteriliyor: {session['ad_soyad']}")
                    return render_template('kullanici_menu.html', hesap=hesap)
    except Exception as e:
        print(f"Hata: {str(e)}")
        session.clear()
        return redirect('/')
    
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/kullanici-bilgileri')
def kullanici_bilgileri():
    if 'hesap_no' not in session:
        return redirect('/')
    
    try:
        with open("musteriler.json", "r", encoding="utf-8") as f:
            musteriler = json.load(f)
            for musteri in musteriler["musteriler"]:
                if str(musteri["hesap_no"]) == str(session['hesap_no']):
                    return render_template('kullanici_bilgileri.html', musteri=musteri)
    except Exception as e:
        print(f"Hata: {str(e)}")
        return redirect('/')
    
    return redirect('/')

@app.route('/hesap-bilgileri')
def hesap_bilgileri():
    if 'hesap_no' not in session:
        return redirect('/')
    
    try:
        with open("hesaplar.json", "r", encoding="utf-8") as f:
            hesaplar = json.load(f)
            for hesap in hesaplar["hesaplar"]:
                if str(hesap["hesap_no"]) == str(session['hesap_no']):
                    return render_template('hesap_bilgileri.html', hesap=hesap)
    except Exception as e:
        print(f"Hata: {str(e)}")
        return redirect('/')
    
    return redirect('/')

@app.route('/para-transferi', methods=['GET', 'POST'])
def para_transferi():
    if 'hesap_no' not in session:
        return redirect('/')
    
    bakiyeler = {'tl': 0, 'usd': 0, 'eur': 0, 'altin': 0, 'gumus': 0}
    try:
        with open("hesaplar.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            
        # Gönderen hesabın bakiyelerini al
        for hesap in data["hesaplar"]:
            if str(hesap["hesap_no"]) == str(session['hesap_no']):
                bakiyeler = {
                    'tl': float(hesap['bakiye_tl']),
                    'usd': float(hesap['bakiye_usd']),
                    'eur': float(hesap['bakiye_eur']), 
                    'altin': float(hesap['bakiye_altin']),
                    'gumus': float(hesap['bakiye_gumus'])
                }
                break

        if request.method == 'POST':
            alici_hesap_no = str(request.form.get('alici_hesap_no'))
            transfer_turu = str(request.form.get('transfer_turu'))
            miktar = float(request.form.get('miktar', 0))
            aciklama = request.form.get('aciklama', '')

            # Kendi hesabına transfer kontrolü
            if str(alici_hesap_no) == str(session['hesap_no']):
                flash('Kendinize transfer yapamazsınız!', 'error')
                return render_template('transfer.html', bakiyeler=bakiyeler)

            # Alıcı hesabın varlığını ve bilgilerini kontrol et
            alici_hesap = None
            musteri_adi = None
            
            # Önce hesap varlığını kontrol et
            with open("hesaplar.json", "r", encoding="utf-8") as f:
                hesaplar_data = json.load(f)
                for hesap in hesaplar_data["hesaplar"]:
                    if str(hesap["hesap_no"]) == str(alici_hesap_no):
                        alici_hesap = hesap
                        break
            
            if not alici_hesap:
                flash('Alıcı hesap bulunamadı!', 'error')
                return render_template('transfer.html', bakiyeler=bakiyeler)

            # Transfer işlemlerini gerçekleştir
            if miktar <= 0:
                flash('Geçersiz transfer miktarı!', 'error')
                return render_template('transfer.html', bakiyeler=bakiyeler)

            bakiye_key = f'bakiye_{transfer_turu.lower()}'
            if float(miktar) > bakiyeler[transfer_turu.lower()]:
                flash(f'Yetersiz {transfer_turu.upper()} bakiyesi!', 'error')
                return render_template('transfer.html', bakiyeler=bakiyeler)

            # Transfer işlemini gerçekleştir
            for i, hesap in enumerate(data["hesaplar"]):
                if str(hesap["hesap_no"]) == str(session['hesap_no']):
                    gonderici_bakiye = float(hesap[bakiye_key])
                    data["hesaplar"][i][bakiye_key] = str(gonderici_bakiye - miktar)
                elif str(hesap["hesap_no"]) == str(alici_hesap_no):
                    alici_bakiye = float(hesap[bakiye_key])
                    data["hesaplar"][i][bakiye_key] = str(alici_bakiye + miktar)

            # Dosyayı güncelle
            with open("hesaplar.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            # İşlem kaydını tut
            islem_kaydet(
                hesap_no=str(session['hesap_no']),
                islem_tipi="Para Transferi",
                miktar=float(miktar),
                birim=transfer_turu.upper(),
                aciklama=aciklama,
                karsi_hesap=alici_hesap_no
            )

            # Transfer başarılı olduğunda
            with open("musteriler.json", "r", encoding="utf-8") as f:
                musteriler = json.load(f)
                for musteri in musteriler["musteriler"]:
                    if str(musteri["hesap_no"]) == alici_hesap_no:
                        alici_adi = f"{musteri['ad']} {musteri['soyad']}"
                        session['transfer_sonuc'] = {
                            'tip': 'success',
                            'mesaj': f'{miktar} {transfer_turu.upper()} başarıyla transfer edildi!',
                            'miktar': f"{miktar:.2f}",
                            'birim': transfer_turu.upper(),
                            'alici': alici_adi
                        }
                        break

            return redirect(url_for('kullanici_menu'))

    except Exception as e:
        print(f"Transfer sırasında hata: {str(e)}")
        flash('Bir hata oluştu!', 'error')
    
    return render_template('transfer.html', bakiyeler=bakiyeler)

@app.route('/get_musteri_bilgisi/<hesap_no>')
def get_musteri_bilgisi(hesap_no):
    try:
        with open("musteriler.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            for musteri in data["musteriler"]:
                if str(musteri["hesap_no"]) == str(hesap_no):
                    return jsonify({
                        'success': True,
                        'ad': musteri['ad'],
                        'soyad': musteri['soyad']
                    })
        return jsonify({'success': False})
    except Exception as e:
        print(f"Hata: {str(e)}")
        return jsonify({'success': False})

@app.route('/doviz-bilgileri')
def doviz_bilgileri():
    if 'hesap_no' not in session:
        return redirect('/')
    
    try:
        kur = KurBilgileri()
        kurlar = kur.get_all_rates()
        guncelleme = datetime.now().strftime("%H:%M:%S")
        
        print("Debug - Kurlar:", kurlar)  # Debug için
        print("Debug - Template rendering başlıyor")  # Debug için
        
        return render_template(
            'doviz_bilgileri.html',
            kurlar=kurlar,
            guncelleme=guncelleme
        )
    except Exception as e:
        print(f"Hata oluştu: {str(e)}")  # Debug için
        flash('Döviz bilgileri alınırken bir hata oluştu!', 'error')
        return redirect('/kullanici-menu')

@app.route('/doviz-islem', methods=['GET', 'POST'])
def doviz_islem():
    if 'hesap_no' not in session:
        return redirect('/')
        
    try:
        # Bakiye bilgilerini al
        with open("hesaplar.json", "r", encoding="utf-8") as f:
            hesaplar = json.load(f)
            for hesap in hesaplar["hesaplar"]:
                if str(hesap["hesap_no"]) == str(session['hesap_no']):
                    bakiyeler = {
                        'tl': float(hesap['bakiye_tl']),
                        'usd': float(hesap['bakiye_usd']),
                        'eur': float(hesap['bakiye_eur']),
                        'altin': float(hesap['bakiye_altin']),
                        'gumus': float(hesap['bakiye_gumus'])
                    }
                    
                    # Güncel kurları al
                    kur = KurBilgileri()
                    kurlar = kur.get_all_rates()
                    
                    return render_template(
                        'doviz_islem.html',
                        bakiyeler=bakiyeler,
                        kurlar=kurlar,
                        datetime=datetime  # datetime modülünü template'e gönder
                    )
                    
        flash('Hesap bilgileri alınamadı!', 'error')
        return redirect('/kullanici-menu')
        
    except Exception as e:
        print(f"Hata: {str(e)}")
        flash('Bir hata oluştu!', 'error')
        return redirect('/kullanici-menu')

@app.route('/doviz-islem-detay/<birim>/<islem_turu>')
def doviz_islem_detay(birim, islem_turu):
    if 'hesap_no' not in session:
        return redirect('/')
        
    try:
        # Kullanıcı bakiyelerini al
        with open("hesaplar.json", "r", encoding="utf-8") as f:
            hesaplar = json.load(f)
            for hesap in hesaplar["hesaplar"]:
                if str(hesap["hesap_no"]) == str(session['hesap_no']):
                    bakiyeler = {
                        'tl': float(hesap['bakiye_tl']),
                        'usd': float(hesap['bakiye_usd']),
                        'eur': float(hesap['bakiye_eur']),
                        'altin': float(hesap['bakiye_altin']),
                        'gumus': float(hesap['bakiye_gumus'])
                    }
                    
                    # Güncel kurları al
                    kur = KurBilgileri()
                    kurlar = kur.get_all_rates()
                    
                    return render_template(
                        'doviz_islem_detay.html',
                        birim=birim,
                        islem_turu=islem_turu,
                        bakiyeler=bakiyeler,
                        kurlar=kurlar
                    )
                    
        flash('Hesap bilgileri alınamadı!', 'error')
        return redirect('/kullanici-menu')
        
    except Exception as e:
        print(f"Hata: {str(e)}")
        flash('Bir hata oluştu!', 'error')
        return redirect('/kullanici-menu')

@app.route('/doviz-islem-yap', methods=['GET', 'POST'])
def doviz_islem_yap():
    if 'hesap_no' not in session:
        return redirect('/')
    
    birim = request.args.get('birim')
    islem_turu = request.args.get('islem_turu')
    
    if request.method == 'GET':
        try:
            # Kullanıcı bakiyelerini al
            with open("hesaplar.json", "r", encoding="utf-8") as f:
                hesaplar = json.load(f)
                for hesap in hesaplar["hesaplar"]:
                    if str(hesap["hesap_no"]) == str(session['hesap_no']):
                        bakiyeler = {
                            'tl': float(hesap['bakiye_tl']),
                            'usd': float(hesap['bakiye_usd']),
                            'eur': float(hesap['bakiye_eur']),
                            'altin': float(hesap['bakiye_altin']),
                            'gumus': float(hesap['bakiye_gumus'])
                        }
                        
                        # Güncel kurları al
                        kur = KurBilgileri()
                        kurlar = kur.get_all_rates()
                        
                        return render_template(
                            'doviz_islem_detay.html',
                            birim=birim,
                            islem_turu=islem_turu,
                            bakiyeler=bakiyeler,
                            kurlar=kurlar
                        )
                        
            flash('Hesap bilgileri alınamadı!', 'error')
            return redirect('/kullanici-menu')
            
        except Exception as e:
            print(f"Hata: {str(e)}")
            flash('Bir hata oluştu!', 'error')
            return redirect('/kullanici-menu')
    
    try:
        birim = request.form.get('birim')
        islem_turu = request.form.get('islem_turu')
        miktar = float(request.form.get('miktar', 0))

        if not all([birim, islem_turu, miktar]):
            flash('Tüm alanları doldurunuz!', 'error')
            return redirect(f'/doviz-islem-detay/{birim}')

        # Hesap bilgilerini al
        with open("hesaplar.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            hesaplar = data["hesaplar"]
            
            # Kullanıcının hesabını bul
            hesap = next((h for h in hesaplar if str(h["hesap_no"]) == str(session['hesap_no'])), None)
            
            if not hesap:
                flash('Hesap bilgileri alınamadı!', 'error')
                return redirect('/kullanici-menu')

            # Güncel kurları al
            kur = KurBilgileri()
            kurlar = kur.get_all_rates()
            
            # TL ve birim bakiyelerini float'a çevir
            tl_bakiye = float(hesap['bakiye_tl'])
            birim_bakiye = float(hesap[f'bakiye_{birim.lower()}'])
            
            # İşlem türüne göre kontrol ve hesaplama
            if islem_turu == 'alis':
                total_tl = miktar * kurlar[birim]['satis']
                if total_tl > tl_bakiye:
                    flash('Yetersiz TL bakiye!', 'error')
                    return redirect(f'/doviz-islem-detay/{birim}')
                    
                # Alış işlemi
                hesap['bakiye_tl'] = str(tl_bakiye - total_tl)
                hesap[f'bakiye_{birim.lower()}'] = str(birim_bakiye + miktar)
                islem_aciklama = f"{miktar} {birim} Alış"
                
            else:  # satış işlemi
                if miktar > birim_bakiye:
                    flash(f'Yetersiz {birim} bakiye!', 'error')
                    return redirect(f'/doviz-islem-detay/{birim}')
                    
                # Satış işlemi
                total_tl = miktar * kurlar[birim]['alis']
                hesap['bakiye_tl'] = str(tl_bakiye + total_tl)
                hesap[f'bakiye_{birim.lower()}'] = str(birim_bakiye - miktar)
                islem_aciklama = f"{miktar} {birim} Satış"

            # Değişiklikleri kaydet
            with open("hesaplar.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
                
            # İşlem kaydını tut
            islem_kaydet(
                hesap_no=str(session['hesap_no']),
                islem_tipi=f"Döviz İşlemi ({islem_turu.upper()})",
                miktar=miktar,
                birim=birim,
                aciklama=islem_aciklama,
                kur=kurlar[birim]['satis'] if islem_turu == 'alis' else kurlar[birim]['alis']
            )
            
            # İşlem başarılı olduğunda session'a bilgi ekle
            session['doviz_islem_sonuc'] = {  # transfer_sonuc yerine doviz_islem_sonuc kullanıyoruz
                'tip': 'success',
                'mesaj': f'İşlem başarıyla gerçekleştirildi!',
                'miktar': f"{miktar:.2f}",
                'birim': birim,
                'islem_turu': islem_turu.upper(),
                'toplam_tl': f"{total_tl:.2f}",
                'kur': f"{kurlar[birim]['satis' if islem_turu == 'alis' else 'alis']:.4f}",
                'yeni_bakiye': f"{float(hesap[f'bakiye_{birim.lower()}']):.2f}",
                'yeni_tl_bakiye': f"{float(hesap['bakiye_tl']):.2f}"  # Yeni TL bakiye eklendi
            }
            
            return redirect('/kullanici-menu')
            
    except Exception as e:
        print(f"Döviz işlemi hatası: {str(e)}")
        flash('İşlem sırasında bir hata oluştu!', 'error')
        return redirect('/kullanici-menu')

@app.route('/islem-gecmisi')
def islem_gecmisi():
    if 'hesap_no' not in session:
        return redirect('/')
        
    try:
        with open('islem_gecmisi.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Kullanıcıya ait işlemleri filtrele ve tarihe göre sırala
            islemler = [i for i in data['islemler'] if str(i['hesap_no']) == str(session['hesap_no'])]
            islemler.reverse()  # En son işlemler başta görünsün
            return render_template('islem_gecmisi.html', islemler=islemler)
    except Exception as e:
        print(f"Hata: {str(e)}")
        flash('İşlem geçmişi alınırken bir hata oluştu!', 'error')
        return redirect('/kullanici-menu')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/clear_transfer_message')
def clear_transfer_message():
    if 'transfer_sonuc' in session:
        session.pop('transfer_sonuc')
    return '', 204

@app.route('/clear_doviz_message')
def clear_doviz_message():
    if 'doviz_islem_sonuc' in session:
        session.pop('doviz_islem_sonuc')
    return '', 204

@app.route('/yonetici-giris', methods=['GET', 'POST'])
def yonetici_login():
    if request.method == 'POST':
        sifre = request.form.get('sifre')
        
        if sifre == "0616":  # Yönetici şifresi
            session['yonetici'] = True
            flash('Başarıyla giriş yapıldı!', 'success')
            return redirect(url_for('yonetici_panel'))
        else:
            flash('Geçersiz şifre!', 'error')
            
    return render_template('yonetici_giris.html')

@app.route('/yonetici-panel')
def yonetici_panel():
    if not session.get('yonetici'):
        return redirect(url_for('yonetici_login'))
    
    try:
        with open("musteriler.json", "r", encoding="utf-8") as f:
            musteriler = json.load(f)
        with open("hesaplar.json", "r", encoding="utf-8") as f:
            hesaplar = json.load(f)
            
        return render_template(
            'yonetici_panel.html', 
            musteriler=musteriler["musteriler"],
            hesaplar=hesaplar["hesaplar"]
        )
    except Exception as e:
        print(f"Hata: {str(e)}")
        flash('Veriler yüklenirken bir hata oluştu!', 'error')
        return redirect(url_for('index'))

@app.route('/musteri-detay/<hesap_no>')
def musteri_detay(hesap_no):
    if not session.get('yonetici'):
        return jsonify({'success': False, 'message': 'Yetkiniz yok!'})
    
    try:
        # Müşteri bilgilerini al
        with open("musteriler.json", "r", encoding="utf-8") as f:
            musteriler = json.load(f)
            musteri = next((m for m in musteriler["musteriler"] 
                          if str(m["hesap_no"]) == str(hesap_no)), None)
        
        # Hesap bilgilerini al
        with open("hesaplar.json", "r", encoding="utf-8") as f:
            hesaplar = json.load(f)
            hesap = next((h for h in hesaplar["hesaplar"] 
                         if str(h["hesap_no"]) == str(hesap_no)), None)
        
        # İşlem geçmişini al
        with open("islem_gecmisi.json", "r", encoding="utf-8") as f:
            gecmis = json.load(f)
            islemler = [i for i in gecmis["islemler"] if str(i["hesap_no"]) == str(hesap_no)]
            islemler.reverse()  # En son işlemler başta
        
        if musteri and hesap:
            return jsonify({
                'success': True,
                'musteri': musteri,
                'hesap': hesap,
                'islemler': islemler
            })
            
        return jsonify({'success': False, 'message': 'Müşteri bulunamadı!'})
        
    except Exception as e:
        print(f"Hata: {str(e)}")
        return jsonify({'success': False, 'message': 'Bir hata oluştu!'})

@app.route('/yeni-musteri', methods=['GET', 'POST'])
def yeni_musteri_kayit():
    if request.method == 'POST':
        try:
            # Müşteri verilerini hazırla
            yeni_musteri = {
                "ad": request.form['ad'].strip(),
                "soyad": request.form['soyad'].strip(),
                "tc_no": request.form['tc_no'],
                "dogum_tarihi": request.form['dogum_tarihi'],
                "sifre": request.form['sifre'],
                "telefon": request.form['telefon'],
                "email": request.form['email'],
                "adres": request.form['adres']
            }
            
            # Müşteri verilerini musteriler.json'a kaydet
            with open("musteriler.json", "r+", encoding="utf-8") as f:
                data = json.load(f)
                hesap_no = str(len(data["musteriler"]) + 1000)
                yeni_musteri["hesap_no"] = hesap_no
                data["musteriler"].append(yeni_musteri)
                f.seek(0)
                json.dump(data, f, indent=4, ensure_ascii=False)
                f.truncate()
            
            # Hesap bilgilerini hesaplar.json'a kaydet
            with open("hesaplar.json", "r+", encoding="utf-8") as f:
                data = json.load(f)
                yeni_hesap = {
                    "hesap_no": hesap_no,
                    "bakiye_tl": "0",
                    "bakiye_usd": "0",
                    "bakiye_eur": "0",
                    "bakiye_altin": "0",
                    "bakiye_gumus": "0"
                }
                data["hesaplar"].append(yeni_hesap)
                f.seek(0)
                json.dump(data, f, indent=4, ensure_ascii=False)
                f.truncate()
            
            flash(f'Kayıt başarıyla oluşturuldu! Hesap numaranız: {hesap_no}', 'success')
            return redirect(url_for('index'))
            
        except Exception as e:
            print(f"Kayıt hatası: {str(e)}")
            flash('Kayıt oluşturulurken bir hata oluştu!', 'error')
            
    return render_template('yeni_musteri.html')

if __name__ == '__main__':
    print("\nUygulama başlatılıyor...")
    print("Tarayıcıda şu adresi açın: http://localhost:8080")
    app.run(host='localhost', port=8080, debug=True)