# app.py
import os
from flask import Flask
from extensions import db
from models.userTable import UserTable   # we’ll fix import order below

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "SQLALCHEMY_DATABASE_URI",
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@"
        f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # bind our single db instance to this app
    db.init_app(app)

    # now that db is bound, we can import any blueprints/models that reference it
    from models.userTable import UserTable
    from controllers.todo import bp as todo_bp
    from controllers.category import bp as category_bp

    app.register_blueprint(todo_bp)
    app.register_blueprint(category_bp)

    # create tables + seed
    with app.app_context():
        db.create_all()
        if not UserTable.query.filter_by(username="MrMikPik").first():
            u = UserTable(uid=3,username="MrMikPik", password="pik@example.com", major = "dat", money_spent=500,beer_count=5000)
            db.session.add(u)
            db.session.commit()

    @app.route("/")
    def hello_world():
        return "<p>Hello, World!</p>"

    return app

app = create_app()

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)
