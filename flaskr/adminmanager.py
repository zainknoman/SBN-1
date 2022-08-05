from __main__ import app
from flask import session, request, render_template, flash
from forms import AdminUsers, AdminManager
from dal import db
import bcrypt
from datetime import datetime
from bson.objectid import ObjectId

def getall_admins():
    sbn_data = db.connect.sbn_users.find({'is_admin':True})
    return sbn_data
def getAdmin_email(user_email):
    user = db.connect.sbn_users.find_one({'email_address':user_email, 'is_admin':True})
    return user
def getAdmin_username(username):
	user = db.connect.sbn_users.find_one({'username':username, 'is_admin':True})
	return user
def addAdminAccount(txtUsername,txtEmail,txtFullname,txtPassword):
    bytePwd = txtPassword.encode('utf-8')
    mysalt = bcrypt.gensalt()
    hashPassword = bcrypt.hashpw(bytePwd,mysalt)
    db.connect.sbn_users.insert_one({'username':txtUsername,'email_address':txtEmail,'full_name':txtFullname,'password':hashPassword,'is_admin':True,'created_date':datetime.now().replace(microsecond=0),'updated_date':None,'is_approved':False,'is_active':None})
def get_admins(approve):
    # sbn_data = dal.sbn_users.find({'$and':[{'is_admin':{'$eq':True}},{'is_approved':{'$eq':approve}}]})
    sbn_data = db.connect.sbn_users.find({'is_admin':True,'is_approved':approve})
    return sbn_data 
def getAdmin_Id(ob):
    user = db.connect.sbn_users.find_one({'_id':ObjectId(ob), 'is_admin':True})
    return user
def approveAdminAccount(uxr,approve):
    db.connect.sbn_users.find_one_and_update({'username':uxr},{'$set':{'is_approved':approve, 'updated_date':datetime.now().replace(microsecond=0)}})


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
    
    if form.username.data == session.get('username'):
        flash("Self accounts can not be entertained","error")
        form.submit.render_kw = {'disabled':'disabled'}

    # find_admin = getAdmin_username(uxr)
    find_admin = getAdmin_Id(uxr)
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