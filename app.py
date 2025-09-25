from flask import Flask, render_template, request, jsonify
import pickle

app = Flask(__name__)

movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movie_titles = movies['title'].values


def recommend(movie_title):
    """Finds the top 5 most similar movies, ignoring case."""
    try:
        search_title = movie_title.strip().lower()
        movie_index = movies[movies['title'].str.lower() == search_title].index[0]
        distances = similarity[movie_index]
        recommended_movies_indices = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        recommended = [movies.iloc[i[0]].title for i in recommended_movies_indices]
        return recommended
    except:
        return []


@app.route('/')
def index():
    return render_template('index.html', movies=movie_titles)

@app.route('/recommend', methods=['POST'])
def get_recommendations_api():
    data = request.get_json()
    movie = data.get('movie')
    recommendations = recommend(movie)
    return jsonify({'recommendations': recommendations})

if __name__ == '__main__':
    app.run(debug=True)