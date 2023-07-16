from flask import Blueprint,render_template, request, flash, redirect, url_for
from modules.models import User, Brokerage
from werkzeug.security import generate_password_hash, check_password_hash 
from flask_login import login_user, login_required, logout_user, current_user
from . import db
import modules.robin_stocks_api as api
import robin_stocks.robinhood as r
import pyotp
##this file is the blueprint of our app

auth = Blueprint('auth',__name__) #set up blueprint for our application

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user= User.query.filter_by(username=username).first()

        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category ='success')
                login_user(user, remember=True)
                return redirect(url_for('auth.setup'))
            else:
                flash('Incorrect Password.', category='error')
        else:
            flash('Username does not exist', category='error')
    
    return render_template("login.html", user = current_user)



@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def signUp():
    if request.method =='POST':
        username = request.form.get('username')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(username=username).first()

        if user:
            flash('Username is taken', category ='error')
        elif password1 != password2:
            flash("Passwords dont match.", category="error")
        else:
            new_user = User(username = username, password = generate_password_hash(password1, method='sha256'),name = name )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember = True)
            flash('Account created!', category='success')
            return redirect(url_for('auth.setup'))
    
    return render_template("sign_up.html", user = current_user)

@auth.route('/setup', methods=['GET', 'POST'])
def setup():
    if request.method == 'POST':
        brokerage = request.form['brokerage']
        username = request.form['username']
        password = request.form['password']
        otp = request.form.get('otp')  # OTP is NOT optional
        try:
            if brokerage == 'brokerage1':
                api.login_to_robinhood(username, password, otp)
                return redirect(url_for('views.home'))
            elif brokerage == 'brokerage2':
                api.login_to_robinhood(username, password,otp)
                addBrokerage = Brokerage(username=username, password = password, otp = otp)
                db.session.add(addBrokerage)
                db.session.commit()
                flash('Brokerage Added!', category='success')
                return redirect(url_for('views.home'))
            else:
                raise ValueError("Invalid brokerage selected.")
               
        except Exception as e:
            flash(str(e), category='error')
            return redirect(url_for('auth.setup'))
    else:
        return render_template('setup.html',user = current_user)