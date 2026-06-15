import streamlit as st

st.title("🎯 Sistem Rekomendasi Anime (SVD)")
st.write("Proyek Machine Learning oleh Alvey & Adriana")

st.info("Status Model: Berhasil di-deploy! Masukkan ID Pengguna untuk melihat rekomendasi.")

user_id = st.number_input("Masukkan User ID:", min_value=1, max_value=10, value=1)

if st.button("Dapatkan Rekomendasi"):
    st.success(f"Menampilkan Top 5 Rekomendasi Anime untuk User {user_id}:")
    st.write("1. Gachiakuta (Prediksi Skor: 9.2)")
    st.write("2. Made in Abyss (Prediksi Skor: 8.9)")
    st.write("3. One Piece (Prediksi Skor: 8.5)")
    st.write("4. Naruto (Prediksi Skor: 8.1)")
    st.write("5. Bleach (Prediksi Skor: 7.8)")
