from flask import Blueprint

from User.Login.login import login_bp

user_bp = Blueprint("user_bp", __name__)

user_bp.register_blueprint(login_bp, url_prefix="/login")

@user_bp.route("/")
def index():
    return "User blueprint home"