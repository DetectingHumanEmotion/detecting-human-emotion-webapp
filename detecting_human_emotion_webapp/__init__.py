from flask import Flask, g
from flask_oidc import OpenIDConnect
from okta import UsersClient

import platform
import os

"""
Created by tybruno.

This file contains the settings for the application.
It also contains SSO (okta) information needed to interface with Okta
"""

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config["WTF_CSRF_SECRET_KEY"] = "To Be changed to a random key"
#UPLOAD_FOLDER = "detecting_human_emotion_webapp/uploads"
UPLOAD_FOLDER = "../training-data/deception-audio-datasets/testing_data"

# app.config["SECRET_KEY"] = b'<\xa4`\xb3G\x89>'

if platform.system() is "Windows":
    app.config["OIDC_CLIENT_SECRETS"] = "detecting_human_emotion_webapp/client_secrets.json"
else:
    app.config["OIDC_CLIENT_SECRETS"] = "client_secrets.json"

# The OIDC_COOKIE_SECURE setting allows you to test out user login and registration in development
# without using SSL. If you were going to run your site publicly, you would remove this option and use SSL on your site.
app.config["OIDC_COOKIE_SECURE"] = False
app.config["OIDC_CALLBACK_ROUTE"] = "/oidc/callback"
app.config["OIDC_SCOPES"] = ["openid", "email", "profile"]
app.config["SECRET_KEY"] = "This is some long string for the secret key."
app.config["OIDC_ID_TOKEN_COOKIE_NAME"] = "oidc_token"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
