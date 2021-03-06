from flask import render_template, flash, redirect, url_for, request
from stbooking import app, db, bcrypt
from stbooking.forms import RegistrationForm, LoginForm, BookingForm
from stbooking.models import Guest, Room, Booking, UserAccount, AdminAccount, Role
from flask_user import current_user, roles_required, UserManager
from flask_login import login_user, logout_user
from sqlalchemy import and_, or_
import logging

logging.basicConfig(level=logging.DEBUG)

user_manager = UserManager(app, db, UserAccount)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/bookings")
@roles_required('guest')
def bookings():
    page = request.args.get('page',1, type=int)
    bookings = Booking.query.filter(Guest.id==current_user.guest_id).paginate(page=page, per_page=3)
    return render_template('bookings.html', bookings=bookings, page='bookings')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        guest = Guest(first_name=form.firstname.data, last_name=form.lastname.data, email=form.email.data, phone=form.phone.data)
        db.session.add(guest)
        db.session.commit()
        user = UserAccount(email=form.email.data, password=hashed_pw, guest_id=guest.id)
        user_role = get_role('guest')

        if not user_role:
            user.roles.append(Role(name='guest'))
        else:
            user.roles.append(user_role)

        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.email.data}.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = UserAccount.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
        
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Failed. Please check username and password.', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/book", methods=['GET', 'POST'])
def book():
    form = BookingForm()
    if form.validate_on_submit():
        available_room = Room.query.filter(Room.room_type==form.room.data.title(), Room.room_status=='VACANT').first()

        if not available_room:
            booked_rooms = Room.query.filter(Room.room_type==form.room.data.title(), Room.room_status=='BOOKED').all()

            available_room = get_available_booked_room(booked_rooms, form)

        if not available_room: #if get_available_booked_room returns None, then no rooms available
            flash(f'No vacant {form.room.data.title()} Rooms available.', 'warning')
            return redirect(url_for('book'))

        exists = Guest.query.filter_by(email=form.email.data).first() is not None

        if exists:
            guest = Guest.query.filter_by(email=form.email.data).first()
        else:
            guest = Guest(first_name=form.firstname.data, last_name=form.lastname.data, email=form.email.data, phone=form.phone.data)

        db.session.add(guest)
        db.session.commit()

        booking = Booking(start_date=form.start_date.data, end_date=form.end_date.data, guest_id=guest.id, room_id=available_room.id)
        available_room.room_status = 'BOOKED'
        db.session.add(booking)

        flash('You have successfully booked a room.', 'success')
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('book.html', title='Book', form=form, legend='Book Today!')
    

@app.route("/booking/<int:booking_id>/update", methods=['GET', 'POST'])
@roles_required('guest')
def update_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    form = BookingForm()

    if form.validate_on_submit():
        booking.guest.first_name = form.firstname.data
        booking.guest.last_name = form.lastname.data
        booking.guest.email = form.email.data
        booking.room.room_type = form.room.data
        booking.start_date = form.start_date.data
        booking.end_date = form.end_date.data
        booking.guest.phone = form.phone.data

        available_room = Room.query.filter(Room.room_type==booking.room.room_type.title(), Room.room_status=='VACANT').first()

        if not available_room:
            booked_rooms = Room.query.filter(Room.room_type==form.room.data.title(), Room.room_status=='BOOKED').all()

            available_room = get_available_booked_room(booked_rooms, form)

        booking.room.room_id = available_room.id

        db.session.commit()
        flash('Your booking has been updated!', 'success')
        return redirect(url_for('bookings'))
    elif request.method == 'GET':
        form.firstname.data = booking.guest.first_name
        form.lastname.data = booking.guest.last_name
        form.email.data = booking.guest.email
        form.room.data = booking.room.room_type
        form.start_date.data = booking.start_date
        form.end_date.data = booking.end_date
        form.phone.data = booking.guest.phone
    return render_template('book.html', title='Update Booking', form=form, legend='Update Booking')

@app.route("/booking/<int:booking_id>/delete", methods=['POST'])
@roles_required('guest')
def delete_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    booking.room.room_status = 'VACANT'
    db.session.delete(booking)
    db.session.commit()
    flash('Your booking has been deleted!', 'success')
    return redirect(url_for('bookings'))


def get_available_booked_room(booked_rooms, form):
    for booked_room in booked_rooms:
        #check if bookings for each room collides with booking dates
        room_bookings = Booking.query.filter_by(room_id = booked_room.id).all()

        if not room_bookings: #true if a room is booked but there are no bookings associated with it
            return booked_room

        for room_booking in room_bookings:
            #check if booking dates collide with each booking with conditional; (StartA <= EndB) and (EndA >= StartB)
            if form.start_date.data <= room_booking.end_date and form.end_date.data >= room_booking.start_date:
                break #if collision is found, break out of this loop to check other booked rooms
            else:
                continue
        else:
            return booked_room #if no collisions with booking dates of a booked room, return room object

    else:
        return None #if all rooms are looped without returning a booked_room


def get_role(role):
    return Role.query.filter_by(name=role).first()
