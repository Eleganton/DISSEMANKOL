from flask_sqlalchemy import SQLAlchemy
from database import db_connection
from extensions import db

class UserTable(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=True)
    password = db.Column(db.String(30), nullable=True)
    major = db.Column(db.String(80), nullable=True)
    money_spent = db.Column(db.Integer,nullable=True)
    beer_count = db.Column(db.Integer,nullable=True)

def drink_beer(uid):
    user = UserTable.query.get(uid)
    user.beer_count += 1
    db.session.commit()

