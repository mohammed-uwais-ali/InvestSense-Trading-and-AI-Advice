from .import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Brokerage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(150))
    otp = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Float, nullable=False)
    percent_change = db.Column(db.Float, nullable=False)
    equity_change = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    pe_ratio = db.Column(db.Float, nullable=False)
    portfolio_percentage = db.Column(db.Float, nullable=False)
    average_buy_price = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#User will be stored in our database
class User(db.Model, UserMixin):
    #defining what we need to store in our layout
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(150))
    name = db.Column(db.String(150))
    brokerage = db.relationship('Brokerage')
    portfolio = db.relationship('Portfolio')