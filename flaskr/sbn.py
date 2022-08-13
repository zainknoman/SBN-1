from flask import Flask, render_template, url_for, request, flash, redirect, session
from forms import (RegistrationForm, LoginForm, ForgotPwdForm, ForgotUsrForm, ProfileForm, 
    AnnouncementsForm, PackageConfigForm, RewardConfigForm, WalletConfigForm, WeeklyRewardForm,
    MemberManager, AdminManager, AdminUsers,
    JackpotForm, MonthlyRewardForm)
from flask_pymongo import PyMongo
from flask_wtf.csrf import CSRFProtect
from bson.objectid import ObjectId
from datetime import datetime
import bcrypt
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)

app = Flask(__name__)
import login
import adminmanager
app.config['SECRET_KEY'] = '65be61ace4c4e656af472288a7202919'
app.config['MONGO_URI'] = "mongodb://localhost:27017/sbndb"
# for cross site 
# python commandline 
# import secrets
# secrets.token_hex(16)
csrf = CSRFProtect()
csrf.init_app(app)


mongodb_client = PyMongo(app)
# app.config["CACHE_TYPE"] = "null" 
dal = mongodb_client.db

# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.session_protection = "strong"
# login_manager.login_view = "login"
# login_manager.login_message_category = "info"
# login_manager.login_message = "Please login to access the page"

def generateAdminAccount():
    find_admin = dal.sbn_users.find_one({'username':'admin'})
    if not find_admin:
        dal.create_collection("sbn_users")
        txtPassword = "admin@1234"
        bytePwd = txtPassword.encode('utf-8')
        mysalt = bcrypt.gensalt()
        hashPassword = bcrypt.hashpw(bytePwd,mysalt)
        dal.sbn_users.insert_one({'username':"admin",'email_address':"admin@sbn.com",'full_name':"Administrator",'password':hashPassword,'is_admin':True,'created_date':datetime.now().replace(microsecond=0),'updated_date':datetime.now().replace(microsecond=0),'is_approved':True,'is_active':None})

def generatePackages():
    find_packages = dal.sbn_packages.find_one({'package_id':'pkg500'})
    if not find_packages:
        dal.create_collection("sbn_packages")
        dal.sbn_packages.insert_one({'package_id':"pkg500",'package':500,'package_date':datetime.now().replace(microsecond=0)})
        dal.sbn_packages.insert_one({'package_id':"pkg1000",'package':1000,'package_date':datetime.now().replace(microsecond=0)})
        dal.sbn_packages.insert_one({'package_id':"pkg2000",'package':2000,'package_date':datetime.now().replace(microsecond=0)})
        dal.sbn_packages.insert_one({'package_id':"pkg3000",'package':3000,'package_date':datetime.now().replace(microsecond=0)})
        dal.sbn_packages.insert_one({'package_id':"pkg5000",'package':5000,'package_date':datetime.now().replace(microsecond=0)})

def generateRewards():
    find_reward = dal.reward_config.find_one({'reward':'Weekly'})
    if not find_reward:
        dal.create_collection("reward_config")
        dal.reward_config.insert_one({'reward':"Weekly",'percentage':1,'createdDate':datetime.now().replace(microsecond=0),'updatedDate':None})
        dal.reward_config.insert_one({'reward':"Monthly",'percentage':1,'createdDate':datetime.now().replace(microsecond=0),'updatedDate':None})
        dal.reward_config.insert_one({'reward':"Member",'percentage':1,'createdDate':datetime.now().replace(microsecond=0),'updatedDate':None})
        
def generateWallet():
    # find_wallet = dal.sbn_wallet.find()
    # if not find_wallet:
    try:
        dal.create_collection("sbn_wallet")
        dal.sbn_wallet.insert_one({'wallet':'65be61ace4c4e656af472288a7202919','updatedDate':datetime.now().replace(microsecond=0)})
    except:
        return

def getall_members():
    sbn_data = dal.sbn_users.find({'is_admin':False})
    return sbn_data
