import pandas as pd
import streamlit as st
st.title('Movie Recommender System')
import pickle
# file = open("movies.pkl", 'rb')
# df = pickle.load(file)
# titles = df['title'].values
# movies_list = st.selectbox('Select Movie', titles)

import requests
import os
#$env:TMDB_API_KEY="your_api" in terminal
API_KEY = os.getenv("TMDB_API_KEY")
#st.write("API Key loaded:", API_KEY is not None) ,tells if api loaded successfully
#Above is done to secure api

# import sys
# st.write("Python:", sys.executable)
# st.write("API_KEY:", API_KEY)

def fetch_url_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
        response = requests.get(url, timeout=10)
        #st.write(response.status_code)
        data = response.json()
        #st.write(data)
        #st.write("https://image.tmdb.org/t/p/w500" + data["poster_path"]), to know if it really fetches or not
        return "https://image.tmdb.org/t/p/w500" + data["poster_path"]

    except Exception:
        #used to return null if the poster isn't available
        return "no_poster.png"

#Function to fetch Recommended Movies using movie df and similarity matrix
def recommend(mov_input):
    mov_index = movies[movies['title'] == mov_input].index[0]
    simi_row = simi[mov_index]
    mov_list = sorted(list(enumerate(simi_row)), key = lambda x : x[1], reverse = True)[1:6]

    recommended = [] #To store recommended movie titles
    poster_url = [] #To store posters of the recommended movies
    for tup in mov_list:
        MovId = fetch_url_poster(movies.iloc[tup[0]]['id'])
        #fetch 'movie id' from movie df using index, and referenced it to find fetch poster
        poster_url.append(MovId)

        recommended.append(movies.iloc[tup[0]]['title'])

    return poster_url, recommended

#Importing Movies dataframe(new_df)
file = open("movies_dict.pkl", 'rb')
Movies_dict = pickle.load(file)
movies = pd.DataFrame(Movies_dict)
titles = movies['title'].values

movie = st.selectbox('Discover the Top 5 similar movies based on your selection! 🔥',
                     titles,
                     index=None,
                     placeholder="Choose a movie...")

#Importing Similarity Matrix
fileSimi = open("simi_list2.pkl", 'rb')
simi_list = pickle.load(fileSimi)

import numpy as np
simi = np.array(simi_list)


if st.button('🎬 Get Recommendations!'):
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