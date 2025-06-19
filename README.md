# Panduan Menjalankan Aplikasi Dashboard

Aplikasi ini dibuat menggunakan **Python** dengan framework **Streamlit** untuk visualisasi data dalam bentuk dashboard interaktif, serta menggunakan **PostgreSQL** sebagai sistem manajemen data warehouse. File SQL untuk data warehouse sudah tersedia dan dapat langsung diimport.

Aplikasi dapat diakses melalui: 

**https://chicagocrimedashboard.streamlit.app/**

Apabila ingin melakukan installasi dan menjalankan aplikasi di lingkungan lokal Anda, dapat pengikut langkah-langkah sebagai berikut:

## Prasyarat

Sebelum memulai, pastikan Anda telah menginstal software berikut:

1. **Python** - Unduh dan instal dari [situs resmi Python](https://www.python.org/).
2. **PostgreSQL** - Unduh dan instal dari [situs resmi PostgreSQL](https://www.postgresql.org/).
3. **Git** (opsional) - Unduh dan instal dari [situs resmi Git](https://git-scm.com/).
4. pip – biasanya sudah termasuk saat menginstal Python

---

## Langkah-langkah Menjalankan Aplikasi

### 1. Clone atau Unduh Repository

Pertama, clone repositori ini ke komputer lokal Anda menggunakan perintah berikut:  
 ```bash
git clone https://github.com/ghinaanfasha/chicago_crime_dashboard.git
 ```   
Jika Anda tidak menggunakan Git, Anda dapat mengunduh repositori ini dalam bentuk ZIP dan mengekstraknya.

### 2.Buat & Konfigurasi PostgreSQL

Buka pgAdmin lalu buat database baru dengan nama:

**chicago_crime**

Atau bisa menggunakan nama lain, sesuaikan dengan konfigurasi aplikasi nantinya.
Lalu Import file SQL dari folder database ke database yang baru dibuat:

  a. **Buka SQL Shell (psql)**  

  Saat instalasi PostgreSQL, biasanya sudah ada aplikasi SQL Shell (psql).
        
  b. **Ikuti prompt:**  
        - Server [localhost]    : (enter saja kalau localhost)
        - Database              : masukkan nama database tujuan
        - Port [5432]           : (enter saja kalau port 5432)
        - Username [postgres]   : (enter saja kalau username postgres)
        - Password              : masukkan password
        
  c. **Setelah masuk, masukkan path file sql**:
 ```bash
 \i 'C:/path/ke/file.sql'
 ```
     	
### 3. Konfigurasi Koneksi Database
Buka file db_config.py dan pastikan konfigurasi seperti berikut:
 ```bash
 DB_CONFIG = {
    'host': 'localhost',
    'port': '5432',
    'database': 'nama_database',
    'user': 'postgres',
    'password': 'password'
}
 ```

Sesuaikan kongurasi diatas dengan konfigurasi database PostgreSQL anda

### 4. Instalasi Dependensi Python

Setelah database dibuat, jalankan perintah berikut di terminal untuk menginstall dependensi yang dibutuhkan:  
 ```bash
 pip install -r requirements.txt
 ```

### 5. Jalankan Aplikasi Dashboard

Setelah semua langkah di atas selesai, Anda dapat menjalankan aplikasi dengan perintah:  
 ```bash
 streamlit run main.py
 ```
Aplikasi akan berjalan di **http://localhost:8501**. Buka alamat tersebut di browser Anda.
