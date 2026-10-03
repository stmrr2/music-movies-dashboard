import streamlit as st #Streamlitを使うための準備。stという名前で使えるようにしている
import pandas as pd
import plotly.express as px

# データ読み込み
@st.cache_data #データを保存し毎回読み直さないようにする
def load_data():
    df = pd.read_csv("music_movies.csv") #CSVファイルを読み込んでDataFrameにする(Read a CSV file and create a DataFrame)
    df.drop_duplicates(subset="id", inplace=True)
    df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
    df["vote_average"] = pd.to_numeric(df["vote_average"], errors="coerce") #評価を数値型に変換(Converting ratings to numeric types)
    df["vote_count"] = pd.to_numeric(df["vote_count"], errors="coerce")
    df["popularity"] = pd.to_numeric(df["popularity"], errors="coerce")
    df["year"] = df["release_date"].dt.year #公開日から「年」だけを取り出す(Extract only the "year" from the publication date)
    return df

df = load_data()
# genres をリスト化
df["genre_list"] = df["genres"].fillna("").apply(lambda x: [g.strip() for g in x.split(",")])


st.title("🎵 Music Movies Dashboard")

# サイドバーフィルター
st.sidebar.header("Filters")
year_min, year_max = int(df["year"].min()), int(df["year"].max())

start_year = st.sidebar.number_input( #開始年を入力できるボックス(A box where you can enter the start year)
    "Start Year",
    min_value=year_min,
    max_value=year_max,
    value=year_min,
    step=1
)

end_year = st.sidebar.number_input(
    "End Year",
    min_value=year_min,
    max_value=year_max,
    value=year_max,
    step=1
)

search_title = st.sidebar.text_input("Search Title (partial)")

# 全ジャンル一覧を取得(Get list of all genres)
all_genres = sorted({g for sublist in df["genre_list"] for g in sublist if g})

selected_genres = st.sidebar.multiselect( #複数ジャンルを選択できるボックス(A box where you can select multiple genres)
    "Select Genre (within Music)",
    options=all_genres
)

# フィルタ適用（年 + タイトル検索）(Apply filter)
filtered_df = df[ #指定した年の範囲に絞る(Narrow to a specified year range)
    (df["year"] >= start_year) &
    (df["year"] <= end_year)
]
if start_year > end_year: #年が逆ならエラー表示(If the year is reversed, an error message will be displayed.)
    st.sidebar.error("Start Year must be less than or equal to End Year")


if search_title: #タイトルに入力文字が含まれる映画だけ残す(Keep only movies whose titles contain the entered characters)
    filtered_df = filtered_df[filtered_df["title"].str.contains(search_title, case=False, na=False)]

if selected_genres: #選んだジャンルが1つでも含まれている映画だけ残す(Keep only movies that contain at least one of the selected genres)
    filtered_df = filtered_df[
        filtered_df["genre_list"].apply(
            lambda genres: any(g in genres for g in selected_genres)
        )
    ]


# タブ構成
tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Trends", "Top Lists", "By Language"]) #4つのタブを作る

# Overviewタブ
with tab1:
    st.subheader("Movie Data")
    st.dataframe(filtered_df[["title", "year", "genres", "vote_average", "vote_count", "popularity"]]) #データを表で表示

# Trends
with tab2:
    if not filtered_df.empty:

        # 年ごとの平均評価
        trend_df = filtered_df.groupby("year").agg(
            avg_rating=("vote_average", "mean")
        ).reset_index()

        # 前年との差分
        trend_df["diff"] = trend_df["avg_rating"].diff()

        # NaNを除く（最初の年はdiffがNaN）
        trend_df_clean = trend_df.dropna()

        st.markdown("### Average Rating Trend by Year")

        # グラフ
        fig_rating = px.line(
            trend_df,
            x="year",
            y="avg_rating",
        )
        st.plotly_chart(fig_rating, use_container_width=True)

        # グラフ下にインサイト
        if not trend_df_clean.empty:

            max_increase_row = trend_df_clean.loc[trend_df_clean["diff"].idxmax()] #一番大きい値の行を取得(Get the row with the largest value)
            max_decrease_row = trend_df_clean.loc[trend_df_clean["diff"].idxmin()]

            st.markdown("### Trend Insights")
            st.write(
                f"⤴  The year with the largest increase in average rating was "
                f"**{int(max_increase_row['year'])}**, "
                f"with an increase of +{max_increase_row['diff']:.2f} compared to the previous year."
            )
            st.write(
                f"⤵  The year with the largest decrease in average rating was "
                f"**{int(max_decrease_row['year'])}**, "
                f"with a decrease of {max_decrease_row['diff']:.2f} compared to the previous year."
            )

    else:
        st.info("No data to show trends.")


# Top Lists
with tab3:
    if not filtered_df.empty:
        top_popular = filtered_df.sort_values("popularity", ascending=False).head(10) #人気順に並べて上位10件取得

        st.markdown("### Top 10 Most Popular")
        fig_top_pop = px.bar( #横棒グラフを作成
            top_popular,
            x="popularity",
            y="title",
            orientation="h",
            # y軸を人気順に設定（最大人気が上）
            category_orders={"title": top_popular["title"].tolist()}  # 逆順にしない
        )
        st.plotly_chart(fig_top_pop, use_container_width=True)

        # インサイト
        st.markdown("### Insights")
        most_popular = top_popular.iloc[0]  # 最大人気は先頭行
        avg_rating_top10 = top_popular["vote_average"].mean()
        st.write(
            f"🏆 The most popular movie is **{most_popular['title']}** "
            f"with a popularity score of {most_popular['popularity']:.2f}."
        )
        st.write(
            f"⭐ The average rating of the top 10 most popular movies is {avg_rating_top10:.2f}."
        )
    else:
        st.info("No data to show top lists.")


# By Language
with tab4:
    if not filtered_df.empty:
        lang_count = filtered_df["original_language"].value_counts().reset_index() #言語ごとの本数を数える
        lang_count.columns = ["language", "movie_count"]

        st.markdown("### Movie Count by Language")
        fig_lang_count = px.bar(lang_count, x="language", y="movie_count")
        st.plotly_chart(fig_lang_count, use_container_width=True)

        # インサイト
        st.markdown("### Insights")
        top_lang = lang_count.iloc[0]
        total_movies = lang_count["movie_count"].sum()
        share = (top_lang["movie_count"] / total_movies) * 100
        st.write(
            f"🌐 The language with the most movies is **{top_lang['language']}**, "
            f"with {top_lang['movie_count']} movies ({share:.1f}% of total)."
        )

    else:
        st.info("No data to show by language.")

st.divider()

st.subheader("Credits")

st.image("tmdb_logo.svg", width=180)

st.write("Data source: TMDB (The Movie Database).")

st.caption(
    "This product uses the TMDB API but is not endorsed or certified by TMDB."
)
