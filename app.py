import  pickle
import streamlit as st
import pandas as pd
import requests
movies_dict=pickle.load(open('movie_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)

st.title('Movie Recommender System')
import streamlit as st

similarity=pickle.load(open('similarity.pkl','rb'))

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=389b5cf8ad9e92f162ae245e38e3154a&language=en-US'.format(movie_id))
    data = response.json()

    if "poster_path" in data:
        return "https://image.tmdb.org/t/p/w500/" + data["poster_path"]
    else:
        return "Poster not available"


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]
    movie_list=(sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1]))[1:6]
    recommended_movies=[]
    recommended_movie_posters=[]
    #fetch poster from api

    for i in movie_list:
        movie_id=i[0]
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movies.iloc[i[0]].movie_id))
    return recommended_movies,recommended_movie_posters

selected_movie_name= st.selectbox(
    'Pick a Movie You Like.....',
    movies['title'].values)

if st.button('Recommend'):
    names,posters= recommend(selected_movie_name)
    import streamlit as st

    col1, col2, col3 , col4 , col5= st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])

st.button("Reset", type="primary")
