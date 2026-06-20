# Laporan Proyek Machine Learning - Sistem Rekomendasi Anime 🎯

Proyek Machine Learning ini dikerjakan oleh:

* Alvey Reza Pahlevi
* Adriana Syahban

---

## Project Overview

Anime memiliki jumlah judul yang sangat banyak dengan genre, tipe, rating, dan tingkat popularitas yang beragam. Banyaknya pilihan tersebut dapat menyulitkan pengguna dalam menentukan anime yang ingin ditonton berikutnya. Oleh karena itu, sistem rekomendasi dibutuhkan untuk membantu pengguna menemukan anime yang lebih sesuai dengan preferensi mereka.

Proyek ini membangun sistem rekomendasi anime menggunakan dataset **Anime Recommendations Database**. Dataset tersebut berisi informasi anime dan data rating pengguna. Sistem rekomendasi dikembangkan menggunakan dua pendekatan, yaitu **Content-Based Filtering** dan **Collaborative Filtering**.

Manfaat proyek:

* Membantu pengguna menemukan anime berdasarkan kemiripan genre dan tipe.
* Memberikan rekomendasi personal berdasarkan pola rating pengguna.
* Membandingkan dua pendekatan sistem rekomendasi.

---

## Business Understanding

### Problem Statements

1. Bagaimana membangun sistem rekomendasi anime yang dapat membantu pengguna menemukan anime sesuai preferensi?
2. Bagaimana menerapkan pendekatan Content-Based Filtering dan Collaborative Filtering pada data anime?
3. Bagaimana membandingkan hasil rekomendasi dari kedua pendekatan tersebut?

### Goals

1. Mengembangkan sistem rekomendasi anime berbasis Machine Learning.
2. Menerapkan dua pendekatan, yaitu Content-Based Filtering dan Collaborative Filtering.
3. Mengevaluasi hasil rekomendasi berdasarkan kemiripan konten dan error prediksi rating.

### Solution Approach

1. **Content-Based Filtering**
   Sistem merekomendasikan anime berdasarkan kemiripan fitur seperti judul, genre, dan tipe anime. Fitur teks diubah menjadi representasi numerik menggunakan **TF-IDF**, kemudian dihitung tingkat kemiripannya menggunakan **Cosine Similarity**.

2. **Collaborative Filtering**
   Sistem merekomendasikan anime berdasarkan pola rating pengguna. Pendekatan ini memanfaatkan kemiripan antar pengguna menggunakan **User-Based Collaborative Filtering** untuk menghasilkan rekomendasi anime yang lebih personal.

---

## Data Understanding

Dataset yang digunakan berasal dari **Anime Recommendations Database**. Dataset asli terdiri dari dua file utama, yaitu `anime.csv` dan `rating.csv`.

Pada proyek ini digunakan data hasil sampling agar proses pemodelan dan deployment lebih ringan.

### Dataset Components

| Dataset           |         Jumlah Data | Fitur Utama                                            |
| ----------------- | ------------------: | ------------------------------------------------------ |
| anime_sample.csv  |      300 data anime | anime_id, name, genre, type, episodes, rating, members |
| rating_sample.csv | 103.449 data rating | user_id, anime_id, rating                              |

### Uraian Fitur

* **anime_id**: ID unik untuk setiap anime.
* **name**: Judul anime.
* **genre**: Genre anime.
* **type**: Tipe anime seperti TV, Movie, OVA, dan lainnya.
* **episodes**: Jumlah episode anime.
* **rating**: Rating rata-rata anime.
* **members**: Jumlah anggota komunitas yang menambahkan anime tersebut.
* **user_id**: ID unik pengguna.
* **rating**: Rating yang diberikan pengguna terhadap anime.

### Kondisi Data

Berdasarkan hasil pengecekan data:

* Dataset anime memiliki beberapa nilai kosong pada kolom tertentu seperti genre atau type.
* Dataset rating memiliki rating tidak valid bernilai `-1` pada dataset asli.
* Data asli berukuran cukup besar, sehingga dilakukan sampling agar aplikasi dapat berjalan lebih ringan di Streamlit.

---

## Exploratory Data Analysis (EDA)

EDA dilakukan untuk memahami karakteristik data sebelum proses modeling.

