from flask import Flask, render_template, request, redirect, abort, url_for, make_response, flash, session
import os
from os import urandom
from bson.json_util import dumps
from bson.objectid import ObjectId
import sys
import datetime
from dotenv import dotenv_values
import certifi
import re
from mongodb import Database

import flask_login
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

Database.initialize()
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = urandom(32)

# set up flask-login for user authentication
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

# try:
#     # verify the connection works by pinging the database
#     # cxn.admin.command('ping') # The ping command is cheap and does not require auth.
#     #db = cxn[config['MONGO_DBNAME']] # store a reference to the database
#     #print(' *', 'Connected to MongoDB!') # if we get here, the connection worked!
# except Exception as e:
#     # the ping command failed, so the connection is not available.
#     # render_template('error.html', error=e) # render the edit template
#     print(' *', "Failed to connect to MongoDB at", config['MONGO_URI'])
#     print('Database connection error:', e) # debug


# a class to represent a user
class User(flask_login.UserMixin):
    # inheriting from the UserMixin class gives this blank class default implementations of the necessary methods that flask-login requires all User objects to have
    # see some discussion of this here: https://stackoverflow.com/questions/63231163/what-is-the-usermixin-in-flask
    def __init__(self, data):
        '''
        Constructor for User objects
        @param data: a dictionary containing the user's data pulled from the database
        '''
        self.id = data['_id'] # shortcut to the _id field
        self.data = data # all user data from the database is stored within the data field

def locate_user(user_id=None, username=None):
    '''
    Return a User object for the user with the given id or username, or None if no such user exists.
    @param user_id: the user_id of the user to locate
    @param username: the username address of the user to locate
    '''
    if user_id:
        # loop up by user_id
        criteria = {"_id": ObjectId(user_id)}
    else:
        # loop up by username
        criteria = {"username": username}
    doc = Database.find_single('user', criteria) # find a user with the given criteria

    # if user exists in the database, create a User object and return it
    if doc:
        # return a user object representing this user
        user = User(doc)
        return user
    # else
    return None

@login_manager.user_loader
def user_loader(user_id):
    '''
    This function is called automatically by flask-login with every request the browser makes to the server.
    If there is an existing session, meaning the user has already logged in, then this function will return the logged-in user's data as a User object.
    @param user_id: the user_id of the user to load
    @return a User object if the user is logged-in, otherwise None
    '''
    return locate_user(user_id=user_id) # return a User object if a user with this user_id exists


# set up any context processors
# context processors allow us to make selected variables or functions available from within all templates

@app.context_processor
def inject_user():
    # make the currently-logged-in user, if any, available to all templates as 'user'
    return dict(user=flask_login.current_user)

@app.route('/')
def login():
    """
    Processes login and redirects accordingly if request was made
    Otherwise display login form
    """

    # if the current user is already signed in, there is no need to sign up, so redirect them
    if flask_login.current_user.is_authenticated:
        flash('You are already logged in, silly!') # flash can be used to pass a special message to the template we are about to render
        return redirect(url_for('home')) # tell the web browser to make a request for the / route (the home function)
    if (request.args):
        if bool(request.args["username"]) and bool(request.args["password"]):
            usernameInput = request.args["username"]
            passwordInput = request.args["password"]
            user = locate_user(username=usernameInput)
            if user:
                    if check_password_hash(user.data['password'], passwordInput):
                        flask_login.login_user(user)
                        return(redirect(url_for("home")))
                    else:
                        flash('Invalid password.')
                        return(redirect(url_for("login")))
            else:
                flash('No user found for username.')
                return(redirect(url_for("login")))
        else:
            flash('Please enter an username and password.')
            return(redirect(url_for("login")))
    else:
        return render_template("login.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Route for the register page
    """
    if request.method == 'GET':
        return render_template("register.html")
    if request.method == 'POST':
        u = request.form['username']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        p = request.form['password']

        if not u or not p or not firstName or not lastName:
            flash('Please fill all fields.')
        elif locate_user(username=u):
            flash('An account was already created with this username.')
        else:
            hashed_password = generate_password_hash(p)
            Database.insert_one('user', {"username": u, 'firstName': firstName, 'lastName': lastName,  "password": hashed_password})
            flash('Success!')
            return redirect(url_for('login'))
    else:
        if flask_login.current_user.is_authenticated:
            flash('You are already logged in, silly!')
            return redirect(url_for('homepage'))
    return render_template("register.html")

@app.route('/home')
@flask_login.login_required
def home():
    return render_template("home.html")

@app.route('/home', methods=["POST"])
@flask_login.login_required
def uploadFile():
    """
    Route for the home page
    """
    # Upload file flask
    uploaded_img = request.files['uploaded-file']
    # Extracting uploaded data file name
    img_filename = secure_filename(uploaded_img.filename)
    # Upload file to database (defined uploaded folder in static path)
    uploaded_img.save(os.path.join(app.config['UPLOAD_FOLDER'], img_filename))
    # Storing uploaded file path in flask session
    session['uploaded_img_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], img_filename)

    # find user data like array of tasks
    #flask_login.current_user.data['todos']

    # pass in today todos and the user's username to the homepage template
    return render_template("home.html")

@app.route('/logout')
@flask_login.login_required
def logout():
    """
    Route to logout
    """
    flask_login.logout_user()
    return(redirect(url_for("login")))

if __name__=='__main__':
    app.run(debug=True)
