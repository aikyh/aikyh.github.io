from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators, PasswordField
from wtforms.fields import EmailField, DateField


class CreateCompanyForm(Form):
    company_name = StringField('Company Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = StringField('Email', [validators.Length(min=1, max=150), validators.DataRequired()])
    date_joined = DateField('Date Joined', format='%Y-%m-%d')
    address = StringField('Address', [validators.length(max=200), validators.DataRequired()])
    password = PasswordField('Password', [validators.Optional()])