import os
import time

import pandas as pd
import requests

# Set your TMDB API Read Access Token in the environment variable below.
# Never hard-code or commit API tokens to GitHub.
TOKEN = os.getenv("TMDB_BEARER_TOKEN")
if not TOKEN:
    raise RuntimeError("TMDB_BEARER_TOKEN is not set.")

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {TOKEN}",
}

genre_url = "https://api.themoviedb.org/3/genre/movie/list"
response = requests.get(genre_url, headers=headers, timeout=30)
response.raise_for_status()
genre_map = {g["id"]: g["name"] for g in response.json()["genres"]}

all_results = []
discover_url = "https://api.themoviedb.org/3/discover/movie"
params = {
    "language": "en-US",
    "page": 1,
    "with_genres": 10402,
    "sort_by": "popularity.desc",
    "vote_count.gte": 200,
}

response = requests.get(discover_url, headers=headers, params=params, timeout=30)
response.raise_for_status()
data = response.json()
all_results.extend(data["results"])
total_pages = min(data["total_pages"], 5)

for page in range(2, total_pages + 1):
    params["page"] = page
    response = requests.get(discover_url, headers=headers, params=params, timeout=30)
    response.raise_for_status()
    all_results.extend(response.json()["results"])
    time.sleep(0.1)

df = pd.DataFrame(all_results)
df.drop_duplicates(subset=["id"], inplace=True)
df.dropna(subset=["id", "popularity"], inplace=True)
df["vote_average"] = df["vote_average"].astype(float)
df["genres"] = df["genre_ids"].apply(
    lambda ids: ", ".join([genre_map.get(i, str(i)) for i in ids])
    if isinstance(ids, list)
    else ""
)

df.to_csv("music_movies.csv", index=False)
print("music_movies.csv saved successfully")
