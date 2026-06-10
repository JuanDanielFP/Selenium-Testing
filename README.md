# Automation Testing - Selenium (Exercise 3-4)

Proyek ini berisi *script* otomatisasi pengujian (*Automation Testing*) menggunakan bahasa pemrograman **Python** dan **Selenium WebDriver**. Pengujian dilakukan pada website *e-commerce* demo: [SauceDemo](https://www.saucedemo.com/).

## 📌 Skenario Pengujian (*Test Cases*)
Pengujian yang diotomatisasi dalam *script* ini meliputi:
1. **Simulasi Register** (Simulasi *passed* karena website SauceDemo tidak menyediakan fitur *register*).
2. **Login Authentication** (Pengujian login *Positive* dan *Negative*).
3. **Sorting Produk** (Pengurutan nama A-Z dan harga *Low to High*).
4. **Checkout Process** (Skenario End-to-End: Tambah produk ke keranjang, navigasi ke *cart*, isi formulir *checkout*, hingga pemesanan selesai).

---

## 🛠️ Persyaratan Sistem (*Prerequisites*)
Sebelum menjalankan proyek ini, pastikan komputer Anda sudah terinstal:
- **Python 3.x** (Bisa diunduh di [python.org](https://www.python.org/))
- **Google Chrome** browser versi terbaru
- **Git** (Opsional, untuk melakukan *clone* repositori)

---

## 🚀 Cara Instalasi & Menjalankan Pengujian

### 1. Clone Repositori
Buka Terminal/Command Prompt/PowerShell Anda, lalu jalankan perintah berikut untuk mengunduh proyek ini:
```bash
git clone https://github.com/JuanDanielFP/Automation-Testing.git
cd Automation-Testing
```

### 2. Instalasi Dependencies (Library)
Proyek ini membutuhkan *library* Selenium agar bisa berjalan. Instal menggunakan PIP dengan perintah berikut:
```bash
pip install selenium
```

### 3. Menjalankan *Script* Automation
Setelah *library* terinstal, Anda dapat langsung menjalankan *script* pengujiannya:
```bash
python exercise3-4.py
```
> **Catatan:** Jika Anda pengguna Mac/Linux, Anda mungkin perlu menggunakan perintah `python3 exercise3-4.py` atau `pip3`.

---

## ⚙️ Konfigurasi Tambahan (Melihat Browser)
Secara bawaan (*default*), pengujian diatur untuk berjalan pada mode **Headless** (Proses browser berjalan di latar belakang tanpa memunculkan UI / jendela aplikasi browser). 

Jika Anda ingin **melihat browser bergerak secara langsung**, Anda bisa merubah konfigurasi di dalam file `exercise3-4.py`:
1. Buka file `exercise3-4.py`.
2. Cari fungsi `setUp(self)` di dalam `class BaseTest` (sekitar baris ke-19).
3. Ubah nilai variabel `headless` menjadi `False`:
   ```python
   headless = False  # Ubah ke False jika ingin melihat browser berjalan
   ```