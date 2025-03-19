from dosya_islemleri_modul import para_transferi_yap, islem_kaydet
from kur_bilgileri import KurBilgileri

def doviz_kiymetli_maden_alim_satim(hesap_no):
    print("\n--- Döviz/Kıymetli Maden Alış Satış İşlemleri ---")
    print("1. USD Al")
    print("2. EUR Al")
    print("3. USD Sat")
    print("4. EUR Sat")
    print("5. Altın Al (Gram)")
    print("6. Altın Sat (Gram)")
    print("7. Gümüş Al (Gram)")
    print("8. Gümüş Sat (Gram)")
    print("9. Ana Menüye Dön")

    secim = input("Seçiminiz: ")

    if secim == '1':
        doviz_al(hesap_no, "usd")
    elif secim == '2':
        doviz_al(hesap_no, "eur")
    elif secim == '3':
        doviz_sat(hesap_no, "usd")
    elif secim == '4':
        doviz_sat(hesap_no, "eur")
    elif secim == '5':
        altin_al(hesap_no)
    elif secim == '6':
        altin_sat(hesap_no)
    elif secim == '7':
        gumus_al(hesap_no)
    elif secim == '8':
        gumus_sat(hesap_no)
    elif secim == '9':
        from musteri_islemleri import musteri_menu
        musteri_menu(hesap_no)
    else:
        print("Geçersiz seçim!")
        doviz_kiymetli_maden_alim_satim(hesap_no)

def doviz_al(hesap_no, doviz_tipi):
    kb = KurBilgileri()
    alis_kuru, _ = kb.kur_bilgisi_al(doviz_tipi.upper())
    
    if not alis_kuru:
        raise Exception("Kur bilgisi alınamadı!")
        
    print(f"\nGüncel {doviz_tipi.upper()}/TL Kuru: {alis_kuru}")
    miktar = float(input(f"\nAlmak istediğiniz {doviz_tipi.upper()} miktarı: "))
    
    if miktar <= 0:
        raise Exception("Geçersiz miktar!")
        
    toplam_tutar = miktar * alis_kuru
    
    # TL çek ve döviz ekle
    if para_transferi_yap(hesap_no, "BANK", toplam_tutar, "tl"):
        if para_transferi_yap("BANK", hesap_no, miktar, doviz_tipi.lower()):
            # İşlemi kaydet
            islem_kaydet(
                hesap_no=hesap_no,
                islem_tipi=f"{doviz_tipi.upper()} Alış",
                miktar=miktar,
                birim=doviz_tipi.upper(),
                aciklama=f"{doviz_tipi.upper()} alış işlemi",
                kur=alis_kuru
            )
            return True
    return False

def doviz_sat(hesap_no, doviz_tipi):
    kb = KurBilgileri()
    _, satis_kuru = kb.kur_bilgisi_al(doviz_tipi.upper())
    
    if not satis_kuru:
        raise Exception("Kur bilgisi alınamadı!")
        
    print(f"\nGüncel {doviz_tipi.upper()}/TL Kuru: {satis_kuru}")
    miktar = float(input(f"\nSatmak istediğiniz {doviz_tipi.upper()} miktarı: "))
    
    if miktar <= 0:
        raise Exception("Geçersiz miktar!")
        
    toplam_tutar = miktar * satis_kuru
    
    # Döviz çek ve TL ekle
    if para_transferi_yap(hesap_no, "BANK", miktar, doviz_tipi.lower()):
        if para_transferi_yap("BANK", hesap_no, toplam_tutar, "tl"):
            # İşlemi kaydet
            islem_kaydet(
                hesap_no=hesap_no,
                islem_tipi=f"{doviz_tipi.upper()} Satış",
                miktar=miktar,
                birim=doviz_tipi.upper(),
                aciklama=f"{doviz_tipi.upper()} satış işlemi",
                kur=satis_kuru
            )
            return True
    return False

