import asyncio
import os
import pickle
import aiohttp
import numpy as np
import pandas as pd
import streamlit as st


st.title("Movie Recommender System")

#For Secure API Key fetching
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")

@st.cache_resource
def load_data():
    with open("movies.pkl", "rb") as file:
        movies = pickle.load(file)

    with open("similarity.pkl", "rb") as file:
        simi = pickle.load(file)

    return movies, simi

movies, simi = load_data()
titles = movies["title"].values

async def fetch_poster(session, movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"

    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
            if response.status != 200:
                return "no_poster.png"

            data = await response.json()
            poster_path = data.get("poster_path")
            if poster_path is None:
                return "no_poster.png"
            return f"https://image.tmdb.org/t/p/w500{poster_path}"

    except Exception:
        return "no_poster.png"

async def fetch_posters(movie_ids):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_poster(session, movie_id) for movie_id in movie_ids]
        return await asyncio.gather(*tasks)

def recommend(movie_input):
    movie_index = movies[movies["title"] == movie_input].index[0]
    similarity_row = simi[movie_index]
    movie_list = sorted(list(enumerate(similarity_row)),
                        key=lambda x: x[1],
                        reverse=True)[1:6]

    recommended_movies = [movies.iloc[tup[0]]["title"] for tup in movie_list]

    movie_ids = [movies.iloc[tup[0]]["id"] for tup in movie_list]
    poster_urls = asyncio.run(fetch_posters(movie_ids))

    return poster_urls, recommended_movies


movie = st.selectbox(
    "Discover the Top 5 similar movies based on your selection! 🔥",
    titles,
    index=None,
    placeholder="Choose a movie..."
)

if st.button("🎬 Get Recommendations!"):
    if movie is None:
        st.warning("Please select a movie first!")

    else:
        poster, recommended_movies = recommend(movie)

        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.image(poster[0])
            st.text(recommended_movies[0])

        with col2:
            st.image(poster[1])
            st.text(recommended_movies[1])

        with col3:
            st.image(poster[2])
            st.text(recommended_movies[2])

        with col4:
            st.image(poster[3])
            st.text(recommended_movies[3])

        with col5:
            st.image(poster[4])
            st.text(recommended_movies[4])

# Versions at time of pickling
# numpy : 2.1.3
# pandas : 2.2.3
# sklearn : 1.6.1