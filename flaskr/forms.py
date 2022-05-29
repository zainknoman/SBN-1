from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
	username = StringField('Username', 
		validators=[DataRequired(), Length(min=5,max=15)])
	email_address = StringField('Email Address', 
		validators=[DataRequired(), Email()])
	full_name = StringField('Full Name', 
		validators=[DataRequired(), Length(min=5,max=100)])
	country = StringField('Country', 
		validators=[Length(min=5,max=30)])
	mobile = StringField('Mobile', 
		validators=[DataRequired(), Length(min=10,max=30)])
	id_passport = StringField('ID / Passport', 
		validators=[Length(min=10,max=30)])
	referral_code = StringField('Referral Code', 
		validators=[Length(min=5,max=15)])
	password = PasswordField('Password', 
		validators=[DataRequired(), Length(min=5,max=15)])
	confirm_pass = PasswordField('Confirm Password', 
		validators=[DataRequired(), Length(min=5,max=15),EqualTo('password')])
	terms = StringField('Terms & Conditions')
	submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
	email = StringField('Email', 
		validators=[DataRequired(), Length(min=5,max=15), Email()])
	password = PasswordField('Password', 
		validators=[DataRequired(), Length(min=5,max=15)])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')