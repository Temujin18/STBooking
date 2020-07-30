from flask import render_template, flash, redirect, url_for
from stbooking import app, db, bcrypt
from stbooking.forms import RegistrationForm, LoginForm, BookingForm
from stbooking.models import Guest, Room, Booking
import logging

logging.basicConfig(level=logging.DEBUG)

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
        # hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
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
        guest = Guest(first_name=form.firstname.data, last_name=form.lastname.data, email=form.email.data, phone=form.phone.data)
        db.session.add(guest)
        try:
            first_vacant = Room.query.filter(Room.room_type==form.room.data.title(), Room.room_status=='VACANT').first_or_404()
            logging.debug(form.room.data, first_vacant)
            booking = Booking(start_date=form.start_date.data, end_date=form.end_date.data, guest_id=guest.id, room_id=first_vacant.id)
            db.session.add(booking)
        except:
            flash(f'No vacant {form.room.data.title()} Rooms available.', 'warning')
            return redirect(url_for('book'))
        else:
            flash('You have successfully booked a room.', 'success')
            db.session.commit()
        return redirect(url_for('index'))
    return render_template('book.html', title='Book', form=form)

@app.route("/manage/rooms", methods=['GET', 'POST'])
def manage_rooms():
    rooms = Room.query.order_by(Room.id.asc())
    return render_template('manage_rooms.html', title='Manage Rooms', rooms=rooms)