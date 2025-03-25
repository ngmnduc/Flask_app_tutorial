from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime

class Note(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone = True), default= func.now())
    user_id= db.Column(db.Integer, db.ForeignKey('user.id'))


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    amount = db.Column(db.Float, nullable = True) # Bắt buộc phải cung cấp giá trị
    categories = db.Column(db.String(50), nullable = True)
    timestamp  = db.Column(db.Datetime(timezone = True), default = func.now ())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
    expense = db.relationship('Expense')