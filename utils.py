import pickle
import numpy as np
import streamlit as st
import requests

access_key = st.secrets["TMDB_KEY"]


def pickle_split(array, num_parts):
    # calculate the size of each part
    part_size = len(array) // num_parts
    remainder = len(array) % num_parts
    
    # track the start index for slicing
    start_index = 0
    
    for i in range(num_parts):
        # calculate the end index for this part
        # save the part to a pickle file
        end_index = start_index + part_size + (1 if i < remainder else 0)  # Distribute the remainder elements
        part = array[start_index:end_index]
        
        with open(f"./archive/part{i+1}.pkl", "wb") as file:
            pickle.dump(part, file)
        
        # update the start index for the next part
        start_index = end_index

def pickle_load(num_parts):
    # load each pickle file and combine the data
    # concatenate all parts back together

    parts = []
    for i in range(num_parts):
        with open(f"./archive/part{i+1}.pkl", "rb") as file:
            part = pickle.load(file)
            parts.append(part)
    
    combined_array = np.concatenate(parts, axis=0)
    return combined_array

def fetch_poster_path(movie_id):
    
    tmdb_url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {access_key}"
    }

    response = requests.get(tmdb_url, headers= headers)
    data = response.json()
    poster_path = data.get('poster_path')

    if poster_path:
        return "https://image.tmdb.org/t/p/original" + poster_path
    else:
        return None