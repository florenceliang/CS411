from __future__ import print_function
from flask import Flask, render_template,redirect,session, jsonify, request, url_for, session
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from functools import wraps
import pymongo
import uuid
import sys
import json
import sqlite3
# Internal imports
#from db import init_db_command
#from user import User

import json
import os
import sqlite3


from oauthlib.oauth2 import WebApplicationClient
import requests

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
# Configuration
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

DEBUG = True
app = Flask(__name__)
app.secret_key = "fkjerhshdjjkefjksdjhkfshjkdsjhksfdjjsadjhka"

# User session management setup
# https://flask-login.readthedocs.io/en/latest
login_manager = LoginManager()
login_manager.init_app(app)

# Naive database setup
try:
    init_db_command()
except:
#except sqlite3.OperationalError:
    # Assume it's already been created
    pass

# OAuth 2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)

#Data Dictionary
#data_dict = {}

# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    #data_dict['user id'] = user_id
    return User.get(user_id)

@app.route("/")
def index():
    if current_user.is_authenticated:
        return render_template("dashboard.html") #, username = current_user.name, useremail = current_user.email, profilepic = current_user.profile_pic, userid = data_dict['user id'])
            #(
            #"<p>Hello, {}! You're logged in! Email: {}</p>"
            #"<div><p>Google Profile Picture:</p>"
            #'<img src="{}" alt="Google profile pic"></img></div>'
            #'<a class="button" href="/logout">Logout</a>'.format(
                #current_user.name, current_user.email, current_user.profile_pic
           # )
        #)
    else:
        #return render_template("login.html")
        return '<a class="button" href="/login">Google Login</a>'
        #return None

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

@app.route("/login")
def oauthlogin():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    print("HERE", request_uri)
    return redirect(request_uri)

@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    # Create a user in your db with the information provided
    # by Google
    '''user = User(
        id_=unique_id, name=users_name, email=users_email, profile_pic=picture
    )

    # Doesn't exist? Add it to the database.
    if not User.get(unique_id):
        User.create(unique_id, users_name, users_email, picture)

    # Begin user session by logging the user in
    login_user(user)

    # Send user back to homepage'''
    return redirect('/dashboard/')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

#Database
client_db = pymongo.MongoClient('localhost', 27017)
db = client_db.user_login_system

# Decorators
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            return redirect('/')
    return wrap

# Routes
from user import routes
@app.route("/postmethod", methods = ['POST'])
def post_javascript_data():
    jsdata = request.form['canvas_data']

    #jsonify(jsdata)
    #print(jsdata[12: -2], file = sys.stderr)
    #return jsonify(jsdata)
    return jsdata

def create_csv(text):
    unique_id = str(uuid.uuid4())
    with open('images/'+unique_id+'.csv', 'a') as file:
        file.write(text[1:-1]+"\n")
    return unique_id

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard/')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/player/')
def player():
    return render_template('player.html')
