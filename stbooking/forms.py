from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DateField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo
import phonenumbers
from datetime import date
from stbooking.models import UserAccount, Guest

class Phone(object):
        def __init__(self, message=None):
            if not message:
                message = 'Please enter a valid phone number.'
            self.message = message
        
        def __call__(self, form, field):
            if len(field.data) > 11:
                raise ValidationError('Phone number: (0/63)9XX XXX XXXX.')
            try:
                input_number = phonenumbers.parse(field.data)
                if not (phonenumbers.is_valid_number(input_number)):
                        raise ValidationError('Phone number: (0/63)9XX XXX XXXX.')
            except:
                input_number = phonenumbers.parse("+63"+field.data)
                if not (phonenumbers.is_valid_number(input_number)):
                        raise ValidationError('Phone number: (0/63)9XX XXX XXXX.')

class BookingForm(FlaskForm):
    firstname = StringField('First Name', 
            validators=[DataRequired(), Length(min=2, max=50)])
    
    lastname = StringField('Last Name', 
            validators=[DataRequired(), Length(min=2, max=50)])
    
    email = StringField('Email', validators=[Email()])

    phone = StringField('Cell Number', validators=[DataRequired(), Phone()])

    __room_types = [('single','Single'),('double','Double'),('triple','Triple'),('quad','Quad'),('queen','Queen'),('king','King')]
    room = SelectField('Room Type', choices=__room_types)

    start_date = DateField('Start Date', format='%m-%d-%Y', validators=[DataRequired()], default=date.today)
    end_date = DateField('End Date', format='%m-%d-%Y', validators=[DataRequired()])

    def validate_end_date(form, field):
        if field.data < form.start_date.data:
            raise ValidationError("End date must not be earlier than start date.")

    submit = SubmitField('Book Now')

class RegistrationForm(FlaskForm):
    username = StringField('Username',
            validators=[DataRequired(), Length(min=2, max=20)])
    
    email = StringField('Email',
            validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired()])

    confirm_password = PasswordField('Confirm Password',
            validators=[DataRequired(), EqualTo('password')])

    firstname = StringField('First Name', 
            validators=[DataRequired(), Length(min=2, max=50)])
    
    lastname = StringField('Last Name', 
            validators=[DataRequired(), Length(min=2, max=50)])

    phone = StringField('Cell Number', validators=[DataRequired(), Phone()])

    def validate_username(form, username):
        exists = UserAccount.query.filter_by(username=username.data).scalar() is not None
        if exists:
            raise ValidationError("Username already exists.")

    def validate_email(form, email):
        exists = Guest.query.filter_by(email=email.data).scalar() is not None
        if exists:
            raise ValidationError("Email already in use.")

    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email',
            validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired()])

    remember = BooleanField('Remember Me')

    submit = SubmitField('Log In')