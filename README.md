# BeritaSearch - Dense Retrieval

Project akhir mata kuliah Temu Kembali Informasi. Aplikasi ini adalah Search Engine Tematik menggunakan metode **Dense Retrieval**.

## Arsitektur Sistem

- Frontend: Laravel (Blade Template)
- Backend: Python (FastAPI)
- Model AI: Sentence-Transformers (all-mpnet-base-v2)
- Vector Database: FAISS

## Cara Menjalankan Project

### 1\. Menjalankan Mesin AI (Backend)

1. Buka terminal, masuk ke folder `python\_backend`
2. Instal library: `pip install -r requirements.txt`
3. Lakukan Indexing dataset: `python index\_data.py` (tunggu hingga selesai)
4. Jalankan server: `python app.py`

### 2\. Menjalankan Tampilan Web (Frontend)

1. Buka terminal baru di folder utama project.
2. Jalankan perintah: `composer install`
3. Jalankan server web: `php artisan serve`
4. Buka browser dan akses: `http://localhost:8000`
