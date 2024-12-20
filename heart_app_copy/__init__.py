from flask import Flask, session
import os
from dotenv import load_dotenv

# This file creates a Flask app object that other parts of the application can use

app = Flask(__name__)
load_dotenv()
app.secret_key= os.getenv("FLASK_SECRET_KEY")