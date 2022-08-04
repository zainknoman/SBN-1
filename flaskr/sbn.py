from flask import Flask, render_template, url_for, request, flash, redirect, session
from forms import (RegistrationForm, LoginForm, ForgotPwdForm, ForgotUsrForm, ProfileForm, 
    AnnouncementsForm, PackageConfigForm, RewardConfigForm, WalletConfigForm, WeeklyRewardForm,
    MemberManager, AdminManager, AdminUsers)
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

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message_category = "info"
login_manager.login_message = "Please login to access the page"

def generateAdminAccount():
    txtPassword = "admin@1234"
    bytePwd = txtPassword.encode('utf-8')
    mysalt = bcrypt.gensalt()
    hashPassword = bcrypt.hashpw(bytePwd,mysalt)
    dal.sbn_users.insert_one({'username':"admin",'email_address':"admin@sbn.com",'full_name':"Administrator",'password':hashPassword,'is_admin':True,'created_date':datetime.now().replace(microsecond=0),'updated_date':datetime.now().replace(microsecond=0),'is_approved':True,'is_active':None})

def get_admins(approve):
    # sbn_data = dal.sbn_users.find({'$and':[{'is_admin':{'$eq':True}},{'is_approved':{'$eq':approve}}]})
    sbn_data = dal.sbn_users.find({'is_admin':True,'is_approved':approve})
    return sbn_data 

def getall_admins():
    sbn_data = dal.sbn_users.find({'is_admin':True})
    return sbn_data

def getall_members():
    sbn_data = dal.sbn_users.find({'is_admin':False})
    return sbn_data

def addAdminAccount(txtUsername,txtEmail,txtFullname,txtPassword):
    bytePwd = txtPassword.encode('utf-8')
    mysalt = bcrypt.gensalt()
    hashPassword = bcrypt.hashpw(bytePwd,mysalt)
    dal.sbn_users.insert_one({'username':txtUsername,'email_address':txtEmail,'full_name':txtFullname,'password':hashPassword,'is_admin':True,'created_date':datetime.now().replace(microsecond=0),'updated_date':None,'is_approved':False,'is_active':None})

def addMemberAccount(txtUsername,txtEmail,txtFullname,txtCountry,txtMobile,txtReferralLink,txtReferralCode,hashPassword,txtCreatedDate,txtIsTerms):
    dal.sbn_users.insert_one({'username':txtUsername,'email_address':txtEmail,'full_name':txtFullname,'password':hashPassword,'country':txtCountry,'mobile':txtMobile,'id_passport':None,'referral_link':txtReferralLink,'referral_code':txtReferralCode,'is_admin':False,'is_terms':txtIsTerms,'created_date':txtCreatedDate,'updated_date':None,'active_date':None,'is_approved':False,'is_active':False,'withdraw_wallet':0,'weekly_reward':0,'monthly_reward':0, 'jackpot_reward':0,'direct_reward':0})

def approveAdminAccount(uxr,approve):
    dal.sbn_users.find_one_and_update({'username':uxr},{'$set':{'is_approved':approve, 'updated_date':datetime.now().replace(microsecond=0)}})

# def getUsers():
#     sbn_users = dal.sbn_users.aggregate([{'$lookup':{'from':'user_package','localField':'username','foreignField':'username','as':'packages'}}])
#     return sbn_users

def get_memberManager(todo):
    if todo == 'approval':
        sbn_data = dal.sbn_users.find({'$and':[{'is_admin':{'$eq':False}},{'is_approved':{'$eq':False}}]})
    elif todo == 'activation':
        sbn_data = dal.sbn_users.find({'$and':[{'is_admin':{'$eq':False}},{'is_active':{'$eq':False}}]})
    return sbn_data 

def get_approvedMembers():
    sbn_data = dal.sbn_users.find({'$and':[{'is_admin':{'$eq':False}},{'is_approved':{'$eq':True}}]})
    return sbn_data

def get_activeMembers():
    sbn_data = dal.sbn_users.find({'$and':[{'is_admin':{'$eq':False}},{'is_active':{'$eq':True}}]})
    return sbn_data
    

# def get_inactive_member():
#     sbn_data = dal.sbn_users.find({'$and':[{'is_admin':{'$eq':False}},{'is_active':{'$eq':False}}]})
#     return sbn_data

def approveMemberAccount(uxr,approve):
    dal.sbn_users.find_one_and_update({'username':uxr},{'$set':{'is_approved':approve, 'updated_date':datetime.now().replace(microsecond=0)}})

