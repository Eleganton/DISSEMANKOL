from flask_sqlalchemy import SQLAlchemy
from database import db_connection

db = SQLAlchemy()

class User:
    def __init__(db.Model):
        self.id = id
        self.name = name
        self.major = major
        self.m_status = m_status
        self.money_spent = money_spent

def list_users():
    conn = db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, name, major, m_status, money_spent FROM categories')
    db_categories = cur.fetchall()

    categories = []
    for db_category in db_categories:
        categories.append(Category(db_category[0], db_category[1]))
    conn.close()
    return categories