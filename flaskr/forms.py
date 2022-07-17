from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo



class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=5,max=15)])
	email_address = StringField('Email Address', validators=[DataRequired(), Email()])
	full_name = StringField('Full Name', validators=[DataRequired(), Length(min=5,max=100)])
	country = StringField('Country', validators=[Length(min=5,max=30)])
	mobile = StringField('Mobile', validators=[Length(min=10,max=30)])
	id_passport = StringField('ID / Passport', validators=[Length(min=10,max=30)])
	referral_link = StringField('Referral Link', validators=[Length(min=5,max=15)])
	referral_code = StringField('Referral Code', validators=[Length(min=5,max=15)])
	password = PasswordField('Password', validators=[DataRequired(), Length(min=8,max=15)])
	confirm_pass = PasswordField('Confirm Password', 
		validators=[DataRequired(), Length(min=8,max=15),EqualTo('password')])
	terms = StringField('Terms & Conditions', validators=[DataRequired()])
	submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
	email_address = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired(), Length(min=8,max=15)])
	# remember = BooleanField('Remember Me')
	submit = SubmitField('Login')


class ForgotPwdForm(FlaskForm):
	email_address = StringField('Email', validators=[DataRequired(), Email()])
	submit = SubmitField('Send')

class ForgotUsrForm(FlaskForm):
	email_address = StringField('Email', validators=[DataRequired(), Email()])
	submit = SubmitField('Send')

class ProfileForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=5,max=15)])
	email_address = StringField('Email Address', validators=[DataRequired(), Email()])
	full_name = StringField('Full Name', validators=[DataRequired(), Length(min=5,max=100)])
	country = StringField('Country', validators=[Length(min=5,max=30)])
	mobile = StringField('Mobile', validators=[Length(min=10,max=30)])
	id_passport = StringField('ID / Passport', validators=[Length(min=10,max=30)])
	referral_link = StringField('Referral Link', validators=[Length(min=5,max=15)])
	referral_code = StringField('Referral Code', validators=[Length(min=5,max=15)])
	submit = SubmitField('Impact')

class AnnouncementsForm(FlaskForm):
	
	createdDate = StringField('Created On', validators=[])
	announcements = StringField('Announcements', validators=[DataRequired()])
	isactive = BooleanField('Status', validators=[])
	submit = SubmitField('Impact')

class PackageConfigForm(FlaskForm):
	createdDate = StringField('Created On', validators=[])
	package_id = StringField('Package Id')
	package = StringField('Package Amount', validators=[DataRequired(), Length(min=3,max=5)])
	submit = SubmitField('Add Package')


class RewardConfigForm(FlaskForm):
	createdDate = StringField('Created On', validators=[])
	reward = StringField('Reward Type')
	percentage = IntegerField('Reward Percentage', validators=[DataRequired(), Length(min=1,max=2)])
	submit = SubmitField('Impact')

class WalletConfigForm(FlaskForm):
	createdDate = StringField('Updated On', validators=[])
	sbn_wallet = StringField('SBN Wallet', validators=[DataRequired()])
	wallet_hidden = HiddenField()
	submit = SubmitField('Impact')
	load = SubmitField('Load')