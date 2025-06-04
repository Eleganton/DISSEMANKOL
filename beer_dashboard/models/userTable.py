# models/user.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db

class UserTable(db.Model, UserMixin):
    uid             = db.Column(db.Integer, primary_key=True)
    username        = db.Column(db.String(30), unique=True, nullable=False)
    password_hash   = db.Column(db.String(256), nullable=False)
    major           = db.Column(db.String(80), nullable=True)
    money_spent     = db.Column(db.Float, default=0.0, nullable=False)
    beer_count      = db.Column(db.Integer, default=0, nullable=False)

    def set_password(self, raw_password: str):
        """Hashes `raw_password` and stores it."""
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password: str) -> bool:
        """Returns True if `raw_password` matches the stored hash."""
        return check_password_hash(self.password_hash, raw_password)
    
    def get_id(self) -> str:
        """Return the unique identifier for Flask-Login."""
        return str(self.uid)
