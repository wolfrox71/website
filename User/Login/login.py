from flask import Blueprint, session, redirect, url_for, render_template
import global_functions

login_bp = Blueprint("login_bp", __name__, template_folder="templates")


@login_bp.route("/")
def index():
    isLoggedIn: bool = global_functions.validSessionID()
    if isLoggedIn:
        status = ""
    else:
        status = "not "
    return render_template("login_home.html", status=status)

@login_bp.route("/login")
def login():
    session["sessionID"] = global_functions.generateSessionID()
    return redirect(url_for("home_bp.index"))

@login_bp.route("/logout")
def logout():
    del session["sessionID"]
    return redirect(url_for("home_bp.index"))