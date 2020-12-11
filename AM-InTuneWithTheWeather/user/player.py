from flask import session, jsonify
from user.spotify import spotifyAPI
import random
from app import db


class Player:
    def __init__(self):
        self.client = (
            spotifyAPI()
        )  # Initialize a new spotify API object so we can begin making searches
        self.auth_value = (
            self.client.get_auth()
        )  # Test check to see that our authorization to make API calls works

    def findPlaylist(self):
        currentWeather = "snowing"  # replace with call to db for current weather
        desiredMood = session["user"][currentWeather]
        genres = [
            "hiphop",
            "pop",
            "country",
            "rock",
            "latin",
            "r&b",
            "indie",
            "party",
            "classical",
            "jazz",
            "folk&acoustic",
            "soul",
            "metal",
        ]
        appropriateGenres = []
        for genre in genres:  # filter out genres that are associated with current mood
            associatedMood = session["user"][genre]
            if associatedMood == desiredMood:
                appropriateGenres.append(genre)

        playlists = []
        if len(appropriateGenres) == 0:
            # if no genres match the desired mood, query top numResults # of playlists that correspond with desired mood
            numResults = 10
            playlists = self.client.playlistSearch_Keywords(
                desiredMood, "US", numResults
            )
        else:
            # if one (or more) genres are associated with desired mood, randomly pick one genre and query numResults # of playlists that correspond with desired mood and genre
            numResults = 4
            randomGenre = random.choice(appropriateGenres)
            playlists = self.client.playlistSearch_Keywords(
                [desiredMood, randomGenre], "US", numResults
            )

        if (
            len(playlists) == 0
        ):  # if spotify api call fails, use playlist stored in mongo
            print("api call returned empty, playing stored playlist")
            return
        else:  # select random playlist from results
            randomPlaylistId = random.choice(playlists)[-1]
            self.updateCurrentPlaylist(randomPlaylistId)

    def updateCurrentPlaylist(self, playlistId):
        # update locally
        session["user"]["playlist"] = playlistId

        # update in database
        if db.users.update(
            {"_id": session["user"]["_id"]}, {"$set": {"playlist": playlistId}}
        ):
            return jsonify({"error": "Successfully updated"}), 0
        return jsonify({"error": "Could not create playlist"}), 398
