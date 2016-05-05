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



@app.route('/logout')
def logout_user():
    """This will logout the user and redirect them to the homepage
    Removes session variables associated with current_user"""


    session.pop('current_user', None)

    return redirect("/")



@app.route('/users')
def user_list():
    """Show list of users"""

    users = User.query.all()
    return render_template('user_list.html', users=users)


@app.route('/process_login', methods=['GET', 'POST'])
def process_login():
    """
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    zipcode = db.Column(db.String(15), nullable=True)
    """

    #args returned as dictionary from the form
    #pulling each and binding to variables for query to db
    email = request.form["user-email"]
    password = request.form["user-password"]
    
    # query the db-ratings for existence of the user
    # .first() will give us the first record as an object (all the fields in db) 
    # if it exist if not None
    # had we done .all it would have returned an object with all the matched
    # records and you would access each row using index id
    user = User.query.filter_by(email = email).first()
 
    if not user:
        #add the user to the site
        flash('User does not exist yet. You have been registered.')

        #Create the object with attributes of email and password; for now we are leaving 
        #age and zip as null; then add the new user record to the DB and commit it
        
        newUser = User(email=email, password=password)
        db.session.add(newUser)
        db.session.commit()
    else:
        # the user does exist, check if their password matches. 
        # if the password doesn't match, alert user and
        # redirect user back to the log in page.
        if user.password != password:
            flash('Password did not match email.  Please try again.')
            return redirect("/")


    
    # Once new user is created or existing user logs in,
    # create a session for the user
    session["current_user"] = email
    flash(session["current_user"] + ', successfully logged into the system')
    
    return render_template("user_query.html")



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