def addMemberAccount(txtUsername,txtEmail,txtFullname,txtCountry,txtMobile,txtReferralLink,txtReferralCode,hashPassword,txtCreatedDate,txtIsTerms):
    if not txtMobile:
        txtMobile = None
    if not txtCountry:
        txtCountry = None
    if not txtReferralLink:
        txtReferralLink = None
        
    dal.sbn_users.insert_one({'username':txtUsername,'email_address':txtEmail,'full_name':txtFullname,'password':hashPassword,'country':txtCountry,'mobile':txtMobile,'id_passport':None,'referral_link':txtReferralLink,'referral_code':txtReferralCode,'is_admin':False,'is_terms':txtIsTerms,'created_date':txtCreatedDate,'updated_date':None,'active_date':None,'is_approved':False,'is_active':False,'packages':[None],'withdraw_wallet':0,'weekly_reward':0,'monthly_reward':0, 'jackpot_reward':0,'direct_reward':0})
def approveMemberAccount(uxr,approve):
    dal.sbn_users.find_one_and_update({'username':uxr},{'$set':{'is_approved':approve, 'updated_date':datetime.now().replace(microsecond=0)}})
def activeMemberAccount(uxr,active):
    dal.sbn_users.find_one_and_update({'username':uxr},{'$set':{'is_active':active, 'active_date':datetime.now().replace(microsecond=0)}})

def get_memberManager(todo):
    sbn_data = ''
    if todo == 'approval':
        sbn_data = dal.sbn_users.find({'$and':[{'is_admin':{'$eq':False}},{'is_approved':{'$eq':False}}]})
    elif todo == 'activation':
        sbn_data = dal.sbn_users.find({'$and':[{'is_admin':{'$eq':False}},{'is_active':{'$eq':False}}]})
    elif todo == 'disapproval':
        sbn_data = dal.sbn_users.find({'$and':[{'is_admin':{'$eq':False}},{'is_approved':{'$eq':True}}]})
    elif todo == 'deactivation':
        sbn_data = dal.sbn_users.find({'$and':[{'is_admin':{'$eq':False}},{'is_active':{'$eq':True}}]})
    return sbn_data 

def get_activeMembers(pkg):
    if pkg:
        sbn_data = dal.sbn_users.find({'$and':[{'is_admin':{'$eq':False}},{'is_active':{'$eq':True}},{'packages':{'$in':[pkg]}}]})
    else:
        sbn_data = dal.sbn_users.find({'$and':[{'is_admin':{'$eq':False}},{'is_active':{'$eq':True}}]})
    return sbn_data

def get_announcements():
    sbn_data = dal.sbn_announcements.find()
    return sbn_data
def get_announcement(ob):
    sbn_data = dal.sbn_announcements.find_one({'_id':ObjectId(ob)})
    return sbn_data
def addAnnouncement(content,status):
    dal.sbn_announcements.insert_one({'announcement':content, 'isactive':status, 'createdDate':datetime.now().replace(microsecond=0)})
def updateAnnouncement(annId,content,status):
    dal.sbn_announcements.find_one_and_update({'_id':ObjectId(annId)},{'$set':{'announcement':content, 'isactive':status}})





def flushMemberManager():
    form = MemberManager()
    form.username.data = None
    form.full_name.data = None
    form.email_address.data = None
    return




# class User(UserMixin):
#     def __init__(self, username, password):
#         self.username = username
#         self.password = password
#         self.active = True
#         if self.username == 'admin':
#             self.is_admin = True
#         else:
#             self.is_admin = False

#     def get_id(self):
#         return self.username

#     @property
#     def is_active(self):
#         return self.active

# def getLogin_email(user_email):
#     user = dal.sbn_users.find_one({'email_address':user_email})
#     return user
# def getLogin_username(username):
#     user = dal.sbn_users.find_one({'username':username})
#     return user


def getMember_email(user_email):
    user = dal.sbn_users.find_one({'email_address':user_email, 'is_admin':False})
    return user
def getMember_username(username):
    user = dal.sbn_users.find_one({'username':username, 'is_admin':False})
    return user
def getMember_Id(ob):
    user = dal.sbn_users.find_one({'_id':ObjectId(ob), 'is_admin':False})
    return user

