import pandas as pd
import os

# Membaca dataset asli
anime = pd.read_csv("data/anime.csv")
rating = pd.read_csv("data/rating.csv")

# Menghapus rating -1 karena artinya user menonton tapi tidak memberi rating
rating = rating[rating["rating"] != -1]

# Ambil anime yang punya jumlah member tinggi agar data lebih relevan
anime_sample = anime.sort_values("members", ascending=False).head(300)

# Ambil rating yang hanya berkaitan dengan anime_sample
rating_sample = rating[rating["anime_id"].isin(anime_sample["anime_id"])]

# Batasi jumlah user agar file tidak terlalu besar
selected_users = rating_sample["user_id"].value_counts().head(500).index
rating_sample = rating_sample[rating_sample["user_id"].isin(selected_users)]

# Simpan hasil sample
os.makedirs("data_sample", exist_ok=True)

anime_sample.to_csv("data_sample/anime_sample.csv", index=False)
rating_sample.to_csv("data_sample/rating_sample.csv", index=False)

print("Sample data berhasil dibuat.")
print("Anime sample:", anime_sample.shape)
print("Rating sample:", rating_sample.shape)