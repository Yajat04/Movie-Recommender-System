#!/usr/bin/env bash

echo "Downloading movies dataframe and similarity matrix..."


wget -O movies.pkl \
https://huggingface.co/datasets/Yajat004/movie-recommender-system/resolve/main/movies.pkl

wget -O similarity.pkl \
https://huggingface.co/datasets/Yajat004/movie-recommender-system/resolve/main/similarity.pkl

