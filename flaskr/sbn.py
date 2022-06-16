from flask import Flask, render_template, url_for
from forms import RegistrationForm, LoginForm, ForgotPwdForm, ForgotUsrForm, ProfileForm, AnnouncementsForm
from flask_pymongo import PyMongo

app = Flask(__name__)

# for cross site 
# python commandline 
# import secrets
# secrets.token_hex(16)
app.config['SECRET_KEY'] = '65be61ace4c4e656af472288a7202919'
app.config['MONGO_URI'] = "mongodb://localhost:27017/"



@app.route('/')
def coming_soon():
    return render_template('/index.html', title='SBN is coming!')
@app.route('/login/', methods=['GET','POST'])
def login():
    form = LoginForm()
    return render_template('/auth/login.html', title='Login User', form=form )

@app.route('/signup/', methods=['GET','POST'])
def signup():
    form = RegistrationForm()
    return render_template('/auth/signup.html', title='Register User', form=form)

@app.route('/verify/')
def verify_usr():
    return render_template('/auth/verify_usr.html', title='User Verification')

@app.route('/forgot_pwd/', methods=['GET','POST'])
def forgot_pwd():
    form = ForgotPwdForm()
    return render_template('/usrmgm/forgot_pwd.html', title='Forgot Password', form=form)

@app.route('/forgot_usr/', methods=['GET','POST'])
def forgot_usr():
    form = ForgotUsrForm()
    return render_template('/usrmgm/forgot_usr.html', title='Forgot User', form=form)

@app.route('/profile/', methods=['GET'])
def profile():
    form = ProfileForm()
    return render_template('/usrmgm/profile.html', title='Profile', form=form)

@app.route('/mydashboard/')
def mydashboard():
    return render_template('mydashboard.html', title='User Dashboard')

@app.route('/admin_panel/')
def admin_panel():
    return render_template('/adminpanel/adminpanel.html', title='Admin Dashboard')

@app.route('/announcements/')
def announcements():
    return render_template('/adminpanel/announcements.html', title='Announcements')



if __name__ == '__main__':
    app.run(debug=True)