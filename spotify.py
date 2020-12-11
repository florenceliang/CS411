import os
import base64
import json
import requests
import sys
import datetime
from urllib.parse import urlencode

# Class that handles API calls to the Spotify web API
class spotifyAPI():
    access_token = None
    access_token_expiration = datetime.datetime.now()
    access_token_expired = True
    clientID = None
    clientSecret = None
    tokenURL = "https://accounts.spotify.com/api/token"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clientID = os.getenv("SPOTIFY_CLIENT_ID")
        self.clientSecret = os.getenv("SPOTIFY_CLIENT_SECRET")

    def get_client_creds(self):
        clientID = self.clientID
        clientSecret = self.clientSecret

        # Check if the client ID and Secret has been set to their proper values before proceeding.
        if clientID == None or clientSecret == None:
            raise Exception("clientID and/or clientSecret has not been set yet.")

        client_creds = (clientID + ':' + clientSecret).encode()
        client_creds_64 = base64.b64encode(client_creds).decode('utf-8')
        client_creds_final = "Basic " + client_creds_64
        
        return client_creds_final

    def get_token_header(self):
        client_creds = self.get_client_creds()
        token_header = {'Authorization': client_creds}
        return token_header

    def get_token_data(self):
        return {"grant_type" : "client_credentials"}

    # Get access token using our client credentials to be able to make search API calls.
    def get_auth(self):
        tokenURL = self.tokenURL
        token_header = self.get_token_header()
        token_data = self.get_token_data()

        r = requests.post(tokenURL, headers = token_header, data = token_data)
        
        # Check the token response to confirm that our post was responded with an OK
        valid_response = r.status_code in range(200,299)
        if valid_response == False:
            return False
        else:
            token_response = r.json()
            self.access_token = token_response["access_token"]
            time_now = datetime.datetime.now()
            expiration_duration = token_response["expires_in"]
            expiration_time = time_now + datetime.timedelta(seconds = expiration_duration)
            self.access_token_expiration = expiration_time
            self.access_token_expired = expiration_time < time_now
            return True

    # Versatile get method to get a specific resource from spotify, e.g. album name, artist name
    def get_resource(self, resource_type, id, version="v1"):
        endpoint = f"https://api.spotify.com/{version}/{resource_type}/{id}"
        headers = {
            "Authorization" : f"Bearer {self.access_token}"
        }
        r = requests.get(endpoint, headers=headers)
        valid_response = r.status_code in range(200,299)
        if valid_response == False:
            return {}
        else:
            return r.json()

    # Method that utilizes get_resource to get the name of an album with the matching id
    def get_albums(self, id):
        return self.get_resource("albums", id)

    # Method that utilizes get_resource to get the name of an artist with the matching id
    def get_artists(self, id):
        return self.get_resource("artists", id)

    # Search method that returns a search list of tracks
    # genre: specifies the genre being searched for
    # market_location: the primary market location that tracks will be searched within, written in ISO 3166-1 alpha-2 country code format
    # limit: the number of items returned in the search
    def songSearch_Genre(self, genre, market_location, limit):
        access_token = self.access_token
        auth_headers = {
            "Authorization" : f"Bearer {access_token}"
        }
        endpoint = "https://api.spotify.com/v1/search"
        data = urlencode({
            "q" : "genre:" + genre,
            "type" : "track",
            "market" : market_location,
            "limit" : str(limit)
        })
    
        lookup_URL = endpoint + "?" + data
        r = requests.get(lookup_URL, headers = auth_headers)
        valid_response = r.status_code in range(200,299)

        if valid_response == False:
            print("Invalid API call.")
            return []
        else:
            lookup_data = r.json()
            listings = lookup_data["tracks"]["items"]

            results = []

            for i in range(0, len(listings)):
                track_title = listings[i]["name"]
                track_artist = listings[i]["artists"][0]["name"]
                track_ID = listings[i]["id"]

                results.append([track_title, track_artist, track_ID])

            """
            ***Uncomment these two lines to look at the json response returned from the get request.***
        
            json_pretty = json.dumps(lookup_data, indent=2)
            print(json_pretty)
            """
            

            return results

    # Search method that returns a list of playlists matching a specified genre
    # genre: specifies the genre that should be found within the playlist title or description
    # market_location: the primary market location that tracks will be searched within, written in ISO 3166-1 alpha-2 country code format
    # limit: the number of items returned in the search
    def playlistSearch_Genre(self, genre, market_location, limit):
        access_token = self.access_token
        auth_headers = {
            "Authorization" : f"Bearer {access_token}"
        }
        endpoint = "https://api.spotify.com/v1/search"
        data = urlencode({
            "q" : genre,
            "type" : "playlist",
            "market" : market_location,
            "owner" : "Spotify",
            "limit" : str(limit)
        })

        lookup_URL = endpoint + "?" + data
        r = requests.get(lookup_URL, headers = auth_headers)
        valid_response = r.status_code in range(200,299)

        if valid_response == False:
            print("Invalid API call.")
            return []
        else:
            lookup_data = r.json()
            playlists = lookup_data["playlists"]["items"]

            results = []
            for i in range(0, len(playlists)):
                playlist_title = playlists[i]["name"]
                playlist_descript = playlists[i]["description"]
                playlist_link = playlists[i]["external_urls"]["spotify"]
                playlist_ID = playlists[i]["id"]

                results.append([playlist_title, playlist_descript, playlist_ID])


            """
            ***Uncomment these two lines to look at the json response returned from the get request.***

            json_pretty = json.dumps(lookup_data, indent=2)
            print(json_pretty)

            """

            return results

    # TODO: Return only Spotify-made playlists (not public playlists created by other users).
    # Search method that returns a list of playlists matching a list of keywords
    # keywords: specifies keywords that should be found within the playlist title or description
    # market_location: the primary market location that tracks will be searched within, written in ISO 3166-1 alpha-2 country code format
    # limit: the number of items returned in the search
    def playlistSearch_Keywords(self, keywords, market_location, limit):
        access_token = self.access_token
        auth_headers = {
            "Authorization" : f"Bearer {access_token}"
        }
        endpoint = "https://api.spotify.com/v1/search"

        query = keywords[0]
        for kw in keywords[1:]:
            query = query + "+" + kw

        data = urlencode({
            "q" : query,
            "type" : "playlist",
            "market" : market_location,
            "owner" : "Spotify",
            "limit" : str(limit)
        })

        lookup_URL = endpoint + "?" + data
        r = requests.get(lookup_URL, headers = auth_headers)
        valid_response = r.status_code in range(200,299)

        if valid_response == False:
            print("Invalid API call.")
            return []
        else:
            lookup_data = r.json()
            playlists = lookup_data["playlists"]["items"]

            results = []
            for i in range(0, len(playlists)):
                playlist_title = playlists[i]["name"]
                playlist_descript = playlists[i]["description"]
                playlist_link = playlists[i]["external_urls"]["spotify"]
                playlist_ID = playlists[i]["id"]

                results.append([playlist_title, playlist_descript, playlist_ID])

            """
            ***Uncomment these two lines to look at the json response returned from the get request.***
            
            json_pretty = json.dumps(lookup_data, indent=2)
            print(json_pretty)
            """


            return results
        
    def pretty_display(self, results):
        for item in results:
            print(item)

""" Test calls and display: Uncomment any pair to search and display their respective function calls. """
# UNCOMMENT THESE TWO LINES TO RUN THE TEST CALLS
#client = spotifyAPI()           # Initialize a new spotify API object so we can begin making searches
#auth_value = client.get_auth()  # Test check to see that our authorization to make API calls works

# Search for tracks by genre
#sunny_songs = client.songSearch_Genre("rap", "US", 3)   # Test check to see that our search call using the API works
#client.pretty_display(sunny_songs)

# Search for playlists by a genre
#rainy_playlist = client.playlistSearch_Keywords("lofi", "US", 2)
#client.pretty_display(rainy_playlist)

#snowy_playlist_advanced = client.playlistSearch_Keywords(["lofi", "hip", "hop"], "US", 2)
#client.pretty_display(snowy_playlist_advanced)