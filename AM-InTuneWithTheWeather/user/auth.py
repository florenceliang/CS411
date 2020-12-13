import os
import json
import requests
import functools
from flask import (
    Flask, Blueprint, redirect, request, session, url_for
)
from flask_login import (
    LoginManager, current_user, login_required, login_user, logout_user
)
from oauthlib.oauth2 import WebApplicationClient
import user
from user.models import User

#blueprint = Blueprint('auth', __name__, url_base='/auth')

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