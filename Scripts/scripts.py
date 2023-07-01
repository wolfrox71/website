from flask import Blueprint, render_template

scripts_bp = Blueprint("script_bp", __name__, template_folder="templates")

@scripts_bp.route("/")
def index():
    return render_template("home.html", scripts=["a","b","c"])

@scripts_bp.route("<id>")
def script(id):
    return id