Beberapa analisis yang dilakukan:

1. Melihat anime terpopuler berdasarkan jumlah members.
2. Melihat distribusi rating pengguna.
3. Melihat genre anime yang paling banyak muncul.

Hasil EDA menunjukkan bahwa data anime memiliki variasi genre yang cukup luas. Selain itu, rating pengguna tersebar dalam beberapa nilai, sehingga data dapat digunakan untuk membangun sistem rekomendasi.

---

## Data Preparation

Tahapan data preparation dilakukan untuk memastikan data siap digunakan dalam proses pemodelan.

Langkah-langkah yang dilakukan:

1. Mengisi nilai kosong pada kolom `genre`, `type`, dan `name`.
2. Menghapus rating tidak valid bernilai `-1`.
3. Menghapus data duplikat pada anime dan rating.
4. Membuat fitur gabungan dari `name`, `genre`, dan `type` untuk Content-Based Filtering.
5. Membuat user-item matrix untuk Collaborative Filtering.
6. Membagi data train dan test untuk evaluasi prediksi rating.

Tahapan ini penting agar sistem rekomendasi dapat menghasilkan output yang lebih relevan dan mengurangi kesalahan akibat data kosong atau duplikat.

---

## Modeling and Results

Pada proyek ini digunakan dua pendekatan sistem rekomendasi.

### 1. Content-Based Filtering

Content-Based Filtering digunakan untuk merekomendasikan anime berdasarkan kemiripan konten. Fitur yang digunakan adalah gabungan dari judul anime, genre, dan tipe anime.

Tahapan model:

* Menggabungkan fitur `name`, `genre`, dan `type`.
* Mengubah teks menjadi vektor numerik menggunakan **TF-IDF Vectorizer**.
* Menghitung kemiripan antar anime menggunakan **Cosine Similarity**.
* Menampilkan Top-N anime yang paling mirip dengan anime pilihan pengguna.

Contoh hasil rekomendasi untuk anime **Dragon Ball**:

| Judul Anime        | Genre                                                                   | Tipe |
| ------------------ | ----------------------------------------------------------------------- | ---- |
| Dragon Ball Z      | Action, Adventure, Comedy, Fantasy, Martial Arts, Shounen, Super Power  | TV   |
| Dragon Ball GT     | Action, Adventure, Comedy, Fantasy, Magic, Sci-Fi, Shounen, Super Power | TV   |
| Naruto             | Action, Comedy, Martial Arts, Shounen, Super Power                      | TV   |
| Naruto: Shippuuden | Action, Comedy, Martial Arts, Shounen, Super Power                      | TV   |
| Katanagatari       | Action, Adventure, Historical, Martial Arts, Romance                    | TV   |

Kelebihan:

* Tidak membutuhkan data rating pengguna.
* Cocok untuk merekomendasikan anime dengan genre atau tipe yang mirip.

Kekurangan:

* Rekomendasi terbatas pada kemiripan konten.
* Belum mempertimbangkan selera personal pengguna.

---

### 2. Collaborative Filtering

Collaborative Filtering digunakan untuk merekomendasikan anime berdasarkan pola rating pengguna. Pendekatan ini mencari pengguna lain yang memiliki pola rating mirip, kemudian merekomendasikan anime yang disukai oleh pengguna serupa.

Tahapan model:

* Membuat user-item matrix berdasarkan `user_id`, `anime_id`, dan `rating`.
* Menghitung kemiripan antar pengguna menggunakan **Cosine Similarity**.
* Mengambil beberapa pengguna yang paling mirip.
* Menghasilkan rekomendasi anime berdasarkan rating dari pengguna-pengguna serupa.

Contoh hasil rekomendasi untuk salah satu User ID:

| Judul Anime             | Genre                                                             | Tipe |
| ----------------------- | ----------------------------------------------------------------- | ---- |
| One Punch Man           | Action, Comedy, Parody, Sci-Fi, Seinen, Super Power, Supernatural | TV   |
| Boku dake ga Inai Machi | Mystery, Psychological, Seinen, Supernatural                      | TV   |
| Baccano!                | Action, Comedy, Historical, Mystery, Seinen, Supernatural         | TV   |
| Shokugeki no Souma      | Ecchi, School, Shounen                                            | TV   |
| Haikyuu!! Second Season | Comedy, Drama, School, Shounen, Sports                            | TV   |

