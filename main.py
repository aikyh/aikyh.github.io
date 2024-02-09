from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import *
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import random
import string
import datetime
import json

main = Blueprint('main', __name__)


def get_user_id_by_email(email):
    user = User.query.filter_by(email=email).first()
    return user.id if user else None


def get_user_details_by_id(user_id):
    user = Details.query.filter_by(user_id=user_id).first()
    return user.id if user else None


# def get_donation_start_date():
#     # Assume you have a Donation record in the database
#     # with a field called 'start_date'
#     # Replace this with your actual database retrieval logic
#     return datetime(2023, 1, 1)  # Replace with the actual start date

@main.route('/')
def landingpage():
    return render_template("landingpage.html")


@main.route('/home')
def home():
    current_date = datetime.datetime.now().date()
    date_from_database = '2024-01-01'

    # if there is a getter setter method then
    # start_date_from_db = get_donation_start_date()
    # donation_instance = Donation(start_date_from_db)
    # return render_template('home.html', current_date=current_date)
    return render_template('home.html', date_from_database=date_from_database)


@main.route('/profile', methods=['POST', 'GET'])
@login_required
def profile():
    user_details = Details.query.filter_by(user_id=current_user.id).first()

    if request.method == 'POST':
        email = current_user.email
        user_id = int(get_user_id_by_email(email))
        dof_str = request.form.get('dof')
        contact = int(request.form.get('contact'))
        fulladd = request.form.get('fulladd')
        postal = int(request.form.get('postalcode'))
        street = request.form.get('street_name')
        lvl = int(request.form.get('lvlno'))
        unit_no = int(request.form.get('unit_no'))

        dof = datetime.datetime.strptime(dof_str, '%Y-%m-%d').date()

        if user_details:
            # If user details exist, update them
            user_details.dof = dof
            user_details.contact = contact
            user_details.fulladd = fulladd
            user_details.postal = postal
            user_details.streetname = street
            user_details.lvl = lvl
            user_details.unit = unit_no
        else:
            # If no user details exist, create a new entry
            user_details = Details(user_id=user_id,
                                   dof=dof,
                                   email=email,
                                   contact=contact,
                                   fulladd=fulladd,
                                   postal=postal,
                                   lvl=lvl,
                                   unit=unit_no,
                                   streetname=street)

            db.session.add(user_details)

        db.session.commit()

        return redirect(url_for('main.home'))

    return render_template('profile_page.html', first_name=current_user.first_name, mail=current_user.email,
                           user_details=user_details)


@main.route('/companydashboard', methods=['POST', 'GET'])
def company_dashboard():
    return render_template("companyhomepage.html")


@main.route('/retrieveUserJoinedEvent', methods=['POST', 'GET'])
def company_retrieve_event_details():
    return render_template("companyretrieveUserEvent.html")


@main.route("/usersignedup", methods=['POST', 'GET'])
def usersignedup():
    return render_template("usersignedup.html")


@main.route("/usersbought", methods=['GET', 'POST'])
def usersbought():
    return render_template("userbought.html")
