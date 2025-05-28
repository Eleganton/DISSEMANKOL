# app.py
import os
from flask import Flask, render_template, redirect, url_for
from extensions import db
from models.userTable import UserTable
from flask_login import LoginManager, login_user, login_required, current_user

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-key")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "SQLALCHEMY_DATABASE_URI",
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@"
        f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # init extensions
    db.init_app(app)
    login_manager = LoginManager(app)
    login_manager.login_view = "login"

    @login_manager.user_loader
    def load_user(user_id):
        return UserTable.query.get(int(user_id))

    # create tables + seed one user
    with app.app_context():
        db.create_all()
        if not UserTable.query.first():
            u = UserTable(username="MrMikPik", password="pik@example.com")
            u.set_password("pik@example.com")  # hash it
            db.session.add(u)
            db.session.commit()

    # a dummy login so we can get into the dashboard
    @app.route("/login")
    def login():
        u = UserTable.query.first()
        login_user(u)
        return redirect(url_for("profile"))

    # the dashboard
    @app.route("/")
    @login_required
    def profile():
        # current_user is your one user
        return render_template(
            "profile.html",
            username=current_user.username,
            beer_count=current_user.beer_count,
            money_spent=current_user.money_spent
        )

    # “drink” endpoint
    @app.route("/drink", methods=["POST"])
    @login_required
    def drink():
        current_user.beer_count  += 1
        current_user.money_spent += 15.0
        db.session.commit()
        return redirect(url_for("profile"))

    return app

app = create_app()

