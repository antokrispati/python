from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
import re

# Daftar URL yang discrape
urls = [
    # "https://www.vidio.com/live/734-trans7",
    # "https://www.vidio.com/live/733-trans-tv",
    "https://www.vidio.com/live/204-sctv",
    "https://www.vidio.com/live/205-indosiar",
    "https://www.vidio.com/live/777-metro-tv",
    "https://www.vidio.com/live/783-tvone",
    "https://www.vidio.com/live/874-kompas-tv",
    "https://www.vidio.com/live/782-antv",
    "https://www.vidio.com/live/1561-rtv",
    "https://www.vidio.com/live/206-moji"
]
    
# Setup Selenium Webdriver
driver = webdriver.Chrome()

# Hasil data akan disimpan di sini
results = []

# Fungsi untuk mengambil angka penonton (menghapus huruf "K" dan mengkonversi ke angka)
def extract_view_count(text):
    # Mencari angka sebelum huruf "K"
    match = re.search(r'(\d+(\.\d+)?)\s*K?', text)
    if match:
        return float(match.group(1)) * 1000 if 'K' in text else float(match.group(1))
    return None

# Loop untuk setiap URL
for url in urls:
    driver.get(url)  # Buka URL
    time.sleep(3)  # Tunggu hingga halaman selesai dimuat

    # Ambil source HTML dan parsing dengan BeautifulSoup
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")

   
    # 1. Ambil Judul Program
    h1_element = soup.find("p", {"data-testid": "secondary-title"})
    nama_chanel = h1_element.text.split("•")[0].strip() if h1_element else "Tidak ditemukan"

    # 2. Ambil jumlah penonton
    p_element = soup.find("p", {"data-testid": "secondary-title"})
    if p_element:
        span_in_p = p_element.find("span")
        if span_in_p:
            jumlah_penonton = extract_view_count(span_in_p.text)
        

    # 3. Filter Acara dengan Status LIVE
    acara_live = soup.find_all("div", class_="schedule-card-module_container__52wDH")
    for acara in acara_live:
        # Cek apakah ada label LIVE
        live_label = acara.find("span", class_="badge-label-module_live__rC2JM")
        if live_label and "LIVE" in live_label.text:
            # Ambil jadwal waktu
            jadwal_waktu = acara.find("div", class_="schedule-card-module_time__25AcS")
            jadwal_waktu = jadwal_waktu.text if jadwal_waktu else "Tidak ditemukan"

            # Ambil nama acara
            nama_acara = acara.find("div", class_="schedule-card-module_title__JUdOU")
            nama_acara = nama_acara.text if nama_acara else "Tidak ditemukan"

            # Cetak hasil
            # print("Nama Chanel:", nama_chanel)
            # print("Jumlah Penonton:", jumlah_penonton)
            # print("Jadwal Waktu:", jadwal_waktu)
            # print("Nama Acara:", nama_acara)
            # print("Status: LIVE")
            # print("=" * 50)
            
            #Tambahkan data ke list
            results.append({"Nama Channel": nama_chanel,
                              "Jumlah Penonton": jumlah_penonton,
                              "Waktu": jadwal_waktu,
                              "Nama Acara": nama_acara
                              })

# Tutup browser setelah selesai
driver.quit()

# Simpan data ke file Excel
df = pd.DataFrame(results)
df.to_excel("Data_Vidio.com.xlsx", index=False)

print("Data berhasil disimpan ke file hasil_scraping.xlsx")