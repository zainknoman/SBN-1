from __main__ import app
from flask import session, redirect, url_for, request, render_template, flash
from forms import LoginForm
import bcrypt
from dal import db


def killSession():
    session['username'] = None
    session['full_name'] = None
    session['is_admin'] = None
    session['is_approved'] = None
    session['is_active'] = None
    session.clear()

def get_Login(content):
    user = db.connect.sbn_users.find_one({'$or':[{'username':{'$eq':content}},{'email_address':{'$eq':content}}]})
    return user

@app.route('/logout/')
# @login_required
def logout():
    # user = current_user
    # user.authenticated = False
    # logout_user()
    killSession()
    return redirect(url_for('login'))

@app.route('/login/', methods=['GET','POST'])
def login():
    if "username" in session:
        if session['is_admin'] == True:
            return redirect(url_for('admin_panel'))
        else:
            return redirect(url_for('dashboard'))

    form = LoginForm()
    
    if request.method == "POST":
        if form.validate_on_submit():
            if form.login.data:
                txtPassword = form.password.data
                bytePwd = txtPassword.encode('utf-8')
                
                # users_find = getLogin_username(form.username.data)#load_user(form.email_address.data)#dal.sbn_users.find_one({'email_address':form.email_address.data})
                users_find = get_Login(form.username.data)
                if users_find:
                    hashPassword = users_find['password']

                    if bcrypt.checkpw(bytePwd, hashPassword):
                        session['username']=users_find['username']
                        session['full_name']=users_find['full_name']
                        session['is_admin']=users_find['is_admin']
                        session['is_approved']=users_find['is_approved']
                        session['is_active']=users_find['is_active']

                        if users_find['is_approved'] == False:
                            flash("Administrator has not approved your account yet, kindly wait 24 hrs you will be notified by email","error")
                            return render_template('/auth/login.html', title='Login User', form=form )
                        if users_find['is_admin'] == True:
                            return redirect(url_for('admin_panel'))
                        else:
                            return redirect(url_for('dashboard'))
                    else:
                        flash("Incorrect Password","error")
                else:
                    flash("User does not exist!","error")

    return render_template('/auth/login.html', title='Login User', form=form )
