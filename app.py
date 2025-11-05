import streamlit as st
import pickle
import pandas as pd
import requests

# Function to fetch movie poster
def fetch_poster(movie_id):
    # Replace 'YOUR_API_KEY' with your actual TMDb API key
    api_key = "a4a32f16b2531f2405ca69a96685dbad"
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching poster: {e}")
    return "https://via.placeholder.com/500x750.png?text=No+Poster+Found"

# Load the pickle files
movies_dict = pickle.load(open('movies_list_pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity_pkl', 'rb'))

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

st.title('Netflix Movie Recommendation System')

selected_movie_name = st.selectbox(
    'Select a movie to get recommendations',
    movies['title'].values)

if st.button('Recommend'):
    names,posters = recommend(selected_movie_name)
    
    st.write("Recommended Movies:")
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])