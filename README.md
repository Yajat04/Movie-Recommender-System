# This project implements a content-based movie recommendation system using the TMDB 5000 Movies and TMDB 5000 Credits datasets. 
It recommends movies similar to a selected title by analyzing metadata such as genres, keywords, cast, crew, and movie overviews.

## Recommendation Pipeline:
- Cleaned and preprocessed movie metadata.
- Performed feature engineering by combining relevant textual attributes into a unified representation.
- Applied CountVectorizer for text vectorization.
- Computed Cosine Similarity to identify and recommend similar movies.
- Used pickle module to use the data in "app" file

## Features:
- Built an interactive Streamlit web application.
- Integrated the TMDB API to fetch movie posters, ratings, release dates, and other movie details.
- Designed a clean, user-friendly interface with search functionality and visually rich recommendation cards.

## Upcoming Features:
- Deploy the application for public access.
