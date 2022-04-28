from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(50))
    rating = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    movie_id = db.Column(db.Integer)

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


