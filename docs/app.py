from flask import Flask, render_template, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_required, logout_user, current_user
from flask_migrate import Migrate
import os

# =====================
# APP
# =====================
app = Flask(__name__)

# =====================
# CONFIG
# =====================
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "password")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL",
    "sqlite:///local.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# =====================
# EXTENSIONS
# =====================
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
migrate = Migrate(app, db)

# =====================
# MODELS
# =====================
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    balance = db.Column(db.Integer, default=1000)

class GameResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

# =====================
# LOGIN
# =====================
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# =====================
# ROUTES
# =====================
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login")
def login():
    return "Login em construção"

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/chart-data")
@login_required
def chart_data():
    results = GameResult.query.filter_by(
        user_id=current_user.id
    ).order_by(GameResult.timestamp).all()

    return jsonify({
        "x": list(range(len(results))),
        "y": [r.balance for r in results]
    })

# =====================
# RUN
# =====================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
