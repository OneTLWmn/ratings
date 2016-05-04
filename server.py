"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, flash, session, request
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Movie, Rating




app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route('/users')
def user_list():
    """Show list of users"""

    users = User.query.all()
    return render_template('user_list.html', users=users)

@app.route('/login_form', methods=['GET', 'POST'])
def login():
    """Users login template"""

    return render_template('user_login_form.html')


@app.route('/process_login', methods=['GET', 'POST'])
def process_login():
    #args returned as dictionary from the form
    #pulling each and binding to variables for query to db
    email = request.form["user-email"]
    password = request.form["user-password"]
    
    #Debugging prints
    # print (type(request.form))
    # print("Email: ", email) 
    # print("Password: ", password)
    
    # query the db-ratings for existence of the user
    
    user = User.query.filter_by(email = email).all()

    
        # print
    return render_template("homepage.html")



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
