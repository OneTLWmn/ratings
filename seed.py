"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from sqlalchemy import func
from model import User, Movie
# from model import Rating
# from model import Movie

from model import connect_to_db, db
from server import app
from datetime import datetime

def load_users():
    """Load users from u.user into database."""

    print "Users"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/u.user"):
        row = row.rstrip()
        user_id, age, gender, occupation, zipcode = row.split("|")[0:5]

        user = User(user_id=user_id,
                    age=age,
                    zipcode=zipcode)

        # We need to add to the session or it won't ever be stored
        db.session.add(user)

    # Once we're done, we should commit our work
    db.session.commit()


def load_movies():
    """Load movies from u.item into database."""

    print "Movies"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Movie.query.delete()

    # Read u.item file and insert data into movies table
    # emptyPipe is an variable with an empty value, because we split on 
    # a pipe and there was a double pipe before the imdb url
    for row in open("seed_data/u.item"):
        row = row.rstrip()
        movie_id, title, release_str, emptyPipe, imdb_url = row.split("|")[0:5]
        
        # removing unecessary year from title it's redundant
        title = title.split(" (")[0]
        
        # The date comes as string from file: 01-Jan-1995
        # change it to a datetime object
        if release_str:
            release_at = datetime.strptime(release_str, '%d-%b-%Y')
        else:
            release_at = None

        # Sets up each movie as an instance of the Movie class
        # (which will become a record in our movies table)     
        movie = Movie(movie_id=movie_id,
                    title = title,
                    release_at = release_at,
                    imdb_url = imdb_url)
     # We need to add to the session or it won't ever be stored
        db.session.add(movie)

    # Once we're done, we should commit our work
    db.session.commit()

def load_ratings():
    """Load ratings from u.data into database."""


def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_users()
    load_movies()
    load_ratings()
    set_val_user_id()
