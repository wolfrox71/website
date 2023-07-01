from flask import Blueprint, session

login_bp = Blueprint("login_bp", __name__)


@login_bp.route("/")
def index():
    return "Login blueprint home"