from wtforms import (Form, StringField, RadioField, SelectField, TextAreaField, validators, PasswordField, IntegerField,
                     FloatField)
from wtforms.fields import TimeField, IntegerField, EmailField, FileField, DateField
from wtforms.validators import DataRequired, Length, ValidationError
from flask_wtf.file import FileAllowed, FileRequired


class CreateCompanyForm(Form):
    company_name = StringField('Company Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = EmailField('Email', [validators.Length(min=1, max=150), validators.DataRequired()])
    date_joined = DateField('Date Joined', format='%Y-%m-%d')
    address = StringField('Address', [validators.length(max=200), validators.DataRequired()])
    password = PasswordField('Password', [validators.Optional()])


# Admin side (Events)
class CreateReviewForm(Form):
    customer_name = StringField('Customer Name', [validators.Length(min=1, max=150), validators.DataRequired(),
                                                  validators.Regexp(r'^[A-Za-z ]*$',
                                                                    message="Please enter only letters.")])
    product_name = SelectField('Product Name',
                               choices=[('', 'Select'), ('Tomato Seed', 'Tomato Seed'), ('Potato Seed', 'Potato Seed')],
                               default='', validators=[validators.InputRequired()])
    rating = IntegerField('Rating', [validators.NumberRange(min=1, max=5), validators.DataRequired()])
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    review_date = DateField('Review Date', format='%Y-%m-%d')
    comments = TextAreaField('Comments', [validators.Length(min=1, max=500), validators.DataRequired()])


# User side (Events)
class CheckInForm(Form):
    name = StringField('Name: ', [validators.DataRequired(message="Please enter your full name")],
                       render_kw={"placeholder": "Eg. Angeline Tan"})
    email = EmailField('Email: ', [validators.DataRequired(message="Please enter your email address")],
                       render_kw={"placeholder": "Eg. angelinetan123@gmail.com"})

class CreateReplyForm(Form):
    customer_name = StringField('Customer Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    product_name = SelectField('Product Name', choices=[('', 'Select'), ('Tomato Seed', 'Tomato Seed'),
                                                            ('Potato Seed', 'Potato Seed')], default='',
                                   validators=[validators.InputRequired()])
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    reply_date = DateField('Reply Date', format='%Y-%m-%d')
    comments = TextAreaField('Comments', [validators.Length(min=1, max=500), validators.DataRequired()])
    def validate_name(self, name):
        excluded_chars = "*?!'^+%&/()=}][{$#1234567890"
        for char in name.data:
            if char in excluded_chars:
                raise ValidationError('Name can only contain alphabets')

    def validate_email(self, email):
        excluded_chars = "*?!'^+%&/()={}[]$#"
        for char in email.data:
            if char in excluded_chars:
                raise ValidationError("Invalid Email")
class RegsisterForm(Form):
    name = StringField('Name: ', [validators.DataRequired(message="Please enter your full name")],
                       render_kw={"placeholder": "Eg. Angeline Tan"})
    email = EmailField('Email: ', [validators.DataRequired(message="Please enter your email address")],
                       render_kw={"placeholder": "Eg. angelinetan123@gmail.com"})


    def validate_name(self, name):
        excluded_chars = "*?!'^+%&/()=}][{$#1234567890"
        for char in name.data:
            if char in excluded_chars:
                raise ValidationError('Name can only contain alphabets')

    def validate_email(self, email):
        excluded_chars = "*?!'^+%&/()={}[]$#"
        for char in email.data:
            if char in excluded_chars:
                raise ValidationError("Invalid Email")

class CreateCheckoutForm(Form):
    amount = IntegerField('You are donating a total of', render_kw={"readonly": True})

    fname = StringField('First Name', [validators.DataRequired()])

    lname = StringField('Last Name', [validators.DataRequired()])

    phone = StringField('Phone Number', [validators.Length(min=8, max=8), DataRequired()],
                        render_kw={"placeholder": "8 Digit Phone Number"})

    email = EmailField('Email Address', [validators.DataRequired()], render_kw={"placeholder": "Example@gmail.com"})

    add1 = StringField('Address Line 1', [validators.DataRequired()],
                       render_kw={"placeholder": "Street"})

    add2 = StringField('Address Line 2', [validators.DataRequired()],
                       render_kw={"placeholder": "Block & Unit Number"})

    pcode = StringField('Postal Code', [validators.Length(min=6, max=6), DataRequired()],
                        render_kw={"placeholder": "6 Digit Postal Code"})

    dmethod = RadioField('Delivery Method', [validators.DataRequired()],
                         choices=[('S', 'Standard (2-8 Business days)'), ('E', 'Express (1 Business day)')],
                         default='Select')

    cname = StringField('Full Name on Card', [validators.DataRequired()])

    cnum = StringField('Card Number', [validators.Length(min=16, max=16), DataRequired()],
                       render_kw={"placeholder": "XXXX XXXX XXXX XXXX"})

    edate = DateField('Expiry Date', [validators.DataRequired()])

    cvc = StringField('CVC', [validators.Length(min=3, max=3), DataRequired()],
                      render_kw={"placeholder": "3 Digit CVC"})

