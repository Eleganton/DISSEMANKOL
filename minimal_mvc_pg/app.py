import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from extensions import db
from models.userTable import UserTable
import re

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-key")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "SQLALCHEMY_DATABASE_URI",
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@"
        f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize extensions
    db.init_app(app)
    login_manager = LoginManager(app)
    login_manager.login_view = "login"
    login_manager.login_message_category = "info"

    @login_manager.user_loader
    def load_user(user_id):
        return UserTable.query.get(int(user_id))

    # Ensure database and seed
    with app.app_context():
        db.create_all()
        if not UserTable.query.first():
            u = UserTable(username="MrMikPik", major="DIS")
            u.set_password("pik@example.com")
            db.session.add(u)
            db.session.commit()

    # Signup route
    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'POST':
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '').strip()
            major    = request.form.get('major',    '').strip()

            # 1) Basic presence check
            if not username or not password or not major:
                flash('All fields are required.', 'danger')
                return render_template('signup.html')

            # 2) REGEX: only letters and digits
            if not re.fullmatch(r'[A-Za-z0-9]+', username):
                flash('Username may only contain letters and numbers.', 'danger')
                return render_template('signup.html')

            # 3) Uniqueness
            if UserTable.query.filter_by(username=username).first():
                flash('Username already taken.', 'warning')
                return render_template('signup.html')

            # 4) Create and log in
            user = UserTable(username=username, major=major)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash('Account created and logged in!', 'success')
            return redirect(url_for('profile'))

        return render_template('signup.html')

    # Login route
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('profile'))
        if request.method == 'POST':
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '').strip()
            user = UserTable.query.filter_by(username=username).first()
            if user and user.check_password(password):
                login_user(user)
                flash('Logged in successfully.', 'success')
                return redirect(url_for('profile'))
            flash('Invalid username or password.', 'danger')
        return render_template('login.html')

    # Logout route
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('Logged out.', 'info')
        return redirect(url_for('login'))

    # Profile/dashboard route
    @app.route('/')
    @login_required
    def profile():
        # Query top 10 leaderboard by beer_count
        leaderboard = UserTable.query.order_by(UserTable.beer_count.desc()).limit(10).all()
        return render_template(
            'profile.html',
            username=current_user.username,
            major=current_user.major,
            beer_count=current_user.beer_count,
            money_spent=current_user.money_spent,
            leaderboard=leaderboard
        )

    # Drink endpoint
    @app.route('/drink', methods=['POST'])
    @login_required
    def drink():
        current_user.beer_count += 1
        current_user.money_spent += 5.0
        db.session.commit()
        flash('Enjoy your beer!', 'success')
        return redirect(url_for('profile'))
    
    @app.route('/deleteUser', methods=['POST'])  
    @login_required
    def deleteUser():
        user = current_user._get_current_object()
        logout_user()
        db.session.delete(user)
        db.session.commit()
        flash('Your account has been deleted.', 'info')
        return redirect(url_for('login'))


    return app