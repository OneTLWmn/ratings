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


@app.route('/process_login', methods=['GET', 'POST'])
def login():
    """Users login template"""

    email = request.form["user-email"]
    password = request.form["user-password"]
    print "\n\n\n\n &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"
    print ("password: ", password)
    print ("email: ", email)
    print "\n\n\n\n &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"  
    #check for value yes/no of response; set true if yes;
    #false if no
    user = User.query.filter_by(email = email).all()
    
    flash('You were successfully logged in')
    
    return render_template("query_page.html")
    
@app.route('/users')
def user_list():
    """Show list of users"""

    users = User.query.all()
    return render_template('user_list.html', users=users)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
