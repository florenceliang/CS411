import os
import json
import requests
import functools
from app import app
from flask import (
    Flask, Blueprint, redirect, request, session, url_for
)
from flask_login import (
    current_user, login_required, login_user, logout_user
)
from oauthlib.oauth2 import WebApplicationClient
import user
from user.models import User

# blueprint = Blueprint('auth', __name__, url_base='/auth')

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)

client = WebApplicationClient(GOOGLE_CLIENT_ID)

@app.route('/user/loginGoogle', methods = ['POST'])
def loginGoogle():
    # Google login URL that should be reached
    auth_endpoint = "https://accounts.google.com/o/oauth2/v2/auth"
    redirect_uri = request.base_url + "/callback"

    # Set the scopes that our app will get from Google if the user
    # consents on login page
    request_uri = client.prepare_request_uri(
        auth_endpoint,
        redirect_uri = redirect_uri,
        scope = ["email", "profile", "openid"]
    )
    return redirect(request_uri)

@app.route('/user/loginGoogle/callback', methods = ['POST', 'GET'])
def callback():
    auth_code = request.args.get("code")

    # Token URL to be given permission from Google to obtain and use
    # a user's google login information.
    token_endpoint = "https://oauth2.googleapis.com/token"

    token_request = client.prepare_token_request(
        token_endpoint,
        authorization_response = request.url,
        redirect_url = request.base_url,
        code = auth_code
    )

    token_url = token_request[0]
    headers = token_request[1]
    body = token_request[2]

    # token json response containing
    token_resp = requests.post(token_url, headers = headers, data = body, auth = (GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET)).json()

    # Parse the json response
    token = client.parse_request_body_response(token_resp)
    user_info_endpoint = "https://openidconnect.googleapis.com/v1/userinfo"

    uri, headers, data = token.add_token(user_info_endpoint)

    user_info_resp = requests.get(uri, headers = headers, data = data).json()

    if user_info_resp["email_verified"] == False:
        return "Google account is either unavailable or permission was not granted.", 400
    else:
        user_id = user_info_resp["sub"]
        user_email = user_info_resp["email"]
        user_name = user_info_resp["given_name"]

        user = User().signup_Google(user_id, user_name, user_email)
