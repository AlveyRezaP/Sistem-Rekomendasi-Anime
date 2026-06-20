import streamlit as st
import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


st.set_page_config(
    page_title="Sistem Rekomendasi Anime",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 Sistem Rekomendasi Anime")
st.write("Aplikasi rekomendasi anime menggunakan Content-Based Filtering dan Collaborative Filtering.")


@st.cache_data
def load_data():
    anime = pd.read_csv("data_sample/anime_sample.csv")
    rating = pd.read_csv("data_sample/rating_sample.csv")

    anime["genre"] = anime["genre"].fillna("")
    anime["type"] = anime["type"].fillna("")
    anime["name"] = anime["name"].fillna("Unknown")

    return anime, rating


anime, rating = load_data()


# =========================
# Content-Based Filtering
# =========================
def content_based_recommendation(anime_title, top_n=5):
    anime_cb = anime.copy()
    anime_cb["combined_features"] = (
        anime_cb["name"].astype(str) + " " +
        anime_cb["genre"].astype(str) + " " +
        anime_cb["type"].astype(str)
    )

    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(anime_cb["combined_features"])

    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    indices = pd.Series(anime_cb.index, index=anime_cb["name"]).drop_duplicates()

    if anime_title not in indices:
        return pd.DataFrame()

    idx = indices[anime_title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:top_n + 1]

    anime_indices = [i[0] for i in sim_scores]

    result = anime_cb.iloc[anime_indices][["name", "genre", "type", "rating", "members"]]
    result = result.rename(columns={
        "name": "Judul Anime",
        "genre": "Genre",
        "type": "Tipe",
        "rating": "Rating Rata-rata",
        "members": "Members"
    })

    return result


# =========================
# Collaborative Filtering
# =========================
def collaborative_recommendation(user_id, top_n=5):
    rating_cf = rating.copy()

    user_item_matrix = rating_cf.pivot_table(
        index="user_id",
        columns="anime_id",
        values="rating"
    ).fillna(0)

    if user_id not in user_item_matrix.index:
        popular = anime.sort_values("members", ascending=False).head(top_n)
        return popular[["name", "genre", "type", "rating", "members"]].rename(columns={
            "name": "Judul Anime",
            "genre": "Genre",
            "type": "Tipe",
            "rating": "Rating Rata-rata",
            "members": "Members"
        })

    user_similarity = cosine_similarity(user_item_matrix)
    user_similarity_df = pd.DataFrame(
        user_similarity,
        index=user_item_matrix.index,
        columns=user_item_matrix.index
    )

    similar_users = (
        user_similarity_df[user_id]
        .drop(index=user_id)
        .sort_values(ascending=False)
        .head(5)
    )

    similar_user_ratings = user_item_matrix.loc[similar_users.index]
    weighted_scores = np.dot(similar_users.values, similar_user_ratings)

    if similar_users.sum() != 0:
        weighted_scores = weighted_scores / similar_users.sum()

    recommendation_scores = pd.Series(
        weighted_scores,
        index=user_item_matrix.columns
    )

    watched_anime = user_item_matrix.loc[user_id]
    recommendation_scores = recommendation_scores[watched_anime == 0]

    top_anime_ids = recommendation_scores.sort_values(ascending=False).head(top_n).index

    result = anime[anime["anime_id"].isin(top_anime_ids)]
    result = result[["name", "genre", "type", "rating", "members"]]
    result = result.rename(columns={
        "name": "Judul Anime",
        "genre": "Genre",
        "type": "Tipe",
        "rating": "Rating Rata-rata",
        "members": "Members"
    })

    return result


st.sidebar.header("Menu Rekomendasi")
menu = st.sidebar.radio(
    "Pilih metode rekomendasi:",
    ["Content-Based Filtering", "Collaborative Filtering"]
)


if menu == "Content-Based Filtering":
    st.header("📌 Content-Based Filtering")
    st.write("Metode ini merekomendasikan anime berdasarkan kemiripan judul, genre, dan tipe anime.")

    anime_list = sorted(anime["name"].dropna().unique())
    selected_anime = st.selectbox("Pilih anime:", anime_list)

    top_n = st.slider("Jumlah rekomendasi:", 3, 10, 5)

    if st.button("Tampilkan Rekomendasi Content-Based"):
        result = content_based_recommendation(selected_anime, top_n)

        if result.empty:
            st.warning("Anime tidak ditemukan.")
        else:
            st.success(f"Rekomendasi anime yang mirip dengan: {selected_anime}")
            st.dataframe(result, use_container_width=True)


else:
    st.header("👥 Collaborative Filtering")
    st.write("Metode ini merekomendasikan anime berdasarkan pola rating dari pengguna lain yang memiliki kemiripan.")

    user_ids = sorted(rating["user_id"].unique())
    selected_user = st.selectbox("Pilih User ID:", user_ids)

    top_n = st.slider("Jumlah rekomendasi:", 3, 10, 5)

    if st.button("Tampilkan Rekomendasi Collaborative"):
        result = collaborative_recommendation(selected_user, top_n)

        if result.empty:
            st.warning("Rekomendasi tidak ditemukan.")
        else:
            st.success(f"Rekomendasi anime untuk User ID: {selected_user}")
            st.dataframe(result, use_container_width=True)


st.divider()

st.subheader("📊 Informasi Dataset")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Jumlah Anime", anime.shape[0])

with col2:
    st.metric("Jumlah Rating", rating.shape[0])

with col3:
    st.metric("Jumlah User", rating["user_id"].nunique())