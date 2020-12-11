from flask import Flask, jsonify, request, session, redirect
from passlib.hash import pbkdf2_sha256
from app import db
import uuid

class User:
    def start_session(self, user):
        del user['password']
        session['logged_in'] = True
        session['user'] = user 
        return jsonify(user), 200

    def signup(self):
        print(request.form)

        # Create the user object
        user = {
            "_id": uuid.uuid4().hex,
            "name": request.form.get('name'),
            "email": request.form.get('email'),
            "password": request.form.get('password'),
            "sunny": request.form.get('sunny'),
            "raining": request.form.get('raining'),
            "snowing": request.form.get('snowing'),
            "foggy": request.form.get('foggy'),
            "cloudy": request.form.get('cloudy'),
            "hiphop": request.form.get('hiphop'),
            "pop": request.form.get('pop'),
            "country": request.form.get('country'),
            "rock": request.form.get('rock'),
            "latin": request.form.get('latin'),
            "r&b": request.form.get('r&b'),
            "indie": request.form.get('indie'),
            "party": request.form.get('party'),
            "classical": request.form.get('classical'),
            "jazz": request.form.get('jazz'),
            "folk&acoustic": request.form.get('folk&acoustic'),
            "soul": request.form.get('soul'),
            "metal": request.form.get('metal'),
            "playlist": "5Zp1iiAdhAiF8t5IXRdEfV",
            "city": "Boston",
            "weather": "sunny"
        }
        # Need to add weather and location

        # Encrypt the password
        user['password'] = pbkdf2_sha256.encrypt(user['password'])

        # Check for existing user with same email
        if db.users.find_one({"email": user['email']}):
            return jsonify({"error": "Email address already in use"}), 400

        if db.users.insert_one(user):
            return self.start_session(user)

        return jsonify({"error": "Signup failed"}), 400

    def signout(self):
        session.clear()
        return redirect('/')

    def login(self):
        user = db.users.find_one({
            "email": request.form.get('email')
        })

        if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
            return self.start_session(user)

        return jsonify({"error": "invalid login credentials"}), 401

    def makeMoodChanges(self):
        if db.users.update(
                {'_id': session['user']['_id']}, {'$set': {
                    'sunny': request.form.get('sunny'),
                    'raining': request.form.get('raining'),
                    'snowing': request.form.get('snowing'),
                    'foggy': request.form.get('foggy'),
                    'cloudy': request.form.get('cloudy')
                }}):
            session['user'] = db.users.find_one(
                {"_id": session['user']['_id']})
            return jsonify({"error": "Successfully updated"}), 0
        return jsonify({"error": "Could not make mood changes"}), 399

    def getWeatherData(self):
        jsdata = request.form['canvas_data']
        bs = eval(jsdata[1:-1])
        weather = bs.get('outcome')
        city = bs.get('city')
        print(city)
        print(weather)
        if db.users.update(
            {'_id': session['user']['_id']}, {'$set': { 
                "city": city,
                "weather": weather
            }}):
            session['user'] = db.users.find_one({"_id":session['user']['_id']})
            return jsonify({"error":"Successfully updated"}), 0
        return jsonify({"error":"Could not make mood changes"}), 399


    def makeGenreChanges(self):
        if db.users.update(
                {'_id': session['user']['_id']}, {'$set': {
                    "hiphop": request.form.get('hiphop'),
                    "pop": request.form.get('pop'),
                    "country": request.form.get('country'),
                    "rock": request.form.get('rock'),
                    "latin": request.form.get('latin'),
                    "r&b": request.form.get('r&b'),
                    "indie": request.form.get('indie'),
                    "party": request.form.get('party'),
                    "classical": request.form.get('classical'),
                    "jazz": request.form.get('jazz'),
                    "folk&acoustic": request.form.get('folk&acoustic'),
                    "soul": request.form.get('soul'),
                    "metal": request.form.get('metal')
                }}):
            session['user'] = db.users.find_one(
                {"_id": session['user']['_id']})
            return jsonify({"error": "Successfully updated"}), 0
        return jsonify({"error": "Could not make genre preference changes"}), 398
