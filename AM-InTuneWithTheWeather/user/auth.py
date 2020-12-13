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

blueprint = Blueprint('auth', __name__, url_base='/auth')