Kelebihan:

* Rekomendasi lebih personal karena mempertimbangkan pola rating pengguna.
* Dapat menemukan anime yang tidak selalu mirip secara genre, tetapi disukai oleh pengguna dengan pola minat serupa.

Kekurangan:

* Membutuhkan data interaksi pengguna yang cukup.
* Kurang optimal untuk user baru yang belum memiliki riwayat rating.

---

## Evaluation

Evaluasi dilakukan berdasarkan karakteristik masing-masing pendekatan.

### Evaluasi Content-Based Filtering

Content-Based Filtering dievaluasi menggunakan **Precision@K** sederhana. Evaluasi ini melihat apakah rekomendasi yang diberikan memiliki genre yang relevan dengan anime input.

Contoh hasil evaluasi:

| Metrik      |                         Nilai |
| ----------- | ----------------------------: |
| Precision@5 | Mengikuti hasil pada notebook |

Semakin tinggi nilai Precision@K, maka semakin banyak anime rekomendasi yang memiliki kemiripan genre dengan anime input.

### Evaluasi Collaborative Filtering

Collaborative Filtering dievaluasi menggunakan **MAE** dan **RMSE**.

* **MAE (Mean Absolute Error)** mengukur rata-rata selisih absolut antara rating asli dan rating prediksi.
* **RMSE (Root Mean Squared Error)** mengukur akar rata-rata kuadrat error antara rating asli dan rating prediksi.

Contoh hasil evaluasi:

| Metrik |                         Nilai |
| ------ | ----------------------------: |
| MAE    | Mengikuti hasil pada notebook |
| RMSE   | Mengikuti hasil pada notebook |

Semakin kecil nilai MAE dan RMSE, maka semakin baik kemampuan model dalam memprediksi rating pengguna.

---

## Deployment

Deployment dilakukan menggunakan **Streamlit** melalui file `app.py`.

Aplikasi memiliki dua menu utama:

1. **Content-Based Filtering**
   Pengguna memilih judul anime, kemudian sistem menampilkan anime yang mirip berdasarkan judul, genre, dan tipe.

2. **Collaborative Filtering**
   Pengguna memilih User ID, kemudian sistem menampilkan rekomendasi anime berdasarkan pola rating pengguna lain yang mirip.

File pendukung deployment:

* `app.py`
* `requirements.txt`
* `data_sample/anime_sample.csv`
* `data_sample/rating_sample.csv`

Cara menjalankan aplikasi:

```bash
python -m streamlit run app.py
```

---

## Struktur Repository

```text
Sistem-Rekomendasi-Anime/
│
├── README.md
├── Rekomendasi_Anime_Alvey_Adriana.ipynb
├── app.py
├── requirements.txt
├── .gitignore
│
├── data_sample/
│   ├── anime_sample.csv
│   └── rating_sample.csv
│
└── buat_sample_data.py
```

Folder `data/` berisi dataset asli dan tidak diunggah ke repository karena ukuran file terlalu besar. Dataset yang digunakan untuk deployment disimpan pada folder `data_sample/`.

---

## Kesimpulan

Berdasarkan hasil proyek, sistem rekomendasi anime berhasil dibangun menggunakan dua pendekatan, yaitu Content-Based Filtering dan Collaborative Filtering.

**Content-Based Filtering** cocok digunakan untuk memberikan rekomendasi berdasarkan kemiripan fitur anime seperti genre, judul, dan tipe. Pendekatan ini tidak membutuhkan data rating pengguna yang banyak, tetapi rekomendasinya terbatas pada kemiripan konten.

**Collaborative Filtering** mampu memberikan rekomendasi yang lebih personal karena memanfaatkan pola rating dari pengguna lain. Namun, pendekatan ini membutuhkan data interaksi pengguna yang cukup agar hasil rekomendasi lebih baik.

Secara keseluruhan, kedua pendekatan memiliki kelebihan masing-masing. Pengembangan selanjutnya dapat dilakukan dengan menggabungkan keduanya menjadi **Hybrid Recommender System** agar rekomendasi menjadi lebih akurat dan relevan.