class CreateCheckoutForm2(Form):
        amount = IntegerField('You are purchasing a total of', render_kw={"readonly": True})

        fname = StringField('First Name', [validators.DataRequired()])

        lname = StringField('Last Name', [validators.DataRequired()])

        phone = StringField('Phone Number', [validators.Length(min=8, max=8), DataRequired()],
                            render_kw={"placeholder": "8 Digit Phone Number"})

        email = EmailField('Email Address', [validators.DataRequired()], render_kw={"placeholder": "Example@gmail.com"})

        add1 = StringField('Address Line 1', [validators.DataRequired()],
                           render_kw={"placeholder": "Street"})

        add2 = StringField('Address Line 2', [validators.DataRequired()],
                           render_kw={"placeholder": "Block & Unit Number"})

        pcode = StringField('Postal Code', [validators.Length(min=6, max=6), DataRequired()],
                            render_kw={"placeholder": "6 Digit Postal Code"})

        dmethod = RadioField('Delivery Method', [validators.DataRequired()],
                             choices=[('S', 'Standard (2-8 Business days)'), ('E', 'Express (1 Business day)')],
                             default='Select')

        cname = StringField('Full Name on Card', [validators.DataRequired()])

        cnum = StringField('Card Number', [validators.Length(min=16, max=16), DataRequired()],
                           render_kw={"placeholder": "XXXX XXXX XXXX XXXX"})

        edate = DateField('Expiry Date', [validators.DataRequired()])

        cvc = StringField('CVC', [validators.Length(min=3, max=3), DataRequired()],
                          render_kw={"placeholder": "3 Digit CVC"})
class CreateUpdateForm2(Form):
            fname = StringField('First Name', [validators.DataRequired()])

            lname = StringField('Last Name', [validators.DataRequired()])

            phone = StringField('Phone Number', [validators.Length(min=8, max=8), DataRequired()],
                                render_kw={"placeholder": "8 Digit Phone Number"})

            email = EmailField('Email Address', [validators.DataRequired()],
                               render_kw={"placeholder": "Example@gmail.com"})

            add1 = StringField('Address Line 1', [validators.DataRequired()],
                               render_kw={"placeholder": "Street"})

            add2 = StringField('Address Line 2', [validators.DataRequired()],
                               render_kw={"placeholder": "Block & Unit Number"})

            pcode = StringField('Postal Code', [validators.Length(min=6, max=6), DataRequired()],
                                render_kw={"placeholder": "6 Digit Postal Code"})

            dmethod = RadioField('Delivery Method', [validators.DataRequired()],
                                 choices=[('S', 'Standard (2-8 Business days)'), ('E', 'Express (1 Business day)')],
                                 default='Select')


class CreateUpdateForm(Form):
    fname = StringField('First Name', [validators.DataRequired()])

    lname = StringField('Last Name', [validators.DataRequired()])

    phone = StringField('Phone Number', [validators.Length(min=8, max=8), DataRequired()],
                        render_kw={"placeholder": "8 Digit Phone Number"})

    email = EmailField('Email Address', [validators.DataRequired()], render_kw={"placeholder": "Example@gmail.com"})

    add1 = StringField('Address Line 1', [validators.DataRequired()],
                       render_kw={"placeholder": "Street"})

    add2 = StringField('Address Line 2', [validators.DataRequired()],
                       render_kw={"placeholder": "Block & Unit Number"})

    pcode = StringField('Postal Code', [validators.Length(min=6, max=6), DataRequired()],
                        render_kw={"placeholder": "6 Digit Postal Code"})

    dmethod = RadioField('Delivery Method', [validators.DataRequired()],
                         choices=[('S', 'Standard (2-8 Business days)'), ('E', 'Express (1 Business day)')],
                         default='Select')


class CreateProductForm(Form):
    name = StringField('Name', [validators.DataRequired()])

    price = FloatField('Price', [validators.DataRequired()])

    description = TextAreaField('Description', [validators.DataRequired()],
                                render_kw={"placeholder": "Describe the product..."})
    tags = RadioField('Type', [validators.DataRequired()], choices=[('S', 'Seed'), ('F', 'Fertiliser')],
                      default='Select')


class CreateEventForm(Form):
    name = StringField('Name: ', [validators.DataRequired()])
    timing = TimeField('Timing: ', [validators.DataRequired()])
    location = StringField('Location: ', [validators.DataRequired()])
    date = DateField('Date: ', [validators.DataRequired()])
    description = TextAreaField('Description: ', [validators.Optional()])
    person_in_charge = StringField("Person-In-Charge: ")
    budget = IntegerField("Budget($): ", [validators.NumberRange(min=0)])
    collaborators = StringField("Collaborators: ")
    photo = FileField("Upload Image: ", validators=[FileRequired(), FileAllowed(["jpg", "png", "jpeg"])])

    def validate_name(self, name):
        excluded_chars = "*?!'^+%&/()=}][{$#1234567890"
        for char in name.data:
            if char in excluded_chars:
                raise ValidationError('Event name can only contain alphabets')

    def validate_collaborators(self, collaborators):
        excluded_chars = "*?!'^+%&/()=}][{$#"
        for char in collaborators.data:
            if char in excluded_chars:
                raise ValidationError('Collaborators can only contain alphanumeric values')

    def validate_person_in_charge(self, person_in_charge):
        excluded_chars = "*?!'^+%&/()=}][{$#"
        for char in person_in_charge.data:
            if char in excluded_chars:
                raise ValidationError('Person-In-Charge must only contain alphanumeric values')
