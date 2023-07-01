from flask import Blueprint, session, redirect, url_for

login_bp = Blueprint("login_bp", __name__)


@login_bp.route("/")
def index():
    isLoggedIn: bool = "sessionID" in session and session["sessionID"] is not None
    return str(isLoggedIn) 

@login_bp.route("/login")
def login():
    session["sessionID"] = "a"
    return redirect(url_for("home_bp.index"))

@login_bp.route("/logout")
def logout():
    del session["sessionID"]
    return redirect(url_for("home_bp.index"))