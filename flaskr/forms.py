from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo



class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=5,max=15)])
	email_address = StringField('Email Address', validators=[DataRequired(), Email()])
	full_name = StringField('Full Name', validators=[DataRequired(), Length(min=5,max=100)])
	country = StringField('Country', validators=[Length(min=0,max=30)])
	mobile = StringField('Mobile', validators=[Length(min=0,max=30)])
	#id_passport = StringField('ID / Passport', validators=[Length(min=10,max=30)])
	
	#referral_code = StringField('Referral Code', validators=[Length(min=5,max=15)])
	password = PasswordField('Password', validators=[DataRequired(), Length(min=8,max=15)])
	confirm_pass = PasswordField('Confirm Password', 
		validators=[DataRequired(), Length(min=8,max=15),EqualTo('password')])
	#is_admin = BooleanField('Is Admin')
	#createdDate = StringField('Created On')
	#activeDate = StringField('Activated On')
	#updatedDate = StringField('Activated On')
	#is_approved = BooleanField('Is Approved')
	#is_active = BooleanField('Is Active')
	#withdraw_wallet = StringField('Withdraw Wallet')
	#weekly_reward = StringField('Weekly Wallet')
	#monthly_reward = StringField('Monthly Wallet')
	#jackpot_reward = StringField('Jackpot Wallet')
	#direct_reward = StringField('Direct Wallet')
	is_terms = BooleanField('Terms & Conditions', validators=[DataRequired()])
	referral_link = StringField('Referral Link', validators=[Length(min=0,max=10)])
	signup = SubmitField('Sign Up')

class MemberActivation(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=5,max=15)])
	email_address = StringField('Email Address', validators=[DataRequired(), Email()])
	full_name = StringField('Full Name', validators=[DataRequired(), Length(min=5,max=100)])
	createdDate = StringField('Created On')
	activeDate = StringField('Activated On')
	is_active = BooleanField('Is Active')
	load = SubmitField('Load')
	activate = SubmitField('Activate')

class MemberApproval(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=5,max=15)])
	email_address = StringField('Email Address', validators=[DataRequired(), Email()])
	full_name = StringField('Full Name', validators=[DataRequired(), Length(min=5,max=100)])
	createdDate = StringField('Created On')
	updatedDate = StringField('Activated On')
	is_approved = BooleanField('Is Approved')
	load = SubmitField('Load')
	approve = SubmitField('Approve')

class AdminUsers(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=5,max=15)])
	email_address = StringField('Email Address', validators=[DataRequired(), Email()])
	full_name = StringField('Full Name', validators=[DataRequired(), Length(min=5,max=100)])
	password = PasswordField('Password', validators=[DataRequired(), Length(min=8,max=15)])
	confirm_pass = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=8,max=15),EqualTo('password')])
	# createdDate = StringField('Created On')
	submit = SubmitField('Add Admin')

class AdminManager(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=5,max=15)])
	email_address = StringField('Email Address', validators=[DataRequired(), Email()])
	full_name = StringField('Full Name', validators=[DataRequired(), Length(min=5,max=100)])
	# updatedDate = StringField('Updated On')
	# is_approved = BooleanField('Is Approved')
	approve_hidden = HiddenField()
	load = SubmitField('Load')
	submit = SubmitField()

class MemberManager(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=5,max=15)])
	email_address = StringField('Email Address', validators=[DataRequired(), Email()])
	full_name = StringField('Full Name', validators=[DataRequired(), Length(min=5,max=100)])
	# updatedDate = StringField('Updated On')
	# is_approved = BooleanField('Is Approved')
	member_hidden = HiddenField()
	load = SubmitField('Load')
	submit = SubmitField()

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=5,max=15)])
	# email_address = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired(), Length(min=8,max=15)])
	# remember = BooleanField('Remember Me')
	login = SubmitField('Login')


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
	announcement = StringField('Announcements', validators=[DataRequired()])
	isactive = BooleanField('Active', validators=[])
	anna_hidden = HiddenField()
	submit = SubmitField('Add')
	load = SubmitField('Load')

class PackageConfigForm(FlaskForm):
	createdDate = StringField('Created On', validators=[])
	package_id = StringField('Package Id')
	package = StringField('Package Amount', validators=[DataRequired(), Length(min=3,max=5)])
	submit = SubmitField('Add Package')


class RewardConfigForm(FlaskForm):
	createdDate = StringField('Created On', validators=[])
	reward = StringField('Reward Type')
	percentage = StringField('Reward Percentage', validators=[DataRequired(), Length(min=1,max=2)])
	reward_hidden = HiddenField()
	submit = SubmitField('Impact')
	load = SubmitField('Load')

class WalletConfigForm(FlaskForm):
	createdDate = StringField('Updated On', validators=[])
	sbn_wallet = StringField('SBN Wallet', validators=[DataRequired()])
	wallet_hidden = HiddenField()
	submit = SubmitField('Impact')
	load = SubmitField('Load')

class WeeklyRewardForm(FlaskForm):
	percentage = StringField('Percentage in numbers', validators=[DataRequired(), Length(min=1,max=2)])
	submit = SubmitField('Impact to all')
