from wtforms import (Form, StringField, RadioField, SelectField, TextAreaField, validators, PasswordField, IntegerField,
                     DateField, FloatField)
from wtforms.fields import EmailField, DateField
from wtforms.validators import DataRequired, Length


class CreateCompanyForm(Form):
    company_name = StringField('Company Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = StringField('Email', [validators.Length(min=1, max=150), validators.DataRequired()])
    date_joined = DateField('Date Joined', format='%Y-%m-%d')
    address = StringField('Address', [validators.length(max=200), validators.DataRequired()])
    password = PasswordField('Password', [validators.Optional()])


class CreateReviewForm(Form):
    customer_name = StringField('Customer Name', [validators.Length(min=1, max=150), validators.DataRequired(), validators.Regexp(r'^[A-Za-z ]*$', message="Please enter only letters.")])
    product_name = SelectField('Product Name', choices=[('', 'Select'), ('Tomato Seed', 'Tomato Seed'), ('Potato Seed', 'Potato Seed')], default='', validators=[validators.InputRequired()])
    rating = IntegerField('Rating', [validators.NumberRange(min=1, max=5), validators.DataRequired()])
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    review_date = DateField('Review Date', format='%Y-%m-%d')
    comments = TextAreaField('Comments', [validators.Length(min=1, max=500), validators.DataRequired()])


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