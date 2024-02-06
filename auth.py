
from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from models import User, db, Admin, Details
from werkzeug.security import generate_password_hash, check_password_hash
from bcrypt import *
from main import *

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    user_entered_password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    admin_email = "VegeGrove@admin"
    admin_password = "Vegegrove1234"

    user = db.session.query(User).filter_by(email=email).first()

    if user and check_password_hash(user.password, user_entered_password):
        login_user(user, remember=remember)
        flash('You have been logged in as a regular user.')
        return redirect(url_for('main.home'))

    # Check in the Company table
    company_user = db.session.query(Company).filter_by(email=email).first()

    if company_user and check_password_hash(company_user.password, user_entered_password):
        login_user(company_user, remember=remember)
        flash('You have been logged in as a company user.')
        return redirect(url_for('main.company_dashboard'))

    # Check in the Admin table

    if email == admin_email and user_entered_password == admin_password:
        flash('you have been logged in as admin')
        return redirect(url_for('admin.homepage'))


    # If none of the above matches, show an error message
    flash('Please check your login credentials and try again')
    return redirect(url_for('auth.login'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    user = db.session.query(User).filter_by(
        email=email).first()  # db.session.query this is used to directly create a query object

    if user:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    if len(password) < 8:
        flash('Password must be at least 8 characters long')
        return redirect(url_for('auth.signup'))

    if password != confirm_password:
        print('password does not match')
        flash('password does not match')
        return redirect(url_for('auth.signup'))

    new_user = User(email=email, first_name=first_name, last_name=last_name, password=generate_password_hash(password))

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))  # Correct usage


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.landingpage'))  # Correct usage


@auth.route('/changepassword', methods=['POST', 'GET'])
def userChangePassword():
    print("Reached userChangePassword route")
    user = User.query.filter_by(id=current_user.id).first()  # this uses User to directly create the query

    if request.method == 'POST':
        print("Entered POST condition")
        ori = request.form.get('ori')
        password = request.form.get('new')
        confirm_password = request.form.get('confirm_new')
        print(f"Original Password: {ori}")
        print(f"New Password: {password}")
        print(f"Confirm Password: {confirm_password}")
        user = User.query.filter_by(email=current_user.email).first()
        print(user)

        print(f"Original Password: {ori}")
        print(f"New Password: {password}")
        print(f"Confirm Password: {confirm_password}")
        if not user or not check_password_hash(user.password, ori):
            flash('Incorrect password entered for the original password')
            return redirect(url_for('auth.userChangePassword'))

        elif password != confirm_password:
            flash('Password does not match')
            return redirect(url_for('auth.userChangePassword'))

        elif len(password) < 8:
            flash('Password must be at least 8 characters long')
            return redirect(url_for('auth.userChangePassword'))

        else:
            # Update the password directly without hashing again
            user.password = generate_password_hash(password)
            db.session.commit()

            flash('You have successfully changed your password')
            return redirect(url_for('main.home'))

    return render_template('Changepassword.html', mail=current_user.email, id=current_user.id)


@auth.route('/forgetpassword', methods=['POST', 'GET'])
def forgetpassword():
    if request.method == 'POST':
        print(f' it has reached post mode')
        user_email = request.form.get('email')
        password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        user = User.query.filter_by(email=user_email).first()
        print(user_email)
        print(user)
        print(password)
        print(confirm_password)
        if user:
            print(f'User exists ')
            if password != confirm_password:
                print("Password does not match")
                flash("Password does not match")
                return redirect(url_for('auth.forgetpassword'))
            elif len(password) and len(confirm_password) < 8:
                print("Password must be more than 8 character")
                flash("Password must be more than 8 character")
                return redirect(url_for('auth.forgetpassword'))
            else:
                print(password)
                print(user.password)
                user.password = generate_password_hash(password)
                db.session.commit()
                print(user.password)
                return render_template('resetpwsuccessful.html')

        else:
            print("user does not exist")
            flash("user does not exists")
            return redirect(url_for('auth.signup'))

    return render_template('forgetpassword.html')
