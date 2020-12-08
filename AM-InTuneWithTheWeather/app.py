from __future__ import print_function
from flask import Flask, render_template,redirect,session, jsonify, request, url_for
from functools import wraps
import pymongo
import uuid
import sys

app = Flask(__name__)
app.secret_key = "fkjerhshdjjkefjksdjhkfshjkdsjhksfdjjsadjhka"

#Database
client = pymongo.MongoClient('localhost', 27017)
db = client.user_login_system

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
