# Gerekli Kütüphanelerin import edilmesi #
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys 
# Klavye komutlarını verebilmek için.
from selenium.webdriver.support.ui import WebDriverWait 
#time.sleep yerine, belirli bir elemanın görünür hale gelmesiyle işlem yapmasını sağlamak için.
from selenium.webdriver.support import expected_conditions as EC 
#time.sleep yerine, belirli bir elemanın görünür hale gelmesiyle işlem yapmasını sağlamak için.
import time
import path as ph
import pandas as pd
import os
import numpy as np
from selenium.common.exceptions import ElementClickInterceptedException

# path = ph.path_driver2
options = webdriver.FirefoxOptions()
# options.add_experimental_option("detach", True)
options.add_argument('--disable-notifications')
options.add_argument("--disable-infobars")
options.add_argument("start-maximized")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--ignore-certificate-errors")

driver = webdriver.Firefox(service = FirefoxService(GeckoDriverManager().install()))
driver.maximize_window()

driver.get(ph.url_proje_firefox)
wait = WebDriverWait(driver, 20)

UserName = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="otds_username"]')))
UserName.click()
UserName.send_keys(ph.User_Name)

time.sleep(1)

PassWord = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="otds_password"]')))
PassWord.click()
PassWord.send_keys(ph.User_Password)

time.sleep(1)

Sign = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="loginbutton"]')))
Sign.click()

time.sleep(2)
Abone_Proje_Arsivi = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="rowCell0"]/td[3]/a[1]')))
Abone_Proje_Arsivi.click()

time.sleep(1)
Proje_Arsivi = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="rowCell5"]/td[3]/a[1]')))
Proje_Arsivi.click()

time.sleep(1)
Name_Sirala = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="browseViewCoreTable"]/tbody/tr[1]/td[3]/a')))
Name_Sirala.click()

time.sleep(1)
I00001_2023 = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="rowCell1"]/td[3]/a[1]')))
I00001_2023.click()

time.sleep(1)
Name_Sirala_1 = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="browseViewCoreTable"]/tbody/tr[1]/td[3]/a')))
Name_Sirala_1.click()

ArsivNo = "I00001"
ArsivGrupNo = "I00001-2023"
ArsivNo_Yanlis = []
ArsivGrup_Yanlis = []
ProjeNo_Yanlis = []
Proje_Balya_Tipi_Durumu = []

time.sleep(1)
# Toplam kaç sayfa ve tiff var ?
Total_items = int(driver.find_element(By.XPATH, '/html/body/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr/td/form[3]/div/div/div/table/tbody/tr/td[2]/div/div[2]/table/tbody/tr/td/table/tbody/tr[2]/td[1]').text.split(" ")[-2])
Total_page = int(np.ceil(Total_items / 25))

print(f"\n I00001-2023 Klasöründe Toplam: {Total_items} Adet .tiff Dosyası Var.")

