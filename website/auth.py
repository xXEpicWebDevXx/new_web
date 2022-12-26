from hashlib import sha256
from . import db
from flask_login import login_user,login_required,logout_user,current_user
from click import password_option
from flask import Blueprint, render_template, request, redirect, url_for
from .models import *
from werkzeug.security import generate_password_hash, check_password_hash
auth = Blueprint('auth', __name__)





@auth.route('/signUp',methods=['GET','POST'])
def SignUp(): #Signup
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        privs = 0
        if email == 'admin@admin':
            privs = 3
        new_user = User(email = email, password=generate_password_hash(password,method='sha256'),nick = name,privs = privs)
        print(new_user.id)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('views.home'))
        
    return render_template('accountCreation.html')

@auth.route('/logout',methods=['GET'])
@login_required
def Logout():
    logout_user()
    return redirect("/")

@auth.route('/Login',methods=['GET','POST'])
#@login_required
def login(): #Login 
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                print('Logged')
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
    

    return render_template('login.html')