from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)


@app.route('/')
@app.route('/login/')
def login():
    return render_template('/auth/login.html')

@app.route('/signup/')
def signup():
    return render_template('/auth/signup.html')

@app.route('/verify/')
def verify_usr():
    return render_template('/auth/verify_usr.html')

@app.route('/forgot_pwd/')
def forgot_pwd():
    return render_template('/usrmgm/forgot_pwd.html')

@app.route('/forgot_usr/')
def forgot_usr():
    return render_template('/usrmgm/forgot_usr.html')

@app.route('/change_pwd/')
def change_pwd():
    return render_template('/usrmgm/change_pwd.html')




if __name__ == '__main__':
    app.run(debug=True)