def reg_weekly(sbn_members,percentage):
    display = False
    reward = 0
    for data in sbn_members:
        username = data['username']
        packages = data['packages']
        for pkg in packages:
            package_amount = pkg[3:]
            reward += float(int(package_amount)*int(percentage)/100)
            
        try:
            dal.sbn_users.update_one({'username':username},{'$set':{'weekly_reward':float(reward)}})
            reward = 0
            display = True
        except Exception as e:
            display = False
            flash("Something went wrong!","error")

    return display

def reg_jackpot(uxr,pkg,amt):
    display = False
    currentMonth = datetime.now().month
    
    if currentMonth >= 10 and currentMonth <= 12:
        currentQuarter = 4
        # currentMonth = Oct
        nextQuarter = 1
        nextMonth = 1
    if currentMonth >= 7 and currentMonth <= 9:
        currentQuarter = 3
        # currentMonth = July
        nextQuarter = 4
        nextMonth = 10
    if currentMonth >= 4 and currentMonth <= 6:
        currentQuarter = 2
        # currentMonth = Apr
        nextQuarter = 3
        nextMonth = 7
    if currentMonth >= 1 and currentMonth <= 3:
        currentQuarter = 1
        # currentMonth = jan
        nextQuarter = 2
        nextMonth = 4

    jack_data = dal.jackpot_data.find_one({'status':True})
    if jack_data:
        current_quarter = jack_data['current_quarter']
    else:
        current_quarter = 0
    
    if current_quarter != currentQuarter:
        user_data = dal.sbn_users.find_one({'username':uxr})
        email_address = user_data['email_address']
        
        try:
            dal.jackpot_data.delete_many({})
            dal.jackpot_history.update_many({'status':{'$eq':True}},{'$set':{'status':False}})
            dal.jackpot_data.insert_one({'createdDate':datetime.now().replace(microsecond=0),'current_quarter':currentQuarter,'username':uxr,'email_address':email_address,'package_id':pkg,'amount':float(amt),'status':True})
            dal.jackpot_history.insert_one({'createdDate':datetime.now().replace(microsecond=0),'current_quarter':currentQuarter,'username':uxr,'email_address':email_address,'package_id':pkg,'amount':float(amt),'status':True})
            dal.sbn_users.update_one({'username':uxr},{'$set':{'jackpot_reward':float(amt)}})
            display = True

        except Exception as e:
            flash(e,"error")
            flash("Something went wrong!","error")    
    else:
        flash("Jackpot already registerd for this quarter!","error")
    return display

# @login_manager.user_loader
def load_user(email):
    #return User.get(username)
    #return dal.sbn_users.find_one({'email_address':user_id})
    return getMember_email(email)


@app.route("/launch_config", methods=['GET'])
def launch_config():
    generateAdminAccount()
    generatePackages()
    generateRewards()
    generateWallet()

    return redirect(url_for('login'))

@app.route('/')
@app.route("/index", methods=['GET'])
def index():
    # generateAdminAccount()
    sbnusers = dal.sbn_users.find_one({'username':'hayyan'})
    return render_template('/index.html', title='SBN is coming!', sbnusers = sbnusers)


