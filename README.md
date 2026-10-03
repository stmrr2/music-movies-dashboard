# Music Movies Dashboard

音楽映画データを可視化するPythonダッシュボードです。  
PythonとStreamlitを用い、公開年やジャンルによる絞り込み、評価推移、人気作品、言語別の作品数などを確認できます。

## 主な機能

- 公開年の範囲指定
- 映画タイトルの部分検索
- ジャンルによる絞り込み
- 年ごとの平均評価の推移表示
- 人気作品Top 10の可視化
- 言語別の作品数集計
- データから簡単なインサイトを自動表示

## 使用技術

- Python
- pandas
- Streamlit
- Plotly
- TMDB API

## ファイル構成

```text
.
├── app.py             # Streamlitダッシュボード
├── fetch_data.py      # TMDB APIからデータを取得
├── music_movies.csv   # ダッシュボード表示用データ
├── requirements.txt
├── .gitignore
└── README.md

## 公開アプリ

[Streamlitでアプリを見る](https://stmrr2-music-movies-dashboard-app-hjio7m.streamlit.app/)
