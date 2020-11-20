import os
import base64
import json
import requests
import sys
import datetime
from bs4 import BeautifulSoup
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
