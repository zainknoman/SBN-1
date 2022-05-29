from flask import Flask, render_template, url_for
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

# for cross site 
# python commandline 
# import secrets
# secrets.token_hex(16)
app.config['SECRET_KEY'] = '65be61ace4c4e656af472288a7202919'



@app.route('/')
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

@app.route('/forgot_pwd/')
def forgot_pwd():
    return render_template('/usrmgm/forgot_pwd.html', title='Forgot Password')

@app.route('/forgot_usr/')
def forgot_usr():
    return render_template('/usrmgm/forgot_usr.html', title='Forgot User')

@app.route('/change_pwd/')
def change_pwd():
    return render_template('/usrmgm/change_pwd.html', title='Change Password')

@app.route('/mydashboard/')
def mydashboard():
    return render_template('mydashboard.html', title='User Dashboard')

@app.route('/admin_dash/')
def admin_dash():
    return render_template('/adminpanel/adminpanel.html', title='Admin Dashboard')


if __name__ == '__main__':
    app.run(debug=True)