def activeMemberAccount(uxr,active):
    dal.sbn_users.find_one_and_update({'username':uxr},{'$set':{'is_active':active, 'active_date':datetime.now().replace(microsecond=0)}})


def flushAdminUsers():
    form = AdminUsers()
    form.username.data = None
    form.full_name.data = None
    form.email_address.data = None
    form.password.data = None
    return

def flushAdminManager():
    form = AdminManager()
    form.username.data = None
    form.full_name.data = None
    form.email_address.data = None
    return

def flushMemberManager():
    form = MemberManager()
    form.username.data = None
    form.full_name.data = None
    form.email_address.data = None
    return

def killSession():
    session['username'] = None
    session['full_name'] = None
    session['is_admin'] = None
    session['is_approved'] = None
    session['is_active'] = None
    session.clear()
    
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

def getLogin_email(user_email):
    user = dal.sbn_users.find_one({'email_address':user_email})
    return user

def getLogin_username(username):
    user = dal.sbn_users.find_one({'username':username})
    return user

def getMember_email(user_email):
    user = dal.sbn_users.find_one({'email_address':user_email, 'is_admin':False})
    return user

def getAdmin_email(user_email):
    user = dal.sbn_users.find_one({'email_address':user_email, 'is_admin':True})
    return user

def getMember_username(username):
    user = dal.sbn_users.find_one({'username':username, 'is_admin':False})
    return user

def getAdmin_username(username):
    user = dal.sbn_users.find_one({'username':username, 'is_admin':True})
    return user

@login_manager.user_loader
def load_user(email):
    #return User.get(username)
    #return dal.sbn_users.find_one({'email_address':user_id})
    return getMember_email(email)

@app.route('/')
@app.route("/index", methods=['GET'])
def index():
    # generateAdminAccount()
    sbnusers = dal.sbn_users.find_one({'username':'hayyan'})
    return render_template('/index.html', title='SBN is coming!', sbnusers = sbnusers)

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
                # mysalt = bcrypt.gensalt()
                # hashPassword = bcrypt.hashpw(bytePwd,mysalt)
                users_find = getLogin_username(form.username.data)#load_user(form.email_address.data)#dal.sbn_users.find_one({'email_address':form.email_address.data})
                if users_find:
                    hashPassword = users_find['password']

                    if bcrypt.checkpw(bytePwd, hashPassword):
                        session['username']=users_find['username']
                        session['full_name']=users_find['full_name']
                        session['is_admin']=users_find['is_admin']
                        session['is_approved']=users_find['is_approved']
                        session['is_active']=users_find['is_active']
                        #login_user(users_find)
                        #next = flask.request.args.get('next')
                        #current_user.is_active()
                        # is_safe_url should check if the url is safe for redirects.
                        # See http://flask.pocoo.org/snippets/62/ for an example.
                        # if not is_safe_url(next):
                        #     return flask.abort(400)

                        if users_find['is_approved'] == False:
                            flash("Administrator has not approved your account yet, kindly wait 24 hrs you will be notified by email","error")
                            return render_template('/auth/login.html', title='Login User', form=form )
                        if users_find['is_admin'] == True:
                            
                            #return render_template('/adminpanel/users_activation.html', title='Admin Dashboard', users_find=users_find, reg_form=reg_form)
                            #return redirect(next or url_for('/admin_panel'))
                            return redirect(url_for('admin_panel'))
                        else:
                            #return redirect(next or url_for('/mydashboard'))
                            return redirect(url_for('dashboard'))
                    else:
                        flash("Incorrect Password","error")
                else:
                    flash("User does not exist!","error")

    return render_template('/auth/login.html', title='Login User', form=form )

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


@app.route('/dashboard/')
def dashboard():
    if "username" in session:
        if session['is_admin'] == False and session['is_approved'] == True :
            return render_template('dashboard.html', title='User Dashboard')

    return redirect(url_for('logout'))

@app.route('/admin_panel/')
#@login_required
def admin_panel():
    # if "username" in session:
    if session['is_admin'] == True and session['is_approved'] == True:
        # form = UserActivation()
        # return render_template('/adminpanel/users_activation.html', title='Admin Dashboard', form=form)
        return redirect(url_for('admin_add'))
   
    return redirect(url_for('logout'))

# ********** ADMIN MANAGER START***********