@app.route('/signup/', methods=['GET','POST'])
def signup():
    form = RegistrationForm()
    if request.method == "POST":
        
        if form.signup.data:
            if form.validate_on_submit():
                txtReferralCode = datetime.utcnow().strftime('%H%M%S%f')[:-3]
                # dal.sbn_users.insert_one({'username':"admin",'email_address':"admin@sbn.com",'full_name':"Administrator",'password':"admin123",'is_admin':'true','created_date':datetime.now().replace(microsecond=0),'is_active':'true'})
                # dal.sbn_users.insert_one({'username':"hayyan",'email_address':"fagholic@gmail.com",'full_name':"hayyan mustafa",'password':"abc@1234",'country':"Pakistan",'mobile':"null",'id_passport':"null",'referral_link':"null",'referral_code':txtReferralCode,'is_admin':'true','is_terms':'true','created_date':datetime.now().replace(microsecond=0),'is_approved':'false','is_active':'false','withdraw_wallet':0,'weekly_reward':0,'monthly_reward':0, 'jackpot_reward':0,'direct_reward':0})
                users_find = dal.sbn_users.find_one({'username':form.username.data})
                if users_find:
                    flash("Username "+form.username.data+" already exists please try another","error")
                    return render_template('/auth/signup.html', title='Sign Up User', form=form)
                else:
                    txtUsername = form.username.data
                    txtEmail = form.email_address.data
                    txtFullname = form.full_name.data
                    txtCountry = form.country.data
                    txtMobile = form.mobile.data
                    txtReferralLink = form.referral_link.data
                    txtReferralCode = datetime.utcnow().strftime('%H%M%S%f')[:-3]
                    # flash(txtReferralCode,"success")
                    txtPassword = form.password.data
                    bytePwd = txtPassword.encode('utf-8')
                    mysalt = bcrypt.gensalt()
                    hashPassword = bcrypt.hashpw(bytePwd,mysalt)
                    # if bcrypt.checkpw(txtPassword,hashPassword) - (input,dbpwd)
                    txtCreatedDate = datetime.now().replace(microsecond=0)
                    txtIsTerms = form.is_terms.data
                    
                    addMemberAccount(txtUsername,txtEmail,txtFullname,txtCountry,txtMobile,txtReferralLink,txtReferralCode,hashPassword,txtCreatedDate,txtIsTerms)
                    flash("Sign Up Successfull!","success")
            else:
                flash(form.errors,"error")

    return render_template('/auth/signup.html', title='Sign Up User', form=form)

@app.route('/dashboard/')
def dashboard():
    if "username" in session:
        if session['is_admin'] == False and session['is_approved'] == True :
            return render_template('dashboard.html', title='User Dashboard')

    return redirect(url_for('logout'))

@app.route('/admin_panel/')
#@login_required
def admin_panel():
    if session.get('is_admin') == True and session.get('is_approved') == True:
        return redirect(url_for('admin_add'))
   
    return redirect(url_for('logout'))



# ********** MEMBER MANAGER START***********

@app.route('/member_all/', methods=['GET'])
def member_all():
    form = MemberManager()
    member_data = getall_members()
    return render_template('/adminpanel/member_all.html', title='Member Accounts', member_data=member_data, form=form)


@app.route('/member_manager/<todo>', methods=['GET','POST'])
def member_manager(todo):
    todo = todo
    form = MemberManager()
    txtTitle = 'Manage Members'
    if todo == 'approval':
        form.submit.label.text = 'Approve'
        txtMsg = 'Please load the desired member account for approval!'
        txtTitle = 'Member Approvals'
    elif todo == 'activation':
        form.submit.label.text = 'Activate'
        txtMsg = 'Please load the desired member account for activation!'
        txtTitle = 'Member Activation'
    elif todo == 'disapproval':
        form.submit.label.text = 'Disapprove'
        txtMsg = 'Please load the desired member account for disapproval!'
        txtTitle = 'Member Disapprovals'
    elif todo == 'deactivation':
        form.submit.label.text = 'Deactivate'
        txtMsg = 'Please load the desired member account for deactivation!'
        txtTitle = 'Member Deactivation'
        
    if request.method == "POST":
        if form.validate_on_submit():
            if form.submit.data:
                if form.member_hidden.data:
                    pass
                else:
                    flash(txtMsg,"error")
                    flushMemberManager()

    member_data = get_memberManager(todo)
    return render_template('/adminpanel/member_manager.html', title=txtTitle, todo = todo, member_data=member_data, form=form)


