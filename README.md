# Music Movies Dashboard

ニュージーランド短期留学中のITワークショップで制作した、音楽映画データを可視化するPythonダッシュボードです。就職活動で成果物として閲覧できるよう、公開用にファイル構成とREADMEを整理しています。

## 概要

TMDB (The Movie Database) の映画データをもとに、音楽映画を対象としてデータを絞り込み・可視化します。Streamlit上で、公開年・タイトル・ジャンルによる検索や、評価推移、人気作品、言語別作品数を確認できます。

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
├── fetch_data.py      # TMDB APIからデータを取得（任意）
├── music_movies.csv   # ダッシュボード表示用データ
├── requirements.txt
├── .gitignore
└── README.md
```

## 実行方法

```bash
pip install -r requirements.txt
streamlit run app.py
```

`music_movies.csv` を再取得する場合は、TMDB API Read Access Tokenを環境変数 `TMDB_BEARER_TOKEN` に設定してから実行します。APIトークンはGitHubに公開しないでください。

```bash
python fetch_data.py
```

## 制作時に取り組んだこと

ワークショップではPythonを用いて映画データを扱い、データの取得・整理・集計・可視化を行いました。ダッシュボードでは、利用者が条件を変えながら結果を確認できるよう、複数のフィルターとタブを用意しました。

## Data source / Attribution

Data source: TMDB (The Movie Database).

This product uses the TMDB API but is not endorsed or certified by TMDB.

公開アプリとして利用する場合は、TMDB公式の最新の利用規約・Attribution要件を確認し、承認済みTMDBロゴをCredits/About相当の箇所に追加してください。
