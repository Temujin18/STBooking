from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo
import phonenumbers

class Phone(object):
        def __init__(self, message=None):
            if not message:
                message = 'Please enter a valid phone number.'
            self.message = message
        
        def __call__(self, form, field):
            if len(field.data) > 16:
                raise ValidationError('Invalid phone number.')
            try:
                input_number = phonenumbers.parse(field.data)
                if not (phonenumbers.is_valid_number(input_number)):
                        raise ValidationError('Invalid phone number.')
            except:
                input_number = phonenumbers.parse("+1"+field.data)
                if not (phonenumbers.is_valid_number(input_number)):
                        raise ValidationError('Invalid phone number.')

class BookingForm(FlaskForm):
    firstname = StringField('First Name', 
            validators=[DataRequired(), Length(min=2, max=50)])
    
    lastname = StringField('Last Name', 
            validators=[DataRequired(), Length(min=2, max=50)])
    
    email = StringField('Email', validators=[Email()])

    phone = StringField('Phone', validators=[DataRequired()])

    submit = SubmitField('Book Now')

class RegistrationForm(FlaskForm):
    username = StringField('Username',
            validators=[DataRequired(), Length(min=2, max=20)])
    
    email = StringField('Email',
            validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired()])

    confirm_password = PasswordField('Confirm Password',
            validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email',
            validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired()])

    remember = BooleanField('Remember Me')

    submit = SubmitField('Sign Up')