@app.route('/admin_add/', methods=['GET','POST'])
def admin_add():
    if session.get('is_admin') == None or session.get('is_admin') == False or session.get('is_approved') == False:
        return redirect(url_for('logout'))
    form = AdminUsers()
    if request.method == "POST":
        if form.validate_on_submit():
                
            if form.email_address.data:
                find = getAdmin_email(form.email_address.data)
                if find:
                    flash("Email already registered with our system","error")
                    
            if form.username.data:
                find = getAdmin_username(form.username.data)
                if find:
                    flash("Username aleady registered with our system","error")
                    
            if find is None:
                addAdminAccount(form.username.data,form.email_address.data,form.full_name.data,form.password.data)
                flash("Admin account added successfully!","success")
                flushAdminUsers()

    admin_data = getall_admins()

    return render_template('/adminpanel/admin_add.html', title='Add Admin', admin_data=admin_data, form=form)

@app.route('/admin_manager/<todo>', methods=['GET','POST'])
def admin_manager(todo):
    todo = todo
    form = AdminManager()
    if todo == 'approval':
        form.submit.label.text = 'Approve'
        act = False
    elif todo == 'disapproval':
        form.submit.label.text = 'Disapprove'
        act = True    
    
    # form.submit.label.text = 'Approve'
    if request.method == "POST":
        if form.validate_on_submit():
            if form.submit.data:
                if form.approve_hidden.data:
                    pass
                else:
                    flash("Please load the desired admin user for approval!","error")
                    flushAdminManager()

    admin_data = get_admins(act)
    return render_template('/adminpanel/admin_manager.html', title='Manage Admins', admin_data=admin_data, form=form)

@app.route('/admin_load/<uxr>', methods=['GET','POST'])
def admin_load(uxr):
    uxr = uxr
    act = request.args.get('act')
    txtTitle = 'Manage Admins'
    
    form = AdminManager()

    if eval(act) == True:
        form.submit.label.text = 'Disapprove'
        txtTitle = 'Manage Disapprovals'
    if eval(act) == False:
        form.submit.label.text = 'Approve'
        txtTitle = 'Manage Approvals'
    
    if uxr == session.get('username'):
        flash("Self accounts can not be entertained","error")
        form.submit.render_kw = {'disabled':'disabled'}

    find_admin = getAdmin_username(uxr)
    if find_admin:
        form.approve_hidden.data = find_admin['username']
        form.username.data = form.approve_hidden.data
        form.email_address.data = find_admin['email_address']
        form.full_name.data = find_admin['full_name']
        
        form.username.render_kw = {'disabled': 'disabled'}
        form.email_address.render_kw = {'disabled': 'disabled'}
        form.full_name.render_kw = {'disabled': 'disabled'}

    if request.method == "POST":
        if form.validate_on_submit():
            if form.submit.data:
                if form.submit.label.text == "Approve":
                    approve = True
                    approveAdminAccount(form.username.data,approve)
                    flash("Admin account has been approved for login","success")
                    flushAdminManager()
                if form.submit.label.text == "Disapprove":
                    approve = False
                    approveAdminAccount(form.username.data,approve)
                    flash("Admin account has been disapproved for login","success")
                    flushAdminManager()
        else:
            flash(form.errors,"error")
    
    
    admins = get_admins(eval(act))
    return render_template('/adminpanel/admin_manager.html', title=txtTitle, admin_data=admins, form=form)
    
# ********** ADMIN MANAGER END***********

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
        
    if request.method == "POST":
        if form.validate_on_submit():
            if form.submit.data:
                if form.member_hidden.data:
                    pass
                else:
                    flash(txtMsg,"error")
                    flushMemberManager()

    member_data = get_memberManager(todo)
    return render_template('/adminpanel/member_manager.html', title=txtTitle, member_data=member_data, form=form)


@app.route('/member_load/<uxr>', methods=['GET','POST'])
def member_load(uxr):
    uxr = uxr
    act = request.args.get('act')
    sts = request.args.get('sts')
    txtTitle = 'Manage Members'
    todo = 'approval'
    form = MemberManager()

    
    if eval(sts) == False:
        form.submit.label.text = 'Activate'
        todo = 'activation'
        txtTitle = 'Member Activation'
    if eval(act) == False:
        form.submit.label.text = 'Approve'
        todo = 'approval'
        txtTitle = 'Member Approvals'


    if uxr == session.get('username'):
        flash("Self accounts can not be entertained","error")
        form.submit.render_kw = {'disabled':'disabled'}

    find_member = getMember_username(uxr)
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
        else:
            flash(form.errors,"error")
    
    
    mems = get_memberManager(todo)
    return render_template('/adminpanel/member_manager.html', title=txtTitle, member_data=mems, form=form)

