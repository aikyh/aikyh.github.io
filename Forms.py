from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators, PasswordField, IntegerField
from wtforms.fields import EmailField, DateField


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