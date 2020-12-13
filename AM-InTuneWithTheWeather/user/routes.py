from flask import Flask
from app import app
from user.models import User


@app.route('/user/signup', methods=['POST'])
def signup():
    return User().signup()

@app.route('/user/signout')
def signout():
    return User().signout()

@app.route('/user/login', methods=['POST'])
def login():
    return User().login()

@app.route("/user/weather", methods = ['POST'])
def getWeather():
    return User().getWeatherData()

@app.route('/user/makemoodchanges', methods=['POST'])
def makeMoodChanges():
    return User().makeMoodChanges()


@app.route('/user/makegenrechanges', methods=['POST'])
def makeGenreChanges():
    return User().makeGenreChanges()
