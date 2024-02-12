from flask_login import UserMixin
from sqlalchemy import ForeignKey, Column, Date, create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
import bcrypt

DATABASE_URI = "sqlite:///database.db"
db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = Column(db.Integer, primary_key=True)
    email = Column(db.String(100), unique=True)
    password = Column(db.String(100))
    confirm_password = Column(db.String(100))
    first_name = Column(db.String(1000))
    last_name = Column(db.String(1000))
    details = relationship('Details', back_populates='user')


class Details(db.Model, UserMixin):
    __tablename__ = "details"

    id = Column(db.Integer, primary_key=True)
    user_id = Column(db.Integer, ForeignKey("user.id"))
    email = Column(db.String)
    dof = Column(db.Date)
    contact = Column(db.Integer)
    fulladd = Column(db.String(10000))
    postal = Column(db.Integer)
    streetname = Column(db.String(1000))
    lvl = Column(db.Integer)
    unit = Column(db.Integer)
    user = relationship('User', back_populates='details')


class Admin(db.Model, UserMixin):
    __tablename__ = "admin"
    admin_id = Column(db.Integer, primary_key=True)
    email = Column(db.String, unique=True)
    password = Column(db.String)


# models.py
class Company(db.Model, UserMixin):
    __tablename__ = "Company"
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(150), nullable=False)  # Add or update this line
    email = db.Column(db.String(150), nullable=False)
    date_joined = db.Column(db.Date)
    address = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(255), nullable=False)


class Registeredevent(db.Model, UserMixin):
    __tablename__ = "RegisteredEvent"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    contact_number = db.Column(db.Integer)
    number_of_people = db.Column(db.Integer)