@app.route('/member_load/<uxr>', methods=['GET','POST'])
def member_load(uxr):
    uxr = uxr
    todo = request.args.get('status')
    txtTitle = 'Manage Members'
    form = MemberManager()

    if todo == 'approval':
        form.submit.label.text = 'Approve'
        txtTitle = 'Member Approvals'
    if todo == 'activation':
        form.submit.label.text = 'Activate'
        txtTitle = 'Member Activation'
    if todo == 'disapproval':
        form.submit.label.text = 'Disapprove'
        txtTitle = 'Member Disapprovals'
    if todo == 'deactivation':
        form.submit.label.text = 'Deactivate'
        txtTitle = 'Member Deactivation'


    if form.username.data == session.get('username'):
        flash("Self accounts can not be entertained","error")
        form.submit.render_kw = {'disabled':'disabled'}

    # find_member = getMember_username(uxr)
    find_member = getMember_Id(uxr)
    if find_member:
        form.member_hidden.data = find_member['username']
        form.username.data = form.member_hidden.data
        form.email_address.data = find_member['email_address']
        form.full_name.data = find_member['full_name']
        
        form.username.render_kw = {'disabled': 'disabled'}
        form.email_address.render_kw = {'disabled': 'disabled'}
        form.full_name.render_kw = {'disabled': 'disabled'}

    if request.method == "POST":
        if form.validate_on_submit():
            if form.submit.data:
                if form.submit.label.text == "Approve":
                    approveMemberAccount(form.username.data,True)
                    flash("Member account has been approved for login","success")
                    flushMemberManager()
                if form.submit.label.text == "Activate":
                    activeMemberAccount(form.username.data,True)
                    flash("Member account has been activated for earning","success")
                    flushMemberManager()
                if form.submit.label.text == "Disapprove":
                    approveMemberAccount(form.username.data,False)
                    flash("Member account has been disapproved for login","success")
                    flushMemberManager()
                if form.submit.label.text == "Deactivate":
                    activeMemberAccount(form.username.data,False)
                    flash("Member account has been deactivated for earning","success")
                    flushMemberManager()    
        else:
            flash(form.errors,"error")
    
    
    mems = get_memberManager(todo)
    return render_template('/adminpanel/member_manager.html', title=txtTitle, member_data=mems, form=form)

# ********** MEMBER MANAGER END***********

# ********** ANNOUNCEMENT START***********

@app.route('/announcements/', methods=['GET','POST'])
def announcements():
    form = AnnouncementsForm()
    txtTitle = 'Announcement'
    if request.method == "POST":
        if form.validate_on_submit():
            if form.submit.data:
                txtTitle = 'Add Announcement'
                addAnnouncement(form.announcement.data,form.isactive.data)
                flash("Announcement Added Successfully!","success")
                form.announcement.data = ''
                form.isactive.data = False
        else:
            flash(form.errors,"error")


    ann_data = get_announcements()
    return render_template('/adminpanel/announcements.html', title=txtTitle, ann_data=ann_data, form=form)


@app.route('/announcement_load/<ob>', methods=['GET','POST'])
def announcement_load(ob):
    form = AnnouncementsForm()
    txtTitle = 'Announcement'
    ob = ob

    if request.method == "POST":
        if form.submit.data:
            if form.validate_on_submit():
                txtTitle = 'Update Announcement'
                updateAnnouncement(ob,form.announcement.data,form.isactive.data)
                flash("Announcement updated","success")
                form.announcement.data = ''
                form.isactive.data = False
            else:
                flash(form.errors,"error")

    find_anna = get_announcement(ob)
    if find_anna:
        form.submit.label.text = "Impact"
        txtTitle = 'Update Announcement'
        form.anna_hidden.data = find_anna['announcement']
        form.announcement.data = form.anna_hidden.data
        form.isactive.data = find_anna['isactive']

    ann_data = get_announcements()
    return render_template('/adminpanel/announcements.html', title=txtTitle, ann_data=ann_data, form=form)
    

# ********** ANNOUNCEMENT END***********




# ********** PACKAGE START***********
@app.route('/package_config/', methods=['GET','POST'])
def package_config():
    form = PackageConfigForm()
    if request.method == "POST":
        if form.validate_on_submit():
        # if request.form["btn_submit"] == "add_package":
            if form.submit.data:
                pkg = form.package.data
                pkg_id = 'pkg'+str(pkg)
                # pkg_date = datetime.now()
                # pkg_date = pkg_date.strftime("%x %X")
                pkg_date = datetime.now().replace(microsecond=0)
                if pkg != "" and pkg_id != "":
                    pkg_find = dal.sbn_packages.find_one({'package_id':pkg_id})
                    if pkg_find:
                        flash("Package already exists "+pkg_id,"error")
                        
                    else:
                        dal.sbn_packages.insert_one({'package': pkg, 'package_id': pkg_id, 'package_date':pkg_date})
                        flash("Package added "+pkg_id, "success")
                else:
                    flash("Please enter package","error")
            
    pkg_sbn = dal.sbn_packages.find()
    return render_template('/adminpanel/config/package_config.html', title='Package Config', pkg_sbn=pkg_sbn, form=form)

