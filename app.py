import pickle
import streamlit as st
from typing import Tuple, List

# Cache the data loading
@st.cache_data
def load_data():
    try:
        movies = pickle.load(open('movies.pkl', 'rb'))
        similarity = pickle.load(open('similarity.pkl', 'rb'))
        return movies, similarity
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return None, None

def recommend(movie: str) -> Tuple[List[str], List[str]]:
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        
        names = []
        for i in distances[1:6]:  # Get top 5 similar movies
            names.append(movies.iloc[i[0]].title)
                
        return names
    except Exception as e:
        st.error(f"Recommendation error: {e}")
        return []

# Main App
st.header('Movie Recommender System')

movies, similarity = load_data()
if movies is not None and similarity is not None:
    movie_list = movies['title'].tolist()
    selected_movie = st.selectbox(
        "Type or select a movie from the dropdown",
        movie_list
    )

    if st.button('Show Recommendation'):
        with st.spinner('Finding similar movies...'):
            recommended_movies = recommend(selected_movie)
        
        if recommended_movies:
            st.subheader("Recommended Movies:")
            for i, movie in enumerate(recommended_movies, 1):
                st.write(f"{i}. {movie}")
        else:
            st.warning("No recommendations found or there was an error.")