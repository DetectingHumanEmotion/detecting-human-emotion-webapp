from flask import Flask
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

app.config["WTF_CSRF_SECRET_KEY"] = "To Be changed to a random key"
app.config["SECRET_KEY"] = b'<\xa4`\xb3G\x89>'
