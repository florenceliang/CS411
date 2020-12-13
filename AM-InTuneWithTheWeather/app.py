from flask import Flask, render_template, redirect, session
from functools import wraps
import pymongo
import uuid
import sys

app = Flask(__name__)
app.secret_key = "fkjerhshdjjkefjksdjhkfshjkdsjhksfdjjsadjhka"

# Database
# local: client = pymongo.MongoClient('localhost', 27017)
client = pymongo.MongoClient("mongodb+srv://411projectteam:411projecteam@cluster0.94v8n.mongodb.net/user_login_system?retryWrites=true&w=majority")
db = client.user_login_system

# Decorators


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/')
    return wrap


# Routes
from user import routes
from user.models import User
from user.player import Player

thePlayer = Player()


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/dashboard/')
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/player/')
def player():
    thePlayer.findPlaylist()
    return render_template('player.html')