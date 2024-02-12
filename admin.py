from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from Forms import CreateCompanyForm
from models import User, db, Admin, Details, Company
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

# Assuming Company is a class in your Company module

admin = Blueprint('admin', __name__)


@admin.route('/admin_home')
def homepage():
    return render_template('base2.html')


@admin.route('/createUser', methods=['GET', 'POST'])
def create_user():
    form = CreateCompanyForm(request.form)
    if request.method == 'POST' and form.validate():
        company_name = form.company_name.data
        email = form.email.data
        date_joined = form.date_joined.data
        address = form.address.data
        password = form.password.data

        if len(password) < 8:
            flash('Password needs to be more than 8 character', "danger")
            return redirect(url_for('admin.create_user'))
        else:

            new_company = Company(company_name=company_name, email=email, date_joined=date_joined,
                                  address=address, password=generate_password_hash(password))

            db.session.add(new_company)
            db.session.commit()
            return redirect(url_for("admin.retrieve_company"))

    return render_template("createUser.html", form=form)


@admin.route('/retrieveCompany')
def retrieve_company():
    companies = Company.query.all()
    return render_template('retrieveUsers.html', companies=companies)


@admin.route('/updateCompany/<int:id>/', methods=['GET', 'POST'])
def update_company(id):
    company = Company.query.get_or_404(id)
    update_company_form = CreateCompanyForm(request.form, obj=company)

    # Remove the password field from the form
    del update_company_form.password
    if request.method == 'POST' and update_company_form.validate():
        # Populate the object with form data excluding the password
        update_company_form.populate_obj(company)

        db.session.commit()

        return redirect(url_for("admin.retrieve_company"))

    return render_template("updateUser.html", form=update_company_form, company=company)


from sqlalchemy.orm.exc import NoResultFound


@admin.route('/deleteCompany/<int:company_id>', methods=['POST', 'GET'])
def deleteCompany(company_id):
    try:
        company = Company.query.filter_by(id=company_id).one()
        db.session.delete(company)
        db.session.commit()

    except NoResultFound:
        print(f"Company {company_id} not found.", "danger")

    return redirect(url_for("admin.retrieve_company"))
