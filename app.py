from flask import Flask, render_template, request, jsonify
import pickle

app = Flask(__name__)

movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movie_titles = movies['title'].values


def recommend(movie_title):
    """Finds the top 5 most similar movies, ignoring case."""
    try:
        # Convert the input title to lowercase and remove extra spaces
        search_title = movie_title.strip().lower()

        # Find the index by comparing with lowercase titles from the data
        # 'str.lower()' converts all titles in the 'title' column to lowercase for matching
        movie_index = movies[movies['title'].str.lower() == search_title].index[0]

        # --- The rest of the function is the same ---
        distances = similarity[movie_index]
        recommended_movies_indices = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        recommended = [movies.iloc[i[0]].title for i in recommended_movies_indices]
        return recommended
    except:
        # If any error occurs (like the movie not being found), return an empty list.
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