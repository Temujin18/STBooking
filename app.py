from flask import Flask, render_template
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm
import os

load_dotenv()

DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_NAME = os.environ['DB_NAME']
SECRET_KEY = os.environ['SECRET_KEY']

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASSWORD}@localhost:5432/{DB_NAME}'
app.config['SECRET_KEY'] = SECRET_KEY

db = SQLAlchemy(app)

@app.route("/")
def index():
    return render_template('layout.html')

@app.route("/register")
def register():
    form = RegistrationForm()
    return render_template('register.html', form=form)

@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)