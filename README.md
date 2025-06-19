# Panduan Menjalankan Aplikasi Dashboard

Aplikasi ini dibuat menggunakan **Python** dengan framework **Streamlit** untuk visualisasi data dalam bentuk dashboard interaktif, serta menggunakan **PostgreSQL** sebagai sistem manajemen database. File SQL untuk database sudah tersedia dan dapat langsung diimpor.
Aplikasi dapat diakses melalui: 
**https://chicagocrimedashboard.streamlit.app/**

Apabila ingin melakukan installasi dan menjalankan aplikasi di lingkungan lokal anda, dapat pengikut langkah-langkah sebagai berikut:

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
**https://github.com/ghinaanfasha/chicago_crime_dashboard.git**    
Jika Anda tidak menggunakan Git, Anda dapat mengunduh repositori ini dalam bentuk ZIP dan mengekstraknya.

### 2.Buat & Konfigurasi Database PostgreSQL

1) Buka pgAdmin atau gunakan psql untuk membuat database baru dengan nama:
chicago_crime
2) Impor file SQL dari folder database/ ke database yang baru dibuat:

  a. **Melalui pgAdmin**  
      Klik kanan pada database → pilih **Restore** → pilih file `chicago_crime.sql` dari folder `database/`.

   b. **Melalui terminal**  
      Jalankan perintah berikut di terminal:

      ```bash
      psql -U postgres -d chicago_crime -f database/chicago_crime.sql
      ```
		

### 3. Konfigurasi Koneksi Database
Buka file db_config.py dan pastikan konfigurasi seperti berikut:
 ```bash
 DB_CONFIG = {
    'host': 'localhost',
    'port': '5432',
    'database': 'nama_database',
    'user': 'postgres',
    'password': 'password_anda'
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