@app.route('/package_delete/<id>', methods=['POST'])
def package_delete(id):
    dal.sbn_packages.find_one_and_delete({'package_id':id})
    flash("Package deleted "+id,"success")
    # form = PackageConfigForm()
    # pkg_sbn = dal.sbn_packages.find()
    # return render_template('/adminpanel/config/package_config.html', title='Package Config', pkg_sbn=pkg_sbn, form=form) 
    return redirect("/package_config/")

# ********** PACKAGE END***********

# ********** REWARD START***********

@app.route('/reward_config/', methods=['GET','POST'])
def reward_config():
    form = RewardConfigForm()

    if request.method == "POST":
        if form.validate_on_submit():
            if form.submit.data:
                if form.reward_hidden.data:
                    pass
                else:
                    flash("Please load the desired reward to update!","error")
                    # form.reward.label.text = 'Reward Type'
                    form.percentage.data = ''

    reward_weekly = dal.reward_config.find_one({'reward':'Weekly'})
    reward_monthly = dal.reward_config.find_one({'reward':'Monthly'})
    reward_member = dal.reward_config.find_one({'reward':'Member'})
    return render_template('/adminpanel/config/reward_config.html', title='Reward Config', reward_weekly = reward_weekly, reward_monthly=reward_monthly, reward_member = reward_member, form=form)


@app.route('/reward_load/<reward>', methods=['GET','POST'])
def reward_load(reward):
    form = RewardConfigForm()
    reward = reward
    if request.method == "POST":
        if form.validate_on_submit():
            if form.submit.data:
                dal.reward_config.find_one_and_update({'reward':reward},{'$set':{'percentage':form.percentage.data,'updatedDate':datetime.now().replace(microsecond=0)}})
                flash("Reward updated "+reward,"success")
                form.percentage.data = ''
    
    find_reward = dal.reward_config.find_one({'reward':reward})
    if find_reward:
        form.reward_hidden.data = find_reward['reward']
        form.reward.label.text = form.reward_hidden.data
        form.percentage.data = find_reward['percentage']
         
        
    
    reward_weekly = dal.reward_config.find_one({'reward':'Weekly'})
    reward_monthly = dal.reward_config.find_one({'reward':'Monthly'})
    reward_member = dal.reward_config.find_one({'reward':'Member'})
    return render_template('/adminpanel/config/reward_config.html', title='Reward Config', reward_weekly = reward_weekly, reward_monthly=reward_monthly, reward_member = reward_member, form=form)
    

# ********** REWARD END***********

# ********** WALLET START***********
@app.route('/wallet_config/', methods=['GET','POST'])
def wallet_config():
    form = WalletConfigForm()
    
    if request.method == "POST":
        if form.validate_on_submit():
            if form.submit.data:
                if form.wallet_hidden.data:
                    pass
                else:
                    flash("Please load the wallet to update!","error")
                    form.sbn_wallet.data = ''
            
    sbn_wallet = dal.sbn_wallet.find()
    return render_template('/adminpanel/config/wallet_config.html', title='Wallet Config', sbn_wallet = sbn_wallet, form=form)

@app.route('/wallet_load/<wallet>', methods=['GET','POST'])
def wallet_load(wallet):
    form = WalletConfigForm()
    wallet = wallet
    if request.method == "POST":
        if form.validate_on_submit():
            if form.submit.data:
                dal.sbn_wallet.find_one_and_update({'wallet':wallet},{'$set':{'wallet':form.sbn_wallet.data,'updatedDate':datetime.now().replace(microsecond=0)}})
                flash("Wallet updated "+form.sbn_wallet.data,"success")
    
    find_wallet = dal.sbn_wallet.find_one({'wallet':wallet})
    if find_wallet:
        form.wallet_hidden.data = find_wallet['wallet']
        form.sbn_wallet.data = form.wallet_hidden.data
    
    sbn_wallet = dal.sbn_wallet.find()
    return render_template('/adminpanel/config/wallet_config.html', title='Wallet Config', sbn_wallet = sbn_wallet, form=form)
    