for x in range(67, (Total_page + 1)):
    print(f"\nToplam {Total_page} Tane Sayfa Var.\n")
    print(f"\n{x}. sayfada yer alan tifflerin bilgileri kontrol ediliyor.\n")
    if x != 1:
        BirPage_ileri = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#PageNextImg')))
        BirPage_ileri.click()
        time.sleep(2)
        page_count = []
        page_info = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="browseViewCoreTable"]'))).text.split("\n")
        for y in page_info:
            if y.strip().endswith(".tiff"):
                page = y.strip().replace(".tiff", "")
                page_count.append(page)
        for i in range(0, len(page_count)):
            print(f"\n {x}. Sayfanın, {i+1}. Projesi İşleme Alınıyor. (Proje Nosu: {page_count[i]})")
            time.sleep(0.5) # Minik bekleme
            try:
                Ilgili_Tiff = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f'#rowCell{i} > td.browseItemName > a:nth-child(2)')))  
                Ilgili_Tiff.click()
                Properties = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="menuItem_Properties"]')))
                Properties.click()
            except Exception as e:
                raise Exception(f"Proje No'nun Özelliklerine Gidilemedi !!! Hata: {str(e)}")

            time.sleep(1) # Bazen, tiff adını alamıyor. Eski isimde kalıyor.
            try:
                get_tiff = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr[2]/td/table/tbody/tr[1]/td/div/div[6]/div[2]'))).text.split(".")[0]
            except Exception as e:
                raise Exception(f"Proje Numarası Kopyalanamadı !!! Hata: {e}")


            #time.sleep(1)
            try:
                Categories = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="LLInnerContainer"]/tbody/tr[2]/td/table/tbody/tr[1]/td/form/table/tbody/tr[1]/td/ul/div[2]/li[5]')))
                Categories.click()
                time.sleep(0.2)
                print(f"{get_tiff} No'lu Projenin 'Arşiv Bilgisi' Ekranındayız.")
            except Exception as e:
                raise Exception(f"{get_tiff} No'lu Projenin Kategori Ekranına Geçilemedi !!! Hata: {e}")

            ####################################
            # Arşiv Bilgisi Kontrol
            #################################### 
            try:
                time.sleep(0.2)
                a = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#_1_1_2_1'))).get_attribute("value")
                if a == ArsivNo:
                    print(f"{get_tiff} No'lu Projenin Arşiv Numarası: {a} ve Doğru.")
                else:
                    print(f"{get_tiff} No'lu Projenin Arşiv Numarası: {a} ve Yanlış !")
                    print(f"{get_tiff} No'lu Proje 'Yanlış' Olarak Kaydediliyor !!!")
                    ArsivNo_Yanlis.append(get_tiff)
            except Exception as e:
                raise Exception(f"{get_tiff} No'lu Projenin 'Arşiv Numarası' Alınırken Hata Oluştu. Hata: {e}")

            try:
                time.sleep(0.2)
                b = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#_1_1_3_1'))).get_attribute("value")
                if b == ArsivGrupNo:
                    print(f"{get_tiff} No'lu Projenin Arşiv Grup Bilgisi: {b} ve Doğru.\n")
                else:
                    print(f"{get_tiff} No'lu Projenin Arşiv Grup Bilgisi: {b} ve Yanlış !")
                    print(f"{get_tiff} No'lu Proje 'Yanlış Arşiv Grup' Olarak Kaydediliyor !!!")
                    ArsivGrup_Yanlis.append(get_tiff)
            except Exception as e:
                raise Exception(f"{get_tiff} No'lu Projenin 'Arşiv Grup' Alınırken Hata Oluştu. Hata: {e}")

            ####################################
            # Proje Doküman Bilgisi
            #################################### 
            try:
                ProjeDokuman = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr/td/form/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr/td[3]/a')))
                ProjeDokuman.click()
                time.sleep(2)
                print(f"{get_tiff} No'lu Projenin 'Proje Doküman Bilgisi' Ekranındayız.")
                c = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#_1_1_2_1'))).get_attribute("value")
                d = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#_1_1_3_1'))).get_attribute("value")
                if c == get_tiff and d == get_tiff:
                    print(f"{get_tiff} No'lu Projenin Eski ve Yeni Proje Numarası: {c} ve Doğru.")
                else:
                    print(f"{get_tiff} No'lu Projenin Eski ve Yeni Proje Numarası: {c} ve Yanlış !!!")
                    print(f"{get_tiff} No'lu Proje 'Yanlış' Olarak Kaydediliyor !!!")
                    ProjeNo_Yanlis.append(get_tiff)
                time.sleep(0.2)
                e = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#_1_1_4_1'))).get_attribute("value")
                f = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#_1_1_5_1'))).get_attribute("value")
                g = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#_1_1_6_1'))).get_attribute("value")
                if e == ArsivNo and f == 'Proje' and g == 'Güncel':
                    print(f"{get_tiff} No'lu Projenin Balya Numarası - Proje Tipi ve Durumu Doğru.\n")
                    print("-" * 50)
                else:
                    print(f"{get_tiff} No'lu Projenin Balya Numarası - Proje Tipi ve Durumu Yanlış !!!")
                    print(f"{get_tiff} No'lu Proje 'Yanlış' Olarak Kaydediliyor !!!")
                    Proje_Balya_Tipi_Durumu.append(get_tiff)
            except Exception as e:
                raise Exception(f"{get_tiff} No'lu Projenin 'Proje Doküman Bilgisi' Alınırken Hata Oluştu. Hata: {e}")

            ####################################
            # Ana-Sayfaya Dönüş
            #################################### 
            try:
                AnaSayfa = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="80455978_0"]')))
                AnaSayfa.click()
                time.sleep(2)
            except Exception as e:
                raise Exception(f"{get_tiff} No'lu Projeden Sonra Ana-Sayfaya Dönüşte Hata Oluştu. Hata: {e}")

print(f"\nİşlem Tamamlandı!\n")
print(f"Yanlış Arşiv Numara Bilgisine Sahip olan Proje Sayısı: {len(ArsivNo_Yanlis)}")
print(f"Yanlış Arşiv Grup Bilgisine Sahip olan Proje Sayısı: {len(ArsivGrup_Yanlis)}")
print(f"Yanlış Proje Doküman Bilgisine Sahip olan Proje Sayısı: {len(ProjeNo_Yanlis)}")
print(f"Yanlış Proje Tipi Bilgisine Sahip olan Proje Sayısı: {len(Proje_Balya_Tipi_Durumu)}")