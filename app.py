from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_cors import CORS 
import os 

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sqlite")

CORS(app)
db = SQLAlchemy(app)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False, unique=True)
    genre = db.Column(db.String(), nullable=False)
    rating = db.Column(db.Integer)

    def __init__(self, title, genre, rating):
        self.title = title
        self.genre = genre
        self.rating = rating

@app.route("/movies/post", methods=["POST"])
def create_movie():
    post_data = request.get_json()
    title = post_data.get("title")
    genre = post_data.get("genre")
    rating = post_data.get("rating")

    record = Movie(title, genre, rating)
    db.session.add(record)
    db.session.commit()

    return jsonify("Data Posted")

@app.route("/movies/get", methods=["GET"])
def get_all_movies():
    if request.content_type != "application/json":
        return jsonify("Error: Please use header content_type: application/json")
    all_movies = db.session.query(Movie.id, Movie.title, Movie.genre, Movie.rating).all()
    return jsonify(all_movies)


if __name__ == "__main__":
    app.debug = True
    app.run()