import streamlit as st
from pathlib import Path
import shutil
import pickle
from utils import pickle_load, fetch_poster_path

STREAMLIT_STATIC_PATH = Path(st.__path__[0]) / 'static'
CSS_PATH = (STREAMLIT_STATIC_PATH / "assests/css")

if not CSS_PATH.is_dir():
    CSS_PATH.mkdir(parents=True, exist_ok=True)

css_file = CSS_PATH / "custom_styles.css"
if not css_file.exists():
    shutil.copy("assets/css/custom_styles.css", css_file)

st.markdown('<link rel="stylesheet" href="assets/css/custom_style.css" type="text/css"/>', unsafe_allow_html=True)

similarity = pickle_load(5)
movies = pickle.load(open('./archive/movies_voted.pkl', 'rb'))

st.set_page_config(layout="wide", page_title="Whatcha Watchin", page_icon="🎥")

st.title('🎥 Whatcha Watchin? 🎥')
st.subheader("Discover movie recommendations tailored to your taste!")

def recommend(movie):
    try:
        movie_idx = movies[movies['title'] == movie].index[0]
        sim_score = similarity[movie_idx]
        recommended_movies_idx = sorted(list(enumerate(sim_score)), reverse=True, key=lambda x: x[1])[1:6]

        recommended_movies_names = []
        recommended_movies_posters = []

        for i in recommended_movies_idx:
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movies_names.append(movies.iloc[i[0]].title)
            recommended_movies_posters.append(fetch_poster_path(movie_id))
        return recommended_movies_names, recommended_movies_posters

    except IndexError:
        return [], []

input_movies = st.multiselect("🎬 Select up to 5 movies you like", movies['title'].values, max_selections=5)

if st.button('🎥 Suggest Recommendations 🎥'):
    combined_results = {}

    for movie in input_movies:
        names, posters = recommend(movie)
        for name, poster in zip(names, posters):
            if name not in combined_results:
                combined_results[name] = poster

    if combined_results:
        sorted_recommendations = [
            (name, combined_results[name], movies.loc[movies['title'] == name, 'vote_average'].values[0])
            for name in combined_results if not movies.loc[movies['title'] == name].empty
        ]
        sorted_recommendations = sorted(sorted_recommendations, key=lambda x: x[2], reverse=True)[:10]

        st.write("## Recommended Movies:")
        cols = st.columns(5)
        for idx, (name, poster, vote_average) in enumerate(sorted_recommendations):
            with cols[idx % 5]:
                st.markdown(f"<div class='container'><div class='recommendation-title'>{name}</div><div class='rating'>⭐ {vote_average}/10</div>", unsafe_allow_html=True)
                if poster:
                    st.image(poster, use_column_width='always', caption=name)
