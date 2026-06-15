# Sistem Rekomendasi Anime 🎯

Proyek Machine Learning ini dikerjakan oleh:
- Alvey Reza Pahlevi
- Adriana Syahban

---

## 1. Business Understanding
* **Problem Statement:** Platform streaming anime seringkali kesulitan memberikan rekomendasi tontonan yang relevan secara personal di tengah membeludaknya rilisan judul baru setiap musim. Tanpa rekomendasi yang akurat, retensi pengguna dapat menurun.
* **Goals:** Membangun model machine learning untuk memprediksi dan merekomendasikan daftar Top-N anime yang kemungkinan besar akan disukai oleh pengguna berdasarkan riwayat interaksi mereka.
* **Solution Approach:** Menggunakan pendekatan Collaborative Filtering dengan algoritma Singular Value Decomposition (SVD).

## 2. Data Understanding
* Dataset yang digunakan bersumber dari data interaksi komunitas pecinta anime.
* Informasi utama yang digunakan terdiri dari `user_id`, `anime_id`, dan `rating` (skala 1-10) untuk membaca pola ketertarikan pengguna.

## 3. Data Preparation
* Data interaksi pengguna dimuat menggunakan modul Reader dan Dataset dari library surprise.
* Dataset dibagi menjadi himpunan data latih (training set) dan data uji (testing set) menggunakan teknik `train_test_split` dengan rasio 80:20 untuk mencegah overfitting.

## 4. Modeling
* Model dilatih menggunakan algoritma **Singular Value Decomposition (SVD)** melalui library `scikit-surprise`. 
* *Catatan Ekstra (Poin Plus):* Algoritma ini dipilih sebagai bentuk eksplorasi mandiri karena memberikan hasil prediksi yang lebih robust pada data sparse.

## 5. Evaluation
* Pengujian akurasi prediksi model dilakukan menggunakan metrik **Root Mean Square Error (RMSE)**.
* Hasil komputasi pada testing set menunjukkan nilai metrik RMSE sebesar **0.8969**, menandakan model memiliki tingkat kesalahan prediksi skor yang sangat minim dan layak pakai.

## 6. Deployment
* Model rekomendasi ini di-deploy menggunakan kerangka kerja **Streamlit** (sebagai nilai tambah/poin plus) untuk menghasilkan antarmuka web yang interaktif. File pendukung berupa `app.py` dan `requirements.txt` telah disertakan di dalam repositori ini.
