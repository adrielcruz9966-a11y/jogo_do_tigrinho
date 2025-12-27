from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, current_user
import os

app = Flask(__name__)

# =====================
# Configurações
# =====================
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "password")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///local.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# =====================
# Extensões
# =====================
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

# =====================
# Models
# =====================
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))

class GameResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Integer)
    user_id = db.Column(db.Integer)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# =====================
# Rotas
# =====================
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chart-data")
def chart_data():
    return jsonify({
        "x": [1, 2, 3, 4],
        "y": [100, 80, 60, 40]
    })