# ********** WALLET END***********


@app.route('/weekly_reward/', methods=['GET','POST'])
def weekly_reward():
    form = WeeklyRewardForm()
    sbn_members = get_activeMembers(None)
    reward_weekly = dal.reward_config.find_one({'reward':'Weekly'})
    if reward_weekly:
        form.percentage.data = reward_weekly['percentage']

    display = None
    if request.method == "POST":
        if form.validate_on_submit():
            if form.submit.data:
                display = reg_weekly(sbn_members,form.percentage.data)

    if display == True:            
        flash("Weekly reward has been registered for all users!","success")

    sbn_members = get_activeMembers(None)
    return render_template('/adminpanel/dashboard/weekly_rewards.html', title='Weekly Rewards', sbn_members=sbn_members, form=form)

@app.route('/monthly_reward/', methods=['GET','POST'])
def monthly_reward():
    form = MonthlyRewardForm()
    # form.submit.render_kw = {'disabled':'disabled'}
    form.load.render_kw = {'disabled':'disabled'}
    pkg = request.args.get("pack")
    if pkg:
        form.load.render_kw = {'enabled':'enabled'}
    
    reward_monthly = dal.reward_config.find_one({'reward':'Monthly'})
    if reward_monthly:
        form.percentage.data = reward_monthly['percentage']


    sbn_members = get_activeMembers(pkg)
    sbn_packages = dal.sbn_packages.find()
    return render_template('/adminpanel/dashboard/monthly_rewards.html', title='Monthly Rewards',pkg=pkg, sbn_members=sbn_members, sbn_packages=sbn_packages, form=form)

@app.route('/direct_reward/', methods=['GET','POST'])
def direct_reward():
    reg_form = RegistrationForm()
    reward_form = RewardConfigForm()
    return render_template('/adminpanel/dashboard/direct_rewards.html', title='Direct Rewards', reg_form=reg_form, reward_form=reward_form)

@app.route('/jackpot/', methods=['GET','POST'])
def jackpot():
    form = JackpotForm()
    form.submit.render_kw = {'disabled':'disabled'}
    form.load.render_kw = {'disabled':'disabled'}
    pkg = request.args.get("pack")
    if pkg:
        form.load.render_kw = {'enabled':'enabled'}
    sbn_members = get_activeMembers(pkg)
    sbn_packages = dal.sbn_packages.find()

    return render_template('/adminpanel/dashboard/jackpot.html', title='Jackpot',pkg=pkg, sbn_members=sbn_members,sbn_packages=sbn_packages, form=form)

@app.route('/jackpot_load/<uxr>', methods=['GET','POST'])
def jackpot_load(uxr):

    form = JackpotForm()
    form.submit.render_kw = {'enabled':'enabled'}
    pkg = request.args.get('pack')
    form.username.label.text = str(uxr)
    form.username.data = str(uxr)
    if pkg:
        form.pkg_amount.label.text = pkg[3:]
        form.pkg_amount.data = pkg[3:]

    if request.method == "POST":
        if form.validate_on_submit():
            if form.submit.data:
                if form.username.data:
                    pass
                else:    
                    flash("Please load the desired member","error")
                if form.pkg_amount.data:
                    pass
                else:
                    flash("Please select the package","error")
                if form.multiplier.data:
                    jack_amount = float(form.multiplier.data)*int(form.pkg_amount.data)
                    display = reg_jackpot(uxr,pkg,jack_amount)
                    if display == True:
                        flash("Jackpot successfully registered against "+uxr,"success")
                else:
                    flash("Please enter no. of terms","error")
                

    sbn_members = get_activeMembers(pkg)
    sbn_packages = dal.sbn_packages.find()

    return render_template('/adminpanel/dashboard/jackpot.html', title='Jackpot', sbn_members=sbn_members,sbn_packages=sbn_packages, form=form)


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

if __name__ == '__main__':
    app.run(debug=True)



