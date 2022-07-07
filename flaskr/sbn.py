from flask import Flask, render_template, url_for
from forms import RegistrationForm, LoginForm, ForgotPwdForm, ForgotUsrForm, ProfileForm, AnnouncementsForm, PackageConfigForm, RewardConfigForm, WalletConfigForm
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

# for cross site 
# python commandline 
# import secrets
# secrets.token_hex(16)
app.config['SECRET_KEY'] = '65be61ace4c4e656af472288a7202919'
app.config['MONGO_URI'] = "mongodb://localhost:27017/sbndb"
mongodb_client = PyMongo(app)
# app.config["CACHE_TYPE"] = "null" 
dal = mongodb_client.db

def getUsers():
    sbn_users = dal.sbn_users.aggregate([{'$lookup':{'from':'user_package','localField':'username','foreignField':'username','as':'packages'}}])
    return sbn_users
@app.route('/')
@app.route("/index", methods=['GET'])
def index():
    sbnusers = dal.sbn_users.find_one({'username':'hayyan'})
    return render_template('/index.html', title='SBN is coming!', sbnusers = sbnusers)
    
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

# @app.route('/mydashboard/')
# def mydashboard():
#     return render_template('mydashboard.html', title='User Dashboard')


@app.route('/mydashboard/')
def mydashboard():
    return render_template('dashboard.html', title='User Dashboard')

@app.route('/admin_panel/')
def admin_panel():
    return render_template('/adminpanel/adminpanel.html', title='Admin Dashboard')

@app.route('/announcements/', methods=['GET','POST'])
def announcements():
    ann_form = AnnouncementsForm()
    sbn_ann = dal.sbn_announcements.find()
    return render_template('/adminpanel/announcements.html', title='Announcements', sbn_ann=sbn_ann, ann_form=ann_form)

@app.route('/user_settings/', methods=['GET','POST'])
def user_settings():
    form = RegistrationForm()
    return render_template('/adminpanel/users_activation.html', title='User Settings', form=form)

@app.route('/package_config/', methods=['GET','POST'])
def package_config():
    form = PackageConfigForm()
    pkg_sbn = dal.sbn_packages.find()
    return render_template('/adminpanel/config/package_config.html', title='Package Config', pkg_sbn=pkg_sbn, form=form)

@app.route('/reward_config/', methods=['GET','POST'])
def reward_config():
    form = RewardConfigForm()
    reward_weekly = dal.reward_config.find_one({'reward':'Weekly'})
    reward_monthly = dal.reward_config.find_one({'reward':'Monthly'})
    reward_member = dal.reward_config.find_one({'reward':'Member'})
    return render_template('/adminpanel/config/reward_config.html', title='Reward Config', reward_weekly = reward_weekly, reward_monthly=reward_monthly, reward_member = reward_member, form=form)

@app.route('/wallet_config/', methods=['GET','POST'])
def wallet_config():
    form = WalletConfigForm()
    sbn_wallet = dal.sbn_wallet.find()
    return render_template('/adminpanel/config/wallet_config.html', title='Wallet Config', sbn_wallet = sbn_wallet, form=form)

@app.route('/weekly_reward/', methods=['GET','POST'])
def weekly_reward():
    form = RewardConfigForm()
    sbn_weekly = getUsers()
    return render_template('/adminpanel/dashboard/weekly_rewards.html', title='Weekly Rewards', form=form, sbn_weekly=sbn_weekly)

@app.route('/monthly_reward/', methods=['GET','POST'])
def monthly_reward():
    form = RewardConfigForm()
    sbn_packages = dal.sbn_packages.find()
    sbn_monthly = getUsers()
    return render_template('/adminpanel/dashboard/monthly_rewards.html', title='Monthly Rewards', form=form, sbn_packages = sbn_packages, sbn_monthly=sbn_monthly)

@app.route('/direct_reward/', methods=['GET','POST'])
def direct_reward():
    reg_form = RegistrationForm()
    reward_form = RewardConfigForm()
    return render_template('/adminpanel/dashboard/direct_rewards.html', title='Direct Rewards', reg_form=reg_form, reward_form=reward_form)

@app.route('/jackpot/', methods=['GET','POST'])
def jackpot():
    reg_form = RegistrationForm()
    # sbn_jackpot = dal.sbn_users.find({'is_active':'true','is_admin':'false'})
    sbn_jackpot = getUsers()
    return render_template('/adminpanel/dashboard/jackpot.html', title='Jackpot', sbn_jackpot=sbn_jackpot, reg_form=reg_form)


if __name__ == '__main__':
    app.run(debug=True)