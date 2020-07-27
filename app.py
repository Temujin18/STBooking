from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']

app = Flask(__name__)

@app.route("/")
def hello():
    return f'<h1>Hello! {DB_USER}</h1>'