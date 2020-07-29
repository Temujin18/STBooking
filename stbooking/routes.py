from flask import render_template, flash, redirect, url_for
from stbooking import app
from stbooking.forms import RegistrationForm, LoginForm, BookingForm
from stbooking.models import Guest, Room, Booking

@app.route("/")
def index():
    return render_template('layout.html')

@app.route("/bookings")
def bookings():
    bookings = Booking.query.all()
    return render_template('bookings.html', bookings=bookings)

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
            
            return redirect(url_for('bookings'))
        else:
            flash('Login Failed. Please check username and password.', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/book", methods=['GET', 'POST'])
def book():
    form = BookingForm()
    if form.validate_on_submit():
        flash('You have successfully booked a room.', 'success')
        return redirect(url_for('index'))
    return render_template('book.html', title='Book', form=form)