def altin_al(hesap_no):
    kb = KurBilgileri()
    alis_kuru, _ = kb.kur_bilgisi_al('ALTIN')
    
    if not alis_kuru:
        raise Exception("Altın kuru alınamadı!")
        
    print(f"\nGüncel Altın/TL Kuru: {alis_kuru}")
    miktar = float(input("\nAlmak istediğiniz altın miktarı (gr): "))
    
    if miktar <= 0:
        raise Exception("Geçersiz miktar!")
        
    toplam_tutar = miktar * alis_kuru
    
    # TL çek ve altın ekle
    if para_transferi_yap(hesap_no, "BANK", toplam_tutar, "tl"):
        if para_transferi_yap("BANK", hesap_no, miktar, "altin"):
            # İşlemi kaydet
            islem_kaydet(
                hesap_no=hesap_no,
                islem_tipi="Altın Alış",
                miktar=miktar,
                birim="ALTIN",
                aciklama="Altın alış işlemi",
                kur=alis_kuru
            )
            return True
    return False

def altin_sat(hesap_no):
    kb = KurBilgileri()
    _, satis_kuru = kb.kur_bilgisi_al('ALTIN')
    
    if not satis_kuru:
        raise Exception("Altın kuru alınamadı!")
        
    print(f"\nGüncel Altın/TL Kuru: {satis_kuru}")
    miktar = float(input("\nSatmak istediğiniz altın miktarı (gr): "))
    
    if miktar <= 0:
        raise Exception("Geçersiz miktar!")
        
    toplam_tutar = miktar * satis_kuru
    
    # Altın çek ve TL ekle
    if para_transferi_yap(hesap_no, "BANK", miktar, "altin"):
        if para_transferi_yap("BANK", hesap_no, toplam_tutar, "tl"):
            # İşlemi kaydet
            islem_kaydet(
                hesap_no=hesap_no,
                islem_tipi="Altın Satış",
                miktar=miktar,
                birim="ALTIN",
                aciklama="Altın satış işlemi",
                kur=satis_kuru
            )
            return True
    return False

def gumus_al(hesap_no):
    kb = KurBilgileri()
    alis_kuru, _ = kb.kur_bilgisi_al('GUMUS')
    
    if not alis_kuru:
        raise Exception("Gümüş kuru alınamadı!")
        
    print(f"\nGüncel Gümüş/TL Kuru: {alis_kuru}")
    miktar = float(input("\nAlmak istediğiniz gümüş miktarı (gr): "))
    
    if miktar <= 0:
        raise Exception("Geçersiz miktar!")
        
    toplam_tutar = miktar * alis_kuru
    
    # TL çek ve gümüş ekle
    if para_transferi_yap(hesap_no, "BANK", toplam_tutar, "tl"):
        if para_transferi_yap("BANK", hesap_no, miktar, "gumus"):
            # İşlemi kaydet
            islem_kaydet(
                hesap_no=hesap_no,
                islem_tipi="Gümüş Alış",
                miktar=miktar,
                birim="GUMUS",
                aciklama="Gümüş alış işlemi",
                kur=alis_kuru
            )
            return True
    return False

def gumus_sat(hesap_no):
    kb = KurBilgileri()
    _, satis_kuru = kb.kur_bilgisi_al('GUMUS')
    
    if not satis_kuru:
        raise Exception("Gümüş kuru alınamadı!")
        
    print(f"\nGüncel Gümüş/TL Kuru: {satis_kuru}")
    miktar = float(input("\nSatmak istediğiniz gümüş miktarı (gr): "))
    
    if miktar <= 0:
        raise Exception("Geçersiz miktar!")
        
    toplam_tutar = miktar * satis_kuru
    
    # Gümüş çek ve TL ekle
    if para_transferi_yap(hesap_no, "BANK", miktar, "gumus"):
        if para_transferi_yap("BANK", hesap_no, toplam_tutar, "tl"):
            # İşlemi kaydet
            islem_kaydet(
                hesap_no=hesap_no,
                islem_tipi="Gümüş Satış",
                miktar=miktar,
                birim="GUMUS",
                aciklama="Gümüş satış işlemi",
                kur=satis_kuru
            )
            return True
    return False