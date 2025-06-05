from flask import Flask, render_template, request, jsonify
import pickle
import random

app = Flask(__name__)

movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_titles = movies['title'].values

def recommend(movie):
    if movie not in movie_titles:
        return random.sample(list(movie_titles), 5)
    index = movies[movies['title'] == movie].index[0]
    distances = list(enumerate(similarity[index]))
    distances = sorted(distances, key=lambda x: x[1], reverse=True)
    recommended = []
    for i in distances[1:6]:
        recommended.append(movies.iloc[i[0]].title)
    return recommended

@app.route('/')
def index():
    return render_template('index.html', movies=movie_titles)

@app.route('/recommend', methods=['POST'])
def get_recommendations():
    movie = request.json.get('movie')
    recommendations = recommend(movie)
    return jsonify(recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)
