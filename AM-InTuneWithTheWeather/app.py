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
