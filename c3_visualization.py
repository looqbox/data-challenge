import pandas as pd
import plotly.express as px
import streamlit as st

from db import load_movies

st.set_page_config(page_title="IMDB dashboard", page_icon="🎬", layout="wide")
st.title("IMDB Movies: Popularity and Rating")


@st.cache_data
def load_data():
    df = load_movies()
    df["Decade"] = (df["Year"] // 10 * 10)
    return df


df = load_data()


k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Films", f"{len(df):,}")
k2.metric("Avg Rating", f"{df['Rating'].mean():.1f}")
k3.metric("Avg Votes", f"{df['Votes'].mean():,.0f}")
k4.metric("Median Votes", f"{df['Votes'].median():,.0f}")

st.divider()


st.subheader("Votes vs Rating")
fig = px.scatter(
    df.dropna(subset=["Votes", "Rating"]),
    x="Votes",
    y="Rating",
    color="Decade",
    color_continuous_scale=["#c8f5d5", "#3FD569", "#1a6b35"],
    hover_data=["Title", "Year", "Director"],
    trendline="ols",
    log_x=True,
    labels={"Votes": "Votes (log scale)", "Rating": "IMDB Rating"},
)
st.plotly_chart(fig, use_container_width=True)

st.caption(
    "Votes on a log scale because the distribution is highly skewed "
    "(a few blockbusters with millions of votes, most films with very few)."
)

st.divider()


c1, c2 = st.columns(2)

with c1:
    st.subheader("Low visibility, high ratings")
    st.caption("Rating ≥ 8 · Votes ≤ 50k")
    gems = (
        df[(df["Rating"] >= 8) & (df["Votes"] <= 50_000)]
        [["Title", "Year", "Director", "Genre", "Rating", "Votes"]]
        .sort_values("Rating", ascending=False)
        .reset_index(drop=True)
    )
    st.dataframe(gems, use_container_width=True)
    st.caption(f"{len(gems)} films found")

with c2:
    st.subheader("High visibility, below-median ratings")
    st.caption("Top 25% by votes · Below median rating")
    vote_q75 = df["Votes"].quantile(0.75)
    median_rating = df["Rating"].median()
    overhyped = (
        df[(df["Votes"] >= vote_q75) & (df["Rating"] < median_rating)]
        [["Title", "Year", "Director", "Rating", "Votes"]]
        .sort_values("Votes", ascending=False)
        .reset_index(drop=True)
    )
    st.dataframe(overhyped, use_container_width=True)
    st.caption(f"{len(overhyped)} films found")