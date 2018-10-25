from flask import Flask,g
from flask_oidc import OpenIDConnect
from okta import UsersClient
# from flask_pymongo import PyMongo
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config["WTF_CSRF_SECRET_KEY"] = "To Be changed to a random key"
# app.config["SECRET_KEY"] = b'<\xa4`\xb3G\x89>'

app.config["OIDC_CLIENT_SECRETS"] = "detecting_human_emotion_webapp/client_secrets.json"

#The OIDC_COOKIE_SECURE setting allows you to test out user login and registration in development
# without using SSL. If you were going to run your site publicly, you would remove this option and use SSL on your site.
app.config["OIDC_COOKIE_SECURE"] = False
app.config["OIDC_CALLBACK_ROUTE"] = "/oidc/callback"
app.config["OIDC_SCOPES"] = ["openid", "email", "profile"]
app.config["SECRET_KEY"] = "This is some long string for the secret key."
app.config["OIDC_ID_TOKEN_COOKIE_NAME"] = "oidc_token"

