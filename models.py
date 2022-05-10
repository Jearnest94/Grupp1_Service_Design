import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.String)
    endpoint = db.Column(db.String)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)
    reviews = db.relationship('Review', back_populates='user')
    latesttoken = db.Column(db.String(150))


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(50))
    rating = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.movie_id'))
    movie = db.relationship('Movie', back_populates='reviews')
    user = db.relationship('User', back_populates='reviews')


class Movie(db.Model):
    movie_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Poster_Link = db.Column(db.Text)
    Series_Title = db.Column(db.Text)
    Released_Year = db.Column(db.Integer)
    Certificate = db.Column(db.Text)
    Runtime = db.Column(db.Text)
    Genre = db.Column(db.Text)
    IMDB_Rating = db.Column(db.REAL)
    Overview = db.Column(db.Text)
    Meta_score = db.Column(db.Integer)
    Director = db.Column(db.Text)
    Star1 = db.Column(db.Text)
    Star2 = db.Column(db.Text)
    Star3 = db.Column(db.Text)
    Star4 = db.Column(db.Text)
    No_of_Votes = db.Column(db.Integer)
    Gross = db.Column(db.Text)
    reviews = db.relationship('Review', back_populates='movie')

    def update(self, other_movie):
        self.Series_Title = other_movie.Series_Title
        self.Released_Year = other_movie.Released_Year
        self.Runtime = other_movie.Runtime
        self.Genre = other_movie.Genre
        self.IMDB_Rating = other_movie.IMDB_Rating
        self.Overview = other_movie.Overview
        self.Director = other_movie.Director
        self.Star1 = other_movie.Star1
