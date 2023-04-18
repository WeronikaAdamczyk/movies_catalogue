from flask import Flask, render_template, url_for
import tmdb_client
from tmdb_client import get_popular_movies
from flask import request

app = Flask(__name__)


# @app.route('/')
# def homepage():
#     response = get_popular_movies()
#     movies=response["results"]
#     return render_template("homepage.html", movies=movies)
lists = ["now_playing","popular","upcoming","top_rated"]


@app.context_processor
def utility_processor():
    def tmdb_image_url(path, size):
        return tmdb_client.get_poster_url(path, size)
    return {"tmdb_image_url": tmdb_image_url}


@app.route('/')
def homepage():
    selected_list = request.args.get('list_type', 'popular')
    if not lists.__contains__(selected_list):
        selected_list='popular'
    movies = tmdb_client.get_movies(how_many=8, list_type=selected_list)
    return render_template("homepage.html", movies=movies, current_list=selected_list,lists=lists)




@app.route("/movie/<movie_id>")
def movie_details(movie_id):
   details = tmdb_client.get_single_movie(movie_id)
   cast = tmdb_client.get_single_movie_cast(movie_id)
   return render_template("movie_details.html", movie=details, cast=cast)


if __name__ == '__main__':
    app.run(debug=True)