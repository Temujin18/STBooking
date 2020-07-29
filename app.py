from flask import Flask, render_template, flash, redirect, url_for
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm
import os
import enum

load_dotenv()

DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_NAME = os.environ['DB_NAME']
SECRET_KEY = os.environ['SECRET_KEY']

# Room table in postgres has room_type enum with values single, double, triple, quad, queen, king
# Room table also has room_status enum with values booked, vacant, out order


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASSWORD}@localhost:5432/{DB_NAME}'
app.config['SECRET_KEY'] = SECRET_KEY

db = SQLAlchemy(app)

# class RoomType(enum.Enum):
#     SINGLE = 'single'
#     DOUBLE = 'double'
#     TRIPLE = 'triple'
#     QUAD = 'quad'
#     QUEEN = 'queen'
#     KING = 'king'

# class RoomStatus(enum.Enum):
#     BOOKED = 'booked'
#     VACANT = 'vacant'
#     OUT_OF_ORDER = 'out of order'

class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    guest_booking = db.relationship('Booking', backref='guest', lazy=False)

    def __repr__(self):
        return f"Guest({self.id}, {self.first_name}, {self.last_name})"

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_type = db.Column(db.String(20), nullable=False)
    room_status = db.Column(db.String(20), nullable=False)
    room_booking = db.relationship('Booking', backref='room', lazy=False)

    def __repr__(self):
        return f"Room({self.id}, {self.room_type}, {self.room_status})"

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey('guest.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)

    def __repr__(self):
        return f"Booking({self.id}, {self.room}, {self.guest})"


@app.route("/")
def index():
    return render_template('layout.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}.', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@stbook.com' and form.password.data == 'stbook':
            flash('You are now logged in!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login Failed. Please check username and password.', 'danger')
    return render_template('login.html', title='Login', form=form)

if __name__ == "__main__":
    app.run(debug=True)