# ********** MEMBER MANAGER END***********

# ********** ANNOUNCEMENT START***********

@app.route('/announcements/', methods=['GET','POST'])
def announcements():
    form = AnnouncementsForm()
    if request.method == "POST":
        if form.validate_on_submit():
            if form.submit.data:
                if form.submit.label.text == "Impact":
                    if form.anna_hidden.data:
                        pass
                    else:
                        flash("Please load the desired announcement to update!","error")
                        form.announcement.data = ''
                else:
                    if form.submit.label.text == "Add":
                        dal.sbn_announcements.insert_one({'announcement':form.announcement.data, 'isactive':form.isactive.data, 'createdDate':datetime.now().replace(microsecond=0)})
                        flash("Announcement Added Successfully!","success")
                        form.announcement.data = ''

    sbn_ann = dal.sbn_announcements.find()
    return render_template('/adminpanel/announcements.html', title='Announcements', sbn_ann=sbn_ann, form=form)


@app.route('/announcement_load/<id>', methods=['GET','POST'])
def announcement_load(id):
    form = AnnouncementsForm()
    id = id
    if request.method == "POST":
        if form.validate_on_submit():
            if form.submit.data:
                # flash(form.submit.label.text,"success")
                if form.submit.label.text == "Impact":
                    dal.sbn_announcements.find_one_and_update({'_id':ObjectId(id)},{'$set':{'announcement':form.announcement.data, 'isactive':form.isactive.data, 'createdDate':datetime.now().replace(microsecond=0)}})
                    flash("Announcement updated","success")
                    form.announcement.data = ''
    
    find_anna = dal.sbn_announcements.find_one({'_id':ObjectId(id)})
    if find_anna:
        form.submit.label.text = "Impact"
        form.anna_hidden.data = find_anna['announcement']
        form.announcement.data = form.anna_hidden.data
        form.isactive.data = find_anna['isactive']
    
    sbn_ann = dal.sbn_announcements.find()
    return render_template('/adminpanel/announcements.html', title='Announcements', sbn_ann=sbn_ann, form=form)
    

# ********** ANNOUNCEMENT END***********



@app.route('/member_approval/', methods=['GET','POST'])
def member_approval():
    form = MemberApproval()
    mem_data = get_unapproved_member()
    return render_template('/adminpanel/member_approval.html', title='Member Approval', form=form)

@app.route('/member_activation/', methods=['GET','POST'])
def member_activation():
    form = MemberActivation()
    mem_data = get_inactive_member()
    return render_template('/adminpanel/member_activation.html', title='Member Activation', form=form)

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
                dal.reward_config.find_one_and_update({'reward':reward},{'$set':{'percentage':form.percentage.data,'createdDate':datetime.now().replace(microsecond=0)}})
                flash("Reward updated "+reward,"success")
                form.percentage.data = ''
    
    find_reward = dal.reward_config.find_one({'reward':reward})
    if find_reward:
        db_reward = find_reward['reward']
        db_per = find_reward['percentage']
        form.reward_hidden.data = db_reward
        form.reward.label.text = form.reward_hidden.data
        form.percentage.data = db_per
        
    
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
                dal.sbn_wallet.find_one_and_update({'wallet':wallet},{'$set':{'wallet':form.sbn_wallet.data}})
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
    sbn_weekly = null#getUsers()
    reward_weekly = dal.reward_config.find_one({'reward':'Weekly'})
    form.percentage.data = reward_weekly['percentage']
    return render_template('/adminpanel/dashboard/weekly_rewards.html', title='Weekly Rewards', form=form, sbn_weekly=sbn_weekly)

@app.route('/monthly_reward/', methods=['GET','POST'])
def monthly_reward():
    form = RewardConfigForm()
    sbn_packages = dal.sbn_packages.find()
    sbn_monthly = null#getUsers()
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
    sbn_jackpot = null#getUsers()
    return render_template('/adminpanel/dashboard/jackpot.html', title='Jackpot', sbn_jackpot=sbn_jackpot, reg_form=reg_form)


if __name__ == '__main__':
    app.run(debug=True)


